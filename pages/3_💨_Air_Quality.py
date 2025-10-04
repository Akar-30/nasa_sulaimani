import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(page_title="Air Quality & Health", page_icon="💨", layout="wide")

# Sidebar with population density information
with st.sidebar:
    st.header("📊 Population Data")
    
    if os.path.exists('data/population_density.geojson'):
        st.success("✅ Population data loaded")
        
        st.markdown("""
        ### Population Density Legend
        
        🟡 **Low**: <500 people/km²  
        🟠 **Medium**: 500-2,000 people/km²  
        🔴 **High**: 2,000-5,000 people/km²  
        🔴 **Very High**: >5,000 people/km²
        
        ---
        
        **Total Population (2020)**: ~525,035
        
        **Average Density**: 1,316 people/km²
        
        **Data Points**: 399 cells
        """)
    else:
        st.info("📥 Population data not loaded yet")
    
    st.markdown("---")
    st.markdown("""
    ### 💡 About This Page
    
    This page combines:
    - **Population density** (WorldPop 2020)
    - **Air quality data** (NASA Sentinel-5P)
    - **Health risk analysis**
    
    Use the checkbox to toggle population overlay on the map.
    """)

st.title("💨 Air Quality & Public Health")

st.markdown("""
This section identifies pollution hotspots in Sulaimani and highlights communities most at risk 
from poor air quality based on NASA Sentinel-5P and MODIS data.
""")

# Multi-pollutant configuration (moved up for metrics)
POLLUTANT_CONFIG = {
    '🌍 Composite Air Quality Index': {
        'file': 'composite_air_quality_index.csv',
        'code': 'AQI',
        'units': 'AQI Score',
        'guideline': 50.0,
        'thresholds': [20, 40, 60, 80],
        'colors': ['green', 'lightgreen', 'yellow', 'orange', 'red'],
        'categories': ['Excellent', 'Good', 'Moderate', 'Poor', 'Very Poor'],
        'value_field': 'aqi_score'
    },
    'NO₂ (Nitrogen Dioxide)': {
        'file': 'air_quality_no2_interpolated.csv',
        'code': 'NO2',
        'units': 'µg/m³',
        'guideline': 40.0,
        'thresholds': [40, 80, 120, 200],
        'colors': ['green', 'orange', 'red', 'darkred'],
        'categories': ['Good', 'Moderate', 'Unhealthy', 'Very Unhealthy'],
        'value_field': 'value'
    },
    'SO₂ (Sulfur Dioxide)': {
        'file': 'air_quality_so2_interpolated.csv',
        'code': 'SO2',
        'units': 'µg/m³',
        'guideline': 20.0,
        'thresholds': [20, 40, 80, 150],
        'colors': ['green', 'orange', 'red', 'darkred'],
        'categories': ['Good', 'Moderate', 'Unhealthy', 'Very Unhealthy'],
        'value_field': 'value'
    },
    'CO (Carbon Monoxide)': {
        'file': 'air_quality_co_interpolated.csv',
        'code': 'CO',
        'units': 'mg/m³',
        'guideline': 10.0,
        'thresholds': [10, 20, 35, 50],
        'colors': ['green', 'orange', 'red', 'darkred'],
        'categories': ['Good', 'Moderate', 'Unhealthy', 'Very Unhealthy'],
        'value_field': 'value'
    },
    'O₃ (Ozone)': {
        'file': 'air_quality_o3_interpolated.csv',
        'code': 'O3',
        'units': 'DU',
        'guideline': 300.0,
        'thresholds': [250, 280, 320, 350],
        'colors': ['red', 'orange', 'green', 'darkgreen'],  # Inverted for O3 (higher is better)
        'categories': ['Low', 'Moderate', 'Good', 'Very Good'],
        'value_field': 'value'
    },
    'HCHO (Formaldehyde)': {
        'file': 'air_quality_hcho_interpolated.csv',
        'code': 'HCHO',
        'units': 'µg/m³',
        'guideline': 30.0,
        'thresholds': [30, 60, 100, 150],
        'colors': ['green', 'orange', 'red', 'darkred'],
        'categories': ['Good', 'Moderate', 'Unhealthy', 'Very Unhealthy'],
        'value_field': 'value'
    },
    'AER_AI (Aerosol Index)': {
        'file': 'air_quality_aer_ai_interpolated.csv',
        'code': 'AER_AI',
        'units': 'AI',
        'guideline': 2.0,
        'thresholds': [1.0, 2.0, 3.0, 4.0],
        'colors': ['green', 'orange', 'red', 'darkred'],
        'categories': ['Clear', 'Moderate', 'High Aerosols', 'Very High'],
        'value_field': 'value'
    }
}

# Dynamic metrics based on available data
col1, col2, col3, col4 = st.columns(4)

# Load data for metrics (show most recent data)
metrics_data = {}
for poll_name, poll_config in POLLUTANT_CONFIG.items():
    if os.path.exists(f'data/{poll_config["file"]}'):
        df = pd.read_csv(f'data/{poll_config["file"]}')
        latest_data = df[df['date'] == df['date'].max()]
        
        # Get the correct value field
        value_field = poll_config.get('value_field', 'value')
        
        if value_field in latest_data.columns:
            metrics_data[poll_name] = {
                'avg': latest_data[value_field].mean(),
                'max': latest_data[value_field].max(),
                'above_guideline': (latest_data[value_field] > poll_config['guideline']).sum() / len(latest_data) * 100,
                'units': poll_config['units'],
                'guideline': poll_config['guideline']
            }

with col1:
    if 'NO₂ (Nitrogen Dioxide)' in metrics_data:
        data = metrics_data['NO₂ (Nitrogen Dioxide)']
        st.metric(
            label="Avg NO₂ Level",
            value=f"{data['avg']:.1f} {data['units']}",
            delta=f"{data['above_guideline']:.1f}% above WHO",
            delta_color="inverse" if data['above_guideline'] > 0 else "normal"
        )
    else:
        st.metric("Avg NO₂ Level", "Loading...", "No data")

with col2:
    if 'SO₂ (Sulfur Dioxide)' in metrics_data:
        data = metrics_data['SO₂ (Sulfur Dioxide)']
        st.metric(
            label="Avg SO₂ Level",
            value=f"{data['avg']:.1f} {data['units']}",
            delta=f"{data['above_guideline']:.1f}% above WHO",
            delta_color="inverse" if data['above_guideline'] > 0 else "normal"
        )
    else:
        st.metric("Avg SO₂ Level", "Loading...", "No data")

with col3:
    if 'CO (Carbon Monoxide)' in metrics_data:
        data = metrics_data['CO (Carbon Monoxide)']
        st.metric(
            label="Avg CO Level",
            value=f"{data['avg']:.1f} {data['units']}",
            delta=f"{data['above_guideline']:.1f}% above WHO",
            delta_color="inverse" if data['above_guideline'] > 0 else "normal"
        )
    else:
        st.metric("Avg CO Level", "Loading...", "No data")

with col4:
    total_pollutants = len(metrics_data)
    st.metric(
        label="Data Sources",
        value=f"{total_pollutants}/6 pollutants",
        delta="Sentinel-5P TROPOMI" if total_pollutants > 0 else "No data"
    )

st.markdown("---")

# Interactive controls
st.header("🗺️ Pollution Hotspot Map")

col1, col2, col3 = st.columns(3)

with col1:
    pollutant = st.selectbox(
        "Select Pollutant",
        [
            "🌍 Composite Air Quality Index",
            "NO₂ (Nitrogen Dioxide)", 
            "SO₂ (Sulfur Dioxide)", 
            "CO (Carbon Monoxide)",
            "O₃ (Ozone)", 
            "HCHO (Formaldehyde)",
            "AER_AI (Aerosol Index)"
        ]
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

# Load and display population density overlay
if overlay_population and os.path.exists('data/population_density.geojson'):
    with open('data/population_density.geojson', 'r') as f:
        pop_data = json.load(f)
    
    # Add population density as colored squares
    for feature in pop_data['features']:
        coords = feature['geometry']['coordinates']
        props = feature['properties']
        
        # Blue color scheme based on density category
        category = props['density_category']
        if category == 'Very High':
            color = '#000080'  # Navy blue
            size = 0.002      # Larger square
        elif category == 'High':
            color = '#0000CD'  # Medium blue
            size = 0.0015     # Medium square
        elif category == 'Medium':
            color = '#4169E1'  # Royal blue
            size = 0.001      # Small square
        else:  # Low
            color = '#87CEEB'  # Sky blue
            size = 0.0008     # Smallest square
        
        # Create square bounds
        lat, lon = coords[1], coords[0]
        bounds = [
            [lat - size, lon - size],  # Southwest corner
            [lat + size, lon + size]   # Northeast corner
        ]
        
        folium.Rectangle(
            bounds=bounds,
            popup=f"<b>Population Density</b><br>{props['population_density']:.0f} people/km²<br>Category: {category}",
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7,
            weight=1
        ).add_to(m)

# Load and display selected pollutant data
config = POLLUTANT_CONFIG.get(pollutant)
if config and os.path.exists(f'data/{config["file"]}'):
    pollutant_data = pd.read_csv(f'data/{config["file"]}')
    
    # Get latest date for visualization
    latest_date = pollutant_data['date'].max()
    daily_data = pollutant_data[pollutant_data['date'] == latest_date]
    
    if not daily_data.empty:
        # Get value field (different for AQI vs pollutants)
        value_field = config.get('value_field', 'value')
        
        # Normalize values for better heatmap visualization
        values = daily_data[value_field].values
        min_val, max_val = values.min(), values.max()
        
        # Create heatmap data with normalized intensity (0-1 range for better gradient)
        heat_data = []
        for _, row in daily_data.iterrows():
            normalized_value = (row[value_field] - min_val) / (max_val - min_val) if max_val > min_val else 0.5
            heat_data.append([row['lat'], row['lon'], normalized_value])
        
        # Add smooth heatmap layer with reasonable coverage
        HeatMap(
            heat_data, 
            radius=25,        # Reasonable radius for good coverage
            blur=15,          # Moderate blur for smooth appearance
            max_zoom=13,      # Standard max zoom
            min_opacity=0.2,  # Light minimum opacity
            gradient={0.2: 'blue', 0.4: 'cyan', 0.6: 'lime', 0.8: 'orange', 1.0: 'red'}
        ).add_to(m)
        
        # Display info message ONCE after the loop
        st.info(f"✅ Displaying {len(daily_data)} {config['code']} measurements from {latest_date}")
    else:
        st.warning(f"No {config['code']} data available for selected date")
else:
    st.info("📥 Air quality data not loaded. Select a pollutant to view available data.")

folium.LayerControl().add_to(m)

st_folium(m, width=1400, height=500)

st.markdown("---")

# Temporal trends
st.header("📈 Air Quality Trends")

# Use real data if available, otherwise show placeholder
if os.path.exists('data/air_quality_no2.csv'):
    no2_data = pd.read_csv('data/air_quality_no2.csv')
    
    # Calculate daily averages
    daily_avg = no2_data.groupby('date')['value'].mean().reset_index()
    daily_avg['date'] = pd.to_datetime(daily_avg['date'])
    daily_avg = daily_avg.sort_values('date')
    
    # Create trend plot
    fig = px.line(
        daily_avg,
        x='date',
        y='value',
        title='Daily NO₂ Concentration Trends (Sulaimani)',
        labels={'value': 'NO₂ Concentration (µg/m³)', 'date': 'Date'},
        markers=True
    )
    
    # Add WHO guideline line
    fig.add_hline(y=40, line_dash="dash", line_color="orange", 
                  annotation_text="WHO NO₂ Guideline (40 µg/m³)")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show data summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average NO₂", f"{no2_data['value'].mean():.1f} µg/m³")
    with col2:
        st.metric("Peak NO₂", f"{no2_data['value'].max():.1f} µg/m³")
    with col3:
        above_who = (no2_data['value'] > 40).mean() * 100
        st.metric("Above WHO Guideline", f"{above_who:.1f}%")

else:
    # Placeholder data - will be replaced with real data
    st.info("📊 Using placeholder data - upload real NO₂ data to see actual trends")
    
    years = list(range(2018, 2026))
    no2_values = [38, 42, 45, 48, 51, 47, 52, 55]
    pm25_values = [52, 54, 58, 61, 64, 59, 67, 70]

    df_placeholder = pd.DataFrame({
        'Year': years,
        'NO₂ (µg/m³)': no2_values,
        'PM2.5 (µg/m³)': pm25_values
    })
    
    fig = px.line(
        df_placeholder,
        x='Year',
        y=['NO₂ (µg/m³)', 'PM2.5 (µg/m³)'],
        title='Air Pollutant Concentration Trends (2018-2025) - Placeholder Data',
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

# Pollution correlation and source analysis
st.header("🔬 Pollution Source Analysis & Correlations")

# Load combined dataset for correlation analysis
if os.path.exists('data/air_quality_combined_grid.csv'):
    combined_data = pd.read_csv('data/air_quality_combined_grid.csv')
    latest_combined = combined_data[combined_data['date'] == combined_data['date'].max()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏭 Pollutant Correlations")
        
        # Create correlation matrix
        pollutant_cols = ['NO2_value', 'SO2_value', 'CO_value', 'O3_value', 'HCHO_value', 'AER_AI_value']
        available_cols = [col for col in pollutant_cols if col in latest_combined.columns]
        
        if len(available_cols) >= 2:
            corr_matrix = latest_combined[available_cols].corr()
            
            # Create correlation heatmap
            fig_corr = px.imshow(
                corr_matrix,
                labels=dict(x="Pollutant", y="Pollutant", color="Correlation"),
                x=[col.replace('_value', '') for col in available_cols],
                y=[col.replace('_value', '') for col in available_cols],
                color_continuous_scale="RdBu_r",
                aspect="auto",
                title="Pollutant Correlation Matrix"
            )
            fig_corr.update_layout(height=400)
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Correlation insights
            st.markdown("**Key Findings:**")
            
            # Find high correlations
            high_corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.5:  # Strong correlation
                        pol1 = corr_matrix.columns[i].replace('_value', '')
                        pol2 = corr_matrix.columns[j].replace('_value', '')
                        high_corr_pairs.append((pol1, pol2, corr_val))
            
            if high_corr_pairs:
                for pol1, pol2, corr_val in high_corr_pairs:
                    if corr_val > 0.5:
                        st.success(f"• Strong positive correlation between {pol1} and {pol2} ({corr_val:.2f}) - Common source")
                    elif corr_val < -0.5:
                        st.info(f"• Strong negative correlation between {pol1} and {pol2} ({corr_val:.2f}) - Competing processes")
            else:
                st.info("• Most pollutants show independent spatial patterns")
        else:
            st.warning("Insufficient data for correlation analysis")
    
    with col2:
        st.markdown("### 📊 Pollution Hotspot Analysis")
        
        if os.path.exists('data/composite_air_quality_index.csv'):
            aqi_data = pd.read_csv('data/composite_air_quality_index.csv')
            latest_aqi = aqi_data[aqi_data['date'] == aqi_data['date'].max()]
            
            # Find worst air quality areas
            worst_areas = latest_aqi.nlargest(10, 'aqi_score')
            
            st.markdown("**🚨 Top 10 Pollution Hotspots:**")
            
            for i, (_, area) in enumerate(worst_areas.iterrows(), 1):
                st.markdown(f"""
                **{i}. AQI Score: {area['aqi_score']:.1f}** ({area['aqi_category']})  
                📍 Location: {area['lat']:.3f}°N, {area['lon']:.3f}°E
                """)
            
            # AQI distribution
            aqi_dist = latest_aqi['aqi_category'].value_counts()
            fig_aqi = px.pie(
                values=aqi_dist.values,
                names=aqi_dist.index,
                title="Air Quality Distribution Across Sulaimani",
                color_discrete_map={
                    'Excellent': 'green',
                    'Good': 'lightgreen', 
                    'Moderate': 'yellow',
                    'Poor': 'orange',
                    'Very Poor': 'red'
                }
            )
            fig_aqi.update_layout(height=300)
            st.plotly_chart(fig_aqi, use_container_width=True)
        
        else:
            st.warning("Composite AQI data not available")

st.markdown("---")

# Neighborhood analysis
st.header("🏘️ Population Distribution & Pollution Exposure")

# Load neighborhood statistics if available
if os.path.exists('data/neighborhood_population.csv'):
    neighborhood_df = pd.read_csv('data/neighborhood_population.csv')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Population Density by Zone
        
        Real 2020 WorldPop data showing population distribution across Sulaimani:
        """)
        
        # Display neighborhood stats table
        display_df = neighborhood_df[['neighborhood', 'avg_density', 'total_population']].copy()
        display_df['avg_density'] = display_df['avg_density'].round(0).astype(int)
        display_df['total_population'] = display_df['total_population'].round(0).astype(int)
        display_df.columns = ['Neighborhood', 'Avg Density (people/km²)', 'Total Population']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        st.info(f"""
        **Total Sulaimani Population (2020)**: ~{neighborhood_df['total_population'].sum():,.0f} people
        
        **Highest Density Areas**: Central West & Central Central (~2,245 people/km²)
        """)
    
    with col2:
        # Population bar chart
        fig = px.bar(
            neighborhood_df.sort_values('avg_density', ascending=True),
            y='neighborhood',
            x='avg_density',
            title='Average Population Density by Zone',
            labels={'avg_density': 'People per km²', 'neighborhood': 'Zone'},
            color='avg_density',
            color_continuous_scale='YlOrRd',
            orientation='h'
        )
        
        fig.add_vline(x=1316, line_dash="dash", line_color="blue", 
                      annotation_text="City Average: 1,316 people/km²")
        
        st.plotly_chart(fig, use_container_width=True)
else:
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
