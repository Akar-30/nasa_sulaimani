# 📥 Data Preparation Guide for Sulaimani Sustainable Growth Platform

This guide helps you prepare NASA Earth observation data for the Sulaimani platform.

## 🎯 Overview

All data files should be placed in the `/data` directory. The platform supports CSV and GeoJSON formats.

---

## 1️⃣ Air Quality Data

### Files Needed

#### `air_quality_no2.csv`

**Source**: Sentinel-5P TROPOMI  
**Format**: CSV  
**Columns**:

- `date` (YYYY-MM-DD): Date of observation
- `lat` (float): Latitude
- `lon` (float): Longitude  
- `value` (float): NO₂ concentration in µg/m³

**Example**:

```csv
date,lat,lon,value
2024-01-15,35.5608,45.4347,45.2
2024-01-15,35.5708,45.4447,52.8
2024-01-15,35.5508,45.4247,38.5
```

#### `air_quality_pm25.csv`

**Source**: MODIS AOD or Sentinel-5P  
**Format**: CSV  
**Columns**: Same as NO₂ file above, but with PM2.5 values

#### `pollution_hotspots.geojson`

**Format**: GeoJSON (Polygon)  
**Properties**:

- `name` (string): Hotspot name
- `pollutant` (string): NO₂, PM2.5, etc.
- `level` (string): "High", "Very High"
- `population_affected` (int): Estimated affected population

**Example**:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[45.414, 35.540], [45.424, 35.540], ...]]
      },
      "properties": {
        "name": "Industrial Zone",
        "pollutant": "PM2.5",
        "level": "Very High",
        "population_affected": 15000
      }
    }
  ]
}
```

#### `population_density.geojson`

**Format**: GeoJSON (Polygon)  
**Properties**:

- `neighborhood` (string): Neighborhood name
- `population` (int): Population count
- `density` (float): People per km²

---

## 2️⃣ Heat & Vegetation Data

### Files Needed

#### `temperature_lst.csv`

**Source**: Landsat 8/9 thermal bands  
**Format**: CSV  
**Columns**:

- `date` (YYYY-MM-DD)
- `lat` (float)
- `lon` (float)
- `temperature` (float): Land Surface Temperature in °C

**Processing Steps**:

1. Download Landsat Collection 2 Level-2 Surface Temperature
2. Cloud mask and quality filter
3. Extract temperature values for Sulaimani bounds
4. Convert Kelvin to Celsius if needed
5. Aggregate to grid or points

#### `ndvi_values.csv`

**Source**: MODIS or Landsat NDVI  
**Format**: CSV  
**Columns**:

- `date` (YYYY-MM-DD)
- `lat` (float)
- `lon` (float)
- `ndvi` (float): NDVI value (-1 to 1)

**Processing Steps**:

1. Calculate NDVI: (NIR - Red) / (NIR + Red)
2. Filter for quality pixels
3. Extract for Sulaimani area

#### `green_spaces.geojson`

**Format**: GeoJSON (Polygon)  
**Properties**:

- `name` (string): Park/green space name
- `type` (string): "park", "agriculture", "forest"
- `area_hectares` (float): Area in hectares

#### `heat_islands.geojson`

**Format**: GeoJSON (Polygon)  
**Properties**:

- `zone_id` (string): Identifier
- `avg_temp` (float): Average summer temperature
- `temp_above_rural` (float): Temperature difference vs rural

---

## 3️⃣ Urban Growth Data

### Files Needed

#### `urban_extent_XXXX.geojson` (for years 2005, 2010, 2015, 2020, 2025)

**Source**: Copernicus GHSL or manual digitization  
**Format**: GeoJSON (Polygon)  
**Properties**:

- `year` (int): Year of extent
- `area_km2` (float): Urban area in km²
- `population` (int): Estimated population

**Processing Steps**:

1. Download GHSL Built-Up Grid
2. Threshold to identify urban pixels
3. Vectorize to polygons
4. Simplify geometry for web display

**Example**:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[45.380, 35.520], ...]]
      },
      "properties": {
        "year": 2025,
        "area_km2": 182.5,
        "population": 750000
      }
    }
  ]
}
```

#### `population_growth.csv`

**Source**: WorldPop  
**Format**: CSV  
**Columns**:

- `year` (int)
- `zone` (string): Geographic zone/neighborhood
- `population` (int)
- `density_per_km2` (float)

---

## 4️⃣ Water Resources Data

### Files Needed

#### `groundwater_trend.csv`

**Source**: NASA GRACE  
**Format**: CSV  
**Columns**:

- `year` (int): Year
- `month` (int): Month (1-12)
- `value` (float): Liquid water equivalent thickness anomaly (cm)

**Processing Steps**:

1. Download GRACE Mascon data
2. Extract values for Sulaimani region
3. Calculate anomalies vs baseline period
4. Annual or seasonal aggregation

**Example**:

```csv
year,month,value
2003,1,0.0
2003,2,-0.5
2004,1,-1.2
...
2025,10,-33.2
```

#### `precipitation.csv`

**Source**: IMERG or TRMM  
**Format**: CSV  
**Columns**:

- `year` (int)
- `month` (int, optional)
- `precipitation_mm` (float): Monthly or annual precipitation

#### `water_stress_zones.geojson`

**Format**: GeoJSON (Polygon)  
**Properties**:

- `zone_name` (string)
- `stress_level` (string): "Low", "Medium", "High", "Very High"
- `groundwater_decline` (float): cm/year decline rate
- `population` (int): Affected population

---

## 🛠️ Data Processing Tools & Resources

### Recommended Tools

1. **Google Earth Engine** (Recommended for beginners)
   - Pre-processed datasets
   - Cloud computing
   - Export to Drive as CSV/GeoJSON
   - [Code Editor](https://code.earthengine.google.com/)

2. **Python Libraries**:

   ```python
   # Install
   pip install earthengine-api geopandas rasterio pandas
   
   # Example: Load and process Landsat
   import ee
   import geemap
   
   ee.Initialize()
   
   # Define Sulaimani area
   roi = ee.Geometry.Rectangle([45.35, 35.48, 45.52, 35.64])
   
   # Get Landsat LST
   landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
       .filterBounds(roi) \
       .filterDate('2024-06-01', '2024-08-31')
   ```

3. **QGIS** (For GeoJSON creation)
   - Free GIS software
   - Digitize urban boundaries
   - Convert rasters to vectors
   - Export as GeoJSON

### Data Access Links

- **NASA Earthdata**: <https://earthdata.nasa.gov/>
- **Copernicus Hub**: <https://scihub.copernicus.eu/>
- **Google Earth Engine**: <https://earthengine.google.com/>
- **WorldPop**: <https://www.worldpop.org/>
- **GRACE Data**: <https://grace.jpl.nasa.gov/data/get-data/>

---

## ✅ Data Quality Checklist

Before adding your data, verify:

- [ ] Files are named exactly as specified
- [ ] CSV files have correct column names
- [ ] Dates are in YYYY-MM-DD format
- [ ] Coordinates are in WGS84 (EPSG:4326)
- [ ] GeoJSON files are valid (use [geojson.io](http://geojson.io))
- [ ] No missing values in critical columns
- [ ] File sizes are reasonable (<50 MB for web display)
- [ ] Data covers the Sulaimani area (35.48-35.64°N, 45.35-45.52°E)

---

## 🔍 Validation Script

Run this Python script to check your data:

```python
import pandas as pd
import geopandas as gpd
from pathlib import Path

DATA_DIR = Path("data")

# Check CSV files
csv_files = {
    "air_quality_no2.csv": ["date", "lat", "lon", "value"],
    "temperature_lst.csv": ["date", "lat", "lon", "temperature"],
    # ... add more
}

for filename, required_cols in csv_files.items():
    filepath = DATA_DIR / filename
    if filepath.exists():
        df = pd.read_csv(filepath)
        missing = set(required_cols) - set(df.columns)
        if missing:
            print(f"❌ {filename}: Missing columns {missing}")
        else:
            print(f"✅ {filename}: OK ({len(df)} rows)")
    else:
        print(f"⚠️  {filename}: Not found")

# Check GeoJSON files
geojson_files = [
    "pollution_hotspots.geojson",
    "green_spaces.geojson",
    # ... add more
]

for filename in geojson_files:
    filepath = DATA_DIR / filename
    if filepath.exists():
        try:
            gdf = gpd.read_file(filepath)
            print(f"✅ {filename}: OK ({len(gdf)} features)")
        except Exception as e:
            print(f"❌ {filename}: Error - {e}")
    else:
        print(f"⚠️  {filename}: Not found")
```

---

## 📞 Need Help?

If you encounter issues:

1. Check file formats match specifications exactly
2. Validate GeoJSON at [geojsonlint.com](https://geojsonlint.com/)
3. Ensure coordinates are within Sulaimani bounds
4. Review NASA data documentation
5. Contact the team

---

## 🚀 Next Steps

1. **Download raw NASA data** from sources above
2. **Process data** using Earth Engine or Python
3. **Save files** in `/data` directory with correct names
4. **Run validation script** to check
5. **Launch app** with `streamlit run Home.py`
6. **Verify visualizations** appear correctly

Good luck with your data preparation! 🌍
