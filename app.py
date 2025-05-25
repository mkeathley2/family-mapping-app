"""
Family Mapping App v0.0.3

A comprehensive Flask web application for geocoding family addresses and visualizing them on an interactive map.

Features:
- File upload and dataset management
- Real-time geocoding with progress tracking and cancellation
- Failed address tracking and export
- Interactive map with circle selection
- CSV export with PeopleID links
- Individual and bulk dataset deletion

Author: Family Mapping App Team
Version: 0.0.3
"""

from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
import pandas as pd
import io
import math
import json
import time
import os
import uuid
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import threading

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# Configuration
UPLOAD_FOLDER = 'datasets'
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
            
            print(f"Column mapping: {column_mapping}")
            
            # If we have the exact columns, use them directly
            if all(col in df_columns for col in COLUMNS):
                df = raw_df[COLUMNS].copy()
                print("Using exact column match")
            elif len(column_mapping) >= 4:  # At least name, address, city, state
                # Rename columns to match our expected format
                df = raw_df.rename(columns=column_mapping)
                # Fill missing columns with empty strings
                for col in COLUMNS:
                    if col not in df.columns:
                        df[col] = ''
                df = df[COLUMNS].copy()
                print("Using column mapping")
            else:
                # Use positional mapping based on typical CSV structure
                # Assume: Name, Address, Extra, City, State, Zip, PeopleID
                df = pd.DataFrame()
                df['Family Name'] = raw_df.iloc[:, 0] if len(raw_df.columns) > 0 else ''
                df['Address'] = raw_df.iloc[:, 1] if len(raw_df.columns) > 1 else ''
                df['City'] = raw_df.iloc[:, 3] if len(raw_df.columns) > 3 else ''
                df['State'] = raw_df.iloc[:, 4] if len(raw_df.columns) > 4 else ''
                df['Zip'] = raw_df.iloc[:, 5] if len(raw_df.columns) > 5 else ''
                df['PeopleID'] = raw_df.iloc[:, 6] if len(raw_df.columns) > 6 else ''
                print("Using positional mapping (fallback)")
        
        print(f"Mapped DataFrame has {len(df)} rows")
        print(f"Sample data - First row: {df.iloc[0].to_dict() if len(df) > 0 else 'No data'}")
        
        # Clean up the data
        df = df.fillna('')  # Replace NaN with empty strings
        df = df.astype(str)  # Convert all to strings
        
        # Remove rows with missing critical data
        original_count = len(df)
        df = df[df['Address'].str.strip() != '']
        df = df[df['City'].str.strip() != '']
        df = df[df['State'].str.strip() != '']
        
        print(f"After cleaning: {len(df)} valid addresses (removed {original_count - len(df)} invalid)")
        
        if len(df) == 0:
            raise ValueError("No valid addresses found in the uploaded file. Please check that your CSV has Address, City, and State columns with data.")
        
        # Clean up zip codes (remove extra digits)
        df['Zip'] = df['Zip'].str.split('-').str[0]  # Take only first part of zip
        
        geocoding_progress[progress_id]['total'] = len(df)
        geocoding_progress[progress_id]['status'] = 'geocoding'
        
        # Setup geocoder with proper rate limiting for Nominatim
        # Nominatim Usage Policy: max 1 request per second
        geolocator = Nominatim(user_agent="family_mapper_v2", timeout=15)
        rate_limiter = RateLimiter(geolocator.geocode, min_delay_seconds=1.0)
        
        # Geocode addresses
        results = []
        failed_addresses = []
        successful_geocodes = 0
        consecutive_failures = 0
        max_consecutive_failures = 5
        
        for idx, row in df.iterrows():
            # Check for cancellation request
            if geocoding_cancel_flags.get(progress_id, False):
                print(f"Geocoding canceled for progress_id: {progress_id}")
                geocoding_progress[progress_id]['status'] = 'canceled'
                geocoding_progress[progress_id]['completed'] = True
                
                # Clean up the dataset directory
                try:
                    import shutil
                    if os.path.exists(dataset_path):
                        shutil.rmtree(dataset_path)
                        print(f"Deleted canceled dataset directory: {dataset_path}")
                except Exception as cleanup_error:
                    print(f"Error cleaning up canceled dataset: {str(cleanup_error)}")
                
                # Clean up cancellation flag
                geocoding_cancel_flags.pop(progress_id, None)
                return
            
            # Clean and format address
            address_parts = []
            if row['Address'].strip():
                address_parts.append(row['Address'].strip())
            if row['City'].strip():
                address_parts.append(row['City'].strip())
            if row['State'].strip():
                address_parts.append(row['State'].strip())
            if row['Zip'].strip():
                address_parts.append(row['Zip'].strip())
            
            address = ', '.join(address_parts)
            geocoding_progress[progress_id]['current_address'] = address
            geocoding_progress[progress_id]['progress'] = idx + 1
            
            lat, lon = None, None
            geocoding_failed = False
            failure_reason = ""
            
            try:
                location = rate_limiter(address)
                if location:
                    lat, lon = location.latitude, location.longitude
                    successful_geocodes += 1
                    consecutive_failures = 0  # Reset failure counter on success
                    print(f"✓ Geocoded: {address} -> {lat}, {lon}")
                else:
                    geocoding_failed = True
                    failure_reason = "No results found"
                    print(f"✗ No results for: {address}")
                    
            except Exception as e:
                geocoding_failed = True
                consecutive_failures += 1
                error_msg = str(e)
                failure_reason = error_msg
                print(f"✗ Error geocoding {address}: {error_msg}")
                
                # Check for rate limiting or service unavailable errors
                if "timeout" in error_msg.lower() or "unavailable" in error_msg.lower() or "max retries" in error_msg.lower():
                    print(f"⚠️  Service issue detected. Waiting extra time before continuing...")
                    time.sleep(2)  # Extra delay for service issues
                    
                # If too many consecutive failures, pause longer
                if consecutive_failures >= max_consecutive_failures:
                    print(f"⚠️  {consecutive_failures} consecutive failures. Pausing for 10 seconds...")
                    time.sleep(10)
                    consecutive_failures = 0
            
            # Track failed addresses
            if geocoding_failed:
                failed_addresses.append({
                    **row.to_dict(),
                    'Full_Address': address,
                    'Failure_Reason': failure_reason
                })
            
            results.append({
                **row.to_dict(),
                'Latitude': lat,
                'Longitude': lon
            })
        
        # Save results
        result_df = pd.DataFrame(results)
        cache_file = os.path.join(dataset_path, 'geocoded_cache.csv')
        result_df.to_csv(cache_file, index=False)
        
        # Save failed addresses if any
        if failed_addresses:
            failed_df = pd.DataFrame(failed_addresses)
            
            # Rename 'Family Name' column to 'Name' if it exists
            if 'Family Name' in failed_df.columns:
                failed_df = failed_df.rename(columns={'Family Name': 'Name'})
                print(f"Renamed 'Family Name' column to 'Name' in failed addresses")
            
            # Add PeopleID Link column
            if 'PeopleID' in failed_df.columns:
                failed_df['PeopleID Link'] = failed_df['PeopleID'].apply(
                    lambda x: f"https://my.hpumc.org/Person2/{x}" if pd.notna(x) and str(x).strip() != '' else ''
                )
                print(f"Added PeopleID Link column for {len(failed_df)} failed addresses")
            
            failed_file = os.path.join(dataset_path, 'failed_addresses.csv')
            failed_df.to_csv(failed_file, index=False)
            print(f"Saved {len(failed_addresses)} failed addresses to {failed_file}")
        
        # Copy original file
        original_file = os.path.join(dataset_path, 'original.csv')
        raw_df.to_csv(original_file, index=False)
        
        geocoding_progress[progress_id]['status'] = 'completed'
        geocoding_progress[progress_id]['completed'] = True
        geocoding_progress[progress_id]['progress'] = len(df)
        geocoding_progress[progress_id]['successful_count'] = successful_geocodes
        geocoding_progress[progress_id]['failed_count'] = len(failed_addresses)
        geocoding_progress[progress_id]['has_failed_addresses'] = len(failed_addresses) > 0
        
        # Print summary
        print(f"Geocoding completed: {successful_geocodes}/{len(df)} addresses successfully geocoded")
        if failed_addresses:
            print(f"Failed to geocode {len(failed_addresses)} addresses")
        
    except Exception as e:
        print(f"Geocoding error: {str(e)}")
        import traceback
        traceback.print_exc()
        geocoding_progress[progress_id]['status'] = 'error'
        geocoding_progress[progress_id]['error'] = str(e)
    finally:
        # Clean up uploaded file
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
        
        # Clean up cancellation flag
        geocoding_cancel_flags.pop(progress_id, None)

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
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        dataset_name = request.form.get('dataset_name', '').strip()
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not dataset_name:
            return jsonify({'error': 'Dataset name is required'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only CSV files are allowed'}), 400
        
        # Ensure the main datasets directory exists
        try:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        except Exception as e:
            print(f"Error creating datasets directory: {str(e)}")
            return jsonify({'error': f'Cannot create datasets directory: {str(e)}'}), 500
        
        # Check if dataset already exists
        dataset_path = os.path.join(UPLOAD_FOLDER, dataset_name)
        if os.path.exists(dataset_path):
            return jsonify({'error': 'Dataset name already exists'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, f"temp_{uuid.uuid4()}_{filename}")
        
        try:
            file.save(temp_path)
        except Exception as e:
            print(f"Error saving uploaded file: {str(e)}")
            return jsonify({'error': f'Cannot save uploaded file: {str(e)}'}), 500
        
        # Start geocoding in background
        progress_id = str(uuid.uuid4())
        thread = threading.Thread(target=geocode_dataset, args=(dataset_name, temp_path, progress_id))
        thread.daemon = True
        thread.start()
        
        return jsonify({'progress_id': progress_id})
        
    except Exception as e:
        print(f"Upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/progress/<progress_id>')
def get_progress(progress_id):
    return jsonify(geocoding_progress.get(progress_id, {'status': 'not_found'}))

@app.route('/cancel_geocoding/<progress_id>', methods=['POST'])
def cancel_geocoding(progress_id):
    """Cancel an ongoing geocoding operation"""
    try:
        data = request.json
        dataset_name = data.get('dataset_name')
        
        if not dataset_name:
            return jsonify({'success': False, 'error': 'Dataset name is required'}), 400
        
        # Set cancellation flag
        geocoding_cancel_flags[progress_id] = True
        print(f"Cancellation requested for progress_id: {progress_id}, dataset: {dataset_name}")
        
        return jsonify({'success': True, 'message': 'Cancellation request sent'})
        
    except Exception as e:
        print(f"Error canceling geocoding: {str(e)}")
        return jsonify({'success': False, 'error': f'Failed to cancel geocoding: {str(e)}'}), 500

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
    session['current_dataset'] = dataset_name
    return redirect(url_for('index'))

@app.route('/clear_all_datasets', methods=['POST'])
def clear_all_datasets():
    """Clear all datasets and start fresh"""
    try:
        import shutil
        
        # Remove the entire datasets directory
        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
            print(f"Removed datasets directory: {UPLOAD_FOLDER}")
        
        # Recreate the empty datasets directory
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        print(f"Recreated datasets directory: {UPLOAD_FOLDER}")
        
        # Clear the current dataset from session
        session.pop('current_dataset', None)
        
        print("All datasets cleared successfully")
        return jsonify({'success': True, 'message': 'All datasets cleared successfully'})
        
    except Exception as e:
        print(f"Error clearing datasets: {str(e)}")
        # Try to recreate the directory even if deletion failed
        try:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            print(f"Recreated datasets directory after error: {UPLOAD_FOLDER}")
        except Exception as create_error:
            print(f"Error recreating datasets directory: {str(create_error)}")
        
        return jsonify({'success': False, 'error': f'Failed to clear datasets: {str(e)}'}), 500

@app.route('/delete_dataset/<dataset_name>', methods=['DELETE'])
def delete_dataset(dataset_name):
    """Delete a specific dataset"""
    try:
        import shutil
        
        # Construct the dataset path
        dataset_path = os.path.join(UPLOAD_FOLDER, dataset_name)
        
        # Check if dataset exists
        if not os.path.exists(dataset_path):
            return jsonify({'success': False, 'error': 'Dataset not found'}), 404
        
        # Remove the dataset directory
        shutil.rmtree(dataset_path)
        print(f"Removed dataset directory: {dataset_path}")
        
        # If this was the current dataset, clear it from session
        if session.get('current_dataset') == dataset_name:
            session.pop('current_dataset', None)
            print(f"Cleared current dataset from session: {dataset_name}")
        
        print(f"Dataset '{dataset_name}' deleted successfully")
        return jsonify({'success': True, 'message': f'Dataset "{dataset_name}" deleted successfully'})
        
    except Exception as e:
        print(f"Error deleting dataset '{dataset_name}': {str(e)}")
        return jsonify({'success': False, 'error': f'Failed to delete dataset: {str(e)}'}), 500

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
    
    output = io.StringIO()
    selected.to_csv(output, index=False)
    output.seek(0)
    
    filename = f'selected_addresses_{current_dataset or "default"}.csv'
    return send_file(io.BytesIO(output.getvalue().encode()), 
                     mimetype='text/csv', 
                     as_attachment=True, 
                     download_name=filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8765) 