# Family Mapping App v0.0.5 🎉

## 🌍 Major Update: Cross-Platform Standalone Support!

We're excited to announce **full cross-platform support** for the Family Mapping App! Now available for **Windows**, **macOS**, and **Linux** users with no installation required.

### 🆕 What's New in v0.0.5

#### ✨ Cross-Platform Standalone Versions
- **🪟 Windows**: Enhanced Windows support with improved compatibility
- **🍎 macOS**: Brand new native macOS support with security guidance
- **🐧 Linux**: New Linux support for all major distributions
- **🤖 Automated Builds**: GitHub Actions automatically builds all platforms

#### 🛠️ Platform-Specific Improvements
- **Smart Platform Detection**: App automatically detects your operating system
- **Native Start Scripts**: Platform-appropriate launchers for each OS
- **Tailored Documentation**: OS-specific README files with troubleshooting
- **Better Error Handling**: Platform-aware error messages and guidance

#### 🔧 Technical Enhancements
- **Improved Path Handling**: Better cross-platform file system compatibility
- **Enhanced Security**: macOS Gatekeeper compatibility and Linux permissions
- **Optimized Builds**: Smaller, faster executables for each platform
- **Better Dependencies**: Streamlined requirements for each OS

## 📦 Available Downloads

### Standalone Versions (No Installation Required!)

#### 🪟 Windows Users
- **File**: `family-mapping-app-standalone-windows-v0.0.5.zip`
- **Size**: ~12MB
- **Requirements**: Windows 10+
- **How to Run**: Extract → Double-click `START_HERE.bat`

#### 🍎 macOS Users  
- **File**: `family-mapping-app-standalone-macos-v0.0.5.zip`
- **Size**: ~15MB
- **Requirements**: macOS 10.14+
- **How to Run**: Extract → Double-click `START_HERE.sh`
- **Note**: May require security approval on first run

#### 🐧 Linux Users
- **File**: `family-mapping-app-standalone-linux-v0.0.5.tar.gz`
- **Size**: ~14MB  
- **Requirements**: Ubuntu 18.04+, Fedora 30+, or equivalent
- **How to Run**: Extract → Run `./START_HERE.sh` in terminal

### Docker Version (For Advanced Users)
- **File**: `family-mapping-app-v0.0.5.zip`
- **Image**: `mkeathley75028/family-mapping-app:v0.0.5`
- **Full feature set with Docker deployment**

## 🚀 Quick Start Guide

### For First-Time Users:
1. **Choose your platform** from the downloads above
2. **Download and extract** the appropriate file
3. **Run the start script** for your OS
4. **Upload your CSV** with family addresses
5. **See your family mapped** on an interactive map!

### For Existing Users:
- Your data in the `datasets` folder will be preserved
- Simply download the new version for your platform
- No need to migrate or convert anything

## 🛠️ Platform-Specific Notes

### 🪟 Windows
- **Antivirus**: Some antivirus software may flag the executable initially
- **Permissions**: Run as administrator if you encounter issues
- **Compatibility**: Tested on Windows 10 and Windows 11

### 🍎 macOS
- **Security**: First run requires approval in System Preferences > Security & Privacy
- **Gatekeeper**: Right-click and "Open" to bypass initial security warnings
- **Compatibility**: Tested on macOS 10.14 through macOS 14 (Sonoma)

### 🐧 Linux
- **Distributions**: Tested on Ubuntu, Fedora, Debian, and CentOS
- **Dependencies**: Most modern distributions work out of the box
- **Permissions**: Scripts automatically set executable permissions

## 🔧 Technical Details

### Build System
- **PyInstaller**: Cross-platform executable generation
- **GitHub Actions**: Automated builds for all platforms
- **Spec Files**: Platform-optimized build configurations
- **Dependencies**: Minimal runtime requirements

### Security & Privacy
- **Local Processing**: All data stays on your computer
- **No Telemetry**: No usage tracking or data collection
- **Open Source**: Full source code available for review
- **Geocoding**: Only addresses sent to OpenStreetMap for coordinate lookup

## 🐛 Bug Fixes
- Fixed CSV delimiter detection across platforms
- Improved error handling for file permissions
- Better browser auto-launch on all platforms
- Enhanced geocoding reliability and rate limiting

## 🔄 Upgrading

### From v0.0.4:
- Download the new version for your platform
- Your existing data will be preserved automatically
- No migration steps required

### From Earlier Versions:
- Backup your `datasets` folder (optional)
- Download the new standalone version
- Extract and run - data will be preserved

## 🤝 Community & Support

### Getting Help:
1. Check the platform-specific README files
2. Review troubleshooting sections for your OS
3. [Open an issue](https://github.com/mkeathley2/family-mapping-app/issues) with details
4. Include your OS version and error messages

### Contributing:
- **Bug Reports**: Help us improve cross-platform compatibility
- **Feature Requests**: Suggest platform-specific enhancements
- **Testing**: Try the app on different OS versions
- **Documentation**: Help improve platform-specific guides

## 🎯 What's Next?

### Planned for v0.0.6:
- **Mobile Support**: iOS and Android companion apps
- **Cloud Sync**: Optional cloud backup for your data
- **Advanced Mapping**: More map styles and visualization options
- **Batch Processing**: Handle larger address datasets

### Long-term Goals:
- **Real-time Collaboration**: Share maps with family members
- **Historical Tracking**: Track address changes over time
- **Integration**: Connect with genealogy platforms

---

## 🎉 Choose Your Adventure:

- **🚀 Just want to map addresses?** → Download the Standalone version for your OS
- **🔧 Want full features and updates?** → Use the Docker version  
- **💻 Want to contribute or customize?** → Clone the repository

**Made with ❤️ for families who want to visualize their connections across the map** 🗺️

*Now supporting Windows, macOS, and Linux - because every family deserves to see their story on the map!* 