package main

import (
	"context"
	"encoding/json"
	"log"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go-v2/config"
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
		return Response{StatusCode: 200, Body: "Container is running"}, nil
	} else if srv.RunningCount == 0 {
		return Response{StatusCode: 200, Body: "Container is not running"}, nil
	} else if srv.RunningCount > 1 {
		return Response{StatusCode: 500, Body: "Multiple containers are running"}, nil
	}

	return Response{StatusCode: 500, Body: "Internal server error"}, nil
}

func main() {
	lambda.Start(handleRequest)
}
