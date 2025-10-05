#!/usr/bin/env python3
"""
Quick diagnostic script to check coordinate system
"""
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon

print("🔍 COORDINATE SYSTEM DIAGNOSTIC")
print("="*50)

# Load sample data to check coordinate ranges
try:
    topo_data = pd.read_csv('data_solution/enhanced_topography_detailed.csv')
    print(f"✅ Loaded topography data: {len(topo_data)} points")
    print(f"📊 Latitude range: {topo_data['lat'].min():.6f} to {topo_data['lat'].max():.6f}")
    print(f"📊 Longitude range: {topo_data['lon'].min():.6f} to {topo_data['lon'].max():.6f}")
    
    # Test different polygon coordinate formats
    sulaimani_lat, sulaimani_lon = 35.5647, 45.4164
    buffer_size = 0.01
    
    # Format 1: [lat, lon] pairs (st_folium format)
    coords_format1 = [
        [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size],
        [sulaimani_lat - buffer_size, sulaimani_lon + buffer_size], 
        [sulaimani_lat + buffer_size, sulaimani_lon + buffer_size],
        [sulaimani_lat + buffer_size, sulaimani_lon - buffer_size],
        [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size]
    ]
    
    # Format 2: [lon, lat] pairs (shapely format)
    coords_format2 = [
        [sulaimani_lon - buffer_size, sulaimani_lat - buffer_size],
        [sulaimani_lon + buffer_size, sulaimani_lat - buffer_size], 
        [sulaimani_lon + buffer_size, sulaimani_lat + buffer_size],
        [sulaimani_lon - buffer_size, sulaimani_lat + buffer_size],
        [sulaimani_lon - buffer_size, sulaimani_lat - buffer_size]
    ]
    
    print(f"\n🧪 TESTING POLYGON FORMATS")
    print(f"Test center: {sulaimani_lat:.6f}°N, {sulaimani_lon:.6f}°E")
    
    # Test Format 1: st_folium [lat, lon] -> shapely [lon, lat] 
    try:
        shapely_coords1 = [(coord[1], coord[0]) for coord in coords_format1]
        polygon1 = Polygon(shapely_coords1)
        
        points_found = 0
        for _, row in topo_data.iterrows():
            point = Point(row['lon'], row['lat'])
            if polygon1.buffer(0.001).contains(point):
                points_found += 1
        
        print(f"🔸 Format 1 [lat,lon]->shapely[lon,lat]: {points_found} points found")
        print(f"   Polygon bounds: {polygon1.bounds}")
        
    except Exception as e:
        print(f"❌ Format 1 error: {e}")
    
    # Test Format 2: Direct [lon, lat]
    try:
        polygon2 = Polygon(coords_format2)
        
        points_found = 0
        for _, row in topo_data.iterrows():
            point = Point(row['lon'], row['lat'])
            if polygon2.buffer(0.001).contains(point):
                points_found += 1
        
        print(f"🔸 Format 2 direct [lon,lat]: {points_found} points found")
        print(f"   Polygon bounds: {polygon2.bounds}")
        
    except Exception as e:
        print(f"❌ Format 2 error: {e}")

    # Show sample data points near center
    print(f"\n📍 SAMPLE DATA POINTS NEAR CENTER:")
    distances = np.sqrt((topo_data['lat'] - sulaimani_lat)**2 + (topo_data['lon'] - sulaimani_lon)**2)
    closest_5 = topo_data.iloc[distances.argsort()[:5]]
    
    for i, (_, row) in enumerate(closest_5.iterrows()):
        dist = distances.iloc[row.name]
        print(f"   {i+1}. Lat: {row['lat']:.6f}, Lon: {row['lon']:.6f}, Dist: {dist:.6f}°")

except Exception as e:
    print(f"❌ Error loading data: {e}")

print("\n" + "="*50)