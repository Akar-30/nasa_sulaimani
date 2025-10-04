"""
Process Sentinel-5P NO₂ NetCDF files and extract data for Sulaimani
Converts raw satellite data to CSV format for Streamlit visualization
"""

import netCDF4 as nc
import numpy as np
import pandas as pd
import os
from datetime import datetime
import glob

# Sulaimani bounding box (expanded coverage)
SULAIMANI_BOUNDS = {
    'min_lon': 45.25,
    'max_lon': 45.62,
    'min_lat': 35.40,
    'max_lat': 35.72
}

def extract_no2_from_netcdf(netcdf_file):
    """
    Extract NO₂ data from a Sentinel-5P NetCDF file for Sulaimani area
    
    Args:
        netcdf_file (str): Path to NetCDF file
    
    Returns:
        pandas.DataFrame: Extracted NO₂ data with columns: date, lat, lon, value
    """
    print(f"\nProcessing: {os.path.basename(netcdf_file)}")
    
    try:
        # Open NetCDF file
        dataset = nc.Dataset(netcdf_file, 'r')
        
        # Extract metadata
        print("Reading metadata...")
        
        # Get time information (from filename or metadata)
        filename = os.path.basename(netcdf_file)
        # Typical S5P filename: S5P_PAL__L2__NO2____20241006T223202_...
        try:
            date_str = filename.split('_')[5][:8]  # Extract YYYYMMDD
            date = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
        except:
            date = datetime.now().strftime('%Y-%m-%d')
        
        print(f"Date: {date}")
        
        # Navigate to the PRODUCT group where data is stored
        product_group = dataset.groups['PRODUCT']
        
        # Extract NO₂ column data
        # Variable name might be 'nitrogendioxide_tropospheric_column' or similar
        no2_var_names = [
            'nitrogendioxide_tropospheric_column',
            'nitrogen_dioxide_tropospheric_column',
            'NO2_column_number_density',
            'nitrogendioxide_total_column'
        ]
        
        no2_data = None
        no2_var_name = None
        
        for var_name in no2_var_names:
            if var_name in product_group.variables:
                no2_var_name = var_name
                no2_data = product_group.variables[var_name][:]
                break
        
        if no2_data is None:
            print(f"Available variables: {list(product_group.variables.keys())}")
            raise ValueError("Could not find NO₂ data variable in NetCDF file")
        
        print(f"Found NO₂ data: {no2_var_name}")
        
        # Extract coordinates
        latitude = product_group.variables['latitude'][:]
        longitude = product_group.variables['longitude'][:]
        
        # Extract quality assurance value (if available)
        qa_value = None
        if 'qa_value' in product_group.variables:
            qa_value = product_group.variables['qa_value'][:]
        
        # Close dataset
        dataset.close()
        
        print(f"Data shape: {no2_data.shape}")
        print(f"Lat range: {latitude.min():.2f} to {latitude.max():.2f}")
        print(f"Lon range: {longitude.min():.2f} to {longitude.max():.2f}")
        
        # Flatten arrays and filter for Sulaimani
        print("Filtering for Sulaimani area...")
        
        # Remove time dimension if present (S5P data is usually [time, scanline, ground_pixel])
        if len(no2_data.shape) == 3:
            no2_data = no2_data[0]
            if qa_value is not None:
                qa_value = qa_value[0]
        
        # Flatten 2D arrays to 1D
        lat_flat = latitude.flatten()
        lon_flat = longitude.flatten()
        no2_flat = no2_data.flatten()
        
        if qa_value is not None:
            qa_flat = qa_value.flatten()
        else:
            qa_flat = np.ones_like(no2_flat)  # Assume good quality if not available
        
        # Create mask for Sulaimani area and valid data
        sulaimani_mask = (
            (lat_flat >= SULAIMANI_BOUNDS['min_lat']) &
            (lat_flat <= SULAIMANI_BOUNDS['max_lat']) &
            (lon_flat >= SULAIMANI_BOUNDS['min_lon']) &
            (lon_flat <= SULAIMANI_BOUNDS['max_lon']) &
            (~np.isnan(no2_flat)) &
            (no2_flat > 0) &
            (qa_flat >= 0.5)  # Quality threshold (0.5 = 50% good quality)
        )
        
        # Apply mask
        lat_sulaimani = lat_flat[sulaimani_mask]
        lon_sulaimani = lon_flat[sulaimani_mask]
        no2_sulaimani = no2_flat[sulaimani_mask]
        
        print(f"Found {len(lat_sulaimani)} valid pixels over Sulaimani")
        
        if len(lat_sulaimani) == 0:
            print("⚠️ No valid data found for Sulaimani area")
            return pd.DataFrame()
        
        # Convert NO₂ units (mol/m² to µg/m³)
        # Conversion factor: multiply by ~1.9e9 to get µg/m³
        # This is approximate and depends on atmospheric conditions
        no2_ugm3 = no2_sulaimani * 1.9e9
        
        # Create DataFrame
        df = pd.DataFrame({
            'date': date,
            'lat': lat_sulaimani,
            'lon': lon_sulaimani,
            'value': no2_ugm3
        })
        
        print(f"NO₂ range: {df['value'].min():.2f} to {df['value'].max():.2f} µg/m³")
        print(f"Mean NO₂: {df['value'].mean():.2f} µg/m³")
        
        return df
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


def process_all_no2_files(input_dir='data/raw_no2', output_file='data/air_quality_no2.csv'):
    """
    Process all NetCDF files in the directory and combine into single CSV
    
    Args:
        input_dir (str): Directory containing NetCDF files
        output_file (str): Output CSV file path
    """
    print("="*80)
    print("SENTINEL-5P NO₂ DATA PROCESSOR FOR SULAIMANI")
    print("="*80)
    
    # Find all NetCDF files
    nc_files = glob.glob(os.path.join(input_dir, '*.nc'))
    
    if not nc_files:
        print(f"\n❌ No NetCDF files found in {input_dir}")
        print("\nPlease run download_no2_data.py first to download satellite data.")
        return
    
    print(f"\nFound {len(nc_files)} NetCDF file(s)")
    
    # Process each file
    all_data = []
    
    for i, nc_file in enumerate(nc_files, 1):
        print(f"\n--- Processing file {i}/{len(nc_files)} ---")
        df = extract_no2_from_netcdf(nc_file)
        
        if not df.empty:
            all_data.append(df)
    
    if not all_data:
        print("\n❌ No valid data extracted from any files")
        return
    
    # Combine all data
    print("\n" + "="*80)
    print("COMBINING DATA")
    print("="*80)
    
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Sort by date and location
    combined_df = combined_df.sort_values(['date', 'lat', 'lon']).reset_index(drop=True)
    
    # Remove duplicates (keep average if multiple measurements for same location)
    print(f"Total records before deduplication: {len(combined_df)}")
    
    # Group by date, lat, lon and take mean
    combined_df = combined_df.groupby(['date', 'lat', 'lon'], as_index=False).agg({
        'value': 'mean'
    })
    
    print(f"Total records after deduplication: {len(combined_df)}")
    
    # Round values for cleaner output
    combined_df['lat'] = combined_df['lat'].round(4)
    combined_df['lon'] = combined_df['lon'].round(4)
    combined_df['value'] = combined_df['value'].round(2)
    
    # Save to CSV
    combined_df.to_csv(output_file, index=False)
    
    print(f"\n✅ Saved to: {output_file}")
    
    # Display statistics
    print("\n" + "="*80)
    print("DATA STATISTICS")
    print("="*80)
    
    print(f"\nTotal records: {len(combined_df)}")
    print(f"Date range: {combined_df['date'].min()} to {combined_df['date'].max()}")
    print(f"Unique dates: {combined_df['date'].nunique()}")
    print(f"\nNO₂ Concentration (µg/m³):")
    print(f"  Min:    {combined_df['value'].min():.2f}")
    print(f"  Max:    {combined_df['value'].max():.2f}")
    print(f"  Mean:   {combined_df['value'].mean():.2f}")
    print(f"  Median: {combined_df['value'].median():.2f}")
    
    # WHO guideline comparison
    who_guideline = 40  # µg/m³ annual average
    above_who = (combined_df['value'] > who_guideline).sum()
    percent_above = (above_who / len(combined_df)) * 100
    
    print(f"\nWHO Guideline (40 µg/m³):")
    print(f"  Records above guideline: {above_who} ({percent_above:.1f}%)")
    
    # Preview data
    print("\n" + "="*80)
    print("DATA PREVIEW")
    print("="*80)
    print(combined_df.head(10))
    
    print("\n✅ Processing complete!")
    print("\n📝 Next steps:")
    print("1. The air_quality_no2.csv file is ready for your Streamlit app")
    print("2. Run: streamlit run Home.py")
    print("3. Navigate to 'Air Quality' page to see NO₂ visualization")
    
    return combined_df


if __name__ == "__main__":
    # Process all downloaded NetCDF files
    df = process_all_no2_files()
    
    # Optional: Create additional file with pollution categories
    if df is not None and not df.empty:
        print("\n" + "="*80)
        print("CREATING POLLUTION HOTSPOTS FILE")
        print("="*80)
        
        # Calculate pollution categories
        df_hotspots = df.copy()
        df_hotspots['category'] = pd.cut(
            df_hotspots['value'],
            bins=[0, 40, 80, 120, float('inf')],
            labels=['Good', 'Moderate', 'Unhealthy', 'Very Unhealthy']
        )
        
        # Keep only high pollution areas
        hotspots = df_hotspots[df_hotspots['value'] > 80].copy()
        
        if not hotspots.empty:
            hotspots.to_csv('data/pollution_hotspots.csv', index=False)
            print(f"✅ Saved {len(hotspots)} pollution hotspots to: data/pollution_hotspots.csv")
        else:
            print("ℹ️ No pollution hotspots found (all values below 80 µg/m³)")
