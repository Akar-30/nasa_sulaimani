import streamlit as st

st.set_page_config(page_title="About & Team", page_icon="👥", layout="wide")

st.title("👥 About This Project")

st.markdown("---")

# Project overview
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## 🌍 Project: Sulaimani Sustainable Growth
    
    This interactive platform was created for the **2025 NASA Space Apps Challenge** to address 
    the critical question:
    
    > **"How can Sulaimani City grow sustainably to ensure both people's wellbeing and 
    > environmental resilience, informed by NASA Earth observation data?"**
    
    ### 🎯 Our Approach
    
    We combined multiple NASA and partner datasets to create a comprehensive view of Sulaimani's 
    urban challenges and opportunities:
    
    - **Air Quality Analysis** using Sentinel-5P and MODIS data
    - **Heat Island Mapping** with Landsat thermal imagery
    - **Urban Growth Tracking** through Copernicus GHSL and WorldPop
    - **Water Resource Assessment** via GRACE and IMERG datasets
    
    By integrating these diverse data sources, we identified priority areas for intervention 
    and developed actionable recommendations for sustainable urban planning.
    """)

with col2:
    st.info("""
    ### 📊 Key Achievements
    
    - ✅ Integrated 7+ NASA datasets
    - ✅ Analyzed 20 years of urban growth
    - ✅ Identified critical hotspots
    - ✅ Proposed concrete solutions
    - ✅ Interactive visualizations
    - ✅ Actionable recommendations
    """)
    
    st.success("""
    ### 🏆 Impact
    
    This platform can help:
    - Guide zoning decisions
    - Prioritize green infrastructure
    - Protect vulnerable communities
    - Ensure sustainable water use
    - Monitor environmental health
    """)

st.markdown("---")

# Why Sulaimani
st.header("🏙️ Why Sulaimani?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### The Challenge
    
    Sulaimani, the cultural capital of Iraqi Kurdistan, faces rapid urbanization pressures:
    
    - **40%+ population growth** in 20 years
    - **Expanding urban footprint** consuming agricultural land
    - **Rising temperatures** and heat islands
    - **Air pollution** from traffic and industry
    - **Water scarcity** concerns
    - **Infrastructure gaps** in new developments
    
    These challenges are common to many rapidly growing cities in semi-arid regions.
    """)

with col2:
    st.markdown("""
    ### The Opportunity
    
    Sulaimani is at a critical juncture:
    
    - **Young, dynamic population** ready for sustainable development
    - **Strong local governance** capable of implementing changes
    - **Growing awareness** of environmental issues
    - **Available technology** (NASA data, mapping tools)
    - **Regional influence** as a model for other cities
    
    With the right data and planning, Sulaimani can become a regional leader 
    in sustainable urban development.
    """)

st.markdown("---")

# Team section
st.header("👥 Our Team")

st.markdown("""
We are a multidisciplinary team passionate about using space technology to solve 
Earth's challenges. Our backgrounds span:
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    #### 🛰️ Remote Sensing
    - Satellite data analysis
    - GIS expertise
    - Spatial statistics
    """)

with col2:
    st.markdown("""
    #### 🏗️ Urban Planning
    - City planning
    - Land use analysis
    - Infrastructure design
    """)

with col3:
    st.markdown("""
    #### 💻 Data Science
    - Python programming
    - Data visualization
    - Web development
    """)

with col4:
    st.markdown("""
    #### 🌱 Environmental Science
    - Climate analysis
    - Ecology
    - Sustainability
    """)

st.markdown("---")

# Data sources
st.header("📚 Data Sources & Credits")

st.markdown("""
This project would not be possible without the open data provided by:
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🛰️ NASA & Partners
    
    **NASA Earth Observations:**
    - **MODIS**: Air quality (AOD) and vegetation (NDVI)
    - **Landsat 8/9**: Land surface temperature and high-resolution imagery
    - **GRACE**: Groundwater availability trends
    - **IMERG/TRMM**: Precipitation data
    - **NASA Earth Observatory**: Historical imagery
    
    **ESA Copernicus:**
    - **Sentinel-5P (TROPOMI)**: Air pollutants (NO₂, SO₂, O₃)
    - **Copernicus GHSL**: Urban built-up area mapping
    
    **Other Sources:**
    - **WorldPop**: Population density estimates
    - **OpenStreetMap**: Base mapping data
    """)

with col2:
    st.markdown("""
    ### 🔗 Useful Resources
    
    **Data Access:**
    - [NASA Earthdata](https://earthdata.nasa.gov/)
    - [Copernicus Open Access Hub](https://scihub.copernicus.eu/)
    - [WorldPop Data Portal](https://www.worldpop.org/)
    - [Google Earth Engine](https://earthengine.google.com/)
    
    **Tools & Documentation:**
    - [Streamlit Documentation](https://docs.streamlit.io/)
    - [Folium Mapping](https://python-visualization.github.io/folium/)
    - [Plotly Visualization](https://plotly.com/python/)
    - [GeoPandas](https://geopandas.org/)
    
    **NASA Resources:**
    - [NASA ARSET Training](https://appliedsciences.nasa.gov/what-we-do/capacity-building/arset)
    - [NASA Space Apps Challenge](https://www.spaceappschallenge.org/)
    """)

st.markdown("---")

# Technical details
st.header("⚙️ Technical Implementation")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🛠️ Technology Stack
    
    **Frontend:**
    - **Streamlit**: Web application framework
    - **Folium**: Interactive maps (Leaflet.js)
    - **Plotly**: Data visualizations and charts
    
    **Data Processing:**
    - **Pandas**: Data manipulation
    - **GeoPandas**: Geospatial data handling
    - **Rasterio**: Satellite imagery processing
    - **NumPy**: Numerical computations
    
    **Deployment:**
    - **Streamlit Cloud**: Free hosting
    - **GitHub**: Version control
    - **Python 3.9+**: Programming language
    """)

with col2:
    st.markdown("""
    ### 📁 Project Structure
    
    ```
    nasa_sulaimani/
    ├── Home.py                  # Main landing page
    ├── pages/
    │   ├── 1_Challenge.py       # Urban challenges
    │   ├── 2_Data_Pathway.py    # Data overview
    │   ├── 3_Air_Quality.py     # Air pollution
    │   ├── 4_Heat_Greenspace.py # Temperature & vegetation
    │   ├── 5_Urban_Water.py     # Growth & water
    │   ├── 6_Solutions.py       # Recommendations
    │   └── 7_About.py           # This page
    ├── data/                    # NASA datasets (CSV, GeoJSON)
    ├── utils/                   # Helper functions
    └── requirements.txt         # Dependencies
    ```
    """)

st.markdown("---")

# Future work
st.header("🚀 Future Enhancements")

st.markdown("""
This platform is a starting point. Potential future improvements include:
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 📊 Data
    - Real-time data updates
    - More historical coverage
    - Higher spatial resolution
    - Ground sensor integration
    - Citizen science data
    """)

with col2:
    st.markdown("""
    #### 🔧 Features
    - Predictive modeling
    - Scenario planning tools
    - Mobile application
    - Multi-language support
    - API for third-party apps
    """)

with col3:
    st.markdown("""
    #### 🌍 Scale
    - Regional comparison
    - Other Iraqi cities
    - Middle East cities
    - Climate projections
    - Economic analysis
    """)

st.markdown("---")

# Contact
st.header("📧 Contact & Collaboration")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🤝 Get Involved
    
    We welcome collaboration from:
    - **City planners** interested in using NASA data
    - **Researchers** working on urban sustainability
    - **Developers** who want to contribute code
    - **Citizens** who want to provide local knowledge
    - **Organizations** seeking partnership opportunities
    """)

with col2:
    st.markdown("""
    ### 📬 Reach Out
    
    **GitHub Repository:**  
    [github.com/your-team/sulaimani-growth](#) (Add your link)
    
    **Email:**  
    team@sulaimani-growth.org (Add your email)
    
    **Social Media:**  
    Twitter: @SulaimaniGrowth (Add your handles)
    
    **License:**  
    MIT License - Free to use and adapt
    """)

st.markdown("---")

# Acknowledgments
st.success("""
### 🙏 Acknowledgments

Special thanks to:
- **NASA** for making Earth observation data freely available
- **ESA Copernicus** for Sentinel satellite data
- **Space Apps Challenge** organizers for this opportunity
- **Sulaimani community** for inspiring this project
- **Open-source community** for amazing tools and libraries

*Together, we can build sustainable cities for all.* 🌍
""")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🚀 NASA Space Apps Challenge 2025 | Sulaimani Team</p>
    <p>Built with ❤️ using NASA Earth observation data</p>
    <p>Last updated: October 2025</p>
</div>
""", unsafe_allow_html=True)
