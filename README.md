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
- 💻 **Standalone Version**: No installation required - just download and run!

## 🚀 Quick Start (Choose Your Option)

### Option 1: Standalone Version (Easiest - No Installation Required!) ⭐

**Perfect for non-technical users who just want to run the app immediately**

1. **Download the Standalone Version**:
   - Go to [Releases](https://github.com/mkeathley2/family-mapping-app/releases)
   - Download `family-mapping-app-standalone-v*.zip`
   - Extract the zip file to a folder on your computer

2. **Run the App**:
   - **Double-click** `START_HERE.bat`
   - Wait for the app to start (may take a moment)
   - Your web browser will open automatically to the app

3. **Use the App**:
   - Upload your CSV file with family addresses
   - See them mapped automatically!
   - Download results with coordinates

**Requirements**: Windows 10+, Internet connection. That's it! 🎉

### Option 2: Docker Version (For Technical Users)

**Best for developers or users who want the latest features**

1. **Install Docker Desktop**:
   - **Windows/Mac**: Download from [docker.com](https://www.docker.com/products/docker-desktop)
   - Follow the installation wizard and start Docker Desktop

2. **Download the App**:
   - Go to [Releases](https://github.com/mkeathley2/family-mapping-app/releases)
   - Download the latest `family-mapping-app-v*.zip` file
   - Extract it to a folder on your computer

3. **Run the Application**:
   - **Windows**: Double-click `start-app-hub.bat`
   - **Mac/Linux**: Open Terminal, navigate to the folder, run `./start-app-hub.sh`

4. **Access the App**:
   - Open your web browser
   - Go to: http://localhost:8765
   - Start uploading and mapping your addresses! 🎉

### Option 3: Docker Command Line

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

### Option 4: Clone & Build (For Developers)

```bash
git clone https://github.com/mkeathley2/family-mapping-app.git
cd family-mapping-app

# Windows:
start-app.bat

# Mac/Linux:
./start-app.sh
```

## 📋 Requirements

### Standalone Version
- **Windows 10 or newer**
- **Internet connection** (for geocoding and map tiles)
- **4GB RAM** minimum

### Docker Version
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

### For Standalone Users:
- Download the new standalone version from releases
- Extract and run - your data in the `datasets` folder will be preserved

### For Docker Users:
- Download and run the new start scripts from the latest release

### For Command Line Users:
```bash
docker stop family-mapping-app
docker rm family-mapping-app
docker pull mkeathley75028/family-mapping-app:latest
# Then run the docker run command again
```

### For Developers:
```bash
git pull
# Windows: update-app.bat
# Mac/Linux: ./update-app.sh
```

## 🛠️ Troubleshooting

### Standalone Version Issues:

**App won't start?**
- Make sure you're running Windows 10 or newer
- Try right-clicking `START_HERE.bat` and selecting "Run as administrator"

**Browser doesn't open?**
- Manually open your web browser and go to: http://localhost:8765

### Docker Version Issues:

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
2. Make sure you have the minimum system requirements
3. Try restarting the app or your computer
4. [Open an issue](https://github.com/mkeathley2/family-mapping-app/issues) with specific error messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Flask and Leaflet.js
- Geocoding powered by OpenStreetMap's Nominatim service
- Containerized with Docker for easy deployment
- Standalone version created with PyInstaller

---

**Made with ❤️ for families who want to visualize their connections across the map** 