"""
Quick Enhanced Data Preparation - Skip Topography
Focus on essential datasets for solution page
"""

import numpy as np
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import time
import os
from scipy.interpolate import griddata
import warnings
warnings.filterwarnings('ignore')

# Enhanced coverage coordinates for Sulaimani
NORTH_LAT = 35.714444  # 35°42'52"N
SOUTH_LAT = 35.427222  # 35°25'38"N  
WEST_LON = 45.155833   # 45°09'21"E
EAST_LON = 45.551944   # 45°33'07"E

# High resolution grid (100x100 = 10,000 points)
GRID_SIZE = 100

def create_enhanced_grid():
    """Create high-resolution coordinate grid for detailed analysis"""
    lats = np.linspace(SOUTH_LAT, NORTH_LAT, GRID_SIZE)
    lons = np.linspace(WEST_LON, EAST_LON, GRID_SIZE)
    
    lat_grid, lon_grid = np.meshgrid(lats, lons, indexing='ij')
    coordinates = []
    
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            coordinates.append({
                'lat': lat_grid[i, j],
                'lon': lon_grid[i, j],
                'grid_i': i,
                'grid_j': j
            })
    
    return pd.DataFrame(coordinates)

def generate_synthetic_topography():
    """Generate realistic topography data for Sulaimani region"""
    print("🗻 Generating synthetic topography data...")
    grid_df = create_enhanced_grid()
    
    elevation_data = []
    
    # Sulaimani's realistic elevation profile (500-1200m typical range)
    for _, row in grid_df.iterrows():
        lat, lon = row['lat'], row['lon']
        
        # Generate realistic elevation based on geographic position
        ns_factor = (lat - SOUTH_LAT) / (NORTH_LAT - SOUTH_LAT)  # North higher
        ew_factor = (lon - WEST_LON) / (EAST_LON - WEST_LON)    # East higher
        
        # Base elevation with gradients
        base_elevation = 600 + (ns_factor * 400) + (ew_factor * 200)
        
        # Add realistic terrain variation
        noise = np.random.normal(0, 50)
        elevation = max(400, min(1400, base_elevation + noise))
        
        # Calculate slope based on local elevation differences
        slope = calculate_realistic_slope(ns_factor, ew_factor)
        suitability = calculate_development_suitability(elevation, slope)
        
        elevation_data.append({
            'lat': lat,
            'lon': lon,
            'elevation': elevation,
            'slope_percentage': slope,
            'development_suitability': suitability,
            'terrain_category': categorize_terrain(slope),
            'grid_i': row['grid_i'],
            'grid_j': row['grid_j'],
            'timestamp': datetime.now().isoformat()
        })
    
    topography_df = pd.DataFrame(elevation_data)
    os.makedirs('data_solution', exist_ok=True)
    topography_df.to_csv('data_solution/enhanced_topography_detailed.csv', index=False)
    
    print(f"✅ Generated {len(topography_df):,} topography points")
    return topography_df

def calculate_realistic_slope(ns_factor, ew_factor):
    """Calculate realistic slope based on Sulaimani's terrain"""
    mountain_factor = (ns_factor + ew_factor) / 2
    base_slope = mountain_factor * 12  # 0-12% base slope
    variation = np.random.uniform(-3, 5)
    return max(0, min(30, base_slope + variation))

def categorize_terrain(slope):
    """Categorize terrain based on slope"""
    if slope < 2:
        return 'Flat'
    elif slope < 5:
        return 'Gentle'
    elif slope < 10:
        return 'Moderate'
    elif slope < 20:
        return 'Steep'
    else:
        return 'Very Steep'

def calculate_development_suitability(elevation, slope):
    """Calculate development suitability (0-100 score)"""
    # Elevation factor (prefer 500-900m)
    if 500 <= elevation <= 900:
        elev_score = 100
    elif 400 <= elevation <= 1200:
        elev_score = 80
    else:
        elev_score = max(0, 100 - abs(elevation - 700) / 10)
    
    # Slope factor (prefer < 10%)
    if slope < 5:
        slope_score = 100
    elif slope < 10:
        slope_score = 80
    elif slope < 15:
        slope_score = 60
    else:
        slope_score = max(0, 100 - (slope - 15) * 5)
    
    return (elev_score * 0.4 + slope_score * 0.6)

def generate_enhanced_infrastructure():
    """Generate enhanced infrastructure accessibility data"""
    print("🏗️ Generating enhanced infrastructure data...")
    grid_df = create_enhanced_grid()
    
    infrastructure_data = []
    
    # Define major infrastructure points in Sulaimani
    major_roads = [
        (35.5608, 45.4347),  # City center
        (35.5708, 45.4247),  # Northern district
        (35.5508, 45.4447),  # Eastern district
        (35.5508, 45.4247),  # Western district
    ]
    
    hospitals = [
        (35.5658, 45.4397),  # Central hospital
        (35.5758, 45.4447),  # Northern hospital
    ]
    
    schools = [
        (35.5608, 45.4347),  # City center schools
        (35.5708, 45.4247),  # Northern schools
        (35.5508, 45.4447),  # Eastern schools
        (35.5508, 45.4247),  # Western schools
        (35.5558, 45.4497),  # Suburban schools
    ]
    
    for _, row in grid_df.iterrows():
        lat, lon = row['lat'], row['lon']
        
        # Calculate distances to infrastructure
        road_distances = [calculate_distance(lat, lon, r[0], r[1]) for r in major_roads]
        hospital_distances = [calculate_distance(lat, lon, h[0], h[1]) for h in hospitals]
        school_distances = [calculate_distance(lat, lon, s[0], s[1]) for s in schools]
        
        # Calculate accessibility scores
        road_score = max(0, 100 - min(road_distances) * 50)  # 50 points per km
        health_score = max(0, 100 - min(hospital_distances) * 30)  # 30 points per km
        edu_score = max(0, 100 - min(school_distances) * 40)   # 40 points per km
        
        # Combined infrastructure score
        total_score = (road_score * 0.4 + health_score * 0.3 + edu_score * 0.3)
        
        infrastructure_data.append({
            'lat': lat,
            'lon': lon,
            'road_accessibility': road_score,
            'healthcare_accessibility': health_score,
            'education_accessibility': edu_score,
            'infrastructure_score': total_score,
            'nearest_road_km': min(road_distances),
            'nearest_hospital_km': min(hospital_distances),
            'nearest_school_km': min(school_distances),
            'grid_i': row['grid_i'],
            'grid_j': row['grid_j'],
            'timestamp': datetime.now().isoformat()
        })
    
    infra_df = pd.DataFrame(infrastructure_data)
    infra_df.to_csv('data_solution/enhanced_infrastructure_detailed.csv', index=False)
    
    print(f"✅ Generated {len(infra_df):,} infrastructure points")
    return infra_df

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in km using Haversine formula"""
    R = 6371  # Earth's radius in km
    
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    
    a = (np.sin(dlat/2)**2 + 
         np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2)
    
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c

def generate_enhanced_population():
    """Generate enhanced population density data"""
    print("👥 Generating enhanced population data...")
    grid_df = create_enhanced_grid()
    
    population_data = []
    
    # Population centers in Sulaimani
    for _, row in grid_df.iterrows():
        lat, lon = row['lat'], row['lon']
        
        # Distance from city center
        center_dist = calculate_distance(lat, lon, 35.5608, 45.4347)
        
        # Urban density model (higher near center, lower at edges)
        if center_dist < 2:
            base_density = np.random.uniform(3000, 8000)  # Urban core
        elif center_dist < 5:
            base_density = np.random.uniform(1500, 4000)  # Suburban
        elif center_dist < 10:
            base_density = np.random.uniform(500, 2000)   # Peri-urban
        else:
            base_density = np.random.uniform(50, 800)     # Rural
        
        # Calculate development suitability based on optimal density
        optimal_density = 2500  # People per km²
        density_deviation = abs(base_density - optimal_density) / optimal_density
        suitability = max(0, 100 - (density_deviation * 100))
        
        population_data.append({
            'lat': lat,
            'lon': lon,
            'population_density': base_density,
            'development_suitability_score': suitability,
            'distance_to_center_km': center_dist,
            'urban_category': categorize_urban_density(base_density),
            'grid_i': row['grid_i'],
            'grid_j': row['grid_j'],
            'timestamp': datetime.now().isoformat()
        })
    
    pop_df = pd.DataFrame(population_data)
    pop_df.to_csv('data_solution/enhanced_population_detailed.csv', index=False)
    
    print(f"✅ Generated {len(pop_df):,} population points")
    return pop_df

def categorize_urban_density(density):
    """Categorize urban areas by density"""
    if density < 500:
        return 'Rural'
    elif density < 1500:
        return 'Low Density'
    elif density < 3000:
        return 'Medium Density'
    elif density < 6000:
        return 'High Density'
    else:
        return 'Very High Density'

def generate_enhanced_economic_activity():
    """Generate enhanced economic activity data based on nighttime lights"""
    print("💡 Generating enhanced economic activity data...")
    grid_df = create_enhanced_grid()
    
    economic_data = []
    
    for _, row in grid_df.iterrows():
        lat, lon = row['lat'], row['lon']
        
        # Distance from economic centers
        center_dist = calculate_distance(lat, lon, 35.5608, 45.4347)
        
        # Economic activity model
        if center_dist < 2:
            light_intensity = np.random.uniform(0.6, 1.0)  # Commercial core
        elif center_dist < 5:
            light_intensity = np.random.uniform(0.3, 0.7)  # Mixed use
        elif center_dist < 10:
            light_intensity = np.random.uniform(0.1, 0.4)  # Residential
        else:
            light_intensity = np.random.uniform(0.0, 0.2)  # Rural
        
        # Economic activity score
        activity_score = light_intensity * 100
        
        economic_data.append({
            'lat': lat,
            'lon': lon,
            'normalized_light_intensity': light_intensity,
            'economic_activity_score': activity_score,
            'commercial_potential': categorize_commercial_potential(activity_score),
            'grid_i': row['grid_i'],
            'grid_j': row['grid_j'],
            'timestamp': datetime.now().isoformat()
        })
    
    econ_df = pd.DataFrame(economic_data)
    econ_df.to_csv('data_solution/enhanced_economic_activity_detailed.csv', index=False)
    
    print(f"✅ Generated {len(econ_df):,} economic activity points")
    return econ_df

def categorize_commercial_potential(score):
    """Categorize commercial potential"""
    if score < 20:
        return 'Low'
    elif score < 40:
        return 'Moderate'
    elif score < 70:
        return 'High'
    else:
        return 'Very High'

def main():
    """Main function to prepare all enhanced data (skip slow topography download)"""
    print("🚀 Starting FAST enhanced data preparation...")
    print(f"📍 Coverage area: NW({NORTH_LAT}, {WEST_LON}) to SE({SOUTH_LAT}, {EAST_LON})")
    print(f"🎯 Grid resolution: {GRID_SIZE}x{GRID_SIZE} = {GRID_SIZE**2:,} points")
    print("⚠️ Skipping real topography data (too slow) - using synthetic data")
    
    os.makedirs('data_solution', exist_ok=True)
    
    try:
        # Generate all datasets (synthetic for speed)
        print("\n📊 Generating synthetic datasets for solution page...")
        
        topo_df = generate_synthetic_topography()
        infra_df = generate_enhanced_infrastructure()
        pop_df = generate_enhanced_population()
        econ_df = generate_enhanced_economic_activity()
        
        # Create summary
        summary = {
            'coverage_area': {
                'north_lat': NORTH_LAT,
                'south_lat': SOUTH_LAT,
                'west_lon': WEST_LON,
                'east_lon': EAST_LON
            },
            'grid_resolution': {
                'grid_size': GRID_SIZE,
                'total_points': GRID_SIZE**2,
                'spacing_km': calculate_distance(SOUTH_LAT, WEST_LON, 
                                               SOUTH_LAT + (NORTH_LAT-SOUTH_LAT)/GRID_SIZE, 
                                               WEST_LON)
            },
            'datasets': {
                'topography_points': len(topo_df),
                'infrastructure_points': len(infra_df),
                'population_points': len(pop_df),
                'economic_points': len(econ_df),
                'total_data_points': len(topo_df) + len(infra_df) + len(pop_df) + len(econ_df)
            },
            'generation_timestamp': datetime.now().isoformat(),
            'note': 'Synthetic data generated for fast solution page preparation'
        }
        
        # Save summary
        with open('data_solution/enhanced_data_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"""
🎉 Enhanced data preparation complete!
📂 Data saved in 'data_solution/' folder:
   - Enhanced topography: {len(topo_df):,} points
   - Enhanced infrastructure: {len(infra_df):,} points  
   - Enhanced population: {len(pop_df):,} points
   - Enhanced economic activity: {len(econ_df):,} points

🎯 Total coverage: {GRID_SIZE**2:,} analysis points
📊 Ready for small-area solution analysis!
        """)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in data preparation: {e}")
        return False

if __name__ == "__main__":
    main()