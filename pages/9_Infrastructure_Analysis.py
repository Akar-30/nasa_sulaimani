import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import requests
import time
from math import sqrt, atan2, degrees, radians, sin, cos, asin
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
import math

# Page configuration
st.set_page_config(
    page_title="🏗️ Infrastructure Analysis - NASA Space Apps",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Infrastructure Accessibility Analysis")
st.markdown("**Proximity to Essential Services for Sustainable Urban Expansion**")

# Introduction
st.markdown("""
### 🎯 **Analysis Goal**
Identify areas with **optimal access to infrastructure** for sustainable urban expansion in Sulaimani city.
Proximity to roads, hospitals, schools, and services is crucial for livability and development feasibility.

### � **Enhanced Coverage Area (2x Expansion)**
- **City Core (0.2°)** ≈ 22km radius (~1,520 km²)
- **Extended (0.3°)** ≈ 33km radius (~3,420 km²)  
- **Regional (0.5°)** ≈ 55km radius (~9,500 km²)

### �📊 **Data Sources**
- **Overpass API (OpenStreetMap)** - Real-time infrastructure data
- **Roads & Highways** - Transportation networks
- **Healthcare Facilities** - Hospitals, clinics, pharmacies
- **Educational Institutions** - Schools, universities, libraries
- **Essential Services** - Government offices, utilities
""")

# Sulaimani coordinates and configuration
SULAIMANI_CENTER = [35.5608, 45.4347]
DATA_DIR = "data"

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize session state
if 'infrastructure_analysis_completed' not in st.session_state:
    st.session_state.infrastructure_analysis_completed = False
if 'infrastructure_df' not in st.session_state:
    st.session_state.infrastructure_df = None
if 'infrastructure_params' not in st.session_state:
    st.session_state.infrastructure_params = {}

# Analysis configuration
st.subheader("⚙️ Analysis Configuration")

col1, col2, col3 = st.columns(3)

with col1:
    grid_resolution = st.selectbox(
        "Grid Resolution",
        ["High (0.005°)", "Medium (0.01°)", "Low (0.02°)"],
        index=1,
        help="Higher resolution provides more detailed analysis but takes longer"
    )

with col2:
    search_radius = st.selectbox(
        "Search Radius", 
        ["City Core (0.2°)", "Extended (0.3°)", "Regional (0.5°)"],
        index=1,
        help="Area radius around Sulaimani center to analyze (2x enhanced coverage)"
    )

with col3:
    max_distance = st.slider(
        "Maximum Distance (km)",
        min_value=1.0,
        max_value=20.0,
        value=10.0,
        step=0.5,
        help="Maximum distance to consider for infrastructure scoring"
    )

# Parse configuration
resolution_map = {"High (0.005°)": 0.005, "Medium (0.01°)": 0.01, "Low (0.02°)": 0.02}
radius_map = {"City Core (0.2°)": 0.2, "Extended (0.3°)": 0.3, "Regional (0.5°)": 0.5}

grid_res = resolution_map[grid_resolution]
search_rad = radius_map[search_radius]

# Infrastructure types to query
INFRASTRUCTURE_TYPES = {
    "roads": {
        "query": '["highway"]',
        "name": "Roads & Highways",
        "weight": 0.3,
        "icon": "🛣️"
    },
    "hospitals": {
        "query": '["amenity"~"hospital|clinic|doctors"]',
        "name": "Healthcare Facilities",
        "weight": 0.25,
        "icon": "🏥"
    },
    "schools": {
        "query": '["amenity"~"school|university|college"]',
        "name": "Educational Institutions",
        "weight": 0.2,
        "icon": "🏫"
    },
    "services": {
        "query": '["amenity"~"police|fire_station|post_office|bank|pharmacy"]',
        "name": "Essential Services",
        "weight": 0.15,
        "icon": "🏢"
    },
    "transport": {
        "query": '["amenity"~"bus_station|taxi"]',
        "name": "Public Transport",
        "weight": 0.1,
        "icon": "🚌"
    }
}

# Data saving and loading functions
def save_infrastructure_data(infrastructure_df, params):
    """Save infrastructure analysis data to CSV file"""
    filename = f"infrastructure_data_{params['resolution']:.3f}_{params['radius']:.2f}_{params['max_dist']:.1f}.csv"
    filepath = os.path.join(DATA_DIR, filename)
    infrastructure_df.to_csv(filepath, index=False)
    return filepath

def load_infrastructure_data(params):
    """Load infrastructure analysis data from CSV file if exists"""
    filename = f"infrastructure_data_{params['resolution']:.3f}_{params['radius']:.2f}_{params['max_dist']:.1f}.csv"
    filepath = os.path.join(DATA_DIR, filename)
    
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            # Verify the DataFrame has the expected columns
            expected_cols = ['lat', 'lon', 'roads_distance', 'hospitals_distance', 'schools_distance', 
                           'services_distance', 'transport_distance', 'accessibility_score']
            if all(col in df.columns for col in expected_cols):
                return df
        except Exception as e:
            st.warning(f"Error loading saved data: {str(e)}")
    
    return None

def get_saved_infrastructure_datasets():
    """Get list of saved infrastructure datasets"""
    datasets = []
    if os.path.exists(DATA_DIR):
        for file in os.listdir(DATA_DIR):
            if file.startswith("infrastructure_data_") and file.endswith(".csv"):
                try:
                    parts = file.replace("infrastructure_data_", "").replace(".csv", "").split("_")
                    if len(parts) == 3:
                        resolution = float(parts[0])
                        radius = float(parts[1])
                        max_dist = float(parts[2])
                        datasets.append({
                            'filename': file,
                            'resolution': resolution,
                            'radius': radius,
                            'max_dist': max_dist,
                            'filepath': os.path.join(DATA_DIR, file)
                        })
                except:
                    continue
    return datasets

# Track current parameters
current_params = {
    'resolution': grid_res,
    'radius': search_rad, 
    'max_dist': max_distance
}

st.markdown("---")

# Show saved datasets section
st.subheader("💾 Saved Infrastructure Datasets")
saved_datasets = get_saved_infrastructure_datasets()

if saved_datasets:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        dataset_options = []
        for d in saved_datasets:
            try:
                file_size = os.path.getsize(d['filepath']) / 1024  # KB
                size_str = f"{file_size:.1f}KB" if file_size < 1024 else f"{file_size/1024:.1f}MB"
            except:
                size_str = "Unknown"
            
            dataset_options.append(f"Res: {d['resolution']:.3f}°, Radius: {d['radius']:.2f}°, Max Dist: {d['max_dist']:.1f}km ({size_str})")
        
        selected_idx = st.selectbox("Load Saved Dataset:", ["None"] + dataset_options, index=0)
    
    with col2:
        if st.button("🗑️ Clear All Saved Data", help="Delete all saved infrastructure datasets"):
            for dataset in saved_datasets:
                try:
                    os.remove(dataset['filepath'])
                except:
                    pass
            st.success("All saved datasets cleared!")
            st.rerun()
    
    if selected_idx != "None":
        dataset_idx = dataset_options.index(selected_idx)
        selected_dataset = saved_datasets[dataset_idx]
        
        if st.button("📂 Load Selected Dataset", type="primary"):
            loaded_df = pd.read_csv(selected_dataset['filepath'])
            st.session_state.infrastructure_df = loaded_df
            st.session_state.infrastructure_analysis_completed = True
            st.session_state.infrastructure_params = {
                'resolution': selected_dataset['resolution'],
                'radius': selected_dataset['radius'], 
                'max_dist': selected_dataset['max_dist']
            }
            st.success(f"✅ Loaded infrastructure dataset with {len(loaded_df)} points!")
            st.rerun()
else:
    st.info("No saved datasets found. Run an analysis to create your first dataset.")

st.markdown("---")

# Generate coordinate grid
@st.cache_data(ttl=3600)
def generate_coordinate_grid(center_lat, center_lon, radius, resolution):
    """Generate a grid of coordinates around Sulaimani"""
    lats = np.arange(center_lat - radius, center_lat + radius + resolution, resolution)
    lons = np.arange(center_lon - radius, center_lon + radius + resolution, resolution)
    
    coordinates = []
    for lat in lats:
        for lon in lons:
            coordinates.append({'lat': lat, 'lon': lon})
    
    return pd.DataFrame(coordinates)

# Overpass API query functions
@st.cache_data(ttl=3600)
def query_overpass_api(bbox, infrastructure_type):
    """Query Overpass API for specific infrastructure type"""
    south, west, north, east = bbox
    
    query = f"""
    [out:json][timeout:25];
    (
      node{INFRASTRUCTURE_TYPES[infrastructure_type]['query']}({south},{west},{north},{east});
      way{INFRASTRUCTURE_TYPES[infrastructure_type]['query']}({south},{west},{north},{east});
      relation{INFRASTRUCTURE_TYPES[infrastructure_type]['query']}({south},{west},{north},{east});
    );
    out geom;
    """
    
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    try:
        response = requests.post(overpass_url, data=query, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"Overpass API error for {infrastructure_type}: {response.status_code}")
            return None
    except Exception as e:
        st.warning(f"Error querying {infrastructure_type}: {str(e)}")
        return None

def extract_coordinates(osm_data):
    """Extract coordinates from OSM data"""
    coordinates = []
    
    if not osm_data or 'elements' not in osm_data:
        return coordinates
    
    for element in osm_data['elements']:
        if element['type'] == 'node' and 'lat' in element and 'lon' in element:
            coordinates.append((element['lat'], element['lon']))
        elif element['type'] == 'way' and 'geometry' in element:
            # Use the center of the way
            geom_coords = element['geometry']
            if geom_coords:
                center_lat = sum(point['lat'] for point in geom_coords) / len(geom_coords)
                center_lon = sum(point['lon'] for point in geom_coords) / len(geom_coords)
                coordinates.append((center_lat, center_lon))
    
    return coordinates

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on earth (in kilometers)"""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    return c * r

def calculate_min_distance_to_infrastructure(grid_point, infrastructure_coords):
    """Calculate minimum distance from grid point to any infrastructure point"""
    if not infrastructure_coords:
        return float('inf')  # No infrastructure found
    
    lat1, lon1 = grid_point
    min_distance = float('inf')
    
    for lat2, lon2 in infrastructure_coords:
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        min_distance = min(min_distance, distance)
    
    return min_distance

def normalize_distance_to_score(distance, max_dist):
    """Convert distance to accessibility score (0-100)"""
    if distance == float('inf'):
        return 0  # No infrastructure found
    
    # Normalize: closer = higher score
    if distance >= max_dist:
        return 0
    else:
        return 100 * (1 - distance / max_dist)

def display_infrastructure_results(infrastructure_df, max_dist):
    """Display comprehensive infrastructure accessibility results"""
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_accessibility = infrastructure_df['accessibility_score'].mean()
        st.metric("Average Accessibility", f"{avg_accessibility:.1f}/100")
    
    with col2:
        avg_road_dist = infrastructure_df['roads_distance'].mean()
        st.metric("Avg Distance to Roads", f"{avg_road_dist:.2f} km")
    
    with col3:
        avg_hospital_dist = infrastructure_df['hospitals_distance'].mean()
        st.metric("Avg Distance to Hospitals", f"{avg_hospital_dist:.2f} km")
    
    with col4:
        high_access_areas = (infrastructure_df['accessibility_score'] >= 70).mean() * 100
        st.metric("High Accessibility Areas", f"{high_access_areas:.1f}%")
    
    # Interactive map
    st.subheader("🗺️ Infrastructure Accessibility Map")
    
    # Create folium map
    m = folium.Map(
        location=SULAIMANI_CENTER,
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Add infrastructure accessibility heatmap
    from folium.plugins import HeatMap
    
    # Prepare heatmap data (lat, lon, accessibility_score)
    heat_data = [[row['lat'], row['lon'], row['accessibility_score']/100] 
                 for _, row in infrastructure_df.iterrows()]
    
    HeatMap(
        heat_data,
        radius=20,
        blur=15,
        max_zoom=13,
        gradient={0.2: 'red', 0.4: 'orange', 0.6: 'yellow', 0.8: 'lightgreen', 1.0: 'green'}
    ).add_to(m)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                top: 10px; right: 10px; width: 220px; height: 140px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p><b>Infrastructure Accessibility</b></p>
    <p><i class="fa fa-circle" style="color:green"></i> High Access (Well Connected)</p>
    <p><i class="fa fa-circle" style="color:yellow"></i> Medium Access</p>
    <p><i class="fa fa-circle" style="color:red"></i> Low Access (Remote)</p>
    <p><b>Max Distance:</b> {max_dist:.1f} km</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html.format(max_dist=max_dist)))
    
    folium.LayerControl().add_to(m)
    st_folium(m, width=1400, height=500)
    
    # Infrastructure analysis charts
    st.subheader("📊 Infrastructure Distance Analysis")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Distance Distribution by Infrastructure Type', 'Accessibility Score Distribution',
                       'Distance vs Accessibility Correlation', 'Infrastructure Weights Impact'),
        vertical_spacing=0.1
    )
    
    # 1. Distance distribution by infrastructure type
    infrastructure_cols = ['roads_distance', 'hospitals_distance', 'schools_distance', 'services_distance', 'transport_distance']
    infrastructure_names = ['Roads', 'Hospitals', 'Schools', 'Services', 'Transport']
    colors = ['blue', 'red', 'green', 'purple', 'orange']
    
    for i, (col, name, color) in enumerate(zip(infrastructure_cols, infrastructure_names, colors)):
        fig.add_trace(
            go.Box(y=infrastructure_df[col], name=name, marker_color=color),
            row=1, col=1
        )
    
    # 2. Accessibility score distribution
    fig.add_trace(
        go.Histogram(
            x=infrastructure_df['accessibility_score'],
            name='Accessibility Score',
            nbinsx=20,
            marker_color='lightblue'
        ),
        row=1, col=2
    )
    
    # 3. Distance vs Accessibility correlation
    fig.add_trace(
        go.Scatter(
            x=infrastructure_df['roads_distance'],
            y=infrastructure_df['accessibility_score'],
            mode='markers',
            name='Roads Impact',
            marker=dict(color='blue', size=4),
            text=[f"Roads: {dist:.2f}km<br>Score: {score:.1f}" 
                  for dist, score in zip(infrastructure_df['roads_distance'], infrastructure_df['accessibility_score'])],
            hovertemplate='%{text}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # 4. Infrastructure weights visualization
    weights = [INFRASTRUCTURE_TYPES[key]['weight'] for key in ['roads', 'hospitals', 'schools', 'services', 'transport']]
    fig.add_trace(
        go.Bar(
            x=infrastructure_names,
            y=weights,
            name='Weights',
            marker_color=['blue', 'red', 'green', 'purple', 'orange']
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=800, showlegend=True)
    fig.update_xaxes(title_text="Infrastructure Type", row=1, col=1)
    fig.update_yaxes(title_text="Distance (km)", row=1, col=1)
    fig.update_xaxes(title_text="Accessibility Score", row=1, col=2)
    fig.update_yaxes(title_text="Frequency", row=1, col=2)
    fig.update_xaxes(title_text="Distance to Roads (km)", row=2, col=1)
    fig.update_yaxes(title_text="Accessibility Score", row=2, col=1)
    fig.update_xaxes(title_text="Infrastructure Type", row=2, col=2)
    fig.update_yaxes(title_text="Weight", row=2, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("📋 Infrastructure Development Recommendations")
    
    # Identify areas with different accessibility levels
    high_access = infrastructure_df[infrastructure_df['accessibility_score'] >= 70]
    medium_access = infrastructure_df[
        (infrastructure_df['accessibility_score'] >= 40) & (infrastructure_df['accessibility_score'] < 70)
    ]
    low_access = infrastructure_df[infrastructure_df['accessibility_score'] < 40]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"**🟢 High Access Areas: {len(high_access)} points ({len(high_access)/len(infrastructure_df)*100:.1f}%)**")
        st.warning(f"**🟡 Medium Access Areas: {len(medium_access)} points ({len(medium_access)/len(infrastructure_df)*100:.1f}%)**")
        st.error(f"**🔴 Low Access Areas: {len(low_access)} points ({len(low_access)/len(infrastructure_df)*100:.1f}%)**")
        
        if len(high_access) > 0:
            best_area = high_access.loc[high_access['accessibility_score'].idxmax()]
            st.success(f"""
            **🏆 Best Connected Location:**
            - Coordinates: {best_area['lat']:.4f}°N, {best_area['lon']:.4f}°E
            - Accessibility Score: {best_area['accessibility_score']:.1f}/100
            - Roads: {best_area['roads_distance']:.2f}km
            - Hospitals: {best_area['hospitals_distance']:.2f}km
            - Schools: {best_area['schools_distance']:.2f}km
            """)
    
    with col2:
        st.markdown("""
        **🏗️ Infrastructure Development Priorities:**
        
        ✅ **Priority Development Zones (High Access):**
        - Well connected to existing infrastructure
        - Lower development costs
        - Immediate service availability
        
        ⚠️ **Secondary Development (Medium Access):**
        - Requires moderate infrastructure investment
        - Extend existing service networks
        - Phased development recommended
        
        ❌ **Infrastructure First (Low Access):**
        - Requires significant infrastructure investment
        - Build roads and services before housing
        - Long-term development planning needed
        
        **🎯 Infrastructure Gaps:**
        - Focus on areas >5km from hospitals
        - Improve road connectivity in remote areas
        - Add public transport to underserved zones
        """)
    
    # Data export
    st.subheader("💾 Export Infrastructure Analysis")
    
    export_data = infrastructure_df.copy()
    export_data.columns = [col.replace('_', ' ').title() for col in export_data.columns]
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = export_data.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV Data",
            data=csv_data,
            file_name=f"sulaimani_infrastructure_analysis_{len(export_data)}_points.csv",
            mime="text/csv"
        )
    
    with col2:
        st.info(f"""
        **📊 Analysis Summary:**
        - Analysis Points: {len(export_data):,}
        - Infrastructure Types: 5
        - Max Distance: {max_dist:.1f}km
        - Avg Accessibility: {infrastructure_df['accessibility_score'].mean():.1f}/100
        """)

# Check for parameter changes
params_changed = st.session_state.infrastructure_params != current_params

# Main analysis section
st.header("🔬 Infrastructure Accessibility Analysis")

if st.button("🔍 Analyze Infrastructure Accessibility", type="primary", help="Start comprehensive infrastructure accessibility analysis"):
    
    # Check if data already exists
    existing_data = load_infrastructure_data(current_params)
    if existing_data is not None:
        st.session_state.infrastructure_df = existing_data
        st.session_state.infrastructure_analysis_completed = True
        st.session_state.infrastructure_params = current_params
        st.success(f"✅ Loaded existing data with {len(existing_data)} points!")
        st.rerun()
    
    # Update parameters
    st.session_state.infrastructure_params = current_params
    
    with st.spinner("Analyzing infrastructure accessibility..."):
        try:
            # Step 1: Generate coordinate grid
            st.write("**Step 1:** Generating coordinate grid...")
            coordinates_df = generate_coordinate_grid(
                SULAIMANI_CENTER[0], SULAIMANI_CENTER[1], 
                search_rad, grid_res
            )
            st.success(f"✅ Generated {len(coordinates_df)} coordinate points")
            
            # Step 2: Query infrastructure data
            st.write("**Step 2:** Querying infrastructure data from OpenStreetMap...")
            
            # Define bounding box
            bbox = (
                SULAIMANI_CENTER[0] - search_rad,  # south
                SULAIMANI_CENTER[1] - search_rad,  # west
                SULAIMANI_CENTER[0] + search_rad,  # north
                SULAIMANI_CENTER[1] + search_rad   # east
            )
            
            # Query each infrastructure type
            infrastructure_data = {}
            progress_bar = st.progress(0)
            
            for i, infra_type in enumerate(INFRASTRUCTURE_TYPES.keys()):
                status_text = st.empty()
                status_text.text(f"Querying {INFRASTRUCTURE_TYPES[infra_type]['name']}...")
                
                osm_data = query_overpass_api(bbox, infra_type)
                infrastructure_coords = extract_coordinates(osm_data)
                infrastructure_data[infra_type] = infrastructure_coords
                
                st.success(f"✅ Found {len(infrastructure_coords)} {INFRASTRUCTURE_TYPES[infra_type]['name']} points")
                
                progress = (i + 1) / len(INFRASTRUCTURE_TYPES)
                progress_bar.progress(progress)
                
                # Rate limiting
                time.sleep(1)
            
            progress_bar.empty()
            
            # Step 3: Calculate distances and accessibility scores
            st.write("**Step 3:** Calculating accessibility scores...")
            
            # Calculate distances for each infrastructure type
            distance_columns = {}
            
            progress_bar = st.progress(0)
            total_calculations = len(coordinates_df) * len(INFRASTRUCTURE_TYPES)
            calculation_count = 0
            
            for infra_type in INFRASTRUCTURE_TYPES.keys():
                distances = []
                
                for _, row in coordinates_df.iterrows():
                    grid_point = (row['lat'], row['lon'])
                    min_dist = calculate_min_distance_to_infrastructure(
                        grid_point, infrastructure_data[infra_type]
                    )
                    distances.append(min_dist)
                    
                    calculation_count += 1
                    if calculation_count % 100 == 0:  # Update progress every 100 calculations
                        progress_bar.progress(calculation_count / total_calculations)
                
                distance_columns[f"{infra_type}_distance"] = distances
            
            # Add distance columns to DataFrame
            for col_name, distances in distance_columns.items():
                coordinates_df[col_name] = distances
            
            # Calculate weighted accessibility score
            accessibility_scores = []
            
            for _, row in coordinates_df.iterrows():
                weighted_score = 0
                
                for infra_type in INFRASTRUCTURE_TYPES.keys():
                    distance = row[f"{infra_type}_distance"]
                    score = normalize_distance_to_score(distance, max_distance)
                    weight = INFRASTRUCTURE_TYPES[infra_type]['weight']
                    weighted_score += score * weight
                
                accessibility_scores.append(weighted_score)
            
            coordinates_df['accessibility_score'] = accessibility_scores
            
            progress_bar.empty()
            
            # Store results in session state
            st.session_state.infrastructure_df = coordinates_df
            st.session_state.infrastructure_analysis_completed = True
            
            # Save data to file
            try:
                saved_path = save_infrastructure_data(coordinates_df, current_params)
                st.success(f"✅ Computed infrastructure accessibility for {len(coordinates_df)} points and saved to {saved_path}")
            except Exception as e:
                st.warning(f"Analysis completed but couldn't save data: {str(e)}")
                st.success(f"✅ Computed infrastructure accessibility for {len(coordinates_df)} points")
            
            # Results visualization
            st.header("📊 Infrastructure Accessibility Results")
            
            # Use the comprehensive display function
            display_infrastructure_results(coordinates_df, max_distance)
            
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            st.stop()

# Display results if analysis has been completed
if st.session_state.infrastructure_analysis_completed and st.session_state.infrastructure_df is not None:
    infrastructure_df = st.session_state.infrastructure_df
    
    # Check if parameters changed - show warning if so
    if st.session_state.infrastructure_params != current_params:
        st.warning("⚠️ Analysis parameters have changed. Click 'Analyze Infrastructure Accessibility' to update results.")
    
    st.header("📊 Infrastructure Accessibility Results (Cached)")
    
    # Use the display function for comprehensive results
    display_infrastructure_results(infrastructure_df, max_distance)
    
    # Clear analysis button
    if st.button("🔄 Clear Analysis", help="Clear cached results to run new analysis"):
        # Clear all session state
        for key in list(st.session_state.keys()):
            if key.startswith('infrastructure') or 'infrastructure' in key:
                del st.session_state[key]
        st.session_state.infrastructure_analysis_completed = False
        st.session_state.infrastructure_df = None
        st.session_state.infrastructure_params = {}
        st.rerun()

elif not st.session_state.infrastructure_analysis_completed:
    st.info("👆 Click the 'Analyze Infrastructure Accessibility' button to start the infrastructure accessibility analysis")

# Footer
st.markdown("---")
st.markdown("""
### 🔬 **Technical Methodology**

**Infrastructure Query**: Using Overpass API to query OpenStreetMap data
- `Roads`: highways, primary, secondary, tertiary roads
- `Healthcare`: hospitals, clinics, doctors, pharmacies  
- `Education`: schools, universities, colleges
- `Services`: police, fire stations, banks, post offices
- `Transport`: bus stations, taxi stands

**Distance Calculation**: Haversine formula for great circle distance
- `Distance = 2 × R × arcsin(√(sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)))`

**Accessibility Scoring**: Weighted inverse distance normalization (0-100 scale)
- **High Accessibility (70-100)**: Close to all major infrastructure
- **Medium Accessibility (40-69)**: Moderate distance to services
- **Low Accessibility (0-39)**: Remote from essential infrastructure

**Weighting System**: Roads (30%), Healthcare (25%), Education (20%), Services (15%), Transport (10%)

### 📚 **References**
- OpenStreetMap Overpass API: https://overpass-api.de/
- Infrastructure accessibility for sustainable urban planning
- Geospatial analysis for smart city development
""")