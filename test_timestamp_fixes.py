#!/usr/bin/env python3
"""
Quick test for temporal visualization fixes in Air Quality page
This script tests the plotly timestamp fixes
"""

import pandas as pd
import plotly.express as px
import streamlit as st

def test_timestamp_fixes():
    """Test the timestamp fixes for plotly charts"""
    print("🧪 Testing Air Quality Page Timestamp Fixes...")
    
    try:
        # Create test data similar to what Air Quality page uses
        dates = pd.date_range('2010-01-01', '2024-12-31', freq='MS')
        values = [20 + i * 0.5 + (i % 12) * 2 for i in range(len(dates))]
        test_data = {
            'date': dates,
            'value': values
        }
        df = pd.DataFrame(test_data)
        
        # Test the chart creation (similar to Air Quality page)
        fig = px.line(
            df,
            x='date',
            y='value',
            title='Test Chart - 15-Year Trends',
            labels={'value': 'Concentration (µg/m³)', 'date': 'Date'},
            markers=True
        )
        
        # Test the problematic functions with string dates (FIXED VERSION)
        fig.add_hline(y=40, line_dash="dash", line_color="orange", 
                      annotation_text="WHO Guideline")
        
        # This should work with string dates
        fig.add_vline(x='2018-01-01', line_dash="dot", line_color="gray",
                      annotation_text="Data Source Transition")
        
        # This should also work with string dates
        fig.add_vrect(x0='2020-03-01', x1='2020-12-31',
                      fillcolor="lightblue", opacity=0.2, annotation_text="COVID-19")
        
        print("✅ Timestamp fixes successful!")
        print("✅ add_vline with string date: WORKING")
        print("✅ add_vrect with string dates: WORKING") 
        print("✅ Chart creation: WORKING")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in timestamp fixes: {e}")
        return False

if __name__ == "__main__":
    success = test_timestamp_fixes()
    if success:
        print("\n🎉 All timestamp fixes are working correctly!")
        print("🚀 Air Quality page should now run without timestamp errors")
    else:
        print("\n💥 There are still issues with timestamp handling")