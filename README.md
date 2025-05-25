# Family Mapping App v0.0.2

An interactive web application for geocoding family addresses and visualizing them on a map with powerful selection and export tools. Now with dataset management and file upload capabilities!

## 🔒 Privacy & Data Security

**⚠️ IMPORTANT: This repository contains NO real address data!**

- **No Personal Information**: This GitHub repository does not contain any real addresses, family names, or personal information
- **Sample Data Only**: The included `sample_addresses.csv` contains only fictional example data for demonstration
- **Your Data Stays Local**: All address data you upload stays on your local machine and is never shared
- **Git Protection**: The `.gitignore` file ensures that any real address data you import will never be accidentally uploaded to version control

**To use this app with your own data:**
1. Download/clone this repository
2. Follow the installation instructions below
3. Upload your own CSV files through the web interface
4. Your data will be stored locally in the `datasets/` folder (which is excluded from git)

## 🆕 What's New in v0.0.2

### 📤 File Upload & Dataset Management
- **Upload CSV Files**: Upload your own CSV files directly through the web interface
- **Named Datasets**: Give each dataset a custom name (e.g., "Family Reunion 2024")
- **Multiple Datasets**: Switch between different address datasets easily
- **Dataset History**: View all uploaded datasets with creation dates and address counts

### 📊 Real-time Progress Tracking
- **Live Progress Bar**: Watch geocoding progress in real-time
- **Current Address Display**: See which address is currently being processed
- **Background Processing**: Upload and continue using the app while geocoding happens
- **Smart Column Mapping**: Automatically detects and maps CSV columns

### 🎨 Enhanced User Interface
- **Modern Design**: Clean, professional interface with improved layout
- **Dataset Panel**: Easy-to-use dataset management on the left side
- **Progress Modal**: Beautiful progress tracking with visual feedback
- **Error Handling**: Clear error messages and user guidance

## Features

### 🗺️ Interactive Map Interface
- **Visual Address Display**: View all geocoded addresses as markers on an interactive map
- **Dual Mode System**: Toggle between map navigation and circle drawing modes
- **Responsive Design**: Clean, modern interface with intuitive controls

### 📁 Dataset Management
- **Upload New Datasets**: Drag and drop CSV files with custom names
- **Switch Between Datasets**: Click any dataset to load it instantly
- **Dataset Information**: See address counts and last modified dates
- **Persistent Selection**: Your current dataset is remembered between sessions

### 🎯 Circle Selection Tool
- **Draw Custom Circles**: Click and drag to create selection circles of any size
- **Real-time Feedback**: See circle size change as you drag
- **Minimum Radius**: 50-meter minimum ensures meaningful selections
- **Performance Optimized**: Fast, smooth circle drawing with no lag

### 📊 Data Export
- **CSV Export**: Export addresses within selected circles to CSV files
- **Complete Data**: Includes family names, addresses, coordinates, and location details
- **Dataset-specific Names**: Export files named after your current dataset
- **Instant Download**: One-click export with automatic file download

### 🔧 Geocoding Engine
- **Background Processing**: Geocoding happens in the background with progress tracking
- **Smart Column Detection**: Automatically maps common column names
- **Error Handling**: Robust handling of invalid or incomplete addresses
- **Rate Limiting**: Respects geocoding service limits

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git (for version control)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/mkeathley2/family-mapping-app.git
   cd family-mapping-app
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
1. **Start the web server:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   - Navigate to `http://127.0.0.1:5000`
   - The app will load with the dataset management interface

## How to Use

### 📤 Uploading Your First Dataset
1. **Prepare your CSV file** with columns like:
   - Family Name, Address, City, State, Zip, PeopleID
   - Or similar variations (the app will auto-detect)
   - **See `sample_addresses.csv`** for an example of the expected format

2. **Upload through the web interface:**
   - Enter a dataset name (e.g., "Smith Family Reunion 2024")
   - Select your CSV file
   - Click "Upload & Geocode"

3. **Watch the progress:**
   - A progress modal will show geocoding status
   - See real-time updates as addresses are processed
   - Page automatically refreshes when complete

### 🗂️ Managing Datasets
- **View All Datasets**: See all uploaded datasets in the left panel
- **Switch Datasets**: Click any dataset name to load it
- **Current Dataset**: Highlighted in green with address count
- **Dataset Info**: Shows creation date and number of addresses

### 🎯 Creating Selections
1. **Enable Drawing**: Click "Draw Circle Mode" (button turns red)
2. **Draw Circle**: Click and drag anywhere on the map to create a selection circle
3. **Adjust Size**: Drag further from center for larger circles
4. **Return to Navigation**: Click "Map Navigation" to return to normal map interaction

### 📊 Exporting Data
1. **Draw a Circle**: Create a selection circle around desired addresses
2. **Export**: Click the green "Export Selection to CSV" button
3. **Download**: CSV file automatically downloads with dataset name included

## Project Structure

```
family-mapping-app/
├── app.py                 # Flask web application with dataset management
├── geocode_addresses.py   # Legacy geocoding script
├── sample_addresses.csv   # Example CSV format (fictional data)
├── templates/
│   └── map.html          # Enhanced interactive map interface
├── datasets/             # Directory for uploaded datasets (excluded from git)
│   ├── dataset1/
│   │   ├── geocoded_cache.csv
│   │   └── original.csv
│   └── dataset2/
│       ├── geocoded_cache.csv
│       └── original.csv
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules (protects your data)
└── README.md            # This file
```

## Technical Details

### Backend (Flask)
- **Framework**: Flask web framework with session management
- **File Upload**: Secure file handling with Werkzeug
- **Background Processing**: Threading for non-blocking geocoding
- **Progress Tracking**: Real-time progress updates via AJAX
- **Dataset Management**: Organized file structure for multiple datasets

### Frontend (Leaflet.js)
- **Mapping**: Leaflet.js for interactive maps
- **Progress UI**: Modal with real-time progress bar
- **Dataset UI**: Dynamic dataset switching and management
- **File Upload**: Modern drag-and-drop interface
- **Responsive Design**: Works on desktop and mobile

### Data Flow
1. **Upload**: User uploads CSV through web interface
2. **Processing**: Background thread geocodes addresses with progress tracking
3. **Storage**: Results stored in organized dataset folders
4. **Visualization**: Addresses displayed on interactive map
5. **Selection**: Draw circles to select addresses
6. **Export**: Generate CSV of selected addresses

## Configuration

### Map Settings
- **Default Center**: Dallas, TX (32.7767, -96.7970)
- **Default Zoom**: Level 11
- **Minimum Circle Radius**: 50 meters

### File Upload
- **Supported Formats**: CSV files only
- **Column Detection**: Automatic mapping of common column names
- **File Size**: No explicit limit (limited by server configuration)
- **Security**: Secure filename handling and validation

### Dataset Storage
- **Location**: `datasets/` directory
- **Structure**: Each dataset gets its own folder
- **Files**: Original CSV and geocoded cache stored separately

## Troubleshooting

### Upload Issues
- **File Format**: Ensure you're uploading a CSV file
- **Column Names**: Use common names like "Address", "City", "State", "Zip"
- **Dataset Names**: Use unique names for each dataset
- **File Size**: Very large files may take longer to process

### Geocoding Issues
- **Progress Stuck**: Refresh the page and check if dataset was created
- **Missing Addresses**: Some addresses may not geocode successfully
- **Rate Limiting**: Geocoding respects service limits (1 request per second)

### Browser Compatibility
- **Recommended**: Chrome, Firefox, Safari, Edge (modern versions)
- **JavaScript Required**: Application requires JavaScript to be enabled
- **Local Storage**: Uses browser sessions for dataset selection

## Version History

### v0.0.2 (Current)
- ✅ File upload interface
- ✅ Dataset management system
- ✅ Real-time progress tracking
- ✅ Background geocoding
- ✅ Enhanced UI/UX
- ✅ Smart column mapping

### v0.0.1
- ✅ Basic map interface
- ✅ Circle selection tool
- ✅ CSV export functionality
- ✅ Command-line geocoding

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Development Setup
- Follow the installation steps above
- Make changes to the code
- Test with `python app.py`
- Commit and push your changes

## License

[MIT](LICENSE) - Feel free to use this project for personal or commercial purposes.

## Support

If you encounter issues or have questions:
1. Check the troubleshooting section above
2. Review existing GitHub issues
3. Create a new issue with detailed information about your problem

---

**Built with ❤️ for family mapping and address visualization** 