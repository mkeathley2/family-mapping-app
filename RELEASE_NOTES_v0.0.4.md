# Family Mapping App v0.0.4 🎉

## 🚀 Major Update: Standalone Version Added!

Now you can choose between **two easy ways** to run the Family Mapping App:

### ⭐ NEW: Standalone Version (No Installation Required!)
Perfect for **non-technical users** who just want to map their family addresses immediately!

- **✅ Zero Installation** - No Docker, Python, or any software needed
- **✅ One-Click Start** - Just double-click and go!
- **✅ Windows Ready** - Works on Windows 10 and newer
- **✅ 12MB Download** - Compact and fast
- **✅ Offline Processing** - Your data stays on your computer

### 🐳 Docker Version (For Technical Users)
The original containerized version with all the advanced features.

## 📦 What's New in v0.0.4

### ✨ New Features
- **🆕 Standalone Executable** - No installation required version
- **🎯 Simplified Interface** - Streamlined for ease of use
- **📱 Auto-Browser Launch** - Opens your browser automatically
- **📁 Smart File Detection** - Automatically finds address columns
- **🔒 Enhanced Privacy** - All processing happens locally

### 🛠️ Improvements
- **⚡ Faster Startup** - Optimized loading times
- **🧠 Better Error Handling** - Clearer error messages
- **📊 Improved CSV Support** - Better column detection
- **🗺️ Enhanced Mapping** - Smoother map interactions

## 🚀 Quick Start Options

### Option 1: Standalone (Recommended for Most Users) ⭐
1. Download `family-mapping-app-standalone-v0.0.4.zip`
2. Extract the files
3. Double-click `START_HERE.bat`
4. Your browser opens automatically - start mapping!

**Requirements**: Windows 10+, Internet connection

### Option 2: Docker (For Advanced Users)
1. Download `family-mapping-app-v0.0.4.zip`
2. Install Docker Desktop
3. Run the start script for your OS
4. Access at http://localhost:8765

**Requirements**: Docker Desktop, 4GB RAM

## 📋 System Requirements

### Standalone Version
- Windows 10 or newer
- 4GB RAM minimum
- Internet connection (for geocoding)
- 50MB free disk space

### Docker Version
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- 4GB RAM minimum
- 1GB free disk space
- Modern web browser

## 🔧 Technical Details

### Standalone Version
- **Size**: ~12MB executable
- **Technology**: PyInstaller + Flask
- **Geocoding**: OpenStreetMap Nominatim
- **Port**: 8765 (localhost only)
- **Data Storage**: Local `datasets` folder

### Docker Version
- **Image**: `mkeathley75028/family-mapping-app:v0.0.4`
- **Size**: ~762MB
- **Technology**: Docker + Flask
- **Features**: Full feature set with advanced options

## 🐛 Bug Fixes
- Fixed CSV delimiter detection
- Improved geocoding reliability
- Better error messages for file uploads
- Enhanced browser compatibility

## 🔄 Upgrading

### From v0.0.3 Standalone Users:
- Download the new standalone version
- Your data in the `datasets` folder will be preserved

### From v0.0.3 Docker Users:
- Download new start scripts OR pull the latest Docker image
- Your data will be preserved automatically

## 🙏 Support

**Need help?**
1. Check the README.md for troubleshooting
2. Make sure you meet the system requirements
3. Try the standalone version if Docker gives you trouble
4. Open an issue with specific error messages

## 📚 Documentation

- **Standalone Users**: See README.md in the standalone package
- **Docker Users**: See main README.md in the repository
- **Developers**: Check the source code and build scripts

---

**🎯 Choose Your Adventure:**
- **Just want to map addresses?** → Download the Standalone version
- **Want full features and updates?** → Use the Docker version
- **Want to contribute or customize?** → Clone the repository

**Made with ❤️ for families who want to visualize their connections across the map** 🗺️ 