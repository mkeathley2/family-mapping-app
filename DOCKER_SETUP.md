# Family Mapping App - Docker Setup Guide

## For You (Developer) - Docker Hub Setup

### 1. Docker Hub Account Setup
You already have a Docker Hub account with username `mkeathley75028`. Here's what you need to do:

1. **Login to Docker Hub**: Go to https://hub.docker.com and sign in
2. **Create Repository**: 
   - Click "Create Repository"
   - Repository name: `family-mapping-app`
   - Description: "Interactive family address mapping application with geocoding and CSV export"
   - Visibility: Public (so users can download it easily)
   - Click "Create"

### 2. Build and Push to Docker Hub

Run these commands in your project directory:

```bash
# Login to Docker Hub (you'll be prompted for password)
docker login

# Build the Docker image
docker build -t mkeathley75028/family-mapping-app:latest .

# Tag for versioning (replace with actual version)
docker tag mkeathley75028/family-mapping-app:latest mkeathley75028/family-mapping-app:v0.0.3

# Push to Docker Hub
docker push mkeathley75028/family-mapping-app:latest
docker push mkeathley75028/family-mapping-app:v0.0.3
```

### 3. Update Version Numbers

When you release new versions:

```bash
# Build new version
docker build -t mkeathley75028/family-mapping-app:v0.0.4 .
docker tag mkeathley75028/family-mapping-app:v0.0.4 mkeathley75028/family-mapping-app:latest

# Push new version
docker push mkeathley75028/family-mapping-app:v0.0.4
docker push mkeathley75028/family-mapping-app:latest
```

## For Your Users - Installation Instructions

### Option 1: Simple Download & Run (Recommended for non-technical users)

1. **Install Docker Desktop**:
   - Windows/Mac: Download from https://www.docker.com/products/docker-desktop
   - Follow the installation wizard
   - Start Docker Desktop and wait for it to be ready

2. **Download Start Scripts**:
   - Go to: https://github.com/mkeathley75028/family-mapping-app/releases
   - Download the latest release
   - Extract the files to a folder on your computer

3. **Run the Application**:
   - **Windows**: Double-click `start-app-hub.bat`
   - **Mac/Linux**: Open Terminal, navigate to the folder, run `./start-app-hub.sh`

4. **Access the App**:
   - Open your web browser
   - Go to: http://localhost:8765
   - Start uploading and mapping your addresses!

### Option 2: Clone Repository (For technical users)

```bash
# Clone the repository
git clone https://github.com/mkeathley75028/family-mapping-app.git
cd family-mapping-app

# Start the application
# Windows:
start-app.bat

# Mac/Linux:
./start-app.sh
```

## Data Persistence

- Your data is automatically saved in a `datasets` folder
- This folder persists between app updates and restarts
- You can backup this folder to preserve your data
- When updating the app, your data will be preserved

## Updating the App

### For Users:
- **Option 1 Users**: Just download and run the new start scripts
- **Option 2 Users**: Run the update script:
  - Windows: `update-app.bat`
  - Mac/Linux: `./update-app.sh`

## Troubleshooting

### Common Issues:

1. **"Docker is not running"**:
   - Make sure Docker Desktop is installed and running
   - Look for the Docker whale icon in your system tray/menu bar

2. **Port 8765 already in use**:
   - Stop any existing containers: `docker stop family-mapping-app`
   - Or restart your computer

3. **Permission errors**:
   - Make sure you have admin/sudo privileges
   - On Mac/Linux, you might need to run: `chmod +x *.sh`

4. **Can't access http://localhost:8765**:
   - Wait a minute for the app to fully start
   - Check if Docker container is running: `docker ps`
   - Check Docker logs: `docker logs family-mapping-app`

## Support

If users have issues:
1. Check the troubleshooting section above
2. Make sure Docker Desktop is properly installed and running
3. Try restarting Docker Desktop
4. Contact you for support with specific error messages 