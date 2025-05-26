#!/usr/bin/env python3
"""
Family Mapping App - Standalone Version
A simplified version optimized for PyInstaller packaging
Cross-platform support for Windows, macOS, and Linux
"""

import os
import sys
import json
import webbrowser
import threading
import time
import platform
import math
import uuid
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
    from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
    from werkzeug.utils import secure_filename
    import pandas as pd
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
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
COLUMNS = ['Family Name', 'Address', 'City', 'State', 'Zip', 'PeopleID']

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global progress tracking
geocoding_progress = {}
geocoding_cancel_flags = {}  # Track cancellation requests

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_datasets():
    """Get list of all available datasets"""
    datasets = []
    if os.path.exists(UPLOAD_FOLDER):
        try:
            for item in os.listdir(UPLOAD_FOLDER):
                dataset_path = os.path.join(UPLOAD_FOLDER, item)
                if os.path.isdir(dataset_path):
                    cache_file = os.path.join(dataset_path, 'geocoded_cache.csv')
                    if os.path.exists(cache_file):
                        # Check if file is not empty/corrupted
                        if os.path.getsize(cache_file) < 10:
                            print(f"Warning: Skipping corrupted dataset {item} (cache file too small)")
                            continue
                            
                        # Get file modification time
                        mod_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
                        # Count addresses
                        try:
                            df = pd.read_csv(cache_file)
                            count = len(df)
                        except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
                            print(f"Warning: Skipping corrupted dataset {item}: {str(e)}")
                            continue
                        except Exception as e:
                            print(f"Warning: Error reading dataset {item}: {str(e)}")
                            count = 0
                            
                        datasets.append({
                            'name': item,
                            'path': dataset_path,
                            'last_modified': mod_time.strftime('%Y-%m-%d %H:%M'),
                            'address_count': count
                        })
        except (PermissionError, OSError) as e:
            print(f"Warning: Cannot access datasets directory: {str(e)}")
            # Recreate the directory if it doesn't exist or has permission issues
            try:
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            except Exception as create_error:
                print(f"Error recreating datasets directory: {str(create_error)}")
    else:
        # Create the directory if it doesn't exist
        try:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        except Exception as create_error:
            print(f"Error creating datasets directory: {str(create_error)}")
    
    return sorted(datasets, key=lambda x: x['last_modified'], reverse=True)

def load_valid_addresses(dataset_name=None):
    """Load addresses from a specific dataset or default"""
    if dataset_name:
        cache_file = os.path.join(UPLOAD_FOLDER, dataset_name, 'geocoded_cache.csv')
    else:
        cache_file = 'geocoded_cache.csv'  # Default legacy file
    
    if not os.path.exists(cache_file):
        return pd.DataFrame()
    
    # Check if file is empty or too small
    if os.path.getsize(cache_file) < 10:  # Less than 10 bytes is likely empty/corrupted
        print(f"Warning: {cache_file} is empty or corrupted (size: {os.path.getsize(cache_file)} bytes)")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(cache_file)
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        print(f"Error reading {cache_file}: {str(e)}")
        return pd.DataFrame()
    
    # Check if DataFrame is empty or missing required columns
    if df.empty or 'Latitude' not in df.columns or 'Longitude' not in df.columns:
        return pd.DataFrame()
    
    # Filter out rows with missing or invalid lat/lon
    df = df.dropna(subset=['Latitude', 'Longitude'])
    df = df[(df['Latitude'].apply(lambda x: isinstance(x, (int, float)) or str(x).replace('.', '', 1).isdigit())) &
            (df['Longitude'].apply(lambda x: isinstance(x, (int, float)) or str(x).replace('.', '', 1).isdigit()))]
    df['Latitude'] = df['Latitude'].astype(float)
    df['Longitude'] = df['Longitude'].astype(float)
    return df

def geocode_dataset(dataset_name, csv_file_path, progress_id):
    """Geocode a dataset in the background"""
    try:
        # Initialize progress
        geocoding_progress[progress_id] = {
            'status': 'starting',
            'progress': 0,
            'total': 0,
            'current_address': '',
            'completed': False,
            'error': None
        }
        
        # Create dataset directory
        dataset_path = os.path.join(UPLOAD_FOLDER, dataset_name)
        os.makedirs(dataset_path, exist_ok=True)
        
        # Read the uploaded CSV
        print(f"Reading CSV file: {csv_file_path}")
        raw_df = pd.read_csv(csv_file_path)
        print(f"Raw CSV has {len(raw_df)} rows and columns: {list(raw_df.columns)}")
        
        # Check if the first row contains data instead of headers
        # This happens when CSV doesn't have proper column names
        first_row_values = raw_df.iloc[0].tolist() if len(raw_df) > 0 else []
        columns_look_like_data = any(
            str(val).strip() and (
                any(char.isdigit() for char in str(val)) or  # Contains numbers
                len(str(val).split()) > 1 or  # Multiple words
                str(val).lower() in ['tx', 'ca', 'ny', 'fl']  # State abbreviations
            ) for val in first_row_values[:5]  # Check first 5 columns
        )
        
        if columns_look_like_data:
            print("Detected that first row contains data, not headers. Using positional mapping.")
            # Read again without treating first row as headers
            raw_df = pd.read_csv(csv_file_path, header=None)
            print(f"Re-read CSV without headers: {len(raw_df)} rows and {len(raw_df.columns)} columns")
            
            # Use positional mapping for CSV without headers
            df = pd.DataFrame()
            df['Family Name'] = raw_df.iloc[:, 0] if len(raw_df.columns) > 0 else ''
            df['Address'] = raw_df.iloc[:, 1] if len(raw_df.columns) > 1 else ''
            df['City'] = raw_df.iloc[:, 3] if len(raw_df.columns) > 3 else ''
            df['State'] = raw_df.iloc[:, 4] if len(raw_df.columns) > 4 else ''
            df['Zip'] = raw_df.iloc[:, 5] if len(raw_df.columns) > 5 else ''
            df['PeopleID'] = raw_df.iloc[:, 6] if len(raw_df.columns) > 6 else ''
            print("Using positional mapping (no headers)")
        else:
            # Try to map columns automatically using column names
            df_columns = raw_df.columns.tolist()
            column_mapping = {}
            
            # More robust column mapping logic for files with headers
            for i, col in enumerate(df_columns):
                col_lower = str(col).lower()
                if i == 0 or 'family' in col_lower or ('name' in col_lower and 'file' not in col_lower):
                    column_mapping['Family Name'] = col
                elif i == 1 or ('address' in col_lower and 'email' not in col_lower):
                    column_mapping['Address'] = col
                elif i == 3 or 'city' in col_lower:
                    column_mapping['City'] = col
                elif i == 4 or 'state' in col_lower:
                    column_mapping['State'] = col
                elif i == 5 or 'zip' in col_lower or 'postal' in col_lower:
                    column_mapping['Zip'] = col
                elif i == 6 or 'people' in col_lower or 'id' in col_lower:
                    column_mapping['PeopleID'] = col
            
            # Create mapped DataFrame
            df = pd.DataFrame()
            df['Family Name'] = raw_df[column_mapping.get('Family Name', raw_df.columns[0])] if column_mapping.get('Family Name') or len(raw_df.columns) > 0 else ''
            df['Address'] = raw_df[column_mapping.get('Address', raw_df.columns[1] if len(raw_df.columns) > 1 else raw_df.columns[0])]
            df['City'] = raw_df[column_mapping.get('City', raw_df.columns[3] if len(raw_df.columns) > 3 else '')] if column_mapping.get('City') or len(raw_df.columns) > 3 else ''
            df['State'] = raw_df[column_mapping.get('State', raw_df.columns[4] if len(raw_df.columns) > 4 else '')] if column_mapping.get('State') or len(raw_df.columns) > 4 else ''
            df['Zip'] = raw_df[column_mapping.get('Zip', raw_df.columns[5] if len(raw_df.columns) > 5 else '')] if column_mapping.get('Zip') or len(raw_df.columns) > 5 else ''
            df['PeopleID'] = raw_df[column_mapping.get('PeopleID', raw_df.columns[6] if len(raw_df.columns) > 6 else '')] if column_mapping.get('PeopleID') or len(raw_df.columns) > 6 else ''
            print(f"Using column mapping: {column_mapping}")
        
        # Clean and validate data
        df = df.fillna('')
        df = df.astype(str)
        
        # Filter out rows without addresses
        df = df[df['Address'].str.strip() != '']
        
        if len(df) == 0:
            geocoding_progress[progress_id]['error'] = 'No valid addresses found in the CSV file'
            geocoding_progress[progress_id]['status'] = 'error'
            return
        
        geocoding_progress[progress_id]['total'] = len(df)
        geocoding_progress[progress_id]['status'] = 'geocoding'
        
        # Initialize geocoder
        geolocator = Nominatim(user_agent="FamilyMappingApp/1.0")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        
        geocoded_data = []
        failed_addresses = []
        
        for index, row in df.iterrows():
            # Check for cancellation
            if geocoding_cancel_flags.get(progress_id, False):
                print(f"Geocoding cancelled for progress_id: {progress_id}")
                geocoding_progress[progress_id]['status'] = 'cancelled'
                return
            
            # Build full address
            address_parts = [row['Address']]
            if row['City']:
                address_parts.append(row['City'])
            if row['State']:
                address_parts.append(row['State'])
            if row['Zip']:
                address_parts.append(row['Zip'])
            
            full_address = ', '.join(address_parts)
            
            # Update progress
            geocoding_progress[progress_id]['progress'] = index + 1
            geocoding_progress[progress_id]['current_address'] = full_address
            
            print(f"Geocoding {index + 1}/{len(df)}: {full_address}")
            
            try:
                location = geocode(full_address)
                if location:
                    geocoded_data.append({
                        'Family Name': row['Family Name'],
                        'Address': row['Address'],
                        'City': row['City'],
                        'State': row['State'],
                        'Zip': row['Zip'],
                        'PeopleID': row['PeopleID'],
                        'Latitude': location.latitude,
                        'Longitude': location.longitude,
                        'Full Address': full_address
                    })
                else:
                    failed_addresses.append({
                        'Family Name': row['Family Name'],
                        'Address': row['Address'],
                        'City': row['City'],
                        'State': row['State'],
                        'Zip': row['Zip'],
                        'PeopleID': row['PeopleID'],
                        'Full Address': full_address,
                        'Error': 'No location found'
                    })
            except Exception as e:
                print(f"Error geocoding {full_address}: {str(e)}")
                failed_addresses.append({
                    'Family Name': row['Family Name'],
                    'Address': row['Address'],
                    'City': row['City'],
                    'State': row['State'],
                    'Zip': row['Zip'],
                    'PeopleID': row['PeopleID'],
                    'Full Address': full_address,
                    'Error': str(e)
                })
        
        # Save results
        if geocoded_data:
            geocoded_df = pd.DataFrame(geocoded_data)
            cache_file = os.path.join(dataset_path, 'geocoded_cache.csv')
            geocoded_df.to_csv(cache_file, index=False)
        
        if failed_addresses:
            failed_df = pd.DataFrame(failed_addresses)
            failed_file = os.path.join(dataset_path, 'failed_addresses.csv')
            failed_df.to_csv(failed_file, index=False)
        
        # Update final progress
        geocoding_progress[progress_id]['status'] = 'completed'
        geocoding_progress[progress_id]['completed'] = True
        geocoding_progress[progress_id]['successful_count'] = len(geocoded_data)
        geocoding_progress[progress_id]['failed_count'] = len(failed_addresses)
        geocoding_progress[progress_id]['has_failed_addresses'] = len(failed_addresses) > 0
        
        print(f"Geocoding completed: {len(geocoded_data)} successful, {len(failed_addresses)} failed")
        
    except Exception as e:
        print(f"Error in geocode_dataset: {str(e)}")
        geocoding_progress[progress_id]['error'] = str(e)
        geocoding_progress[progress_id]['status'] = 'error'

@app.route('/')
def index():
    datasets = get_datasets()
    current_dataset = session.get('current_dataset')
    
    if current_dataset and current_dataset in [d['name'] for d in datasets]:
        df = load_valid_addresses(current_dataset)
    elif datasets:
        # Use the most recent dataset
        current_dataset = datasets[0]['name']
        session['current_dataset'] = current_dataset
        df = load_valid_addresses(current_dataset)
    else:
        # Try legacy file
        df = load_valid_addresses()
        current_dataset = 'Default'
    
    addresses_json = df.to_json(orient='records')
    address_count = len(df)
    
    response = app.make_response(render_template('map.html', 
                                                addresses_json=addresses_json,
                                                address_count=address_count,
                                                datasets=datasets,
                                                current_dataset=current_dataset))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload - exactly like original app.py"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        dataset_name = request.form.get('dataset_name', '').strip()
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not dataset_name:
            return jsonify({'error': 'Dataset name is required'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Create temporary file path
            temp_path = os.path.join(UPLOAD_FOLDER, f"temp_{filename}")
            file.save(temp_path)
            
            # Generate progress ID
            progress_id = str(uuid.uuid4())
            
            # Start geocoding in background thread
            thread = threading.Thread(
                target=geocode_dataset,
                args=(dataset_name, temp_path, progress_id)
            )
            thread.daemon = True
            thread.start()
            
            return jsonify({'progress_id': progress_id})
        
        return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/progress/<progress_id>')
def get_progress(progress_id):
    """Get geocoding progress"""
    return jsonify(geocoding_progress.get(progress_id, {'status': 'not_found'}))

@app.route('/cancel_geocoding/<progress_id>', methods=['POST'])
def cancel_geocoding(progress_id):
    """Cancel ongoing geocoding"""
    try:
        data = request.get_json()
        dataset_name = data.get('dataset_name')
        
        if not dataset_name:
            return jsonify({'error': 'Dataset name required'}), 400
        
        # Set cancellation flag
        geocoding_cancel_flags[progress_id] = True
        
        # Clean up dataset directory
        dataset_path = os.path.join(UPLOAD_FOLDER, dataset_name)
        if os.path.exists(dataset_path):
            import shutil
            try:
                shutil.rmtree(dataset_path)
                print(f"Deleted dataset directory: {dataset_path}")
            except Exception as e:
                print(f"Error deleting dataset directory: {str(e)}")
        
        # Clean up progress tracking
        if progress_id in geocoding_progress:
            del geocoding_progress[progress_id]
        if progress_id in geocoding_cancel_flags:
            del geocoding_cancel_flags[progress_id]
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_failed_addresses/<dataset_name>')
def download_failed_addresses(dataset_name):
    """Download failed addresses for a specific dataset"""
    try:
        failed_file = os.path.join(UPLOAD_FOLDER, dataset_name, 'failed_addresses.csv')
        
        if not os.path.exists(failed_file):
            return jsonify({'error': 'No failed addresses file found for this dataset'}), 404
        
        # Read the failed addresses CSV and rename the column
        try:
            failed_df = pd.read_csv(failed_file)
            
            # Rename 'Family Name' column to 'Name' if it exists
            if 'Family Name' in failed_df.columns:
                failed_df = failed_df.rename(columns={'Family Name': 'Name'})
                print(f"Renamed 'Family Name' column to 'Name' for failed addresses download")
            
            # Add PeopleID Link column if it doesn't exist
            if 'PeopleID' in failed_df.columns and 'PeopleID Link' not in failed_df.columns:
                failed_df['PeopleID Link'] = failed_df['PeopleID'].apply(
                    lambda x: f"https://my.hpumc.org/Person2/{x}" if pd.notna(x) and str(x).strip() != '' else ''
                )
                print(f"Added PeopleID Link column for {len(failed_df)} failed addresses download")
            
            # Create a temporary file with the renamed column
            import io
            output = io.StringIO()
            failed_df.to_csv(output, index=False)
            output.seek(0)
            
            filename = f'failed_addresses_{dataset_name}.csv'
            return send_file(io.BytesIO(output.getvalue().encode()), 
                            mimetype='text/csv', 
                            as_attachment=True, 
                            download_name=filename)
            
        except Exception as e:
            print(f"Error processing failed addresses file: {str(e)}")
            # Fallback to original file if processing fails
            filename = f'failed_addresses_{dataset_name}.csv'
            return send_file(failed_file, 
                            mimetype='text/csv', 
                            as_attachment=True, 
                            download_name=filename)
        
    except Exception as e:
        print(f"Error downloading failed addresses: {str(e)}")
        return jsonify({'error': f'Failed to download failed addresses: {str(e)}'}), 500

@app.route('/switch_dataset/<dataset_name>')
def switch_dataset(dataset_name):
    """Switch to a different dataset"""
    session['current_dataset'] = dataset_name
    return redirect(url_for('index'))

@app.route('/clear_all_datasets', methods=['POST'])
def clear_all_datasets():
    """Clear all datasets"""
    try:
        import shutil
        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        session.pop('current_dataset', None)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f'Failed to clear datasets: {str(e)}'}), 500

@app.route('/delete_dataset/<dataset_name>', methods=['DELETE'])
def delete_dataset(dataset_name):
    """Delete a specific dataset"""
    try:
        import shutil
        dataset_path = os.path.join(UPLOAD_FOLDER, dataset_name)
        if os.path.exists(dataset_path):
            shutil.rmtree(dataset_path)
        
        # Clear session if this was the current dataset
        if session.get('current_dataset') == dataset_name:
            session.pop('current_dataset', None)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f'Failed to delete dataset: {str(e)}'}), 500

@app.route('/export_csv', methods=['POST'])
def export_csv():
    data = request.json
    center = data['center']  # [lat, lng]
    radius = data['radius']  # in meters
    
    current_dataset = session.get('current_dataset')
    df = load_valid_addresses(current_dataset)
    
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000  # meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    selected = df[df.apply(lambda row: haversine(center[0], center[1], row['Latitude'], row['Longitude']) <= radius, axis=1)]
    
    # Make a copy to avoid SettingWithCopyWarning
    selected = selected.copy()
    
    # Rename 'Family Name' column to 'Name' if it exists
    if 'Family Name' in selected.columns:
        selected = selected.rename(columns={'Family Name': 'Name'})
        print(f"Renamed 'Family Name' column to 'Name' for export")
    
    # Add PeopleID Link column
    if 'PeopleID' in selected.columns:
        selected['PeopleID Link'] = selected['PeopleID'].apply(
            lambda x: f"https://my.hpumc.org/Person2/{x}" if pd.notna(x) and str(x).strip() != '' else ''
        )
        print(f"Added PeopleID Link column for {len(selected)} selected addresses")
    
    import io
    output = io.StringIO()
    selected.to_csv(output, index=False)
    output.seek(0)
    
    filename = f'selected_addresses_{current_dataset or "default"}.csv'
    return send_file(io.BytesIO(output.getvalue().encode()), 
                     mimetype='text/csv', 
                     as_attachment=True, 
                     download_name=filename)

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