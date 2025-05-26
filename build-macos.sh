#!/bin/bash

echo "========================================"
echo "   Building macOS Standalone Package"
echo "========================================"
echo

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Build the executable
echo "Building macOS executable..."
pyinstaller family_mapping_app_macos.spec

if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

# Create package directory
echo "Creating package directory..."
rm -rf standalone-package-macos
mkdir standalone-package-macos

# Copy files
echo "Copying files..."
cp dist/FamilyMappingApp standalone-package-macos/
cp START_HERE.sh standalone-package-macos/
cp STANDALONE_README_MACOS.md standalone-package-macos/README.md
cp sample_family_addresses.csv standalone-package-macos/

# Make scripts executable
chmod +x standalone-package-macos/START_HERE.sh
chmod +x standalone-package-macos/FamilyMappingApp

# Create version info
echo "Creating version info..."
cat > standalone-package-macos/VERSION.txt << EOF
Family Mapping App - Standalone Version for macOS
Version: v0.0.4-standalone-macos
Build Date: $(date)

This package contains:
- FamilyMappingApp (Main application)
- START_HERE.sh (Double-click to run)
- README.md (Instructions)
- sample_family_addresses.csv (Example file)

No installation required - just double-click START_HERE.sh!
EOF

# Create zip file
echo "Creating zip file..."
rm -f family-mapping-app-standalone-macos-v0.0.4.zip
zip -r family-mapping-app-standalone-macos-v0.0.4.zip standalone-package-macos/

echo
echo "========================================"
echo "   macOS Package Complete!"
echo "========================================"
echo
echo "Files created:"
echo "- standalone-package-macos/ (folder with all files)"
echo "- family-mapping-app-standalone-macos-v0.0.4.zip (ready for distribution)"
echo
echo "The zip file is ready to share with macOS users!"
echo "They just need to:"
echo "1. Download and extract the zip"
echo "2. Double-click START_HERE.sh"
echo "3. Use the app in their browser"
echo 