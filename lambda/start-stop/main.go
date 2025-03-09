package main

import (
	"context"
	"encoding/json"
	"log"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ecs"
)

type Request struct {
	Command string `json:"command"`
}

type Response struct {
	StatusCode int    `json:"statusCode"`
	Body       string `json:"body"`
}

func handleRequest(ctx context.Context, event json.RawMessage) (Response, error) {
	cluster := "minecraft-cluster"
	service := "mincraft-server-service"

	var request Request
	err := json.Unmarshal(event, &request)
	if err != nil {
		log.Printf("Failed to unmarshal event: %v", err)
		return Response{StatusCode: 400, Body: "Invalid request"}, err
	}

	cfg, err := config.LoadDefaultConfig(ctx,
		config.WithRegion("eu-north-1"),
	)
	if err != nil {
		return Response{StatusCode: 500, Body: "Failed to load configuration"}, err
	}

	ecsClient := ecs.NewFromConfig(cfg)

	var desiredCount int32
	if request.Command == "Start" {
		desiredCount = 1
	} else if request.Command == "Stop" {
		desiredCount = 0
	} else {
		return Response{StatusCode: 400, Body: "Invalid command. Use 'Start' or 'Stop'"}, nil
	}

	input := &ecs.UpdateServiceInput{
		Cluster:      &cluster,
		Service:      &service,
		DesiredCount: &desiredCount,
	}

	_, err = ecsClient.UpdateService(ctx, input)
	if err != nil {
		log.Printf("Failed to update service: %v", err)
		return Response{StatusCode: 500, Body: "Failed to update container"}, err
	}

	if request.Command == "Start" {
		return Response{StatusCode: 200, Body: "Container started."}, nil
	} else if request.Command == "Stop" {
		return Response{StatusCode: 200, Body: "Container stopped."}, nil
	}

	return Response{StatusCode: 500, Body: "Internal server error"}, nil

}

func main() {
	lambda.Start(handleRequest)
}
