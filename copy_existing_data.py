"""
Copy existing air quality and climate data to data_solution folder
"""

import pandas as pd
import os
import shutil

def copy_existing_data():
    """Copy existing datasets to data_solution folder"""
    print("📂 Copying existing data to data_solution folder...")
    
    os.makedirs('data_solution', exist_ok=True)
    
    # Copy air quality data if available
    air_files = [
        'data/air_quality_no2_15_year.csv',
        'data/air_quality_co_15_year.csv', 
        'data/air_quality_so2_15_year.csv',
        'data/air_quality_o3_15_year.csv',
        'data/air_quality_hcho_15_year.csv',
        'data/air_quality_aer_ai_15_year.csv',
        'data/composite_air_quality_index.csv'
    ]
    
    for file in air_files:
        if os.path.exists(file):
            dest = file.replace('data/', 'data_solution/enhanced_')
            shutil.copy2(file, dest)
            print(f"✅ Copied {file} -> {dest}")
    
    # Copy climate data if available
    climate_files = [
        'data/temperature_data.csv',
        'data/vegetation_data.csv',
        'data/daily_temperature_summary.csv',
        'data/daily_vegetation_summary.csv'
    ]
    
    for file in climate_files:
        if os.path.exists(file):
            dest = file.replace('data/', 'data_solution/enhanced_')
            shutil.copy2(file, dest)
            print(f"✅ Copied {file} -> {dest}")
    
    # Copy population data if available
    pop_files = [
        'data/population_density_0.010_0.15_2023.csv',
        'data/population_density_0.005_0.20_2023.csv',
        'data/neighborhood_population.csv'
    ]
    
    for file in pop_files:
        if os.path.exists(file):
            dest = file.replace('data/', 'data_solution/enhanced_')
            shutil.copy2(file, dest)
            print(f"✅ Copied {file} -> {dest}")
    
    # Copy nightlights data if available
    lights_files = [
        'data/nightlights_data_0.010_0.15_2023.csv',
        'data/nightlights_data_0.020_0.10_2023.csv'
    ]
    
    for file in lights_files:
        if os.path.exists(file):
            dest = file.replace('data/', 'data_solution/enhanced_')
            shutil.copy2(file, dest)
            print(f"✅ Copied {file} -> {dest}")
    
    # Copy infrastructure data if available
    infra_files = [
        'data/infrastructure_data_0.010_0.15_10.0.csv',
        'data/infrastructure_data_0.010_0.30_10.0.csv'
    ]
    
    for file in infra_files:
        if os.path.exists(file):
            dest = file.replace('data/', 'data_solution/enhanced_')
            shutil.copy2(file, dest)
            print(f"✅ Copied {file} -> {dest}")
    
    print("📊 Data copying complete!")

if __name__ == "__main__":
    copy_existing_data()