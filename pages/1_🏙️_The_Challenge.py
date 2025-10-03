import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="The Challenge", page_icon="🏙️", layout="wide")

st.title("🏙️ The Challenge: Sulaimani Today")

st.markdown("""
This section explains the local context of Sulaimani's rapid urban growth and the environmental 
challenges the city faces, backed by NASA Earth observation data.
""")

# Problem Overview
st.header("⚠️ Urban Challenges")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🌆 Rapid Urban Growth
    Sulaimani has experienced unprecedented growth over the past two decades:
    - Population increase of **40%+** since 2005
    - Urban footprint expanded into agricultural land
    - Infrastructure struggling to keep pace
    - Informal settlements in high-risk areas
    """)
    
with col2:
    st.markdown("""
    ### 🌡️ Climate & Environmental Risks
    The city faces mounting environmental pressures:
    - Rising temperatures and heat islands
    - Air pollution from traffic and industry
    - Declining green space and vegetation
    - Water scarcity and groundwater depletion
    """)

st.markdown("---")

# Problem at a Glance Infographic
st.header("📊 Problems at a Glance")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🌡️ Heat Stress")
    
    # Placeholder chart - will be replaced with real data
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=38.5,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Summer Peak Temp (°C)"},
        delta={'reference': 36.2, 'increasing': {'color': "red"}},
        gauge={
            'axis': {'range': [None, 50]},
            'bar': {'color': "darkred"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 40], 'color': "yellow"},
                {'range': [40, 50], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 40
            }
        }
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 💨 Air Quality")
    
    # Air quality trend placeholder
    years = list(range(2015, 2026))
    aqi_values = [85, 92, 98, 105, 112, 118, 125, 132, 128, 135, 142]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=aqi_values,
        mode='lines+markers',
        name='AQI',
        line=dict(color='orange', width=3),
        fill='tozeroy'
    ))
    fig.add_hline(y=100, line_dash="dash", line_color="red", 
                  annotation_text="Unhealthy Threshold")
    fig.update_layout(
        title="Air Quality Index Trend",
        xaxis_title="Year",
        yaxis_title="AQI",
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.markdown("### 💧 Water Scarcity")
    
    # Water availability gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=65,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Water Availability Index"},
        delta={'reference': 85, 'decreasing': {'color': "red"}},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "lightblue"}
            ],
        }
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Urban Growth Map
st.header("🗺️ Urban Expansion Over Time")

st.markdown("""
The map below shows how Sulaimani has expanded over the past 20 years. 
Use the slider to see the progression of urban development.
""")

# Year selector
year = st.slider("Select Year", 2005, 2025, 2025, 5)

# Create map
m = folium.Map(
    location=[35.5608, 45.4347],
    zoom_start=11,
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

# TODO: Add urban expansion layers based on year selected
# This will use your prepared data showing urban growth

folium.LayerControl().add_to(m)

st_folium(m, width=1400, height=500)

st.info(f"""
**Viewing urban extent for year: {year}**

Once you provide the urban growth data (GeoJSON files for different years), 
this map will show the expanding city boundaries and new development areas.
""")

# NASA Background Datasets
st.markdown("---")
st.header("🛰️ NASA Datasets Used")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Air Quality Data
    - **Sentinel-5P (TROPOMI)**: NO₂, SO₂, O₃ levels
    - **MODIS Aerosol Optical Depth**: Particulate matter distribution
    - **Temporal Coverage**: 2018-2025
    - **Spatial Resolution**: 5.5km × 3.5km
    """)
    
    st.markdown("""
    ### Temperature & Vegetation
    - **Landsat 8/9**: Thermal bands for Land Surface Temperature
    - **MODIS NDVI**: Vegetation health and coverage
    - **Temporal Coverage**: 2005-2025
    - **Spatial Resolution**: 30m (Landsat), 250m (MODIS)
    """)

with col2:
    st.markdown("""
    ### Urban Growth Data
    - **Copernicus GHSL**: Built-up area mapping
    - **WorldPop**: Population density estimates
    - **NASA Earth Observatory**: Historical imagery
    - **Temporal Coverage**: 2000-2025
    """)
    
    st.markdown("""
    ### Water Resources
    - **GRACE**: Groundwater availability trends
    - **IMERG/TRMM**: Precipitation data
    - **MODIS**: Vegetation as water stress proxy
    - **Temporal Coverage**: 2002-2025
    """)

# Call to action
st.markdown("---")
st.success("""
### 🔍 Next Steps
Explore the **Data Pathway** section to see how we process and analyze these datasets 
to answer critical questions about Sulaimani's sustainable growth.
""")
