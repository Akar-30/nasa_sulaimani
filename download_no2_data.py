"""
Download Sentinel-5P NO₂ data for Sulaimani from S5P-PAL Data Portal
"""

from pystac import Catalog
from pystac_client import ItemSearch
import requests
import os
import json
from datetime import datetime, timedelta

# S5P-PAL API endpoint
L2_CATALOG = "https://data-portal.s5p-pal.com/api/s5p-l2"

# Sulaimani bounding box (expanded coverage)
SULAIMANI_BBOX = {
    'type': 'Polygon',
    'coordinates': [[
        [45.25, 35.40],  # Southwest
        [45.62, 35.40],  # Southeast
        [45.62, 35.72],  # Northeast
        [45.25, 35.72],  # Northwest
        [45.25, 35.40]   # Close polygon
    ]]
}

def search_no2_products(start_date, end_date, max_products=50):
    """
    Search for NO₂ products for Sulaimani area
    
    Args:
        start_date (str): Start date in format 'YYYY-MM-DD'
        end_date (str): End date in format 'YYYY-MM-DD'
        max_products (int): Maximum number of products to retrieve
    
    Returns:
        list: List of STAC items matching the criteria
    """
    print(f"Searching for NO₂ products from {start_date} to {end_date}...")
    print(f"Area: Sulaimani (45.25-45.62°E, 35.40-35.72°N)")
    
    catalog = Catalog.from_file(L2_CATALOG)
    endpoint = catalog.get_single_link("search").target
    
    # Search parameters
    timefilter = f"{start_date}/{end_date}"
    
    # Use filter to select only NO₂ products (L2__NO2___)
    filter_query = "s5p:file_type='L2__NO2___'"
    
    items = ItemSearch(
        endpoint,
        datetime=timefilter,
        intersects=SULAIMANI_BBOX,
        filter=filter_query,
        max_items=max_products
    ).items()
    
    items_list = list(items)
    print(f"Found {len(items_list)} NO₂ products for Sulaimani")
    
    return items_list


def display_product_info(items):
    """Display information about found products"""
    print("\n" + "="*80)
    print("AVAILABLE NO₂ PRODUCTS:")
    print("="*80)
    
    for i, item in enumerate(items, 1):
        # Extract product metadata
        product_id = item.id
        start_time = item.properties.get('start_datetime', 'N/A')
        end_time = item.properties.get('end_datetime', 'N/A')
        orbit = item.properties.get('s5p:orbit', 'N/A')
        
        # Get file info from assets
        if 'product' in item.assets:
            product = item.assets['product']
            file_path = product.extra_fields.get('file:local_path', 'N/A')
            file_size_mb = product.extra_fields.get('file:size', 0) / (1024 * 1024)
        else:
            file_path = 'N/A'
            file_size_mb = 0
        
        print(f"\n{i}. Product ID: {product_id}")
        print(f"   Time: {start_time} to {end_time}")
        print(f"   Orbit: {orbit}")
        print(f"   File: {file_path}")
        print(f"   Size: {file_size_mb:.2f} MB")


def download_product(item, output_dir='data/raw_no2'):
    """
    Download a single NO₂ product
    
    Args:
        item: STAC item to download
        output_dir (str): Directory to save the file
    
    Returns:
        str: Path to downloaded file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get product information
    product = item.assets['product']
    download_url = product.href
    product_local_path = product.extra_fields['file:local_path']
    product_size = product.extra_fields['file:size']
    
    # Local file path
    local_filename = os.path.join(output_dir, os.path.basename(product_local_path))
    
    # Check if file already exists
    if os.path.exists(local_filename):
        file_size = os.path.getsize(local_filename)
        if file_size == product_size:
            print(f"✅ File already exists and matches size: {local_filename}")
            return local_filename
    
    # Download the file
    print(f"Downloading {os.path.basename(product_local_path)}...")
    print(f"Size: {product_size / (1024 * 1024):.2f} MB")
    
    try:
        r = requests.get(download_url, stream=True)
        r.raise_for_status()
        
        # Download with progress indication
        downloaded = 0
        chunk_size = 8192
        
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = (downloaded / product_size) * 100
                    print(f"\rProgress: {percent:.1f}%", end='', flush=True)
        
        print()  # New line after progress
        
        # Verify file size
        file_size = os.path.getsize(local_filename)
        if file_size == product_size:
            print(f"✅ Download successful: {local_filename}")
            return local_filename
        else:
            print(f"❌ Warning: File size mismatch ({file_size} vs {product_size})")
            return None
            
    except Exception as e:
        print(f"❌ Error downloading file: {e}")
        return None


def download_recent_no2_data(days_back=30, max_products=10):
    """
    Download recent NO₂ data for Sulaimani
    
    Args:
        days_back (int): How many days back to search
        max_products (int): Maximum number of products to download
    """
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    print("="*80)
    print("SENTINEL-5P NO₂ DATA DOWNLOADER FOR SULAIMANI")
    print("="*80)
    
    # Search for products
    items = search_no2_products(start_date_str, end_date_str, max_products)
    
    if not items:
        print("\n❌ No products found for the specified time period and location.")
        print("\nTips:")
        print("- Try increasing the time period (days_back parameter)")
        print("- Check if the S5P-PAL service is accessible")
        print("- Verify that Sulaimani is within satellite coverage")
        return []
    
    # Display product information
    display_product_info(items)
    
    # Ask user which products to download
    print("\n" + "="*80)
    print("DOWNLOAD OPTIONS:")
    print("="*80)
    print(f"Found {len(items)} product(s)")
    
    choice = input(f"\nDownload all products? (y/n) [default: y]: ").strip().lower()
    
    downloaded_files = []
    
    if choice == 'n':
        # Allow user to select specific products
        indices = input(f"Enter product numbers to download (comma-separated, e.g., 1,3,5): ").strip()
        try:
            selected_indices = [int(i.strip()) - 1 for i in indices.split(',')]
            selected_items = [items[i] for i in selected_indices if 0 <= i < len(items)]
        except:
            print("Invalid input. Downloading all products...")
            selected_items = items
    else:
        selected_items = items
    
    # Download selected products
    print(f"\n📥 Downloading {len(selected_items)} product(s)...\n")
    
    for i, item in enumerate(selected_items, 1):
        print(f"\n--- Downloading {i}/{len(selected_items)} ---")
        file_path = download_product(item)
        if file_path:
            downloaded_files.append(file_path)
    
    # Summary
    print("\n" + "="*80)
    print("DOWNLOAD SUMMARY")
    print("="*80)
    print(f"✅ Successfully downloaded {len(downloaded_files)} file(s)")
    
    if downloaded_files:
        print("\nDownloaded files:")
        for file_path in downloaded_files:
            print(f"  - {file_path}")
        
        print("\n📝 Next steps:")
        print("1. Process the NetCDF files to extract NO₂ values for Sulaimani")
        print("2. Create air_quality_no2.csv with format: date,lat,lon,value")
        print("3. Save to /data folder for use in Streamlit app")
        print("\nRun: python process_no2_netcdf.py (to be created)")
    
    return downloaded_files


def search_by_date_range(start_date, end_date):
    """
    Search and display products for a specific date range
    (useful for finding data for specific time periods)
    """
    items = search_no2_products(start_date, end_date, max_products=100)
    
    if items:
        display_product_info(items)
        
        # Save product list to JSON for reference
        products_info = []
        for item in items:
            products_info.append({
                'id': item.id,
                'start_time': item.properties.get('start_datetime'),
                'end_time': item.properties.get('end_datetime'),
                'orbit': item.properties.get('s5p:orbit'),
                'download_url': item.assets['product'].href if 'product' in item.assets else None
            })
        
        with open('data/no2_products_list.json', 'w') as f:
            json.dump(products_info, f, indent=2)
        
        print(f"\n📝 Product list saved to: data/no2_products_list.json")
    
    return items


if __name__ == "__main__":
    # Example 1: Download recent NO₂ data (last 30 days)
    download_recent_no2_data(days_back=30, max_products=10)
    
    # Example 2: Search for specific date range (uncomment to use)
    # items = search_by_date_range("2024-01-01", "2024-01-31")
    
    # Example 3: Download specific products by date
    # items = search_no2_products("2024-09-01", "2024-09-30", max_products=50)
    # display_product_info(items)
    # if items:
    #     download_product(items[0])  # Download first product
