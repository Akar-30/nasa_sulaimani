"""
Create sample NO₂ air quality data for Sulaimani demonstration
This simulates what the real Sentinel-5P data would look like
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Sulaimani bounding box (expanded coverage)
SULAIMANI_BOUNDS = {
    'min_lon': 45.25,
    'max_lon': 45.62,
    'min_lat': 35.40,
    'max_lat': 35.72
}

def generate_sample_no2_data(num_days=10, points_per_day=150):
    """
    Generate realistic sample NO₂ data for Sulaimani
    
    Args:
        num_days (int): Number of days to simulate
        points_per_day (int): Number of measurement points per day
    
    Returns:
        pandas.DataFrame: Sample NO₂ data
    """
    print("🛰️ Generating Sample NO₂ Data for Sulaimani...")
    print(f"Simulating {num_days} days with {points_per_day} measurements per day")
    
    data = []
    
    # Create date range (last 10 days)
    end_date = datetime.now()
    dates = [end_date - timedelta(days=i) for i in range(num_days-1, -1, -1)]
    
    for date in dates:
        date_str = date.strftime('%Y-%m-%d')
        
        # Generate random points within Sulaimani bounds
        lats = np.random.uniform(
            SULAIMANI_BOUNDS['min_lat'], 
            SULAIMANI_BOUNDS['max_lat'], 
            points_per_day
        )
        lons = np.random.uniform(
            SULAIMANI_BOUNDS['min_lon'], 
            SULAIMANI_BOUNDS['max_lon'], 
            points_per_day
        )
        
        # Generate realistic NO₂ concentrations
        # Urban areas typically have higher NO₂ (40-80 µg/m³)
        # Rural areas have lower NO₂ (10-40 µg/m³)
        
        base_values = []
        for lat, lon in zip(lats, lons):
            # Distance from city center (35.5608, 45.4347)
            center_lat, center_lon = 35.5608, 45.4347
            distance = np.sqrt((lat - center_lat)**2 + (lon - center_lon)**2)
            
            # Higher pollution near city center
            if distance < 0.05:  # City center
                base_no2 = np.random.normal(65, 15)  # High NO₂
            elif distance < 0.10:  # Urban areas
                base_no2 = np.random.normal(45, 12)  # Moderate NO₂
            else:  # Suburban/rural
                base_no2 = np.random.normal(25, 8)   # Lower NO₂
            
            # Add some seasonal variation (higher in winter)
            seasonal_factor = 1.0 + 0.2 * np.sin(2 * np.pi * date.timetuple().tm_yday / 365)
            
            # Add daily variation (higher during rush hours - simulated)
            daily_factor = np.random.uniform(0.8, 1.3)
            
            # Add some industrial hotspots
            # Industrial area around (35.54, 45.41)
            if abs(lat - 35.54) < 0.02 and abs(lon - 45.41) < 0.02:
                base_no2 += np.random.uniform(20, 40)  # Industrial boost
            
            final_no2 = base_no2 * seasonal_factor * daily_factor
            
            # Ensure values are realistic (0-150 µg/m³)
            final_no2 = max(5, min(150, final_no2))
            
            base_values.append(final_no2)
        
        # Create records for this date
        for lat, lon, no2_value in zip(lats, lons, base_values):
            data.append({
                'date': date_str,
                'lat': round(lat, 4),
                'lon': round(lon, 4),
                'value': round(no2_value, 2)
            })
    
    df = pd.DataFrame(data)
    
    # Sort by date and location
    df = df.sort_values(['date', 'lat', 'lon']).reset_index(drop=True)
    
    return df


def create_sample_no2_files():
    """Create sample NO₂ data files for demonstration"""
    
    print("="*80)
    print("CREATING SAMPLE NO₂ DATA FOR SULAIMANI")
    print("="*80)
    print("(This simulates what real Sentinel-5P data would look like)")
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Generate sample data
    df = generate_sample_no2_data(num_days=10, points_per_day=150)
    
    # Save main data file
    output_file = 'data/air_quality_no2.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Saved {len(df)} NO₂ records to: {output_file}")
    
    # Display statistics
    print("\n" + "="*80)
    print("SAMPLE NO₂ DATA STATISTICS")
    print("="*80)
    
    print(f"\nTotal records: {len(df):,}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Unique dates: {df['date'].nunique()}")
    
    print(f"\nNO₂ Concentration (µg/m³):")
    print(f"  Min:    {df['value'].min():.2f}")
    print(f"  Max:    {df['value'].max():.2f}")
    print(f"  Mean:   {df['value'].mean():.2f}")
    print(f"  Median: {df['value'].median():.2f}")
    
    # WHO guideline comparison
    who_guideline = 40  # µg/m³ annual average
    above_who = (df['value'] > who_guideline).sum()
    percent_above = (above_who / len(df)) * 100
    
    print(f"\nWHO Guideline Analysis (40 µg/m³):")
    print(f"  Records above guideline: {above_who:,} ({percent_above:.1f}%)")
    
    # Create pollution categories
    df['category'] = pd.cut(
        df['value'],
        bins=[0, 40, 80, 120, float('inf')],
        labels=['Good', 'Moderate', 'Unhealthy', 'Very Unhealthy']
    )
    
    category_counts = df['category'].value_counts()
    print(f"\nPollution Categories:")
    for category, count in category_counts.items():
        percent = (count / len(df)) * 100
        print(f"  {category}: {count:,} ({percent:.1f}%)")
    
    # Save hotspots file (high pollution areas)
    hotspots = df[df['value'] > 80].copy()
    if not hotspots.empty:
        hotspots_file = 'data/pollution_hotspots.csv'
        hotspots.to_csv(hotspots_file, index=False)
        print(f"\n✅ Saved {len(hotspots)} pollution hotspots to: {hotspots_file}")
    
    # Preview data
    print("\n" + "="*80)
    print("DATA PREVIEW")
    print("="*80)
    print(df.head(10))
    
    print(f"\n✅ Sample NO₂ data created successfully!")
    print("\n📝 Next steps:")
    print("1. Run: streamlit run Home.py")
    print("2. Navigate to '💨 Air Quality' page")
    print("3. You'll see NO₂ heatmap overlay on the map")
    print("4. Toggle 'Show Population Density' to see exposure analysis")
    
    print(f"\n💡 This sample data shows:")
    print(f"  - Higher pollution in city center ({df[df['value'] > 60]['value'].mean():.1f} µg/m³)")
    print(f"  - Lower pollution in suburbs ({df[df['value'] < 30]['value'].mean():.1f} µg/m³)")
    print(f"  - Industrial hotspots with elevated NO₂")
    print(f"  - Temporal variation over {df['date'].nunique()} days")
    
    print(f"\n🔄 To get real Sentinel-5P data later:")
    print(f"  1. Wait for S5P-PAL API to be available")
    print(f"  2. Run: python download_no2_data.py")
    print(f"  3. Run: python process_no2_netcdf.py")
    
    return df


if __name__ == "__main__":
    create_sample_no2_files()