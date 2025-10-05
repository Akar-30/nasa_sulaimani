import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point
import os
import sys

# Test the exact Enhanced Solution logic after our fix
print("🔬 Testing Enhanced Solution Polygon Analysis Fix")
print("=" * 50)

# Load enhanced data (same as Enhanced Solution page)
def load_enhanced_data():
    """Load high-resolution enhanced datasets"""
    data = {}
    
    # Enhanced Air Quality Data
    try:
        if os.path.exists('data_solution/enhanced_air_quality_detailed.csv'):
            data['air_quality'] = pd.read_csv('data_solution/enhanced_air_quality_detailed.csv')
            print(f"✅ Enhanced Air Quality: {len(data['air_quality']):,} measurements")
        else:
            data['air_quality'] = None
            print("❌ Enhanced air quality data not available")
    except Exception as e:
        data['air_quality'] = None
        print(f"❌ Air quality data error: {e}")
    
    # Enhanced Topography Data
    try:
        if os.path.exists('data_solution/enhanced_topography_detailed.csv'):
            data['topography'] = pd.read_csv('data_solution/enhanced_topography_detailed.csv')
            print(f"✅ Enhanced Topography: {len(data['topography']):,} measurements")
        else:
            data['topography'] = None
            print("❌ Enhanced topography data not available")
    except Exception as e:
        data['topography'] = None
        print(f"❌ Topography data error: {e}")
    
    return data

# Simulate analyze_enhanced_area function with our fixes
def test_analyze_enhanced_area(polygon_coords, enhanced_data):
    """Test enhanced multi-criteria analysis for selected polygon area"""
    if not polygon_coords or len(polygon_coords) < 3:
        print("❌ Invalid polygon coordinates")
        return None
    
    # Create polygon from coordinates
    try:
        # Handle different coordinate formats from st_folium
        if isinstance(polygon_coords[0], list) and len(polygon_coords[0]) == 2:
            # Format: [[lat, lon], [lat, lon], ...] - typical from st_folium
            shapely_coords = [(coord[1], coord[0]) for coord in polygon_coords]  # lon, lat for shapely
            polygon = Polygon(shapely_coords)
            print(f"✅ Polygon created with bounds: {polygon.bounds}")
        else:
            # Try direct format
            polygon = Polygon(polygon_coords)
        
        # Enhanced validation: test polygon across multiple data sections
        test_data = enhanced_data.get('topography')  # Use topography for quick test
        if test_data is not None and len(test_data) > 0:
            buffered_polygon = polygon.buffer(0.001)
            test_points = 0
            
            # Test multiple sections of data, not just first 100 rows
            data_length = len(test_data)
            test_sections = [
                (0, min(100, data_length)),  # First section
                (data_length//4, min(data_length//4 + 100, data_length)),  # Quarter section
                (data_length//2, min(data_length//2 + 100, data_length)),  # Half section
                (3*data_length//4, min(3*data_length//4 + 100, data_length))  # Three-quarter section
            ]
            
            print(f"🔍 Testing polygon validation across {len(test_sections)} data sections...")
            
            for i, (start_idx, end_idx) in enumerate(test_sections):
                section_points = 0
                if test_points > 0:
                    break
                for _, row in test_data.iloc[start_idx:end_idx].iterrows():
                    point = Point(row['lon'], row['lat'])
                    if buffered_polygon.contains(point):
                        test_points += 1
                        section_points += 1
                        if test_points >= 3:  # Found enough points to confirm format
                            break
                
                print(f"   Section {i+1} (rows {start_idx}-{end_idx}): {section_points} points found")
            
            print(f"✅ Polygon validation: {test_points} points found")
            
            if test_points > 0:
                print("🎯 Polygon coordinate format is CORRECT - proceeding with analysis")
                return True
            else:
                print("⚠️ No points found in polygon - may need alternative coordinate format")
                return False
        else:
            print("❌ No topography data available for validation")
            return False
            
    except Exception as e:
        print(f"❌ Error creating polygon: {e}")
        return False

# Test with Sulaimani coordinates
print("\n🌍 Testing with Sulaimani area coordinates")
print("-" * 40)

enhanced_data = load_enhanced_data()

# Simulate st_folium polygon coordinates for Sulaimani area
sulaimani_lat, sulaimani_lon = 35.5647, 45.4164
buffer_size = 0.02

# st_folium returns coordinates in [lat, lon] format
test_polygon_coords = [
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon + buffer_size],
    [sulaimani_lat + buffer_size, sulaimani_lon + buffer_size],
    [sulaimani_lat + buffer_size, sulaimani_lon - buffer_size],
    [sulaimani_lat - buffer_size, sulaimani_lon - buffer_size]
]

print(f"Test polygon coordinates (st_folium format [lat, lon]):")
for i, coord in enumerate(test_polygon_coords[:4]):
    print(f"   Point {i+1}: [{coord[0]:.6f}, {coord[1]:.6f}]")

# Run the test
result = test_analyze_enhanced_area(test_polygon_coords, enhanced_data)

if result:
    print("\n🎉 SUCCESS: Enhanced Solution polygon analysis should now work!")
    print("✅ The fix for multiple data section validation is working")
    print("✅ Coordinate format processing is correct") 
    print("✅ User should now see analysis results when drawing polygons in Sulaimani area")
else:
    print("\n❌ ISSUE: Enhanced Solution still has problems")
    print("Need further debugging...")

print("\n" + "=" * 50)
print("Test completed. Please try the Enhanced Solution page in the web app.")