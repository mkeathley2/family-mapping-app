# Family Mapping App

An interactive web application for geocoding family addresses and visualizing them on a map with powerful selection and export tools.

## Features

### 🗺️ Interactive Map Interface
- **Visual Address Display**: View all geocoded addresses as markers on an interactive map
- **Dual Mode System**: Toggle between map navigation and circle drawing modes
- **Responsive Design**: Clean, modern interface with intuitive controls

### 🎯 Circle Selection Tool
- **Draw Custom Circles**: Click and drag to create selection circles of any size
- **Real-time Feedback**: See circle size change as you drag
- **Minimum Radius**: 50-meter minimum ensures meaningful selections
- **Performance Optimized**: Fast, smooth circle drawing with no lag

### 📊 Data Export
- **CSV Export**: Export addresses within selected circles to CSV files
- **Complete Data**: Includes family names, addresses, coordinates, and location details
- **Instant Download**: One-click export with automatic file download

### 🔧 Geocoding Engine
- **Address Geocoding**: Convert addresses to latitude/longitude coordinates
- **Smart Caching**: Results cached to avoid redundant API calls
- **Error Handling**: Robust handling of invalid or incomplete addresses

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
   pip install flask pandas requests
   ```

### Setup Your Data
1. **Prepare your address file:**
   - Create or update `addresses.csv` with your family addresses
   - Required columns: `Family Name`, `Address`, `City`, `State`, `Zip`

2. **Geocode your addresses:**
   ```bash
   python geocode_addresses.py
   ```
   - This creates `geocoded_cache.csv` with latitude/longitude coordinates

### Running the Application
1. **Start the web server:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   - Navigate to `http://127.0.0.1:5000`
   - The map will load centered on Dallas, TX with all your addresses displayed

## How to Use

### Basic Navigation
1. **Map Navigation Mode** (default): Drag to pan, scroll to zoom, click markers for details
2. **Draw Circle Mode**: Click the blue "Draw Circle Mode" button to enable drawing

### Creating Selections
1. **Enable Drawing**: Click "Draw Circle Mode" (button turns red)
2. **Draw Circle**: Click and drag anywhere on the map to create a selection circle
3. **Adjust Size**: Drag further from center for larger circles
4. **Return to Navigation**: Click "Map Navigation" to return to normal map interaction

### Exporting Data
1. **Draw a Circle**: Create a selection circle around desired addresses
2. **Export**: Click the green "Export Addresses in Circle to CSV" button
3. **Download**: CSV file automatically downloads with selected addresses

## Project Structure

```
family-mapping-app/
├── app.py                 # Flask web application
├── geocode_addresses.py   # Address geocoding script
├── templates/
│   └── map.html          # Interactive map interface
├── addresses.csv         # Input address data
├── geocoded_cache.csv    # Geocoded results (generated)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Technical Details

### Backend (Flask)
- **Framework**: Flask web framework
- **Data Processing**: Pandas for CSV handling
- **Geocoding**: Custom geocoding with caching
- **Export**: Dynamic CSV generation and download

### Frontend (Leaflet.js)
- **Mapping**: Leaflet.js for interactive maps
- **Tiles**: OpenStreetMap tile layer
- **Performance**: Optimized circle drawing with early returns
- **UI**: Clean, responsive design with mode switching

### Data Flow
1. **Input**: CSV file with family addresses
2. **Geocoding**: Convert addresses to coordinates
3. **Caching**: Store results to avoid re-geocoding
4. **Visualization**: Display on interactive map
5. **Selection**: Draw circles to select addresses
6. **Export**: Generate CSV of selected addresses

## Configuration

### Map Settings
- **Default Center**: Dallas, TX (32.7767, -96.7970)
- **Default Zoom**: Level 11
- **Minimum Circle Radius**: 50 meters

### File Formats
- **Input CSV**: `Family Name`, `Address`, `City`, `State`, `Zip`
- **Output CSV**: All input fields plus `Latitude`, `Longitude`

## Troubleshooting

### Common Issues
- **No addresses showing**: Check that `geocoded_cache.csv` exists and has valid coordinates
- **Slow performance**: Ensure you're in the correct mode (navigation vs. drawing)
- **Export not working**: Make sure you've drawn a circle and it contains addresses

### Browser Compatibility
- **Recommended**: Chrome, Firefox, Safari, Edge (modern versions)
- **JavaScript Required**: Application requires JavaScript to be enabled

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