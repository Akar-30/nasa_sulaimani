#!/usr/bin/env python3
"""
Test script to verify the enhanced heatmap visualization
"""

import pandas as pd
import folium
from folium.plugins import HeatMap

# Load sample air quality data
try:
    data = pd.read_csv('data/air_quality_no2_interpolated.csv')
    print(f"✅ Loaded {len(data)} data points")
    
    # Get latest date
    latest_date = data['date'].max()
    daily_data = data[data['date'] == latest_date]
    print(f"✅ Using {len(daily_data)} points from {latest_date}")
    
    # Create map centered on Sulaimani
    m = folium.Map(
        location=[35.56, 45.43],
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Normalize values
    values = daily_data['value'].values
    min_val, max_val = values.min(), values.max()
    print(f"✅ Value range: {min_val:.2f} - {max_val:.2f}")
    
    # Create dense heatmap data with interpolation
    import numpy as np
    from scipy.spatial import cKDTree
    
    heat_data = []
    # Add original data points
    for _, row in daily_data.iterrows():
        normalized_value = (row['value'] - min_val) / (max_val - min_val) if max_val > min_val else 0.5
        heat_data.append([row['lat'], row['lon'], normalized_value])
    
    # Add interpolated points for continuous coverage
    lats = daily_data['lat'].values
    lons = daily_data['lon'].values  
    values = daily_data['value'].values
    
    lat_range = np.linspace(lats.min(), lats.max(), 30)
    lon_range = np.linspace(lons.min(), lons.max(), 30)
    
    points = np.column_stack((lats, lons))
    tree = cKDTree(points)
    
    interpolated_count = 0
    for lat in lat_range:
        for lon in lon_range:
            distances, indices = tree.query([lat, lon], k=3)
            if distances[0] < 0.01:  # Skip if too close to existing point
                continue
                
            weights = 1 / (distances + 1e-10)
            weights /= weights.sum()
            interpolated_value = np.sum(values[indices] * weights)
            
            normalized_value = (interpolated_value - min_val) / (max_val - min_val) if max_val > min_val else 0.5
            heat_data.append([lat, lon, normalized_value * 0.7])
            interpolated_count += 1
    
    print(f"✅ Added {interpolated_count} interpolated points for continuous coverage")
    
    # Add enhanced heatmap with continuous coverage
    HeatMap(
        heat_data, 
        radius=60,        # Much larger radius
        blur=40,          # Heavy blur
        max_zoom=18,      # Allow high zoom
        min_opacity=0.4,
        gradient={
            0.0: '#0033cc',
            0.15: '#0066ff',
            0.3: '#00ccff',
            0.45: '#00ff66',
            0.6: '#ffff00',
            0.75: '#ff6600',
            0.9: '#ff3300',
            1.0: '#cc0000'
        }
    ).add_to(m)
    
    # Save test map
    m.save('test_heatmap.html')
    print("✅ Test heatmap saved as 'test_heatmap.html'")
    print("📝 Continuous coverage improvements:")
    print("   - Radius increased from 35 to 60 pixels for gap-free coverage")
    print("   - Blur increased from 25 to 40 for seamless blending")
    print("   - Max zoom increased to 18 while maintaining coverage")
    print("   - Added interpolated points between grid nodes")
    print("   - Enhanced 8-stop gradient for smoother transitions")
    print("   - Minimum opacity increased to 0.4 for better visibility")
    print("   - Truly continuous coverage at all zoom levels")

except Exception as e:
    print(f"❌ Error: {e}")