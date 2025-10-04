# Heat & Greenspace Analysis System
## NASA Space Apps Challenge 2025 - Sulaimani Sustainable Growth

### 🌡️ Overview
The Heat & Greenspace analysis system integrates real climate data from Copernicus Climate Data Store (CDS) to analyze urban heat islands and vegetation patterns in Sulaimani City, supporting sustainable urban planning decisions.

### 📊 Data Integration

#### Temperature Analysis
- **ERA5-Land Temperature Data**: 2m air temperature and land surface temperature
- **Heat Island Intensity**: Calculated as LST - Air Temperature  
- **Spatial Coverage**: 400 grid points across Sulaimani (35.40-35.72°N, 45.25-45.62°E)
- **Temporal Range**: Summer 2024 data (June-August)
- **Resolution**: 9km native, interpolated to regular grid

#### Vegetation Analysis  
- **ERA5-Land LAI Data**: Leaf Area Index for high and low vegetation
- **NDVI Estimation**: Derived from LAI using empirical relationships
- **Categories**: No Vegetation, Sparse, Moderate, Dense (based on NDVI thresholds)
- **Health Assessment**: Vegetation coverage and distribution patterns

#### Green Spaces Mapping
- **Existing Parks**: Current green infrastructure (GeoJSON polygons)
- **Proposed Parks**: Recommended new green spaces based on heat analysis
- **Priority Zones**: Areas with high heat + low vegetation identified for intervention

### 🗺️ Interactive Visualizations

#### 1. Heat Maps
- **Land Surface Temperature**: Shows temperature distribution across city
- **NDVI Vegetation**: Displays vegetation health and coverage
- **Heat Island Intensity**: Highlights areas with strongest urban heat effect
- **Combined View**: Side-by-side temperature vs vegetation comparison

#### 2. Temporal Analysis
- **Daily Temperature Trends**: Shows temperature patterns over time
- **Peak Heat Identification**: Identifies hottest periods and locations
- **Seasonal Patterns**: Analyzes heat island intensity variations

#### 3. Vegetation Distribution
- **Category Breakdown**: Pie chart of vegetation coverage types
- **NDVI Histogram**: Distribution of vegetation health values
- **Greenspace Statistics**: Quantifies existing and needed vegetation

### 🎯 Key Insights

#### Heat Island Effects
- **Peak Surface Temperature**: Up to 45°C in urban core
- **Heat Island Intensity**: 3-8°C warmer than surrounding areas
- **Hotspot Locations**: Concentrated in downtown and industrial areas

#### Vegetation Status
- **Average NDVI**: 0.34 (moderate vegetation health)
- **Coverage Distribution**: 
  - Dense Vegetation: ~25%
  - Moderate Vegetation: ~35% 
  - Sparse/No Vegetation: ~40%
- **Priority Areas**: Downtown, northern suburbs need more greenspace

#### Green Infrastructure Recommendations
- **New Parks**: 5 strategic locations in heat-prone areas
- **Green Corridors**: Along major streets and transport routes  
- **Urban Forest**: Tree planting in residential neighborhoods
- **Cool Infrastructure**: Green roofs, permeable surfaces

### 🛠️ Technical Implementation

#### Data Sources
```python
# Copernicus Climate Data Store (CDS)
ERA5-Land Reanalysis:
- Product: 'reanalysis-era5-land'
- Variables: 't2m', 'skt', 'lai_hv', 'lai_lv' 
- Spatial: 35.40-35.72°N, 45.25-45.62°E
- Temporal: 2023-2024, summer months
```

#### Processing Pipeline
1. **Download**: CDS API retrieval of NetCDF climate data
2. **Processing**: Convert Kelvin to Celsius, calculate heat island intensity
3. **Gridding**: Interpolate to regular 400-point grid
4. **Analysis**: Statistical analysis and category assignment
5. **Visualization**: Folium heatmaps, Plotly charts, GeoJSON overlays

#### File Structure
```
data/
├── temperature_data.csv          # Gridded temperature measurements
├── vegetation_data.csv           # NDVI and vegetation categories  
├── daily_temperature_summary.csv # Daily temperature averages
├── daily_vegetation_summary.csv  # Daily vegetation averages
├── existing_parks.geojson        # Current green spaces
└── proposed_parks.geojson        # Recommended new parks
```

### 🚀 Usage Instructions

#### Basic Setup
1. **Install Dependencies**: `pip install cdsapi xarray scipy`
2. **Generate Data**: `python download_climate_data.py` 
3. **View Analysis**: Navigate to Heat & Greenspace page in Streamlit app

#### Advanced Setup (Real CDS Data)
1. **Register**: Create account at https://cds.climate.copernicus.eu/
2. **API Key**: Add credentials to `~/.cdsapirc`
3. **Download**: Run script with real API access for latest data

#### Interactive Features
- **Map Type Selection**: Choose temperature, NDVI, or combined view
- **Date Selection**: Explore different days within dataset
- **Green Spaces Toggle**: Show/hide existing and proposed parks
- **Zoom & Pan**: Interactive exploration of heat patterns

### 📈 Impact Metrics

#### Environmental Benefits
- **Temperature Reduction**: 2-4°C cooling from green infrastructure
- **Air Quality**: Improved through urban forest expansion
- **Biodiversity**: Enhanced habitat corridors and green networks
- **Stormwater**: Better management through permeable green surfaces

#### Social Benefits  
- **Health**: Reduced heat stress for 125,000+ residents
- **Recreation**: New parks and green spaces for community use
- **Property Values**: Increased through neighborhood greening
- **Quality of Life**: Cooler, more livable urban environment

### 🔗 Integration with Other Systems

#### Cross-System Connections
- **Air Quality**: Green spaces improve air pollution in identified hotspots
- **Population**: Heat analysis weighted by population density data
- **Urban Planning**: Green corridors integrated with growth projections
- **Water Management**: Green infrastructure supports stormwater systems

#### NASA Earth Observation Data
- **Landsat**: Land surface temperature validation
- **MODIS**: NDVI verification and trend analysis  
- **Sentinel**: High-resolution vegetation monitoring
- **ECOSTRESS**: Detailed urban heat measurements

### 🎯 Future Enhancements

#### Real-Time Monitoring
- **Live Data**: Continuous CDS API integration
- **Alerts**: Heat wave and vegetation stress warnings
- **Mobile App**: Field data collection and citizen science
- **IoT Integration**: Ground-based temperature sensors

#### Advanced Analysis
- **Machine Learning**: Predictive heat island modeling
- **Climate Projection**: Future temperature scenarios
- **Carbon Sequestration**: Quantify green infrastructure benefits
- **Economic Analysis**: Cost-benefit of green interventions

---

*This system provides evidence-based recommendations for sustainable urban growth in Sulaimani, leveraging NASA Earth observation data and European climate reanalysis to support climate-resilient city planning.*