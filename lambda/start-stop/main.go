package startstop

import (
	"context"
	"encoding/json"
	"log"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ecs"
)

type Request struct {
	Command    string `json:"command"`
	InstanceId string `json:"instance_id"`
}

type Response struct {
	StatusCode int    `json:"statusCode"`
	Body       string `json:"body"`
}

func handleRequest(ctx context.Context, event json.RawMessage) Response {
	// todo, load
	cluster := ""
	service := ""

	var request Request
	err := json.Unmarshal(event, &request)
	if err != nil {
		log.Printf("Failed to unmarshal event: %v", err)
		return Response{StatusCode: 400, Body: "Invalid request"}
	}

	cfg, err := config.LoadDefaultConfig(ctx,
		config.WithRegion("eu-north-1"),
	)
	if err != nil {
		return Response{StatusCode: 500, Body: "Failed to load configurationt"}
	}

	ecsClient := ecs.NewFromConfig(cfg)

	var desiredCount int32
	if request.Command == "Start" {
		desiredCount = 1
	} else if request.Command == "Stop" {
		desiredCount = 0
	} else {
		return Response{StatusCode: 400, Body: "Invalid command. Use 'Start' or 'Stop'"}
	}

	input := &ecs.UpdateServiceInput{
		Cluster:      &cluster,
		Service:      &service,
		DesiredCount: &desiredCount,
	}

	_, err = ecsClient.UpdateService(ctx, input)
	if err != nil {
		log.Printf("Failed to update service: %v", err)
		return Response{StatusCode: 500, Body: "Failed to update container"}
	}

	if request.Command == "Start" {
		return Response{StatusCode: 200, Body: "Container started."}
	} else if request.Command == "Stop" {
		return Response{StatusCode: 200, Body: "Container stoped."}
	}

	return Response{StatusCode: 500, Body: "Internal server error"}

}

func main() {
	lambda.Start(handleRequest)
}
