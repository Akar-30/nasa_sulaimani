import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from folium.plugins import Draw, HeatMap
from shapely.geometry import Point, Polygon

st.set_page_config(page_title="🎯 Integrated Solution Analysis", page_icon="🎯", layout="wide")

st.title("🎯 Integrated Area Analysis & Solutions")
st.markdown("**Multi-Criteria Development Suitability & Improvement Recommendations**")

st.markdown("""
### 🌍 **How It Works**
1. **Draw a shape** on the map below to select your area of interest
2. **Get instant analysis** of all sustainability criteria for that area
3. **Receive specific recommendations** for improvements needed
4. **View integrated scoring** across all environmental and infrastructure factors

### 📊 **Analysis Criteria**
- 💨 **Air Quality** (6 pollutants + health risk)
- 🌡️ **Heat & Greenspace** (temperature + vegetation)
- 🗻 **Topography** (elevation + slope suitability)
- 🏗️ **Infrastructure** (accessibility to services)
- 💡 **Economic Activity** (nighttime lights)
- 👥 **Population Density** (optimal development balance)
""")

# Sulaimani coordinates - adjusted for enhanced data coverage
SULAIMANI_CENTER = [35.5608, 45.4347]
# Enhanced data bounds for reference
ENHANCED_BOUNDS = {
    'north': 35.714444,
    'south': 35.427222, 
    'west': 45.155833,
    'east': 45.551944
}

# Load all available data
@st.cache_data
def load_all_criteria_data():
    """Load enhanced data from data_solution folder"""
    data = {}
    
    # Try enhanced solution data first (higher resolution)
    try:
        # Enhanced Air Quality Data
        if os.path.exists('data_solution/enhanced_air_quality_detailed.csv'):
            data['air_quality'] = pd.read_csv('data_solution/enhanced_air_quality_detailed.csv')
        elif os.path.exists('data_solution/enhanced_composite_air_quality_index.csv'):
            data['air_quality'] = pd.read_csv('data_solution/enhanced_composite_air_quality_index.csv')
        elif os.path.exists('data/composite_air_quality_index.csv'):
            data['air_quality'] = pd.read_csv('data/composite_air_quality_index.csv')
        else:
            data['air_quality'] = None
        
        # Enhanced Temperature & Vegetation Data
        if os.path.exists('data_solution/enhanced_temperature_detailed.csv'):
            data['temperature'] = pd.read_csv('data_solution/enhanced_temperature_detailed.csv')
        elif os.path.exists('data_solution/enhanced_temperature_data.csv'):
            data['temperature'] = pd.read_csv('data_solution/enhanced_temperature_data.csv')
        elif os.path.exists('data/temperature_data.csv'):
            data['temperature'] = pd.read_csv('data/temperature_data.csv')
        else:
            data['temperature'] = None
            
        if os.path.exists('data_solution/enhanced_vegetation_detailed.csv'):
            data['vegetation'] = pd.read_csv('data_solution/enhanced_vegetation_detailed.csv')
        elif os.path.exists('data_solution/enhanced_vegetation_data.csv'):
            data['vegetation'] = pd.read_csv('data_solution/enhanced_vegetation_data.csv')
        elif os.path.exists('data/vegetation_data.csv'):
            data['vegetation'] = pd.read_csv('data/vegetation_data.csv')
        else:
            data['vegetation'] = None
        
        # Enhanced Infrastructure Data
        if os.path.exists('data_solution/enhanced_infrastructure_detailed.csv'):
            data['infrastructure'] = pd.read_csv('data_solution/enhanced_infrastructure_detailed.csv')
        else:
            # Check enhanced copied files first
            enhanced_infra_files = [
                'data_solution/enhanced_infrastructure_data_0.010_0.15_10.0.csv',
                'data_solution/enhanced_infrastructure_data_0.010_0.30_10.0.csv'
            ]
            
            for file in enhanced_infra_files:
                if os.path.exists(file):
                    try:
                        data['infrastructure'] = pd.read_csv(file)
                        break
                    except:
                        continue
            
            if 'infrastructure' not in data:
                # Fallback to original infrastructure files
                infrastructure_files = [
                    'data/infrastructure_data_0.010_0.15_10.0.csv',
                    'data/infrastructure_data_0.010_0.30_10.0.csv',
                    'data/infrastructure_data_0.020_0.10_2.0.csv'
                ]
                
                for file in infrastructure_files:
                    if os.path.exists(file):
                        try:
                            data['infrastructure'] = pd.read_csv(file)
                            break
                        except:
                            continue
                
                if 'infrastructure' not in data:
                    data['infrastructure'] = None
        
        # Enhanced Population Data
        if os.path.exists('data_solution/enhanced_population_detailed.csv'):
            data['population'] = pd.read_csv('data_solution/enhanced_population_detailed.csv')
        else:
            # Check enhanced copied files first
            enhanced_pop_files = [
                'data_solution/enhanced_population_density_0.010_0.15_2023.csv',
                'data_solution/enhanced_population_density_0.005_0.20_2023.csv'
            ]
            
            for file in enhanced_pop_files:
                if os.path.exists(file):
                    try:
                        data['population'] = pd.read_csv(file)
                        break
                    except:
                        continue
            
            if 'population' not in data:
                # Fallback to original population files
                pop_files = [
                    'data/population_density_0.010_0.15_2023.csv',
                    'data/population_density_0.005_0.20_2023.csv',
                    'data/population_density_0.020_0.15_2023.csv'
                ]
                for file in pop_files:
                    if os.path.exists(file):
                        try:
                            data['population'] = pd.read_csv(file)
                            break
                        except:
                            continue
                
                if 'population' not in data:
                    data['population'] = None
        
        # Enhanced Economic Activity Data (Nightlights)
        if os.path.exists('data_solution/enhanced_economic_activity_detailed.csv'):
            data['nightlights'] = pd.read_csv('data_solution/enhanced_economic_activity_detailed.csv')
        elif os.path.exists('data_solution/enhanced_nightlights_data_0.010_0.15_2023.csv'):
            data['nightlights'] = pd.read_csv('data_solution/enhanced_nightlights_data_0.010_0.15_2023.csv')
        else:
            # Fallback to original nightlights files
            lights_files = [
                'data/nightlights_data_0.010_0.15_2023.csv',
                'data/nightlights_data_0.020_0.10_2023.csv'
            ]
            for file in lights_files:
                if os.path.exists(file):
                    try:
                        data['nightlights'] = pd.read_csv(file)
                        break
                    except:
                        continue
            
            if 'nightlights' not in data:
                data['nightlights'] = None
        
        # Enhanced Topography Data
        if os.path.exists('data_solution/enhanced_topography_detailed.csv'):
            data['topography'] = pd.read_csv('data_solution/enhanced_topography_detailed.csv')
        else:
            data['topography'] = None
    
    except Exception as e:
        print(f"Error loading enhanced data: {e}")
        data = {
            'air_quality': None,
            'temperature': None,
            'vegetation': None,
            'infrastructure': None,
            'population': None,
            'nightlights': None,
            'topography': None
        }
    
    return data

def analyze_area_criteria(polygon_coords, all_data):
    """Analyze all criteria for the selected polygon area"""
    
    print("\n" + "="*60)
    print("🔍 ANALYZE_AREA_CRITERIA DEBUG START")
    print("="*60)
    
    if not polygon_coords or len(polygon_coords) < 3:
        print("❌ No valid polygon coordinates received")
        return None
    
    print(f"📍 Received {len(polygon_coords)} polygon coordinates")
    print(f"🔢 First coordinate: {polygon_coords[0]}")
    print(f"🔢 Coordinate type check: {type(polygon_coords[0])}")
    
    # Create polygon from coordinates - Handle multiple st_folium formats
    try:
        polygon = None
        
        # Format detection and conversion
        if isinstance(polygon_coords[0], list):
            if len(polygon_coords[0]) == 2 and isinstance(polygon_coords[0][0], (int, float)):
                # Format: [[lat, lon], [lat, lon], ...] OR [[lon, lat], [lon, lat], ...]
                first_coord = polygon_coords[0]
                
                # Heuristic: if first value is > 40, likely latitude (since our area is ~35-36°N)
                if first_coord[0] > 40 or (35 < first_coord[0] < 37):
                    print("📋 Detected st_folium [lat, lon] format")
                    shapely_coords = [(coord[1], coord[0]) for coord in polygon_coords]  # swap to [lon, lat]
                    polygon = Polygon(shapely_coords)
                    print(f"🔄 Converted [lat,lon] -> [lon,lat]: {shapely_coords[:2]}...")
                else:
                    print("📋 Detected [lon, lat] format")
                    polygon = Polygon(polygon_coords)
                    print(f"🔄 Using direct [lon,lat]: {polygon_coords[:2]}...")
                    
            elif len(polygon_coords[0]) > 2:
                print("📋 Detected nested coordinate format - extracting first level")
                # Sometimes st_folium returns nested: [[[lon, lat], [lon, lat]]]
                actual_coords = polygon_coords[0]
                if isinstance(actual_coords[0], list):
                    polygon = Polygon(actual_coords)
                    print(f"🔄 Using nested coordinates: {actual_coords[:2]}...")
        
        if polygon is None:
            print("📋 Fallback: trying direct coordinate format")
            polygon = Polygon(polygon_coords)
        
        # Debug: Print polygon info
        bounds = polygon.bounds
        center_lon = (bounds[0] + bounds[2]) / 2
        center_lat = (bounds[1] + bounds[3]) / 2
        
        print(f"Debug: Polygon center - Lat: {center_lat:.6f}, Lon: {center_lon:.6f}")
        print(f"Debug: Polygon bounds - West: {bounds[0]:.6f}, South: {bounds[1]:.6f}, East: {bounds[2]:.6f}, North: {bounds[3]:.6f}")
        print(f"Debug: Polygon area: {polygon.area:.8f} square degrees")
        
        # Quick validation: test if polygon finds any data points
        test_data = all_data.get('topography')  # Use topography for quick test
        if test_data is not None and len(test_data) > 0:
            buffered_polygon = polygon.buffer(0.001)
            test_points = 0
            for _, row in test_data.head(100).iterrows():  # Test first 100 points
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    test_points += 1
            
            print(f"🧪 Validation: Found {test_points} test points in polygon")
            
            # If no points found, try alternative coordinate format
            if test_points == 0:
                print("⚠️ No points found - trying alternative coordinate format")
                try:
                    # Try swapping lat/lon interpretation
                    alt_coords = [(coord[0], coord[1]) for coord in polygon_coords]  # Keep original order
                    if isinstance(polygon_coords[0], list) and len(polygon_coords[0]) == 2:
                        alt_coords = [(coord[0], coord[1]) for coord in polygon_coords]  # direct format
                    alt_polygon = Polygon(alt_coords)
                    alt_buffered = alt_polygon.buffer(0.001)
                    
                    alt_test_points = 0
                    for _, row in test_data.head(100).iterrows():
                        point = Point(row['lon'], row['lat'])
                        if alt_buffered.contains(point):
                            alt_test_points += 1
                    
                    print(f"🔄 Alternative format found {alt_test_points} test points")
                    if alt_test_points > test_points:
                        print("✅ Using alternative coordinate format")
                        polygon = alt_polygon
                        bounds = polygon.bounds
                        center_lon = (bounds[0] + bounds[2]) / 2
                        center_lat = (bounds[1] + bounds[3]) / 2
                        print(f"🆕 New polygon center - Lat: {center_lat:.6f}, Lon: {center_lon:.6f}")
                        
                except Exception as alt_e:
                    print(f"❌ Alternative format failed: {alt_e}")
        
    except Exception as e:
        print(f"Debug: Error creating polygon: {e}")
        print(f"Debug: Polygon coords format: {polygon_coords}")
        return None
    
    results = {
        'area_km2': 0,
        'air_quality': {'score': 0, 'status': 'No Data', 'recommendations': []},
        'heat_greenspace': {'score': 0, 'status': 'No Data', 'recommendations': []},
        'topography': {'score': 0, 'status': 'No Data', 'recommendations': []},
        'infrastructure': {'score': 0, 'status': 'No Data', 'recommendations': []},
        'economic_activity': {'score': 0, 'status': 'No Data', 'recommendations': []},
        'population': {'score': 0, 'status': 'No Data', 'recommendations': []},
        'overall_score': 0,
        'overall_status': 'Insufficient Data'
    }
    
    # Calculate approximate area in km²
    try:
        # Simple approximation for small areas
        bounds = polygon.bounds
        lat_diff = bounds[3] - bounds[1]  # max_lat - min_lat
        lon_diff = bounds[2] - bounds[0]  # max_lon - min_lon
        # Rough conversion: 1° ≈ 111 km
        area_km2 = lat_diff * lon_diff * 111 * 111
        results['area_km2'] = area_km2
    except:
        results['area_km2'] = 1.0
    
    valid_scores = []
    
    # Debug: Print available data info
    for key, data in all_data.items():
        if data is not None:
            print(f"Debug: {key} data available - {len(data)} rows")
            if len(data) > 0:
                print(f"Debug: {key} lat range: {data['lat'].min():.6f} to {data['lat'].max():.6f}")
                print(f"Debug: {key} lon range: {data['lon'].min():.6f} to {data['lon'].max():.6f}")
        else:
            print(f"Debug: {key} data is None")
    
    # Analyze Air Quality
    if all_data['air_quality'] is not None and len(all_data['air_quality']) > 0:
        try:
            aqi_data = all_data['air_quality']
            # Get latest data
            latest_aqi = aqi_data[aqi_data['date'] == aqi_data['date'].max()]
            
            # Find points within polygon (with small buffer for edge cases)
            points_in_area = []
            total_checked = 0
            buffered_polygon = polygon.buffer(0.001)  # Small buffer ~100m
            
            for _, row in latest_aqi.iterrows():
                total_checked += 1
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    points_in_area.append(row['aqi_score'])
            
            print(f"Debug: Air Quality - Checked {total_checked} points, found {len(points_in_area)} in polygon")
            
            if points_in_area:
                avg_aqi = np.mean(points_in_area)
                # Convert AQI to 0-100 suitability score (lower AQI = higher suitability)
                score = max(0, 100 - avg_aqi)
                results['air_quality']['score'] = score
                
                if score >= 80:
                    results['air_quality']['status'] = 'Excellent Air Quality'
                    results['air_quality']['recommendations'] = ['Maintain current air quality standards']
                elif score >= 60:
                    results['air_quality']['status'] = 'Good Air Quality'
                    results['air_quality']['recommendations'] = ['Monitor pollution sources', 'Promote clean transportation']
                elif score >= 40:
                    results['air_quality']['status'] = 'Moderate Air Quality'
                    results['air_quality']['recommendations'] = [
                        'Install air quality monitoring stations',
                        'Create green buffers along roads',
                        'Restrict heavy traffic during peak hours'
                    ]
                else:
                    results['air_quality']['status'] = 'Poor Air Quality'
                    results['air_quality']['recommendations'] = [
                        'Urgent need for emission controls',
                        'Relocate sensitive facilities (schools, hospitals)',
                        'Implement industrial pollution controls',
                        'Create extensive green corridors'
                    ]
                
                valid_scores.append(score)
        except Exception as e:
            pass
    
    # Analyze Heat & Greenspace
    if all_data['temperature'] is not None and all_data['vegetation'] is not None:
        try:
            temp_data = all_data['temperature']
            veg_data = all_data['vegetation']
            
            # Get latest data
            latest_temp = temp_data[temp_data['date'] == temp_data['date'].max()]
            latest_veg = veg_data[veg_data['date'] == veg_data['date'].max()]
            
            # Find points in area (with buffer)
            temp_values = []
            ndvi_values = []
            buffered_polygon = polygon.buffer(0.001)
            
            for _, row in latest_temp.iterrows():
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    temp_values.append(row['land_surface_temperature'])
            
            for _, row in latest_veg.iterrows():
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    ndvi_values.append(row['estimated_ndvi'])
            
            if temp_values and ndvi_values:
                avg_temp = np.mean(temp_values)
                avg_ndvi = np.mean(ndvi_values)
                
                # Calculate heat stress score (lower temp = higher score)
                temp_score = max(0, min(100, (50 - avg_temp) * 10 + 50))
                # Calculate vegetation score (higher NDVI = higher score)
                ndvi_score = min(100, avg_ndvi * 100 / 0.8)  # 0.8 is excellent NDVI
                
                # Combined score
                score = (temp_score + ndvi_score) / 2
                results['heat_greenspace']['score'] = score
                
                recommendations = []
                if avg_temp > 40:
                    recommendations.extend([
                        'Install shade structures and cool pavements',
                        'Create water features for cooling',
                        'Urgent tree planting program'
                    ])
                elif avg_temp > 35:
                    recommendations.extend(['Increase tree canopy coverage', 'Add green roofs'])
                
                if avg_ndvi < 0.3:
                    recommendations.extend([
                        'Establish new parks and green spaces',
                        'Implement mandatory green building standards',
                        'Create community gardens'
                    ])
                
                if score >= 80:
                    results['heat_greenspace']['status'] = 'Excellent Climate Conditions'
                elif score >= 60:
                    results['heat_greenspace']['status'] = 'Good Climate Balance'
                elif score >= 40:
                    results['heat_greenspace']['status'] = 'Moderate Heat Stress'
                else:
                    results['heat_greenspace']['status'] = 'High Heat Stress Risk'
                
                results['heat_greenspace']['recommendations'] = recommendations if recommendations else ['Maintain current green infrastructure']
                valid_scores.append(score)
        except:
            pass
    
    # Analyze Infrastructure (if available)
    if all_data['infrastructure'] is not None:
        try:
            infra_data = all_data['infrastructure']
            
            # Find points in area (with buffer)
            infra_scores = []
            buffered_polygon = polygon.buffer(0.001)
            
            for _, row in infra_data.iterrows():
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    if 'infrastructure_score' in row:
                        infra_scores.append(row['infrastructure_score'])
                    elif 'total_score' in row:
                        infra_scores.append(row['total_score'])
            
            if infra_scores:
                score = np.mean(infra_scores)
                results['infrastructure']['score'] = score
                
                if score >= 80:
                    results['infrastructure']['status'] = 'Excellent Infrastructure Access'
                    results['infrastructure']['recommendations'] = ['Maintain current service levels']
                elif score >= 60:
                    results['infrastructure']['status'] = 'Good Infrastructure Access'
                    results['infrastructure']['recommendations'] = ['Upgrade secondary infrastructure']
                elif score >= 40:
                    results['infrastructure']['status'] = 'Limited Infrastructure'
                    results['infrastructure']['recommendations'] = [
                        'Improve road connectivity',
                        'Add healthcare facilities',
                        'Enhance public transportation'
                    ]
                else:
                    results['infrastructure']['status'] = 'Poor Infrastructure'
                    results['infrastructure']['recommendations'] = [
                        'Urgent infrastructure development needed',
                        'Build new roads and utilities',
                        'Establish essential services (hospital, school)',
                        'Install telecommunications infrastructure'
                    ]
                
                valid_scores.append(score)
        except:
            pass
    
    # Analyze Population Density (if available)
    if all_data['population'] is not None:
        try:
            pop_data = all_data['population']
            
            # Find points in area (with buffer)
            pop_scores = []
            densities = []
            buffered_polygon = polygon.buffer(0.001)
            
            for _, row in pop_data.iterrows():
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    if 'development_suitability_score' in row:
                        pop_scores.append(row['development_suitability_score'])
                    if 'population_density' in row:
                        densities.append(row['population_density'])
            
            if pop_scores:
                score = np.mean(pop_scores)
                avg_density = np.mean(densities) if densities else 0
                
                results['population']['score'] = score
                
                recommendations = []
                if avg_density > 5000:
                    recommendations = [
                        'Area is overcrowded - avoid further development',
                        'Improve public services for existing population',
                        'Consider population redistribution strategies'
                    ]
                elif avg_density < 500:
                    recommendations = [
                        'Low density area - ensure infrastructure before development',
                        'Plan for gradual population growth',
                        'Establish community services'
                    ]
                else:
                    recommendations = ['Suitable for sustainable development', 'Plan infrastructure to match growth']
                
                if score >= 80:
                    results['population']['status'] = 'Optimal Development Density'
                elif score >= 60:
                    results['population']['status'] = 'Good Development Potential'
                elif score >= 40:
                    results['population']['status'] = 'Moderate Development Suitability'
                else:
                    results['population']['status'] = 'Limited Development Potential'
                
                results['population']['recommendations'] = recommendations
                valid_scores.append(score)
        except:
            pass
    
    # Analyze Economic Activity (if available)
    if all_data['nightlights'] is not None:
        try:
            lights_data = all_data['nightlights']
            
            # Find points in area (with buffer)
            light_values = []
            activity_scores = []
            buffered_polygon = polygon.buffer(0.001)
            
            for _, row in lights_data.iterrows():
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    if 'normalized_light_intensity' in row:
                        light_values.append(row['normalized_light_intensity'])
                    if 'economic_activity_score' in row:
                        activity_scores.append(row['economic_activity_score'])
            
            if activity_scores:
                score = np.mean(activity_scores)
                results['economic_activity']['score'] = score
                
                avg_light = np.mean(light_values) if light_values else 0
                
                if score >= 80:
                    results['economic_activity']['status'] = 'Strong Economic Activity'
                    results['economic_activity']['recommendations'] = [
                        'Maintain economic vitality',
                        'Ensure infrastructure can handle activity levels'
                    ]
                elif score >= 60:
                    results['economic_activity']['status'] = 'Moderate Economic Activity'
                    results['economic_activity']['recommendations'] = [
                        'Support local business development',
                        'Improve commercial infrastructure'
                    ]
                elif score >= 40:
                    results['economic_activity']['status'] = 'Developing Economic Area'
                    results['economic_activity']['recommendations'] = [
                        'Encourage business investment',
                        'Develop commercial zones',
                        'Improve accessibility'
                    ]
                else:
                    results['economic_activity']['status'] = 'Limited Economic Activity'
                    results['economic_activity']['recommendations'] = [
                        'Create economic development incentives',
                        'Establish business districts',
                        'Improve connectivity to economic centers'
                    ]
                
                valid_scores.append(score)
        except:
            pass
    
    # Analyze Topography (if available)
    if all_data['topography'] is not None:
        try:
            topo_data = all_data['topography']
            
            # Find points in area (with buffer)
            slopes = []
            elevations = []
            suitability_scores = []
            buffered_polygon = polygon.buffer(0.001)
            
            for _, row in topo_data.iterrows():
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    if 'slope_percentage' in row:
                        slopes.append(row['slope_percentage'])
                    if 'elevation' in row:
                        elevations.append(row['elevation'])
                    if 'development_suitability' in row:
                        suitability_scores.append(row['development_suitability'])
            
            if suitability_scores:
                score = np.mean(suitability_scores)
                results['topography'] = {
                    'score': score,
                    'status': 'No Data',
                    'recommendations': []
                }
                
                avg_slope = np.mean(slopes) if slopes else 0
                avg_elevation = np.mean(elevations) if elevations else 0
                
                recommendations = []
                if avg_slope > 15:
                    recommendations.extend([
                        'Steep terrain - requires careful engineering',
                        'Consider terracing for development',
                        'Higher construction costs expected'
                    ])
                elif avg_slope > 10:
                    recommendations.extend([
                        'Moderate slopes - manageable with proper planning',
                        'Standard slope stabilization needed'
                    ])
                
                if avg_elevation > 1000:
                    recommendations.append('High altitude considerations for infrastructure')
                elif avg_elevation < 500:
                    recommendations.append('Low elevation - check for drainage issues')
                
                if score >= 80:
                    results['topography']['status'] = 'Excellent Terrain Suitability'
                elif score >= 60:
                    results['topography']['status'] = 'Good Terrain Conditions'
                elif score >= 40:
                    results['topography']['status'] = 'Moderate Terrain Challenges'
                else:
                    results['topography']['status'] = 'Difficult Terrain'
                    recommendations.append('Consider alternative locations for major development')
                
                results['topography']['recommendations'] = recommendations if recommendations else ['Suitable terrain for development']
                valid_scores.append(score)
        except Exception as e:
            pass
    
    # Calculate overall score and status
    if valid_scores:
        results['overall_score'] = np.mean(valid_scores)
        
        if results['overall_score'] >= 80:
            results['overall_status'] = '🟢 Highly Suitable for Development'
        elif results['overall_score'] >= 65:
            results['overall_status'] = '🟡 Moderately Suitable for Development'
        elif results['overall_score'] >= 50:
            results['overall_status'] = '🟠 Limited Suitability - Improvements Needed'
        else:
            results['overall_status'] = '🔴 Not Suitable - Major Improvements Required'
    
    return results

def create_suitability_map():
    """Create interactive map with drawing capabilities"""
    m = folium.Map(
        location=SULAIMANI_CENTER,
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Add satellite layer
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add coverage area indicator
    coverage_bounds = [
        [ENHANCED_BOUNDS['south'], ENHANCED_BOUNDS['west']],  # Southwest
        [ENHANCED_BOUNDS['north'], ENHANCED_BOUNDS['west']],  # Northwest  
        [ENHANCED_BOUNDS['north'], ENHANCED_BOUNDS['east']],  # Northeast
        [ENHANCED_BOUNDS['south'], ENHANCED_BOUNDS['east']]   # Southeast
    ]
    
    folium.Rectangle(
        bounds=[[ENHANCED_BOUNDS['south'], ENHANCED_BOUNDS['west']], 
                [ENHANCED_BOUNDS['north'], ENHANCED_BOUNDS['east']]],
        color='blue',
        weight=2,
        fill=False,
        popup="Enhanced Data Coverage Area - Draw your analysis area within this region",
        tooltip="Enhanced Analysis Coverage Zone"
    ).add_to(m)
    
    # Add Sulaimani center marker
    folium.Marker(
        SULAIMANI_CENTER,
        popup="Sulaimani City Center<br>Draw your area around here for analysis",
        tooltip="Sulaimani Center",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # Add drawing tools
    draw = Draw(
        export=True,
        filename='area_selection.geojson',
        position='topleft',
        draw_options={
            'polyline': False,
            'polygon': True,
            'circle': True,
            'rectangle': True,
            'marker': False,
            'circlemarker': False,
        },
        edit_options={'edit': True}
    )
    draw.add_to(m)
    
    folium.LayerControl().add_to(m)
    
    return m

# Load all data
with st.spinner("Loading multi-criteria data..."):
    all_data = load_all_criteria_data()

# Show data availability status
st.subheader("📊 Data Availability Status")
data_status_cols = st.columns(6)

data_status = {
    "Air Quality": all_data['air_quality'] is not None,
    "Heat/Greenspace": all_data['temperature'] is not None and all_data['vegetation'] is not None,
    "Topography": all_data['topography'] is not None,
    "Infrastructure": all_data['infrastructure'] is not None,
    "Economic Activity": all_data['nightlights'] is not None,
    "Population": all_data['population'] is not None
}

for i, (criteria, available) in enumerate(data_status.items()):
    with data_status_cols[i]:
        if available:
            st.success(f"✅ {criteria}")
        else:
            st.error(f"❌ {criteria}")

if not any(data_status.values()):
    st.warning("""
    ⚠️ **No analysis data available!** Please run the individual analysis pages first to generate data:
    - Air Quality Analysis (for pollution data)
    - Heat & Greenspace Analysis (for temperature/vegetation data)
    - Infrastructure Analysis (for accessibility data)
    - Population Density Analysis (for demographic data)
    - Nighttime Lights Analysis (for economic activity data)
    """)

st.markdown("---")

# Interactive map section
st.subheader("🗺️ Interactive Area Selection & Analysis")
st.markdown("""
**Instructions:**
1. Use the drawing tools on the map (polygon, rectangle, or circle)
2. **Draw a shape around Sulaimani city center area** (near coordinates 35.56°N, 45.43°E)
3. Click 'Analyze Selected Area' to get comprehensive analysis
4. View detailed recommendations for improvements

**💡 Tip**: For best results, draw your area within the enhanced coverage zone around Sulaimani city.
""")

# Create and display map
map_obj = create_suitability_map()
map_data = st_folium(map_obj, width=1400, height=500, returned_objects=["all_drawings"])

# DEBUG: Show what st_folium returns
st.write("🔍 **DEBUG: st_folium map_data keys:**", list(map_data.keys()) if map_data else "None")
if map_data and 'all_drawings' in map_data:
    st.write("🔍 **DEBUG: all_drawings content:**", map_data['all_drawings'])
    st.write("🔍 **DEBUG: Number of drawings:**", len(map_data['all_drawings']) if map_data['all_drawings'] else 0)
else:
    st.write("🔍 **DEBUG: No all_drawings found in map_data**")

# Analysis button and results
col1, col2 = st.columns([1, 3])

with col1:
    analyze_button = st.button("🔍 Analyze Selected Area", type="primary", use_container_width=True)

with col2:
    st.markdown("*Draw a shape on the map above, then click analyze to get comprehensive assessment*")

# Show analysis results
st.write(f"🔍 **DEBUG: Analyze button clicked:** {analyze_button}")
st.write(f"🔍 **DEBUG: map_data exists:** {map_data is not None}")

if analyze_button:
    st.write("🔍 **DEBUG: Button was clicked - checking for drawings...**")
    
    if map_data and 'all_drawings' in map_data and map_data['all_drawings']:
        if len(map_data['all_drawings']) > 0:
            st.write("🔍 **DEBUG: Found drawings - processing...**")
            # Get the most recent drawing
            latest_drawing = map_data['all_drawings'][-1]
        
        if latest_drawing['geometry']['type'] in ['Polygon', 'Circle']:
            st.markdown("---")
            st.subheader("📋 Area Analysis Results")
            
            # Extract coordinates with debug output
            st.write("🔍 **DEBUG: Raw drawing data received:**")
            st.json(latest_drawing)
            
            if latest_drawing['geometry']['type'] == 'Polygon':
                coords = latest_drawing['geometry']['coordinates'][0]
                st.write(f"📍 **Polygon coordinates extracted:** {len(coords)} points")
                st.write(f"🔢 **First 3 coordinates:** {coords[:3]}")
            else:
                # For circles, create approximate polygon
                center = latest_drawing['geometry']['coordinates']
                radius = latest_drawing['properties'].get('radius', 1000) / 111000  # Convert to degrees
                st.write(f"⭕ **Circle center:** {center}, **radius:** {radius} degrees")
                coords = []
                for angle in range(0, 360, 10):
                    lat = center[1] + radius * np.cos(np.radians(angle))
                    lon = center[0] + radius * np.sin(np.radians(angle))
                    coords.append([lat, lon])
            
            # Show coordinate processing debug info
            st.write("🗺️ **Coordinates being sent to analysis:**")
            st.write(f"📊 **Format check - First coordinate:** {coords[0] if coords else 'No coordinates'}")
            st.write(f"📏 **Total coordinates:** {len(coords) if coords else 0}")
            
            # Check data bounds vs polygon bounds
            if coords and len(coords) > 2:
                coord_lats = [c[0] if isinstance(c[0], (int, float)) else c[1] for c in coords]
                coord_lons = [c[1] if isinstance(c[0], (int, float)) else c[0] for c in coords]
                poly_bounds = {
                    'min_lat': min(coord_lats), 'max_lat': max(coord_lats),
                    'min_lon': min(coord_lons), 'max_lon': max(coord_lons)
                }
                st.write(f"🌍 **Polygon bounds:** {poly_bounds}")
                st.write(f"📏 **Enhanced data bounds:** North: {ENHANCED_BOUNDS['north']}, South: {ENHANCED_BOUNDS['south']}, West: {ENHANCED_BOUNDS['west']}, East: {ENHANCED_BOUNDS['east']}")
            
            # Perform analysis
            with st.spinner("Analyzing area across all criteria..."):
                results = analyze_area_criteria(coords, all_data)
            
            if results:
                # Overall Status
                st.markdown(f"### {results['overall_status']}")
                st.markdown(f"**Overall Suitability Score: {results['overall_score']:.1f}/100**")
                st.markdown(f"**Analysis Area: {results['area_km2']:.2f} km²**")
                
                # Criteria breakdown
                criteria_cols = st.columns(3)
                
                criteria_data = [
                    ("💨 Air Quality", results['air_quality']),
                    ("🌡️ Heat & Greenspace", results['heat_greenspace']),
                    ("🗻 Topography", results['topography']),
                    ("🏗️ Infrastructure", results['infrastructure']),
                    ("💡 Economic Activity", results['economic_activity']),
                    ("👥 Population Balance", results['population'])
                ]
                
                for i, (name, data) in enumerate(criteria_data):
                    with criteria_cols[i % 3]:
                        score = data['score']
                        status = data['status']
                        
                        # Color code based on score
                        if score >= 80:
                            color = "green"
                        elif score >= 60:
                            color = "orange" 
                        elif score >= 40:
                            color = "orange"
                        else:
                            color = "red"
                        
                        st.markdown(f"**{name}**")
                        st.markdown(f":{color}[{status}]")
                        st.markdown(f"Score: **{score:.1f}/100**")
                        
                        if data['recommendations']:
                            with st.expander(f"View {name.split()[1]} Recommendations"):
                                for rec in data['recommendations']:
                                    st.markdown(f"• {rec}")
                        
                        st.markdown("---")
                
                # Visual scoring chart
                st.subheader("📊 Criteria Scoring Breakdown")
                
                chart_data = []
                for name, data in criteria_data:
                    if data['score'] > 0:  # Only include criteria with data
                        chart_data.append({
                            'Criteria': name,
                            'Score': data['score'],
                            'Status': 'Excellent' if data['score'] >= 80 else 
                                    'Good' if data['score'] >= 60 else 
                                    'Moderate' if data['score'] >= 40 else 'Poor'
                        })
                
                if chart_data:
                    df_chart = pd.DataFrame(chart_data)
                    
                    fig = px.bar(
                        df_chart,
                        x='Criteria',
                        y='Score',
                        color='Status',
                        color_discrete_map={
                            'Excellent': 'green',
                            'Good': 'lightgreen', 
                            'Moderate': 'orange',
                            'Poor': 'red'
                        },
                        title='Sustainability Criteria Assessment',
                        labels={'Score': 'Suitability Score (0-100)'}
                    )
                    
                    fig.add_hline(y=80, line_dash="dash", line_color="green", 
                                 annotation_text="Excellent Threshold (80)")
                    fig.add_hline(y=60, line_dash="dash", line_color="orange", 
                                 annotation_text="Good Threshold (60)")
                    fig.add_hline(y=40, line_dash="dash", line_color="red", 
                                 annotation_text="Minimum Suitability (40)")
                    
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Integrated recommendations
                st.subheader("🎯 Integrated Development Recommendations")
                
                all_recommendations = []
                for _, data in criteria_data:
                    all_recommendations.extend(data['recommendations'])
                
                if all_recommendations:
                    # Prioritize recommendations
                    priority_recs = []
                    general_recs = []
                    
                    for rec in set(all_recommendations):  # Remove duplicates
                        if any(word in rec.lower() for word in ['urgent', 'critical', 'major', 'avoid']):
                            priority_recs.append(rec)
                        else:
                            general_recs.append(rec)
                    
                    if priority_recs:
                        st.error("**🚨 High Priority Actions:**")
                        for rec in priority_recs:
                            st.markdown(f"• {rec}")
                    
                    if general_recs:
                        st.info("**📋 General Recommendations:**")
                        for rec in general_recs:
                            st.markdown(f"• {rec}")
                else:
                    st.success("✅ **Area shows good conditions across available criteria.**")
            
            else:
                st.error("❌ Unable to analyze the selected area. Please ensure you've drawn a valid shape.")
        else:
            st.warning("⚠️ Please draw a polygon, rectangle, or circle on the map to analyze.")
    else:
        st.warning("⚠️ No area selected. Please draw a shape on the map first.")
        st.write("🔍 **DEBUG: Failed condition check:**")
        st.write(f"   - map_data exists: {map_data is not None}")
        st.write(f"   - 'all_drawings' in map_data: {'all_drawings' in map_data if map_data else 'N/A'}")
        st.write(f"   - map_data['all_drawings'] truthy: {bool(map_data.get('all_drawings')) if map_data else 'N/A'}")

elif analyze_button:
    st.warning("⚠️ Please draw an area on the map before analyzing.")
    st.write("🔍 **DEBUG: analyze_button=True but no map_data condition met**")

# Additional information
st.markdown("---")
st.info("""
### 💡 **About This Integrated Analysis**

This tool combines data from all sustainability analysis modules to provide comprehensive area assessment:

**🔍 Analysis Method:**
- Identifies all data points within your selected area
- Calculates average scores for each criteria
- Provides weighted recommendations based on local conditions
- Uses international standards (WHO, UN-Habitat) for thresholds

**📊 Scoring System:**
- **80-100**: Excellent conditions
- **60-79**: Good conditions  
- **40-59**: Moderate conditions - improvements beneficial
- **0-39**: Poor conditions - improvements essential

**🎯 Use Cases:**
- **Development Planning**: Assess suitability before expansion
- **Policy Making**: Identify areas needing investment
- **Environmental Planning**: Balance development with sustainability
- **Infrastructure Planning**: Prioritize service improvements
""")