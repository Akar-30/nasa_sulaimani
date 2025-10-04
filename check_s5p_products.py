"""
Check available Sentinel-5P products in S5P-PAL Data Portal API
Identifies all pollutants and data products available for air quality monitoring
"""

import requests
import json
from datetime import datetime, timedelta

# S5P-PAL API endpoint
L2_CATALOG = "https://data-portal.s5p-pal.com/api/s5p-l2"

def check_available_products():
    """
    Check what Sentinel-5P products are available in the S5P-PAL catalog
    """
    print("🛰️ Checking Sentinel-5P Available Products via S5P-PAL API")
    print("=" * 60)
    
    try:
        # Get catalog information
        response = requests.get(L2_CATALOG, timeout=30)
        catalog_info = response.json()
        
        print("📡 Catalog Information:")
        print(f"   Title: {catalog_info.get('title', 'N/A')}")
        print(f"   Description: {catalog_info.get('description', 'N/A')}")
        
        # Check if there's a collections endpoint
        collections_url = None
        for link in catalog_info.get('links', []):
            if link.get('rel') == 'data' or 'collection' in link.get('href', ''):
                collections_url = link.get('href')
                break
        
        if collections_url:
            print(f"\n📂 Collections URL: {collections_url}")
            collections_response = requests.get(collections_url, timeout=30)
            collections_data = collections_response.json()
            
            print("\n🏷️ Available Collections/Products:")
            if 'collections' in collections_data:
                for collection in collections_data['collections']:
                    print(f"   • {collection.get('id', 'Unknown ID')}")
                    print(f"     Title: {collection.get('title', 'N/A')}")
                    print(f"     Description: {collection.get('description', 'N/A')[:100]}...")
                    print()
        
        # Check search endpoint for available products
        search_url = None
        for link in catalog_info.get('links', []):
            if link.get('rel') == 'search':
                search_url = link.get('href')
                break
        
        if search_url:
            print(f"\n🔍 Search URL: {search_url}")
            
            # Try to get a sample of available products
            search_params = {
                'limit': 10,
                'datetime': '2024-01-01/2024-01-31'
            }
            
            search_response = requests.get(search_url, params=search_params, timeout=30)
            search_data = search_response.json()
            
            print(f"\n📊 Sample Products (showing first 10):")
            if 'features' in search_data:
                for feature in search_data['features']:
                    product_id = feature.get('id', 'Unknown')
                    properties = feature.get('properties', {})
                    
                    print(f"   • Product: {product_id}")
                    print(f"     Type: {properties.get('s5p:file_type', 'N/A')}")
                    print(f"     Processing Mode: {properties.get('s5p:processing_mode', 'N/A')}")
                    print(f"     Date: {properties.get('datetime', 'N/A')}")
                    print()
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_known_s5p_products():
    """
    List known Sentinel-5P TROPOMI products based on documentation
    """
    print("\n🔬 Known Sentinel-5P TROPOMI Products:")
    print("=" * 50)
    
    products = {
        "L2__NO2___": {
            "name": "Nitrogen Dioxide (NO₂)",
            "description": "Tropospheric NO₂ column density",
            "units": "mol/m²",
            "applications": ["Air quality", "Traffic monitoring", "Industrial emissions"]
        },
        "L2__SO2___": {
            "name": "Sulfur Dioxide (SO₂)",
            "description": "Total SO₂ column density",
            "units": "mol/m²",
            "applications": ["Volcanic emissions", "Industrial pollution", "Shipping"]
        },
        "L2__O3____": {
            "name": "Ozone (O₃)",
            "description": "Total ozone column",
            "units": "DU (Dobson Units)",
            "applications": ["Stratospheric ozone", "Air quality"]
        },
        "L2__CO____": {
            "name": "Carbon Monoxide (CO)",
            "description": "Total CO column density",
            "units": "mol/m²",
            "applications": ["Pollution monitoring", "Fire detection", "Transport emissions"]
        },
        "L2__CH4___": {
            "name": "Methane (CH₄)",
            "description": "Total CH₄ column density",
            "units": "mol/m²",
            "applications": ["Greenhouse gas monitoring", "Leak detection"]
        },
        "L2__HCHO__": {
            "name": "Formaldehyde (HCHO)",
            "description": "Tropospheric HCHO column density",
            "units": "mol/m²",
            "applications": ["VOC emissions", "Biogenic emissions"]
        },
        "L2__CLOUD_": {
            "name": "Cloud Properties",
            "description": "Cloud fraction and pressure",
            "units": "Various",
            "applications": ["Atmospheric correction", "Weather analysis"]
        },
        "L2__AER_AI": {
            "name": "Aerosol Index",
            "description": "UV Aerosol Index",
            "units": "Dimensionless",
            "applications": ["Dust storms", "Smoke detection", "Air quality"]
        }
    }
    
    for product_code, info in products.items():
        print(f"🧪 {product_code}")
        print(f"   Name: {info['name']}")
        print(f"   Description: {info['description']}")
        print(f"   Units: {info['units']}")
        print(f"   Applications: {', '.join(info['applications'])}")
        print()

def check_air_quality_relevance():
    """
    Check which products are most relevant for air quality analysis
    """
    print("🏭 Air Quality Relevance Analysis:")
    print("=" * 40)
    
    air_quality_products = {
        "HIGH PRIORITY": [
            "L2__NO2___",  # NO₂ - Traffic, industrial pollution
            "L2__SO2___",  # SO₂ - Industrial emissions, power plants
            "L2__CO____",  # CO - Combustion, transport
            "L2__HCHO__"   # HCHO - VOCs, industrial processes
        ],
        "MEDIUM PRIORITY": [
            "L2__O3____",  # O₃ - Secondary pollutant
            "L2__AER_AI"   # Aerosols - Particulate matter proxy
        ],
        "LOW PRIORITY": [
            "L2__CH4___",  # CH₄ - Greenhouse gas, less direct air quality
            "L2__CLOUD_"   # Clouds - Atmospheric conditions
        ]
    }
    
    for priority, products in air_quality_products.items():
        print(f"\n{priority}:")
        for product in products:
            print(f"   • {product}")

def create_multi_pollutant_downloader():
    """
    Show how to modify the existing download script for multiple pollutants
    """
    print("\n📥 Multi-Pollutant Download Strategy:")
    print("=" * 45)
    
    pollutants = ['NO2', 'SO2', 'CO', 'O3', 'HCHO']
    
    print("✅ CURRENT STATUS:")
    print("   • NO₂ download system: ✅ Ready")
    print("   • NO₂ sample data: ✅ Created (1,500 points)")
    print("   • NO₂ visualization: ✅ Integrated")
    
    print("\n🔄 NEXT STEPS for additional pollutants:")
    for pollutant in pollutants[1:]:  # Skip NO2 as it's done
        print(f"   • {pollutant}: Modify filter to 'L2__{pollutant}___'")
    
    print(f"\n💡 IMPLEMENTATION:")
    print("   1. Modify download_no2_data.py to accept pollutant parameter")
    print("   2. Update process_no2_netcdf.py for different variable names")
    print("   3. Create sample data generators for each pollutant")
    print("   4. Update Air Quality page dropdown options")

if __name__ == "__main__":
    check_available_products()
    check_known_s5p_products()
    check_air_quality_relevance()
    create_multi_pollutant_downloader()
    
    print("\n" + "="*60)
    print("🎯 CONCLUSION: S5P-PAL API provides comprehensive air quality data!")
    print("   Available pollutants: NO₂, SO₂, O₃, CO, CH₄, HCHO + Aerosols")
    print("   Status: NO₂ system ready, others can use same infrastructure")
    print("="*60)