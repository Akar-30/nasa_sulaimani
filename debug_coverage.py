import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point

# Load air quality data to check actual coverage
df = pd.read_csv('data_solution/enhanced_air_quality_detailed.csv')
print(f"Air quality data coverage:")
print(f"  Latitude range: {df['lat'].min():.6f} to {df['lat'].max():.6f}")
print(f"  Longitude range: {df['lon'].min():.6f} to {df['lon'].max():.6f}")
print(f"  Total points: {len(df)}")
print()

# Check Sulaimani city center coordinates
sulaimani_lat, sulaimani_lon = 35.5647, 45.4164
print(f"Sulaimani center: {sulaimani_lat}, {sulaimani_lon}")
print()

# Find closest data points to Sulaimani center
distances = np.sqrt((df['lat'] - sulaimani_lat)**2 + (df['lon'] - sulaimani_lon)**2)
closest_indices = distances.nsmallest(10).index

print("10 closest data points to Sulaimani center:")
for idx in closest_indices:
    row = df.iloc[idx]
    dist = distances[idx]
    print(f"  Point {idx}: ({row['lat']:.6f}, {row['lon']:.6f}) - Distance: {dist:.6f}")

# Test if data exists around Sulaimani center
buffer = 0.1  # Large buffer to capture nearby points
nearby_points = df[
    (df['lat'] >= sulaimani_lat - buffer) & 
    (df['lat'] <= sulaimani_lat + buffer) &
    (df['lon'] >= sulaimani_lon - buffer) & 
    (df['lon'] <= sulaimani_lon + buffer)
]

print(f"\nPoints within {buffer} degrees of Sulaimani center: {len(nearby_points)}")

if len(nearby_points) > 0:
    print("Sample nearby points:")
    for _, row in nearby_points.head(5).iterrows():
        print(f"  ({row['lat']:.6f}, {row['lon']:.6f})")