# Family Mapping App v0.0.6 - Fixed Standalone Interface

## 🎯 Major Interface Fix

This release fixes the standalone application to **match the original app.py interface exactly**. Users should not notice any difference between the standalone and original versions.

## 🔧 What Was Fixed

### Interface Consistency
- **Removed extra opening screen styling** - The standalone app now uses the same clean interface as the original
- **Restored original map.html template** - No more simplified standalone template
- **Map centers on Dallas, Texas** - Just like the original app (32.7767, -96.7970)
- **Same header panel and controls** - Identical layout and functionality

### CSV File Handling
- **No headers required** - Restored the original smart CSV detection logic
- **Positional mapping support** - Automatically detects CSV files without proper column names
- **Robust column mapping** - Handles various CSV formats just like the original
- **Same error messages** - Consistent user experience

### Dataset Management
- **Full dataset system** - Complete dataset management with progress tracking
- **Background geocoding** - Real-time progress updates and cancellation support
- **Failed address tracking** - Download failed addresses for review
- **Dataset switching** - Multiple dataset support with session management

## 📦 Cross-Platform Packages

All three platforms now have the identical interface:

### Windows 10+
- Download: `family-mapping-app-standalone-windows-v0.0.6.zip`
- Run: Double-click `START_HERE.bat`

### macOS 10.14+
- Download: `family-mapping-app-standalone-macos-v0.0.6.zip`
- Run: Double-click `START_HERE.sh` (approve security prompt)

### Linux (Ubuntu 18.04+)
- Download: `family-mapping-app-standalone-linux-v0.0.6.tar.gz`
- Run: `./START_HERE.sh` in terminal

## 🚀 Features

- **No installation required** - Just download, extract, and run
- **Automatic browser opening** - Opens http://localhost:8765 automatically
- **OpenStreetMap geocoding** - Free, no API keys needed
- **CSV export with coordinates** - Download results with lat/lon data
- **Circle selection tool** - Select addresses within a radius
- **Real-time progress tracking** - See geocoding progress with current address
- **Cross-platform compatibility** - Same experience on all operating systems

## 🔄 Upgrade Instructions

If you have v0.0.5 or earlier:
1. Download the new v0.0.6 package for your platform
2. Extract to a new folder (don't overwrite the old version)
3. Your data from previous versions is not compatible (different interface)
4. Re-upload your CSV files to the new version

## 🐛 Bug Fixes

- Fixed standalone app requiring CSV headers
- Fixed map centering on wrong location (was center of US, now Dallas)
- Fixed interface differences between standalone and original
- Fixed missing dataset management features
- Fixed progress tracking and cancellation
- Fixed CSV column detection logic

## 📋 Technical Details

- **Framework**: Flask web application with Leaflet.js mapping
- **Geocoding**: OpenStreetMap Nominatim service (rate-limited, respectful)
- **Build**: PyInstaller cross-platform executables
- **Dependencies**: All bundled, no external requirements
- **Port**: Runs on localhost:8765

## 🆘 Support

If you encounter issues:
1. Make sure no other applications are using port 8765
2. Check that your CSV file has address data in the expected columns
3. Try the sample file included in the package
4. Contact support with specific error messages

---

**Download Links**: https://github.com/mkeathley2/family-mapping-app/releases/tag/v0.0.6 