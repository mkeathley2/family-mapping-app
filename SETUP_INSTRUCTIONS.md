# Complete Docker Setup Instructions for mkeathley75028

## Prerequisites

### 1. Install Docker Desktop
1. Go to https://www.docker.com/products/docker-desktop
2. Download Docker Desktop for Windows
3. Run the installer and follow the setup wizard
4. **Important**: Make sure to enable WSL 2 integration if prompted
5. Restart your computer if required
6. Start Docker Desktop and wait for it to be ready (whale icon in system tray)

### 2. Verify Docker Installation
Open PowerShell or Command Prompt and run:
```bash
docker --version
docker ps
```
You should see version information and an empty container list.

## Step-by-Step Deployment

### Step 1: Login to Docker Hub
```bash
docker login
```
- Enter username: `mkeathley75028`
- Enter your Docker Hub password

### Step 2: Create Docker Hub Repository
1. Go to https://hub.docker.com
2. Click "Create Repository"
3. Repository name: `family-mapping-app`
4. Description: "Interactive family address mapping application with geocoding and CSV export"
5. Visibility: **Public** (so users can download easily)
6. Click "Create"

### Step 3: Build and Push Docker Image
Run these commands in your project directory:

```bash
# Build the image
docker build -t mkeathley75028/family-mapping-app:latest .

# Tag for version
docker tag mkeathley75028/family-mapping-app:latest mkeathley75028/family-mapping-app:v0.0.3

# Push to Docker Hub
docker push mkeathley75028/family-mapping-app:latest
docker push mkeathley75028/family-mapping-app:v0.0.3
```

### Step 4: Test Your Docker Image
```bash
# Test locally
docker run -d --name test-app -p 8765:8765 mkeathley75028/family-mapping-app:latest

# Check if it's running
docker ps

# Test in browser: http://localhost:8765

# Stop test
docker stop test-app
docker rm test-app
```

### Step 5: Create Release Package for Users
```bash
# Run the release package script
create-release-package.bat
```

This will create a `release-package` folder with all the files users need.

### Step 6: Upload to GitHub Releases
1. Go to your GitHub repository: https://github.com/mkeathley75028/family-mapping-app
2. Click "Releases" → "Create a new release"
3. Tag version: `v0.0.3`
4. Release title: `Family Mapping App v0.0.3 - Docker Release`
5. Description:
```markdown
# Family Mapping App v0.0.3 - Docker Release

## What's New
- Docker containerization for easy deployment
- Cross-platform support (Windows, Mac, Linux)
- Simplified installation process
- Data persistence between updates

## Quick Start
1. Install Docker Desktop
2. Download and extract the release files
3. Run the start script for your platform
4. Open http://localhost:8765

See README.md for detailed instructions.
```
6. Attach the `release-package` folder as a ZIP file
7. Click "Publish release"

## For Future Updates

When you want to release a new version:

```bash
# Update version in your code
# Build new version
docker build -t mkeathley75028/family-mapping-app:v0.0.4 .
docker tag mkeathley75028/family-mapping-app:v0.0.4 mkeathley75028/family-mapping-app:latest

# Push new version
docker push mkeathley75028/family-mapping-app:v0.0.4
docker push mkeathley75028/family-mapping-app:latest

# Create new release package
create-release-package.bat

# Upload to GitHub releases
```

## User Instructions Summary

Your users will need to:

### Windows Users:
1. Install Docker Desktop
2. Download your release ZIP
3. Extract files
4. Double-click `start-app-hub.bat`
5. Open browser to http://localhost:8765

### Mac/Linux Users:
1. Install Docker Desktop
2. Download your release ZIP
3. Extract files
4. Open Terminal in the folder
5. Run `./start-app-hub.sh`
6. Open browser to http://localhost:8765

## Troubleshooting

### If Docker commands don't work:
1. Make sure Docker Desktop is running (whale icon in system tray)
2. Restart Docker Desktop
3. Restart your computer
4. Try running PowerShell as Administrator

### If build fails:
1. Make sure you're in the correct directory (with Dockerfile)
2. Check that all files are present
3. Make sure Docker has enough disk space

### If push fails:
1. Make sure you're logged in: `docker login`
2. Check your internet connection
3. Verify repository name is correct

## Benefits for Your Users

✅ **Easy Installation**: Just install Docker and run a script
✅ **Cross-Platform**: Works on Windows, Mac, and Linux
✅ **No Python Setup**: Everything is containerized
✅ **Data Persistence**: User data survives updates
✅ **Automatic Updates**: Users can easily get new versions
✅ **Isolated Environment**: Won't conflict with other software

## Next Steps

1. Install Docker Desktop
2. Follow the steps above to build and push your image
3. Test the user experience yourself
4. Create the GitHub release
5. Share with your users!

Your app will be available as: `mkeathley75028/family-mapping-app:latest` 