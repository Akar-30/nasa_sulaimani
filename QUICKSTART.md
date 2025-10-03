# 🚀 QUICK START GUIDE - Sulaimani Sustainable Growth Platform

## ⏱️ Get Running in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

**Windows:**

```bash
install.bat
```

**Mac/Linux:**

```bash
chmod +x install.sh
./install.sh
```

**Or manually:**

```bash
pip install -r requirements.txt
```

---

### Step 2: Run the App (30 seconds)

```bash
streamlit run Home.py
```

The app opens automatically at `http://localhost:8501`

---

### Step 3: Explore the Platform (2 minutes)

Navigate through the pages using the **sidebar**:

1. 🏙️ **The Challenge** - See Sulaimani's urban challenges
2. 📊 **Data Pathway** - Learn about NASA datasets used
3. 💨 **Air Quality** - View pollution maps (placeholder data)
4. 🌡️ **Heat & Greenspace** - Explore heat islands
5. 🏗️ **Urban Growth & Water** - Track expansion
6. ✅ **Solutions & Vision** - See recommendations
7. 👥 **About & Team** - Project information

---

## 📥 Adding Your NASA Data

### Priority Files (Start Here)

1. **Air Quality** (most impactful visualization):

   ```
   data/air_quality_no2.csv
   data/pollution_hotspots.geojson
   ```

2. **Urban Growth** (shows change over time):

   ```
   data/urban_extent_2025.geojson
   data/urban_extent_2015.geojson
   ```

3. **Heat Map**:

   ```
   data/temperature_lst.csv
   data/heat_islands.geojson
   ```

### File Format Example

**CSV File** (`air_quality_no2.csv`):

```csv
date,lat,lon,value
2024-01-15,35.5608,45.4347,45.2
2024-01-15,35.5708,45.4447,52.8
```

**GeoJSON File** (create at [geojson.io](http://geojson.io)):

```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "geometry": {"type": "Polygon", "coordinates": [[[45.4, 35.5], ...]]},
    "properties": {"name": "Downtown", "value": 125}
  }]
}
```

📖 **Full specifications:** See `DATA_GUIDE.md`

---

## 🎯 Your One-Day Development Plan

### Morning (4 hours) - YOUR TASK: Data Preparation

**Hour 1-2: Download NASA Data**

- Google Earth Engine (recommended)
- NASA Earthdata
- Copernicus Hub

**Hour 3-4: Process & Export Data**

- Filter to Sulaimani bounds (35.48-35.64°N, 45.35-45.52°E)
- Export as CSV or GeoJSON
- Save to `/data` folder

### Afternoon (4 hours) - WEBSITE IS ALREADY BUILT

**Hour 5-6: Test & Customize**

- Run `streamlit run Home.py`
- Verify your data loads correctly
- Adjust text/descriptions as needed

**Hour 7-8: Polish & Deploy**

- Add team information to About page
- Take screenshots for presentation
- Deploy to Streamlit Cloud (free!)

---

## 🔧 Common Issues & Solutions

### Issue: "Module not found"

**Solution:** Run `pip install -r requirements.txt`

### Issue: Maps show no data

**Solution:** Check:

1. Files are in `/data` folder
2. Filenames match exactly (case-sensitive)
3. CSV has correct column names
4. Run validation script (see DATA_GUIDE.md)

### Issue: App won't start

**Solution:**

```bash
# Check Streamlit is installed
streamlit --version

# Try running with verbose logging
streamlit run Home.py --logger.level=debug
```

---

## 🌐 Deployment to Streamlit Cloud (FREE!)

### Steps

1. **Push to GitHub**

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO
   git push -u origin main
   ```

2. **Deploy**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Main file: `Home.py`
   - Click "Deploy"

3. **Share!**
   - Your app gets a URL: `https://your-app-name.streamlit.app`
   - Share with NASA judges and community

---

## 📊 What Data Do You Actually Need?

### Minimum Viable Product (MVP)

Just these 3 files to get started:

1. `air_quality_no2.csv` - Shows pollution (any pollutant works)
2. `urban_extent_2025.geojson` - Current city boundary
3. `temperature_lst.csv` OR `ndvi_values.csv` - Heat or vegetation

### Full Experience

All files listed in DATA_GUIDE.md for complete visualizations

---

## 💡 Pro Tips

1. **Start small**: Get 1-2 visualizations working first
2. **Use Google Earth Engine**: Fastest way to process NASA data
3. **Test locally**: Make sure everything works before deploying
4. **Screenshot everything**: For your presentation
5. **Tell a story**: Use the data to support your narrative

---

## 📞 Need Help?

**During development:**

- Check `DATA_GUIDE.md` for data specifications
- Validate GeoJSON at [geojsonlint.com](https://geojsonlint.com)
- Test CSV in Excel/spreadsheet first

**Common resources:**

- Streamlit docs: <https://docs.streamlit.io>
- Folium examples: <https://python-visualization.github.io/folium/>
- Plotly gallery: <https://plotly.com/python/>

---

## ✅ Pre-Presentation Checklist

- [ ] All pages load without errors
- [ ] At least 3-4 maps show real data
- [ ] Team info updated in About page
- [ ] App deployed to Streamlit Cloud
- [ ] Screenshots captured for slides
- [ ] Tested on mobile device
- [ ] Practiced demo (2-3 minutes)

---

## 🎉 You're Ready

The website structure is **100% complete**. Focus your energy on:

1. 📥 **Data preparation** (your expertise!)
2. 🎨 **Content refinement** (adjust text to match your findings)
3. 🚀 **Deployment & presentation**

Good luck with NASA Space Apps Challenge! 🌍🛰️
