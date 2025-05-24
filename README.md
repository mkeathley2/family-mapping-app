# Family Mapping App

This project maps addresses to neighborhoods using geocoding and provides tools for working with address data.

## Features
- Geocode addresses and cache results
- Map addresses to neighborhoods
- Easily extendable for new data sources

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git (for version control)

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/mkeathley2/family-mapping-app.git
   cd family-mapping-app
   ```
2. (Optional) Create and activate a virtual environment:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
- Place your address data in `addresses.csv`.
- Run the geocoding script:
  ```sh
  python geocode_addresses.py
  ```
- Results will be saved in `geocoded_cache.csv`.

## Project Structure
- `geocode_addresses.py` — Main script for geocoding addresses
- `addresses.csv` — Input file for addresses
- `geocoded_cache.csv` — Output file with geocoded results
- `.gitignore` — Files and folders to ignore in version control

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE) 