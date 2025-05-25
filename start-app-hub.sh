#!/bin/bash

echo "========================================"
echo "   Family Mapping App - Starting..."
echo "========================================"
echo

# Check if Docker is running
if ! docker version >/dev/null 2>&1; then
    echo "ERROR: Docker is not running or not installed!"
    echo "Please install Docker Desktop and make sure it's running."
    echo "Download from: https://www.docker.com/products/docker-desktop"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Docker is running - Good!"
echo

# Create datasets directory if it doesn't exist
if [ ! -d "datasets" ]; then
    echo "Creating datasets directory..."
    mkdir -p datasets
fi

echo "Starting Family Mapping App..."
echo "This may take a few minutes the first time (downloading application)"
echo

# Stop any existing container
docker stop family-mapping-app >/dev/null 2>&1
docker rm family-mapping-app >/dev/null 2>&1

# Pull latest image and run
if docker run -d \
    --name family-mapping-app \
    -p 8765:8765 \
    -v "$(pwd)/datasets:/app/datasets" \
    --restart unless-stopped \
    mkeathley75028/family-mapping-app:latest; then
    
    echo
    echo "========================================"
    echo "   SUCCESS! App is now running!"
    echo "========================================"
    echo
    echo "Open your web browser and go to:"
    echo "   http://localhost:8765"
    echo
    echo "To stop the app, run: ./stop-app-hub.sh"
    echo
    echo "The app will continue running in the background"
    echo "until you stop it or restart your computer."
    echo
    echo "Your data will be saved in the 'datasets' folder."
    echo
else
    echo
    echo "ERROR: Failed to start the application!"
    echo "Please check the error messages above."
    echo
fi

read -p "Press Enter to continue..." 