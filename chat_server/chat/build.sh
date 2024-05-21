#!/bin/bash

# Set the image name (replace with your actual image name)
IMAGE_NAME="chat-image"

echo "Building Docker image..."
docker build -t $IMAGE_NAME .

if [ $? -eq 0 ]; then
  echo "Build successful."
else
  echo "Error: Docker image build failed."
fi