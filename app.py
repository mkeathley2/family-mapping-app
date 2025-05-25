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
COLUMNS = ['Family Name', 'Address', 'City', 'State', 'Zip']

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global progress tracking
geocoding_progress = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_datasets():
    """Get list of all available datasets"""
    datasets = []
    if os.path.exists(UPLOAD_FOLDER):
        for item in os.listdir(UPLOAD_FOLDER):
            dataset_path = os.path.join(UPLOAD_FOLDER, item)
            if os.path.isdir(dataset_path):
                cache_file = os.path.join(dataset_path, 'geocoded_cache.csv')
                if os.path.exists(cache_file):
                    # Get file modification time
                    mod_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
                    # Count addresses
                    try:
                        df = pd.read_csv(cache_file)
                        count = len(df)
                    except:
                        count = 0
                    datasets.append({
                        'name': item,
                        'path': dataset_path,
                        'last_modified': mod_time.strftime('%Y-%m-%d %H:%M'),
                        'address_count': count
                    })
    return sorted(datasets, key=lambda x: x['last_modified'], reverse=True)

def load_valid_addresses(dataset_name=None):
    """Load addresses from a specific dataset or default"""
    if dataset_name:
        cache_file = os.path.join(UPLOAD_FOLDER, dataset_name, 'geocoded_cache.csv')
    else:
        cache_file = 'geocoded_cache.csv'  # Default legacy file
    
    if not os.path.exists(cache_file):
        return pd.DataFrame()
    
    df = pd.read_csv(cache_file)
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
        raw_df = pd.read_csv(csv_file_path)
        
        # Try to map columns automatically
        df_columns = raw_df.columns.tolist()
        column_mapping = {}
        
        # Simple column mapping logic
        for col in df_columns:
            col_lower = col.lower()
            if 'family' in col_lower or 'name' in col_lower:
                column_mapping['Family Name'] = col
            elif 'address' in col_lower and 'email' not in col_lower:
                column_mapping['Address'] = col
            elif 'city' in col_lower:
                column_mapping['City'] = col
            elif 'state' in col_lower:
                column_mapping['State'] = col
            elif 'zip' in col_lower or 'postal' in col_lower:
                column_mapping['Zip'] = col
        
        # If we have the exact columns, use them directly
        if all(col in df_columns for col in COLUMNS):
            df = raw_df[COLUMNS]
        elif len(column_mapping) >= 3:  # At least address, city, state
            # Rename columns to match our expected format
            df = raw_df.rename(columns=column_mapping)
            # Fill missing columns with empty strings
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = ''
            df = df[COLUMNS]
        else:
            # Use first 5 columns and hope for the best
            df = raw_df.iloc[:, :5]
            df.columns = COLUMNS
        
        geocoding_progress[progress_id]['total'] = len(df)
        geocoding_progress[progress_id]['status'] = 'geocoding'
        
        # Setup geocoder
        geolocator = Nominatim(user_agent="family_mapper_v2")
        rate_limiter = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        
        # Geocode addresses
        results = []
        for idx, row in df.iterrows():
            address = f"{row['Address']}, {row['City']}, {row['State']} {row['Zip']}"
            geocoding_progress[progress_id]['current_address'] = address
            geocoding_progress[progress_id]['progress'] = idx
            
            try:
                location = rate_limiter(address)
                if location:
                    results.append({
                        **row.to_dict(),
                        'Latitude': location.latitude,
                        'Longitude': location.longitude
                    })
                else:
                    results.append({
                        **row.to_dict(),
                        'Latitude': None,
                        'Longitude': None
                    })
            except Exception as e:
                results.append({
                    **row.to_dict(),
                    'Latitude': None,
                    'Longitude': None
                })
        
        # Save results
        result_df = pd.DataFrame(results)
        cache_file = os.path.join(dataset_path, 'geocoded_cache.csv')
        result_df.to_csv(cache_file, index=False)
        
        # Copy original file
        original_file = os.path.join(dataset_path, 'original.csv')
        raw_df.to_csv(original_file, index=False)
        
        geocoding_progress[progress_id]['status'] = 'completed'
        geocoding_progress[progress_id]['completed'] = True
        geocoding_progress[progress_id]['progress'] = len(df)
        
    except Exception as e:
        geocoding_progress[progress_id]['status'] = 'error'
        geocoding_progress[progress_id]['error'] = str(e)
    finally:
        # Clean up uploaded file
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)

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
    response = app.make_response(render_template('map.html', 
                                                addresses_json=addresses_json,
                                                datasets=datasets,
                                                current_dataset=current_dataset))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/upload', methods=['POST'])
def upload_file():
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
    
    # Check if dataset already exists
    dataset_path = os.path.join(UPLOAD_FOLDER, dataset_name)
    if os.path.exists(dataset_path):
        return jsonify({'error': 'Dataset name already exists'}), 400
    
    # Save uploaded file temporarily
    filename = secure_filename(file.filename)
    temp_path = os.path.join(UPLOAD_FOLDER, f"temp_{uuid.uuid4()}_{filename}")
    file.save(temp_path)
    
    # Start geocoding in background
    progress_id = str(uuid.uuid4())
    thread = threading.Thread(target=geocode_dataset, args=(dataset_name, temp_path, progress_id))
    thread.daemon = True
    thread.start()
    
    return jsonify({'progress_id': progress_id})

@app.route('/progress/<progress_id>')
def get_progress(progress_id):
    return jsonify(geocoding_progress.get(progress_id, {'status': 'not_found'}))

@app.route('/switch_dataset/<dataset_name>')
def switch_dataset(dataset_name):
    session['current_dataset'] = dataset_name
    return redirect(url_for('index'))

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
    
    output = io.StringIO()
    selected.to_csv(output, index=False)
    output.seek(0)
    
    filename = f'selected_addresses_{current_dataset or "default"}.csv'
    return send_file(io.BytesIO(output.getvalue().encode()), 
                     mimetype='text/csv', 
                     as_attachment=True, 
                     download_name=filename)

if __name__ == '__main__':
    app.run(debug=True) 