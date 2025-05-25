#!/bin/bash

echo "========================================"
echo "   Family Mapping App - Stopping..."
echo "========================================"
echo

# Stop the application
if docker-compose down; then
    echo
    echo "========================================"
    echo "   App has been stopped successfully!"
    echo "========================================"
    echo
    echo "To start the app again, run: ./start-app.sh"
    echo
else
    echo
    echo "ERROR: Failed to stop the application!"
    echo "The app may not be running."
    echo
fi

read -p "Press Enter to continue..." 