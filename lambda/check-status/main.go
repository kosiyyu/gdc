package checkstatus

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

func handleRequest(ctx context.Context, _ json.RawMessage) Response {
	cluster := "your-cluster-name"
	service := "your-service-name"

	cfg, err := config.LoadDefaultConfig(ctx,
		config.WithRegion("eu-north-1"),
	)
	if err != nil {
		return Response{StatusCode: 500, Body: "Failed to load configurationt"}
	}

	ecsClient := ecs.NewFromConfig(cfg)

	input := &ecs.DescribeServicesInput{
		Cluster:  &cluster,
		Services: []string{service},
	}

	result, err := ecsClient.DescribeServices(ctx, input)
	if err != nil {
		log.Printf("Failed to describe service: %v", err)
		return Response{StatusCode: 500, Body: "Failed to check container status: " + err.Error()}
	}

	if len(result.Services) == 0 {
		return Response{StatusCode: 404, Body: "Service not found"}
	}

	srv := result.Services[0]
	if srv.RunningCount == 1 {
		return Response{
			StatusCode: 200,
			Body:       "Container is running",
		}
	} else if srv.RunningCount == 0 {
		return Response{
			StatusCode: 200,
			Body:       "Container is not running",
		}
	} else if srv.RunningCount > 1 {
		return Response{
			StatusCode: 500,
			Body:       "Multiple containers are running",
		}
	}

	return Response{
		StatusCode: 500,
		Body:       "Internal server error",
	}
}

func main() {
	lambda.Start(handleRequest)
}
