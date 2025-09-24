#!/bin/bash
# ./start_containers.sh

# Path to the .env file
ENV_FILE="./dev.env"

# Check if the file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found!"
    exit 1
fi

# Stop and remove any existing containers
echo "Stopping and removing existing containers..."
docker compose --env-file $ENV_FILE down

# Rebuild the images without cache
echo "Building Docker images..."
docker compose --env-file $ENV_FILE build --no-cache

# Start the containers in the background
echo "Starting containers..."
docker compose --env-file $ENV_FILE up -d

# Show the status of the containers
echo "Containers status:"
docker compose --env-file $ENV_FILE ps
