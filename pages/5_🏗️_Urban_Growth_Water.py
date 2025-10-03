import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Urban Growth & Water", page_icon="🏗️", layout="wide")

st.title("🏗️ Urban Growth & Water Resources")

st.markdown("""
This section analyzes urban expansion patterns and water availability to ensure sustainable 
growth that doesn't outpace infrastructure and natural resources.
""")

# Split into two main sections
tab1, tab2 = st.tabs(["🏙️ Urban Growth", "💧 Water Resources"])

with tab1:
    st.header("Urban Expansion Analysis")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Urban Area Growth",
            value="+45%",
            delta="Since 2005"
        )
    
    with col2:
        st.metric(
            label="Population Growth",
            value="+40%",
            delta="~300,000 added"
        )
    
    with col3:
        st.metric(
            label="Fastest Growing Zone",
            value="Southwest",
            delta="+120% expansion"
        )
    
    with col4:
        st.metric(
            label="Agricultural Land Lost",
            value="1,200 ha",
            delta="Converted to urban",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Timeline visualization
    st.subheader("📅 Urban Expansion Timeline")
    
    year_selector = st.select_slider(
        "Select Year to View Urban Extent",
        options=[2005, 2010, 2015, 2020, 2025],
        value=2025
    )
    
    # Create map
    m_growth = folium.Map(
        location=[35.5608, 45.4347],
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Add satellite layer
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite'
    ).add_to(m_growth)
    
    # TODO: Load and display urban extent GeoJSON based on selected year
    # if os.path.exists(f'data/urban_extent_{year_selector}.geojson'):
    #     folium.GeoJson(f'data/urban_extent_{year_selector}.geojson', 
    #                    style_function=lambda x: {'fillColor': 'red', 'fillOpacity': 0.3}).add_to(m_growth)
    
    folium.LayerControl().add_to(m_growth)
    
    st_folium(m_growth, width=1400, height=500)
    
    st.info(f"""
    **Viewing urban extent for {year_selector}**
    
    📥 Provide these files: `urban_extent_2005.geojson`, `urban_extent_2010.geojson`, 
    `urban_extent_2015.geojson`, `urban_extent_2020.geojson`, `urban_extent_2025.geojson`
    """)
    
    st.markdown("---")
    
    # Growth by zone
    st.subheader("📊 Growth by Zone (2005-2025)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Placeholder data
        zones = ['Southwest', 'Northwest', 'Northeast', 'Southeast', 'City Center']
        growth_pct = [120, 65, 55, 48, 15]
        
        fig = px.bar(
            x=zones,
            y=growth_pct,
            title='Urban Area Expansion by Zone',
            labels={'x': 'Zone', 'y': 'Growth (%)'},
            color=growth_pct,
            color_continuous_scale='Reds'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Population density
        pop_density = [8500, 6200, 5800, 4500, 12000]
        
        fig = px.bar(
            x=zones,
            y=pop_density,
            title='Population Density by Zone (per km²)',
            labels={'x': 'Zone', 'y': 'People per km²'},
            color=pop_density,
            color_continuous_scale='Blues'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Infrastructure assessment
    st.subheader("🏗️ Infrastructure Gap Analysis")
    
    st.markdown("""
    Rapidly expanding areas often lack adequate infrastructure. Here's where attention is needed:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning("""
        ### ⚠️ Infrastructure Deficits
        
        **Southwest Suburbs** (Fastest Growing)
        - ❌ Limited water infrastructure
        - ❌ No nearby parks or green spaces
        - ❌ Poor road connectivity
        - ❌ Limited public services
        
        **Northwest Expansion**
        - ❌ Informal settlements
        - ❌ Inadequate sewage systems
        - ❌ Limited electricity capacity
        """)
    
    with col2:
        st.success("""
        ### ✅ Recommended Actions
        
        - **Water Network Expansion**: Priority in SW zone
        - **Green Space Planning**: 3-5 new parks needed
        - **Road Infrastructure**: Connect new suburbs
        - **Zoning Regulations**: Prevent sprawl into high-risk areas
        - **Mixed-Use Development**: Reduce commute distances
        - **Public Transport**: Extend to new areas
        """)

with tab2:
    st.header("💧 Water Resources & Stress")
    
    # Water metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Groundwater Depletion",
            value="-2.5 cm/year",
            delta="Declining trend",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="Annual Precipitation",
            value="520 mm",
            delta="-15% vs 2000-2010",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Water Stress Level",
            value="Medium-High",
            delta="Increasing"
        )
    
    with col4:
        st.metric(
            label="Population at Risk",
            value="~65,000",
            delta="In water-scarce zones"
        )
    
    st.markdown("---")
    
    # Water stress map
    st.subheader("🗺️ Water Stress Zones")
    
    m_water = folium.Map(
        location=[35.5608, 45.4347],
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # TODO: Add water stress zones from your data
    # Example zones (will be replaced with GeoJSON)
    water_stress_zones = [
        {"name": "Western Suburbs", "lat": 35.5408, "lon": 45.4147, "level": "High"},
        {"name": "Southwest Expansion", "lat": 35.5308, "lon": 45.4047, "level": "Very High"},
    ]
    
    for zone in water_stress_zones:
        color = "darkred" if zone["level"] == "Very High" else "orange"
        folium.CircleMarker(
            location=[zone["lat"], zone["lon"]],
            radius=30,
            popup=f"<b>{zone['name']}</b><br>Water Stress: {zone['level']}",
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.3
        ).add_to(m_water)
    
    st_folium(m_water, width=1400, height=450)
    
    st.info("""
    📥 Provide `water_stress_zones.geojson` with polygons showing areas of different water stress levels
    """)
    
    st.markdown("---")
    
    # Water availability trends
    st.subheader("📉 Water Availability Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Groundwater trend (GRACE data placeholder)
        years_water = list(range(2003, 2026))
        groundwater = [0] + [-0.5, -1.2, -2.1, -3.5, -4.8, -6.2, -7.8, -9.5, -11.2, 
                             -13.0, -14.5, -16.2, -18.0, -19.5, -21.2, -23.0, -24.5,
                             -26.2, -28.0, -29.8, -31.5, -33.2]
        
        fig = px.line(
            x=years_water,
            y=groundwater,
            title='Groundwater Storage Change (GRACE Data)',
            labels={'x': 'Year', 'y': 'Change in cm of water equivalent'},
            markers=True
        )
        
        fig.update_traces(line_color='blue')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Precipitation trend (IMERG data placeholder)
        years_precip = list(range(2005, 2026))
        precip = [580, 550, 520, 610, 490, 530, 505, 480, 520, 495, 
                  470, 510, 485, 460, 500, 475, 450, 520, 490, 510, 520]
        
        fig = px.bar(
            x=years_precip,
            y=precip,
            title='Annual Precipitation Trend (mm)',
            labels={'x': 'Year', 'y': 'Precipitation (mm)'},
            color=precip,
            color_continuous_scale='Blues'
        )
        
        fig.add_hline(y=550, line_dash="dash", line_color="blue", 
                      annotation_text="Long-term Average")
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Combined analysis
    st.subheader("🔗 Urban Growth + Water Stress Overlay")
    
    st.markdown("""
    This critical analysis overlays rapidly growing areas with water stress zones to identify 
    unsustainable expansion patterns.
    """)
    
    m_combined = folium.Map(
        location=[35.5608, 45.4347],
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # TODO: Overlay urban growth with water stress
    
    st_folium(m_combined, width=1400, height=450)
    
    st.error("""
    ### ⚠️ Critical Finding
    
    **Western neighborhoods are expanding into areas with declining groundwater**, indicating 
    urgent need for sustainable water planning. New developments in these zones should include:
    - Rainwater harvesting systems
    - Water-efficient infrastructure
    - Green infrastructure to reduce runoff
    - Alternative water sources (treated wastewater for irrigation)
    """)

# Data requirements
st.markdown("---")
st.info("""
### 📥 Data Files Needed for This Page

Please prepare and save in `/data` folder:

**Urban Growth:**
- `urban_extent_2005.geojson`, `urban_extent_2010.geojson`, etc. - Urban boundaries by year
- `population_growth.csv` - Population data by year and zone
- `zone_statistics.csv` - Growth metrics per zone

**Water Resources:**
- `groundwater_trend.csv` - GRACE groundwater data (year, value)
- `precipitation.csv` - IMERG precipitation data (year, value)
- `water_stress_zones.geojson` - Polygon boundaries with stress levels
""")
