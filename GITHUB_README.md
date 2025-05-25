# Family Mapping App 🗺️

An interactive web application for mapping family addresses with geocoding capabilities and CSV export functionality.

![Family Mapping App](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)
![Version](https://img.shields.io/badge/Version-v0.0.3-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 📍 **Interactive Map**: Upload CSV files with addresses and see them plotted on an interactive map
- 🌍 **Geocoding**: Automatic address-to-coordinates conversion using multiple geocoding services
- 📊 **Data Management**: View, edit, and manage your address data in a user-friendly interface
- 💾 **Export Options**: Download your geocoded data as CSV files
- 🔄 **Persistent Storage**: Your data is automatically saved and persists between sessions
- 🐳 **Docker Ready**: Easy deployment with Docker - no complex setup required

## 🚀 Quick Start (Recommended)

### Option 1: Download & Run (Easiest)

1. **Install Docker Desktop**:
   - **Windows/Mac**: Download from [docker.com](https://www.docker.com/products/docker-desktop)
   - Follow the installation wizard and start Docker Desktop

2. **Download the App**:
   - Go to [Releases](https://github.com/mkeathley75028/family-mapping-app/releases)
   - Download the latest `family-mapping-app-v*.zip` file
   - Extract it to a folder on your computer

3. **Run the Application**:
   - **Windows**: Double-click `start-app-hub.bat`
   - **Mac/Linux**: Open Terminal, navigate to the folder, run `./start-app-hub.sh`

4. **Access the App**:
   - Open your web browser
   - Go to: http://localhost:8765
   - Start uploading and mapping your addresses! 🎉

### Option 2: Docker Command Line

If you're comfortable with command line:

```bash
# Create a folder for your data
mkdir family-mapping-data
cd family-mapping-data

# Run the app
docker run -d \
  --name family-mapping-app \
  -p 8765:8765 \
  -v "$(pwd)/datasets:/app/datasets" \
  --restart unless-stopped \
  mkeathley75028/family-mapping-app:latest

# Open http://localhost:8765 in your browser
```

### Option 3: Clone & Build (For Developers)

```bash
git clone https://github.com/mkeathley75028/family-mapping-app.git
cd family-mapping-app

# Windows:
start-app.bat

# Mac/Linux:
./start-app.sh
```

## 📋 Requirements

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Web Browser** (Chrome, Firefox, Safari, Edge)
- **4GB RAM** minimum
- **1GB free disk space**

## 📁 Data Persistence

- Your data is automatically saved in a `datasets` folder
- This folder persists between app updates and restarts
- You can backup this folder to preserve your data
- When updating the app, your data will be preserved

## 🔄 Updating the App

### For Option 1 Users:
- Download and run the new start scripts from the latest release

### For Option 2 Users:
```bash
docker stop family-mapping-app
docker rm family-mapping-app
docker pull mkeathley75028/family-mapping-app:latest
# Then run the docker run command again
```

### For Option 3 Users:
```bash
git pull
# Windows: update-app.bat
# Mac/Linux: ./update-app.sh
```

## 🛠️ Troubleshooting

### Common Issues:

**"Docker is not running"**:
- Make sure Docker Desktop is installed and running
- Look for the Docker whale icon in your system tray/menu bar

**Port 8765 already in use**:
- Stop any existing containers: `docker stop family-mapping-app`
- Or restart your computer

**Permission errors**:
- Make sure you have admin/sudo privileges
- On Mac/Linux: `chmod +x *.sh`

**Can't access http://localhost:8765**:
- Wait a minute for the app to fully start
- Check if container is running: `docker ps`
- Check logs: `docker logs family-mapping-app`

## 🤝 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Make sure Docker Desktop is properly installed and running
3. Try restarting Docker Desktop
4. [Open an issue](https://github.com/mkeathley75028/family-mapping-app/issues) with specific error messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Flask and Leaflet.js
- Geocoding powered by multiple services for reliability
- Containerized with Docker for easy deployment

---

**Made with ❤️ for families who want to visualize their connections across the map** 