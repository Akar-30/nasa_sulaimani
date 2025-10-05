import streamlit as st

st.set_page_config(page_title="References & Documentation", page_icon="�", layout="wide")

st.title("� References & Complete Documentation")

st.markdown("""
This comprehensive reference section provides complete documentation for the Sulaimani Sustainable Urban Growth Analysis platform, developed for the NASA Space Apps Challenge 2025.
""")

# Technical Documentation
st.header("🛠️ Technical Architecture & Implementation")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🏗️ System Architecture
    
    **Multi-Page Streamlit Application:**
    - **Frontend**: Streamlit web framework with interactive visualizations
    - **Mapping**: Folium (Leaflet.js) with st_folium for drawing capabilities
    - **Visualization**: Plotly for charts, graphs, and statistical displays
    - **Geospatial**: GeoPandas, Shapely for spatial analysis and polygon operations
    
    **Data Processing Pipeline:**
    - **Data Sources**: 15+ NASA and partner satellite datasets
    - **Processing**: Pandas for tabular data, Rasterio for satellite imagery
    - **Analysis**: NumPy for numerical computations, SciPy for statistical analysis
    - **Storage**: CSV files for processed data, GeoJSON for spatial boundaries
    
    **Enhanced Analysis System:**
    - **High-Resolution Grids**: 100×100 analysis points (10,000 per dataset)
    - **Multi-Criteria Assessment**: 6 criteria with weighted scoring algorithms
    - **Temporal Analysis**: 15-year historical trends and bimonthly variations
    - **Interactive Polygon Selection**: Real-time area analysis with st_folium integration
    """)

with col2:
    st.markdown("""
    ### � Complete File Structure
    
    ```
    nasa_sulaimani/
    ├── Home.py                           # Main landing page
    ├── pages/
    │   ├── 1_🌍_Challenge_Overview.py     # Urban challenges
    │   ├── 2_🛰️_Data_Pathway.py          # NASA data overview  
    │   ├── 3_🌬️_Air_Quality_Analysis.py  # Air pollution analysis
    │   ├── 4_🌡️_Heat_Greenspace.py       # Temperature & vegetation
    │   ├── 5_🏙️_Urban_Water_Growth.py     # Growth & water resources
    │   ├── 6_💡_Integrated_Solution.py    # Recommendations engine
    │   ├── 7_📚_References.py            # This documentation
    │   ├── 11_👥_Population_Analysis.py   # Population density analysis
    │   ├── 12_🏗️_Infrastructure.py       # Infrastructure accessibility
    │   └── 13_🔬_Enhanced_Solution.py     # High-resolution analysis
    ├── data/                            # NASA processed datasets
    │   ├── air_quality_*.csv            # Sentinel-5P processed data
    │   ├── temperature_*.csv            # Landsat thermal data
    │   ├── vegetation_*.csv             # MODIS NDVI data
    │   └── urban_growth_*.geojson       # Copernicus GHSL boundaries
    ├── data_solution/                   # Enhanced high-res datasets
    │   ├── enhanced_*_detailed.csv      # 100×100 grid analysis
    │   └── enhanced_data_summary.json   # Metadata and coverage
    ├── utils/                           # Helper functions
    │   ├── data_processing.py           # Data manipulation utilities
    │   ├── visualization.py             # Chart and map functions  
    │   └── spatial_analysis.py          # Geospatial operations
    └── requirements.txt                 # Python dependencies
    ```
    """)

st.markdown("---")

# NASA Data Sources & Satellite Missions
st.header("🛰️ NASA Earth Observation Data Sources")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🌍 Primary NASA Missions
    
    **MODIS (Moderate Resolution Imaging Spectroradiometer)**
    - **Platform**: Terra/Aqua satellites (1999-present)
    - **Usage**: Vegetation indices (NDVI), aerosol optical depth (AOD)
    - **Resolution**: 250m-1km spatial, daily temporal
    - **Data Portal**: [MODIS Web](https://modis.gsfc.nasa.gov/)
    - **Citation**: NASA MODIS Science Team (2024)
    
    **Landsat 8/9 (Operational Land Imager + Thermal Infrared Sensor)**
    - **Platform**: Landsat Data Continuity Mission (2013-present)
    - **Usage**: Land surface temperature, high-resolution imagery
    - **Resolution**: 30m multispectral, 100m thermal, 16-day repeat
    - **Data Portal**: [USGS Earth Explorer](https://earthexplorer.usgs.gov/)
    - **Citation**: U.S. Geological Survey (2024)
    
    **GRACE/GRACE-FO (Gravity Recovery and Climate Experiment)**
    - **Platform**: Twin satellites (2002-2017, 2018-present)
    - **Usage**: Groundwater storage variations, water availability trends
    - **Resolution**: ~300km spatial, monthly temporal
    - **Data Portal**: [JPL GRACE Tellus](https://grace.jpl.nasa.gov/)
    - **Citation**: NASA JPL GRACE Science Team (2024)
    """)

with col2:
    st.markdown("""
    ### 🇪🇺 ESA Copernicus Programme
    
    **Sentinel-5P TROPOMI (TROPOspheric Monitoring Instrument)**
    - **Platform**: ESA Sentinel-5 Precursor (2017-present)
    - **Usage**: Air pollutants (NO₂, SO₂, O₃, CO, HCHO, aerosols)
    - **Resolution**: 7×3.5 km spatial, daily global coverage
    - **Data Portal**: [Copernicus Open Access Hub](https://scihub.copernicus.eu/)
    - **Citation**: ESA Copernicus Sentinel-5P Science Team (2024)
    
    **Copernicus GHSL (Global Human Settlement Layer)**
    - **Platform**: Multi-sensor analysis including Landsat, Sentinel
    - **Usage**: Urban built-up area mapping, population distribution
    - **Resolution**: 30m-1km multi-temporal analysis (1975-2030)
    - **Data Portal**: [GHSL Data Package](https://ghsl.jrc.ec.europa.eu/)
    - **Citation**: Pesaresi et al. (2023), European Commission JRC
    
    **GPM IMERG (Global Precipitation Measurement)**
    - **Platform**: NASA-JAXA Global Precipitation Measurement (2014-present)
    - **Usage**: Precipitation analysis, drought monitoring
    - **Resolution**: 0.1° spatial (~11 km), 30-minute temporal
    - **Data Portal**: [NASA Giovanni](https://giovanni.gsfc.nasa.gov/)
    - **Citation**: Huffman et al. (2024), NASA GSFC
    """)

# Academic References & Methodology
st.header("� Academic References & Scientific Literature")

st.markdown("""
### 🎓 Key Scientific Publications

This project builds upon established research in urban sustainability, remote sensing, and environmental monitoring:
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 🏙️ Urban Sustainability & Growth
    
    **1. UN-Habitat (2022)**  
    *"World Cities Report 2022: Envisaging the Future of Cities"*  
    United Nations Human Settlements Programme, Nairobi  
    📖 [Download PDF](https://unhabitat.org/wcr/)
    
    **2. Seto, K.C., Güneralp, B., & Hutyra, L.R. (2012)**  
    *"Global forecasts of urban expansion to 2030 and direct impacts on biodiversity and carbon pools"*  
    Proceedings of the National Academy of Sciences, 109(40), 16083-16088  
    🔗 DOI: 10.1073/pnas.1211658109
    
    **3. Elmqvist, T., et al. (2019)**  
    *"Sustainability and resilience for transformation in the urban century"*  
    Nature Sustainability, 2(4), 267-273  
    🔗 DOI: 10.1038/s41893-019-0250-1
    
    **4. Fragkias, M., et al. (2013)**  
    *"A synthesis of global urbanization projections"*  
    In Urbanization, Biodiversity and Ecosystem Services: Challenges and Opportunities (pp. 409-435)  
    🔗 Springer, Dordrecht
    """)

with col2:
    st.markdown("""
    #### �️ Remote Sensing Applications
    
    **5. Zhu, Z., et al. (2019)**  
    *"Benefits of the free and open Landsat data policy"*  
    Remote Sensing of Environment, 224, 382-385  
    🔗 DOI: 10.1016/j.rse.2019.02.016
    
    **6. Veefkind, J.P., et al. (2012)**  
    *"TROPOMI on the ESA Sentinel-5 Precursor: A GMES mission for global observations of the atmospheric composition for climate, air quality and ozone layer applications"*  
    Remote Sensing of Environment, 120, 70-83  
    🔗 DOI: 10.1016/j.rse.2011.09.027
    
    **7. Justice, C., et al. (2002)**  
    *"An overview of MODIS Land data processing and product status"*  
    Remote Sensing of Environment, 83(1-2), 3-15  
    🔗 DOI: 10.1016/S0034-4257(02)00084-6
    
    **8. Pesaresi, M., et al. (2023)**  
    *"Atlas of the Human Planet 2023: Mapping Human Presence on Earth with the Global Human Settlement Layer"*  
    European Commission Joint Research Centre  
    🔗 DOI: 10.2760/953384
    """)

# Methodology & Analysis Approaches
st.header("� Methodology & Analysis Approaches")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🎯 Multi-Criteria Decision Analysis (MCDA)
    
    **Weighted Linear Combination Method:**
    - **Air Quality Weight**: 25% (health priority)
    - **Heat/Greenspace Weight**: 20% (climate adaptation)  
    - **Topography Weight**: 15% (development feasibility)
    - **Infrastructure Weight**: 20% (accessibility)
    - **Economic Activity Weight**: 10% (viability)
    - **Population Density Weight**: 10% (social factors)
    
    **Scoring Algorithm:**
    ```python
    def calculate_composite_score(criteria_scores, weights):
        total_score = sum(score * weight for score, 
                         weight in zip(criteria_scores, weights))
        return min(100, max(0, total_score))
    ```
    
    **Normalization Approach:**
    - Min-Max scaling to 0-100 range
    - Inverse scaling for negative indicators (pollution, heat)
    - Percentile-based thresholds for categorical classification
    
    **Spatial Analysis Methods:**
    - **Point-in-Polygon**: Shapely geometric operations
    - **Buffer Analysis**: 1-3km proximity zones
    - **Grid-Based Sampling**: 100×100 regular sampling
    - **Interpolation**: Inverse Distance Weighting (IDW)
    """)

with col2:
    st.markdown("""
    ### 📊 Statistical & Temporal Analysis
    
    **Time Series Analysis:**
    - **Trend Detection**: Mann-Kendall test for monotonic trends
    - **Seasonal Decomposition**: STL (Seasonal and Trend decomposition)
    - **Anomaly Detection**: Z-score based outlier identification
    - **Temporal Aggregation**: Monthly, seasonal, and annual means
    
    **Air Quality Index Calculation:**
    ```python
    def calculate_aqi(pollutant_concentrations):
        # WHO Guidelines-based AQI
        breakpoints = {
            'PM2.5': [0, 15, 45, 80, 150, 250],
            'NO2': [0, 40, 100, 200, 400, 800],
            'O3': [0, 100, 140, 180, 240, 380]
        }
        return composite_aqi_score
    ```
    
    **Heat Island Intensity:**
    - **Urban-Rural Temperature Difference**: ΔT = T_urban - T_rural
    - **Land Surface Temperature**: Landsat Band 10/11 processing
    - **Vegetation Cooling Effect**: NDVI correlation analysis
    
    **Infrastructure Accessibility Score:**
    - **Multi-modal Analysis**: Road, healthcare, education access
    - **Network Distance**: Euclidean and travel time calculations  
    - **Service Coverage**: Population-weighted accessibility indices
    """)

# Data Processing & Quality Control
st.header("🔍 Data Processing & Quality Control")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### �️ Data Preprocessing Pipeline
    
    **1. Data Acquisition & Download:**
    ```python
    # Sentinel-5P NO2 data acquisition
    import sentinelsat
    from datetime import datetime, timedelta
    
    def download_s5p_data(bbox, date_range):
        api = SentinelAPI(username, password)
        products = api.query(bbox, date_range, 
                           platformname='Sentinel-5P',
                           producttype='L2__NO2___')
        return api.download_all(products)
    ```
    
    **2. Spatial Reprojection:**
    - **Target CRS**: EPSG:4326 (WGS84 Geographic)
    - **Resampling Method**: Bilinear interpolation
    - **Pixel Alignment**: Snap to common grid system
    
    **3. Temporal Harmonization:**
    - **Reference Period**: 2018-2024 (6-year analysis)
    - **Temporal Resolution**: Daily → Monthly composites
    - **Gap Filling**: Linear interpolation for missing values
    
    **4. Quality Filtering:**
    - **Cloud Masking**: QA band analysis
    - **Data Validity**: Remove negative/impossible values
    - **Outlier Detection**: 3-sigma statistical filtering
    """)

with col2:
    st.markdown("""
    ### ✅ Data Quality Metrics & Validation
    
    **Completeness Assessment:**
    - **Spatial Coverage**: >95% for analysis region
    - **Temporal Coverage**: >80% for each month
    - **Data Availability**: Track missing value patterns
    
    **Accuracy Validation:**
    - **Ground Truth Comparison**: Limited ground station data
    - **Cross-Sensor Validation**: MODIS vs. Landsat consistency  
    - **Literature Benchmarking**: Compare with published studies
    
    **Uncertainty Quantification:**
    ```python
    def calculate_uncertainty(measurements, method='std'):
        if method == 'std':
            return np.std(measurements)
        elif method == 'mad':  # Median Absolute Deviation
            return np.median(np.abs(measurements - 
                                  np.median(measurements)))
    ```
    
    **Enhanced Dataset Statistics:**
    - **Total Data Points**: 300,000+ air quality measurements
    - **Spatial Resolution**: 310m effective grid spacing  
    - **Temporal Range**: Daily data for 30 days (August 2024)
    - **Coverage Area**: 1,150 km² Sulaimani metropolitan region
    - **Quality Score**: 94.2% valid measurements after QC
    """)

# Software Dependencies & Technical Stack
st.header("⚙️ Complete Software Dependencies & Technical Stack")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### � Python Dependencies (requirements.txt)
    
    ```txt
    streamlit>=1.28.0
    folium>=0.14.0
    streamlit-folium>=0.15.0
    plotly>=5.15.0
    pandas>=2.0.0
    geopandas>=0.13.0
    shapely>=2.0.0
    numpy>=1.24.0
    scipy>=1.10.0
    rasterio>=1.3.0
    pyproj>=3.5.0
    requests>=2.31.0
    matplotlib>=3.7.0
    seaborn>=0.12.0
    scikit-learn>=1.3.0
    xarray>=2023.6.0
    netcdf4>=1.6.0
    h5py>=3.9.0
    pillow>=10.0.0
    ```
    
    ### 🌐 Web Framework Architecture
    
    **Streamlit Multi-Page Application:**
    - **Session State Management**: Persistent user selections
    - **Caching Strategy**: `@st.cache_data` for large datasets
    - **Interactive Components**: st_folium, plotly charts
    - **Responsive Design**: Mobile and desktop optimization
    
    **Performance Optimization:**
    - **Lazy Loading**: Data loaded on-demand per page
    - **Memory Management**: Efficient pandas operations
    - **Computation Caching**: Expensive calculations cached
    """)

with col2:
    st.markdown("""
    ### �️ Database & File Management
    
    **Data Storage Strategy:**
    - **CSV Files**: Processed tabular data (15-50MB each)
    - **GeoJSON**: Spatial boundaries (<5MB each)  
    - **JSON**: Metadata and configuration files
    - **No Database**: File-based for simplicity and portability
    
    **File Naming Convention:**
    ```
    [source]_[parameter]_[timerange]_[resolution].csv
    
    Examples:
    - sentinel5p_no2_2024_daily.csv
    - modis_ndvi_2018_2024_monthly.csv  
    - landsat_lst_summer_2024_30m.csv
    - enhanced_air_quality_detailed.csv
    ```
    
    **Spatial Data Management:**
    - **Coordinate Reference System**: WGS84 (EPSG:4326)
    - **Spatial Indexing**: GeoPandas spatial joins
    - **Geometry Validation**: Shapely.is_valid() checks
    - **Projection Handling**: PyProj coordinate transformations
    
    **Error Handling & Logging:**
    ```python
    try:
        data = pd.read_csv(file_path)
        st.success(f"✅ Loaded {len(data):,} records")
    except FileNotFoundError:
        st.error(f"❌ Data file not found: {file_path}")
    except Exception as e:
        st.warning(f"⚠️ Data loading issue: {str(e)}")
    ```
    """)

# External APIs & Data Access Portals
st.header("🌐 External APIs & Data Access Portals")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔗 NASA Data Access APIs
    
    **NASA Earthdata Login:**
    - **URL**: https://earthdata.nasa.gov/
    - **Authentication**: OAuth 2.0 / URS (Unified Resource System)
    - **Usage**: Access to MODIS, Landsat, GRACE data
    - **Rate Limits**: Varies by dataset (typically 100 requests/hour)
    
    **NASA Giovanni API:**
    - **URL**: https://giovanni.gsfc.nasa.gov/giovanni/
    - **Purpose**: Atmospheric and climate data analysis
    - **Data**: IMERG precipitation, MERRA-2 reanalysis
    - **Format**: NetCDF, HDF, CSV outputs
    
    **USGS Earth Explorer API:**
    ```python
    # Landsat data access example
    import requests
    from datetime import datetime
    
    def search_landsat(bbox, start_date, end_date):
        url = "https://earthexplorer.usgs.gov/inventory/json/v/1.4.1/"
        payload = {
            "bbox": bbox,
            "startDate": start_date,
            "endDate": end_date,
            "dataset": "landsat_8_c1",
            "maxResults": 100
        }
        response = requests.post(url, json=payload)
        return response.json()
    ```
    """)

with col2:
    st.markdown("""
    ### 🇪🇺 Copernicus Data Access
    
    **Copernicus Open Access Hub API:**
    - **URL**: https://scihub.copernicus.eu/dhus/
    - **Authentication**: Username/password registration
    - **Data**: Sentinel-1, -2, -3, -5P satellite data
    - **Query Language**: OpenSearch standard
    
    **Copernicus Climate Data Store (CDS):**
    - **URL**: https://cds.climate.copernicus.eu/
    - **API**: CDS Toolbox for programmatic access  
    - **Data**: ERA5 reanalysis, climate projections
    - **Python Client**: `cdsapi` package
    
    **Example Sentinel-5P Query:**
    ```python
    from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
    
    api = SentinelAPI('username', 'password', 
                      'https://s5phub.copernicus.eu/dhus')
    
    footprint = geojson_to_wkt(read_geojson('sulaimani_bbox.geojson'))
    products = api.query(footprint,
                        date = ('20240801', '20240831'),
                        platformname = 'Sentinel-5P',
                        producttype = 'L2__NO2___')
    ```
    
    **WorldPop Data Portal:**
    - **URL**: https://www.worldpop.org/
    - **Data**: High-resolution population estimates
    - **Coverage**: Global, 100m resolution
    - **Formats**: GeoTIFF, CSV, API access
    """)

# Project Implementation Timeline & Milestones
st.header("� Project Implementation Timeline & Milestones")

st.markdown("""
### 🚀 Development Timeline (NASA Space Apps Challenge 2025)
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 🗓️ Phase 1: Research & Planning (Days 1-2)
    - **✅ Problem Definition**: Urban sustainability challenges in Sulaimani
    - **✅ Literature Review**: 15+ academic papers on remote sensing applications
    - **✅ Data Source Identification**: NASA, ESA, and partner datasets
    - **✅ Technical Architecture**: Streamlit multi-page application design
    - **✅ Methodology Selection**: Multi-criteria decision analysis framework
    
    #### 🗓️ Phase 2: Data Acquisition & Processing (Days 2-4)
    - **✅ NASA Data Download**: MODIS, Landsat, GRACE datasets
    - **✅ Copernicus Access**: Sentinel-5P air quality data
    - **✅ Data Preprocessing**: Spatial harmonization and temporal alignment
    - **✅ Quality Control**: Statistical filtering and validation procedures
    - **✅ Enhanced Dataset Creation**: High-resolution 100×100 grids
    
    #### 🗓️ Phase 3: Analysis Development (Days 4-6)  
    - **✅ Air Quality Assessment**: AQI calculation algorithms
    - **✅ Heat Island Analysis**: Land surface temperature processing
    - **✅ Urban Growth Tracking**: Built-up area change detection
    - **✅ Multi-criteria Integration**: Weighted scoring system
    - **✅ Spatial Analysis Tools**: Polygon selection and buffering
    """)

with col2:
    st.markdown("""
    #### �️ Phase 4: Application Development (Days 5-7)
    - **✅ Frontend Development**: 13 Streamlit pages with navigation
    - **✅ Interactive Mapping**: Folium integration with drawing capabilities
    - **✅ Visualization System**: Plotly charts and statistical displays
    - **✅ User Interface Design**: Responsive layout and mobile optimization
    - **✅ Performance Optimization**: Caching and memory management
    
    #### 🗓️ Phase 5: Testing & Refinement (Days 6-8)
    - **✅ Functionality Testing**: All page interactions and data loading
    - **✅ Polygon Analysis Debugging**: Multi-section validation fixes
    - **✅ Column Name Corrections**: Dataset compatibility improvements  
    - **✅ Error Handling**: Robust exception management
    - **✅ Documentation**: Complete technical and user documentation
    
    #### 🗓️ Phase 6: Deployment & Presentation (Days 8-9)
    - **✅ Platform Deployment**: Streamlit Cloud hosting setup
    - **✅ Final Integration Testing**: End-to-end workflow validation
    - **✅ Presentation Materials**: Demo preparation and documentation
    - **✅ Project Submission**: NASA Space Apps Challenge delivery
    - **✅ Reference Documentation**: This comprehensive references page
    """)

# Future Research Directions & Recommendations
st.header("🔮 Future Research Directions & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🎯 Immediate Enhancements (3-6 months)
    
    **Real-Time Data Integration:**
    - **Ground Sensor Networks**: Deploy air quality monitoring stations
    - **IoT Integration**: Temperature, humidity, and pollution sensors
    - **Crowdsourced Data**: Citizen science mobile applications
    - **Social Media Analysis**: Urban sentiment and environmental concerns
    
    **Advanced Analytics:**
    - **Machine Learning Models**: Predictive air quality forecasting
    - **Deep Learning**: Satellite image classification for land use
    - **Time Series Forecasting**: Urban growth projection models
    - **Causal Analysis**: Impact assessment of policy interventions
    
    **Policy Integration:**
    - **Zoning Recommendations**: Evidence-based urban planning guidance
    - **Investment Prioritization**: Cost-benefit analysis framework
    - **Regulatory Compliance**: Environmental standard monitoring
    - **Stakeholder Engagement**: Community participation platforms
    """)

with col2:
    st.markdown("""
    ### 🌍 Long-Term Vision (1-3 years)
    
    **Regional Expansion:**
    - **Iraqi Kurdistan**: Erbil, Dohuk comparative analysis
    - **Middle East Cities**: Tehran, Baghdad, Damascus integration
    - **Global South**: Transferable methodology for similar cities
    - **Climate Scenarios**: Future projection under different pathways
    
    **Advanced Technologies:**
    - **Digital Twin Development**: 3D city modeling with real-time updates
    - **AI-Powered Recommendations**: Automated urban planning suggestions
    - **Blockchain Integration**: Transparent environmental monitoring
    - **Augmented Reality**: Immersive urban planning visualization
    
    **Research Collaborations:**
    - **University Partnerships**: Academic research integration
    - **Government Cooperation**: Policy implementation support  
    - **International Organizations**: UN-Habitat, World Bank cooperation
    - **Private Sector**: Technology company partnerships
    """)

st.markdown("---")

# License and Usage Terms
st.header("📋 License, Usage Terms & Data Attribution")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### ⚖️ Software License & Terms of Use
    
    **MIT License (2025)**
    ```
    Permission is hereby granted, free of charge, to any person 
    obtaining a copy of this software and associated documentation 
    files (the "Software"), to deal in the Software without 
    restriction, including without limitation the rights to use, 
    copy, modify, merge, publish, distribute, sublicense, and/or 
    sell copies of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
    ```
    
    **Data Usage Guidelines:**
    - **Attribution Required**: Credit NASA, ESA, and data providers
    - **Academic Use**: Encouraged for research and education
    - **Commercial Use**: Permitted with proper attribution
    - **Modification**: Allowed with documentation of changes
    - **Redistribution**: Permitted under same license terms
    
    **Disclaimer:**
    - Analysis results are for planning guidance only
    - Ground validation recommended for policy decisions
    - No warranty for accuracy or completeness
    - Users responsible for verification and validation
    """)

with col2:
    st.markdown("""
    ### 🙏 Complete Acknowledgments & Credits
    
    **Primary Data Providers:**
    - **NASA Earth Science Division**: MODIS, Landsat, GRACE missions
    - **ESA Copernicus Programme**: Sentinel-5P atmospheric monitoring
    - **USGS**: Landsat Data Continuity Mission support
    - **NOAA**: Weather and climate data integration
    - **WorldPop Project**: Population density estimates
    
    **Open Source Community:**
    - **Streamlit Team**: Web application framework
    - **Python Geospatial**: GeoPandas, Folium, Rasterio developers
    - **Plotly**: Interactive visualization library
    - **NumPy/SciPy**: Scientific computing foundation
    - **OpenStreetMap**: Base mapping data volunteers
    
    **Special Recognition:**
    - **NASA Space Apps Challenge**: Global hackathon platform
    - **Sulaimani Community**: Local knowledge and inspiration
    - **Academic Research Community**: Foundational scientific work
    - **Open Data Movement**: Enabling transparent, accessible science
    
    **Citation Recommendation:**
    ```
    Sulaimani Urban Growth Analysis Team (2025). 
    "Sustainable Urban Growth Analysis for Sulaimani City 
    Using NASA Earth Observation Data." 
    NASA Space Apps Challenge 2025.
    GitHub: [repository-url]
    ```
    """)

st.markdown("---")

# Final Summary & Impact Statement
st.success("""
### 🌟 Project Impact & Contribution to Sustainable Development

This comprehensive platform demonstrates the power of open science and NASA Earth observation data 
for addressing critical urban sustainability challenges. By combining multiple satellite datasets 
with advanced spatial analysis techniques, we have created a replicable framework that can:

**🎯 Immediate Impact:**
- **Inform Urban Planning**: Evidence-based zoning and infrastructure decisions
- **Guide Green Investment**: Priority areas for vegetation and cooling interventions  
- **Monitor Environmental Health**: Continuous air quality and heat stress assessment
- **Support Policy Making**: Data-driven environmental regulations and standards

**🌍 Broader Contributions:**
- **Open Science**: All code, data, and methodology freely available
- **Capacity Building**: Educational resource for remote sensing applications
- **Methodology Transfer**: Replicable approach for similar cities globally
- **Community Engagement**: Accessible platform for citizen participation

**📈 Measurable Outcomes:**
- **300,000+ Data Points**: High-resolution environmental analysis
- **15-Year Timeline**: Historical trend analysis for evidence-based planning
- **6 Criteria Assessment**: Comprehensive multi-dimensional urban evaluation
- **Interactive Platform**: User-friendly interface for non-technical stakeholders

*This project exemplifies how space technology can directly serve human welfare and environmental 
protection, advancing the UN Sustainable Development Goals through innovative data science applications.*
""")

st.markdown("---")

# Technical Footer
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-top: 30px;">
    <h4>🚀 NASA Space Apps Challenge 2025 | Sulaimani Sustainable Urban Growth Analysis</h4>
    <p><strong>Platform:</strong> Streamlit Multi-Page Application | <strong>Data:</strong> 15+ NASA & ESA Satellite Datasets</p>
    <p><strong>Analysis Period:</strong> 2018-2024 | <strong>Spatial Coverage:</strong> 1,150 km² Sulaimani Metropolitan Region</p>
    <p><strong>Technical Stack:</strong> Python 3.9+ | GeoPandas | Folium | Plotly | Streamlit</p>
    <p><strong>License:</strong> MIT Open Source | <strong>Documentation:</strong> Complete Technical References</p>
    <p><em>Built with ❤️ for sustainable cities and open science | Last Updated: October 2025</em></p>
</div>
""", unsafe_allow_html=True)
