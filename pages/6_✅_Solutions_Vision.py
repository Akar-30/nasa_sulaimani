import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import pandas as pd

st.set_page_config(page_title="Solutions & Vision", page_icon="✅", layout="wide")

st.title("✅ Proposed Solutions & Future Vision")

st.markdown("""
Based on our data analysis, here are concrete, actionable recommendations for sustainable 
growth in Sulaimani City, informed by NASA Earth observation data.
""")

# Solutions by stakeholder
st.header("🎯 Recommendations by Stakeholder")

tab1, tab2, tab3, tab4 = st.tabs([
    "🏛️ Municipality",
    "🏘️ Residents", 
    "📐 Urban Planners",
    "💧 Resource Managers"
])

with tab1:
    st.subheader("For the Municipality")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🌳 Green Infrastructure
        
        **Immediate Actions (6-12 months):**
        - Plant 10,000 street trees along major corridors
        - Establish 3 new urban parks in heat-stressed areas
        - Create green buffer zones along industrial areas
        - Implement cool pavement program
        
        **Medium Term (1-3 years):**
        - Develop 5 large neighborhood parks (>3 hectares each)
        - River restoration and waterfront greenways
        - Green roof incentive program
        - Urban forest master plan
        
        **Budget Required:** $15-20 million
        **Impact:** Reduce heat by 2-3°C, improve air quality by 15%
        """)
    
    with col2:
        st.markdown("""
        ### 🚍 Clean Transport & Mobility
        
        **Immediate Actions:**
        - Expand bus rapid transit (BRT) to new suburbs
        - Create dedicated bike lanes (50 km network)
        - Traffic management in high-pollution zones
        - Electric vehicle charging infrastructure
        
        **Medium Term:**
        - Light rail system feasibility study
        - Car-free zones in city center
        - Park & ride facilities
        - Pedestrian-friendly street redesign
        
        **Budget Required:** $40-50 million
        **Impact:** Reduce traffic emissions by 25%
        """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏗️ Zoning & Land Use
        
        - **Restrict expansion** in water-scarce western zones
        - **Mixed-use development** mandates (reduce commuting)
        - **Green space requirements**: 30% for new developments
        - **Height restrictions** to preserve views and air flow
        - **Industrial zone relocation** away from residential areas
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Monitoring & Data
        
        - Install **10 air quality monitoring stations**
        - Real-time data dashboard (public access)
        - Annual environmental health reports
        - Integrate NASA data in planning decisions
        - Community environmental reporting app
        """)

with tab2:
    st.subheader("For City Residents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🌱 Community Actions
        
        **What You Can Do:**
        - Participate in tree-planting initiatives
        - Report air/water quality issues via app
        - Join neighborhood greening projects
        - Support local markets (reduce transport emissions)
        - Advocate for green spaces in your area
        - Water conservation at home
        - Use public transport when possible
        
        **Community Programs:**
        - Adopt-a-park initiatives
        - Neighborhood environmental committees
        - Green skills training workshops
        - Youth environmental education
        """)
    
    with col2:
        st.markdown("""
        ### 📱 Engagement Tools
        
        **Planned Apps & Platforms:**
        - **Air Quality App**: Real-time AQI by neighborhood
        - **Green Space Finder**: Locate nearest parks
        - **Report Issues**: Water leaks, pollution, heat hazards
        - **Community Garden Map**: Find or start gardens
        - **Transport Planner**: Optimize low-emission routes
        
        **Feedback Mechanisms:**
        - Monthly town halls on environmental issues
        - Online surveys on park locations
        - Participatory budgeting for green projects
        """)

with tab3:
    st.subheader("For Urban Planners")
    
    st.markdown("""
    ### 🛰️ Using NASA Datasets for Planning Decisions
    
    Integrate these Earth observation datasets into your regular planning workflow:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Monthly Monitoring**
        
        - Air quality trends (Sentinel-5P)
        - Vegetation health (MODIS NDVI)
        - Update heat maps quarterly
        - Track urban expansion
        """)
    
    with col2:
        st.info("""
        **Annual Assessments**
        
        - Comprehensive LST analysis
        - Water stress evaluation
        - Green space inventory
        - Growth pattern analysis
        """)
    
    with col3:
        st.info("""
        **5-Year Planning**
        
        - Climate vulnerability mapping
        - Infrastructure gap analysis
        - Long-term growth scenarios
        - Sustainability benchmarks
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 📋 Planning Checklist for New Developments
    
    Before approving new development, verify:
    
    - [ ] **Air Quality Impact**: Will it worsen pollution hotspots?
    - [ ] **Heat Island Effect**: Is there adequate green space (>30%)?
    - [ ] **Water Availability**: Is infrastructure capacity sufficient?
    - [ ] **Transit Access**: Is public transport within 500m?
    - [ ] **Climate Resilience**: Does it account for future heat/drought?
    - [ ] **Environmental Justice**: Does it benefit underserved areas?
    """)

with tab4:
    st.subheader("For Water & Environmental Resource Managers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 💧 Water Management
        
        **Immediate Priorities:**
        - Groundwater monitoring network (GRACE integration)
        - Leak detection in western distribution
        - Rainwater harvesting mandates for new buildings
        - Water-efficient agriculture in peri-urban areas
        
        **Strategic Actions:**
        - Alternative water sources (treated wastewater)
        - Aquifer recharge projects
        - Drought contingency planning
        - Water pricing reforms
        - Desalination feasibility study
        """)
    
    with col2:
        st.markdown("""
        ### 🌿 Environmental Protection
        
        **Key Actions:**
        - Protect remaining agricultural buffer zones
        - Restore degraded land with native vegetation
        - Wildlife corridor preservation
        - Air quality improvement targets (20% by 2030)
        - Climate adaptation strategy
        - Circular economy initiatives
        """)

st.markdown("---")

# Best zones map
st.header("🗺️ Sustainable Expansion Zones")

st.markdown("""
This integrated map shows the **best zones for sustainable urban expansion** based on 
combined analysis of air quality, water availability, heat stress, and existing infrastructure.
""")

# Zone selection
show_layers = st.multiselect(
    "Select Data Layers to Display",
    ["Air Quality", "Water Stress", "Heat Islands", "Existing Infrastructure", "Recommended Expansion Zones"],
    default=["Recommended Expansion Zones"]
)

m_final = folium.Map(
    location=[35.5608, 45.4347],
    zoom_start=11,
    tiles='OpenStreetMap'
)

# Add satellite layer
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite'
).add_to(m_final)

# TODO: Add layers based on selection
# This will combine all your datasets into one comprehensive view

# Example recommended zones (will be from actual analysis)
recommended_zones = [
    {"name": "Northeast Expansion Zone", "lat": 35.5808, "lon": 45.4547, 
     "reason": "Good water access, low pollution, moderate temperatures"},
    {"name": "South Infill Zone", "lat": 35.5408, "lon": 45.4347,
     "reason": "Existing infrastructure, near public transport"},
]

for zone in recommended_zones:
    folium.Marker(
        location=[zone["lat"], zone["lon"]],
        popup=f"<b>{zone['name']}</b><br>{zone['reason']}",
        icon=folium.Icon(color='green', icon='check', prefix='fa')
    ).add_to(m_final)

# Zones to avoid
avoid_zones = [
    {"name": "Western Water-Stressed Area", "lat": 35.5308, "lon": 45.4047,
     "reason": "Groundwater depletion, limited infrastructure"},
]

for zone in avoid_zones:
    folium.Marker(
        location=[zone["lat"], zone["lon"]],
        popup=f"<b>{zone['name']}</b><br>⚠️ {zone['reason']}",
        icon=folium.Icon(color='red', icon='times', prefix='fa')
    ).add_to(m_final)

folium.LayerControl().add_to(m_final)

st_folium(m_final, width=1400, height=500)

# Legend
col1, col2 = st.columns(2)

with col1:
    st.success("""
    ### 🟢 Recommended Expansion Zones
    
    - **Northeast**: Good environmental conditions, infrastructure ready
    - **South Infill**: Utilize existing services, reduce sprawl
    - **Controlled Growth**: Medium density, mixed-use development
    """)

with col2:
    st.error("""
    ### 🔴 Zones to Avoid/Restrict
    
    - **Western Areas**: Severe water stress
    - **Industrial Buffer**: Air quality concerns
    - **Agricultural Land**: Preserve for food security and cooling
    """)

st.markdown("---")

# Future vision
st.header("🔮 The Vision: Future Sulaimani 2035")

st.markdown("""
### A city that grows with people and nature in mind

**By 2035, Sulaimani will be:**
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 🌳 Greener
    - 30% green space coverage
    - Urban forest network
    - Parks within 10-minute walk
    - 50,000+ new trees
    - Restored river corridors
    """)

with col2:
    st.markdown("""
    #### 🌬️ Cleaner
    - 50% reduction in air pollution
    - Zero-emission public transport
    - Industrial emissions controlled
    - Real-time air quality monitoring
    - Car-free city center
    """)

with col3:
    st.markdown("""
    #### 💧 Sustainable
    - Water-neutral development
    - Climate-resilient infrastructure
    - Smart growth patterns
    - Protected agricultural buffer
    - Circular economy
    """)

# Impact projections
st.subheader("📊 Projected Impacts (by 2035)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Temperature Reduction",
        value="-3°C",
        delta="In former heat islands"
    )

with col2:
    st.metric(
        label="Air Quality Improvement",
        value="-40%",
        delta="Pollution reduction"
    )

with col3:
    st.metric(
        label="Green Space",
        value="30%",
        delta="+12% increase"
    )

with col4:
    st.metric(
        label="Sustainable Jobs",
        value="15,000+",
        delta="Green economy"
    )

st.markdown("---")

# Call to action
st.success("""
### 🚀 Next Steps: Implementation Roadmap

**Phase 1 (2025-2027):** Quick wins
- Air quality monitoring network
- First 3 urban parks
- 10,000 street trees
- BRT expansion

**Phase 2 (2027-2030):** Infrastructure
- Water network upgrades
- Green corridors
- Transit improvements
- Zoning reforms

**Phase 3 (2030-2035):** Transformation
- Complete urban forest
- Climate-neutral transport
- Sustainable neighborhoods
- Regional leadership

**Total Investment Required:** $200-250 million over 10 years  
**Return on Investment:** Improved health, productivity, climate resilience, and quality of life for 1+ million residents
""")

st.info("""
### 📥 Data Integration
This page integrates all datasets into comprehensive recommendations. 
Make sure all previous data files are in place for the final dashboard to work properly.
""")
