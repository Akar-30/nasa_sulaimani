import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point

# Load data
df = pd.read_csv('data_solution/enhanced_air_quality_detailed.csv') 
latest_aqi = df[df['date'] == df['date'].max()]
print(f"Data range: lat {df['lat'].min():.6f}-{df['lat'].max():.6f}, lon {df['lon'].min():.6f}-{df['lon'].max():.6f}")

# Working coordinates from our successful test
sulaimani_lat, sulaimani_lon = 35.5647, 45.4164
buffer_size = 0.02

# Format that worked: [lat, lon] input converted to [lon, lat] for shapely
working_input = [
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon + buffer_size], 
    [sulaimani_lat + buffer_size, sulaimani_lon + buffer_size],
    [sulaimani_lat + buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size]
]
working_shapely = [(coord[1], coord[0]) for coord in working_input]
working_polygon = Polygon(working_shapely).buffer(0.001)

# Test working version
working_count = 0
for _, row in latest_aqi.head(1000).iterrows():
    point = Point(row['lon'], row['lat'])
    if working_polygon.contains(point):
        working_count += 1

print(f"Working format points found: {working_count}")
print(f"Working polygon bounds: {working_polygon.bounds}")

# Now test what st_folium ACTUALLY returns
# Looking at Enhanced Solution code, it extracts: latest_drawing['geometry']['coordinates'][0]
# Let's simulate different possible st_folium formats

print("\nTesting possible st_folium formats:")

# Option 1: st_folium returns [lon, lat] (GeoJSON standard)
option1_coords = [
    [sulaimani_lon - buffer_size, sulaimani_lat - buffer_size], 
    [sulaimani_lon - buffer_size, sulaimani_lat + buffer_size],
    [sulaimani_lon + buffer_size, sulaimani_lat + buffer_size],
    [sulaimani_lon + buffer_size, sulaimani_lat - buffer_size],
    [sulaimani_lon - buffer_size, sulaimani_lat - buffer_size]
]

# Option 2: st_folium returns [lat, lon] (unusual but possible)  
option2_coords = [
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon + buffer_size],
    [sulaimani_lat + buffer_size, sulaimani_lon + buffer_size], 
    [sulaimani_lat + buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size]
]

# Test both options with Enhanced Solution's current processing
# Current code: shapely_coords = [(coord[1], coord[0]) for coord in coords]

# Option 1 + current processing: [lon,lat] -> swap -> [lat,lon] = WRONG
opt1_processed = [(coord[1], coord[0]) for coord in option1_coords]
opt1_polygon = Polygon(opt1_processed).buffer(0.001)

# Option 2 + current processing: [lat,lon] -> swap -> [lon,lat] = CORRECT  
opt2_processed = [(coord[1], coord[0]) for coord in option2_coords]
opt2_polygon = Polygon(opt2_processed).buffer(0.001)

opt1_count = sum(1 for _, row in latest_aqi.head(1000).iterrows() 
                 if opt1_polygon.contains(Point(row['lon'], row['lat'])))

opt2_count = sum(1 for _, row in latest_aqi.head(1000).iterrows()
                 if opt2_polygon.contains(Point(row['lon'], row['lat'])))

print(f"Option 1 ([lon,lat] from st_folium): {opt1_count} points")  
print(f"Option 2 ([lat,lon] from st_folium): {opt2_count} points")

print(f"Option 1 bounds: {opt1_polygon.bounds}")
print(f"Option 2 bounds: {opt2_polygon.bounds}")
print(f"Working bounds: {working_polygon.bounds}")

# Check which matches our working solution
if np.allclose(opt2_polygon.bounds, working_polygon.bounds, atol=1e-6):
    print("\n✅ SOLUTION: st_folium returns [lat, lon], current processing is CORRECT")
elif np.allclose(opt1_polygon.bounds, working_polygon.bounds, atol=1e-6):  
    print("\n❌ st_folium returns [lon, lat], current processing is WRONG - need to fix")
else:
    print("\n❓ Neither matches - investigate further")