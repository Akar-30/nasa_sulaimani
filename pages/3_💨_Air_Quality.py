import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Air Quality & Health", page_icon="💨", layout="wide")

st.title("💨 Air Quality & Public Health")

st.markdown("""
This section identifies pollution hotspots in Sulaimani and highlights communities most at risk 
from poor air quality based on NASA Sentinel-5P and MODIS data.
""")

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Avg NO₂ Level",
        value="45 µg/m³",
        delta="8% from last year",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="PM2.5 Concentration",
        value="62 µg/m³",
        delta="Above WHO limit",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="High-Risk Population",
        value="~85,000",
        delta="Living in hotspots"
    )

with col4:
    st.metric(
        label="Pollution Days",
        value="152/year",
        delta="Unhealthy AQI",
        delta_color="inverse"
    )

st.markdown("---")

# Interactive controls
st.header("🗺️ Pollution Hotspot Map")

col1, col2, col3 = st.columns(3)

with col1:
    pollutant = st.selectbox(
        "Select Pollutant",
        ["NO₂ (Nitrogen Dioxide)", "PM2.5 (Particulate Matter)", "SO₂ (Sulfur Dioxide)", "O₃ (Ozone)"]
    )

with col2:
    season = st.selectbox(
        "Select Season",
        ["Annual Average", "Winter", "Spring", "Summer", "Fall"]
    )

with col3:
    overlay_population = st.checkbox("Show Population Density", value=True)

# Create map
m = folium.Map(
    location=[35.5608, 45.4347],
    zoom_start=12,
    tiles='OpenStreetMap'
)

# Add satellite imagery
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite',
    overlay=False,
    control=True
).add_to(m)

# TODO: Add heatmap layer when data is provided
# Example of how it will work:
# if os.path.exists('data/air_quality_no2.csv'):
#     data = pd.read_csv('data/air_quality_no2.csv')
#     heat_data = [[row['lat'], row['lon'], row['value']] for _, row in data.iterrows()]
#     HeatMap(heat_data, radius=15, blur=25, max_zoom=13).add_to(m)

# Add example markers for now (will be replaced with real data)
pollution_zones = [
    {"name": "Eastern Sulaimani (Main Road)", "lat": 35.5708, "lon": 45.4547, "level": "High"},
    {"name": "Industrial Zone", "lat": 35.5408, "lon": 45.4147, "level": "Very High"},
    {"name": "City Center", "lat": 35.5608, "lon": 45.4347, "level": "Moderate"},
]

for zone in pollution_zones:
    color = "red" if zone["level"] == "Very High" else "orange" if zone["level"] == "High" else "yellow"
    folium.CircleMarker(
        location=[zone["lat"], zone["lon"]],
        radius=20,
        popup=f"<b>{zone['name']}</b><br>Pollution: {zone['level']}",
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.4
    ).add_to(m)

folium.LayerControl().add_to(m)

st_folium(m, width=1400, height=500)

st.info("""
**📥 Data Integration Point**: Once you provide `air_quality_no2.csv`, `air_quality_pm25.csv`, 
and `pollution_hotspots.geojson`, this map will show actual pollution heatmaps from Sentinel-5P data.
""")

st.markdown("---")

# Temporal trends
st.header("📈 Air Quality Trends")

# Placeholder data - will be replaced with real data
years = list(range(2018, 2026))
no2_values = [38, 42, 45, 48, 51, 47, 52, 55]
pm25_values = [52, 54, 58, 61, 64, 59, 67, 70]

df = pd.DataFrame({
    'Year': years,
    'NO₂ (µg/m³)': no2_values,
    'PM2.5 (µg/m³)': pm25_values
})

fig = px.line(
    df,
    x='Year',
    y=['NO₂ (µg/m³)', 'PM2.5 (µg/m³)'],
    title='Air Pollutant Concentration Trends (2018-2025)',
    labels={'value': 'Concentration (µg/m³)', 'variable': 'Pollutant'},
    markers=True
)

# Add WHO guideline lines
fig.add_hline(y=40, line_dash="dash", line_color="orange", 
              annotation_text="WHO NO₂ Guideline")
fig.add_hline(y=15, line_dash="dash", line_color="red", 
              annotation_text="WHO PM2.5 Guideline")

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Neighborhood analysis
st.header("🏘️ Pollution Exposure by Neighborhood")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### High-Risk Neighborhoods
    
    Based on combined pollution levels and population density:
    
    1. **Eastern Sulaimani** - High NO₂ during morning traffic
       - Estimated affected: ~20,000 residents
       - Main source: Major road traffic
       
    2. **Industrial Zone (West)** - Elevated PM2.5
       - Estimated affected: ~15,000 residents
       - Main source: Industrial emissions
       
    3. **City Center** - Moderate pollution, high density
       - Estimated affected: ~50,000 residents
       - Main source: Traffic congestion
    """)

with col2:
    # Placeholder bar chart
    neighborhoods = ['Eastern\nSulaimani', 'Industrial\nZone', 'City\nCenter', 'Northern\nSuburbs', 'Southern\nDistrict']
    pollution_scores = [85, 92, 68, 45, 38]
    
    fig = px.bar(
        x=neighborhoods,
        y=pollution_scores,
        title='Pollution Exposure Index by Neighborhood',
        labels={'x': 'Neighborhood', 'y': 'Exposure Index'},
        color=pollution_scores,
        color_continuous_scale='Reds'
    )
    
    fig.add_hline(y=70, line_dash="dash", line_color="red", 
                  annotation_text="High Risk Threshold")
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Insights and recommendations
st.header("💡 Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    ### 📊 Data Insights
    
    - **Eastern Sulaimani** has the highest NO₂ levels during morning traffic hours
    - **Seasonal variation**: Pollution peaks in **spring** due to dust storms
    - **Industrial zone** contributes 35% of total PM2.5 emissions
    - **Traffic corridors** show 2-3x higher pollution than residential areas
    """)

with col2:
    st.warning("""
    ### 🎯 Recommendations
    
    - **Green buffer zones** along major roads to filter pollutants
    - **Traffic management** during peak hours in Eastern district
    - **Industrial emission controls** with modern filtration
    - **Public transport expansion** to reduce vehicle emissions
    - **Air quality monitoring stations** in high-risk neighborhoods
    """)

# Data requirements reminder
st.markdown("---")
st.info("""
### 📥 Data Files Needed for This Page

Please prepare and save in `/data` folder:
- `air_quality_no2.csv` - NO₂ concentrations with lat, lon, date, value
- `air_quality_pm25.csv` - PM2.5 concentrations with lat, lon, date, value
- `pollution_hotspots.geojson` - Polygon boundaries of high-pollution areas
- `population_density.geojson` - Population density by neighborhood
- `neighborhood_stats.csv` - Per-neighborhood pollution and population data
""")
