# World Happiness Report – Python & Streamlit Dashboard

This project analyzes the **World Happiness** dataset and lets you explore it in two ways:

- a **Streamlit web dashboard** (interactive, in your browser)
- a **command‑line script** that runs the full pipeline and saves charts

The code is kept simple and uses:
`pandas`, `numpy`, `matplotlib`, `scipy`, and `streamlit` (plus optional `seaborn`).

---

## 📂 Project Structure

```text
world_happiness_dashboard/
│
├── data/
│   ├── raw/                    # Original dataset (input)
│   └── processed/              # Cleaned data (output)
│
├── reports/                    # Saved plots (PNG files) + insights.txt
│
├── src/
│   ├── data_loader.py          # Load CSV into a DataFrame
│   ├── data_cleaner.py         # Basic cleaning utilities
│   ├── analyzer.py             # Simple analysis helpers
│   ├── index_calculator.py     # Composite happiness index
│   ├── visualizer.py           # Matplotlib plots (used by CLI)
│   └── insight_engine.py       # Rule‑based insights
│   └── main.py                 # Command‑line pipeline
│
├── streamlit_app.py            # Interactive Streamlit dashboard
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

The same core modules (`data_loader`, `data_cleaner`, `analyzer`, `index_calculator`,
`insight_engine`) are reused by both the CLI script and the Streamlit app.

---

## 🔧 Setup

1. Open a terminal in the project root:

   ```bash
   cd world_happiness_dashboard
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Put the dataset in place:

   - Copy `WorldHappiness.csv` into:  
     `data/raw/WorldHappiness.csv`

The CSV should have at least:

- `Country`, `Region`, `Happiness Score`, and ideally:
- `Happiness Rank`, `Economy (GDP per Capita)`, `Family`,
  `Health (Life Expectancy)`, `Freedom`,
  `Trust (Government Corruption)`, `Generosity`,
  and optionally `Year`.

---

## 🌐 Option 1 – Run the Streamlit Dashboard (Recommended)

Start the interactive dashboard:

```bash
streamlit run streamlit_app.py
```

What happens:

1. `streamlit_app.py` calls `load_and_clean_data()` (cached with `@st.cache_data`):
   - Uses `DataLoader` to read `data/raw/WorldHappiness.csv`
   - Uses `DataCleaner` to:
     - standardize country/region names  
     - fill missing numeric values  
     - convert `Year` to numeric (if present)  
     - drop duplicates
2. The cleaned DataFrame is passed to the different pages below.

### Dashboard pages

- **🏠 Overview**
  - Key metrics: average happiness, total countries, highest/lowest scores
  - Top N and bottom N countries by `Happiness Score` (bar charts)
  - Scatter: `Economy (GDP per Capita)` vs `Happiness Score`

- **📈 Country Analysis**
  - Pick a country from the sidebar
  - Shows metrics for that country (happiness, GDP, life expectancy, freedom)
  - Bar chart of the main indicator scores
  - Country comparison table for the top N happiest countries

- **🌎 Regional Analysis**
  - Uses `Analyzer.regional_average_happiness()` to compute:
    - average happiness, standard deviation, and count per region
  - Bar chart of average happiness by region + table of stats
  - Histogram comparing score distributions for selected regions

- **📊 Correlation Analysis**
  - Uses `Analyzer.correlation_analysis(method="both")` on numeric columns
  - Pearson and Spearman correlation matrices (heatmaps)
  - Bar chart for correlations with `Happiness Score`
  - Correlation table

- **🔍 Composite Index**
  - Uses `IndexCalculator` to compute `Composite_Happiness_Index` (0–10) and `Composite_Rank`
  - Optional sliders to set custom weights for:
    - Economy, Family, Health, Freedom, Trust, Generosity
  - Shows metrics for the index (mean, median, std, range)
  - Chart comparing original happiness score vs composite index
  - Table with detailed comparison (optionally includes original happiness rank)

- **💡 Insights**
  - Uses `InsightEngine.generate_all_insights()` to create short text insights, e.g.:
    - high GDP but low happiness
    - stable vs volatile happiness over years
    - score outliers
    - freedom–happiness correlation
    - high generosity but low happiness
  - Also shows:
    - a table of “high GDP, low happiness” countries (if any)
    - a table of happiness outliers

- **🔬 Data Explorer**
  - Choose which columns to show
  - Search by country name
  - Sort by happiness score or country
  - Download the filtered table as CSV
  - See summary statistics for selected numeric columns

---

## 🖥️ Option 2 – Run the Command‑Line Pipeline

You can run the whole analysis from the terminal without the UI:

```bash
python src/main.py
```

`src/main.py` does, in order (matching the code):

1. **Load data**
   - Uses `DataLoader` to read `data/raw/WorldHappiness.csv`
   - Prints shape, columns, and missing values per column
2. **Clean data**
   - Uses `DataCleaner.clean()` (same logic the Streamlit app uses)
   - Saves cleaned CSV to `data/processed/cleaned_data.csv`
3. **Analyze**
   - Uses `Analyzer` to:
     - print top countries by happiness
     - print average happiness by region
     - print top and bottom countries
     - print key correlations with `Happiness Score`
4. **Composite index**
   - Uses `IndexCalculator` to:
     - compute `Composite_Happiness_Index` and `Composite_Rank`
     - print the top 10 countries by this index
     - print basic index statistics (mean, median, std, etc.)
5. **Visualizations**
   - Uses `Visualizer` to create and save PNG files in `reports/`:
     - `country_comparison.png`
     - `region_comparison.png`
     - `gdp_vs_happiness.png`
     - `correlation_heatmap.png`
     - `top_bottom_comparison.png`
6. **Insights**
   - Uses `InsightEngine` to generate rule‑based insights
   - Prints them to the console
   - Saves them to `reports/insights.txt`

At the end you get:

- `data/processed/cleaned_data.csv` – cleaned dataset
- multiple charts in `reports/`
- `reports/insights.txt` – simple text insights

---

## 📝 Summary

- Use **Streamlit** (`streamlit_app.py`) for an interactive dashboard with filters, charts,
  and tables.
- Use **`python src/main.py`** to run the full analysis once and generate all files.

Both paths share the same underlying modules, so the numbers and logic are consistent
between the UI and the command‑line run. If you change a module (for example,
`Analyzer` or `IndexCalculator`), update this README so it keeps matching the code. 


