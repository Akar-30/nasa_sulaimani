import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point

df = pd.read_csv('data_solution/enhanced_topography_detailed.csv')
sulaimani_lat, sulaimani_lon = 35.5647, 45.4164
buffer_size = 0.01

print('DEBUGGING POLYGON vs DATA')

# Test polygon coordinates (st_folium format)
coords = [
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon + buffer_size],
    [sulaimani_lat + buffer_size, sulaimani_lon + buffer_size],
    [sulaimani_lat + buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size]
]

print('Original polygon coords (lat, lon):')
for coord in coords[:4]:
    print(f'  [{coord[0]:.6f}, {coord[1]:.6f}]')

# Convert to shapely format [lon, lat]
shapely_coords = [(coord[1], coord[0]) for coord in coords]
polygon = Polygon(shapely_coords)
buffered = polygon.buffer(0.001)

print(f'Polygon bounds (lon, lat): {polygon.bounds}')
print(f'Buffered bounds (lon, lat): {buffered.bounds}')

# Test actual polygon intersection
points_in_polygon = 0
for i, row in df.iterrows():
    if i > 1000: break  # Test first 1000 points
    point = Point(row['lon'], row['lat'])
    if buffered.contains(point):
        points_in_polygon += 1

print(f'Points in polygon (first 1000): {points_in_polygon}')

# Test specific point near center
closest_row = df.iloc[np.sqrt((df['lat'] - sulaimani_lat)**2 + (df['lon'] - sulaimani_lon)**2).idxmin()]
test_point = Point(closest_row['lon'], closest_row['lat'])
print(f'Closest point: {closest_row["lat"]:.6f}, {closest_row["lon"]:.6f}')
print(f'Point in buffered polygon: {buffered.contains(test_point)}')