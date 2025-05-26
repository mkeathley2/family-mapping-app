#!/bin/bash

echo "========================================"
echo "   Family Mapping App - Standalone"
echo "========================================"
echo
echo "Starting the Family Mapping App..."
echo "This may take a moment to load."
echo
echo "Your web browser will open automatically."
echo "If it doesn't, go to: http://localhost:8765"
echo
echo "To stop the app, press Ctrl+C in this terminal."
echo "========================================"
echo

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Make the executable file executable (in case it's not)
chmod +x "./FamilyMappingApp"

# Run the application
"./FamilyMappingApp"

echo
echo "Application has stopped."
read -p "Press Enter to close this terminal..." 