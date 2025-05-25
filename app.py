from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
import folium
import io
import math
from folium import Element

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
    # Center on Dallas, TX
    m = folium.Map(location=[32.7767, -96.7970], zoom_start=11)
    
    # Add markers
    for idx, row in df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Family Name']}<br>{row['Address']}<br>{row['City']}, {row['State']} {row['Zip']}",
            tooltip=f"{row['Family Name']}"
        ).add_to(m)

    # Add custom JavaScript for circle drawing and export functionality
    custom_js = """
    <script>
        var addressData = """ + df.to_json(orient='records') + """;
        var currentCircle = null;
        var mapVar = null;
        
        function initializeMap() {
            for (let key in window) {
                if (key.startsWith('map_') && window[key] && window[key].on) {
                    mapVar = window[key];
                    break;
                }
            }
            
            if (!mapVar) {
                console.error('Map not found');
                return;
            }
            
            // Add click handler for drawing circles
            mapVar.on('click', function(e) {
                if (currentCircle) {
                    mapVar.removeLayer(currentCircle);
                }
                
                // Create a circle with 1000m radius at clicked location
                currentCircle = L.circle(e.latlng, {
                    color: 'red',
                    fillColor: '#f03',
                    fillOpacity: 0.3,
                    radius: 1000
                }).addTo(mapVar);
                
                // Show export button
                document.getElementById('exportBtn').style.display = 'block';
            });
        }
        
        function exportCircleSelection() {
            if (!currentCircle || !mapVar) {
                alert('Please click on the map to create a circle first!');
                return;
            }
            
            var center = currentCircle.getLatLng();
            var radius = currentCircle.getRadius();
            
            var selectedAddresses = [];
            addressData.forEach(function(addr) {
                var distance = mapVar.distance(
                    [addr.Latitude, addr.Longitude],
                    [center.lat, center.lng]
                );
                if (distance <= radius) {
                    selectedAddresses.push(addr);
                }
            });
            
            if (selectedAddresses.length === 0) {
                alert('No addresses found within the circle!');
                return;
            }
            
            // Convert to CSV and download
            var csv = 'Family Name,Address,City,State,Zip,Latitude,Longitude\\n';
            selectedAddresses.forEach(function(addr) {
                csv += '"' + (addr['Family Name'] || '').replace(/"/g, '""') + '","' + 
                       (addr.Address || '').replace(/"/g, '""') + '","' + 
                       (addr.City || '').replace(/"/g, '""') + '","' + 
                       (addr.State || '').replace(/"/g, '""') + '","' + 
                       (addr.Zip || '').replace(/"/g, '""') + '",' + 
                       addr.Latitude + ',' + addr.Longitude + '\\n';
            });
            
            var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'selected_addresses.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            alert('Exported ' + selectedAddresses.length + ' addresses to CSV!');
        }
        
        // Initialize when page loads
        window.addEventListener('load', function() {
            setTimeout(function() {
                initializeMap();
                
                // Add instructions
                var instructions = document.createElement('div');
                instructions.innerHTML = 'Click anywhere on the map to create a selection circle';
                instructions.style.position = 'absolute';
                instructions.style.top = '10px';
                instructions.style.left = '10px';
                instructions.style.zIndex = '1000';
                instructions.style.padding = '10px';
                instructions.style.backgroundColor = 'rgba(255,255,255,0.9)';
                instructions.style.border = '1px solid #ccc';
                instructions.style.borderRadius = '5px';
                instructions.style.fontSize = '14px';
                document.body.appendChild(instructions);
                
                // Add export button (initially hidden)
                var button = document.createElement('button');
                button.id = 'exportBtn';
                button.innerHTML = 'Export Addresses in Circle to CSV';
                button.style.position = 'absolute';
                button.style.top = '60px';
                button.style.left = '10px';
                button.style.zIndex = '1000';
                button.style.padding = '10px 15px';
                button.style.backgroundColor = '#28a745';
                button.style.color = 'white';
                button.style.border = 'none';
                button.style.borderRadius = '5px';
                button.style.cursor = 'pointer';
                button.style.fontSize = '14px';
                button.style.fontWeight = 'bold';
                button.style.display = 'none';
                button.onclick = exportCircleSelection;
                document.body.appendChild(button);
            }, 1000);
        });
    </script>
    """
    m.get_root().html.add_child(Element(custom_js))
    map_html = m._repr_html_()
    return render_template('map.html', map_html=map_html)

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