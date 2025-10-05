"""
Test script to verify data loading and polygon analysis
"""
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon
import os

def test_data_loading():
    """Test loading of enhanced data"""
    print("🧪 Testing Enhanced Data Loading...")
    
    # Test files
    files_to_test = [
        'data_solution/enhanced_topography_detailed.csv',
        'data_solution/enhanced_infrastructure_detailed.csv', 
        'data_solution/enhanced_population_detailed.csv',
        'data_solution/enhanced_economic_activity_detailed.csv',
        'data_solution/enhanced_composite_air_quality_index.csv',
        'data_solution/enhanced_temperature_data.csv'
    ]
    
    data = {}
    
    for file in files_to_test:
        if os.path.exists(file):
            try:
                df = pd.read_csv(file)
                data[file] = df
                print(f"✅ {file}: {len(df)} rows")
                print(f"   Columns: {list(df.columns)}")
                print(f"   Lat range: {df['lat'].min():.6f} to {df['lat'].max():.6f}")
                print(f"   Lon range: {df['lon'].min():.6f} to {df['lon'].max():.6f}")
            except Exception as e:
                print(f"❌ {file}: {e}")
        else:
            print(f"⚠️ {file}: Not found")
        print()
    
    return data

def test_polygon_analysis():
    """Test polygon analysis with sample data"""
    print("🎯 Testing Polygon Analysis...")
    
    # Create test polygon around Sulaimani center
    center_lat, center_lon = 35.5608, 45.4347
    
    # Small test polygon (about 1km x 1km)
    polygon_coords = [
        [center_lat - 0.005, center_lon - 0.005],  # Southwest
        [center_lat - 0.005, center_lon + 0.005],  # Southeast  
        [center_lat + 0.005, center_lon + 0.005],  # Northeast
        [center_lat + 0.005, center_lon - 0.005]   # Northwest
    ]
    
    # Create polygon (lon, lat for Shapely)
    polygon = Polygon([(coord[1], coord[0]) for coord in polygon_coords])
    print(f"Test polygon bounds: {polygon.bounds}")
    
    # Test with topography data
    if os.path.exists('data_solution/enhanced_topography_detailed.csv'):
        topo_data = pd.read_csv('data_solution/enhanced_topography_detailed.csv')
        
        points_in_area = []
        total_checked = 0
        
        for _, row in topo_data.iterrows():
            total_checked += 1
            point = Point(row['lon'], row['lat'])
            if polygon.contains(point) or polygon.touches(point):
                points_in_area.append(row['development_suitability'])
            
            if total_checked > 1000:  # Test with first 1000 points
                break
        
        print(f"Topography test: Checked {total_checked} points, found {len(points_in_area)} in polygon")
        
        if points_in_area:
            avg_suitability = np.mean(points_in_area)
            print(f"Average suitability in test area: {avg_suitability:.2f}")
        else:
            print("⚠️ No points found in test polygon - coordinate system issue!")
    
    # Test with different coordinate order
    print("\n🔄 Testing alternative coordinate format...")
    polygon_alt = Polygon([(coord[0], coord[1]) for coord in polygon_coords])  # lat, lon
    print(f"Alternative polygon bounds: {polygon_alt.bounds}")
    
    if os.path.exists('data_solution/enhanced_topography_detailed.csv'):
        points_in_area_alt = []
        
        for _, row in topo_data.head(1000).iterrows():
            point = Point(row['lat'], row['lon'])  # Try lat, lon
            if polygon_alt.contains(point) or polygon_alt.touches(point):
                points_in_area_alt.append(row['development_suitability'])
        
        print(f"Alternative format: Found {len(points_in_area_alt)} points in polygon")

if __name__ == "__main__":
    data = test_data_loading()
    test_polygon_analysis()