# 🛰️ Sentinel-5P NO₂ Data Download Guide

## Overview

This guide helps you download real NO₂ (nitrogen dioxide) air quality data from the Sentinel-5P satellite for Sulaimani and integrate it into your website.

## 📋 Prerequisites

### 1. Install Required Packages

```bash
pip install pystac pystac-client requests netCDF4
```

Or install all packages from requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python -c "import pystac_client; print('✅ PySTAC Client installed')"
python -c "import netCDF4; print('✅ NetCDF4 installed')"
```

## 🚀 Quick Start (3 Steps)

### Step 1: Download NO₂ Satellite Data

Run the download script to get recent Sentinel-5P NO₂ data:

```bash
python download_no2_data.py
```

**What it does:**
- Searches for NO₂ products from Sentinel-5P satellite
- Filters data for Sulaimani area (45.25-45.62°E, 35.40-35.72°N)
- Downloads last 30 days of satellite passes
- Saves NetCDF files to `data/raw_no2/` directory

**Expected output:**
```
Found 8 NO₂ products for Sulaimani

1. Product ID: S5P_PAL__L2__NO2____20241006T...
   Time: 2024-10-06T22:32:02
   Orbit: 36186
   File: S5P_PAL__L2__NO2____20241006T223202_20241007T001331_36186_03_020001_20241015T143245.nc
   Size: 45.23 MB

Download all products? (y/n) [default: y]: y
```

### Step 2: Process NetCDF Files to CSV

Convert the downloaded satellite data to Streamlit-ready CSV format:

```bash
python process_no2_netcdf.py
```

**What it does:**
- Reads all NetCDF files from `data/raw_no2/`
- Extracts NO₂ tropospheric column values
- Filters for Sulaimani bounding box
- Converts units from mol/m² to µg/m³
- Saves to `data/air_quality_no2.csv`

**Output format:**
```csv
date,lat,lon,value
2024-10-06,35.5608,45.4347,52.34
2024-10-06,35.5612,45.4351,48.91
...
```

### Step 3: View in Streamlit

Your Air Quality page will automatically load the data:

```bash
streamlit run Home.py
```

Navigate to **"💨 Air Quality"** page to see:
- NO₂ concentration heatmap
- Population exposure overlay
- Temporal trends
- WHO guideline comparisons

## 📊 Understanding the Data

### Sentinel-5P NO₂ Data

**Satellite:** Sentinel-5P TROPOMI instrument  
**Coverage:** Global, daily passes  
**Resolution:** ~7 × 3.5 km at nadir  
**Unit:** Tropospheric NO₂ column (mol/m²)  
**Converted to:** µg/m³ for air quality comparison

### NO₂ Health Guidelines

| Level | NO₂ (µg/m³) | Health Impact |
|-------|-------------|---------------|
| **Good** | 0-40 | WHO guideline (annual) |
| **Moderate** | 40-80 | Sensitive groups may experience effects |
| **Unhealthy** | 80-120 | General population affected |
| **Very Unhealthy** | >120 | Serious health effects |

### Data Quality

- **Quality assurance filtering:** Only pixels with QA ≥ 50% are included
- **Cloud screening:** Cloudy pixels are automatically removed
- **Valid data:** Non-negative, non-NaN values only
- **Deduplication:** Multiple measurements averaged for same location

## 🔧 Advanced Usage

### Custom Date Range

Edit `download_no2_data.py` to specify exact dates:

```python
# Download data for January 2024
items = search_by_date_range("2024-01-01", "2024-01-31")
```

### Download More Products

Increase the search limit:

```python
# Get up to 50 products (default is 10)
download_recent_no2_data(days_back=90, max_products=50)
```

### Filter by Pollution Level

After processing, filter for hotspots only:

```python
import pandas as pd
df = pd.read_csv('data/air_quality_no2.csv')

# Keep only high pollution areas (>80 µg/m³)
hotspots = df[df['value'] > 80]
hotspots.to_csv('data/pollution_hotspots.csv', index=False)
```

## 📁 File Structure

```
nasa_sulaimani/
├── data/
│   ├── raw_no2/                          # Downloaded NetCDF files (large)
│   │   └── S5P_PAL__L2__NO2____*.nc
│   ├── air_quality_no2.csv               # Processed data (Streamlit-ready) ✅
│   ├── pollution_hotspots.csv            # High pollution areas only
│   └── no2_products_list.json            # Product metadata
├── download_no2_data.py                  # Step 1: Download script
├── process_no2_netcdf.py                 # Step 2: Processing script
└── pages/3_💨_Air_Quality.py             # Uses the data automatically
```

## 🐛 Troubleshooting

### Issue: "No products found"

**Cause:** No satellite passes over Sulaimani in the time period  
**Solution:**
- Increase `days_back` parameter (try 60 or 90 days)
- Sentinel-5P has daily coverage, but some days may have data quality issues
- Check S5P-PAL service status: https://data-portal.s5p-pal.com

### Issue: "No valid data found for Sulaimani area"

**Cause:** Cloud cover or quality filtering removed all pixels  
**Solution:**
- Try different dates/products
- Lower quality threshold in `process_no2_netcdf.py` (change `qa_flat >= 0.5` to `0.3`)
- Check if product footprint actually covers Sulaimani (view product metadata)

### Issue: NetCDF processing errors

**Common variable names differ between S5P products**  
**Solution:** The script checks multiple variable names automatically:
- `nitrogendioxide_tropospheric_column`
- `nitrogen_dioxide_tropospheric_column`
- `NO2_column_number_density`

If none match, check the NetCDF file structure:

```python
import netCDF4 as nc
ds = nc.Dataset('data/raw_no2/yourfile.nc')
print(list(ds.groups['PRODUCT'].variables.keys()))
```

### Issue: Download very slow

**Cause:** Large file sizes (40-60 MB per product)  
**Solutions:**
- Download fewer products (reduce `max_products`)
- Use faster internet connection
- Download during off-peak hours
- Files are downloaded with progress indication

### Issue: Packages not found

```bash
pip install --upgrade pystac pystac-client netCDF4 requests
```

If still failing:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📈 Expected Results

### Typical Sulaimani NO₂ Values

Based on similar Middle Eastern cities:
- **Urban center:** 40-80 µg/m³
- **Residential areas:** 20-50 µg/m³
- **Industrial zones:** 60-120 µg/m³
- **Rural suburbs:** 10-30 µg/m³

### Data Density

- **1 satellite pass:** ~50-200 pixels over Sulaimani
- **30 days of data:** 500-2,000 data points
- **After deduplication:** ~300-800 unique locations

## 🎯 Integration with Your Website

### Automatic Features

Once `air_quality_no2.csv` exists, your Air Quality page will:

✅ Load real NO₂ data automatically  
✅ Display heatmap overlay on the map  
✅ Show temporal trends  
✅ Compare with WHO guidelines  
✅ Calculate affected population (when overlaid with population data)

### Manual Enhancements

You can further customize in `pages/3_💨_Air_Quality.py`:

1. **Add seasonal analysis:**
```python
df['month'] = pd.to_datetime(df['date']).dt.month
winter = df[df['month'].isin([12, 1, 2])]
```

2. **Calculate neighborhood averages:**
```python
# Combine with neighborhood_population.csv
# Show average NO₂ per zone
```

3. **Create pollution risk index:**
```python
# Combine NO₂ levels with population density
# High pollution + high population = high risk
```

## 📚 API Reference

### S5P-PAL STAC Catalog

- **Base URL:** https://data-portal.s5p-pal.com/api/s5p-l2
- **Documentation:** https://data-portal.s5p-pal.com
- **Product type:** `L2__NO2___` (NO₂ tropospheric column)
- **Format:** NetCDF-4
- **License:** Copernicus Data (free to use)

### Data Attribution

When presenting your results, include:

> **Data Source:** Sentinel-5P/TROPOMI NO₂ data processed by Sentinel-5P Product Algorithm Laboratory (S5P-PAL). Contains modified Copernicus Sentinel data.

## 🔄 Automation (Optional)

### Schedule Daily Downloads

Create a cron job or Windows Task Scheduler to run:

```bash
# Download yesterday's data
python download_no2_data.py --date yesterday

# Process and update CSV
python process_no2_netcdf.py
```

### Keep Only Recent Data

To save disk space, clean old NetCDF files:

```python
# Add to process_no2_netcdf.py
import os
import glob

# Delete NetCDF files after processing
for nc_file in glob.glob('data/raw_no2/*.nc'):
    os.remove(nc_file)
print("✅ Cleaned up NetCDF files")
```

## 💡 Tips for Best Results

1. **Download multiple dates** - More data = better visualization and trends
2. **Check cloud cover** - Products with heavy clouds have less valid pixels
3. **Combine with population data** - Show impact on residents
4. **Create time series** - Track pollution changes over months
5. **Validate with ground stations** - If available in Sulaimani

## 🎓 Learning Resources

- **Sentinel-5P User Guide:** https://sentinel.esa.int/web/sentinel/user-guides/sentinel-5p-tropomi
- **TROPOMI NO₂ ATBD:** https://sentinel.esa.int/documents/247904/2476257/Sentinel-5P-TROPOMI-ATBD-NO2-data-products
- **PySTAC Documentation:** https://pystac.readthedocs.io/
- **NetCDF Tutorial:** https://unidata.github.io/netcdf4-python/

---

**Next Steps:**
1. Run `python download_no2_data.py`
2. Run `python process_no2_netcdf.py`
3. Open your Streamlit app and view Air Quality page
4. Repeat for other pollutants (PM2.5, SO₂, O₃) if needed!

Good luck with your NASA Space Apps Challenge project! 🚀
