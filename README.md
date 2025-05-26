# 📍 Family Mapping App

**Interactive church family address mapping application with geocoding and neighborhood visualization**

Created by **Matt Keathley @ Highland Park United Methodist Church (HPUMC)** using the **Cursor App** and **Vibe Coding Method**.

## 🎯 Purpose

The Family Mapping App is designed specifically for churches to:
- **Map church families** on an interactive map
- **Visualize neighborhoods** where congregation members live
- **Identify geographic clusters** for ministry planning
- **Export family data** for outreach and pastoral care
- **Manage multiple datasets** for different ministries or events

Perfect for mission trips, small group organization, pastoral visits, and understanding your congregation's geographic distribution.

## ✨ Features

### 🗺️ **Interactive Mapping**
- **Dallas-centered map** with OpenStreetMap tiles
- **Family markers** with popup details (name, address, contact info)
- **Circle selection tool** for neighborhood analysis
- **Zoom and pan** for detailed exploration

### 📊 **Smart CSV Processing**
- **Automatic header detection** - works with or without column headers
- **Positional mapping** for consistent data import
- **Multiple dataset management** with easy switching
- **Progress tracking** with real-time geocoding updates

### 🎯 **Neighborhood Analysis**
- **Draw circles** on the map to select geographic areas
- **Export selected families** to CSV for targeted outreach
- **Count families** in specific neighborhoods
- **Visual clustering** to identify ministry opportunities

### 📥 **Data Management**
- **Upload multiple CSV files** with different family groups
- **Switch between datasets** (Youth Ministry, Mission Trip, etc.)
- **Download failed geocoding results** for manual review
- **Clear datasets** with confirmation prompts

## 🚀 Quick Start

### Option 1: Download Standalone App (Recommended)
1. Go to [Releases](https://github.com/mkeathley2/family-mapping-app/releases)
2. Download for your platform:
   - **Windows**: `family-mapping-app-standalone-windows-v*.zip`
   - **macOS**: `family-mapping-app-standalone-macos-v*.zip`
   - **Linux**: `family-mapping-app-standalone-linux-v*.tar.gz`
3. Extract and run the executable
4. Open http://localhost:8765 in your browser

### Option 2: Run from Source
```bash
# Clone repository
git clone https://github.com/mkeathley2/family-mapping-app.git
cd family-mapping-app

# Install dependencies
pip install flask pandas geopy

# Run application
python app.py
```

## 📋 CSV Format

The app accepts CSV files with family information. Headers are optional - the app uses smart detection.

### Expected Columns (in order):
1. **Family Name** - "The Smith Family"
2. **Address** - "123 Main St"
3. **Unused** - (can be empty)
4. **City** - "Dallas"
5. **State** - "TX"
6. **Zip Code** - "75205"
7. **PeopleID** - Unique identifier (optional)

### Example CSV:
```csv
The Johnson Family,456 Oak Ave,,Dallas,TX,75214,12345
The Williams Family,789 Pine St,,Plano,TX,75023,12346
```

## 🎯 Church Use Cases

### 📍 **Mission Trip Planning**
- Upload mission trip participant addresses
- Identify carpooling opportunities by neighborhood
- Plan pickup routes and meeting locations

### 🏠 **Small Group Organization**
- Map small group members by geographic area
- Form neighborhood-based groups
- Optimize meeting locations

### 👥 **Pastoral Care**
- Visualize congregation distribution
- Plan efficient visitation routes
- Identify isolated members needing outreach

### 🎉 **Event Planning**
- Map event attendees
- Choose optimal venue locations
- Coordinate transportation

## 🛠️ Technical Details

- **Framework**: Flask web application
- **Mapping**: Leaflet.js with OpenStreetMap
- **Geocoding**: Nominatim service with rate limiting
- **Data**: Pandas for CSV processing
- **Standalone**: PyInstaller for cross-platform executables

## 🔧 Development

### Local Development
```bash
# Install dependencies
pip install flask pandas geopy pyinstaller

# Run development server
python app.py

# Build standalone executable
pyinstaller app_standalone.spec
```

### Building Releases
The project uses GitHub Actions for automated cross-platform builds:
- **Windows**: PyInstaller executable
- **macOS**: PyInstaller app bundle  
- **Linux**: PyInstaller binary

## 📖 Usage Guide

### 1. **Upload Family Data**
- Click "Upload New Dataset"
- Enter a descriptive name (e.g., "Youth Ministry 2024")
- Select your CSV file
- Watch real-time geocoding progress

### 2. **Explore the Map**
- View all family locations as markers
- Click markers for family details
- Use zoom controls for detailed view

### 3. **Analyze Neighborhoods**
- Click "Draw Circle Mode"
- Click and drag to create selection circles
- Click "Export Selection to CSV" to download families in that area

### 4. **Manage Datasets**
- Switch between different family groups
- Delete old datasets
- Clear all data when needed

## 🤝 Contributing

This project was created using the **Vibe Coding Method** with **Cursor App** for rapid development and AI-assisted coding.

## 📄 License

Created for Highland Park United Methodist Church and the broader church community.

## 🙏 Acknowledgments

- **Highland Park United Methodist Church** for the ministry vision
- **Cursor App** for AI-powered development
- **Vibe Coding Method** for rapid prototyping
- **OpenStreetMap** for mapping data
- **Nominatim** for geocoding services

---

*Built with ❤️ for church ministry and community connection* 