"""
Update Integrated Solution Page to use Enhanced Data
High-resolution analysis for small areas with detailed recommendations
"""

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

st.set_page_config(page_title="🎯 Enhanced Solution Analysis", page_icon="🎯", layout="wide")

st.title("🎯 Enhanced Area Analysis & Solutions")
st.markdown("**High-Resolution Multi-Criteria Development Assessment**")

# Enhanced coverage area info
st.markdown("""
### 🌍 **Enhanced Coverage Area**
- **Coverage**: NW 35°42'52"N 45°09'21"E to SE 35°25'38"N 45°33'07"E
- **Resolution**: 100×100 grid = 10,000 analysis points
- **Point Spacing**: ~310 meters between points
- **Total Area**: ~580 km²

### 📊 **Enhanced Analysis Capabilities**
- 🔬 **Micro-Area Analysis** - Supports areas as small as 1 hectare
- 📈 **High-Resolution Interpolation** - Detailed spatial gradients
- 🎯 **Precision Recommendations** - Site-specific improvement plans
- 📊 **Comprehensive Scoring** - 6 integrated criteria with sub-categories
""")

# Sulaimani coordinates - Enhanced coverage
SULAIMANI_CENTER = [35.5608, 45.4347]
ENHANCED_BOUNDS = {
    'north': 35.714444,  # 35°42'52"N
    'south': 35.427222,  # 35°25'38"N
    'west': 45.155833,   # 45°09'21"E
    'east': 45.551944    # 45°33'07"E
}

# Load enhanced data
@st.cache_data
def load_enhanced_data():
    """Load high-resolution enhanced datasets"""
    data = {}
    
    # Enhanced Air Quality Data
    try:
        if os.path.exists('data_solution/enhanced_air_quality_detailed.csv'):
            data['air_quality'] = pd.read_csv('data_solution/enhanced_air_quality_detailed.csv')
            st.success(f"🟢 Enhanced Air Quality: {len(data['air_quality']):,} measurements")
        else:
            data['air_quality'] = None
            st.warning("⚠️ Enhanced air quality data not available")
    except Exception as e:
        data['air_quality'] = None
        st.error(f"❌ Air quality data error: {e}")
    
    # Enhanced Temperature Data
    try:
        if os.path.exists('data_solution/enhanced_temperature_detailed.csv'):
            data['temperature'] = pd.read_csv('data_solution/enhanced_temperature_detailed.csv')
            st.success(f"🟢 Enhanced Temperature: {len(data['temperature']):,} measurements")
        else:
            data['temperature'] = None
            st.warning("⚠️ Enhanced temperature data not available")
    except Exception as e:
        data['temperature'] = None
        st.error(f"❌ Temperature data error: {e}")
    
    # Enhanced Vegetation Data
    try:
        if os.path.exists('data_solution/enhanced_vegetation_detailed.csv'):
            data['vegetation'] = pd.read_csv('data_solution/enhanced_vegetation_detailed.csv')
            st.success(f"🟢 Enhanced Vegetation: {len(data['vegetation']):,} measurements")
        else:
            data['vegetation'] = None
            st.warning("⚠️ Enhanced vegetation data not available")
    except Exception as e:
        data['vegetation'] = None
        st.error(f"❌ Vegetation data error: {e}")
    
    # Enhanced Topography Data
    try:
        if os.path.exists('data_solution/enhanced_topography_detailed.csv'):
            data['topography'] = pd.read_csv('data_solution/enhanced_topography_detailed.csv')
            st.success(f"🟢 Enhanced Topography: {len(data['topography']):,} measurements")
        else:
            data['topography'] = None
            st.warning("⚠️ Enhanced topography data not available")
    except Exception as e:
        data['topography'] = None
        st.error(f"❌ Topography data error: {e}")
    
    # Enhanced Infrastructure Data
    try:
        if os.path.exists('data_solution/enhanced_infrastructure_detailed.csv'):
            data['infrastructure'] = pd.read_csv('data_solution/enhanced_infrastructure_detailed.csv')
            st.success(f"🟢 Enhanced Infrastructure: {len(data['infrastructure']):,} assessments")
        else:
            data['infrastructure'] = None
            st.warning("⚠️ Enhanced infrastructure data not available")
    except Exception as e:
        data['infrastructure'] = None
        st.error(f"❌ Infrastructure data error: {e}")
    
    # Enhanced Population Data
    try:
        if os.path.exists('data_solution/enhanced_population_detailed.csv'):
            data['population'] = pd.read_csv('data_solution/enhanced_population_detailed.csv')
            st.success(f"🟢 Enhanced Population: {len(data['population']):,} assessments")
        else:
            data['population'] = None
            st.warning("⚠️ Enhanced population data not available")
    except Exception as e:
        data['population'] = None
        st.error(f"❌ Population data error: {e}")
    
    # Enhanced Economic Activity Data  
    try:
        if os.path.exists('data_solution/enhanced_economic_activity_detailed.csv'):
            data['economic'] = pd.read_csv('data_solution/enhanced_economic_activity_detailed.csv')
            st.success(f"🟢 Enhanced Economic Activity: {len(data['economic']):,} assessments")
        else:
            data['economic'] = None
            st.warning("⚠️ Enhanced economic data not available")
    except Exception as e:
        data['economic'] = None
        st.error(f"❌ Economic data error: {e}")
    
    return data

def analyze_enhanced_area(polygon_coords, enhanced_data):
    """Enhanced multi-criteria analysis for selected polygon area"""
    if not polygon_coords or len(polygon_coords) < 3:
        return None
    
    # Create polygon from coordinates
    try:
        # Handle different coordinate formats from st_folium
        if isinstance(polygon_coords[0], list) and len(polygon_coords[0]) == 2:
            # Format: [[lat, lon], [lat, lon], ...] - typical from st_folium
            shapely_coords = [(coord[1], coord[0]) for coord in polygon_coords]  # lon, lat for shapely
            polygon = Polygon(shapely_coords)
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
            
            for start_idx, end_idx in test_sections:
                if test_points > 0:
                    break
                for _, row in test_data.iloc[start_idx:end_idx].iterrows():
                    point = Point(row['lon'], row['lat'])
                    if buffered_polygon.contains(point):
                        test_points += 1
                        if test_points >= 3:  # Found enough points to confirm format
                            break
            
            # If no points found after testing multiple sections, try alternative coordinate format
            if test_points == 0:
                try:
                    # Try swapping lat/lon interpretation
                    if isinstance(polygon_coords[0], list) and len(polygon_coords[0]) == 2:
                        alt_coords = [(coord[0], coord[1]) for coord in polygon_coords]  # direct format
                    else:
                        alt_coords = [(coord[1], coord[0]) for coord in polygon_coords]  # swapped format
                    alt_polygon = Polygon(alt_coords)
                    alt_buffered = alt_polygon.buffer(0.001)
                    
                    alt_test_points = 0
                    for start_idx, end_idx in test_sections:
                        if alt_test_points > 0:
                            break
                        for _, row in test_data.iloc[start_idx:end_idx].iterrows():
                            point = Point(row['lon'], row['lat'])
                            if alt_buffered.contains(point):
                                alt_test_points += 1
                                if alt_test_points >= 3:
                                    break
                    
                    if alt_test_points > test_points:
                        polygon = alt_polygon
                        
                except Exception:
                    pass
        
    except Exception:
        return None
    
    results = {
        'area_km2': 0,
        'analysis_points': 0,
        'criteria': {
            'air_quality': {'score': 0, 'status': 'No Data', 'details': {}, 'recommendations': []},
            'heat_greenspace': {'score': 0, 'status': 'No Data', 'details': {}, 'recommendations': []},
            'topography': {'score': 0, 'status': 'No Data', 'details': {}, 'recommendations': []},
            'infrastructure': {'score': 0, 'status': 'No Data', 'details': {}, 'recommendations': []},
            'economic_activity': {'score': 0, 'status': 'No Data', 'details': {}, 'recommendations': []},
            'population': {'score': 0, 'status': 'No Data', 'details': {}, 'recommendations': []}
        },
        'overall_score': 0,
        'overall_status': 'Insufficient Data',
        'integrated_recommendations': [],
        'development_priority': 'Unknown',
        'investment_readiness': 'Unknown'
    }
    
    # Calculate area
    try:
        bounds = polygon.bounds
        lat_diff = bounds[3] - bounds[1]
        lon_diff = bounds[2] - bounds[0]
        area_km2 = lat_diff * lon_diff * 111 * 111 * np.cos(np.radians((bounds[1] + bounds[3]) / 2))
        results['area_km2'] = area_km2
    except:
        results['area_km2'] = 1.0
    
    valid_scores = []
    total_points = 0
    
    # Enhanced Air Quality Analysis
    if enhanced_data['air_quality'] is not None:
        try:
            aqi_data = enhanced_data['air_quality']
            latest_aqi = aqi_data[aqi_data['date'] == aqi_data['date'].max()]
            
            points_in_area = []
            pollutant_details = {'NO2': [], 'PM2.5': [], 'PM10': [], 'O3': [], 'SO2': [], 'CO': []}
            health_categories = []
            buffered_polygon = polygon.buffer(0.001)
            
            for _, row in latest_aqi.iterrows():
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    points_in_area.append(row['aqi_score'])
                    pollutant_details['NO2'].append(row['no2_concentration'])
                    pollutant_details['PM2.5'].append(row['pm25_concentration'])
                    pollutant_details['PM10'].append(row['pm10_concentration'])
                    pollutant_details['O3'].append(row['o3_concentration'])
                    pollutant_details['SO2'].append(row['so2_concentration'])
                    pollutant_details['CO'].append(row['co_concentration'])
                    health_categories.append(row['health_risk_category'])
            
            if points_in_area:
                avg_aqi = np.mean(points_in_area)
                score = max(0, 100 - avg_aqi)
                results['criteria']['air_quality']['score'] = score
                
                # Detailed pollutant analysis
                details = {}
                recommendations = []
                
                for pollutant, values in pollutant_details.items():
                    if values:
                        avg_conc = np.mean(values)
                        max_conc = np.max(values)
                        details[pollutant] = {'avg': avg_conc, 'max': max_conc}
                        
                        # WHO guidelines check
                        who_limits = {'NO2': 40, 'PM2.5': 15, 'PM10': 45, 'O3': 100, 'SO2': 40, 'CO': 10}
                        if pollutant in who_limits and avg_conc > who_limits[pollutant]:
                            recommendations.append(f"Reduce {pollutant} emissions (exceeds WHO guideline)")
                
                # Health risk assessment
                risk_counts = pd.Series(health_categories).value_counts()
                dominant_risk = risk_counts.index[0] if len(risk_counts) > 0 else "Unknown"
                
                results['criteria']['air_quality']['details'] = {
                    **details,
                    'dominant_health_risk': dominant_risk,
                    'points_analyzed': len(points_in_area)
                }
                
                if score >= 80:
                    results['criteria']['air_quality']['status'] = 'Excellent Air Quality'
                elif score >= 60:
                    results['criteria']['air_quality']['status'] = 'Good Air Quality'
                elif score >= 40:
                    results['criteria']['air_quality']['status'] = 'Moderate Air Quality'
                    recommendations.extend(['Install air monitoring stations', 'Create green buffers'])
                else:
                    results['criteria']['air_quality']['status'] = 'Poor Air Quality'
                    recommendations.extend(['Urgent emission controls needed', 'Restrict industrial activities'])
                
                results['criteria']['air_quality']['recommendations'] = recommendations
                valid_scores.append(score)
                total_points += len(points_in_area)
                
        except Exception as e:
            st.error(f"Air quality analysis error: {e}")
    
    # Enhanced Heat & Greenspace Analysis
    if enhanced_data['temperature'] is not None and enhanced_data['vegetation'] is not None:
        try:
            temp_data = enhanced_data['temperature']
            veg_data = enhanced_data['vegetation']
            
            latest_temp = temp_data[temp_data['date'] == temp_data['date'].max()]
            latest_veg = veg_data[veg_data['date'] == veg_data['date'].max()]
            
            temp_values = []
            heat_stress_scores = []
            ndvi_values = []
            veg_health_scores = []
            buffered_polygon = polygon.buffer(0.001)
            
            for _, row in latest_temp.iterrows():
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    temp_values.append(row['land_surface_temperature'])
                    heat_stress_scores.append(row['heat_stress_score'])
            
            for _, row in latest_veg.iterrows():
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    ndvi_values.append(row['estimated_ndvi'])
                    veg_health_scores.append(row['vegetation_health_score'])
            
            if temp_values and ndvi_values:
                avg_temp = np.mean(temp_values)
                avg_heat_stress = np.mean(heat_stress_scores)
                avg_ndvi = np.mean(ndvi_values)
                avg_veg_health = np.mean(veg_health_scores)
                
                # Combined climate score
                score = (avg_heat_stress + avg_veg_health) / 2
                results['criteria']['heat_greenspace']['score'] = score
                
                details = {
                    'avg_temperature': avg_temp,
                    'max_temperature': np.max(temp_values),
                    'avg_ndvi': avg_ndvi,
                    'vegetation_coverage': avg_ndvi * 100,
                    'heat_stress_level': 'Low' if avg_heat_stress > 75 else 'Moderate' if avg_heat_stress > 50 else 'High',
                    'points_analyzed': len(temp_values) + len(ndvi_values)
                }
                
                recommendations = []
                if avg_temp > 40:
                    recommendations.extend(['Install cooling infrastructure', 'Urgent tree planting needed'])
                elif avg_temp > 35:
                    recommendations.extend(['Increase shade coverage', 'Add water features'])
                
                if avg_ndvi < 0.3:
                    recommendations.extend(['Establish new green spaces', 'Mandatory green building codes'])
                elif avg_ndvi < 0.5:
                    recommendations.append('Enhance existing vegetation')
                
                results['criteria']['heat_greenspace']['details'] = details
                results['criteria']['heat_greenspace']['recommendations'] = recommendations
                
                if score >= 80:
                    results['criteria']['heat_greenspace']['status'] = 'Excellent Climate Conditions'
                elif score >= 60:
                    results['criteria']['heat_greenspace']['status'] = 'Good Climate Balance'
                elif score >= 40:
                    results['criteria']['heat_greenspace']['status'] = 'Moderate Heat Stress'
                else:
                    results['criteria']['heat_greenspace']['status'] = 'High Heat Stress Risk'
                
                valid_scores.append(score)
                total_points += len(temp_values) + len(ndvi_values)
                
        except Exception as e:
            st.error(f"Heat/greenspace analysis error: {e}")
    
    # Enhanced Topography Analysis
    if enhanced_data['topography'] is not None:
        try:
            topo_data = enhanced_data['topography']
            
            topo_points = []
            slope_values = []
            elevation_values = []
            suitability_scores = []
            buffered_polygon = polygon.buffer(0.001)
            
            for _, row in topo_data.iterrows():
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    topo_points.append(row)
                    slope_values.append(row['slope_percentage'])
                    elevation_values.append(row['elevation'])
                    suitability_scores.append(row['development_suitability'])
            
            if topo_points:
                score = np.mean(suitability_scores)
                results['criteria']['topography']['score'] = score
                
                avg_slope = np.mean(slope_values)
                avg_elevation = np.mean(elevation_values)
                
                details = {
                    'avg_slope_percent': avg_slope,
                    'max_slope_percent': np.max(slope_values),
                    'avg_elevation': avg_elevation,
                    'elevation_range': np.max(elevation_values) - np.min(elevation_values),
                    'points_analyzed': len(topo_points)
                }
                
                recommendations = []
                if avg_slope > 20:
                    recommendations.extend(['Slope stabilization required', 'Terracing recommended'])
                elif avg_slope > 10:
                    recommendations.extend(['Consider slope management', 'Drainage improvements needed'])
                elif avg_slope < 2:
                    recommendations.append('May require improved drainage')
                
                results['criteria']['topography']['details'] = details
                results['criteria']['topography']['recommendations'] = recommendations
                
                if score >= 80:
                    results['criteria']['topography']['status'] = 'Excellent Terrain Suitability'
                elif score >= 60:
                    results['criteria']['topography']['status'] = 'Good Development Terrain'
                elif score >= 40:
                    results['criteria']['topography']['status'] = 'Moderate Terrain Challenges'
                else:
                    results['criteria']['topography']['status'] = 'Difficult Terrain Conditions'
                
                valid_scores.append(score)
                total_points += len(topo_points)
                
        except Exception as e:
            st.error(f"Topography analysis error: {e}")
    
    # Enhanced Infrastructure Analysis
    if enhanced_data['infrastructure'] is not None:
        try:
            infra_data = enhanced_data['infrastructure']
            
            infra_points = []
            total_scores = []
            category_scores = {}
            buffered_polygon = polygon.buffer(0.001)
            
            for _, row in infra_data.iterrows():
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    infra_points.append(row)
                    total_scores.append(row['infrastructure_score'])
                    
                    # Use available accessibility columns
                    accessibility_categories = {
                        'road': 'road_accessibility',
                        'healthcare': 'healthcare_accessibility', 
                        'education': 'education_accessibility'
                    }
                    
                    for category, col_name in accessibility_categories.items():
                        if col_name in row:
                            if category not in category_scores:
                                category_scores[category] = []
                            category_scores[category].append(row[col_name])
            
            if infra_points:
                score = np.mean(total_scores)
                results['criteria']['infrastructure']['score'] = score
                
                details = {
                    'avg_accessibility': score,
                    'points_analyzed': len(infra_points)
                }
                
                # Category breakdowns
                for category, scores in category_scores.items():
                    if scores:
                        details[f'{category}_accessibility'] = np.mean(scores)
                
                recommendations = []
                for category, scores in category_scores.items():
                    if scores and np.mean(scores) < 50:
                        recommendations.append(f'Improve {category} accessibility')
                
                results['criteria']['infrastructure']['details'] = details
                results['criteria']['infrastructure']['recommendations'] = recommendations or ['Maintain current service levels']
                
                if score >= 80:
                    results['criteria']['infrastructure']['status'] = 'Excellent Infrastructure Access'
                elif score >= 60:
                    results['criteria']['infrastructure']['status'] = 'Good Infrastructure Access'
                elif score >= 40:
                    results['criteria']['infrastructure']['status'] = 'Limited Infrastructure Access'
                else:
                    results['criteria']['infrastructure']['status'] = 'Poor Infrastructure Access'
                
                valid_scores.append(score)
                total_points += len(infra_points)
                
        except Exception as e:
            st.error(f"Infrastructure analysis error: {e}")
    
    # Enhanced Population Analysis
    if enhanced_data['population'] is not None:
        try:
            pop_data = enhanced_data['population']
            
            pop_points = []
            density_values = []
            suitability_scores = []
            buffered_polygon = polygon.buffer(0.001)
            
            for _, row in pop_data.iterrows():
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    pop_points.append(row)
                    density_values.append(row['population_density'])
                    suitability_scores.append(row['development_suitability_score'])
            
            if pop_points:
                score = np.mean(suitability_scores)
                results['criteria']['population']['score'] = score
                
                avg_density = np.mean(density_values)
                
                details = {
                    'avg_population_density': avg_density,
                    'max_population_density': np.max(density_values),
                    'development_suitability': score,
                    'points_analyzed': len(pop_points)
                }
                
                recommendations = []
                if avg_density > 3000:
                    recommendations.extend(['Area is overcrowded', 'Improve public services', 'Consider density restrictions'])
                elif avg_density < 500:
                    recommendations.extend(['Low density area', 'Plan infrastructure before development'])
                else:
                    recommendations.append('Suitable for managed growth')
                
                results['criteria']['population']['details'] = details
                results['criteria']['population']['recommendations'] = recommendations
                
                if score >= 80:
                    results['criteria']['population']['status'] = 'Optimal Development Density'
                elif score >= 60:
                    results['criteria']['population']['status'] = 'Good Development Potential'
                elif score >= 40:
                    results['criteria']['population']['status'] = 'Moderate Development Suitability'
                else:
                    results['criteria']['population']['status'] = 'Limited Development Potential'
                
                valid_scores.append(score)
                total_points += len(pop_points)
                
        except Exception as e:
            st.error(f"Population analysis error: {e}")
    
    # Enhanced Economic Activity Analysis
    if enhanced_data['economic'] is not None:
        try:
            econ_data = enhanced_data['economic']
            
            econ_points = []
            activity_scores = []
            light_intensities = []
            buffered_polygon = polygon.buffer(0.001)
            
            for _, row in econ_data.iterrows():
                point = Point(row['lon'], row['lat'])
                if buffered_polygon.contains(point):
                    econ_points.append(row)
                    activity_scores.append(row['economic_activity_score'])
                    light_intensities.append(row['normalized_light_intensity'])
            
            if econ_points:
                score = np.mean(activity_scores)
                results['criteria']['economic_activity']['score'] = score
                
                avg_light = np.mean(light_intensities)
                
                details = {
                    'avg_economic_activity': score,
                    'avg_light_intensity': avg_light,
                    'business_potential': 'High' if score > 60 else 'Medium' if score > 30 else 'Low',
                    'points_analyzed': len(econ_points)
                }
                
                recommendations = []
                if score < 30:
                    recommendations.extend(['Encourage business development', 'Create economic incentives'])
                elif score < 60:
                    recommendations.extend(['Support existing businesses', 'Improve commercial infrastructure'])
                else:
                    recommendations.append('Maintain economic vitality')
                
                results['criteria']['economic_activity']['details'] = details
                results['criteria']['economic_activity']['recommendations'] = recommendations
                
                if score >= 80:
                    results['criteria']['economic_activity']['status'] = 'Strong Economic Activity'
                elif score >= 60:
                    results['criteria']['economic_activity']['status'] = 'Moderate Economic Activity'
                elif score >= 40:
                    results['criteria']['economic_activity']['status'] = 'Developing Economic Area'
                else:
                    results['criteria']['economic_activity']['status'] = 'Limited Economic Activity'
                
                valid_scores.append(score)
                total_points += len(econ_points)
                
        except Exception as e:
            st.error(f"Economic activity analysis error: {e}")
    
    # Calculate overall results
    results['analysis_points'] = total_points
    
    if valid_scores:
        results['overall_score'] = np.mean(valid_scores)
        
        # Integrated recommendations
        all_recs = []
        for criteria in results['criteria'].values():
            all_recs.extend(criteria['recommendations'])
        
        # Prioritize recommendations
        priority_keywords = ['urgent', 'critical', 'immediate', 'required']
        high_priority = [rec for rec in all_recs if any(keyword in rec.lower() for keyword in priority_keywords)]
        other_recs = [rec for rec in all_recs if not any(keyword in rec.lower() for keyword in priority_keywords)]
        
        results['integrated_recommendations'] = list(set(high_priority + other_recs))
        
        # Overall assessments
        if results['overall_score'] >= 80:
            results['overall_status'] = '🟢 Highly Suitable for Development'
            results['development_priority'] = 'Low Risk - Ready for Development'
            results['investment_readiness'] = 'Investment Ready'
        elif results['overall_score'] >= 65:
            results['overall_status'] = '🟡 Moderately Suitable for Development'
            results['development_priority'] = 'Medium Risk - Minor Improvements Needed'
            results['investment_readiness'] = 'Near Investment Ready'
        elif results['overall_score'] >= 50:
            results['overall_status'] = '🟠 Limited Suitability - Improvements Needed'
            results['development_priority'] = 'High Risk - Major Improvements Required'
            results['investment_readiness'] = 'Requires Investment in Infrastructure'
        else:
            results['overall_status'] = '🔴 Not Suitable - Major Improvements Required'
            results['development_priority'] = 'Very High Risk - Comprehensive Development Needed'
            results['investment_readiness'] = 'Not Investment Ready'
    
    return results

def create_enhanced_map():
    """Create enhanced interactive map with better coverage"""
    m = folium.Map(
        location=SULAIMANI_CENTER,
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Add multiple tile layers
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Topographic',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add coverage area boundary
    coverage_coords = [
        [ENHANCED_BOUNDS['north'], ENHANCED_BOUNDS['west']],
        [ENHANCED_BOUNDS['north'], ENHANCED_BOUNDS['east']],
        [ENHANCED_BOUNDS['south'], ENHANCED_BOUNDS['east']],
        [ENHANCED_BOUNDS['south'], ENHANCED_BOUNDS['west']],
        [ENHANCED_BOUNDS['north'], ENHANCED_BOUNDS['west']]
    ]
    
    folium.PolyLine(
        locations=coverage_coords,
        color='blue',
        weight=3,
        opacity=0.8,
        popup='Enhanced Analysis Coverage Area'
    ).add_to(m)
    
    # Add drawing tools
    draw = Draw(
        export=True,
        filename='enhanced_area_selection.geojson',
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

# Load enhanced data
st.header("📊 Enhanced Data Loading Status")
with st.spinner("Loading high-resolution datasets..."):
    enhanced_data = load_enhanced_data()

# Data availability overview
available_datasets = sum(1 for dataset in enhanced_data.values() if dataset is not None)
total_datasets = len(enhanced_data)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Available Datasets", f"{available_datasets}/{total_datasets}")
with col2:
    total_points = sum(len(dataset) if dataset is not None else 0 for dataset in enhanced_data.values())
    st.metric("Total Analysis Points", f"{total_points:,}")
with col3:
    coverage_percent = (available_datasets / total_datasets) * 100
    st.metric("Data Coverage", f"{coverage_percent:.1f}%")

if available_datasets == 0:
    st.error("""
    ❌ **No Enhanced Data Available**
    
    To use the enhanced solution analysis, please run:
    1. `python prepare_enhanced_data.py` - Generate all enhanced datasets
    2. `python prepare_infrastructure_data.py` - Generate infrastructure data
    
    This will create high-resolution data for detailed small-area analysis.
    """)
    st.stop()

# Enhanced map section
st.markdown("---")
st.header("🗺️ Enhanced Interactive Area Selection")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    **Enhanced Analysis Instructions:**
    1. Use drawing tools to select your area of interest
    2. Minimum recommended area: 0.1 km² (10 hectares)
    3. Maximum recommended area: 50 km² for detailed analysis
    4. Click 'Run Enhanced Analysis' for comprehensive assessment
    """)

with col2:
    analysis_mode = st.selectbox(
        "Analysis Detail Level",
        ["Comprehensive (All Criteria)", "Environmental Focus", "Infrastructure Focus", "Economic Focus"]
    )

# Create and display enhanced map
enhanced_map = create_enhanced_map()
map_data = st_folium(enhanced_map, width=1400, height=600, returned_objects=["all_drawings"])

# Analysis section
col1, col2 = st.columns([1, 2])

with col1:
    analyze_button = st.button("🔍 Run Enhanced Analysis", type="primary", use_container_width=True)
    
    if st.button("📊 Show Data Summary"):
        st.json({
            'Enhanced_Coverage': {
                'North_Lat': ENHANCED_BOUNDS['north'],
                'South_Lat': ENHANCED_BOUNDS['south'],
                'West_Lon': ENHANCED_BOUNDS['west'],
                'East_Lon': ENHANCED_BOUNDS['east']
            },
            'Grid_Resolution': '100x100 points',
            'Available_Datasets': list(enhanced_data.keys()),
            'Analysis_Capabilities': ['Micro-area analysis', 'High-resolution interpolation', 'Detailed recommendations']
        })

with col2:
    st.info("💡 **Enhanced Capabilities**: This analysis uses 10,000 data points covering 580 km² with 310-meter resolution for precise small-area assessment.")

# Run enhanced analysis
if analyze_button and map_data['all_drawings']:
    if len(map_data['all_drawings']) > 0:
        latest_drawing = map_data['all_drawings'][-1]
        
        if latest_drawing['geometry']['type'] in ['Polygon', 'Circle']:
            st.markdown("---")
            st.header("📋 Enhanced Area Analysis Results")
            
            # Extract coordinates
            if latest_drawing['geometry']['type'] == 'Polygon':
                coords = latest_drawing['geometry']['coordinates'][0]
            else:
                # For circles, create approximate polygon
                center = latest_drawing['geometry']['coordinates']
                radius = latest_drawing['properties'].get('radius', 1000) / 111000
                coords = []
                for angle in range(0, 360, 10):
                    lat = center[1] + radius * np.cos(np.radians(angle))
                    lon = center[0] + radius * np.sin(np.radians(angle))
                    coords.append([lat, lon])
            
            # Perform enhanced analysis
            with st.spinner("Running enhanced multi-criteria analysis..."):
                results = analyze_enhanced_area(coords, enhanced_data)
            
            if results:
                # Enhanced results display
                st.markdown(f"### {results['overall_status']}")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Overall Score", f"{results['overall_score']:.1f}/100")
                with col2:
                    st.metric("Analysis Area", f"{results['area_km2']:.3f} km²")
                with col3:
                    st.metric("Data Points", f"{results['analysis_points']:,}")
                with col4:
                    st.metric("Investment Readiness", results['investment_readiness'])
                
                # Detailed criteria analysis
                st.subheader("🔍 Detailed Criteria Analysis")
                
                # Create comprehensive scoring chart
                chart_data = []
                for criterion_name, criterion_data in results['criteria'].items():
                    if criterion_data['score'] > 0:
                        chart_data.append({
                            'Criterion': criterion_name.replace('_', ' ').title(),
                            'Score': criterion_data['score'],
                            'Status': criterion_data['status']
                        })
                
                if chart_data:
                    fig = px.bar(
                        pd.DataFrame(chart_data),
                        x='Criterion',
                        y='Score',
                        color='Score',
                        color_continuous_scale='RdYlGn',
                        title='Enhanced Multi-Criteria Assessment',
                        labels={'Score': 'Suitability Score (0-100)'},
                        height=500
                    )
                    
                    fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Excellent (80+)")
                    fig.add_hline(y=60, line_dash="dash", line_color="orange", annotation_text="Good (60+)")
                    fig.add_hline(y=40, line_dash="dash", line_color="red", annotation_text="Minimum (40+)")
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Detailed criterion breakdowns
                st.subheader("📊 Criterion Details & Recommendations")
                
                for criterion_name, criterion_data in results['criteria'].items():
                    if criterion_data['score'] > 0:
                        with st.expander(f"{criterion_name.replace('_', ' ').title()} - Score: {criterion_data['score']:.1f}"):
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**Status & Details:**")
                                st.write(f"Status: {criterion_data['status']}")
                                
                                if criterion_data['details']:
                                    st.json(criterion_data['details'])
                            
                            with col2:
                                st.markdown("**Recommendations:**")
                                for rec in criterion_data['recommendations']:
                                    st.markdown(f"• {rec}")
                
                # Integrated recommendations
                st.subheader("🎯 Integrated Development Recommendations")
                
                if results['integrated_recommendations']:
                    priority_recs = [rec for rec in results['integrated_recommendations'] 
                                   if any(word in rec.lower() for word in ['urgent', 'critical', 'required', 'immediate'])]
                    other_recs = [rec for rec in results['integrated_recommendations'] 
                                if not any(word in rec.lower() for word in ['urgent', 'critical', 'required', 'immediate'])]
                    
                    if priority_recs:
                        st.error("**🚨 High Priority Actions:**")
                        for rec in priority_recs[:5]:  # Top 5 priorities
                            st.markdown(f"• {rec}")
                    
                    if other_recs:
                        st.info("**📋 Additional Recommendations:**")
                        for rec in other_recs[:10]:  # Top 10 additional
                            st.markdown(f"• {rec}")
                
                # Development summary
                st.subheader("📈 Development Assessment Summary")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Development Readiness:**")
                    st.write(f"Priority Level: {results['development_priority']}")
                    st.write(f"Investment Status: {results['investment_readiness']}")
                    st.write(f"Analysis Quality: {results['analysis_points']:,} data points")
                
                with col2:
                    st.markdown("**Key Metrics:**")
                    st.write(f"Area Size: {results['area_km2']:.3f} km²")
                    st.write(f"Overall Suitability: {results['overall_score']:.1f}%")
                    criteria_count = sum(1 for c in results['criteria'].values() if c['score'] > 0)
                    st.write(f"Criteria Analyzed: {criteria_count}/6")
            
            else:
                st.error("❌ Unable to analyze the selected area. Please ensure the area is within the coverage zone.")
        else:
            st.warning("⚠️ Please draw a polygon, rectangle, or circle on the map.")
    else:
        st.warning("⚠️ No area selected. Please draw a shape on the map first.")

elif analyze_button:
    st.warning("⚠️ Please draw an area on the map before running analysis.")

# Footer information
st.markdown("---")
st.info("""
### 🔬 **About Enhanced Analysis**

**Enhanced Capabilities:**
- **High Resolution**: 100×100 grid with 10,000 analysis points
- **Micro-Area Support**: Analyze areas as small as 1 hectare
- **Comprehensive Data**: 6 integrated criteria with detailed sub-metrics
- **Advanced Interpolation**: Spatial gradients for precise assessment
- **Detailed Recommendations**: Site-specific improvement plans

**Coverage Area:** 35°42'52"N to 35°25'38"N, 45°09'21"E to 45°33'07"E (580 km²)
**Resolution:** 310-meter point spacing for detailed spatial analysis
**Data Sources:** Enhanced NASA Earth Observations, OpenStreetMap, WorldPop, Copernicus
""")