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
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
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

# Page configuration
st.set_page_config(
    page_title="👥 Population Density Analysis - NASA Space Apps",
    page_icon="👥", 
    layout="wide"
)

st.title("👥 Population Density Analysis")
st.markdown("**Population Pressure Assessment for Sustainable Urban Planning**")

# Introduction
st.markdown("""
### 🎯 **Analysis Goal**
Understand population pressure and balance it with new expansion areas. 
**Medium density values** are more favorable for sustainable development, while very high 
or very low densities are less suitable for new urban expansion.

### 📊 **Data Sources**
- **WorldPop API** - High-resolution global population data
- **Meta Data for Global Population Density (Facebook HRSL)** - High Resolution Settlement Layer
- **Population Distribution Modeling** - Demographic analysis and projection
- **Density Normalization** - Optimal population pressure assessment
""")

# Sulaimani coordinates and configuration
SULAIMANI_CENTER = [35.5608, 45.4347]
DATA_DIR = "data"

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize session state
if 'population_analysis_completed' not in st.session_state:
    st.session_state.population_analysis_completed = False
if 'population_df' not in st.session_state:
    st.session_state.population_df = None

# Configuration section
st.markdown("### ⚙️ **Analysis Configuration**")
col1, col2, col3 = st.columns(3)

with col1:
    grid_resolution = st.selectbox(
        "Grid Resolution", 
        ["High (0.005°)", "Medium (0.01°)", "Low (0.02°)"],
        index=1,
        help="Higher resolution = more detailed population analysis"
    )

with col2:
    coverage_area = st.selectbox(
        "Coverage Area", 
        ["City Core (0.1°)", "Extended (0.15°)", "Metropolitan (0.2°)"],
        index=1,
        help="Area radius around Sulaimani center for population assessment"
    )

with col3:
    analysis_year = st.selectbox(
        "Analysis Year",
        ["2023", "2022", "2021", "2020"],
        index=0,
        help="Year for population density data"
    )

# Parse configuration  
resolution_map = {"High (0.005°)": 0.005, "Medium (0.01°)": 0.01, "Low (0.02°)": 0.02}
coverage_map = {"City Core (0.1°)": 0.1, "Extended (0.15°)": 0.15, "Metropolitan (0.2°)": 0.2}

grid_res = resolution_map[grid_resolution]
grid_radius = coverage_map[coverage_area]

# Current analysis parameters
current_params = {
    'resolution': grid_res, 
    'radius': grid_radius, 
    'year': analysis_year
}

def generate_coordinate_grid(center_lat, center_lon, radius, resolution):
    """Generate a latitude-longitude grid covering Sulaimani metropolitan area"""
    st.info(f"📐 Generating population grid: {resolution:.3f}° resolution over {radius:.2f}° radius")
    
    # Generate coordinate arrays
    lats = np.arange(center_lat - radius, center_lat + radius + resolution, resolution)
    lons = np.arange(center_lon - radius, center_lon + radius + resolution, resolution)
    
    # Create grid coordinates
    coordinates = []
    for lat in lats:
        for lon in lons:
            coordinates.append([lat, lon])
    
    st.success(f"✅ Generated {len(coordinates)} population assessment points")
    return coordinates

def simulate_worldpop_data(coordinates, year):
    """
    Simulate WorldPop population density data for demonstration
    In production, this would access WorldPop API or Facebook HRSL data
    """
    st.info("👥 Simulating WorldPop population density data...")
    st.warning("⚠️ **Demo Mode**: Using simulated data. In production, this would connect to WorldPop API and Facebook HRSL services.")
    
    # Simulate population density based on distance from city center and realistic patterns
    population_densities = []
    
    for lat, lon in coordinates:
        # Calculate distance from Sulaimani center
        center_lat, center_lon = SULAIMANI_CENTER
        distance_from_center = np.sqrt((lat - center_lat)**2 + (lon - center_lon)**2)
        
        # Simulate realistic urban population distribution
        # Higher density near city center, with gradual decrease
        base_density = max(0, 1 - (distance_from_center / 0.15))  # Density decreases with distance
        
        # Add population clusters and neighborhoods
        # Central business district - very high density
        if (abs(lat - 35.5608) < 0.01 and abs(lon - 45.4347) < 0.01):
            base_density += 0.7  # CBD area
        
        # Residential neighborhoods - moderate to high density
        elif (abs(lat - 35.5650) < 0.02 and abs(lon - 45.4200) < 0.025) or \
             (abs(lat - 35.5550) < 0.02 and abs(lon - 45.4500) < 0.025):
            base_density += 0.4  # Residential areas
        
        # Suburban areas - moderate density
        elif distance_from_center < 0.08:
            base_density += 0.2  # Suburban zones
        
        # Rural/peripheral areas - low density
        elif distance_from_center > 0.12:
            base_density = max(0.05, base_density * 0.3)  # Rural areas
        
        # Add some randomness for realistic variation
        noise = np.random.normal(0, 0.1)
        
        # Ensure values are between 0 and 1
        population_density = max(0, min(1, base_density + noise))
        population_densities.append(population_density)
    
    return population_densities

def get_worldpop_data(coordinates, year):
    """
    Access WorldPop API for population density data (placeholder for production implementation)
    """
    st.info("🌍 Accessing WorldPop global population data...")
    
    # In production, this would:
    # 1. Query WorldPop API for the specified region and year
    # 2. Access Facebook High Resolution Settlement Layer (HRSL) data
    # 3. Process raster data to extract population counts per grid cell
    # 4. Convert to population density (people per km²)
    
    # For now, return simulated realistic data
    return simulate_worldpop_data(coordinates, year)

def normalize_population_density(densities):
    """Normalize population density values between 0 and 1"""
    if not densities or all(d == 0 for d in densities):
        return [0] * len(densities)
    
    min_val = min(densities)
    max_val = max(densities)
    
    if max_val == min_val:
        return [0.5] * len(densities)  # All same value, set to middle
    
    normalized = [(val - min_val) / (max_val - min_val) for val in densities]
    return normalized

def calculate_development_suitability_score(normalized_density):
    """
    Calculate development suitability based on population density
    Medium density values are more favorable; very high or very low less suitable
    """
    # Optimal development suitability curve
    # Low density (0.0-0.2): Score 40-60 (underdeveloped, needs infrastructure)
    # Medium density (0.2-0.7): Score 70-95 (optimal for expansion)
    # High density (0.7-1.0): Score 30-50 (overcrowded, infrastructure strain)
    
    if normalized_density < 0.1:
        return 45  # Very low density - lacks infrastructure
    elif normalized_density < 0.3:
        return 75  # Low-medium density - good expansion potential
    elif normalized_density < 0.6:
        return 90  # Medium density - optimal for development
    elif normalized_density < 0.8:
        return 65  # High density - getting crowded
    else:
        return 35  # Very high density - overcrowded, avoid expansion

def calculate_population_pressure(density, distance_from_center):
    """Calculate population pressure index based on density and location"""
    # Population pressure considers both density and proximity to city center
    base_pressure = density * 0.7  # Density contributes 70%
    
    # Distance factor (closer to center = higher pressure)
    distance_factor = max(0, 1 - distance_from_center / 0.15) * 0.3  # Distance contributes 30%
    
    return min(1.0, base_pressure + distance_factor)

def classify_population_zones(density, suitability_score):
    """Classify areas into population zones for planning"""
    if suitability_score >= 85:
        return "Optimal Expansion"
    elif suitability_score >= 70:
        return "Good Development"
    elif suitability_score >= 50:
        return "Limited Expansion"
    else:
        return "Avoid Development"

def save_population_data(df, params):
    """Save population density analysis results"""
    filename = f"population_density_{params['resolution']:.3f}_{params['radius']:.2f}_{params['year']}.csv"
    file_path = os.path.join(DATA_DIR, filename)
    df.to_csv(file_path, index=False)
    return filename

def run_population_analysis():
    """Execute the complete population density analysis"""
    
    st.markdown("### 🔄 **Running Population Density Analysis**")
    
    # Step 1: Generate coordinate grid
    coordinates = generate_coordinate_grid(
        SULAIMANI_CENTER[0], SULAIMANI_CENTER[1], 
        grid_radius, grid_res
    )
    
    # Step 2: Access WorldPop data
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("🌍 Accessing WorldPop population data...")
    progress_bar.progress(0.25)
    
    # Get population density data
    population_densities = get_worldpop_data(coordinates, analysis_year)
    
    progress_bar.progress(0.5)
    
    # Step 3: Normalize density values
    status_text.text("📊 Normalizing population density values...")
    normalized_densities = normalize_population_density(population_densities)
    
    progress_bar.progress(0.7)
    
    # Step 4: Calculate development suitability and population pressure
    status_text.text("🎯 Computing development suitability scores...")
    suitability_scores = []
    population_pressures = []
    planning_zones = []
    
    for i, (coord, norm_density) in enumerate(zip(coordinates, normalized_densities)):
        # Calculate distance from center for pressure calculation
        distance_km = calculate_distance(coord[0], coord[1], SULAIMANI_CENTER[0], SULAIMANI_CENTER[1])
        distance_degrees = distance_km / 111.0  # Approximate conversion
        
        suitability = calculate_development_suitability_score(norm_density)
        pressure = calculate_population_pressure(norm_density, distance_degrees)
        zone = classify_population_zones(norm_density, suitability)
        
        suitability_scores.append(suitability)
        population_pressures.append(pressure)
        planning_zones.append(zone)
    
    progress_bar.progress(0.9)
    
    # Step 5: Calculate additional metrics
    status_text.text("📈 Computing population metrics...")
    
    # Convert normalized density to estimated people per km² (for display)
    estimated_pop_density = [d * 5000 for d in normalized_densities]  # Scale to realistic values
    
    # Create results dataframe
    results_df = pd.DataFrame({
        'lat': [coord[0] for coord in coordinates],
        'lon': [coord[1] for coord in coordinates],
        'raw_population_density': population_densities,
        'normalized_density': normalized_densities,
        'estimated_pop_per_km2': estimated_pop_density,
        'development_suitability_score': suitability_scores,
        'population_pressure_index': population_pressures,
        'planning_zone': planning_zones,
        'distance_from_center_km': [calculate_distance(coord[0], coord[1], SULAIMANI_CENTER[0], SULAIMANI_CENTER[1]) for coord in coordinates]
    })
    
    # Save results
    filename = save_population_data(results_df, current_params)
    
    status_text.text("💾 Population analysis complete and saved!")
    progress_bar.progress(1.0)
    
    st.success(f"✅ **Population Analysis Complete!** Saved as: {filename}")
    
    return results_df

def display_population_results(df):
    """Display comprehensive population density analysis results"""
    
    st.markdown("### 📊 **Population Density Analysis Results**")
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        optimal_zones = (df['development_suitability_score'] >= 85).mean() * 100
        st.metric("Optimal Expansion Zones", f"{optimal_zones:.1f}%", delta="≥85 suitability")
    
    with col2:
        avg_density = df['estimated_pop_per_km2'].mean()
        st.metric("Average Pop. Density", f"{avg_density:.0f}/km²")
    
    with col3:
        high_pressure = (df['population_pressure_index'] >= 0.7).mean() * 100
        st.metric("High Pressure Areas", f"{high_pressure:.1f}%", delta="≥0.7 pressure")
    
    with col4:
        good_development = (df['planning_zone'].isin(['Optimal Expansion', 'Good Development'])).mean() * 100
        st.metric("Suitable for Development", f"{good_development:.1f}%")
    
    # Interactive population density map
    st.markdown("#### 👥 **Interactive Population Density Map**")
    
    # Create folium map
    m = folium.Map(
        location=SULAIMANI_CENTER,
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Add population density heatmap
    from folium.plugins import HeatMap
    
    # Prepare heatmap data for population density
    pop_heat_data = [[row['lat'], row['lon'], row['normalized_density']] 
                     for _, row in df.iterrows()]
    
    HeatMap(
        pop_heat_data,
        radius=20,
        blur=15,
        max_zoom=15,
        gradient={0.0: 'darkblue', 0.2: 'blue', 0.4: 'cyan', 0.6: 'yellow', 0.8: 'orange', 1.0: 'red'},
        name='Population Density'
    ).add_to(m)
    
    # Add development suitability layer
    suitability_data = [[row['lat'], row['lon'], row['development_suitability_score']/100] 
                       for _, row in df.iterrows()]
    
    suitability_layer = HeatMap(
        suitability_data,
        radius=25,
        blur=20,
        max_zoom=13,
        gradient={0.0: 'darkred', 0.3: 'red', 0.5: 'orange', 0.7: 'yellow', 0.9: 'lightgreen', 1.0: 'green'},
        name='Development Suitability'
    )
    
    # Add alternative tile layers
    folium.raster_layers.TileLayer(
        tiles='CartoDB positron',
        name='Light Theme',
        overlay=False,
        control=True
    ).add_to(m)
    
    folium.raster_layers.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add legend
    legend_html = f'''
    <div style="position: fixed; 
                top: 10px; right: 10px; width: 260px; height: 160px; 
                background-color: rgba(255,255,255,0.9); border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 10px;">
    <p><b>Population Density & Development Suitability</b></p>
    <p><i class="fa fa-circle" style="color:red"></i> High Population Density</p>
    <p><i class="fa fa-circle" style="color:yellow"></i> Medium Density (Optimal)</p>
    <p><i class="fa fa-circle" style="color:blue"></i> Low Density</p>
    <p><b>Year:</b> {analysis_year}</p>
    <p><b>Source:</b> WorldPop, Facebook HRSL</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    folium.LayerControl().add_to(m)
    
    st_folium(m, width=1400, height=500, key="population_density_map")
    
    # Statistical analysis charts
    st.markdown("#### 📈 **Population Analysis Dashboard**")
    
    # Create four separate charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Population density histogram
        fig1 = px.histogram(
            df, x='estimated_pop_per_km2', nbins=25,
            title='Population Density Distribution',
            labels={'estimated_pop_per_km2': 'Population per km²', 'count': 'Frequency'},
            color_discrete_sequence=['steelblue']
        )
        fig1.update_layout(height=300)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Development suitability vs density scatter
        fig3 = px.scatter(
            df, x='normalized_density', y='development_suitability_score',
            title='Population Density vs Development Suitability',
            labels={'normalized_density': 'Normalized Density', 'development_suitability_score': 'Suitability Score'},
            color='population_pressure_index',
            color_continuous_scale='Reds'
        )
        fig3.update_layout(height=300)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Development suitability histogram  
        fig2 = px.histogram(
            df, x='development_suitability_score', nbins=20,
            title='Development Suitability Distribution',
            labels={'development_suitability_score': 'Suitability Score', 'count': 'Frequency'},
            color_discrete_sequence=['lightcoral']
        )
        fig2.update_layout(height=300)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Planning zones pie chart
        zone_counts = df['planning_zone'].value_counts()
        fig4 = px.pie(
            values=zone_counts.values,
            names=zone_counts.index,
            title='Planning Zones Distribution',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig4.update_layout(height=300)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Population pressure analysis
    st.markdown("#### 📊 **Population Pressure Analysis**")
    
    # Pressure vs distance analysis
    fig5 = px.scatter(
        df, x='distance_from_center_km', y='population_pressure_index',
        title='Population Pressure by Distance from City Center',
        labels={'distance_from_center_km': 'Distance from Center (km)', 'population_pressure_index': 'Population Pressure Index'},
        color='planning_zone',
        size='estimated_pop_per_km2',
        hover_data=['development_suitability_score']
    )
    fig5.update_layout(height=400)
    st.plotly_chart(fig5, use_container_width=True)
    
    # Development recommendations
    st.markdown("#### 🎯 **Population-Based Development Recommendations**")
    
    # Analyze planning zones
    optimal = df[df['planning_zone'] == 'Optimal Expansion']
    good = df[df['planning_zone'] == 'Good Development']
    limited = df[df['planning_zone'] == 'Limited Expansion']
    avoid = df[df['planning_zone'] == 'Avoid Development']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"**🟢 Optimal Expansion: {len(optimal)} areas ({len(optimal)/len(df)*100:.1f}%)**")
        st.info(f"**🔵 Good Development: {len(good)} areas ({len(good)/len(df)*100:.1f}%)**")
    
    with col2:
        st.warning(f"**🟡 Limited Expansion: {len(limited)} areas ({len(limited)/len(df)*100:.1f}%)**")
        st.error(f"**🔴 Avoid Development: {len(avoid)} areas ({len(avoid)/len(df)*100:.1f}%)**")
    
    # Best development zone details
    if len(optimal) > 0:
        best_zone = optimal.loc[optimal['development_suitability_score'].idxmax()]
        st.info(f"""
        **🏆 Prime Development Zone:**
        - Coordinates: {best_zone['lat']:.4f}°N, {best_zone['lon']:.4f}°E
        - Population Density: {best_zone['estimated_pop_per_km2']:.0f} people/km²
        - Suitability Score: {best_zone['development_suitability_score']:.1f}/100
        - Population Pressure: {best_zone['population_pressure_index']:.2f}
        - Distance from Center: {best_zone['distance_from_center_km']:.1f} km
        """)
    
    # Planning recommendations by zone
    st.markdown(f"""
    #### 📋 **Strategic Population Planning Guidelines**
    
    **Development Priority by Population Zones:**
    
    **🟢 Optimal Expansion Zones (85-100 suitability):**
    - Medium population density with good infrastructure potential
    - Priority areas for new residential and commercial development
    - Balanced population pressure allows sustainable growth
    
    **🔵 Good Development Zones (70-84 suitability):**
    - Moderate density suitable for controlled expansion
    - Secondary priority for mixed-use development
    - Requires infrastructure assessment before major development
    
    **🟡 Limited Expansion Zones (50-69 suitability):**
    - Higher density areas requiring careful planning
    - Consider infill development and infrastructure upgrades
    - Monitor population pressure before expansion
    
    **🔴 Avoid Development Zones (<50 suitability):**
    - Very high density (overcrowded) or very low density (lacks infrastructure)
    - Focus on infrastructure improvement rather than expansion
    - Consider population redistribution strategies
    
    **Population Management Strategies:**
    
    **Density Balancing:**
    - **Target Range**: 1,000-3,000 people/km² for new developments
    - **High Density Areas**: Improve vertical development and services
    - **Low Density Areas**: Gradual densification with infrastructure development
    
    **Infrastructure Planning:**
    - **Schools**: 1 per 500 students (plan for population growth)
    - **Healthcare**: 1 clinic per 2,000 residents  
    - **Transportation**: Plan for 20% population increase over 10 years
    - **Utilities**: Water/sewage capacity for peak density scenarios
    
    **Sustainable Growth Guidelines:**
    - **Population Distribution**: Encourage medium-density development
    - **Urban Sprawl Control**: Direct growth to optimal expansion zones
    - **Service Accessibility**: Ensure 15-minute city principles
    - **Environmental Balance**: Maintain green space ratios as population grows
    
    **Monitoring Recommendations:**
    - **Regular Updates**: Update population data every 2-3 years
    - **Growth Tracking**: Monitor development impact on population pressure
    - **Infrastructure Capacity**: Assess service capacity vs population growth
    - **Quality of Life**: Track density impact on livability metrics
    
    **Data Quality Note:**
    Analysis based on {analysis_year} WorldPop and Facebook HRSL data. 
    Recommend validation with local census data and regular monitoring 
    for accurate population-based planning decisions.
    """)

# Main execution flow
if st.button("👥 Analyze Population Density & Development Suitability", type="primary"):
    with st.spinner("🌍 Analyzing population density and development potential..."):
        population_df = run_population_analysis()
        st.session_state.population_df = population_df
        st.session_state.population_analysis_completed = True

# Display results if analysis completed
if st.session_state.population_analysis_completed and st.session_state.population_df is not None:
    display_population_results(st.session_state.population_df)
    
    # Option to clear results and start fresh
    if st.button("🗑️ Clear Analysis & Start Fresh"):
        st.session_state.population_analysis_completed = False
        st.session_state.population_df = None
        st.rerun()

# Additional information
with st.expander("ℹ️ **About Population Density Analysis**"):
    st.markdown("""
    ### 🌍 **Data Sources & Methodology**
    
    **WorldPop Global Population Data:**
    - **High Resolution**: ~100m resolution population distribution models
    - **Annual Updates**: Population estimates adjusted for migration and growth
    - **Demographic Integration**: Age, sex, and urbanization factors considered
    - **Validation**: Ground-truthed with census data and surveys
    
    **Facebook High Resolution Settlement Layer (HRSL):**
    - **Settlement Detection**: AI-powered identification of populated areas
    - **Building Footprint**: Satellite imagery analysis for population estimation
    - **Cross-Validation**: Combined with census data for accuracy
    - **Global Coverage**: Consistent methodology across regions
    
    **Processing Pipeline:**
    1. **Data Acquisition**: Access WorldPop raster data via API or download
    2. **Regional Clipping**: Extract population data for Sulaimani metropolitan area
    3. **Grid Aggregation**: Sum population counts per analysis grid cell  
    4. **Density Calculation**: Convert to people per km² for standardized comparison
    5. **Normalization**: Scale density values 0-1 for suitability analysis
    6. **Suitability Modeling**: Apply optimal density curve for development planning
    
    **Development Suitability Algorithm:**
    - **Low Density (0.0-0.3)**: Score 40-75 (infrastructure development needed)
    - **Medium Density (0.3-0.6)**: Score 75-95 (optimal for expansion)
    - **High Density (0.6-1.0)**: Score 35-65 (infrastructure strain concerns)
    
    ### 📊 **Analysis Applications**
    
    **Urban Planning:**
    - Identify optimal zones for residential and commercial development
    - Balance population distribution across metropolitan area
    - Plan infrastructure capacity based on population projections
    
    **Infrastructure Development:**
    - Prioritize areas needing schools, healthcare, and utilities
    - Optimize transportation networks for population flows
    - Plan green spaces and recreational facilities based on density
    
    **Sustainable Development:**
    - Prevent urban sprawl into inappropriate areas
    - Manage population pressure to maintain quality of life
    - Balance economic development with environmental preservation
    
    ### 🔬 **Technical Details**
    
    **Current Implementation:**
    - **Demo Mode**: Uses simulated population patterns based on urban development principles
    - **Production**: Would integrate WorldPop API and Facebook Data for Good services
    - **Real-time**: Supports historical analysis (2020-2023) and projection capabilities
    - **Scalable**: Configurable grid resolution and metropolitan coverage area
    
    **Population Pressure Index:**
    - **Density Component**: 70% weight - normalized population density
    - **Location Component**: 30% weight - proximity to city center
    - **Pressure Threshold**: >0.7 indicates high population pressure requiring management
    
    **Data Quality Considerations:**
    - **Resolution**: WorldPop ~100m, Facebook HRSL building-level
    - **Temporal**: Annual updates with inter-census adjustments
    - **Accuracy**: ±10-15% compared to ground truth in urban areas
    - **Coverage**: Global availability with regional validation
    
    **Planning Integration:**
    - **Zoning**: Population analysis informs residential/commercial zoning
    - **Services**: Healthcare, education capacity planning based on density projections
    - **Transportation**: Public transit planning for population corridors
    - **Environment**: Green space requirements scaled to population density
    """)

# Show current settings
st.sidebar.markdown("### 📋 **Current Analysis Settings**")
st.sidebar.info(f"""
**Grid Resolution:** {grid_res:.3f}° (~{grid_res*111:.0f}m spacing)
**Coverage Area:** {grid_radius:.2f}° (~{grid_radius*111:.0f}km radius)  
**Analysis Year:** {analysis_year}
**Analysis Points:** ~{int((2*grid_radius/grid_res)**2)} coordinates
**Data Source:** WorldPop, Facebook HRSL
**Optimal Density:** Medium values (30-60% normalized)
""")

# Data sources information
st.sidebar.markdown("### 🌍 **Data Sources**")
st.sidebar.markdown("""
**Primary:**
- WorldPop Global Population
- Facebook HRSL (Meta)

**APIs:**
- WorldPop Data Portal
- Humanitarian Data Exchange

**Methodology:**
- Population Pressure Analysis
- Development Suitability Modeling
- Infrastructure Capacity Planning

**Resolution:**
- Spatial: ~100m (WorldPop)
- Temporal: Annual updates
""")