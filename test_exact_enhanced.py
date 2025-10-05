import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point

# Load air quality data and filter to latest date (exactly like Enhanced Solution)
df = pd.read_csv('data_solution/enhanced_air_quality_detailed.csv')
latest_aqi = df[df['date'] == df['date'].max()]
print(f"Latest air quality data: {len(latest_aqi)} points")

# Test with Sulaimani coordinates  
sulaimani_lat, sulaimani_lon = 35.5647, 45.4164
buffer_size = 0.02

# Simulate st_folium polygon coordinates [lat, lon] format
polygon_coords = [
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon + buffer_size],  
    [sulaimani_lat + buffer_size, sulaimani_lon + buffer_size],
    [sulaimani_lat + buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size]
]

# Convert st_folium [lat, lon] to shapely [lon, lat] (exactly like Enhanced Solution)
shapely_coords = [(coord[1], coord[0]) for coord in polygon_coords]
polygon = Polygon(shapely_coords)
buffered_polygon = polygon.buffer(0.001)

print(f"Polygon bounds: {polygon.bounds}")
print(f"Buffered polygon bounds: {buffered_polygon.bounds}")

# Test the exact same logic as Enhanced Solution air quality analysis
points_in_area = []
test_count = 0
for _, row in latest_aqi.iterrows():
    test_count += 1
    if test_count > 10000:  # Test first 10k points like we confirmed work
        break
        
    point = Point(row['lon'], row['lat'])
    if buffered_polygon.contains(point):
        points_in_area.append(row['aqi_score'])

print(f"Points tested: {test_count}")
print(f"Points found in polygon: {len(points_in_area)}")

if points_in_area:
    print(f"Sample AQI scores: {points_in_area[:5]}")
    avg_aqi = np.mean(points_in_area)
    score = max(0, 100 - avg_aqi)
    print(f"Average AQI: {avg_aqi:.1f}")
    print(f"Air quality score: {score:.1f}")
else:
    print("No points found - debugging...")
    # Test a few specific points
    sample_points = latest_aqi.head(5)
    for _, row in sample_points.iterrows():
        point = Point(row['lon'], row['lat'])
        in_polygon = buffered_polygon.contains(point)
        print(f"  Point ({row['lat']:.6f}, {row['lon']:.6f}): {in_polygon}")