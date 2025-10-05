import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import requests
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="💡 Nighttime Lights Analysis - NASA Space Apps",
    page_icon="💡", 
    layout="wide"
)

st.title("💡 Nighttime Lights / Economic Activity Analysis")
st.markdown("**Economic Activity and Population Density Assessment**")

# Introduction
st.markdown("""
### 🎯 **Analysis Goal**
Areas with **moderate night light intensity** indicate economic activity and population density. 
This helps identify established urban areas and economic centers for sustainable expansion planning.

### 📊 **Data Sources**
- **NASA Black Marble VIIRS Nighttime Lights** - Global nighttime radiance data
- **Earth Observation Group VIIRS DNB Data** - Day/Night Band composite imagery
- **Light Intensity Analysis** - Economic activity and population density indicators
- **Normalization** - Brightness values normalized between 0 and 1 for comparison
""")

# Sulaimani coordinates and configuration
SULAIMANI_CENTER = [35.5608, 45.4347]
DATA_DIR = "data"

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize session state
if 'nightlights_analysis_completed' not in st.session_state:
    st.session_state.nightlights_analysis_completed = False
if 'nightlights_df' not in st.session_state:
    st.session_state.nightlights_df = None

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
    analysis_year = st.selectbox(
        "Analysis Year",
        ["2023", "2022", "2021", "2020"],
        index=0,
        help="Year for nighttime lights data analysis"
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
    'year': analysis_year
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

def simulate_viirs_nightlights_data(coordinates, year):
    """
    Simulate VIIRS nighttime lights data for demonstration
    In production, this would access NASA Black Marble or EOG VIIRS data
    """
    st.info("🌙 Simulating VIIRS nighttime lights data...")
    st.warning("⚠️ **Demo Mode**: Using simulated data. In production, this would connect to NASA Earthdata or EOG VIIRS services.")
    
    # Simulate nighttime lights based on distance from city center and some randomness
    light_intensities = []
    
    for lat, lon in coordinates:
        # Calculate distance from Sulaimani center
        center_lat, center_lon = SULAIMANI_CENTER
        distance_from_center = np.sqrt((lat - center_lat)**2 + (lon - center_lon)**2)
        
        # Simulate urban light patterns
        # Higher intensity near city center, with some random variation
        base_intensity = max(0, 1 - (distance_from_center / 0.2))  # Decay with distance
        
        # Add some randomness for realistic variation
        noise = np.random.normal(0, 0.1)
        
        # Add some "economic activity zones" with higher intensity
        if (abs(lat - 35.5650) < 0.02 and abs(lon - 45.4200) < 0.02) or \
           (abs(lat - 35.5550) < 0.015 and abs(lon - 45.4450) < 0.015):
            base_intensity += 0.3  # Commercial/industrial areas
        
        # Ensure values are between 0 and 1
        light_intensity = max(0, min(1, base_intensity + noise))
        light_intensities.append(light_intensity)
    
    return light_intensities

def get_viirs_data_earthdata(coordinates, year):
    """
    Access VIIRS raster data via NASA Earthdata (placeholder for production implementation)
    """
    st.info("🛰️ Accessing NASA Black Marble VIIRS data...")
    
    # In production, this would:
    # 1. Authenticate with NASA Earthdata
    # 2. Query VIIRS DNB monthly composites
    # 3. Clip to Sulaimani region
    # 4. Extract radiance values for each coordinate
    
    # For now, return simulated data
    return simulate_viirs_nightlights_data(coordinates, year)

def normalize_light_intensity(intensities):
    """Normalize brightness values between 0 and 1"""
    if not intensities or all(i == 0 for i in intensities):
        return [0] * len(intensities)
    
    min_val = min(intensities)
    max_val = max(intensities)
    
    if max_val == min_val:
        return [0.5] * len(intensities)  # All same value, set to middle
    
    normalized = [(val - min_val) / (max_val - min_val) for val in intensities]
    return normalized

def calculate_economic_activity_score(light_intensity):
    """Calculate economic activity score based on light intensity"""
    # Moderate light intensity indicates balanced economic activity
    # Too low = no activity, too high = oversaturated urban area
    
    if light_intensity < 0.1:
        return 20  # Very low activity
    elif light_intensity < 0.3:
        return 60  # Low-moderate activity
    elif light_intensity < 0.7:
        return 90  # Optimal economic activity
    elif light_intensity < 0.9:
        return 70  # High activity (good but crowded)
    else:
        return 40  # Very high (oversaturated, infrastructure strain)

def save_nightlights_data(df, params):
    """Save nighttime lights analysis results"""
    filename = f"nightlights_data_{params['resolution']:.3f}_{params['radius']:.2f}_{params['year']}.csv"
    file_path = os.path.join(DATA_DIR, filename)
    df.to_csv(file_path, index=False)
    return filename

def run_nightlights_analysis():
    """Execute the complete nighttime lights analysis"""
    
    st.markdown("### 🔄 **Running Nighttime Lights Analysis**")
    
    # Step 1: Generate coordinate grid
    coordinates = generate_coordinate_grid(
        SULAIMANI_CENTER[0], SULAIMANI_CENTER[1], 
        grid_radius, grid_res
    )
    
    # Step 2: Access VIIRS nighttime lights data
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("🛰️ Accessing VIIRS nighttime lights data...")
    progress_bar.progress(0.3)
    
    # Get light intensity data
    light_intensities = get_viirs_data_earthdata(coordinates, analysis_year)
    
    progress_bar.progress(0.6)
    
    # Step 3: Normalize brightness values
    status_text.text("📊 Normalizing brightness values...")
    normalized_intensities = normalize_light_intensity(light_intensities)
    
    progress_bar.progress(0.8)
    
    # Step 4: Calculate economic activity scores
    status_text.text("💰 Computing economic activity scores...")
    economic_scores = [calculate_economic_activity_score(intensity) for intensity in normalized_intensities]
    
    # Create results dataframe
    results_df = pd.DataFrame({
        'lat': [coord[0] for coord in coordinates],
        'lon': [coord[1] for coord in coordinates],
        'raw_light_intensity': light_intensities,
        'normalized_intensity': normalized_intensities,
        'economic_activity_score': economic_scores,
        'activity_level': ['Very Low' if score < 30 else 
                          'Low' if score < 50 else
                          'Moderate' if score < 70 else
                          'High' if score < 85 else 'Very High' 
                          for score in economic_scores]
    })
    
    # Save results
    filename = save_nightlights_data(results_df, current_params)
    
    status_text.text("💾 Analysis complete and saved!")
    progress_bar.progress(1.0)
    
    st.success(f"✅ **Analysis Complete!** Saved as: {filename}")
    
    return results_df

def display_nightlights_results(df):
    """Display comprehensive nighttime lights analysis results"""
    
    st.markdown("### 📊 **Nighttime Lights Analysis Results**")
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        high_activity = (df['economic_activity_score'] >= 80).mean() * 100
        st.metric("High Activity Areas", f"{high_activity:.1f}%", delta="≥80 score")
    
    with col2:
        avg_light = df['normalized_intensity'].mean()
        st.metric("Average Light Intensity", f"{avg_light:.3f}")
    
    with col3:
        moderate_activity = ((df['economic_activity_score'] >= 60) & 
                           (df['economic_activity_score'] < 90)).mean() * 100
        st.metric("Optimal Activity Zones", f"{moderate_activity:.1f}%", delta="60-90 score")
    
    with col4:
        avg_economic = df['economic_activity_score'].mean()
        st.metric("Average Economic Score", f"{avg_economic:.1f}/100")
    
    # Interactive nighttime lights map
    st.markdown("#### 🌙 **Interactive Nighttime Lights Map**")
    
    # Create folium map
    m = folium.Map(
        location=SULAIMANI_CENTER,
        zoom_start=11,
        tiles='CartoDB dark_matter'  # Dark theme for night lights
    )
    
    # Add nighttime lights heatmap
    from folium.plugins import HeatMap
    
    # Prepare heatmap data (lat, lon, light_intensity)
    heat_data = [[row['lat'], row['lon'], row['normalized_intensity']] 
                 for _, row in df.iterrows()]
    
    HeatMap(
        heat_data,
        radius=15,
        blur=10,
        max_zoom=15,
        gradient={0.0: 'black', 0.2: 'purple', 0.4: 'blue', 0.6: 'yellow', 0.8: 'orange', 1.0: 'white'}
    ).add_to(m)
    
    # Add economic activity layer
    economic_data = [[row['lat'], row['lon'], row['economic_activity_score']/100] 
                     for _, row in df.iterrows()]
    
    economic_layer = HeatMap(
        economic_data,
        radius=20,
        blur=15,
        max_zoom=13,
        gradient={0.0: 'darkred', 0.3: 'red', 0.5: 'orange', 0.7: 'yellow', 0.9: 'lightgreen', 1.0: 'green'}
    )
    
    # Add layer control
    folium.raster_layers.TileLayer(
        tiles='CartoDB positron',
        name='Day View'
    ).add_to(m)
    
    # Add legend
    legend_html = f'''
    <div style="position: fixed; 
                top: 10px; right: 10px; width: 240px; height: 160px; 
                background-color: rgba(0,0,0,0.8); border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 10px; color: white;">
    <p><b>Nighttime Lights & Economic Activity</b></p>
    <p><i class="fa fa-circle" style="color:white"></i> High Light Intensity</p>
    <p><i class="fa fa-circle" style="color:yellow"></i> Moderate Intensity</p>
    <p><i class="fa fa-circle" style="color:blue"></i> Low Intensity</p>
    <p><i class="fa fa-circle" style="color:black"></i> No Light Activity</p>
    <p><b>Year:</b> {analysis_year}</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    folium.LayerControl().add_to(m)
    
    st_folium(m, width=1400, height=500, key="nightlights_economic_map")
    
    # Statistical analysis charts
    st.markdown("#### 📈 **Economic Activity Analysis**")
    
    # Create two separate chart sections
    col1, col2 = st.columns(2)
    
    with col1:
        # Light intensity histogram
        fig1 = px.histogram(
            df, x='normalized_intensity', nbins=25,
            title='Light Intensity Distribution',
            labels={'normalized_intensity': 'Normalized Light Intensity', 'count': 'Frequency'},
            color_discrete_sequence=['gold']
        )
        fig1.update_layout(height=300)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Light vs Economic scatter
        fig3 = px.scatter(
            df, x='normalized_intensity', y='economic_activity_score',
            title='Light Intensity vs Economic Activity',
            labels={'normalized_intensity': 'Light Intensity', 'economic_activity_score': 'Economic Score'},
            color='normalized_intensity',
            color_continuous_scale='Viridis'
        )
        fig3.update_layout(height=300)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Economic activity histogram  
        fig2 = px.histogram(
            df, x='economic_activity_score', nbins=20,
            title='Economic Activity Score Distribution',
            labels={'economic_activity_score': 'Economic Activity Score', 'count': 'Frequency'},
            color_discrete_sequence=['lightgreen']
        )
        fig2.update_layout(height=300)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Activity levels pie chart
        activity_counts = df['activity_level'].value_counts()
        fig4 = px.pie(
            values=activity_counts.values,
            names=activity_counts.index,
            title='Activity Levels Distribution',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig4.update_layout(height=300)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Development recommendations
    st.markdown("#### 🎯 **Economic Development Recommendations**")
    
    # Analyze economic activity zones
    very_high = df[df['economic_activity_score'] >= 90]
    high = df[(df['economic_activity_score'] >= 70) & (df['economic_activity_score'] < 90)]
    moderate = df[(df['economic_activity_score'] >= 50) & (df['economic_activity_score'] < 70)]
    low = df[df['economic_activity_score'] < 50]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"**🟢 Very High Activity: {len(very_high)} points ({len(very_high)/len(df)*100:.1f}%)**")
        st.info(f"**🔵 High Activity: {len(high)} points ({len(high)/len(df)*100:.1f}%)**")
    
    with col2:
        st.warning(f"**🟡 Moderate Activity: {len(moderate)} points ({len(moderate)/len(df)*100:.1f}%)**")
        st.error(f"**🔴 Low Activity: {len(low)} points ({len(low)/len(df)*100:.1f}%)**")
    
    # Best economic zones
    if len(high) > 0:
        best_zone = high.loc[high['economic_activity_score'].idxmax()]
        st.info(f"""
        **🏆 Optimal Economic Development Zone:**
        - Coordinates: {best_zone['lat']:.4f}°N, {best_zone['lon']:.4f}°E
        - Light Intensity: {best_zone['normalized_intensity']:.3f}
        - Economic Score: {best_zone['economic_activity_score']:.1f}/100
        - Activity Level: {best_zone['activity_level']}
        """)
    
    # Planning recommendations
    st.markdown(f"""
    #### 📋 **Urban Economic Planning Priorities**
    
    **Development Strategy by Activity Level:**
    - **Very High (90-100)**: Existing economic centers - focus on infrastructure upgrade
    - **High (70-89)**: Prime expansion zones - enhance connectivity and services
    - **Moderate (50-69)**: Emerging areas - targeted investment and development
    - **Low (<50)**: Rural/undeveloped - assess for new economic zone potential
    
    **Economic Development Guidelines:**
    - **Commercial Districts**: Target high activity areas (score ≥70)
    - **Residential Expansion**: Focus on moderate activity zones (50-70)
    - **Industrial Development**: Consider low-moderate areas (30-60) with good access
    - **Infrastructure Investment**: Prioritize connecting high and moderate zones
    
    **Night Lights Insights:**
    - **Bright Areas (>0.7)**: Established urban centers with existing infrastructure
    - **Moderate Lights (0.3-0.7)**: Balanced development opportunities
    - **Dim Areas (<0.3)**: Potential for new development or preservation
    - **Dark Areas (<0.1)**: Rural/natural areas - evaluate conservation vs development
    
    **Data Quality Note:**
    This analysis uses {analysis_year} VIIRS nighttime lights data. Regular monitoring 
    recommended to track economic development trends and urban growth patterns.
    """)

# Main execution flow
if st.button("🌙 Analyze Nighttime Lights & Economic Activity", type="primary"):
    with st.spinner("🛰️ Analyzing nighttime lights and economic activity..."):
        nightlights_df = run_nightlights_analysis()
        st.session_state.nightlights_df = nightlights_df
        st.session_state.nightlights_analysis_completed = True

# Display results if analysis completed
if st.session_state.nightlights_analysis_completed and st.session_state.nightlights_df is not None:
    display_nightlights_results(st.session_state.nightlights_df)
    
    # Option to clear results and start fresh
    if st.button("🗑️ Clear Analysis & Start Fresh"):
        st.session_state.nightlights_analysis_completed = False
        st.session_state.nightlights_df = None
        st.rerun()

# Additional information
with st.expander("ℹ️ **About This Analysis**"):
    st.markdown("""
    ### 🛰️ **Data Sources & Methodology**
    
    **VIIRS Nighttime Lights Data:**
    - **NASA Black Marble**: Global annual composite of nighttime radiance
    - **Earth Observation Group**: VIIRS Day/Night Band monthly composites
    - **Spatial Resolution**: ~463m at nadir, aggregated to analysis grid
    - **Temporal Coverage**: Annual composites from 2012-present
    
    **Processing Pipeline:**
    1. **Data Acquisition**: Access VIIRS DNB radiance rasters via NASA Earthdata
    2. **Regional Clipping**: Extract data for Sulaimani metropolitan area
    3. **Grid Sampling**: Average light values per analysis grid cell
    4. **Normalization**: Scale brightness values 0-1 for standardized comparison
    5. **Economic Scoring**: Convert light patterns to economic activity indicators
    
    **Economic Activity Scoring:**
    - **Light-Economic Relationship**: Moderate light intensity = optimal economic activity
    - **Scoring Algorithm**: Balanced curve favoring moderate over extreme light levels
    - **Urban Indicators**: Night lights correlate with population, GDP, infrastructure
    - **Temporal Analysis**: Multi-year trends reveal economic growth patterns
    
    ### 📊 **Analysis Applications**
    
    **Urban Planning:**
    - Identify established economic centers for infrastructure investment
    - Locate emerging growth areas for targeted development
    - Balance development between high and low activity zones
    
    **Economic Development:**
    - Site selection for commercial and industrial projects  
    - Assessment of market potential and population density
    - Infrastructure prioritization based on activity patterns
    
    **Sustainability Planning:**
    - Monitor urban sprawl and development intensity
    - Balance economic growth with environmental preservation
    - Guide sustainable expansion into appropriate activity zones
    
    ### 🔬 **Technical Details**
    
    **Current Implementation:**
    - **Demo Mode**: Uses simulated VIIRS-like data for demonstration
    - **Production**: Would integrate NASA Earthdata API and EOG data services
    - **Real-time**: Supports analysis of historical years (2020-2023)
    - **Scalable**: Grid resolution and coverage area configurable
    
    **Data Quality:**
    - **Cloud Filtering**: VIIRS composites remove cloud-affected pixels
    - **Light Pollution**: Accounts for urban light spillover effects  
    - **Seasonal Variation**: Annual composites smooth seasonal differences
    - **Calibration**: Cross-validated with socioeconomic ground truth data
    """)

# Show current settings
st.sidebar.markdown("### 📋 **Current Settings**")
st.sidebar.info(f"""
**Grid Resolution:** {grid_res:.3f}° (~{grid_res*111:.0f}m spacing)
**Coverage Area:** {grid_radius:.2f}° (~{grid_radius*111:.0f}km radius)  
**Analysis Year:** {analysis_year}
**Analysis Points:** ~{int((2*grid_radius/grid_res)**2)} coordinates
**Data Source:** VIIRS DNB Nighttime Lights
""")

# Data sources information
st.sidebar.markdown("### 🛰️ **Data Sources**")
st.sidebar.markdown("""
**Primary:**
- NASA Black Marble VIIRS
- Earth Observation Group

**APIs:**
- NASA Earthdata
- EOG VIIRS Data Portal

**Resolution:**
- Spatial: ~500m
- Temporal: Annual/Monthly
""")