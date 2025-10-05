#!/usr/bin/env python3
"""
Test Enhanced Solution polygon analysis fix
"""

import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point
import sys
import os

def test_enhanced_solution_fix():
    """Test the Enhanced Solution polygon analysis fix"""
    
    print("🧪 Testing Enhanced Solution Polygon Analysis Fix")
    print("=" * 60)
    
    # Load enhanced data to test with
    data_dir = "data_solution"
    
    # Test with topography data
    topo_file = f"{data_dir}/enhanced_topography_detailed.csv"
    
    if os.path.exists(topo_file):
        try:
            topo_data = pd.read_csv(topo_file)
            print(f"✅ Loaded topography data: {len(topo_data)} rows")
            
            # Create test polygon around Sulaimani center
            sulaimani_center_lat = 35.5647
            sulaimani_center_lon = 45.4164
            buffer_size = 0.01  # ~1km 
            
            # Test both coordinate formats
            format1_coords = [  # [lat, lon] format (st_folium style)
                [sulaimani_center_lat - buffer_size, sulaimani_center_lon - buffer_size],
                [sulaimani_center_lat - buffer_size, sulaimani_center_lon + buffer_size],
                [sulaimani_center_lat + buffer_size, sulaimani_center_lon + buffer_size],
                [sulaimani_center_lat + buffer_size, sulaimani_center_lon - buffer_size],
                [sulaimani_center_lat - buffer_size, sulaimani_center_lon - buffer_size]
            ]
            
            # Test coordinate processing logic from Enhanced Solution
            def test_coordinate_format(coords, format_name):
                print(f"\n🔍 Testing {format_name}")
                
                # Mimic Enhanced Solution coordinate processing
                if isinstance(coords[0], list) and len(coords[0]) == 2:
                    shapely_coords = [(coord[1], coord[0]) for coord in coords]  # lon, lat for shapely
                    polygon = Polygon(shapely_coords)
                else:
                    polygon = Polygon(coords)
                
                # Test with buffered polygon
                buffered_polygon = polygon.buffer(0.001)
                
                points_found = 0
                for _, row in topo_data.head(1000).iterrows():  # Test first 1000 points
                    point = Point(row['lon'], row['lat'])
                    if buffered_polygon.contains(point):
                        points_found += 1
                
                print(f"   📊 Points found: {points_found}")
                print(f"   🗺️ Polygon bounds: {polygon.bounds}")
                
                return points_found
            
            # Test format 1
            points1 = test_coordinate_format(format1_coords, "st_folium [lat,lon] format")
            
            print(f"\n🎯 ENHANCED SOLUTION TEST RESULTS:")
            print(f"   Format 1 ([lat,lon]): {points1} points found")
            
            if points1 > 0:
                print("✅ SUCCESS: Enhanced Solution polygon analysis should work!")
                print("   The buffered polygon approach is finding data points correctly.")
            else:
                print("❌ ISSUE: Still no points found in Enhanced Solution")
                print("   Additional debugging may be needed.")
            
        except Exception as e:
            print(f"❌ Error testing Enhanced Solution: {e}")
            
    else:
        print(f"❌ Enhanced topography file not found: {topo_file}")
    
    print("=" * 60)

if __name__ == "__main__":
    test_enhanced_solution_fix()