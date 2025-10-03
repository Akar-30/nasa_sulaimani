# 📋 DATA FILES CHECKLIST

Use this checklist to track your data preparation progress.

## 🎯 Priority 1: Minimum Viable Product (MVP)

Get these 3 files first for a working demo:

- [ ] `air_quality_no2.csv`
      - Columns: date, lat, lon, value
      - Source: Sentinel-5P TROPOMI
      - Impact: Shows pollution hotspots

- [ ] `urban_extent_2025.geojson`
      - GeoJSON polygon of current city boundary
      - Source: Copernicus GHSL or manual digitization
      - Impact: Shows current urban area

- [ ] `temperature_lst.csv` OR `ndvi_values.csv` (choose one)
      - LST columns: date, lat, lon, temperature
      - NDVI columns: date, lat, lon, ndvi
      - Source: Landsat 8/9
      - Impact: Shows heat islands or vegetation

## 📊 Priority 2: Enhanced Visualizations

Add these for better maps (order by impact):

- [ ] `pollution_hotspots.geojson`
      - Polygon boundaries of high-pollution zones
      - Properties: name, pollutant, level, population_affected

- [ ] `heat_islands.geojson`
      - Polygon boundaries of heat island zones
      - Properties: zone_id, avg_temp, temp_above_rural

- [ ] `green_spaces.geojson`
      - Existing parks and vegetation areas
      - Properties: name, type, area_hectares

- [ ] `water_stress_zones.geojson`
      - Areas with water scarcity
      - Properties: zone_name, stress_level, groundwater_decline

- [ ] `population_density.geojson`
      - Neighborhood population data
      - Properties: neighborhood, population, density

## 🕐 Priority 3: Time Series Data

For trend analysis and animations:

- [ ] `urban_extent_2005.geojson`
- [ ] `urban_extent_2010.geojson`
- [ ] `urban_extent_2015.geojson`
- [ ] `urban_extent_2020.geojson`
      - Urban boundaries for different years
      - Enables growth animation

- [ ] `groundwater_trend.csv`
      - Columns: year, month, value
      - Source: GRACE
      - Shows water depletion

- [ ] `precipitation.csv`
      - Columns: year, month, precipitation_mm
      - Source: IMERG
      - Shows rainfall trends

- [ ] `population_growth.csv`
      - Columns: year, zone, population, density_per_km2
      - Source: WorldPop
      - Shows demographic trends

## 📈 Priority 4: Additional Pollutants (Optional)

Enhance air quality section:

- [ ] `air_quality_pm25.csv`
      - Particulate matter data
- [ ] `air_quality_so2.csv`
      - Sulfur dioxide data
- [ ] `air_quality_o3.csv`
      - Ozone data

## ✅ Validation Checklist

Before using each file, verify:

- [ ] File is in `/data` directory
- [ ] Filename matches exactly (case-sensitive)
- [ ] CSV has correct column names
- [ ] No missing values in critical columns
- [ ] Dates in YYYY-MM-DD format
- [ ] Coordinates in WGS84 (EPSG:4326)
- [ ] GeoJSON validated at geojsonlint.com
- [ ] Data covers Sulaimani area (35.48-35.64°N, 45.35-45.52°E)

## 🎯 Quick Win Strategy

### Day 1 Morning (2 hours)

- [ ] Get Sentinel-5P NO2 data → `air_quality_no2.csv`
- [ ] Create simple city boundary → `urban_extent_2025.geojson`

### Day 1 Afternoon (2 hours)

- [ ] Get Landsat LST → `temperature_lst.csv`
- [ ] Test website with these 3 files
- [ ] Verify maps display correctly

### Day 1 Evening (Optional)

- [ ] Add GeoJSON files for better visuals
- [ ] Add time series if time permits

## 📝 Notes & Progress

Track your progress here:

**Data Sources Used:**

- [ ] Google Earth Engine
- [ ] Copernicus Hub
- [ ] NASA Earthdata
- [ ] WorldPop
- [ ] Manual digitization

**Challenges Encountered:**
1.
2.
3.

**Files Still Needed:**
1.
2.
3.

**Next Steps:**
1.
2.
3.

---

## 🔍 File Status Legend

Use these symbols to track status:

- ⬜ Not started
- 🔄 In progress
- ✅ Complete and tested
- ❌ Blocked/issues
- ⏸️ Paused

---

**Updated:** [Add date when you update this]
**Completed:** ____ / 25 files total
**MVP Status:** ____ / 3 essential files
