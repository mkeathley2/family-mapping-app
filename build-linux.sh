#!/bin/bash

echo "========================================"
echo "   Building Linux Standalone Package"
echo "========================================"
echo

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Build the executable
echo "Building Linux executable..."
pyinstaller family_mapping_app_linux.spec

if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

# Create package directory
echo "Creating package directory..."
rm -rf standalone-package-linux
mkdir standalone-package-linux

# Copy files
echo "Copying files..."
cp dist/FamilyMappingApp standalone-package-linux/
cp START_HERE.sh standalone-package-linux/
cp STANDALONE_README_LINUX.md standalone-package-linux/README.md
cp sample_family_addresses.csv standalone-package-linux/

# Make scripts executable
chmod +x standalone-package-linux/START_HERE.sh
chmod +x standalone-package-linux/FamilyMappingApp

# Create version info
echo "Creating version info..."
cat > standalone-package-linux/VERSION.txt << EOF
Family Mapping App - Standalone Version for Linux
Version: v0.0.4-standalone-linux
Build Date: $(date)

This package contains:
- FamilyMappingApp (Main application)
- START_HERE.sh (Run this script)
- README.md (Instructions)
- sample_family_addresses.csv (Example file)

No installation required - just run ./START_HERE.sh!
EOF

# Create tar.gz file (more common on Linux)
echo "Creating tar.gz file..."
rm -f family-mapping-app-standalone-linux-v0.0.4.tar.gz
tar -czf family-mapping-app-standalone-linux-v0.0.4.tar.gz standalone-package-linux/

echo
echo "========================================"
echo "   Linux Package Complete!"
echo "========================================"
echo
echo "Files created:"
echo "- standalone-package-linux/ (folder with all files)"
echo "- family-mapping-app-standalone-linux-v0.0.4.tar.gz (ready for distribution)"
echo
echo "The tar.gz file is ready to share with Linux users!"
echo "They just need to:"
echo "1. Download and extract: tar -xzf family-mapping-app-standalone-linux-v0.0.4.tar.gz"
echo "2. Run: cd standalone-package-linux && ./START_HERE.sh"
echo "3. Use the app in their browser"
echo 