import streamlit as st
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="Sulaimani Sustainable Growth",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .highlight-box {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 20px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.1rem;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Main content
st.markdown('<p class="main-header">🌍 Sulaimani Sustainable Growth</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Using NASA Earth Observation Data for Urban Planning</p>', unsafe_allow_html=True)

# Ultimate Question
st.markdown("""
<div class="highlight-box">
    <h2>🎯 The Ultimate Question</h2>
    <p style="font-size: 1.2rem; font-weight: bold;">
    "How can Sulaimani City grow sustainably to ensure both people's wellbeing and 
    environmental resilience, informed by NASA Earth observation data?"
    </p>
</div>
""", unsafe_allow_html=True)

# Introduction
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 🏙️ About This Project
    
    Sulaimani is growing rapidly. Using **NASA Earth observation data**, we explore how the 
    city can expand in a way that protects people, resources, and the environment.
    
    This interactive platform combines multiple datasets to provide insights for:
    - 👥 **Urban Planners** - Data-driven zoning and infrastructure decisions
    - 🌱 **Environmental Agencies** - Green space and air quality monitoring
    - 🏘️ **City Residents** - Understanding local environmental conditions
    - 💧 **Water Management** - Sustainable resource allocation
    
    Navigate through the sections using the sidebar to explore different aspects of 
    sustainable urban growth in Sulaimani.
    """)

with col2:
    st.info("""
    ### 📊 Data Sources
    - NASA MODIS
    - Sentinel-5P (TROPOMI)
    - Landsat 8/9
    - Copernicus GHSL
    - WorldPop
    - GRACE
    - IMERG
    """)

# Interactive map of Sulaimani
st.markdown("---")
st.subheader("📍 Sulaimani City Overview")

# Create base map (you can add overlays once data is ready)
m = folium.Map(
    location=[35.5608, 45.4347],  # Sulaimani coordinates
    zoom_start=12,
    tiles='OpenStreetMap'
)

# Add satellite imagery option
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite',
    overlay=False,
    control=True
).add_to(m)

# Add marker for city center
folium.Marker(
    [35.5608, 45.4347],
    popup="Sulaimani City Center",
    tooltip="Click for more info",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Layer control
folium.LayerControl().add_to(m)

# Display map
st_folium(m, width=1400, height=500)

# Key Statistics (placeholder - will be populated with real data)
st.markdown("---")
st.subheader("📈 Key Insights at a Glance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🌡️ Avg Temperature Increase",
        value="2.3°C",
        delta="Since 2005",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="🏙️ Urban Expansion",
        value="45%",
        delta="20 years",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="🌳 Green Space Loss",
        value="-18%",
        delta="Declining",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="💨 Air Quality Days",
        value="152",
        delta="Unhealthy days/year",
        delta_color="inverse"
    )

# Navigation guide
st.markdown("---")
st.subheader("🧭 Navigate the Platform")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 🔴 Challenges
    - Urban Growth Analysis
    - Air Quality Assessment
    - Heat Island Mapping
    """)

with col2:
    st.markdown("""
    #### 📊 Data Insights
    - Air Quality & Health
    - Heat & Greenspace
    - Topography Analysis
    - Infrastructure Accessibility
    - Water Resources
    """)

with col3:
    st.markdown("""
    #### ✅ Solutions
    - Sustainable Zoning
    - Green Infrastructure
    - Future Vision
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🚀 Built for NASA Space Apps Challenge 2025 | Sulaimani Team</p>
    <p>Data sources: NASA Earth Observations, Copernicus, WorldPop</p>
</div>
""", unsafe_allow_html=True)
