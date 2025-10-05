import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point

# Simulate what st_folium actually returns in GeoJSON format
# GeoJSON coordinates are [longitude, latitude] format
sulaimani_lat, sulaimani_lon = 35.5647, 45.4164
buffer_size = 0.02

# st_folium GeoJSON polygon coordinates in [lon, lat] format
geojson_coords = [
    [sulaimani_lon - buffer_size, sulaimani_lat - buffer_size],  # [lon, lat]
    [sulaimani_lon - buffer_size, sulaimani_lat + buffer_size],
    [sulaimani_lon + buffer_size, sulaimani_lat + buffer_size],
    [sulaimani_lon + buffer_size, sulaimani_lat - buffer_size],
    [sulaimani_lon - buffer_size, sulaimani_lat - buffer_size]
]

print("GeoJSON coordinates ([lon, lat] format):")
for coord in geojson_coords[:4]:
    print(f"  [{coord[0]:.6f}, {coord[1]:.6f}]")

# Current Enhanced Solution processing assumes these are [lat, lon] and swaps them
# This is WRONG!
wrong_coords = [(coord[1], coord[0]) for coord in geojson_coords]  # thinking it's [lat,lon] -> [lon,lat]
wrong_polygon = Polygon(wrong_coords)

# Correct processing: GeoJSON coords are already [lon, lat] for shapely  
correct_coords = [(coord[0], coord[1]) for coord in geojson_coords]  # keep as [lon, lat]
correct_polygon = Polygon(correct_coords)

print(f"\nWrong polygon bounds: {wrong_polygon.bounds}")
print(f"Correct polygon bounds: {correct_polygon.bounds}")

# Test against air quality data
df = pd.read_csv('data_solution/enhanced_air_quality_detailed.csv')
latest_aqi = df[df['date'] == df['date'].max()]

# Test wrong processing
wrong_buffered = wrong_polygon.buffer(0.001)
wrong_count = 0
for _, row in latest_aqi.head(1000).iterrows():
    point = Point(row['lon'], row['lat'])
    if wrong_buffered.contains(point):
        wrong_count += 1

# Test correct processing  
correct_buffered = correct_polygon.buffer(0.001)
correct_count = 0
for _, row in latest_aqi.head(1000).iterrows():
    point = Point(row['lon'], row['lat'])  
    if correct_buffered.contains(point):
        correct_count += 1

print(f"\nWrong processing points found: {wrong_count}")
print(f"Correct processing points found: {correct_count}")
print()

# The fix: Don't swap coordinates from st_folium GeoJSON
print("FIX: Use GeoJSON coordinates directly as [lon, lat] for shapely")