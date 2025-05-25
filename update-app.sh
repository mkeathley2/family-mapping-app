#!/bin/bash

echo "========================================"
echo "   Family Mapping App - Updating..."
echo "========================================"
echo

# Check if Docker is running
if ! docker version >/dev/null 2>&1; then
    echo "ERROR: Docker is not running or not installed!"
    echo "Please install Docker Desktop and make sure it's running."
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Stopping current version..."
docker-compose down

echo
echo "Pulling latest code from GitHub..."
if ! git pull origin main; then
    echo
    echo "ERROR: Failed to pull updates from GitHub!"
    echo "Make sure you have git installed and internet connection."
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

echo
echo "Rebuilding application with updates..."
docker-compose build --no-cache

echo
echo "Starting updated application..."
if docker-compose up -d; then
    echo
    echo "========================================"
    echo "   UPDATE SUCCESSFUL!"
    echo "========================================"
    echo
    echo "Your app has been updated to the latest version."
    echo "Open your web browser and go to:"
    echo "   http://localhost:8765"
    echo
    echo "Your data has been preserved during the update."
    echo
else
    echo
    echo "ERROR: Failed to start the updated application!"
    echo "Please check the error messages above."
    echo
fi

read -p "Press Enter to continue..." 