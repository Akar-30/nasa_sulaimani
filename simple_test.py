#!/usr/bin/env python3
"""
Simple plotly timestamp test
"""

import pandas as pd
import plotly.express as px

# Create simple test data
df = pd.DataFrame({
    'date': pd.to_datetime(['2020-01-01', '2020-06-01', '2020-12-01']),
    'value': [10, 20, 30]
})

print("📊 Creating test chart...")
fig = px.line(df, x='date', y='value', title='Test Chart')

print("🧪 Testing add_vline with string date...")
try:
    fig.add_vline(x='2020-06-01', line_dash="dot", line_color="gray")
    print("✅ add_vline with string: SUCCESS")
except Exception as e:
    print(f"❌ add_vline with string: {e}")

print("🧪 Testing add_vrect with string dates...")
try:
    fig.add_vrect(x0='2020-03-01', x1='2020-09-01', fillcolor="lightblue", opacity=0.2)
    print("✅ add_vrect with strings: SUCCESS")
except Exception as e:
    print(f"❌ add_vrect with strings: {e}")

print("\n🎯 Timestamp fixes validation complete!")