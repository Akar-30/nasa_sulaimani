import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="Data Pathway", page_icon="📊", layout="wide")

st.title("📊 Our Data Pathway")

st.markdown("""
To guide sustainable growth in Sulaimani City, we used **Earth observation data from NASA 
and international partners**. By analyzing air quality, heat, vegetation, urban expansion, 
and water availability, we can identify challenges and opportunities for people and the environment.
""")

# Data processing workflow
st.header("🔄 Data Processing Workflow")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    ### 1️⃣ Data Collection
    - Download from NASA servers
    - Sentinel-5P, MODIS, Landsat
    - Time series data (2005-2025)
    """)

with col2:
    st.markdown("""
    ### 2️⃣ Processing
    - Cloud masking
    - Atmospheric correction
    - Spatial resampling
    """)

with col3:
    st.markdown("""
    ### 3️⃣ Analysis
    - Calculate indices (NDVI, LST)
    - Temporal aggregation
    - Spatial statistics
    """)

with col4:
    st.markdown("""
    ### 4️⃣ Visualization
    - Interactive maps
    - Time series charts
    - Insights generation
    """)

st.markdown("---")

# Dataset showcase with tabs
st.header("🗂️ Dataset Categories")

tab1, tab2, tab3, tab4 = st.tabs([
    "🌫️ Air Quality",
    "🌡️ Heat & Vegetation", 
    "🏗️ Urban Growth",
    "💧 Water Resources"
])

with tab1:
    st.subheader("Air Quality & Public Health Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Objective**: Identify neighborhoods facing high pollution and where interventions are needed.
        
        **Datasets Used**:
        - **Sentinel-5P (TROPOMI)**: NO₂, SO₂, O₃, aerosols (monthly averages)
        - **MODIS Aerosol Optical Depth (AOD)**: Particulate matter distribution
        - **WorldPop**: Population density overlays
        
        **Analysis Methods**:
        - Map pollution levels across the city
        - Identify high-risk populations near roads, industrial areas
        - Show temporal trends (seasonal patterns)
        - Calculate exposure indices per neighborhood
        """)
    
    with col2:
        st.info("""
        **Data Files Needed:**
        - `air_quality_no2.csv`
        - `air_quality_pm25.csv`
        - `pollution_hotspots.geojson`
        - `population_density.geojson`
        
        **Format**: CSV with columns:
        - date, lat, lon, value
        """)
    
    st.markdown("**Sample Visualization** (will use your data):")
    
    # Placeholder map for air quality
    m = folium.Map(location=[35.5608, 45.4347], zoom_start=12)
    st_folium(m, height=400)

with tab2:
    st.subheader("Urban Heat & Greenspace Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Objective**: Identify urban heat islands and evaluate greenspace availability.
        
        **Datasets Used**:
        - **Landsat 8/9 Thermal Bands**: Land Surface Temperature (LST) maps
        - **MODIS NDVI**: Vegetation index
        - **Copernicus GHSL**: Urban footprint overlay
        
        **Analysis Methods**:
        - Identify hotspots with little vegetation
        - Map parks, rivers, agricultural land
        - Propose tree corridors in heat-prone areas
        - Calculate greenspace percentage per neighborhood
        """)
    
    with col2:
        st.info("""
        **Data Files Needed:**
        - `temperature_lst.csv`
        - `ndvi_values.csv`
        - `green_spaces.geojson`
        - `heat_islands.geojson`
        
        **Format**: GeoTIFF or CSV
        - date, lat, lon, temperature
        - date, lat, lon, ndvi
        """)
    
    st.markdown("**Sample Visualization** (will use your data):")
    m = folium.Map(location=[35.5608, 45.4347], zoom_start=12)
    st_folium(m, height=400)

with tab3:
    st.subheader("Urban Growth & Housing Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Objective**: Understand population growth patterns and sustainable housing needs.
        
        **Datasets Used**:
        - **Copernicus GHSL**: Urban density and built-up area
        - **WorldPop**: Population density and growth trends
        - **NASA Earth Observatory**: Historical urban expansion imagery
        
        **Analysis Methods**:
        - Detect rapidly growing neighborhoods
        - Inform zoning decisions with overlay analysis
        - Identify areas lacking infrastructure
        - Project future growth patterns
        """)
    
    with col2:
        st.info("""
        **Data Files Needed:**
        - `urban_extent_2005.geojson`
        - `urban_extent_2015.geojson`
        - `urban_extent_2025.geojson`
        - `population_growth.csv`
        
        **Format**: GeoJSON polygons
        showing urban boundaries
        """)
    
    st.markdown("**Sample Visualization** (will use your data):")
    m = folium.Map(location=[35.5608, 45.4347], zoom_start=11)
    st_folium(m, height=400)

with tab4:
    st.subheader("Water & Environmental Stress Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Objective**: Evaluate water availability and climate vulnerability.
        
        **Datasets Used**:
        - **GRACE**: Groundwater availability and depletion
        - **IMERG/TRMM**: Precipitation trends and drought risk
        - **MODIS NDVI & Landsat**: Vegetation health as water stress proxy
        
        **Analysis Methods**:
        - Identify areas at risk of water scarcity
        - Overlay with urban growth zones
        - Propose water-saving infrastructure
        - Map drought-vulnerable areas
        """)
    
    with col2:
        st.info("""
        **Data Files Needed:**
        - `groundwater_trend.csv`
        - `precipitation.csv`
        - `water_stress_zones.geojson`
        
        **Format**: Time series CSV
        - year, value
        - lat, lon, stress_level
        """)
    
    st.markdown("**Sample Visualization** (will use your data):")
    m = folium.Map(location=[35.5608, 45.4347], zoom_start=12)
    st_folium(m, height=400)

st.markdown("---")

# Data integration
st.header("🔗 Bringing It All Together")

st.markdown("""
The final dashboard combines **air quality, heat, urban growth, greenspace, and water stress** 
layers into an interactive map. Planners can filter by risk type or neighborhood to:

- Identify priority intervention areas
- Plan sustainable expansion zones
- Allocate resources effectively
- Monitor changes over time

Residents can also report local conditions to complement satellite data.
""")

st.success("""
### 📥 Ready to Add Your Data?

As you prepare the datasets, save them in the `/data` folder following the formats specified above. 
The maps will automatically populate with your actual NASA data!
""")
