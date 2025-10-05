#!/usr/bin/env python3
"""
Test script to verify polygon analysis fix
"""

import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point
import sys
import os

# Add the current directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_polygon_analysis():
    """Test the polygon analysis with a sample polygon around Sulaimani center"""
    
    print("🧪 Testing Enhanced Polygon Analysis")
    print("=" * 50)
    
    # Load enhanced data
    data_dir = "data_solution"
    
    # Test data loading
    files_to_test = [
        f"{data_dir}/enhanced_air_quality_detailed.csv",
        f"{data_dir}/enhanced_vegetation_detailed.csv", 
        f"{data_dir}/enhanced_infrastructure_detailed.csv",
        f"{data_dir}/enhanced_population_detailed.csv",
        f"{data_dir}/enhanced_economic_activity_detailed.csv",
        f"{data_dir}/enhanced_topography_detailed.csv"
    ]
    
    all_data = {}
    
    for i, file_path in enumerate(files_to_test):
        data_name = ['air_quality', 'heat_greenspace', 'infrastructure', 'population', 'nightlights', 'topography'][i]
        
        if os.path.exists(file_path):
            try:
                data = pd.read_csv(file_path)
                all_data[data_name] = data
                print(f"✅ {data_name}: Loaded {len(data)} rows")
                print(f"   Lat range: {data['lat'].min():.6f} to {data['lat'].max():.6f}")
                print(f"   Lon range: {data['lon'].min():.6f} to {data['lon'].max():.6f}")
                
                # Show sample columns
                score_cols = [col for col in data.columns if 'score' in col.lower()]
                print(f"   Score columns: {score_cols}")
                
            except Exception as e:
                print(f"❌ {data_name}: Error loading - {e}")
                all_data[data_name] = None
        else:
            print(f"❌ {data_name}: File not found - {file_path}")
            all_data[data_name] = None
    
    print("\n" + "=" * 50)
    print("🔍 Testing Polygon Analysis")
    
    # Create test polygon around Sulaimani center (35.5647°N, 45.4164°E)
    sulaimani_center_lat = 35.5647
    sulaimani_center_lon = 45.4164
    
    # Create small test polygon (roughly 2km x 2km)
    buffer_size = 0.01  # ~1km 
    
    test_polygon_coords = [
        [sulaimani_center_lon - buffer_size, sulaimani_center_lat - buffer_size],  # SW
        [sulaimani_center_lon + buffer_size, sulaimani_center_lat - buffer_size],  # SE  
        [sulaimani_center_lon + buffer_size, sulaimani_center_lat + buffer_size],  # NE
        [sulaimani_center_lon - buffer_size, sulaimani_center_lat + buffer_size],  # NW
        [sulaimani_center_lon - buffer_size, sulaimani_center_lat - buffer_size],  # Close polygon
    ]
    
    polygon = Polygon(test_polygon_coords)
    buffered_polygon = polygon.buffer(0.001)  # Buffer for intersection testing
    
    print(f"Test polygon center: {sulaimani_center_lat:.6f}°N, {sulaimani_center_lon:.6f}°E")
    print(f"Polygon bounds: {polygon.bounds}")
    print(f"Polygon area: {polygon.area:.8f} square degrees")
    print(f"Buffered area: {buffered_polygon.area:.8f} square degrees")
    
    # Test each dataset
    total_points_found = 0
    
    for data_name, data in all_data.items():
        if data is not None:
            points_in_polygon = 0
            points_in_buffered = 0
            
            for _, row in data.iterrows():
                point = Point(row['lon'], row['lat'])
                
                if polygon.contains(point):
                    points_in_polygon += 1
                    
                if buffered_polygon.contains(point):
                    points_in_buffered += 1
                    
            print(f"\n📊 {data_name}:")
            print(f"   Points in polygon: {points_in_polygon}")
            print(f"   Points in buffered polygon: {points_in_buffered}")
            
            total_points_found += points_in_buffered
            
            # Show closest points for debugging
            if len(data) > 0:
                distances = []
                for _, row in data.iterrows():
                    dist = np.sqrt((row['lat'] - sulaimani_center_lat)**2 + (row['lon'] - sulaimani_center_lon)**2)
                    distances.append(dist)
                
                min_dist = min(distances)
                closest_idx = distances.index(min_dist)
                closest_point = data.iloc[closest_idx]
                
                print(f"   Closest point: {closest_point['lat']:.6f}, {closest_point['lon']:.6f}")
                print(f"   Distance to center: {min_dist:.6f} degrees ({min_dist * 111:.1f} km)")
    
    print("\n" + "=" * 50)
    print(f"🎯 TOTAL POINTS FOUND IN BUFFERED POLYGON: {total_points_found}")
    
    if total_points_found > 0:
        print("✅ SUCCESS: Polygon analysis should now work!")
    else:
        print("❌ ISSUE: Still no points found in polygon")
        print("   This suggests coordinate system mismatch still exists")
    
    print("=" * 50)

if __name__ == "__main__":
    test_polygon_analysis()