#!/bin/bash
set -e

echo "Building Go Lambda function..."
GOOS=linux CGO_ENABLED=0 GOARCH=arm64 go build -tags lambda.norpc -o bootstrap main.go

echo "Creating deployment package..."
zip zip.zip bootstrap