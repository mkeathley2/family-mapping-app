from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
import io
import math
import json
import time

app = Flask(__name__)

def load_valid_addresses():
    df = pd.read_csv('geocoded_cache.csv')
    # Filter out rows with missing or invalid lat/lon
    df = df.dropna(subset=['Latitude', 'Longitude'])
    df = df[(df['Latitude'].apply(lambda x: isinstance(x, (int, float)) or str(x).replace('.', '', 1).isdigit())) &
            (df['Longitude'].apply(lambda x: isinstance(x, (int, float)) or str(x).replace('.', '', 1).isdigit()))]
    df['Latitude'] = df['Latitude'].astype(float)
    df['Longitude'] = df['Longitude'].astype(float)
    return df

@app.route('/')
def index():
    df = load_valid_addresses()
    addresses_json = df.to_json(orient='records')
    response = app.make_response(render_template('map.html', addresses_json=addresses_json))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/export_csv', methods=['POST'])
def export_csv():
    data = request.json
    center = data['center']  # [lat, lng]
    radius = data['radius']  # in meters
    df = load_valid_addresses()
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
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='selected_addresses.csv')

if __name__ == '__main__':
    app.run(debug=True) 