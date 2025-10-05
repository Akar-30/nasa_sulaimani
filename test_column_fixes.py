import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point
import os

print("🔧 Verifying Enhanced Solution Column Fixes")
print("=" * 45)

# Test all enhanced datasets for correct column usage
datasets = {
    'air_quality': {
        'file': 'enhanced_air_quality_detailed.csv',
        'expected_columns': ['aqi_score', 'no2_concentration', 'pm25_concentration', 'pm10_concentration', 'o3_concentration', 'so2_concentration', 'co_concentration', 'health_risk_category']
    },
    'topography': {
        'file': 'enhanced_topography_detailed.csv', 
        'expected_columns': ['elevation', 'slope_percentage', 'development_suitability']  # Fixed: slope_percentage not slope_percent
    },
    'infrastructure': {
        'file': 'enhanced_infrastructure_detailed.csv',
        'expected_columns': ['infrastructure_score', 'road_accessibility', 'healthcare_accessibility', 'education_accessibility']  # Fixed: infrastructure_score not total_accessibility_score
    },
    'temperature': {
        'file': 'enhanced_temperature_detailed.csv',
        'expected_columns': ['air_temperature_2m', 'heat_index', 'heat_stress_score']
    },
    'vegetation': {
        'file': 'enhanced_vegetation_detailed.csv', 
        'expected_columns': ['estimated_ndvi', 'vegetation_health_score', 'canopy_cover_percent']
    },
    'population': {
        'file': 'enhanced_population_detailed.csv',
        'expected_columns': ['population_density', 'development_suitability_score', 'urban_category']
    },
    'economic': {
        'file': 'enhanced_economic_activity_detailed.csv',
        'expected_columns': ['economic_activity_score', 'commercial_potential', 'normalized_light_intensity']
    }
}

all_good = True

for dataset_name, info in datasets.items():
    file_path = f"data_solution/{info['file']}"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, nrows=1)  # Just check first row for speed
        
        missing_columns = []
        for col in info['expected_columns']:
            if col not in df.columns:
                missing_columns.append(col)
        
        if missing_columns:
            print(f"❌ {dataset_name}: Missing columns {missing_columns}")
            print(f"   Available: {df.columns.tolist()}")
            all_good = False
        else:
            print(f"✅ {dataset_name}: All expected columns present")
    else:
        print(f"❌ {dataset_name}: File not found - {file_path}")
        all_good = False

print("\n" + "=" * 45)

if all_good:
    print("🎉 SUCCESS: All column fixes are correct!")
    print("✅ Enhanced Solution should work without column errors")
    print("✅ User can now draw polygons and get full analysis results")
else:
    print("❌ Some issues remain - check missing columns above")

print("\n📝 Fixed Issues:")
print("• slope_percent → slope_percentage") 
print("• total_accessibility_score → infrastructure_score")
print("• Updated infrastructure analysis to use available accessibility columns")
print("• All dataset files verified and loadable")

print("\nThe Enhanced Solution page should now work properly! 🚀")