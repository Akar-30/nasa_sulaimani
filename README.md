# 🌍 Sulaimani Sustainable Growth Platform

An interactive web platform using NASA Earth observation data to guide sustainable urban development in Sulaimani City, Iraqi Kurdistan.

## 🎯 Project Goal

Answer the ultimate question: **"How can Sulaimani City grow sustainably to ensure both people's wellbeing and environmental resilience, informed by NASA Earth observation data?"**

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run Home.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
nasa_sulaimani/
├── Home.py                          # Main landing page
├── pages/
│   ├── 1_🏙️_The_Challenge.py       # Urban challenges overview
│   ├── 2_📊_Data_Pathway.py        # Data sources and methods
│   ├── 3_💨_Air_Quality.py         # Air pollution analysis
│   ├── 4_🌡️_Heat_Greenspace.py    # Heat islands and vegetation
│   ├── 5_🏗️_Urban_Growth_Water.py # Urban expansion and water
│   ├── 6_✅_Solutions_Vision.py     # Recommendations
│   └── 7_👥_About_Team.py          # About and credits
├── data/                            # NASA datasets (add your files here)
├── utils/
│   ├── __init__.py
│   └── data_loader.py              # Data processing utilities
├── assets/                          # Images and static files
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 📥 Data Requirements

Place your processed NASA data files in the `/data` directory. See `DATA_GUIDE.md` for detailed specifications.

### Required Files

**Air Quality:**

- `air_quality_no2.csv` (columns: date, lat, lon, value)
- `air_quality_pm25.csv` (columns: date, lat, lon, value)
- `pollution_hotspots.geojson`
- `population_density.geojson`

**Heat & Vegetation:**

- `temperature_lst.csv` (columns: date, lat, lon, temperature)
- `ndvi_values.csv` (columns: date, lat, lon, ndvi)
- `green_spaces.geojson`
- `heat_islands.geojson`

**Urban Growth:**

- `urban_extent_2005.geojson`
- `urban_extent_2010.geojson`
- `urban_extent_2015.geojson`
- `urban_extent_2020.geojson`
- `urban_extent_2025.geojson`
- `population_growth.csv`

**Water Resources:**

- `groundwater_trend.csv` (columns: year, value)
- `precipitation.csv` (columns: year, value)
- `water_stress_zones.geojson`

## 🛰️ NASA Data Sources

- **Sentinel-5P (TROPOMI)**: Air quality (NO₂, PM2.5, SO₂, O₃)
- **MODIS**: Aerosol Optical Depth, NDVI
- **Landsat 8/9**: Land Surface Temperature, high-resolution imagery
- **GRACE**: Groundwater availability
- **IMERG**: Precipitation data
- **Copernicus GHSL**: Urban built-up areas
- **WorldPop**: Population density

## 🎨 Features

✅ Interactive maps with multiple data layers  
✅ Time-series analysis and trends  
✅ Pollution and heat island identification  
✅ Urban growth tracking  
✅ Water resource assessment  
✅ Actionable recommendations  
✅ Mobile-responsive design  

## 🛠️ Technology Stack

- **Streamlit**: Web framework
- **Folium**: Interactive maps
- **Plotly**: Data visualizations
- **Pandas/GeoPandas**: Data processing
- **Python 3.9+**: Programming language

## 📊 Usage

### For Data Scientists

1. Add your processed NASA data to the `/data` folder
2. Use `utils/data_loader.py` functions to load and process data
3. Update visualizations in the page files

### For Urban Planners

1. Navigate through the pages using the sidebar
2. Filter maps by date, pollutant type, or neighborhood
3. Export insights for planning decisions

### For Developers

1. Fork the repository
2. Add new features or visualizations
3. Submit pull requests

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Select `Home.py` as the main file
5. Deploy!

## 📝 Customization

### Change Theme

Edit `.streamlit/config.toml` to customize colors

### Add New Pages

Create new files in `pages/` directory following the naming pattern: `X_emoji_Name.py`

### Modify Maps

Edit the Folium map configurations in each page file

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - Feel free to use and adapt this project

## 🙏 Acknowledgments

- NASA for Earth observation data
- ESA Copernicus for Sentinel data
- Space Apps Challenge organizers
- Sulaimani community
- Open-source community

## 📧 Contact

- GitHub: [your-repo-link]
- Email: <team@sulaimani-growth.org>
- Twitter: @SulaimaniGrowth

---

🚀 Built for NASA Space Apps Challenge 2025  
🌍 Making Sulaimani a model for sustainable urban growth
