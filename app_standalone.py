#!/usr/bin/env python3
"""
Family Mapping App - Standalone Version
A simplified version optimized for PyInstaller packaging
Cross-platform support for Windows, macOS, and Linux
"""

import os
import sys
import json
import csv
import webbrowser
import threading
import time
import platform
from datetime import datetime
from pathlib import Path

# Add the current directory to Python path for imports
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = os.path.dirname(sys.executable)
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

try:
    from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
    import requests
    from werkzeug.utils import secure_filename
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please make sure all dependencies are installed.")
    if platform.system() == "Windows":
        input("Press Enter to exit...")
    else:
        input("Press Enter to exit...")
    sys.exit(1)

app = Flask(__name__)
app.secret_key = 'family-mapping-standalone-key'

# Configuration
UPLOAD_FOLDER = os.path.join(application_path, 'datasets')
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure datasets directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def geocode_address(address):
    """Simple geocoding using Nominatim (OpenStreetMap)"""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': address,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'FamilyMappingApp/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data:
            result = data[0]
            return {
                'lat': float(result['lat']),
                'lon': float(result['lon']),
                'display_name': result.get('display_name', address)
            }
    except Exception as e:
        print(f"Geocoding error for {address}: {e}")
    
    return None

@app.route('/')
def index():
    return render_template('map_standalone.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the CSV file
            addresses = []
            try:
                with open(filepath, 'r', encoding='utf-8') as csvfile:
                    # Try to detect delimiter
                    sample = csvfile.read(1024)
                    csvfile.seek(0)
                    sniffer = csv.Sniffer()
                    delimiter = sniffer.sniff(sample).delimiter
                    
                    reader = csv.DictReader(csvfile, delimiter=delimiter)
                    for row in reader:
                        # Look for address-like columns
                        address_fields = ['address', 'Address', 'ADDRESS', 'location', 'Location']
                        name_fields = ['name', 'Name', 'NAME', 'family', 'Family']
                        
                        address = None
                        name = None
                        
                        for field in address_fields:
                            if field in row and row[field].strip():
                                address = row[field].strip()
                                break
                        
                        for field in name_fields:
                            if field in row and row[field].strip():
                                name = row[field].strip()
                                break
                        
                        if address:
                            addresses.append({
                                'name': name or 'Unknown',
                                'address': address,
                                'original_row': row
                            })
            
            except Exception as e:
                return jsonify({'error': f'Error reading CSV file: {str(e)}'}), 400
            
            if not addresses:
                return jsonify({'error': 'No valid addresses found in the CSV file. Make sure you have an "address" column.'}), 400
            
            return jsonify({
                'message': f'Successfully uploaded {len(addresses)} addresses',
                'filename': filename,
                'addresses': addresses[:10]  # Return first 10 for preview
            })
        
        return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/geocode/<filename>')
def geocode_file(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        # Read and geocode addresses
        geocoded_data = []
        with open(filepath, 'r', encoding='utf-8') as csvfile:
            sample = csvfile.read(1024)
            csvfile.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            for i, row in enumerate(reader):
                # Look for address column
                address_fields = ['address', 'Address', 'ADDRESS', 'location', 'Location']
                name_fields = ['name', 'Name', 'NAME', 'family', 'Family']
                
                address = None
                name = None
                
                for field in address_fields:
                    if field in row and row[field].strip():
                        address = row[field].strip()
                        break
                
                for field in name_fields:
                    if field in row and row[field].strip():
                        name = row[field].strip()
                        break
                
                if address:
                    print(f"Geocoding {i+1}: {address}")
                    geo_result = geocode_address(address)
                    
                    if geo_result:
                        geocoded_data.append({
                            'name': name or f'Location {i+1}',
                            'address': address,
                            'lat': geo_result['lat'],
                            'lon': geo_result['lon'],
                            'display_name': geo_result['display_name']
                        })
                    else:
                        geocoded_data.append({
                            'name': name or f'Location {i+1}',
                            'address': address,
                            'lat': None,
                            'lon': None,
                            'display_name': address,
                            'error': 'Could not geocode'
                        })
                    
                    # Small delay to be respectful to the geocoding service
                    time.sleep(1)
        
        # Save geocoded results
        output_filename = f"geocoded_{filename}"
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        with open(output_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'address', 'lat', 'lon', 'display_name', 'error']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in geocoded_data:
                writer.writerow(row)
        
        return jsonify({
            'geocoded_data': geocoded_data,
            'output_filename': output_filename
        })
    
    except Exception as e:
        return jsonify({'error': f'Geocoding failed: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/files')
def list_files():
    try:
        files = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.endswith('.csv'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
        return jsonify(files)
    except Exception as e:
        return jsonify({'error': f'Failed to list files: {str(e)}'}), 500

def open_browser():
    """Open the default web browser to the app"""
    time.sleep(1.5)  # Give the server time to start
    webbrowser.open('http://localhost:8765')

def get_platform_info():
    """Get platform-specific information"""
    system = platform.system()
    if system == "Darwin":
        return "macOS", "🍎"
    elif system == "Linux":
        return "Linux", "🐧"
    elif system == "Windows":
        return "Windows", "🪟"
    else:
        return system, "💻"

def main():
    platform_name, platform_emoji = get_platform_info()
    
    print("=" * 50)
    print(f"    Family Mapping App - Standalone Version")
    print(f"    Running on {platform_name} {platform_emoji}")
    print("=" * 50)
    print()
    print("Starting the application...")
    print("This may take a moment...")
    print()
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        print("✓ Server starting on http://localhost:8765")
        print("✓ Your web browser should open automatically")
        print()
        print("If the browser doesn't open, manually go to: http://localhost:8765")
        print()
        if platform.system() == "Windows":
            print("To stop the application, close this window or press Ctrl+C")
        else:
            print("To stop the application, press Ctrl+C in this terminal")
        print("=" * 50)
        
        app.run(host='0.0.0.0', port=8765, debug=False, use_reloader=False)
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error starting server: {e}")
        if platform.system() == "Windows":
            input("Press Enter to exit...")
        else:
            input("Press Enter to exit...")

if __name__ == '__main__':
    main() 