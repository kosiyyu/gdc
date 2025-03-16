package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
	"github.com/aws/aws-sdk-go-v2/service/ecs"
)

type Response struct {
	StatusCode int    `json:"statusCode"`
	Body       string `json:"body"`
}

func handleRequest(ctx context.Context, _ json.RawMessage) (Response, error) {
	cluster := "minecraft-cluster"
	service := "mincraft-server-service"

	cfg, err := config.LoadDefaultConfig(ctx,
		config.WithRegion("eu-north-1"),
	)
	if err != nil {
		return Response{StatusCode: 500, Body: "Failed to load configuration"}, err
	}

	ecsClient := ecs.NewFromConfig(cfg)

	input := &ecs.DescribeServicesInput{
		Cluster:  &cluster,
		Services: []string{service},
	}

	result, err := ecsClient.DescribeServices(ctx, input)
	if err != nil {
		log.Printf("Failed to describe service: %v", err)
		return Response{StatusCode: 500, Body: "Failed to check container status: " + err.Error()}, err
	}

	if len(result.Services) == 0 {
		return Response{StatusCode: 404, Body: "Service not found"}, nil
	}

	srv := result.Services[0]
	if srv.RunningCount == 1 {
		privateIP, err := findPrivateIP(ctx, ecsClient, cluster, service)
		publicIP, err := findPublicIP(ctx, privateIP)
		if err != nil {
			return Response{StatusCode: 200, Body: "Container is running, but couldn't find ip"}, err
		}
		return Response{StatusCode: 200, Body: "Container is running using ip: " + publicIP}, nil
	} else if srv.RunningCount == 0 {
		return Response{StatusCode: 200, Body: "Container is not running"}, nil
	} else if srv.RunningCount > 1 {
		return Response{StatusCode: 500, Body: "Multiple containers are running"}, nil
	}

	return Response{StatusCode: 500, Body: "Internal server error"}, nil
}

func findPrivateIP(ctx context.Context, ecsClient *ecs.Client, cluster string, service string) (string, error) {
	listTasksInput := &ecs.ListTasksInput{
		Cluster:     &cluster,
		ServiceName: &service,
	}

	listTasksOutput, err := ecsClient.ListTasks(ctx, listTasksInput)
	if err != nil {
		log.Printf("ListTasks error: %v", err)
		return "", err
	}

	if len(listTasksOutput.TaskArns) == 0 {
		log.Printf("No tasks found")
		return "", nil
	}

	describeTasksInput := &ecs.DescribeTasksInput{
		Cluster: &cluster,
		Tasks:   listTasksOutput.TaskArns,
	}

	describeTasksOutput, err := ecsClient.DescribeTasks(ctx, describeTasksInput)
	if err != nil {
		log.Printf("DescribeTasks error: %v", err)
		return "", err
	}

	for _, task := range describeTasksOutput.Tasks {
		if task.LastStatus != nil && *task.LastStatus == "RUNNING" {
			if task.Containers != nil && len(task.Containers) > 0 {
				for _, container := range task.Containers {
					if container.NetworkInterfaces != nil && len(container.NetworkInterfaces) > 0 {
						publicIP := container.NetworkInterfaces[0].PrivateIpv4Address
						if publicIP != nil {
							log.Printf("Found IP: %s", *publicIP)
							return *publicIP, nil
						}
					}
				}
			}

			for _, attachment := range task.Attachments {
				if attachment.Type != nil && *attachment.Type == "ElasticNetworkInterface" {
					for _, detail := range attachment.Details {
						if detail.Name != nil && detail.Value != nil {
							if *detail.Name == "privateIPv4Address" {
								log.Printf("Found IP from attachment: %s", *detail.Value)
								return *detail.Value, nil
							}
						}
					}
				}
			}
		}
	}

	log.Printf("No IP found")
	return "", nil
}

func findPublicIP(ctx context.Context, privateIP string) (string, error) {
	cfg, err := config.LoadDefaultConfig(ctx,
		config.WithRegion("eu-north-1"),
	)
	if err != nil {
		return "", fmt.Errorf("failed to load AWS config: %v", err)
	}

	ec2Client := ec2.NewFromConfig(cfg)

	input := &ec2.DescribeNetworkInterfacesInput{
		Filters: []types.Filter{
			{
				Name:   aws.String("private-ip-address"),
				Values: []string{privateIP},
			},
		},
	}

	result, err := ec2Client.DescribeNetworkInterfaces(ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to describe network interfaces: %v", err)
	}

	if len(result.NetworkInterfaces) == 0 {
		return "", fmt.Errorf("no network interface found for private IP %s", privateIP)
	}

	networkInterface := result.NetworkInterfaces[0]
	if networkInterface.Association == nil || networkInterface.Association.PublicIp == nil {
		return "", fmt.Errorf("no public IP associated with private IP %s", privateIP)
	}

	publicIP := *networkInterface.Association.PublicIp
	return publicIP, nil
}

func main() {
	lambda.Start(handleRequest)
}
