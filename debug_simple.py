import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point

# Load data
df = pd.read_csv('data_solution/enhanced_air_quality_detailed.csv')
latest = df[df['date'] == df['date'].max()]

# Test coordinates around Sulaimani
sulaimani_lat, sulaimani_lon = 35.5647, 45.4164
buffer_size = 0.02

# Create polygon in the CORRECT format (st_folium [lat,lon] -> shapely [lon,lat])
coords_latlon = [
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon + buffer_size],
    [sulaimani_lat + buffer_size, sulaimani_lon + buffer_size], 
    [sulaimani_lat + buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size]
]

# Convert to shapely format [lon, lat]
shapely_coords = [(coord[1], coord[0]) for coord in coords_latlon]
polygon = Polygon(shapely_coords)

print(f"Polygon bounds: {polygon.bounds}")
print(f"Polygon area: {polygon.area:.8f}")

# Simple bounding box test first
bbox_count = 0
for _, row in latest.head(1000).iterrows():
    if (polygon.bounds[0] <= row['lon'] <= polygon.bounds[2] and 
        polygon.bounds[1] <= row['lat'] <= polygon.bounds[3]):
        bbox_count += 1

print(f"Points in bounding box (first 1000): {bbox_count}")

# Point-in-polygon test without buffer
pip_count = 0
pip_samples = []
for _, row in latest.head(1000).iterrows():
    point = Point(row['lon'], row['lat'])
    if polygon.contains(point):
        pip_count += 1
        if len(pip_samples) < 3:
            pip_samples.append((row['lat'], row['lon']))

print(f"Points in polygon (first 1000): {pip_count}")
if pip_samples:
    print("Sample points found:")
    for lat, lon in pip_samples:
        print(f"  ({lat:.6f}, {lon:.6f})")

# Test with buffer
buffered = polygon.buffer(0.001)
buffered_count = 0
for _, row in latest.head(1000).iterrows():
    point = Point(row['lon'], row['lat'])  
    if buffered.contains(point):
        buffered_count += 1

print(f"Points in buffered polygon (first 1000): {buffered_count}")

# Test specific point that should be inside
test_lat, test_lon = 35.5647, 45.4164  # Sulaimani center
test_point = Point(test_lon, test_lat)  
print(f"Sulaimani center in polygon: {polygon.contains(test_point)}")
print(f"Sulaimani center in buffered: {buffered.contains(test_point)}")

# Test with much larger buffer
large_buffered = polygon.buffer(0.01)  # 10x larger
large_count = 0
for _, row in latest.head(1000).iterrows():
    point = Point(row['lon'], row['lat'])
    if large_buffered.contains(point):
        large_count += 1

print(f"Points in large buffered polygon (first 1000): {large_count}")