import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import requests
import time
from math import sqrt, atan2, degrees
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Page configuration
st.set_page_config(
    page_title="🗻 Topography Analysis - NASA Space Apps",
    page_icon="🗻", 
    layout="wide"
)

st.title("🗻 Topography & Slope Analysis")
st.markdown("**Terrain Suitability for Sustainable Urban Expansion**")

# Introduction
st.markdown("""
### 🎯 **Analysis Goal**
Areas with **gentle slopes** are more suitable for expansion. Steep terrain increases construction costs, 
infrastructure challenges, and environmental risks.

### 📊 **Data Sources**
- **Open-Meteo Elevation API** - High-resolution digital elevation model
- **OpenTopoData API** - Global terrain data with SRTM coverage  
- **Slope Calculation** - Mathematical gradient analysis between neighboring points
- **Normalization** - Gentler slopes = higher suitability scores
""")

# Sulaimani coordinates and configuration
SULAIMANI_CENTER = [35.5608, 45.4347]
DATA_DIR = "data"

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize session state
if 'topography_analysis_completed' not in st.session_state:
    st.session_state.topography_analysis_completed = False
if 'topography_df' not in st.session_state:
    st.session_state.topography_df = None

# Configuration section
st.markdown("### ⚙️ **Analysis Configuration**")
col1, col2, col3 = st.columns(3)

with col1:
    grid_resolution = st.selectbox(
        "Grid Resolution", 
        ["High (0.005°)", "Medium (0.01°)", "Low (0.02°)"],
        index=1,
        help="Higher resolution = more detailed analysis but slower processing"
    )

with col2:
    coverage_area = st.selectbox(
        "Coverage Area", 
        ["City Core (0.1°)", "Extended (0.15°)", "Regional (0.25°)"],
        index=1,
        help="Area radius around Sulaimani center"
    )

with col3:
    max_slope = st.slider(
        "Max Acceptable Slope (%)",
        min_value=3,
        max_value=20,
        value=8,
        step=1,
        help="Maximum slope percentage for development suitability"
    )

# Parse configuration  
resolution_map = {"High (0.005°)": 0.005, "Medium (0.01°)": 0.01, "Low (0.02°)": 0.02}
coverage_map = {"City Core (0.1°)": 0.1, "Extended (0.15°)": 0.15, "Regional (0.25°)": 0.25}

grid_res = resolution_map[grid_resolution]
grid_radius = coverage_map[coverage_area]

# Current analysis parameters
current_params = {
    'resolution': grid_res, 
    'radius': grid_radius, 
    'max_slope': max_slope
}

def generate_coordinate_grid(center_lat, center_lon, radius, resolution):
    """Generate a latitude-longitude grid covering Sulaimani city"""
    st.info(f"📐 Generating coordinate grid: {resolution:.3f}° resolution over {radius:.2f}° radius")
    
    # Generate coordinate arrays
    lats = np.arange(center_lat - radius, center_lat + radius + resolution, resolution)
    lons = np.arange(center_lon - radius, center_lon + radius + resolution, resolution)
    
    # Create grid coordinates
    coordinates = []
    for lat in lats:
        for lon in lons:
            coordinates.append([lat, lon])
    
    st.success(f"✅ Generated {len(coordinates)} coordinate points")
    return coordinates

def get_elevation_openmeteo(coordinates_batch):
    """Fetch elevation data from Open-Meteo Elevation API"""
    try:
        latitudes = [coord[0] for coord in coordinates_batch]
        longitudes = [coord[1] for coord in coordinates_batch]
        
        params = {
            'latitude': latitudes,
            'longitude': longitudes
        }
        
        response = requests.get(
            "https://api.open-meteo.com/v1/elevation",
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('elevation', [0] * len(coordinates_batch))
        return [0] * len(coordinates_batch)
    except Exception as e:
        st.warning(f"Open-Meteo API error: {e}")
        return [0] * len(coordinates_batch)

def get_elevation_opentopo(coordinates_batch):
    """Fetch elevation data from OpenTopoData API"""
    try:
        # Format coordinates for API
        locations = "|".join([f"{lat},{lon}" for lat, lon in coordinates_batch])
        
        url = f"https://api.opentopodata.org/v1/srtm90m?locations={locations}"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                elevations = []
                for result in data['results']:
                    elevation = result['elevation']
                    elevations.append(elevation if elevation is not None else 0)
                return elevations
        return [0] * len(coordinates_batch)
    except Exception as e:
        st.warning(f"OpenTopoData API error: {e}")
        return [0] * len(coordinates_batch)

def compute_slope_from_neighbors(elevations, coordinates, resolution):
    """Compute slope as difference between neighboring points"""
    slopes = []
    
    # Convert resolution degrees to approximate meters
    meters_per_degree = 111320  # approximate meters per degree at equator
    grid_spacing = resolution * meters_per_degree
    
    for i in range(len(elevations)):
        current_lat, current_lon = coordinates[i]
        current_elevation = elevations[i]
        
        # Find neighboring points within grid resolution
        neighbors = []
        for j in range(len(coordinates)):
            if i == j:
                continue
                
            neighbor_lat, neighbor_lon = coordinates[j]
            neighbor_elevation = elevations[j]
            
            # Check if point is a direct neighbor (within 1.5 * resolution)
            lat_diff = abs(current_lat - neighbor_lat)
            lon_diff = abs(current_lon - neighbor_lon)
            
            if lat_diff <= resolution * 1.5 and lon_diff <= resolution * 1.5:
                # Calculate distance between points
                distance = sqrt((lat_diff * meters_per_degree)**2 + (lon_diff * meters_per_degree)**2)
                if distance > 0:
                    elevation_diff = abs(current_elevation - neighbor_elevation)
                    slope_percent = (elevation_diff / distance) * 100
                    neighbors.append(slope_percent)
        
        # Use maximum slope from all neighbors (worst case scenario)
        if neighbors:
            slope = max(neighbors)
            slopes.append(min(slope, 100))  # Cap at 100%
        else:
            slopes.append(0)
    
    return slopes

def normalize_slope_to_suitability(slopes, max_acceptable_slope):
    """Normalize slope values - gentler slopes get higher suitability scores"""
    suitability_scores = []
    
    for slope in slopes:
        if slope <= max_acceptable_slope:
            # Linear normalization: 0% slope = 100 suitability, max_slope = 0 suitability
            suitability = 100 * (1 - (slope / max_acceptable_slope))
        else:
            # Slopes above threshold get negative suitability
            suitability = 0
        
        suitability_scores.append(max(0, min(100, suitability)))
    
    return suitability_scores

def save_topography_data(df, params):
    """Save topography analysis results"""
    filename = f"topography_data_{params['resolution']:.3f}_{params['radius']:.2f}_{params['max_slope']:.1f}.csv"
    file_path = os.path.join(DATA_DIR, filename)
    df.to_csv(file_path, index=False)
    return filename

def run_topography_analysis():
    """Execute the complete topography/slope analysis"""
    
    st.markdown("### 🔄 **Running Topography Analysis**")
    
    # Step 1: Generate coordinate grid
    coordinates = generate_coordinate_grid(
        SULAIMANI_CENTER[0], SULAIMANI_CENTER[1], 
        grid_radius, grid_res
    )
    
    # Step 2: Fetch elevation data
    batch_size = 50  # Smaller batches for API limits
    all_elevations = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_batches = len(coordinates) // batch_size + (1 if len(coordinates) % batch_size != 0 else 0)
    
    for i in range(0, len(coordinates), batch_size):
        batch = coordinates[i:i + batch_size]
        batch_num = i // batch_size + 1
        
        status_text.text(f"📡 Fetching elevation data - Batch {batch_num}/{total_batches}")
        
        # Try Open-Meteo first, fallback to OpenTopoData
        elevations = get_elevation_openmeteo(batch)
        
        # If Open-Meteo returns all zeros, try OpenTopoData
        if all(e == 0 for e in elevations):
            time.sleep(1)  # Rate limiting
            elevations = get_elevation_opentopo(batch)
        
        all_elevations.extend(elevations)
        
        progress = min((i + batch_size) / len(coordinates), 1.0)
        progress_bar.progress(progress)
        
        # Rate limiting between API calls
        time.sleep(0.5)
    
    # Step 3: Compute slopes
    status_text.text("📊 Computing slopes from neighboring points...")
    slopes = compute_slope_from_neighbors(all_elevations, coordinates, grid_res)
    
    # Step 4: Normalize slopes to suitability scores
    status_text.text("🎯 Normalizing slopes to suitability scores...")
    suitability_scores = normalize_slope_to_suitability(slopes, max_slope)
    
    # Create results dataframe
    results_df = pd.DataFrame({
        'lat': [coord[0] for coord in coordinates],
        'lon': [coord[1] for coord in coordinates],
        'elevation': all_elevations,
        'slope_percent': slopes,
        'suitability_score': suitability_scores,
        'suitable': [score >= 50 for score in suitability_scores]  # 50+ is suitable
    })
    
    # Save results
    filename = save_topography_data(results_df, current_params)
    
    status_text.text("💾 Analysis complete and saved!")
    progress_bar.progress(1.0)
    
    st.success(f"✅ **Analysis Complete!** Saved as: {filename}")
    
    return results_df

def display_topography_results(df):
    """Display comprehensive topography analysis results"""
    
    st.markdown("### 📊 **Topography Analysis Results**")
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        highly_suitable = (df['suitability_score'] >= 80).mean() * 100
        st.metric("Highly Suitable Areas", f"{highly_suitable:.1f}%", delta="≥80 score")
    
    with col2:
        avg_elevation = df['elevation'].mean()
        st.metric("Average Elevation", f"{avg_elevation:.0f}m")
    
    with col3:
        avg_slope = df['slope_percent'].mean()
        st.metric("Average Slope", f"{avg_slope:.1f}%")
    
    with col4:
        avg_suitability = df['suitability_score'].mean()
        st.metric("Average Suitability", f"{avg_suitability:.1f}/100")
    
    # Interactive suitability map
    st.markdown("#### 🗺️ **Interactive Topography Suitability Map**")
    
    # Create folium map
    m = folium.Map(
        location=SULAIMANI_CENTER,
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Add topography suitability heatmap using same style as infrastructure
    from folium.plugins import HeatMap
    
    # Prepare heatmap data (lat, lon, suitability_score normalized 0-1)
    heat_data = [[row['lat'], row['lon'], row['suitability_score']/100] 
                 for _, row in df.iterrows()]
    
    HeatMap(
        heat_data,
        radius=20,
        blur=15,
        max_zoom=13,
        gradient={0.0: 'darkred', 0.2: 'red', 0.4: 'orange', 0.6: 'yellow', 0.8: 'lightgreen', 1.0: 'green'}
    ).add_to(m)
    
    # Add legend matching infrastructure style
    legend_html = f'''
    <div style="position: fixed; 
                top: 10px; right: 10px; width: 220px; height: 140px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p><b>Topography Suitability</b></p>
    <p><i class="fa fa-circle" style="color:green"></i> Highly Suitable (Gentle Slopes)</p>
    <p><i class="fa fa-circle" style="color:yellow"></i> Moderately Suitable</p>
    <p><i class="fa fa-circle" style="color:red"></i> Low Suitability (Steep)</p>
    <p><b>Max Slope:</b> {max_slope}%</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    st_folium(m, width=1400, height=500, key="topography_suitability_heatmap")
    
    # Statistical analysis charts
    st.markdown("#### 📈 **Statistical Analysis**")
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Elevation Distribution', 'Slope Distribution', 
                       'Suitability Score Distribution', 'Elevation vs Slope vs Suitability'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Elevation histogram
    fig.add_trace(
        go.Histogram(x=df['elevation'], name='Elevation (m)', nbinsx=30, marker_color='skyblue'),
        row=1, col=1
    )
    
    # Slope histogram  
    fig.add_trace(
        go.Histogram(x=df['slope_percent'], name='Slope %', nbinsx=30, marker_color='lightcoral'),
        row=1, col=2
    )
    
    # Suitability score histogram
    fig.add_trace(
        go.Histogram(x=df['suitability_score'], name='Suitability Score', nbinsx=20, marker_color='lightgreen'),
        row=2, col=1
    )
    
    # 3D scatter: Elevation vs Slope colored by Suitability
    fig.add_trace(
        go.Scatter(
            x=df['elevation'], 
            y=df['slope_percent'],
            mode='markers',
            marker=dict(
                color=df['suitability_score'],
                colorscale='RdYlGn',
                size=6,
                colorbar=dict(title="Suitability Score"),
                opacity=0.7
            ),
            name='Elevation vs Slope'
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=True, title_text="Comprehensive Topography Analysis")
    fig.update_xaxes(title_text="Elevation (m)", row=1, col=1)
    fig.update_xaxes(title_text="Slope (%)", row=1, col=2)
    fig.update_xaxes(title_text="Suitability Score", row=2, col=1)
    fig.update_xaxes(title_text="Elevation (m)", row=2, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=2)
    fig.update_yaxes(title_text="Count", row=2, col=1)
    fig.update_yaxes(title_text="Slope (%)", row=2, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Development recommendations
    st.markdown("#### 🎯 **Development Recommendations**")
    
    # Analyze suitability categories
    highly_suitable = df[df['suitability_score'] >= 80]
    moderately_suitable = df[(df['suitability_score'] >= 60) & (df['suitability_score'] < 80)]
    low_suitable = df[(df['suitability_score'] >= 40) & (df['suitability_score'] < 60)]
    unsuitable = df[df['suitability_score'] < 40]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"**🟢 Highly Suitable: {len(highly_suitable)} points ({len(highly_suitable)/len(df)*100:.1f}%)**")
        st.warning(f"**🟡 Moderately Suitable: {len(moderately_suitable)} points ({len(moderately_suitable)/len(df)*100:.1f}%)**")
    
    with col2:
        st.info(f"**🔵 Low Suitability: {len(low_suitable)} points ({len(low_suitable)/len(df)*100:.1f}%)**")
        st.error(f"**🔴 Unsuitable: {len(unsuitable)} points ({len(unsuitable)/len(df)*100:.1f}%)**")
    
    # Best development zone
    if len(highly_suitable) > 0:
        best_zone = highly_suitable.loc[highly_suitable['suitability_score'].idxmax()]
        st.info(f"""
        **🏆 Optimal Development Zone:**
        - Coordinates: {best_zone['lat']:.4f}°N, {best_zone['lon']:.4f}°E
        - Elevation: {best_zone['elevation']:.0f}m
        - Slope: {best_zone['slope_percent']:.1f}%
        - Suitability Score: {best_zone['suitability_score']:.1f}/100
        """)
    
    # Planning recommendations
    st.markdown(f"""
    #### 📋 **Urban Planning Priorities**
    
    **Prioritized Development Areas:**
    - **High Priority**: Suitability score ≥80 (gentle slopes ≤{max_slope*0.2:.1f}%)
    - **Medium Priority**: Suitability score 60-79 (moderate slopes ≤{max_slope*0.6:.1f}%)
    - **Low Priority**: Suitability score 40-59 (steeper slopes ≤{max_slope:.1f}%)
    - **Avoid**: Suitability score <40 (slopes >{max_slope:.1f}%)
    
    **Infrastructure Guidelines:**
    - **Roads**: Prioritize areas with suitability score ≥60
    - **Residential**: Focus on suitability score ≥70 areas
    - **Commercial**: Can utilize suitability score ≥50 areas
    - **Industrial**: Minimum suitability score ≥40 required
    
    **Environmental Considerations:**
    - Preserve areas with slopes >{max_slope}% for natural drainage
    - Implement erosion control in moderate slope areas
    - Consider terracing for slopes between {max_slope*0.6:.1f}%-{max_slope:.1f}%
    """)

# Main execution flow
if st.button("🔍 Analyze Topography & Terrain", type="primary"):
    with st.spinner("🗻 Analyzing topography and slope suitability..."):
        topography_df = run_topography_analysis()
        st.session_state.topography_df = topography_df
        st.session_state.topography_analysis_completed = True

# Display results if analysis completed
if st.session_state.topography_analysis_completed and st.session_state.topography_df is not None:
    display_topography_results(st.session_state.topography_df)
    
    # Option to clear results and start fresh
    if st.button("🗑️ Clear Analysis & Start Fresh"):
        st.session_state.topography_analysis_completed = False
        st.session_state.topography_df = None
        st.rerun()

# Additional information
with st.expander("ℹ️ **About This Analysis**"):
    st.markdown("""
    ### 🔬 **Methodology**
    
    **1. Grid Generation:**
    - Generate latitude-longitude grid covering Sulaimani city
    - Configurable resolution: 0.005° to 0.02° spacing
    - Coverage areas: 0.1° to 0.25° radius from city center
    
    **2. Elevation Data:**
    - **Primary**: Open-Meteo Elevation API (global SRTM-based model)
    - **Fallback**: OpenTopoData SRTM90 (90m resolution satellite data)
    - Automatic failover between APIs for reliability
    
    **3. Slope Calculation:**
    - Compute slope from elevation differences between neighboring grid points
    - Use maximum slope from all neighbors (worst-case scenario)
    - Convert elevation difference and distance to percentage slope
    
    **4. Suitability Normalization:**
    - **Gentle slopes (0%)** = 100 suitability score
    - **Maximum acceptable slope** = 0 suitability score  
    - **Linear normalization**: Score = 100 × (1 - slope/max_slope)
    - **Above threshold** = 0 suitability (unsuitable for development)
    
    ### 📊 **Suitability Categories**
    - **Highly Suitable (80-100)**: Ideal for all development types
    - **Moderately Suitable (60-79)**: Good for most development with planning
    - **Low Suitability (40-59)**: Requires special engineering considerations  
    - **Unsuitable (0-39)**: Avoid development, preserve for natural uses
    
    ### 🌍 **Geographic Coverage**
    Current analysis covers Sulaimani city with configurable grid resolution and radius for detailed topographic assessment.
    """)

# Show current settings
st.sidebar.markdown("### 📋 **Current Settings**")
st.sidebar.info(f"""
**Grid Resolution:** {grid_res:.3f}° (~{grid_res*111:.0f}m spacing)
**Coverage Area:** {grid_radius:.2f}° (~{grid_radius*111:.0f}km radius)  
**Max Slope:** {max_slope}%
**Analysis Points:** ~{int((2*grid_radius/grid_res)**2)} coordinates
""")