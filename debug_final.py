import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point

# Load data
df = pd.read_csv('data_solution/enhanced_air_quality_detailed.csv')
sulaimani_lat, sulaimani_lon = 35.5647, 45.4164

# Simulate st_folium drawing around Sulaimani
# When user draws on map, st_folium returns coordinates in [lat, lon] format
buffer_size = 0.02  # Larger area
drawn_coords = [
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size],  # st_folium format: [lat, lon]
    [sulaimani_lat - buffer_size, sulaimani_lon + buffer_size],
    [sulaimani_lat + buffer_size, sulaimani_lon + buffer_size],
    [sulaimani_lat + buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size]
]

print("st_folium drawn coordinates ([lat, lon] format):")
for coord in drawn_coords[:4]:
    print(f"  [{coord[0]:.6f}, {coord[1]:.6f}]")

# Current Enhanced Solution processing (INCORRECT)
# It converts [lat, lon] to [lon, lat] for shapely
incorrect_coords = [(coord[1], coord[0]) for coord in drawn_coords]  # swap to [lon, lat]
incorrect_polygon = Polygon(incorrect_coords)
incorrect_buffered = incorrect_polygon.buffer(0.001)

print(f"\nIncorrect polygon bounds (lon, lat): {incorrect_polygon.bounds}")

# Count points with incorrect processing
incorrect_count = 0
for _, row in df.head(1000).iterrows():
    point = Point(row['lon'], row['lat'])
    if incorrect_buffered.contains(point):
        incorrect_count += 1

print(f"Points found with INCORRECT processing (first 1000): {incorrect_count}")

# CORRECT processing: st_folium [lat, lon] should become shapely [lon, lat]
# But wait - let me check what format st_folium actually returns...
print("\nTesting correct coordinate conversion:")

# Actually, if st_folium returns [lat, lon], then to create shapely polygon [lon, lat]:
correct_coords = [(coord[1], coord[0]) for coord in drawn_coords]  # This IS correct!
correct_polygon = Polygon(correct_coords)
correct_buffered = correct_polygon.buffer(0.001)

print(f"Polygon bounds (lon, lat): {correct_polygon.bounds}")

# The real issue might be the buffer size or coordinate precision
correct_count = 0
sample_points = []
for _, row in df.head(10000).iterrows():  # Test more points
    point = Point(row['lon'], row['lat'])
    if correct_buffered.contains(point):
        correct_count += 1
        if len(sample_points) < 5:
            sample_points.append((row['lat'], row['lon']))

print(f"Points found with correct processing (first 10000): {correct_count}")
if sample_points:
    print("Sample points found:")
    for lat, lon in sample_points:
        print(f"  ({lat:.6f}, {lon:.6f})")

# Test with larger buffer
larger_buffered = correct_polygon.buffer(0.005)  # 5x larger buffer
larger_count = 0
for _, row in df.head(1000).iterrows():
    point = Point(row['lon'], row['lat'])
    if larger_buffered.contains(point):
        larger_count += 1

print(f"Points with larger buffer (first 1000): {larger_count}")