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

# Check if docker-compose is available
if ! docker-compose version >/dev/null 2>&1; then
    echo "ERROR: docker-compose is not available!"
    echo "Please make sure Docker Desktop is properly installed."
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Starting Family Mapping App..."
echo "This may take a few minutes the first time (downloading dependencies)"
echo

# Start the application
if docker-compose up -d; then
    echo
    echo "========================================"
    echo "   SUCCESS! App is now running!"
    echo "========================================"
    echo
    echo "Open your web browser and go to:"
    echo "   http://localhost:8765"
    echo
    echo "To stop the app, run: ./stop-app.sh"
    echo
    echo "The app will continue running in the background"
    echo "until you stop it or restart your computer."
    echo
else
    echo
    echo "ERROR: Failed to start the application!"
    echo "Please check the error messages above."
    echo
fi

read -p "Press Enter to continue..." 