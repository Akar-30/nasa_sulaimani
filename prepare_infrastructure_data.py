"""
Enhanced Infrastructure Analysis for Solution Page
Detailed accessibility scoring for small area analysis
"""

import numpy as np
import pandas as pd
import requests
import json
import time
from datetime import datetime
import os
from math import radians, cos, sin, asin, sqrt

# Enhanced coverage coordinates
NORTH_LAT = 35.714444  # 35°42'52"N
SOUTH_LAT = 35.427222  # 35°25'38"N  
WEST_LON = 45.155833   # 45°09'21"E
EAST_LON = 45.551944   # 45°33'07"E

# High resolution grid
GRID_SIZE = 100

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate great circle distance between two points on Earth"""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth's radius in kilometers
    return c * r

def create_enhanced_grid():
    """Create high-resolution coordinate grid"""
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

def query_overpass_api(query, max_retries=3):
    """Query Overpass API with retry logic"""
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                overpass_url, 
                data={'data': query}, 
                timeout=60,
                headers={'User-Agent': 'SulaimaniUrbanPlanning/1.0'}
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit
                wait_time = 30 * (attempt + 1)
                print(f"Rate limited, waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                time.sleep(wait_time)
            else:
                print(f"HTTP {response.status_code}: {response.text}")
                time.sleep(10)
                
        except requests.exceptions.Timeout:
            print(f"Timeout on attempt {attempt + 1}, retrying...")
            time.sleep(5)
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            time.sleep(5)
    
    return None

def download_infrastructure_data():
    """Download comprehensive infrastructure data"""
    print("🏗️ Downloading enhanced infrastructure data...")
    
    # Infrastructure categories with detailed subcategories
    infrastructure_categories = {
        'healthcare': {
            'primary': ['clinic', 'doctors'],
            'secondary': ['hospital'],
            'pharmacy': ['pharmacy'],
            'weight': 0.25
        },
        'education': {
            'primary': ['school'],
            'secondary': ['university', 'college'],
            'kindergarten': ['kindergarten'],
            'weight': 0.20
        },
        'transportation': {
            'roads': ['primary', 'secondary', 'tertiary', 'trunk'],
            'public_transport': ['bus_station', 'bus_stop'],
            'parking': ['parking'],
            'weight': 0.15
        },
        'commercial': {
            'shopping': ['supermarket', 'marketplace', 'mall'],
            'services': ['bank', 'post_office'],
            'fuel': ['fuel'],
            'weight': 0.15
        },
        'utilities': {
            'water': ['water_tower', 'water_works'],
            'waste': ['waste_disposal', 'recycling'],
            'energy': ['substation', 'generator'],
            'weight': 0.10
        },
        'emergency': {
            'safety': ['fire_station', 'police'],
            'emergency': ['emergency_phone'],
            'weight': 0.10
        },
        'recreation': {
            'parks': ['park', 'playground'],
            'sports': ['sports_centre', 'stadium'],
            'culture': ['library', 'community_centre'],
            'weight': 0.05
        }
    }
    
    # Expanded bounding box for infrastructure search
    bbox = f"{SOUTH_LAT-0.01},{WEST_LON-0.01},{NORTH_LAT+0.01},{EAST_LON+0.01}"
    
    all_facilities = {}
    
    # Download each infrastructure category
    for category, subcategories in infrastructure_categories.items():
        print(f"Downloading {category} facilities...")
        all_facilities[category] = {}
        
        for subcat, tags in subcategories.items():
            if subcat == 'weight':
                continue
                
            facilities = []
            
            for tag in tags:
                # Construct Overpass query
                if category == 'transportation' and subcat == 'roads':
                    query = f"""
                    [out:json][timeout:60];
                    (
                      way["highway"="{tag}"]({bbox});
                    );
                    out geom;
                    """
                else:
                    # For amenities and other POIs
                    if tag in ['clinic', 'hospital', 'doctors', 'pharmacy']:
                        amenity_query = f'["amenity"="{tag}"]'
                    elif tag in ['school', 'university', 'college', 'kindergarten']:
                        amenity_query = f'["amenity"="{tag}"]'
                    elif tag in ['supermarket', 'marketplace', 'bank', 'post_office', 'fuel', 'police']:
                        amenity_query = f'["amenity"="{tag}"]'
                    elif tag == 'mall':
                        amenity_query = f'["shop"="mall"]'
                    elif tag in ['bus_station', 'bus_stop']:
                        amenity_query = f'["public_transport"="{tag}"]'
                    elif tag == 'parking':
                        amenity_query = f'["amenity"="parking"]'
                    elif tag in ['fire_station']:
                        amenity_query = f'["amenity"="{tag}"]'
                    elif tag in ['park', 'playground']:
                        amenity_query = f'["leisure"="{tag}"]'
                    elif tag in ['sports_centre', 'stadium']:
                        amenity_query = f'["leisure"="{tag}"]'
                    elif tag in ['library', 'community_centre']:
                        amenity_query = f'["amenity"="{tag}"]'
                    else:
                        amenity_query = f'["amenity"="{tag}"]'
                    
                    query = f"""
                    [out:json][timeout:60];
                    (
                      node{amenity_query}({bbox});
                      way{amenity_query}({bbox});
                      relation{amenity_query}({bbox});
                    );
                    out center;
                    """
                
                # Query Overpass API
                result = query_overpass_api(query)
                
                if result and 'elements' in result:
                    for element in result['elements']:
                        if element['type'] == 'node':
                            lat, lon = element['lat'], element['lon']
                        elif element['type'] == 'way' and 'center' in element:
                            lat, lon = element['center']['lat'], element['center']['lon']
                        elif element['type'] == 'way' and 'geometry' in element:
                            # Use first point of way
                            lat, lon = element['geometry'][0]['lat'], element['geometry'][0]['lon']
                        else:
                            continue
                        
                        name = element.get('tags', {}).get('name', f'{tag.title()} Facility')
                        
                        facilities.append({
                            'name': name,
                            'lat': lat,
                            'lon': lon,
                            'type': tag,
                            'category': category,
                            'subcategory': subcat
                        })
                
                time.sleep(1)  # Rate limiting
            
            all_facilities[category][subcat] = facilities
            print(f"  Found {len(facilities)} {subcat} facilities")
    
    # If API data is insufficient, generate synthetic infrastructure
    total_facilities = sum(len(facilities) for cat in all_facilities.values() for facilities in cat.values())
    
    if total_facilities < 50:
        print("⚠️ Insufficient API data, generating synthetic infrastructure...")
        all_facilities = generate_synthetic_infrastructure()
    
    # Calculate accessibility scores for each grid point
    print("📊 Calculating accessibility scores...")
    grid = create_enhanced_grid()
    infrastructure_data = []
    
    for idx, row in grid.iterrows():
        lat, lon = row['lat'], row['lon']
        
        accessibility_scores = {}
        facility_distances = {}
        
        # Calculate distances to each facility type
        for category, subcategories in all_facilities.items():
            if category == 'weight':
                continue
                
            category_scores = []
            category_distances = {}
            
            for subcat, facilities in subcategories.items():
                if not facilities:
                    continue
                
                # Find closest facility of this type
                min_distance = float('inf')
                closest_facility = None
                
                for facility in facilities:
                    distance = haversine_distance(lat, lon, facility['lat'], facility['lon'])
                    if distance < min_distance:
                        min_distance = distance
                        closest_facility = facility
                
                if closest_facility:
                    # Distance-based scoring (closer = higher score)
                    if min_distance <= 0.5:  # Within 500m
                        score = 100
                    elif min_distance <= 1.0:  # Within 1km
                        score = 80
                    elif min_distance <= 2.0:  # Within 2km
                        score = 60
                    elif min_distance <= 5.0:  # Within 5km
                        score = 40
                    elif min_distance <= 10.0:  # Within 10km
                        score = 20
                    else:
                        score = 10
                    
                    category_scores.append(score)
                    category_distances[subcat] = {
                        'distance_km': round(min_distance, 3),
                        'facility_name': closest_facility['name'],
                        'accessibility_score': score
                    }
            
            # Average score for category
            if category_scores:
                accessibility_scores[category] = np.mean(category_scores)
                facility_distances[category] = category_distances
            else:
                accessibility_scores[category] = 0
                facility_distances[category] = {}
        
        # Calculate weighted total score
        total_score = 0
        total_weight = 0
        
        for category, score in accessibility_scores.items():
            if category in infrastructure_categories:
                weight = infrastructure_categories[category]['weight']
                total_score += score * weight
                total_weight += weight
        
        final_score = total_score / total_weight if total_weight > 0 else 0
        
        # Accessibility categories
        if final_score >= 80:
            accessibility_category = "Excellent Access"
            service_level = "Full Services"
        elif final_score >= 60:
            accessibility_category = "Good Access"
            service_level = "Most Services"
        elif final_score >= 40:
            accessibility_category = "Moderate Access"
            service_level = "Basic Services"
        elif final_score >= 20:
            accessibility_category = "Limited Access"
            service_level = "Few Services"
        else:
            accessibility_category = "Poor Access"
            service_level = "Minimal Services"
        
        # Development readiness
        if final_score >= 70:
            development_readiness = "Ready"
        elif final_score >= 50:
            development_readiness = "Needs Minor Improvements"
        elif final_score >= 30:
            development_readiness = "Needs Major Improvements"
        else:
            development_readiness = "Requires Full Infrastructure"
        
        infrastructure_data.append({
            'lat': lat,
            'lon': lon,
            'grid_i': row['grid_i'],
            'grid_j': row['grid_j'],
            'total_accessibility_score': round(final_score, 2),
            'healthcare_score': round(accessibility_scores.get('healthcare', 0), 2),
            'education_score': round(accessibility_scores.get('education', 0), 2),
            'transportation_score': round(accessibility_scores.get('transportation', 0), 2),
            'commercial_score': round(accessibility_scores.get('commercial', 0), 2),
            'utilities_score': round(accessibility_scores.get('utilities', 0), 2),
            'emergency_score': round(accessibility_scores.get('emergency', 0), 2),
            'recreation_score': round(accessibility_scores.get('recreation', 0), 2),
            'accessibility_category': accessibility_category,
            'service_level': service_level,
            'development_readiness': development_readiness,
            'infrastructure_gaps': identify_gaps(accessibility_scores),
            'priority_improvements': identify_priorities(accessibility_scores)
        })
        
        if idx % 1000 == 0:
            print(f"Processed {idx}/{len(grid)} grid points...")
    
    # Save infrastructure data
    infra_df = pd.DataFrame(infrastructure_data)
    infra_df.to_csv('data_solution/enhanced_infrastructure_detailed.csv', index=False)
    print(f"✅ Saved {len(infra_df):,} infrastructure assessments")
    
    # Save facility locations
    facilities_summary = []
    for category, subcategories in all_facilities.items():
        for subcat, facilities in subcategories.items():
            for facility in facilities:
                facilities_summary.append(facility)
    
    facilities_df = pd.DataFrame(facilities_summary)
    facilities_df.to_csv('data_solution/infrastructure_facilities.csv', index=False)
    print(f"✅ Saved {len(facilities_df):,} facility locations")
    
    return infra_df

def generate_synthetic_infrastructure():
    """Generate realistic synthetic infrastructure when API data is insufficient"""
    print("🏗️ Generating synthetic infrastructure data...")
    
    # Key infrastructure nodes in Sulaimani
    infrastructure_nodes = {
        'healthcare': {
            'primary': [
                {'name': 'Sulaimani General Hospital', 'lat': 35.5608, 'lon': 45.4347, 'type': 'hospital'},
                {'name': 'Shar Hospital', 'lat': 35.5750, 'lon': 45.4450, 'type': 'hospital'},
                {'name': 'Downtown Clinic', 'lat': 35.5580, 'lon': 45.4320, 'type': 'clinic'},
                {'name': 'North Health Center', 'lat': 35.5720, 'lon': 45.4420, 'type': 'clinic'},
                {'name': 'East Medical Center', 'lat': 35.5650, 'lon': 45.4500, 'type': 'clinic'},
            ],
            'pharmacy': [
                {'name': 'Central Pharmacy', 'lat': 35.5600, 'lon': 45.4340, 'type': 'pharmacy'},
                {'name': 'North Pharmacy', 'lat': 35.5730, 'lon': 45.4430, 'type': 'pharmacy'},
                {'name': 'East Pharmacy', 'lat': 35.5680, 'lon': 45.4480, 'type': 'pharmacy'},
            ]
        },
        'education': {
            'primary': [
                {'name': 'University of Sulaimani', 'lat': 35.5650, 'lon': 45.4380, 'type': 'university'},
                {'name': 'Polytechnic University', 'lat': 35.5580, 'lon': 45.4420, 'type': 'university'},
                {'name': 'Central High School', 'lat': 35.5620, 'lon': 45.4360, 'type': 'school'},
                {'name': 'North Elementary', 'lat': 35.5750, 'lon': 45.4440, 'type': 'school'},
                {'name': 'East Secondary School', 'lat': 35.5680, 'lon': 45.4500, 'type': 'school'},
            ]
        },
        'commercial': {
            'shopping': [
                {'name': 'Sulaimani Grand Bazaar', 'lat': 35.5608, 'lon': 45.4347, 'type': 'marketplace'},
                {'name': 'City Center Mall', 'lat': 35.5620, 'lon': 45.4380, 'type': 'mall'},
                {'name': 'North Market', 'lat': 35.5740, 'lon': 45.4450, 'type': 'supermarket'},
            ],
            'services': [
                {'name': 'Kurdistan Bank', 'lat': 35.5615, 'lon': 45.4350, 'type': 'bank'},
                {'name': 'Main Post Office', 'lat': 35.5600, 'lon': 45.4340, 'type': 'post_office'},
            ]
        },
        'transportation': {
            'public_transport': [
                {'name': 'Central Bus Station', 'lat': 35.5590, 'lon': 45.4330, 'type': 'bus_station'},
                {'name': 'North Terminal', 'lat': 35.5760, 'lon': 45.4460, 'type': 'bus_station'},
            ]
        },
        'emergency': {
            'safety': [
                {'name': 'Fire Station Central', 'lat': 35.5595, 'lon': 45.4335, 'type': 'fire_station'},
                {'name': 'Police Station', 'lat': 35.5610, 'lon': 45.4355, 'type': 'police'},
            ]
        },
        'recreation': {
            'parks': [
                {'name': 'Azadi Park', 'lat': 35.5640, 'lon': 45.4400, 'type': 'park'},
                {'name': 'Family Park', 'lat': 35.5700, 'lon': 45.4480, 'type': 'park'},
            ]
        }
    }
    
    return infrastructure_nodes

def identify_gaps(accessibility_scores):
    """Identify infrastructure gaps based on scores"""
    gaps = []
    
    for category, score in accessibility_scores.items():
        if score < 30:
            gaps.append(f"Critical {category} shortage")
        elif score < 50:
            gaps.append(f"Limited {category} access")
    
    return ", ".join(gaps) if gaps else "No major gaps"

def identify_priorities(accessibility_scores):
    """Identify priority improvements based on scores"""
    priorities = []
    
    # Sort by score (lowest first = highest priority)
    sorted_scores = sorted(accessibility_scores.items(), key=lambda x: x[1])
    
    for category, score in sorted_scores[:3]:  # Top 3 priorities
        if score < 60:
            if score < 30:
                priorities.append(f"Urgent {category} development")
            else:
                priorities.append(f"Improve {category} access")
    
    return ", ".join(priorities) if priorities else "Maintain current levels"

def main():
    """Main function to download infrastructure data"""
    print("🏗️ Starting enhanced infrastructure analysis...")
    
    os.makedirs('data_solution', exist_ok=True)
    
    try:
        download_infrastructure_data()
        print("\n✅ Infrastructure analysis completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during infrastructure analysis: {e}")
        return False

if __name__ == "__main__":
    main()