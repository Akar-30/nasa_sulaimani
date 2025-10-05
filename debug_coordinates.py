import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point

# Load a small sample to check coordinate formats
df = pd.read_csv('data_solution/enhanced_air_quality_detailed.csv', nrows=5)
print("Air quality data sample (first 5 rows):")
print(df[['lat', 'lon']].to_string())
print()

df2 = pd.read_csv('data_solution/enhanced_topography_detailed.csv', nrows=5)
print("Topography data sample (first 5 rows):")
print(df2[['lat', 'lon']].to_string())
print()

# Test st_folium coordinate format
# st_folium typically returns coordinates as [lat, lon]
sulaimani_lat, sulaimani_lon = 35.5647, 45.4164
buffer_size = 0.01

# Simulate st_folium polygon drawing coordinates
st_folium_coords = [
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size],  # [lat, lon]
    [sulaimani_lat - buffer_size, sulaimani_lon + buffer_size],
    [sulaimani_lat + buffer_size, sulaimani_lon + buffer_size], 
    [sulaimani_lat + buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size]
]

print("st_folium format coordinates (lat, lon):")
for coord in st_folium_coords[:4]:
    print(f"  [{coord[0]:.6f}, {coord[1]:.6f}]")
print()

# Test both coordinate interpretations
print("Testing coordinate formats:")

# Format 1: Assume st_folium coords are [lat, lon], convert to shapely [lon, lat]
coords_format1 = [(coord[1], coord[0]) for coord in st_folium_coords]  # swap to [lon, lat]
polygon1 = Polygon(coords_format1)
buffered1 = polygon1.buffer(0.001)

# Format 2: Assume st_folium coords are already [lon, lat] 
coords_format2 = [(coord[0], coord[1]) for coord in st_folium_coords]  # keep as is
polygon2 = Polygon(coords_format2)
buffered2 = polygon2.buffer(0.001)

print(f"Format 1 (swapped) bounds: {polygon1.bounds}")
print(f"Format 2 (direct) bounds: {polygon2.bounds}")
print()

# Test against actual data
for _, row in df.iterrows():
    point = Point(row['lon'], row['lat'])
    in_poly1 = buffered1.contains(point)
    in_poly2 = buffered2.contains(point)
    print(f"Point ({row['lat']:.6f}, {row['lon']:.6f}): Format1={in_poly1}, Format2={in_poly2}")
    break