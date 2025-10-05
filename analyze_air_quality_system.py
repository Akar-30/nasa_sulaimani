"""
Demonstration script showing the enhanced air quality analysis system
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def analyze_air_quality_system():
    """
    Analyze and display the comprehensive air quality system we've built
    """
    print("🌍 SULAIMANI AIR QUALITY ANALYSIS SYSTEM")
    print("=" * 55)
    
    # Check data availability
    data_files = {
        'Combined Grid Data': 'air_quality_combined_grid.csv',
        'Composite AQI': 'composite_air_quality_index.csv',
        'NO₂ Interpolated': 'air_quality_no2_interpolated.csv',
        'SO₂ Interpolated': 'air_quality_so2_interpolated.csv',
        'CO Interpolated': 'air_quality_co_interpolated.csv',
        'O₃ Interpolated': 'air_quality_o3_interpolated.csv',
        'HCHO Interpolated': 'air_quality_hcho_interpolated.csv',
        'Aerosol Index Interpolated': 'air_quality_aer_ai_interpolated.csv',
        'Population Data': 'population_density.csv'
    }
    
    print("📊 DATA AVAILABILITY CHECK:")
    available_datasets = {}
    for name, filename in data_files.items():
        filepath = Path(f'data/{filename}')
        if filepath.exists():
            df = pd.read_csv(filepath)
            available_datasets[name] = df
            print(f"   ✅ {name}: {len(df):,} records")
        else:
            print(f"   ❌ {name}: Not found")
    
    if 'Combined Grid Data' in available_datasets:
        combined_df = available_datasets['Combined Grid Data']
        
        print(f"\n🗺️ SPATIAL GRID ANALYSIS:")
        unique_points = combined_df[['lat', 'lon']].drop_duplicates()
        unique_dates = combined_df['date'].nunique()
        
        print(f"   📐 Grid Points: {len(unique_points)} locations")
        print(f"   📅 Time Period: {unique_dates} days")
        print(f"   🌍 Coverage Area:")
        print(f"      Latitude: {combined_df['lat'].min():.3f}°N to {combined_df['lat'].max():.3f}°N")
        print(f"      Longitude: {combined_df['lon'].min():.3f}°E to {combined_df['lon'].max():.3f}°E")
        
        # Analyze pollutant correlations
        pollutant_cols = [col for col in combined_df.columns if '_value' in col]
        if len(pollutant_cols) >= 2:
            print(f"\n🔬 POLLUTANT CORRELATION ANALYSIS:")
            latest_data = combined_df[combined_df['date'] == combined_df['date'].max()]
            corr_matrix = latest_data[pollutant_cols].corr()
            
            print("   Strong Correlations (|r| > 0.5):")
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.5:
                        pol1 = corr_matrix.columns[i].replace('_value', '')
                        pol2 = corr_matrix.columns[j].replace('_value', '')
                        relation = "positive" if corr_val > 0 else "negative"
                        print(f"      {pol1} ↔ {pol2}: {corr_val:.2f} ({relation})")
    
    if 'Composite AQI' in available_datasets:
        aqi_df = available_datasets['Composite AQI']
        
        print(f"\n🏭 COMPOSITE AIR QUALITY INDEX:")
        latest_aqi = aqi_df[aqi_df['date'] == aqi_df['date'].max()]
        
        print(f"   📊 Average AQI Score: {latest_aqi['aqi_score'].mean():.1f}")
        print(f"   📈 AQI Range: {latest_aqi['aqi_score'].min():.1f} - {latest_aqi['aqi_score'].max():.1f}")
        
        # AQI category distribution
        aqi_dist = latest_aqi['aqi_category'].value_counts()
        print(f"   🎯 Air Quality Distribution:")
        for category, count in aqi_dist.items():
            percentage = (count / len(latest_aqi)) * 100
            print(f"      {category}: {count} points ({percentage:.1f}%)")
        
        # Identify pollution hotspots
        worst_areas = latest_aqi.nlargest(5, 'aqi_score')
        print(f"   🚨 Top 5 Pollution Hotspots:")
        for i, (_, area) in enumerate(worst_areas.iterrows(), 1):
            print(f"      {i}. AQI {area['aqi_score']:.1f} at {area['lat']:.3f}°N, {area['lon']:.3f}°E ({area['aqi_category']})")
    
    # Population exposure analysis
    if 'Population Data' in available_datasets:
        pop_df = available_datasets['Population Data']
        
        print(f"\n👥 POPULATION EXPOSURE ANALYSIS:")
        print(f"   📊 Population Points: {len(pop_df):,}")
        print(f"   🏘️ Total Population: ~{pop_df['population_density'].sum()/1000:.0f}K people")
        
        high_density_areas = pop_df[pop_df['population_density'] > 1000]
        print(f"   🏙️ High Density Areas: {len(high_density_areas)} locations (>1000 people/km²)")
    
    print(f"\n🎯 SYSTEM CAPABILITIES:")
    capabilities = [
        "✅ 6 different air pollutants (NO₂, SO₂, CO, O₃, HCHO, Aerosols)",
        "✅ Consistent 40×40 spatial grid (1600 measurement points)",
        "✅ Smooth spatial interpolation for realistic pollution surfaces", 
        "✅ Composite Air Quality Index combining all pollutants",
        "✅ WHO health guideline comparisons",
        "✅ Pollution source correlation analysis",
        "✅ Population exposure risk assessment",
        "✅ Interactive heatmap visualization", 
        "✅ Hotspot identification and ranking",
        "✅ Ready for real Sentinel-5P satellite integration"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")
    
    print(f"\n📱 WEB INTERFACE:")
    print(f"   🌐 Streamlit App: http://localhost:8501")
    print(f"   📊 Navigate to: '💨 Air Quality' page")
    print(f"   🔄 Try dropdown: '🌍 Composite Air Quality Index'")
    print(f"   🗺️ Toggle population overlay to see exposure analysis")
    
    print(f"\n" + "=" * 55)
    print("🏆 READY FOR NASA SPACE APPS CHALLENGE JUDGES!")
    print("=" * 55)

if __name__ == "__main__":
    analyze_air_quality_system()