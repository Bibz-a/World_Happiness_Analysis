# World Happiness Report Dashboard

A comprehensive data analytics project that analyzes the World Happiness Report dataset to uncover global happiness trends, socioeconomic factors, regional differences, and time-based changes. The project generates an analytical dashboard using clean, modular, object-oriented Python code.

## 📋 Project Overview

This project provides a complete data analytics pipeline for the World Happiness Report dataset, including:

- **Data Loading & Cleaning**: Robust CSV loading with missing value handling
- **Statistical Analysis**: Country comparisons, regional analysis, correlation studies
- **Composite Index Calculation**: Custom happiness index using normalized indicators
- **Visualizations**: Multiple matplotlib charts for data exploration
- **Rule-Based Insights**: Automated insight generation from data patterns

## 🏗️ Project Structure

```
world_happiness_dashboard/
│
├── data/
│   ├── raw/                    # Original dataset
│   └── processed/              # Cleaned and processed data
│
├── src/
│   ├── data_loader.py          # CSV data loading module
│   ├── data_cleaner.py         # Data cleaning and preprocessing
│   ├── analyzer.py              # Statistical analysis functions
│   ├── index_calculator.py     # Composite happiness index calculation
│   ├── visualizer.py           # Matplotlib visualization functions
│   ├── insight_engine.py       # Rule-based insight generation
│   └── main.py                 # Main program entry point
│
├── reports/                    # Generated visualizations and insights
│
├── streamlit_app.py           # Interactive Streamlit web application
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd world_happiness_dashboard
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure your dataset is in place:**
   - Place `WorldHappiness.csv` in the `data/raw/` directory
   - The dataset should contain columns: Country, Region, Happiness Rank, Happiness Score, and various indicators

## 📊 Usage

### 🌐 Running the Interactive Streamlit Dashboard (Recommended)

To launch the interactive web-based dashboard:

```bash
streamlit run streamlit_app.py
```

This will:
- Open a web browser with the interactive dashboard
- Provide a user-friendly GUI with multiple pages
- Allow real-time filtering and exploration
- Display interactive visualizations
- Generate insights on-demand

**Dashboard Features:**
- 🏠 **Overview**: Key metrics, top/bottom countries, GDP vs Happiness
- 📈 **Country Analysis**: Detailed country views and comparisons
- 🌎 **Regional Analysis**: Regional statistics and distributions
- 📊 **Correlation Analysis**: Interactive correlation heatmaps
- 🔍 **Composite Index**: Custom happiness index calculator
- 💡 **Insights**: Rule-based data insights
- 🔬 **Data Explorer**: Interactive data table with search and filters

### 📝 Running the Complete Pipeline (Command Line)

To run the entire analytics pipeline from command line:

```bash
python src/main.py
```

This will:
1. Load the dataset from `data/raw/WorldHappiness.csv`
2. Clean and preprocess the data
3. Perform various analyses
4. Calculate composite happiness index
5. Generate visualizations
6. Generate and save insights

### Using Individual Modules

You can also use individual modules programmatically:

```python
from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.analyzer import Analyzer
from src.visualizer import Visualizer

# Load data
loader = DataLoader(data_path="data/raw")
df = loader.load_csv("WorldHappiness.csv")

# Clean data
cleaner = DataCleaner(df)
cleaned_df = cleaner.clean()

# Analyze
analyzer = Analyzer(cleaned_df)
top_countries = analyzer.country_comparison(top_n=10)

# Visualize
visualizer = Visualizer(cleaned_df)
visualizer.plot_country_comparison(top_n=15)
```

## 🔍 Features

### 1. Data Loading (`data_loader.py`)
- Loads CSV files with error handling
- Provides dataset information and statistics
- Supports flexible file paths

### 2. Data Cleaning (`data_cleaner.py`)
- Standardizes country and region names
- Handles missing values (mean, median, or drop)
- Removes duplicates
- Validates cleaned data

### 3. Analysis (`analyzer.py`)
- **Country Comparison**: Top/bottom countries by happiness
- **Regional Analysis**: Average happiness by region
- **Correlation Analysis**: Pearson and Spearman correlations
- **Trend Analysis**: Year-wise happiness trends
- **Year-over-Year Changes**: Track country-specific changes

### 4. Composite Index (`index_calculator.py`)
- Min-Max normalization of indicators
- Weighted composite happiness index
- Comparison with original happiness scores
- Customizable indicator weights

### 5. Visualizations (`visualizer.py`)
- **Bar Charts**: Country and region comparisons
- **Line Charts**: Happiness trends over time
- **Scatter Plots**: GDP vs Happiness correlation
- **Heatmaps**: Correlation matrices
- All plots are saved as high-resolution PNG files

### 6. Insight Engine (`insight_engine.py`)
- **High GDP, Low Happiness**: Identifies paradox cases
- **Regional Trends**: Improving vs declining regions
- **Stability Analysis**: Stable vs volatile countries
- **Outlier Detection**: Statistical outliers
- **Correlation Insights**: Freedom-happiness relationships
- All insights are rule-based and explainable

## 📈 Output Files

After running the pipeline, you'll find:

- `data/processed/cleaned_data.csv`: Cleaned dataset
- `reports/country_comparison.png`: Top countries bar chart
- `reports/region_comparison.png`: Regional averages chart
- `reports/gdp_vs_happiness.png`: GDP-Happiness scatter plot
- `reports/correlation_heatmap.png`: Correlation matrix
- `reports/top_bottom_comparison.png`: Top vs bottom countries
- `reports/insights.txt`: Generated insights report

## 🎯 Key Insights Generated

The insight engine automatically generates insights such as:

- Countries with high GDP but low happiness scores
- Regions showing improvement or decline over time
- Countries with stable vs volatile happiness trends
- Statistical outliers in happiness scores
- Correlation patterns between indicators and happiness

## 🖥️ Interactive Dashboard Features

The Streamlit dashboard provides an intuitive interface with:

### Navigation Pages
- **Overview Dashboard**: Quick metrics and key visualizations
- **Country Analysis**: Deep dive into individual countries
- **Regional Analysis**: Compare regions and their distributions
- **Correlation Analysis**: Explore relationships between variables
- **Composite Index**: Calculate and compare custom happiness indices
- **Insights**: Generate and view rule-based insights
- **Data Explorer**: Browse and filter raw data

### Interactive Features
- **Filters**: Filter by region and select specific countries
- **Sliders**: Adjust number of countries displayed
- **Multi-select**: Choose multiple regions for comparison
- **Search**: Search countries in the data explorer
- **Custom Weights**: Configure composite index weights
- **Download**: Export filtered data as CSV

### Real-time Updates
- All visualizations update based on selected filters
- Instant insight generation
- Dynamic chart rendering
- Responsive layout for different screen sizes

## 🛠️ Technical Details

### Design Principles

- **Object-Oriented Programming**: All modules use classes for clean organization
- **Modular Design**: Each module has a single, clear responsibility
- **Error Handling**: Comprehensive exception handling throughout
- **Documentation**: Docstrings and comments for clarity
- **No Machine Learning**: Pure statistical and rule-based analysis

### Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Data visualization
- **scipy**: Statistical functions (correlation)
- **streamlit**: Interactive web application framework
- **seaborn**: Enhanced statistical visualizations (optional, with fallback)

## 📝 Code Quality

- Clear class and method names
- Comprehensive docstrings
- Exception handling for robustness
- Readable and maintainable code structure
- Semester-appropriate complexity level

## 🔬 Analysis Capabilities

1. **Descriptive Statistics**: Mean, median, standard deviation
2. **Comparative Analysis**: Country and regional comparisons
3. **Correlation Analysis**: Relationships between variables
4. **Trend Analysis**: Time-based patterns (if year data available)
5. **Index Calculation**: Custom composite metrics
6. **Insight Generation**: Automated pattern detection

## 🎓 Educational Value

This project demonstrates:

- Data loading and preprocessing
- Statistical analysis techniques
- Data visualization best practices
- Object-oriented Python programming
- Rule-based insight generation
- Clean code organization

## ⚠️ Notes

- The dataset should be placed in `data/raw/WorldHappiness.csv`
- If the dataset doesn't have a 'Year' column, year-based analyses will be skipped
- All visualizations are saved automatically to the `reports/` directory
- The composite index uses equal weights by default (customizable)

## 📧 Support

For questions or issues:
1. Check that all dependencies are installed
2. Verify the dataset is in the correct location
3. Ensure Python 3.8+ is being used

## 📄 License

This project is created for educational purposes as part of a semester-level data analytics course.

---

**Happy Analyzing! 🌍😊**

