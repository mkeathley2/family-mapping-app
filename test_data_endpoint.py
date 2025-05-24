import requests

url = 'http://127.0.0.1:5000/data'
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print('Received data rows:', len(data))
    if len(data) > 0:
        print('First row:', data[0])
    else:
        print('No data rows received.')
else:
    print('Failed to fetch /data endpoint:', response.status_code) 