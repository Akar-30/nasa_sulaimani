import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Heat & Greenspace", page_icon="🌡️", layout="wide")

st.title("🌡️ Heat Islands & Greenspace")

st.markdown("""
This section identifies urban heat islands and evaluates greenspace availability to mitigate 
heat stress in Sulaimani, using Landsat and MODIS data.
""")

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Max Surface Temp",
        value="52°C",
        delta="+4°C vs rural",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="Avg NDVI (City)",
        value="0.32",
        delta="-15% since 2005",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="Green Space Coverage",
        value="18%",
        delta="Below WHO standard (30%)"
    )

with col4:
    st.metric(
        label="Heat-Affected Pop.",
        value="~125,000",
        delta="Living in heat islands"
    )

st.markdown("---")

# Interactive map controls
st.header("🗺️ Heat Island & Vegetation Map")

col1, col2, col3 = st.columns(3)

with col1:
    map_type = st.selectbox(
        "Map Type",
        ["Land Surface Temperature", "NDVI (Vegetation)", "Combined Heat + NDVI"]
    )

with col2:
    season_heat = st.selectbox(
        "Season",
        ["Summer (Peak Heat)", "Spring", "Fall", "Winter", "Annual Average"]
    )

with col3:
    show_parks = st.checkbox("Show Existing Parks", value=True)

# Create dual map or single map based on selection
if map_type == "Combined Heat + NDVI":
    st.subheader("Side-by-Side Comparison: Temperature vs Vegetation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🌡️ Land Surface Temperature**")
        m_temp = folium.Map(location=[35.5608, 45.4347], zoom_start=12)
        # TODO: Add temperature layer from your data
        st_folium(m_temp, height=450)
    
    with col2:
        st.markdown("**🌳 Vegetation Index (NDVI)**")
        m_ndvi = folium.Map(location=[35.5608, 45.4347], zoom_start=12)
        # TODO: Add NDVI layer from your data
        st_folium(m_ndvi, height=450)
        
else:
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
    
    # TODO: Add heat/NDVI layers from your data
    
    # Example markers for parks (will be replaced with GeoJSON)
    if show_parks:
        parks = [
            {"name": "Azadi Park", "lat": 35.5608, "lon": 45.4347},
            {"name": "Sami Abdulrahman Park", "lat": 35.5508, "lon": 45.4247},
        ]
        
        for park in parks:
            folium.Marker(
                location=[park["lat"], park["lon"]],
                popup=park["name"],
                icon=folium.Icon(color='green', icon='tree', prefix='fa')
            ).add_to(m)
    
    folium.LayerControl().add_to(m)
    
    st_folium(m, width=1400, height=500)

st.info("""
**📥 Data Integration Point**: Provide `temperature_lst.csv` (Landsat thermal data), 
`ndvi_values.csv` (MODIS NDVI), and `green_spaces.geojson` (existing parks/vegetation) 
to populate these maps with real data.
""")

st.markdown("---")

# Temperature trends
st.header("📈 Heat Island Intensity Over Time")

# Placeholder data
years = list(range(2005, 2026, 5))
urban_temp = [48, 49.5, 51, 52, 52.5]
rural_temp = [44, 44.5, 45, 46, 46.5]

df_temp = pd.DataFrame({
    'Year': years,
    'Urban Core Temperature': urban_temp,
    'Rural/Suburban Temperature': rural_temp
})

fig = px.line(
    df_temp,
    x='Year',
    y=['Urban Core Temperature', 'Rural/Suburban Temperature'],
    title='Urban Heat Island Effect (Summer Peak LST)',
    labels={'value': 'Land Surface Temperature (°C)', 'variable': 'Location'},
    markers=True
)

fig.update_layout(hovermode='x unified')
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Greenspace analysis
st.header("🌳 Greenspace Distribution")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Greenspace Per Neighborhood")
    
    # Placeholder data
    neighborhoods = ['Downtown', 'Northern\nSuburbs', 'Eastern\nDistrict', 'Western\nZone', 'Southern\nArea']
    greenspace_pct = [8, 25, 12, 15, 22]
    
    fig = px.bar(
        x=neighborhoods,
        y=greenspace_pct,
        title='Percentage of Green Space Coverage',
        labels={'x': 'Neighborhood', 'y': 'Green Space (%)'},
        color=greenspace_pct,
        color_continuous_scale='Greens'
    )
    
    fig.add_hline(y=30, line_dash="dash", line_color="green", 
                  annotation_text="WHO Recommendation (30%)")
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### NDVI Trend")
    
    # Placeholder NDVI trend
    years_ndvi = list(range(2005, 2026, 2))
    ndvi_avg = [0.42, 0.40, 0.38, 0.36, 0.34, 0.33, 0.32, 0.31, 0.30, 0.32, 0.31]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years_ndvi,
        y=ndvi_avg,
        mode='lines+markers',
        name='City Average NDVI',
        line=dict(color='green', width=3),
        fill='tozeroy'
    ))
    
    fig.update_layout(
        title='Vegetation Health Trend (NDVI)',
        xaxis_title='Year',
        yaxis_title='NDVI Value',
        yaxis=dict(range=[0, 1])
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Priority zones for greening
st.header("🎯 Priority Zones for Green Infrastructure")

st.markdown("""
Based on combined analysis of high temperatures, low NDVI, and population density, 
the following areas are priorities for urban greening:
""")

col1, col2 = st.columns(2)

with col1:
    st.error("""
    ### 🔴 Critical Priority Areas
    
    1. **Downtown & Northern Suburbs**
       - Highest temperatures (52°C peak LST)
       - NDVI < 0.2 (minimal vegetation)
       - Dense population
       - **Recommendation**: Green corridors along main streets
    
    2. **Eastern Industrial District**
       - High heat + air pollution
       - Almost no vegetation
       - **Recommendation**: Buffer zones with trees
    """)

with col2:
    st.success("""
    ### 🟢 Proposed Solutions
    
    - **New Urban Parks**: 5 new parks in heat-prone areas
    - **Street Trees**: 10,000 trees along major corridors
    - **Green Roofs**: Incentives for building owners
    - **Community Gardens**: Transform vacant lots
    - **River Restoration**: Enhance natural cooling
    - **Cool Pavements**: Reflective materials in hot zones
    """)

st.markdown("---")

# Detailed recommendations map
st.subheader("🗺️ Proposed Green Infrastructure Locations")

m_proposed = folium.Map(
    location=[35.5608, 45.4347],
    zoom_start=12,
    tiles='OpenStreetMap'
)

# TODO: Add proposed park locations from your analysis
# Example proposed parks
proposed_parks = [
    {"name": "Proposed Park #1 - Downtown", "lat": 35.5658, "lon": 45.4397, "size": "3 hectares"},
    {"name": "Proposed Park #2 - North", "lat": 35.5758, "lon": 45.4447, "size": "5 hectares"},
    {"name": "Proposed Park #3 - East", "lat": 35.5708, "lon": 45.4547, "size": "2 hectares"},
]

for park in proposed_parks:
    folium.Marker(
        location=[park["lat"], park["lon"]],
        popup=f"<b>{park['name']}</b><br>Size: {park['size']}",
        icon=folium.Icon(color='lightgreen', icon='plus', prefix='fa')
    ).add_to(m_proposed)

st_folium(m_proposed, width=1400, height=400)

# Data requirements
st.markdown("---")
st.info("""
### 📥 Data Files Needed for This Page

Please prepare and save in `/data` folder:
- `temperature_lst.csv` - Land surface temperature data (lat, lon, date, temperature)
- `ndvi_values.csv` - NDVI values (lat, lon, date, ndvi)
- `green_spaces.geojson` - Existing parks and vegetation polygons
- `heat_islands.geojson` - Identified heat island zones
- `neighborhood_greenspace.csv` - Greenspace statistics per neighborhood
""")
