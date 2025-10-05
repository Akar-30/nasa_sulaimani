import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point

# Load full latest data
df = pd.read_csv('data_solution/enhanced_air_quality_detailed.csv')
latest = df[df['date'] == df['date'].max()]
print(f"Latest data shape: {latest.shape}")

# Create Sulaimani polygon (correct format)
sulaimani_lat, sulaimani_lon = 35.5647, 45.4164
buffer_size = 0.02

coords_latlon = [
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon + buffer_size],
    [sulaimani_lat + buffer_size, sulaimani_lon + buffer_size],
    [sulaimani_lat + buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size]
]

shapely_coords = [(coord[1], coord[0]) for coord in coords_latlon]  # [lat,lon] -> [lon,lat]
polygon = Polygon(shapely_coords)
buffered_polygon = polygon.buffer(0.001)

print(f"Polygon bounds: {polygon.bounds}")

# Test with FULL dataset like Enhanced Solution does
print("Testing with full latest dataset...")
points_in_area = []
processed_count = 0
start_time = pd.Timestamp.now()

for _, row in latest.iterrows():
    processed_count += 1
    if processed_count % 50000 == 0:
        elapsed = (pd.Timestamp.now() - start_time).total_seconds()
        print(f"  Processed {processed_count:,} points in {elapsed:.1f}s...")
    
    point = Point(row['lon'], row['lat'])
    if buffered_polygon.contains(point):
        points_in_area.append(row['aqi_score'])
        
    # Stop early if we find enough points to confirm it works
    if len(points_in_area) >= 10:
        print(f"  Found {len(points_in_area)} points after {processed_count:,} rows - stopping early")
        break

print(f"\nFinal results:")
print(f"Points processed: {processed_count:,}")
print(f"Points in polygon: {len(points_in_area)}")

if points_in_area:
    print(f"Sample AQI scores: {points_in_area[:5]}")
    avg_aqi = np.mean(points_in_area)
    score = max(0, 100 - avg_aqi) 
    print(f"Average AQI: {avg_aqi:.1f}")
    print(f"Air quality score: {score:.1f}")
    print("✅ ENHANCED SOLUTION LOGIC IS WORKING!")
else:
    print("❌ Still no points found")