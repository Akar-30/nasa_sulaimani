"""
Extract Sulaimani population density data from Iraq dataset
"""

import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon
import json

# Sulaimani expanded bounding box (3x larger coverage area)
# This captures the city center plus surrounding suburbs and rural areas
SULAIMANI_BOUNDS = {
    'min_lon': 45.25,  # Extended west by ~0.10 degrees (~11 km)
    'max_lon': 45.62,  # Extended east by ~0.10 degrees (~11 km)
    'min_lat': 35.40,  # Extended south by ~0.08 degrees (~9 km)
    'max_lat': 35.72   # Extended north by ~0.08 degrees (~9 km)
}

def load_iraq_population_data(filepath='data/irq_pd_2020_1km_ASCII_XYZ.csv'):
    """
    Load Iraq population density data
    """
    print("Loading Iraq population data...")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df):,} data points for Iraq")
    return df


def extract_sulaimani_data(df):
    """
    Extract only Sulaimani area data
    """
    print("\nExtracting Sulaimani area...")
    
    # Filter by bounding box
    sulaimani_df = df[
        (df['X'] >= SULAIMANI_BOUNDS['min_lon']) &
        (df['X'] <= SULAIMANI_BOUNDS['max_lon']) &
        (df['Y'] >= SULAIMANI_BOUNDS['min_lat']) &
        (df['Y'] <= SULAIMANI_BOUNDS['max_lat'])
    ].copy()
    
    print(f"Found {len(sulaimani_df):,} data points in Sulaimani area")
    
    # Rename columns to standard format
    sulaimani_df.rename(columns={
        'X': 'lon',
        'Y': 'lat',
        'Z': 'population_density'
    }, inplace=True)
    
    return sulaimani_df


def create_population_density_csv(sulaimani_df, output_path='data/population_density.csv'):
    """
    Create CSV file for population density
    """
    print(f"\nCreating {output_path}...")
    
    # Add date column (2020 data)
    sulaimani_df['date'] = '2020-01-01'
    
    # Select and reorder columns
    output_df = sulaimani_df[['date', 'lat', 'lon', 'population_density']].copy()
    
    # Save to CSV
    output_df.to_csv(output_path, index=False)
    print(f"✅ Saved {len(output_df):,} records to {output_path}")
    
    return output_df


def create_population_density_geojson(sulaimani_df, output_path='data/population_density.geojson'):
    """
    Create GeoJSON with population density zones
    """
    print(f"\nCreating {output_path}...")
    
    # Create categories based on population density
    def categorize_density(density):
        if density < 500:
            return 'Low'
        elif density < 2000:
            return 'Medium'
        elif density < 5000:
            return 'High'
        else:
            return 'Very High'
    
    sulaimani_df['density_category'] = sulaimani_df['population_density'].apply(categorize_density)
    
    # Create points
    geometry = [Point(xy) for xy in zip(sulaimani_df['lon'], sulaimani_df['lat'])]
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        sulaimani_df[['population_density', 'density_category']], 
        geometry=geometry,
        crs='EPSG:4326'
    )
    
    # Save as GeoJSON
    gdf.to_file(output_path, driver='GeoJSON')
    print(f"✅ Saved GeoJSON with {len(gdf):,} features")
    
    return gdf


def create_neighborhood_stats(sulaimani_df, output_path='data/neighborhood_population.csv'):
    """
    Create neighborhood-level statistics
    """
    print(f"\nCreating neighborhood statistics...")
    
    # Create a simple grid-based neighborhood division
    # Divide Sulaimani into ~9 zones (3x3 grid)
    lat_bins = np.linspace(SULAIMANI_BOUNDS['min_lat'], SULAIMANI_BOUNDS['max_lat'], 4)
    lon_bins = np.linspace(SULAIMANI_BOUNDS['min_lon'], SULAIMANI_BOUNDS['max_lon'], 4)
    
    neighborhoods = []
    
    for i in range(len(lat_bins) - 1):
        for j in range(len(lon_bins) - 1):
            # Define zone
            zone_data = sulaimani_df[
                (sulaimani_df['lat'] >= lat_bins[i]) &
                (sulaimani_df['lat'] < lat_bins[i + 1]) &
                (sulaimani_df['lon'] >= lon_bins[j]) &
                (sulaimani_df['lon'] < lon_bins[j + 1])
            ]
            
            if len(zone_data) > 0:
                # Name zones based on position
                lat_name = ['South', 'Central', 'North'][i] if i < 3 else 'North'
                lon_name = ['West', 'Central', 'East'][j] if j < 3 else 'East'
                zone_name = f"{lat_name} {lon_name}"
                
                # Calculate statistics
                avg_density = zone_data['population_density'].mean()
                total_population = zone_data['population_density'].sum()  # Sum of all grid cells
                
                neighborhoods.append({
                    'neighborhood': zone_name,
                    'avg_density': round(avg_density, 2),
                    'total_population': round(total_population, 0),
                    'num_cells': len(zone_data),
                    'min_density': round(zone_data['population_density'].min(), 2),
                    'max_density': round(zone_data['population_density'].max(), 2)
                })
    
    # Create DataFrame
    neighborhood_df = pd.DataFrame(neighborhoods)
    neighborhood_df = neighborhood_df.sort_values('avg_density', ascending=False)
    
    # Save to CSV
    neighborhood_df.to_csv(output_path, index=False)
    print(f"✅ Saved neighborhood statistics to {output_path}")
    print("\nNeighborhood Summary:")
    print(neighborhood_df[['neighborhood', 'avg_density', 'total_population']])
    
    return neighborhood_df


def print_statistics(sulaimani_df):
    """
    Print summary statistics
    """
    print("\n" + "="*60)
    print("SULAIMANI POPULATION DENSITY STATISTICS (2020)")
    print("="*60)
    
    print(f"\nData Points: {len(sulaimani_df):,}")
    print(f"Area Covered: {SULAIMANI_BOUNDS['min_lat']:.2f}°N to {SULAIMANI_BOUNDS['max_lat']:.2f}°N")
    print(f"              {SULAIMANI_BOUNDS['min_lon']:.2f}°E to {SULAIMANI_BOUNDS['max_lon']:.2f}°E")
    
    print(f"\nPopulation Density Statistics:")
    print(f"  Average: {sulaimani_df['population_density'].mean():.2f} people/km²")
    print(f"  Median:  {sulaimani_df['population_density'].median():.2f} people/km²")
    print(f"  Min:     {sulaimani_df['population_density'].min():.2f} people/km²")
    print(f"  Max:     {sulaimani_df['population_density'].max():.2f} people/km²")
    print(f"  Std Dev: {sulaimani_df['population_density'].std():.2f} people/km²")
    
    # Estimated total population (rough estimate)
    # Each cell is ~1km² so sum gives approximate population
    est_total = sulaimani_df['population_density'].sum()
    print(f"\nEstimated Total Population: ~{est_total:,.0f}")
    
    # Density categories
    print("\nPopulation Density Distribution:")
    low = len(sulaimani_df[sulaimani_df['population_density'] < 500])
    medium = len(sulaimani_df[(sulaimani_df['population_density'] >= 500) & 
                               (sulaimani_df['population_density'] < 2000)])
    high = len(sulaimani_df[(sulaimani_df['population_density'] >= 2000) & 
                             (sulaimani_df['population_density'] < 5000)])
    very_high = len(sulaimani_df[sulaimani_df['population_density'] >= 5000])
    
    total = len(sulaimani_df)
    print(f"  Low (<500):           {low:,} cells ({low/total*100:.1f}%)")
    print(f"  Medium (500-2000):    {medium:,} cells ({medium/total*100:.1f}%)")
    print(f"  High (2000-5000):     {high:,} cells ({high/total*100:.1f}%)")
    print(f"  Very High (>5000):    {very_high:,} cells ({very_high/total*100:.1f}%)")
    
    print("\n" + "="*60)


def main():
    """
    Main processing function
    """
    print("🌍 Sulaimani Population Density Data Processor")
    print("=" * 60)
    
    # Load data
    iraq_df = load_iraq_population_data()
    
    # Extract Sulaimani area
    sulaimani_df = extract_sulaimani_data(iraq_df)
    
    if len(sulaimani_df) == 0:
        print("❌ No data found for Sulaimani area!")
        print("Check the bounding box coordinates.")
        return
    
    # Print statistics
    print_statistics(sulaimani_df)
    
    # Create output files
    print("\n" + "="*60)
    print("CREATING OUTPUT FILES")
    print("="*60)
    
    # 1. CSV for point data
    create_population_density_csv(sulaimani_df)
    
    # 2. GeoJSON for map visualization
    create_population_density_geojson(sulaimani_df)
    
    # 3. Neighborhood-level statistics
    create_neighborhood_stats(sulaimani_df)
    
    print("\n" + "="*60)
    print("✅ PROCESSING COMPLETE!")
    print("="*60)
    print("\nFiles created in /data folder:")
    print("  ✅ population_density.csv")
    print("  ✅ population_density.geojson")
    print("  ✅ neighborhood_population.csv")
    print("\nYou can now use these files in your Streamlit app!")
    print("\nNext steps:")
    print("  1. Run: streamlit run Home.py")
    print("  2. Navigate to Air Quality or other pages")
    print("  3. The population overlay will appear on maps")


if __name__ == "__main__":
    main()
