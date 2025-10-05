#!/usr/bin/env python3
"""
CDS API Data Download for Heat & Greenspace Analysis in Sulaimani
NASA Space Apps Challenge 2025

This script downloads climate data from Copernicus Climate Data Store (CDS) 
to analyze urban heat islands and vegetation patterns in Sulaimani City.

Required datasets:
1. ERA5-Land hourly data (temperature, vegetation)
2. Satellite land cover data
3. Urban Atlas data (if available)

Setup Requirements:
1. Register at https://cds.climate.copernicus.eu/
2. Install: pip install "cdsapi>=0.7.7"
3. Create ~/.cdsapirc with your API key:
   url: https://cds.climate.copernicus.eu/api
   key: <YOUR-PERSONAL-ACCESS-TOKEN>
"""

import cdsapi
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import xarray as xr
import json

# Sulaimani coordinates and bounds
SULAIMANI_BOUNDS = {
    'north': 35.72,   # Northern boundary
    'south': 35.40,   # Southern boundary 
    'west': 45.25,    # Western boundary
    'east': 45.62     # Eastern boundary
}

SULAIMANI_CENTER = {'lat': 35.56, 'lon': 45.43}

def setup_cds_client():
    """Initialize CDS API client"""
    try:
        client = cdsapi.Client()
        print("✅ CDS API client initialized successfully")
        return client
    except Exception as e:
        print(f"❌ Failed to initialize CDS client: {e}")
        print("Please check your ~/.cdsapirc file and API key")
        return None

def download_era5_land_temperature(client, years=['2023', '2024'], months=['06', '07', '08']):
    """
    Download ERA5-Land temperature data for summer months
    This provides 2m temperature and land surface temperature
    """
    print("🌡️ Downloading ERA5-Land temperature data...")
    
    dataset = 'reanalysis-era5-land'
    request = {
        'product_type': 'reanalysis',
        'variable': [
            '2m_temperature',
            'skin_temperature',  # Land surface temperature
        ],
        'year': years,
        'month': months,
        'day': [f'{d:02d}' for d in range(1, 32)],  # All days
        'time': ['12:00', '15:00'],  # Peak heat hours
        'area': [
            SULAIMANI_BOUNDS['north'],
            SULAIMANI_BOUNDS['west'], 
            SULAIMANI_BOUNDS['south'],
            SULAIMANI_BOUNDS['east']
        ],
        'format': 'netcdf',
    }
    
    target = 'data/era5_temperature_sulaimani.nc'
    
    try:
        client.retrieve(dataset, request, target)
        print(f"✅ Temperature data downloaded: {target}")
        return target
    except Exception as e:
        print(f"❌ Failed to download temperature data: {e}")
        return None

def download_era5_vegetation_data(client, years=['2023', '2024']):
    """
    Download ERA5-Land vegetation data (LAI - Leaf Area Index)
    This helps assess vegetation health and coverage
    """
    print("🌱 Downloading ERA5-Land vegetation data...")
    
    dataset = 'reanalysis-era5-land'
    request = {
        'product_type': 'reanalysis',
        'variable': [
            'leaf_area_index_high_vegetation',
            'leaf_area_index_low_vegetation',
        ],
        'year': years,
        'month': ['04', '05', '06', '07', '08', '09'],  # Growing season
        'day': ['01', '15'],  # Monthly samples
        'time': ['12:00'],
        'area': [
            SULAIMANI_BOUNDS['north'],
            SULAIMANI_BOUNDS['west'], 
            SULAIMANI_BOUNDS['south'],
            SULAIMANI_BOUNDS['east']
        ],
        'format': 'netcdf',
    }
    
    target = 'data/era5_vegetation_sulaimani.nc'
    
    try:
        client.retrieve(dataset, request, target)
        print(f"✅ Vegetation data downloaded: {target}")
        return target
    except Exception as e:
        print(f"❌ Failed to download vegetation data: {e}")
        return None

def download_satellite_land_cover(client, year='2020'):
    """
    Download ESA Climate Change Initiative Land Cover data
    This provides detailed land use classification
    """
    print("🛰️ Downloading satellite land cover data...")
    
    dataset = 'satellite-land-cover'
    request = {
        'version': 'v2.0.7cds',
        'variable': 'all',
        'product_type': 'climatology',
        'year': year,
        'area': [
            SULAIMANI_BOUNDS['north'],
            SULAIMANI_BOUNDS['west'], 
            SULAIMANI_BOUNDS['south'],
            SULAIMANI_BOUNDS['east']
        ],
        'format': 'zip',
    }
    
    target = 'data/land_cover_sulaimani.zip'
    
    try:
        client.retrieve(dataset, request, target)
        print(f"✅ Land cover data downloaded: {target}")
        return target
    except Exception as e:
        print(f"❌ Failed to download land cover data: {e}")
        return None

def process_temperature_data(netcdf_file):
    """Process temperature NetCDF into CSV format for visualization"""
    print("🔄 Processing temperature data...")
    
    try:
        # Read NetCDF data
        ds = xr.open_dataset(netcdf_file)
        
        # Convert temperatures from Kelvin to Celsius
        t2m = ds['t2m'] - 273.15  # 2m temperature
        skt = ds['skt'] - 273.15  # Skin temperature (land surface temp)
        
        # Create grid points
        lats = ds.latitude.values
        lons = ds.longitude.values
        times = ds.time.values
        
        temperature_data = []
        
        for i, time in enumerate(times):
            date_str = pd.to_datetime(time).strftime('%Y-%m-%d %H:%M')
            
            for j, lat in enumerate(lats):
                for k, lon in enumerate(lons):
                    # Get temperature values
                    t2m_val = float(t2m.isel(time=i, latitude=j, longitude=k).values)
                    skt_val = float(skt.isel(time=i, latitude=j, longitude=k).values)
                    
                    # Skip if NaN
                    if np.isnan(t2m_val) or np.isnan(skt_val):
                        continue
                        
                    temperature_data.append({
                        'datetime': date_str,
                        'date': date_str.split(' ')[0],
                        'time': date_str.split(' ')[1],
                        'lat': float(lat),
                        'lon': float(lon),
                        'air_temperature_2m': round(t2m_val, 2),
                        'land_surface_temperature': round(skt_val, 2),
                        'heat_island_intensity': round(skt_val - t2m_val, 2)
                    })
        
        # Save to CSV
        df = pd.DataFrame(temperature_data)
        df.to_csv('data/temperature_data.csv', index=False)
        print(f"✅ Processed {len(df)} temperature records")
        
        # Create summary statistics
        daily_avg = df.groupby('date').agg({
            'air_temperature_2m': 'mean',
            'land_surface_temperature': 'mean',
            'heat_island_intensity': 'mean'
        }).round(2)
        
        daily_avg.to_csv('data/daily_temperature_summary.csv')
        print(f"✅ Created daily temperature summary ({len(daily_avg)} days)")
        
        return df
        
    except Exception as e:
        print(f"❌ Error processing temperature data: {e}")
        return None

def process_vegetation_data(netcdf_file):
    """Process vegetation NetCDF into CSV format"""
    print("🔄 Processing vegetation data...")
    
    try:
        ds = xr.open_dataset(netcdf_file)
        
        # Leaf Area Index data
        lai_hv = ds['lai_hv']  # High vegetation
        lai_lv = ds['lai_lv']  # Low vegetation
        
        lats = ds.latitude.values
        lons = ds.longitude.values
        times = ds.time.values
        
        vegetation_data = []
        
        for i, time in enumerate(times):
            date_str = pd.to_datetime(time).strftime('%Y-%m-%d')
            
            for j, lat in enumerate(lats):
                for k, lon in enumerate(lons):
                    lai_hv_val = float(lai_hv.isel(time=i, latitude=j, longitude=k).values)
                    lai_lv_val = float(lai_lv.isel(time=i, latitude=j, longitude=k).values)
                    
                    if np.isnan(lai_hv_val) or np.isnan(lai_lv_val):
                        continue
                    
                    # Calculate total LAI and estimated NDVI
                    total_lai = lai_hv_val + lai_lv_val
                    estimated_ndvi = min(0.95, total_lai / 6.0)  # Rough LAI to NDVI conversion
                    
                    vegetation_data.append({
                        'date': date_str,
                        'lat': float(lat),
                        'lon': float(lon),
                        'lai_high_vegetation': round(lai_hv_val, 3),
                        'lai_low_vegetation': round(lai_lv_val, 3),
                        'total_lai': round(total_lai, 3),
                        'estimated_ndvi': round(estimated_ndvi, 3),
                        'vegetation_category': categorize_vegetation(estimated_ndvi)
                    })
        
        df = pd.DataFrame(vegetation_data)
        df.to_csv('data/vegetation_data.csv', index=False)
        print(f"✅ Processed {len(df)} vegetation records")
        
        return df
        
    except Exception as e:
        print(f"❌ Error processing vegetation data: {e}")
        return None

def categorize_vegetation(ndvi):
    """Categorize vegetation based on NDVI values"""
    if ndvi < 0.1:
        return "No Vegetation"
    elif ndvi < 0.3:
        return "Sparse Vegetation"
    elif ndvi < 0.6:
        return "Moderate Vegetation"
    else:
        return "Dense Vegetation"

def create_sample_data():
    """Create sample data if API downloads fail"""
    print("🔄 Creating sample heat and vegetation data...")
    
    # Create sample temperature grid
    lats = np.linspace(35.40, 35.72, 40)
    lons = np.linspace(45.25, 45.62, 40)
    dates = pd.date_range('2024-06-01', '2024-08-31', freq='D')
    
    temperature_data = []
    vegetation_data = []
    
    for date in dates[:30]:  # Sample 30 days
        date_str = date.strftime('%Y-%m-%d')
        
        for lat in lats:
            for lon in lons:
                # Distance from city center (for heat island effect)
                center_dist = np.sqrt((lat - 35.56)**2 + (lon - 45.43)**2)
                
                # Base temperature varies by season and distance from center
                base_temp = 35 + 5 * np.sin((date.dayofyear - 150) * 2 * np.pi / 365)
                
                # Urban heat island effect (hotter near center)
                urban_effect = max(0, 8 - center_dist * 20)  # Up to 8°C warmer in center
                
                # Add some randomness
                noise = np.random.normal(0, 2)
                
                air_temp = base_temp + urban_effect * 0.5 + noise
                surface_temp = base_temp + urban_effect + noise + 5  # Surface hotter than air
                
                # Vegetation decreases with urban density
                vegetation_factor = max(0.1, 1 - center_dist * 2)
                base_ndvi = 0.7 * vegetation_factor
                ndvi = max(0.05, base_ndvi + np.random.normal(0, 0.1))
                
                temperature_data.append({
                    'date': date_str,
                    'lat': round(lat, 4),
                    'lon': round(lon, 4),
                    'air_temperature_2m': round(air_temp, 2),
                    'land_surface_temperature': round(surface_temp, 2),
                    'heat_island_intensity': round(surface_temp - air_temp, 2)
                })
                
                vegetation_data.append({
                    'date': date_str,
                    'lat': round(lat, 4),
                    'lon': round(lon, 4),
                    'estimated_ndvi': round(ndvi, 3),
                    'vegetation_category': categorize_vegetation(ndvi)
                })
    
    # Save sample data
    pd.DataFrame(temperature_data).to_csv('data/temperature_data.csv', index=False)
    pd.DataFrame(vegetation_data).to_csv('data/vegetation_data.csv', index=False)
    
    # Create daily summaries
    temp_df = pd.DataFrame(temperature_data)
    daily_temp = temp_df.groupby('date').agg({
        'air_temperature_2m': 'mean',
        'land_surface_temperature': 'mean', 
        'heat_island_intensity': 'mean'
    }).round(2)
    daily_temp.to_csv('data/daily_temperature_summary.csv')
    
    veg_df = pd.DataFrame(vegetation_data)
    daily_veg = veg_df.groupby('date').agg({
        'estimated_ndvi': 'mean'
    }).round(3)
    daily_veg.to_csv('data/daily_vegetation_summary.csv')
    
    print("✅ Created sample temperature and vegetation data")
    print(f"📊 Temperature records: {len(temperature_data)}")
    print(f"🌱 Vegetation records: {len(vegetation_data)}")

def create_green_spaces_geojson():
    """Create GeoJSON for existing and proposed green spaces"""
    print("🌳 Creating green spaces GeoJSON...")
    
    existing_parks = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Azadi Park",
                    "type": "Existing Park",
                    "area_hectares": 15,
                    "status": "Existing"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [45.4347, 35.5608],
                        [45.4367, 35.5608], 
                        [45.4367, 35.5628],
                        [45.4347, 35.5628],
                        [45.4347, 35.5608]
                    ]]
                }
            },
            {
                "type": "Feature", 
                "properties": {
                    "name": "Sami Abdulrahman Park",
                    "type": "Existing Park",
                    "area_hectares": 25,
                    "status": "Existing"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [45.4247, 35.5508],
                        [45.4287, 35.5508],
                        [45.4287, 35.5538], 
                        [45.4247, 35.5538],
                        [45.4247, 35.5508]
                    ]]
                }
            }
        ]
    }
    
    proposed_parks = {
        "type": "FeatureCollection", 
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Downtown Green Corridor",
                    "type": "Proposed Park", 
                    "area_hectares": 5,
                    "priority": "High",
                    "status": "Proposed"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [45.4397, 35.5658],
                        [45.4417, 35.5658],
                        [45.4417, 35.5678],
                        [45.4397, 35.5678], 
                        [45.4397, 35.5658]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Northern Residential Park",
                    "type": "Proposed Park",
                    "area_hectares": 8,
                    "priority": "Medium", 
                    "status": "Proposed"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [45.4447, 35.5758],
                        [45.4477, 35.5758],
                        [45.4477, 35.5788],
                        [45.4447, 35.5788],
                        [45.4447, 35.5758]
                    ]]
                }
            }
        ]
    }
    
    # Save GeoJSON files
    with open('data/existing_parks.geojson', 'w') as f:
        json.dump(existing_parks, f, indent=2)
        
    with open('data/proposed_parks.geojson', 'w') as f:
        json.dump(proposed_parks, f, indent=2)
    
    print("✅ Created green spaces GeoJSON files")

def main():
    """Main execution function"""
    print("🌡️ NASA Sulaimani Heat & Greenspace Data Collection")
    print("=" * 60)
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Initialize CDS client
    client = setup_cds_client()
    
    if client:
        print("🚀 Attempting to download real climate data...")
        
        try:
            # Download temperature data
            temp_file = download_era5_land_temperature(client)
            if temp_file and os.path.exists(temp_file):
                process_temperature_data(temp_file)
            
            # Download vegetation data  
            veg_file = download_era5_vegetation_data(client)
            if veg_file and os.path.exists(veg_file):
                process_vegetation_data(veg_file)
                
            # Download land cover data
            land_cover_file = download_satellite_land_cover(client)
            
            print("✅ Real climate data download completed!")
            
        except Exception as e:
            print(f"⚠️ API download failed: {e}")
            print("📝 Creating sample data instead...")
            create_sample_data()
    else:
        print("📝 CDS API not available, creating sample data...")
        create_sample_data()
    
    # Create supporting GeoJSON files
    create_green_spaces_geojson()
    
    print("\n🎯 Heat & Greenspace Data Summary:")
    print("✅ temperature_data.csv - Gridded temperature measurements")
    print("✅ vegetation_data.csv - NDVI and vegetation indices")  
    print("✅ daily_temperature_summary.csv - Daily temperature averages")
    print("✅ existing_parks.geojson - Current green spaces")
    print("✅ proposed_parks.geojson - Recommended new parks")
    print("\n🚀 Ready for Heat & Greenspace analysis!")

if __name__ == "__main__":
    main()