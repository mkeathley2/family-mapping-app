#!/bin/bash

echo "========================================"
echo "   Family Mapping App - Stopping..."
echo "========================================"
echo

# Stop and remove the container
if docker stop family-mapping-app && docker rm family-mapping-app; then
    echo
    echo "========================================"
    echo "   App has been stopped successfully!"
    echo "========================================"
    echo
    echo "To start the app again, run: ./start-app-hub.sh"
    echo
    echo "Your data in the 'datasets' folder has been preserved."
    echo
else
    echo
    echo "ERROR: Failed to stop the application!"
    echo "The app may not be running."
    echo
fi

read -p "Press Enter to continue..." 