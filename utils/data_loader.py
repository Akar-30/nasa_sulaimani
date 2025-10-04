"""
Utility functions for loading and processing NASA Earth observation data
"""

import pandas as pd
import geopandas as gpd
import json
import os
from pathlib import Path

# Define data directory
DATA_DIR = Path(__file__).parent.parent / "data"


def load_csv_data(filename):
    """
    Load CSV data file
    
    Args:
        filename (str): Name of the CSV file in the data directory
    
    Returns:
        pandas.DataFrame: Loaded data
    """
    filepath = DATA_DIR / filename
    if filepath.exists():
        return pd.read_csv(filepath)
    else:
        print(f"Warning: {filename} not found in data directory")
        return pd.DataFrame()


def load_geojson(filename):
    """
    Load GeoJSON file
    
    Args:
        filename (str): Name of the GeoJSON file
    
    Returns:
        dict: GeoJSON data
    """
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath, 'r') as f:
            return json.load(f)
    else:
        print(f"Warning: {filename} not found in data directory")
        return None


def load_geodataframe(filename):
    """
    Load GeoJSON as GeoDataFrame
    
    Args:
        filename (str): Name of the GeoJSON file
    
    Returns:
        geopandas.GeoDataFrame: Loaded geodata
    """
    filepath = DATA_DIR / filename
    if filepath.exists():
        return gpd.read_file(filepath)
    else:
        print(f"Warning: {filename} not found in data directory")
        return gpd.GeoDataFrame()


def check_data_files():
    """
    Check which data files are present in the data directory
    
    Returns:
        dict: Dictionary of categories and their file status
    """
    required_files = {
        "Air Quality": [
            "air_quality_no2.csv",
            "air_quality_pm25.csv",
            "pollution_hotspots.geojson",
            "population_density.geojson"
        ],
        "Heat & Vegetation": [
            "temperature_lst.csv",
            "ndvi_values.csv",
            "green_spaces.geojson",
            "heat_islands.geojson"
        ],
        "Urban Growth": [
            "urban_extent_2005.geojson",
            "urban_extent_2010.geojson",
            "urban_extent_2015.geojson",
            "urban_extent_2020.geojson",
            "urban_extent_2025.geojson",
            "population_growth.csv"
        ],
        "Water Resources": [
            "groundwater_trend.csv",
            "precipitation.csv",
            "water_stress_zones.geojson"
        ]
    }
    
    status = {}
    for category, files in required_files.items():
        status[category] = {}
        for filename in files:
            filepath = DATA_DIR / filename
            status[category][filename] = filepath.exists()
    
    return status


def process_air_quality_data(df):
    """
    Process air quality data for visualization
    
    Args:
        df (pandas.DataFrame): Raw air quality data with columns: date, lat, lon, value
    
    Returns:
        pandas.DataFrame: Processed data
    """
    if df.empty:
        return df
    
    # Convert date to datetime if needed
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Add color coding based on pollution levels
    if 'value' in df.columns:
        df['category'] = pd.cut(
            df['value'],
            bins=[0, 40, 80, 120, float('inf')],
            labels=['Good', 'Moderate', 'Unhealthy', 'Very Unhealthy']
        )
    
    return df


def process_temperature_data(df):
    """
    Process land surface temperature data
    
    Args:
        df (pandas.DataFrame): Raw LST data
    
    Returns:
        pandas.DataFrame: Processed data
    """
    if df.empty:
        return df
    
    # Convert date to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Add heat category
    if 'temperature' in df.columns:
        df['heat_category'] = pd.cut(
            df['temperature'],
            bins=[0, 35, 40, 45, float('inf')],
            labels=['Normal', 'Warm', 'Hot', 'Extreme']
        )
    
    return df


def process_ndvi_data(df):
    """
    Process NDVI vegetation data
    
    Args:
        df (pandas.DataFrame): Raw NDVI data
    
    Returns:
        pandas.DataFrame: Processed data
    """
    if df.empty:
        return df
    
    # Convert date to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Add vegetation health category
    if 'ndvi' in df.columns:
        df['veg_health'] = pd.cut(
            df['ndvi'],
            bins=[-1, 0.2, 0.4, 0.6, 1],
            labels=['Bare/Urban', 'Sparse Vegetation', 'Moderate Vegetation', 'Dense Vegetation']
        )
    
    return df


def calculate_statistics(df, column, group_by=None):
    """
    Calculate summary statistics for a column
    
    Args:
        df (pandas.DataFrame): Data
        column (str): Column name to analyze
        group_by (str, optional): Column to group by
    
    Returns:
        pandas.DataFrame: Statistics
    """
    if df.empty or column not in df.columns:
        return pd.DataFrame()
    
    if group_by and group_by in df.columns:
        return df.groupby(group_by)[column].agg(['mean', 'median', 'min', 'max', 'std'])
    else:
        return df[column].describe()


def create_heatmap_data(df, lat_col='lat', lon_col='lon', value_col='value'):
    """
    Prepare data for Folium HeatMap
    
    Args:
        df (pandas.DataFrame): Data with lat, lon, value columns
        lat_col (str): Name of latitude column
        lon_col (str): Name of longitude column
        value_col (str): Name of value column
    
    Returns:
        list: List of [lat, lon, value] for HeatMap
    """
    if df.empty:
        return []
    
    required_cols = [lat_col, lon_col, value_col]
    if not all(col in df.columns for col in required_cols):
        print(f"Warning: Missing required columns {required_cols}")
        return []
    
    return df[[lat_col, lon_col, value_col]].values.tolist()


def get_sulaimani_bounds():
    """
    Get expanded bounding box for Sulaimani (3x coverage area)
    Captures city center plus surrounding suburbs and rural areas
    
    Returns:
        dict: Dictionary with center coordinates and bounds
    """
    return {
        'center': [35.5608, 45.4347],
        'bounds': [
            [35.40, 45.25],  # Southwest (expanded)
            [35.72, 45.62]   # Northeast (expanded)
        ],
        'zoom_default': 11  # Zoom out slightly to show larger area
    }


def format_data_for_plotly(df, x_col, y_col, **kwargs):
    """
    Format data for Plotly charts
    
    Args:
        df (pandas.DataFrame): Data
        x_col (str): X-axis column
        y_col (str): Y-axis column
    
    Returns:
        pandas.DataFrame: Formatted data
    """
    if df.empty:
        return df
    
    if x_col in df.columns and y_col in df.columns:
        return df[[x_col, y_col]].dropna()
    else:
        print(f"Warning: Columns {x_col} or {y_col} not found")
        return pd.DataFrame()
