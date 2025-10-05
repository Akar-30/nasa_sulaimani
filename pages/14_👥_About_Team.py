import streamlit as st

st.set_page_config(page_title="About Team", page_icon="👥", layout="wide")

st.title("👥 About Our Team")

st.markdown("---")

# Project overview
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## 🌍 Project: Sulaimani Sustainable Growth Analysis
    
    This interactive platform was created for the **2025 NASA Space Apps Challenge** to address 
    the critical question:
    
    > **"How can Sulaimani City grow sustainably to ensure both people's wellbeing and 
    > environmental resilience, informed by NASA Earth observation data?"**
    
    ### 🎯 Our Mission
    
    We combined multiple NASA and partner datasets to create a comprehensive view of Sulaimani's 
    urban challenges and opportunities:
    
    - **🌬️ Air Quality Analysis** using Sentinel-5P and MODIS data
    - **🌡️ Heat Island Mapping** with Landsat thermal imagery
    - **🏙️ Urban Growth Tracking** through Copernicus GHSL and WorldPop
    - **💧 Water Resource Assessment** via GRACE and IMERG datasets
    - **🔬 Enhanced Multi-Criteria Analysis** with 100×100 high-resolution grids
    - **💡 Integrated Solution Platform** for evidence-based urban planning
    
    By integrating these diverse data sources, we identified priority areas for intervention 
    and developed actionable recommendations for sustainable urban planning.
    """)

with col2:
    st.info("""
    ### 📊 Key Achievements
    
    - ✅ **13 Interactive Pages** with comprehensive analysis
    - ✅ **15+ NASA Datasets** integrated and processed
    - ✅ **300,000+ Data Points** for high-resolution analysis
    - ✅ **15-Year Timeline** of historical trends
    - ✅ **6 Criteria Assessment** multi-dimensional evaluation
    - ✅ **Real-time Analysis** with interactive polygon selection
    - ✅ **Open Source Platform** with MIT license
    """)
    
    st.success("""
    ### 🏆 Platform Impact
    
    This platform helps:
    - 🎯 **Guide zoning decisions** with evidence-based data
    - 🌱 **Prioritize green infrastructure** for cooling
    - 🛡️ **Protect vulnerable communities** from pollution
    - 💧 **Ensure sustainable water use** monitoring
    - 📊 **Monitor environmental health** continuously
    - 🤝 **Engage citizens** in urban planning decisions
    """)

st.markdown("---")

# Why Sulaimani
st.header("🏙️ Why Sulaimani City?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🚨 The Challenges
    
    Sulaimani, the cultural capital of Iraqi Kurdistan, faces rapid urbanization pressures 
    common to many growing cities in semi-arid regions:
    
    **Urban Growth Pressures:**
    - 📈 **40%+ population growth** in the last 20 years
    - 🏗️ **Expanding urban footprint** consuming agricultural land
    - 🚗 **Increased traffic congestion** and air pollution
    - 🏘️ **Infrastructure gaps** in new developments
    
    **Environmental Challenges:**
    - 🌡️ **Rising temperatures** and urban heat islands
    - 💨 **Air pollution** from traffic and industrial sources
    - 💧 **Water scarcity** concerns in semi-arid climate
    - 🌿 **Loss of green spaces** to urban expansion
    
    **Data Gap:**
    - 📊 **Limited environmental monitoring** infrastructure
    - 🗺️ **Lack of integrated spatial analysis** tools
    - 📋 **Insufficient evidence-based** urban planning
    """)

with col2:
    st.markdown("""
    ### 🌟 The Opportunity
    
    Sulaimani is uniquely positioned to become a model for sustainable urban development:
    
    **Institutional Strengths:**
    - 👨‍💼 **Strong local governance** capable of implementing changes
    - 🎓 **Educational institutions** with technical capacity
    - 💡 **Growing environmental awareness** among citizens
    - 🤝 **International cooperation** opportunities
    
    **Technological Assets:**
    - 🛰️ **NASA Earth observation data** freely available
    - 💻 **Modern mapping and analysis tools** accessible
    - 📱 **Digital infrastructure** for platform deployment
    - 🔗 **Open source technologies** for sustainable solutions
    
    **Regional Impact:**
    - 🌍 **Regional influence** as Kurdistan's cultural capital
    - 🏛️ **Policy leadership** potential for Iraq and region
    - 🎯 **Demonstration project** for similar cities globally
    - 📈 **Economic benefits** from sustainable development
    
    With the right data and planning tools, Sulaimani can lead the region 
    in sustainable urban development and climate resilience.
    """)

st.markdown("---")

# Team section
st.header("👨‍💻 Our Multidisciplinary Team")

st.markdown("""
We are a passionate team of researchers, developers, and urban planning enthusiasts who believe 
in the power of **space technology to solve Earth's challenges**. Our diverse backgrounds create 
a comprehensive approach to urban sustainability analysis:
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    #### 🛰️ Remote Sensing Expertise
    - **Satellite data analysis** and processing
    - **GIS and spatial analysis** methodologies
    - **Multi-temporal change detection**
    - **Earth observation applications**
    - **Geospatial statistics and modeling**
    """)

with col2:
    st.markdown("""
    #### 🏗️ Urban Planning Knowledge
    - **Sustainable city planning** principles
    - **Land use analysis** and zoning
    - **Infrastructure development** strategies
    - **Environmental impact assessment**
    - **Community engagement** methods
    """)

with col3:
    st.markdown("""
    #### 💻 Data Science & Development
    - **Python programming** and data analysis
    - **Web application development** (Streamlit)
    - **Interactive data visualization** (Plotly, Folium)
    - **Machine learning** and statistical analysis
    - **Open source development** practices
    """)

with col4:
    st.markdown("""
    #### 🌱 Environmental Science
    - **Climate change analysis** and adaptation
    - **Air quality assessment** methodologies
    - **Urban ecology** and green infrastructure
    - **Water resource management**
    - **Sustainability indicators** and metrics
    """)

st.markdown("---")

# Methodology
st.header("🔬 Our Approach & Methodology")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📊 Multi-Criteria Decision Analysis (MCDA)
    
    **Integrated Assessment Framework:**
    - **Air Quality (25%)**: Health and environmental priority
    - **Heat/Greenspace (20%)**: Climate adaptation focus
    - **Infrastructure (20%)**: Accessibility and connectivity
    - **Topography (15%)**: Development feasibility
    - **Economic Activity (10%)**: Investment viability
    - **Population Density (10%)**: Social considerations
    
    **Scientific Rigor:**
    - **Peer-reviewed methodologies** from urban planning literature
    - **NASA-validated algorithms** for satellite data processing
    - **Statistical validation** and uncertainty quantification
    - **Cross-dataset validation** for accuracy assurance
    
    **Open Science Principles:**
    - **Transparent methodology** with documented code
    - **Reproducible analysis** with version-controlled data
    - **Open source tools** for accessibility and collaboration
    - **Public data sources** for global applicability
    """)

with col2:
    st.markdown("""
    ### 🎯 Innovation & Impact
    
    **Technical Innovation:**
    - **High-Resolution Grid Analysis**: 100×100 sampling (10,000 points/dataset)
    - **Real-time Polygon Selection**: Interactive area analysis with st_folium
    - **Multi-temporal Analysis**: 15-year historical trend assessment
    - **Integrated Platform**: 13 pages of comprehensive urban analysis
    
    **User-Centered Design:**
    - **Non-technical Interface**: Accessible to city planners and citizens
    - **Interactive Visualizations**: Engaging charts and maps
    - **Evidence-based Recommendations**: Actionable urban planning guidance
    - **Mobile-responsive Design**: Accessible on all devices
    
    **Scalable Framework:**
    - **Replicable Methodology**: Transferable to other cities globally
    - **Modular Architecture**: Easy to extend with new datasets
    - **API-ready Design**: Future integration with external systems
    - **Documentation**: Complete technical references for developers
    """)

st.markdown("---")

# Contact and Collaboration
st.header("🤝 Collaboration & Contact")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🌍 Join Our Mission
    
    We welcome collaboration and partnership from:
    
    **Academic & Research:**
    - 🎓 **Universities** working on urban sustainability research
    - 🔬 **Research institutions** in remote sensing and GIS
    - 📚 **Students** interested in space technology applications
    - 📊 **Data scientists** passionate about environmental analysis
    
    **Government & Policy:**
    - 🏛️ **City planners** seeking evidence-based tools
    - 📋 **Policy makers** interested in environmental monitoring
    - 🌐 **International organizations** (UN-Habitat, World Bank)
    - 🤝 **Regional governments** in Kurdistan and Iraq
    
    **Technology & Innovation:**
    - 💻 **Software developers** wanting to contribute code
    - 🛰️ **Space technology companies** for advanced data sources
    - 📱 **App developers** for mobile platform extensions
    - 🔧 **Open source contributors** for platform improvements
    """)

with col2:
    st.markdown("""
    ### 📬 Get In Touch
    
    **Project Repository:**  
    🔗 **GitHub**: [NASA Space Apps Sulaimani Project](#)  
    (Open source code, datasets, and documentation)
    
    **Contact Information:**  
    ✉️ **Email**: sulaimani.urban.analysis@spaceapps.org  
    📱 **LinkedIn**: [Sulaimani Urban Growth Team](#)  
    🐦 **Twitter**: [@SulaimaniGrowth](#)  
    
    **Collaboration Opportunities:**
    - 💡 **Feature requests** and improvement suggestions  
    - 🔄 **Data sharing** partnerships for enhanced analysis
    - 🎯 **Use case development** for other cities and regions
    - 📖 **Academic partnerships** for research publications
    - 🏆 **Competition participation** in future space challenges
    
    **Technical Support:**
    - 📋 **Issues and bug reports** via GitHub  
    - 💬 **Discussion forums** for methodology questions
    - 📚 **Documentation contributions** and improvements
    - 🎓 **Training workshops** and capacity building sessions
    """)

st.markdown("---")

# Future Vision
st.header("🔮 Future Vision & Roadmap")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 🚀 Short-term (3-6 months)
    
    **Enhanced Features:**
    - **Real-time data integration** from ground sensors
    - **Predictive modeling** for air quality forecasting  
    - **Mobile application** for citizen engagement
    - **Multi-language support** (Arabic, Kurdish, English)
    - **API development** for third-party integrations
    
    **Data Expansion:**
    - **Higher resolution** satellite imagery processing
    - **Additional pollutants** monitoring (PM1, BC)
    - **Ground validation** campaign integration
    - **Citizen science** data collection tools
    """)

with col2:
    st.markdown("""
    #### 🌍 Medium-term (6-18 months)
    
    **Regional Scaling:**
    - **Iraqi Kurdistan cities**: Erbil, Dohuk analysis
    - **Regional comparison** and benchmarking tools
    - **Climate scenario modeling** for future projections
    - **Economic impact assessment** modules
    
    **Advanced Analytics:**
    - **Machine learning** for pattern recognition
    - **Digital twin development** with 3D modeling
    - **Social vulnerability mapping** integration
    - **Transportation network analysis**
    """)

with col3:
    st.markdown("""
    #### 🏆 Long-term (1-3 years)
    
    **Global Impact:**
    - **International expansion** to Global South cities
    - **UN-Habitat partnership** for SDG monitoring
    - **Academic integration** with university curricula  
    - **Policy tool certification** for official use
    
    **Technology Evolution:**
    - **AI-powered recommendations** for urban planning
    - **Blockchain integration** for transparent monitoring
    - **Augmented reality** visualization tools
    - **Automated report generation** for stakeholders
    """)

st.markdown("---")

# Acknowledgments
st.success("""
### 🙏 Special Acknowledgments

**Inspiration & Data Sources:**
- 🛰️ **NASA Earth Science Division** for making Earth observation data freely accessible
- 🇪🇺 **ESA Copernicus Programme** for Sentinel satellite missions and open data policy
- 🌍 **Space Apps Challenge** organizers for creating this incredible global platform
- 🏙️ **Sulaimani community** for inspiring our focus on sustainable urban development
- 🤝 **Open source community** for amazing tools, libraries, and collaborative spirit

**Technical Foundation:**
- 💻 **Python ecosystem** (NumPy, Pandas, GeoPandas, Plotly, Streamlit) developers
- 🗺️ **OpenStreetMap contributors** for base mapping data and geographic information
- 📊 **Scientific community** for peer-reviewed methodologies and validation approaches
- 🎓 **Educational institutions** worldwide advancing remote sensing and urban planning research

**Global Vision:**
- 🌱 **Environmental advocates** working on climate change adaptation and sustainability
- 🏛️ **Urban planners** worldwide creating more livable, resilient cities
- 👥 **Citizens everywhere** demanding evidence-based, transparent governance
- 🚀 **Space enthusiasts** believing in technology's power to solve Earth's challenges

*Together, we're building a more sustainable, data-driven future for urban development. 
Every city deserves the tools to grow wisely and protect both people and planet.* 🌍✨
""")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #666; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin-top: 40px;">
    <h3 style="color: white; margin-bottom: 20px;">🚀 NASA Space Apps Challenge 2025</h3>
    <h4 style="color: white; margin-bottom: 15px;">Sulaimani Sustainable Urban Growth Analysis Team</h4>
    
    <p style="font-size: 16px; margin-bottom: 10px;">
        <strong>Platform:</strong> 13-Page Interactive Analysis | <strong>Data:</strong> 15+ NASA & ESA Datasets | <strong>Coverage:</strong> 1,150 km²
    </p>
    
    <p style="font-size: 14px; margin-bottom: 15px;">
        Built with ❤️ using NASA Earth observation data for sustainable cities worldwide
    </p>
    
    <div style="border-top: 1px solid rgba(255,255,255,0.3); padding-top: 15px; margin-top: 20px;">
        <p style="font-size: 12px; margin: 0;">
            <strong>License:</strong> MIT Open Source | <strong>Documentation:</strong> Complete Technical References Available
        </p>
        <p style="font-size: 12px; margin: 5px 0 0 0;">
            <strong>Last Updated:</strong> October 2025 | <strong>Status:</strong> Active Development & Community Engagement
        </p>
    </div>
</div>
""", unsafe_allow_html=True)