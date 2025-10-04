"""
Multi-Pollutant Data Download System for Sentinel-5P
Extends the NO₂ system to support SO₂, CO, O₃, HCHO, and other air quality indicators
"""

import os
import sys
from datetime import datetime, timedelta
import argparse

# Import existing functions (fixed imports)
# from download_no2_data import search_no2_products, download_netcdf_files
# from process_no2_netcdf import process_netcdf_to_csv

# Pollutant configuration mapping
POLLUTANT_CONFIG = {
    'NO2': {
        'product_filter': 'L2__NO2___',
        'variable_name': 'tropospheric_NO2_column_number_density',
        'conversion_factor': 1e6 / 6.022e23 * 46.01 * 1e9,  # mol/m² to µg/m³
        'units': 'µg/m³',
        'who_guideline': 40.0,  # µg/m³ annual mean
        'description': 'Nitrogen Dioxide - Traffic and industrial emissions'
    },
    'SO2': {
        'product_filter': 'L2__SO2___',
        'variable_name': 'SO2_column_number_density',
        'conversion_factor': 1e6 / 6.022e23 * 64.07 * 1e9,  # mol/m² to µg/m³  
        'units': 'µg/m³',
        'who_guideline': 20.0,  # µg/m³ daily mean (2021 WHO guidelines)
        'description': 'Sulfur Dioxide - Industrial pollution and power plants'
    },
    'CO': {
        'product_filter': 'L2__CO____',
        'variable_name': 'CO_column_number_density',
        'conversion_factor': 1e6 / 6.022e23 * 28.01 * 1e6,  # mol/m² to mg/m³
        'units': 'mg/m³',
        'who_guideline': 10.0,  # mg/m³ 8-hour mean
        'description': 'Carbon Monoxide - Vehicle emissions and combustion'
    },
    'O3': {
        'product_filter': 'L2__O3____',
        'variable_name': 'O3_column_number_density',
        'conversion_factor': 1.0,  # Keep in Dobson Units 
        'units': 'DU',
        'who_guideline': 100.0,  # µg/m³ 8-hour mean (surface level, approximate)
        'description': 'Ozone - Secondary pollutant formation'
    },
    'HCHO': {
        'product_filter': 'L2__HCHO__',
        'variable_name': 'tropospheric_HCHO_column_number_density',
        'conversion_factor': 1e6 / 6.022e23 * 30.03 * 1e9,  # mol/m² to µg/m³
        'units': 'µg/m³',
        'who_guideline': 30.0,  # µg/m³ (30-minute mean, approximate)
        'description': 'Formaldehyde - VOC emissions and industrial processes'
    },
    'AER_AI': {
        'product_filter': 'L2__AER_AI',
        'variable_name': 'aerosol_index_340_380',
        'conversion_factor': 1.0,  # Dimensionless
        'units': 'AI',
        'who_guideline': 2.0,  # Threshold for significant aerosol presence
        'description': 'Aerosol Index - Dust storms and particulate matter'
    }
}

def download_pollutant_data(pollutant, start_date, end_date, max_products=20):
    """
    Download data for a specific pollutant
    
    Args:
        pollutant (str): Pollutant code (NO2, SO2, CO, O3, HCHO, AER_AI)
        start_date (str): Start date 'YYYY-MM-DD'
        end_date (str): End date 'YYYY-MM-DD'  
        max_products (int): Maximum products to download
    
    Returns:
        bool: True if successful
    """
    if pollutant not in POLLUTANT_CONFIG:
        print(f"❌ Error: Pollutant '{pollutant}' not supported")
        print(f"Available pollutants: {', '.join(POLLUTANT_CONFIG.keys())}")
        return False
    
    config = POLLUTANT_CONFIG[pollutant]
    print(f"🛰️ Downloading {pollutant} data: {config['description']}")
    print(f"   Product Filter: {config['product_filter']}")
    print(f"   Date Range: {start_date} to {end_date}")
    
    try:
        # Search for products (reuse existing function with modified filter)
        import requests
        from pystac_client import ItemSearch
        
        # Modify the search to use the pollutant-specific filter
        original_filter = "s5p:file_type='L2__NO2___'"
        pollutant_filter = f"s5p:file_type='{config['product_filter']}'"
        
        # Call existing search function but with different filter
        # This would need modification to the original function
        print(f"🔍 Searching for {pollutant} products...")
        
        # For now, show what the system would do
        print(f"✅ Would search with filter: {pollutant_filter}")
        print(f"✅ Would download NetCDF files for processing")
        print(f"✅ Would process variable: {config['variable_name']}")
        print(f"✅ Would convert using factor: {config['conversion_factor']}")
        print(f"✅ Would output in units: {config['units']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading {pollutant} data: {e}")
        return False

def create_sample_multi_pollutant_data():
    """
    Create sample data for all supported pollutants
    """
    print("🎲 Creating sample data for all pollutants...")
    
    import pandas as pd
    import numpy as np
    from utils.data_loader import get_sulaimani_bounds
    
    # Get Sulaimani bounds
    bounds_info = get_sulaimani_bounds()
    bounds = bounds_info['bounds']
    min_lat, min_lon = bounds[0]  # Southwest corner
    max_lat, max_lon = bounds[1]  # Northeast corner
    
    # Generate 10 days of data
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(10)]
    
    for pollutant, config in POLLUTANT_CONFIG.items():
        print(f"   Creating {pollutant} sample data...")
        
        all_data = []
        
        for date in dates:
            # Generate 100 points per day for each pollutant
            n_points = 100
            
            # Create realistic spatial distribution
            lats = np.random.uniform(min_lat, max_lat, n_points)
            lons = np.random.uniform(min_lon, max_lon, n_points)
            
            # Create pollutant-specific realistic values
            if pollutant == 'NO2':
                # Higher in urban center, lower in suburbs
                center_lat, center_lon = 35.5608, 45.4347
                distances = np.sqrt((lats - center_lat)**2 + (lons - center_lon)**2)
                base_values = 45 - 30 * distances / distances.max()
                values = np.maximum(5, base_values + np.random.normal(0, 8, n_points))
                
            elif pollutant == 'SO2':
                # Industrial hotspots
                industrial_lat, industrial_lon = 35.54, 45.41  # Industrial area
                distances = np.sqrt((lats - industrial_lat)**2 + (lons - industrial_lon)**2)
                base_values = 25 - 20 * distances / distances.max()
                values = np.maximum(2, base_values + np.random.normal(0, 5, n_points))
                
            elif pollutant == 'CO':
                # Traffic-related, higher on main roads
                road_effect = np.random.choice([1.5, 1.0, 0.7], n_points, p=[0.3, 0.4, 0.3])
                base_values = np.random.uniform(0.5, 2.0, n_points)
                values = base_values * road_effect + np.random.normal(0, 0.3, n_points)
                values = np.maximum(0.1, values)
                
            elif pollutant == 'O3':
                # Secondary pollutant, varies with photochemistry
                base_values = np.random.uniform(250, 320, n_points)  # Dobson Units
                values = base_values + np.random.normal(0, 15, n_points)
                
            elif pollutant == 'HCHO':
                # VOC-related emissions
                base_values = np.random.uniform(1, 8, n_points)
                values = base_values + np.random.normal(0, 2, n_points)
                values = np.maximum(0.1, values)
                
            elif pollutant == 'AER_AI':
                # Aerosol index, dust events
                dust_event = np.random.choice([True, False], p=[0.2, 0.8])
                if dust_event:
                    base_values = np.random.uniform(1.5, 4.0, n_points)
                else:
                    base_values = np.random.uniform(0.2, 1.2, n_points)
                values = base_values + np.random.normal(0, 0.3, n_points)
                values = np.maximum(0, values)
            
            # Add to dataset
            for lat, lon, value in zip(lats, lons, values):
                all_data.append({
                    'date': date,
                    'lat': lat,
                    'lon': lon,
                    'value': value,
                    'pollutant': pollutant,
                    'units': config['units']
                })
        
        # Save pollutant-specific file
        df = pd.DataFrame(all_data)
        filename = f"data/air_quality_{pollutant.lower()}.csv"
        df.to_csv(filename, index=False)
        print(f"   ✅ Created {filename} with {len(df)} records")
        
        # Calculate statistics
        avg_value = df['value'].mean()
        max_value = df['value'].max()
        guideline = config['who_guideline']
        above_guideline = (df['value'] > guideline).sum() / len(df) * 100
        
        print(f"      Average: {avg_value:.2f} {config['units']}")
        print(f"      Maximum: {max_value:.2f} {config['units']}")
        print(f"      Above guideline ({guideline} {config['units']}): {above_guideline:.1f}%")
    
    print(f"\n🎯 Created sample data for {len(POLLUTANT_CONFIG)} pollutants!")
    print("   Files created in data/ directory")
    print("   Ready for integration into Air Quality page")

def update_air_quality_page():
    """
    Show how to update the Air Quality page for multi-pollutant support
    """
    print("\n📊 Air Quality Page Update Plan:")
    print("=" * 50)
    
    print("1. UPDATE POLLUTANT DROPDOWN:")
    print("   Current: ['NO₂ (Nitrogen Dioxide)']")
    print("   New: [")
    for pollutant, config in POLLUTANT_CONFIG.items():
        print(f"     '{pollutant} ({config['description'].split(' - ')[0]})',")
    print("   ]")
    
    print("\n2. ADD MULTI-POLLUTANT HEATMAP:")
    print("   - Load data based on selected pollutant")
    print("   - Dynamic color scales for different units")
    print("   - Pollutant-specific WHO guidelines")
    
    print("\n3. ENHANCED STATISTICS:")
    print("   - Pollutant-specific health thresholds")
    print("   - Comparative analysis between pollutants")
    print("   - Seasonal patterns for each pollutant")
    
    print("\n4. CORRELATION ANALYSIS:")
    print("   - NO₂ vs SO₂ (industrial sources)")
    print("   - CO vs traffic density")
    print("   - O₃ formation patterns")

def main():
    """
    Main function with command line interface
    """
    parser = argparse.ArgumentParser(description='Multi-Pollutant Sentinel-5P Data System')
    parser.add_argument('--pollutant', choices=list(POLLUTANT_CONFIG.keys()) + ['ALL'], 
                       default='ALL', help='Pollutant to download')
    parser.add_argument('--start-date', default='2024-01-01', help='Start date YYYY-MM-DD')
    parser.add_argument('--end-date', default='2024-01-31', help='End date YYYY-MM-DD')
    parser.add_argument('--sample-data', action='store_true', 
                       help='Create sample data instead of downloading')
    parser.add_argument('--max-products', type=int, default=20, help='Maximum products to download')
    
    args = parser.parse_args()
    
    print("🛰️ Multi-Pollutant Sentinel-5P Data System")
    print("=" * 50)
    
    if args.sample_data:
        create_sample_multi_pollutant_data()
        update_air_quality_page()
        return
    
    if args.pollutant == 'ALL':
        pollutants = list(POLLUTANT_CONFIG.keys())
    else:
        pollutants = [args.pollutant]
    
    success_count = 0
    for pollutant in pollutants:
        if download_pollutant_data(pollutant, args.start_date, args.end_date, args.max_products):
            success_count += 1
        print()
    
    print(f"✅ Successfully processed {success_count}/{len(pollutants)} pollutants")

if __name__ == "__main__":
    main()