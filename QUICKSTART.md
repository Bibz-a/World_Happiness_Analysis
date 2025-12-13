# Quick Start Guide - Streamlit Dashboard

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch the Dashboard**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Open in Browser**
   - The dashboard will automatically open in your default browser
   - If not, navigate to: `http://localhost:8501`

## 📱 Dashboard Pages

### 🏠 Overview
- Key metrics at a glance
- Top and bottom countries
- GDP vs Happiness scatter plot

### 📈 Country Analysis
- Detailed country profiles
- Indicator breakdowns
- Country comparison tables

### 🌎 Regional Analysis
- Regional averages and statistics
- Distribution comparisons
- Multi-region analysis

### 📊 Correlation Analysis
- Interactive correlation heatmaps
- Pearson and Spearman correlations
- Correlation with happiness score

### 🔍 Composite Index
- Custom happiness index calculator
- Adjustable indicator weights
- Comparison with original scores

### 💡 Insights
- Rule-based insight generation
- High GDP, low happiness detection
- Regional trend analysis
- Outlier identification

### 🔬 Data Explorer
- Interactive data table
- Search and filter functionality
- Column selection
- CSV export

## 🎛️ Interactive Features

- **Sidebar Filters**: Filter by region and select countries
- **Sliders**: Adjust number of countries displayed
- **Multi-select**: Choose multiple regions for comparison
- **Search Bar**: Find specific countries quickly
- **Custom Weights**: Configure composite index weights
- **Download**: Export filtered data

## 💡 Tips

- Use the sidebar to filter data by region
- Click "Generate Insights" to get fresh analysis
- Adjust sliders to see more or fewer countries
- Use the search bar in Data Explorer to find specific countries
- Customize composite index weights to see different rankings

## 🐛 Troubleshooting

**Dashboard won't start?**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that `WorldHappiness.csv` is in `data/raw/` directory

**Visualizations not showing?**
- Refresh the page
- Check browser console for errors
- Ensure matplotlib is properly installed

**Data not loading?**
- Verify the CSV file exists in `data/raw/WorldHappiness.csv`
- Check file permissions
- Ensure the file is not corrupted

