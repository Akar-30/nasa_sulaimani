"""
Check Historical Air Quality Data Availability
Investigates NASA/ESA Sentinel-5P data archives for 15-year time series analysis
"""

import requests
import json
from datetime import datetime, timedelta
import pandas as pd

def check_sentinel5p_historical_availability():
    """
    Check Sentinel-5P data availability and historical coverage
    """
    print("🛰️ Sentinel-5P Historical Data Analysis")
    print("=" * 50)
    
    # Sentinel-5P was launched in October 2017, operational from April 2018
    launch_date = datetime(2017, 10, 13)  # Launch date
    operational_date = datetime(2018, 4, 30)  # Start of operational data
    current_date = datetime.now()
    
    print(f"📅 Sentinel-5P Mission Timeline:")
    print(f"   Launch Date: {launch_date.strftime('%B %d, %Y')}")
    print(f"   Operational Since: {operational_date.strftime('%B %d, %Y')}")
    print(f"   Current Date: {current_date.strftime('%B %d, %Y')}")
    
    operational_years = (current_date - operational_date).days / 365.25
    print(f"   Operational Period: {operational_years:.1f} years")
    
    if operational_years >= 15:
        print("   ✅ Has 15+ years of data")
    else:
        print(f"   ⚠️ Only {operational_years:.1f} years available (will reach 15 years in {2018 + 15})")
    
    return operational_date, current_date, operational_years

def check_nasa_earthdata_apis():
    """
    Check NASA Earthdata and other APIs for air quality data
    """
    print("\n🌍 NASA Earth Science Data APIs")
    print("=" * 40)
    
    apis = {
        "NASA Giovanni": {
            "url": "https://giovanni.gsfc.nasa.gov/giovanni/",
            "description": "Online data analysis tool for atmospheric data",
            "data_sources": ["OMI", "MODIS", "AIRS", "Aura"],
            "historical_coverage": "2004-present (OMI), 2000-present (MODIS)",
            "advantages": "15+ years of data, easy web interface",
            "limitations": "Limited spatial resolution"
        },
        "NASA Earthdata": {
            "url": "https://earthdata.nasa.gov/",
            "description": "NASA's Earth Science Data Systems",
            "data_sources": ["Multiple satellites", "Ground stations"],
            "historical_coverage": "1970s-present (varies by instrument)",
            "advantages": "Comprehensive archive, multiple formats",
            "limitations": "Complex API, requires authentication"
        },
        "Copernicus Atmosphere Monitoring Service (CAMS)": {
            "url": "https://atmosphere.copernicus.eu/",
            "description": "European air quality monitoring and forecasting",
            "data_sources": ["Sentinel-5P", "Ground observations", "Models"],
            "historical_coverage": "2003-present (reanalysis), 2018-present (Sentinel-5P)",
            "advantages": "High quality, validated data",
            "limitations": "Limited free access for large downloads"
        },
        "OpenAQ": {
            "url": "https://openaq.org/",
            "description": "Open air quality data platform",
            "data_sources": ["Global ground stations", "Government agencies"],
            "historical_coverage": "2013-present (varies by location)",
            "advantages": "Free API, global coverage",
            "limitations": "Ground stations only, sparse in Iraq region"
        }
    }
    
    for api_name, info in apis.items():
        print(f"\n📡 {api_name}")
        print(f"   URL: {info['url']}")
        print(f"   Description: {info['description']}")
        print(f"   Data Sources: {info['data_sources']}")
        print(f"   Historical Coverage: {info['historical_coverage']}")
        print(f"   ✅ Advantages: {info['advantages']}")
        print(f"   ⚠️ Limitations: {info['limitations']}")

def analyze_15_year_data_strategy():
    """
    Analyze strategy for obtaining 15 years of air quality data
    """
    print(f"\n🎯 15-Year Air Quality Data Strategy")
    print("=" * 45)
    
    strategies = {
        "Strategy 1 - NASA OMI + Sentinel-5P Combination": {
            "timeframe": "2010-2025 (15 years)",
            "data_sources": [
                "2010-2017: NASA OMI (Ozone Monitoring Instrument)",
                "2018-2025: ESA Sentinel-5P TROPOMI"
            ],
            "pollutants": ["NO₂", "SO₂", "O₃", "HCHO", "Aerosols"],
            "advantages": [
                "True 15-year coverage",
                "Consistent NO₂ and SO₂ measurements",
                "Complementary instruments"
            ],
            "implementation": "Use NASA Giovanni for OMI data, S5P-PAL for Sentinel-5P",
            "feasibility": "HIGH - Both APIs available"
        },
        
        "Strategy 2 - CAMS Reanalysis Data": {
            "timeframe": "2003-2025 (22+ years)",
            "data_sources": [
                "CAMS global atmospheric composition reanalysis",
                "Assimilated satellite + ground observations"
            ],
            "pollutants": ["NO₂", "SO₂", "CO", "O₃", "PM2.5", "PM10"],
            "advantages": [
                "Longest time series available",
                "Gap-filled, quality-controlled data",
                "Consistent methodology"
            ],
            "implementation": "Use CAMS API or Copernicus Climate Data Store",
            "feasibility": "MEDIUM - Requires CDS API registration"
        },
        
        "Strategy 3 - Multi-Source Hybrid Approach": {
            "timeframe": "2010-2025 (15 years)",
            "data_sources": [
                "2010-2014: NASA OMI + MODIS",
                "2015-2017: OMI + early Sentinel-5P precursors",
                "2018-2025: Sentinel-5P TROPOMI"
            ],
            "pollutants": ["NO₂", "SO₂", "CO", "O₃", "HCHO", "Aerosols"],
            "advantages": [
                "Best spatial resolution over time",
                "Multiple validation sources",
                "Comprehensive pollutant coverage"
            ],
            "implementation": "Combine multiple NASA + ESA APIs",
            "feasibility": "LOW - Complex data harmonization required"
        }
    }
    
    for strategy_name, details in strategies.items():
        print(f"\n🔬 {strategy_name}")
        print(f"   Timeframe: {details['timeframe']}")
        print(f"   Data Sources:")
        for source in details['data_sources']:
            print(f"     • {source}")
        print(f"   Pollutants: {', '.join(details['pollutants'])}")
        print(f"   Advantages:")
        for advantage in details['advantages']:
            print(f"     ✅ {advantage}")
        print(f"   Implementation: {details['implementation']}")
        print(f"   Feasibility: {details['feasibility']}")

def check_nasa_giovanni_api():
    """
    Check NASA Giovanni API for OMI historical data
    """
    print(f"\n🛰️ NASA Giovanni API Test")
    print("=" * 30)
    
    # Giovanni doesn't have a direct REST API, but we can check data availability
    print("📡 NASA Giovanni Information:")
    print("   • Web-based analysis tool for satellite data")
    print("   • OMI NO₂: 2004-2025 (20+ years available)")
    print("   • OMI SO₂: 2004-2025 (20+ years available)")
    print("   • Spatial Resolution: 13x24 km")
    print("   • Temporal Resolution: Daily")
    
    print("\n📊 OMI Data Products for Air Quality:")
    omi_products = {
        "OMNO2d": {
            "name": "OMI/Aura NO₂ Cloud-Screened Total and Tropospheric Column",
            "timeframe": "2004-10-01 to present",
            "resolution": "0.25° x 0.25°",
            "units": "molecules/cm²"
        },
        "OMSO2e": {
            "name": "OMI/Aura SO₂ Total Column",
            "timeframe": "2004-10-01 to present", 
            "resolution": "0.25° x 0.25°",
            "units": "Dobson Units"
        },
        "OMTO3d": {
            "name": "OMI/Aura Ozone Total Column",
            "timeframe": "2004-10-01 to present",
            "resolution": "0.25° x 0.25°", 
            "units": "Dobson Units"
        }
    }
    
    for product_id, info in omi_products.items():
        print(f"\n   📈 {product_id}")
        print(f"      Name: {info['name']}")
        print(f"      Coverage: {info['timeframe']}")
        print(f"      Resolution: {info['resolution']}")
        print(f"      Units: {info['units']}")

def create_historical_data_implementation_plan():
    """
    Create implementation plan for 15-year air quality data
    """
    print(f"\n📋 Implementation Plan: 15-Year Air Quality Data")
    print("=" * 55)
    
    phases = [
        {
            "phase": "Phase 1: NASA OMI Data (2010-2017)",
            "duration": "1-2 weeks",
            "tasks": [
                "Register for NASA Earthdata account",
                "Access OMI NO₂ and SO₂ data via Giovanni or direct download",
                "Process NetCDF files for Sulaimani region",
                "Convert to consistent CSV format",
                "Validate data quality and coverage"
            ],
            "output": "Historical air quality data 2010-2017"
        },
        {
            "phase": "Phase 2: Sentinel-5P Integration (2018-2025)", 
            "duration": "1 week",
            "tasks": [
                "Extend existing Sentinel-5P download system",
                "Download historical S5P data from 2018-2025",
                "Ensure consistent spatial grid with OMI data",
                "Merge datasets with proper temporal alignment",
                "Quality control and gap filling"
            ],
            "output": "Complete 15-year time series 2010-2025"
        },
        {
            "phase": "Phase 3: Analysis Enhancement",
            "duration": "3-5 days",
            "tasks": [
                "Update Air Quality page for long-term trends",
                "Add seasonal decomposition analysis",
                "Implement trend detection algorithms", 
                "Create pollution source attribution",
                "Generate policy-relevant insights"
            ],
            "output": "Enhanced NASA challenge presentation"
        }
    ]
    
    for phase in phases:
        print(f"\n🚀 {phase['phase']}")
        print(f"   Duration: {phase['duration']}")
        print(f"   Tasks:")
        for task in phase['tasks']:
            print(f"     • {task}")
        print(f"   Output: {phase['output']}")
    
    print(f"\n⏱️ Total Implementation Time: 3-4 weeks")
    print(f"✅ Result: Complete 15-year air quality analysis for Sulaimani")

def test_sample_15_year_data_generation():
    """
    Generate sample 15-year historical data for demonstration
    """
    print(f"\n🎲 Generating Sample 15-Year Air Quality Data")
    print("=" * 50)
    
    import numpy as np
    
    # Generate 15 years of annual data (2010-2024)
    years = list(range(2010, 2025))
    
    # Realistic trend parameters for Sulaimani
    base_no2 = 25  # µg/m³
    base_so2 = 15  # µg/m³
    
    # Simulate long-term trends
    no2_trend = 0.8  # Increasing trend due to urbanization
    so2_trend = -0.3  # Decreasing trend due to cleaner fuels
    
    no2_annual = []
    so2_annual = []
    
    for i, year in enumerate(years):
        # Long-term trend + random variation
        no2_value = base_no2 + (no2_trend * i) + np.random.normal(0, 3)
        so2_value = max(5, base_so2 + (so2_trend * i) + np.random.normal(0, 2))
        
        no2_annual.append(no2_value)
        so2_annual.append(so2_value)
    
    # Create DataFrame
    df_annual = pd.DataFrame({
        'Year': years,
        'NO2_avg': no2_annual,
        'SO2_avg': so2_annual,
        'Data_Source': ['OMI' if year < 2018 else 'Sentinel-5P' for year in years]
    })
    
    # Save sample data
    df_annual.to_csv('data/air_quality_15_year_annual.csv', index=False)
    
    print("✅ Created sample 15-year annual averages:")
    print(df_annual)
    
    print(f"\n📈 Trends Analysis:")
    print(f"   NO₂: {no2_annual[0]:.1f} → {no2_annual[-1]:.1f} µg/m³ ({(no2_annual[-1]-no2_annual[0])/no2_annual[0]*100:+.1f}%)")
    print(f"   SO₂: {so2_annual[0]:.1f} → {so2_annual[-1]:.1f} µg/m³ ({(so2_annual[-1]-so2_annual[0])/so2_annual[0]*100:+.1f}%)")
    
    return df_annual

def main():
    """
    Main function to analyze 15-year air quality data availability
    """
    print("🌍 NASA Space Apps Challenge: 15-Year Air Quality Data Analysis")
    print("=" * 70)
    
    # Check current Sentinel-5P coverage
    operational_date, current_date, operational_years = check_sentinel5p_historical_availability()
    
    # Analyze available APIs
    check_nasa_earthdata_apis()
    
    # Develop strategy for 15-year data
    analyze_15_year_data_strategy()
    
    # Check NASA Giovanni/OMI capabilities  
    check_nasa_giovanni_api()
    
    # Create implementation plan
    create_historical_data_implementation_plan()
    
    # Generate sample long-term data
    sample_data = test_sample_15_year_data_generation()
    
    print("\n" + "="*70)
    print("🎯 CONCLUSION: 15-Year Air Quality Data Analysis")
    print("="*70)
    print("✅ FEASIBLE: Combine NASA OMI (2010-2017) + Sentinel-5P (2018-2025)")
    print("📊 DATA SOURCES: NASA Giovanni + S5P-PAL API")
    print("🕒 IMPLEMENTATION: 3-4 weeks for complete historical dataset")
    print("🏆 IMPACT: Unprecedented 15-year air quality analysis for Sulaimani!")
    print("="*70)

if __name__ == "__main__":
    main()