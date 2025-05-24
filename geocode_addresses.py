import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import os

INPUT_CSV = 'addresses.csv'
CACHE_CSV = 'geocoded_cache.csv'

# Columns to use
COLUMNS = ['Family Name', 'Address', 'City', 'State', 'Zip']

# Read the input CSV
raw_df = pd.read_csv(INPUT_CSV, header=None)
raw_df.columns = ['Family Name', 'Address', 'Unused', 'City', 'State', 'Zip', 'ID']
df = raw_df[COLUMNS]

# Load cache if exists
if os.path.exists(CACHE_CSV):
    cache_df = pd.read_csv(CACHE_CSV)
else:
    cache_df = pd.DataFrame(columns=COLUMNS + ['Latitude', 'Longitude'])

# Merge to find which addresses need geocoding
merged = pd.merge(df, cache_df, on=COLUMNS, how='left', indicator=True)
to_geocode = merged[merged['_merge'] == 'left_only'][COLUMNS]

print(f"{len(to_geocode)} addresses to geocode (out of {len(df)})")

# Setup geocoder
geolocator = Nominatim(user_agent="family_mapper")
rate_limiter = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def geocode_address(row):
    address = f"{row['Address']}, {row['City']}, {row['State']} {row['Zip']}"
    print(f"Geocoding: {address}")
    location = None
    try:
        location = rate_limiter(address)
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
    if location:
        return pd.Series({'Latitude': location.latitude, 'Longitude': location.longitude})
    else:
        return pd.Series({'Latitude': None, 'Longitude': None})

if not to_geocode.empty:
    for idx, row in to_geocode.iterrows():
        start = time.time()
        latlon = geocode_address(row)
        for col in ['Latitude', 'Longitude']:
            to_geocode.at[idx, col] = latlon[col]
        elapsed = time.time() - start
        if elapsed < 1:
            pause = 1 - elapsed
            print(f"Pausing for {pause:.2f} seconds to respect Nominatim's rate limit...")
            time.sleep(pause)
else:
    print("No new addresses to geocode.")

# Combine and save cache
new_cache = pd.concat([cache_df, to_geocode[COLUMNS + ['Latitude', 'Longitude']]], ignore_index=True)
new_cache = new_cache.drop_duplicates(subset=COLUMNS)
new_cache.to_csv(CACHE_CSV, index=False)
print(f"Geocoding complete. Cached results in {CACHE_CSV}") 