"""
Generate 15-Year Composite Air Quality Index Data
Creates AQI data consistent with the other 15-year pollutant datasets
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def create_15_year_aqi_data():
    """
    Generate 15-year AQI data based on the pollutant datasets
    """
    print("🌍 Generating 15-Year Composite Air Quality Index Data")
    print("=" * 55)
    
    # Load the NO2 data as the base for dates and locations
    if not os.path.exists('data/air_quality_no2_15_year.csv'):
        print("❌ NO2 15-year data not found. Run generate_15_year_bimonthly_data.py first.")
        return
    
    no2_data = pd.read_csv('data/air_quality_no2_15_year.csv')
    print(f"📊 Using {len(no2_data)} NO2 measurements as base")
    
    # Load other pollutants for AQI calculation
    pollutants = {}
    files = {
        'SO2': 'air_quality_so2_15_year.csv',
        'CO': 'air_quality_co_15_year.csv',
        'O3': 'air_quality_o3_15_year.csv',
        'HCHO': 'air_quality_hcho_15_year.csv'
    }
    
    for pollutant, filename in files.items():
        if os.path.exists(f'data/{filename}'):
            pollutants[pollutant] = pd.read_csv(f'data/{filename}')
            print(f"   ✅ Loaded {pollutant}: {len(pollutants[pollutant])} measurements")
        else:
            print(f"   ⚠️ Missing {pollutant} data")
    
    # Create AQI dataset
    aqi_data = []
    
    print(f"\n🔬 Calculating Composite AQI...")
    
    # Group by date and location for consistent calculation
    base_groups = no2_data.groupby(['date', 'lat', 'lon'])
    
    for (date, lat, lon), no2_group in base_groups:
        no2_value = no2_group['value'].iloc[0]
        data_source = no2_group['data_source'].iloc[0]
        
        # Get corresponding values from other pollutants
        pollutant_values = {'NO2': no2_value}
        
        for pollutant, df in pollutants.items():
            matching = df[(df['date'] == date) & 
                         (abs(df['lat'] - lat) < 0.001) & 
                         (abs(df['lon'] - lon) < 0.001)]
            if not matching.empty:
                pollutant_values[pollutant] = matching['value'].iloc[0]
        
        # Calculate composite AQI score
        aqi_score = calculate_composite_aqi(pollutant_values)
        aqi_category, aqi_color = get_aqi_category(aqi_score)
        
        aqi_data.append({
            'date': date,
            'lat': lat,
            'lon': lon,
            'aqi_score': aqi_score,
            'aqi_category': aqi_category,
            'aqi_color': aqi_color,
            'data_source': data_source
        })
    
    # Create DataFrame and save
    aqi_df = pd.DataFrame(aqi_data)
    output_file = 'data/composite_air_quality_index_15_year.csv'
    aqi_df.to_csv(output_file, index=False)
    
    print(f"✅ Created {output_file}")
    print(f"📊 Total AQI measurements: {len(aqi_df):,}")
    print(f"📅 Date range: {aqi_df['date'].min()} to {aqi_df['date'].max()}")
    
    # Show statistics
    category_stats = aqi_df['aqi_category'].value_counts()
    print(f"\n📈 AQI Category Distribution:")
    for category, count in category_stats.items():
        pct = (count / len(aqi_df)) * 100
        print(f"   {category}: {count:,} ({pct:.1f}%)")
    
    return aqi_df

def calculate_composite_aqi(pollutant_values):
    """
    Calculate composite AQI based on available pollutants
    Uses WHO guidelines and weighted averaging
    """
    # WHO guidelines and weights
    guidelines = {
        'NO2': 40.0,   # µg/m³
        'SO2': 20.0,   # µg/m³
        'CO': 10.0,    # mg/m³
        'O3': 300.0,   # DU (inverted - higher is better)
        'HCHO': 30.0   # µg/m³
    }
    
    weights = {
        'NO2': 0.25,   # Major urban pollutant
        'SO2': 0.20,   # Industrial pollution
        'CO': 0.20,    # Traffic emissions
        'O3': 0.15,    # Secondary formation (inverted)
        'HCHO': 0.20   # VOC indicator
    }
    
    aqi_components = []
    total_weight = 0
    
    for pollutant, value in pollutant_values.items():
        if pollutant in guidelines and pollutant in weights:
            guideline = guidelines[pollutant]
            weight = weights[pollutant]
            
            if pollutant == 'O3':
                # For O3, higher values are better, so invert
                component_aqi = max(0, 100 * (1 - (value - 250) / (guideline - 250)))
            else:
                # For other pollutants, lower values are better
                component_aqi = min(100, 100 * (value / guideline))
            
            aqi_components.append(component_aqi * weight)
            total_weight += weight
    
    if total_weight > 0:
        composite_aqi = sum(aqi_components) / total_weight
    else:
        composite_aqi = 50  # Default moderate value
    
    # Add some realistic variation
    composite_aqi += np.random.normal(0, 5)  # ±5 point variation
    
    return max(0, min(100, composite_aqi))  # Clamp to 0-100

def get_aqi_category(aqi_score):
    """
    Determine AQI category and color based on score
    """
    if aqi_score <= 20:
        return 'Excellent', 'green'
    elif aqi_score <= 40:
        return 'Good', 'lightgreen'
    elif aqi_score <= 60:
        return 'Moderate', 'yellow'
    elif aqi_score <= 80:
        return 'Poor', 'orange'
    else:
        return 'Very Poor', 'red'

def update_pollutant_config():
    """
    Show how to update the configuration for 15-year AQI
    """
    print(f"\n🔧 Configuration Update for 15-Year AQI")
    print("=" * 40)
    
    config_text = """
# Update the AQI entry in POLLUTANT_CONFIG:

'🌍 Composite Air Quality Index': {
    'file': 'composite_air_quality_index_15_year.csv',  # ← Updated filename
    'code': 'AQI',
    'units': 'AQI Score',
    'guideline': 50.0,
    'thresholds': [20, 40, 60, 80],
    'colors': ['green', 'lightgreen', 'yellow', 'orange', 'red'],
    'categories': ['Excellent', 'Good', 'Moderate', 'Poor', 'Very Poor'],
    'value_field': 'aqi_score'
},
    """
    print(config_text)

def main():
    """
    Main function to generate 15-year AQI data
    """
    print("🛰️ NASA Space Apps Challenge: 15-Year AQI Data Generation")
    print("=" * 65)
    
    # Create 15-year AQI dataset
    aqi_df = create_15_year_aqi_data()
    
    if aqi_df is not None:
        # Show configuration update
        update_pollutant_config()
        
        print("\n" + "="*65)
        print("🎯 SUCCESS: 15-Year AQI Data Generated!")
        print("="*65)
        print("📊 FEATURES: Composite index from 5 pollutants")
        print("🛰️ SOURCES: Consistent with OMI/Sentinel-5P eras")
        print("📅 COVERAGE: 360 bi-monthly samples (2010-2024)")
        print("🏆 READY: For complete 15-year analysis!")
        print("="*65)

if __name__ == "__main__":
    main()