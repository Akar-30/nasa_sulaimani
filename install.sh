#!/bin/bash
# Installation script for Sulaimani Sustainable Growth Platform

echo "🌍 Sulaimani Sustainable Growth Platform - Setup"
echo "=============================================="
echo ""

# Check Python version
echo "Checking Python version..."
python --version

echo ""
echo "Installing required packages..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "To run the application:"
echo "  streamlit run Home.py"
echo ""
echo "The app will open at http://localhost:8501"
echo ""
echo "📥 Don't forget to add your NASA data files to the /data directory!"
echo "   See DATA_GUIDE.md for details"
