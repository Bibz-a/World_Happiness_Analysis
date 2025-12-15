# Code Explanation – World Happiness Dashboard (Simplified)


Data always flows like this:

```text
CSV → DataLoader → DataCleaner → Analyzer / IndexCalculator / InsightEngine / Visualizer
          ↑
          ├─ used by src/main.py (CLI)
          └─ used by streamlit_app.py (web dashboard)
```

---

## `src/data_loader.py` – Load the CSV

**Purpose:** read `WorldHappiness.csv` from disk into a pandas `DataFrame`.

Main parts:

- `DataLoader(data_path="data/raw")`
  - Stores the folder where the CSV is expected.

- `load_csv(filename="WorldHappiness.csv")`
  - Builds `path = os.path.join(self.data_path, filename)`.
  - If the file does **not** exist:
    - prints `File not found: ...`
    - returns `None`.
  - If it exists:
    - reads it with `pd.read_csv(path)`
    - saves the result to `self.df`
    - prints how many rows were loaded
    - returns the `DataFrame`.

- Helper methods:
  - `get_data()` – return the loaded DataFrame (or `None`).
  - `get_columns()` – list of column names (or `[]` if not loaded).
  - `get_shape()` – `(rows, cols)` (or `(0, 0)` if not loaded).
  - `get_info()` – prints shape, columns, and missing values per column.

This is used by both `src/main.py` and `streamlit_app.py` as the first step.

---

## `src/data_cleaner.py` – Clean the Data

**Purpose:** take the raw DataFrame and fix common issues so later steps are easier.

Usage pattern:

```python
cleaner = DataCleaner(df)
cleaned_df = cleaner.clean()
```

What `clean()` does internally:

1. **`standardize_country_names()`**
   - If the `Country` column exists:
     - strips whitespace
     - converts names to title case (e.g. `"united states"` → `"United States"`).

2. **`standardize_region_names()`**
   - If the `Region` column exists:
     - strips whitespace around region names.

3. **`handle_missing_values(strategy="mean")`**
   - Looks at **numeric** columns only.
   - For each numeric column with missing values:
     - `"mean"`: fill with the column mean (this is what `clean()` uses).
     - `"median"`: fill with the column median.
     - `"zero"`: fill with 0.
     - `"drop"`: drop rows where that column is missing.

4. **`remove_duplicates()`**
   - Removes duplicate rows using `drop_duplicates()`.

At the end:

- `self.cleaned_df` holds a cleaned copy of the data.
- `clean()` returns the cleaned DataFrame.

Extra helpers:

- `get_cleaned_data()` – return `self.cleaned_df`, or raise if `clean()` hasn’t been called.
- `save_cleaned_data(output_path="data/processed/cleaned_data.csv")`
  - Creates the folder if needed.
  - Writes the cleaned data to CSV (no index).

Both the CLI script and the Streamlit app call `DataCleaner.clean()` on the loaded data.

---

## `src/analyzer.py` – Basic Analysis Helpers

**Purpose:** provide a few simple analysis functions that are reused by `main.py` and
`streamlit_app.py`.

You construct it with:

```python
analyzer = Analyzer(cleaned_df)
```

Key methods:

- `get_top_countries(n=10)`
  - Returns the top `n` countries by `Happiness Score` with columns:
    `Country`, `Region`, `Happiness Score`.

- `get_bottom_countries(n=10)`
  - Same idea, but returns the bottom `n` countries by `Happiness Score`.

- `country_comparison(top_n=10)`
  - Essentially the same as `get_top_countries`, but explicitly used for comparison
    in the Streamlit “Country Analysis” page.

- `top_bottom_countries(top_n=5, bottom_n=5)`
  - Returns a `dict`:
    - `'top'`: DataFrame of top `top_n` countries
    - `'bottom'`: DataFrame of bottom `bottom_n` countries
  - Used by the CLI pipeline to print summary tables.

- `average_happiness_by_region()`
  - Returns a Series of mean `Happiness Score` per `Region`, sorted from highest to lowest.

- `regional_average_happiness()`
  - Returns a DataFrame with **one row per region**, columns:
    - `Average Happiness`, `Std Dev`, `Count`
  - This is exactly what the Streamlit “Regional Analysis” page expects.

- `correlation_matrix()`
  - Basic Pearson correlation matrix for all numeric columns.

- `correlation_analysis(method="both")`
  - Looks at numeric columns and returns a dict with:
    - `'pearson'`: Pearson correlations (if requested)
    - `'spearman'`: Spearman correlations (if requested)
  - Used by:
    - the CLI pipeline to print correlations with `Happiness Score`
    - the Streamlit “Correlation Analysis” page to build heatmaps.

- `correlation_with_happiness(column)`
  - Computes both Pearson and Spearman correlation between a given column and
    `Happiness Score`.
  - Returns a small dict like `{"pearson": value, "spearman": value}` or `None` if
    there are not enough data points.

- `year_trend(year_col="Year")`
  - If a `Year` column exists:
    - returns average happiness per year.
  - Otherwise, returns `None`.

- `year_change_for_country(country, year_col="Year")`
  - If enough data exist for the country:
    - returns the change in happiness score from first year to last year.

- `summary_stats()`
  - Returns `df.describe()` for quick numeric summary.

---

## `src/index_calculator.py` – Composite Happiness Index

**Purpose:** compute a simple index that combines several happiness dimensions into a
single score between 0 and 10, plus a rank.

Default indicators:

- `Economy (GDP per Capita)`
- `Family`
- `Health (Life Expectancy)`
- `Freedom`
- `Trust (Government Corruption)`
- `Generosity`

Each indicator starts with an equal weight (1 / number of indicators).  
You can override them using `set_weights(weights)`; if the weights don’t sum to 1, they
are normalized automatically.

### Normalization (`normalize_min_max`)

For each indicator column that exists in the DataFrame:

- find its min and max
- if `max - min > 0`:
  - create a new column `<indicator>_normalized = (value - min) / (max - min)` (0–1)
- else:
  - set `<indicator>_normalized = 0.5` for all rows (no variation).

The normalized data is stored in `self.index_df`.

### Composite index (`calculate_composite_index`)

Steps:

1. Ensure `normalize_min_max()` has been called (if not, call it).
2. Start with a score of 0 for every row.
3. For each indicator:
   - multiply the normalized column by its weight.
   - add that to the score.
4. Multiply by 10 to form `Composite_Happiness_Index` on a 0–10 scale.
5. Compute `Composite_Rank` where 1 = highest composite score.

Extra helper methods:

- `compare_with_original()`
  - Returns a DataFrame with:
    - `Country`, `Region`, `Happiness Score`,
      `Composite_Happiness_Index`, `Composite_Rank`
    - If `Happiness Rank` exists:
      - includes original rank and `Rank_Difference`
    - Adds `Score_Difference` (composite index – original happiness score).

- `get_index_statistics()`
  - Returns a small dict with stats for `Composite_Happiness_Index`:
    - mean, median, std, min, max, 25th and 75th percentiles.

The Streamlit “Composite Index” page and the CLI both rely on this class.

---

## `src/visualizer.py` – Matplotlib Plots (CLI)

**Purpose:** create and save charts used by the command‑line pipeline.

On initialization:

- stores a copy of the DataFrame.
- ensures the output directory exists (default: `reports`).
- sets a simple seaborn‑style plot theme.

Key plot functions:

- `plot_country_comparison(top_n=15, filename="country_comparison.png")`
  - Horizontal bar chart of the top N countries by `Happiness Score`.

- `plot_region_comparison(filename="region_comparison.png")`
  - Bar chart of average happiness by region.

- `plot_happiness_trends(year_column="Year", countries=None, filename="happiness_trends.png")`
  - Line plot of happiness over time (global average or per country).

- `plot_gdp_vs_happiness(filename="gdp_vs_happiness.png")`
  - Scatter: `Economy (GDP per Capita)` vs `Happiness Score`, with a simple linear trend line.

- `plot_correlation_heatmap(filename="correlation_heatmap.png")`
  - Numeric correlation heatmap.

- `plot_top_bottom_comparison(top_n=10, bottom_n=10, filename="top_bottom_comparison.png")`
  - Side‑by‑side bar charts for top N and bottom N countries.

Each function calls `plt.savefig(...)` into the `reports` folder and then `plt.show()`.

---

## `src/insight_engine.py` – Rule‑Based Insights

**Purpose:** generate simple text insights from the cleaned data using **rules**, not
machine learning.

Usage:

```python
engine = InsightEngine(cleaned_df)
insights = engine.generate_all_insights()
engine.print_insights()
engine.save_insights("reports/insights.txt")
```

Key methods:

- `find_high_gdp_low_happiness(gdp_threshold=1.0, happiness_threshold=5.0)`
  - Finds countries where:
    - GDP per capita ≥ threshold
    - `Happiness Score` ≤ threshold
  - Adds a textual insight to `self.insights` and returns the filtered DataFrame.

- `analyze_regional_trends(year_column="Year")`
  - (Logic is present but not included in `generate_all_insights()` in the current code.)
  - Looks at happiness by region over time and collects “improving” and “declining”
    regions based on the change from first to last year.

- `identify_stable_vs_volatile(year_column="Year", stability_threshold=0.2)`
  - For each country, computes the standard deviation of its `Happiness Score` over years:
    - small std → “stable”
    - large std → “volatile”
  - Adds summary text about stable and volatile countries to `self.insights`.

- `find_happiness_outliers(method="iqr")`
  - Uses the IQR method (or a z‑score based fallback) to find happiness score outliers.
  - Adds a short summary listing a few outlier countries to `self.insights`.

- `analyze_freedom_happiness_correlation()`
  - Computes correlation between `Freedom` and `Happiness Score`.
  - Classifies it as strong, moderate, or weak and appends a message.

- `find_high_generosity_low_happiness(...)`
  - Similar to the GDP rule, but for `Generosity` vs `Happiness Score`.

- `generate_all_insights()`
  - Resets `self.insights` and then calls:
    - `find_high_gdp_low_happiness`
    - `identify_stable_vs_volatile`
    - `find_happiness_outliers`
    - `analyze_freedom_happiness_correlation`
    - `find_high_generosity_low_happiness`
  - Returns the list of all text insights.

- `print_insights()` and `save_insights(filename)`
  - Print insights to the console and save them as a numbered list in a text file.

The Streamlit “Insights” page calls `generate_all_insights()` and then displays each
insight with `st.info(...)`, as well as showing some of the supporting tables.

---

## `src/main.py` – Command‑Line Pipeline

**Purpose:** run the full pipeline once from the terminal.

When you run:

```bash
python src/main.py
```

`main()` does, in this order:

1. Print a title banner.
2. **Load data** with `DataLoader` from `data/raw/WorldHappiness.csv`.
3. **Clean data** with `DataCleaner.clean()` and save the cleaned CSV to
   `data/processed/cleaned_data.csv`.
4. **Analyze** with `Analyzer`:
   - top countries
   - average happiness by region
   - top and bottom countries
   - key correlations with `Happiness Score`.
5. **Build composite index** with `IndexCalculator`:
   - compute `Composite_Happiness_Index` and `Composite_Rank`
   - print top countries and index statistics.
6. **Visualize** with `Visualizer`:
   - save PNG charts into `reports/`.
7. **Generate insights** with `InsightEngine`:
   - print insights to the console
   - save them to `reports/insights.txt`.

If anything goes wrong (missing file, unexpected error), the script prints a readable
error message and exits.

---

## `streamlit_app.py` – Interactive Web Dashboard

**Purpose:** provide a friendly, interactive way to explore the same cleaned dataset in
your browser.

Key points:

- Uses `@st.cache_data` to load + clean the data once.
- Uses the **same** helper classes as the CLI:
  - `DataLoader`, `DataCleaner`, `Analyzer`, `IndexCalculator`, `InsightEngine`.
- Organizes the UI into several pages:
  - Overview, Country Analysis, Regional Analysis,
    Correlation Analysis, Composite Index, Insights, Data Explorer.
- Uses standard Streamlit widgets:
  - `st.sidebar.radio`, `st.sidebar.selectbox`, `st.slider`, `st.multiselect`,
    `st.metric`, `st.dataframe`, `st.pyplot`, etc.

You run it with:

```bash
streamlit run streamlit_app.py
```

The logic and numbers you see in the browser match what the CLI produces, because both
paths are built on the **same underlying modules**.

---


