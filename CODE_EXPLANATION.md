# 📚 Complete Code Explanation

This document explains every part of the World Happiness Dashboard codebase in detail.

---

## 🏗️ **Overall Architecture**

The project follows a **modular, object-oriented design** where each module has a specific responsibility:

```
Data Flow:
CSV File → DataLoader → DataCleaner → Analyzer/IndexCalculator/Visualizer/InsightEngine
```

**Key Design Principles:**
1. **Separation of Concerns**: Each class does one thing well
2. **Object-Oriented Programming**: Everything is organized in classes
3. **Method Chaining**: Some methods return `self` for chaining operations
4. **Error Handling**: Try-except blocks handle errors gracefully

---

## 📦 **Module 1: data_loader.py**

### Purpose
Loads CSV files into pandas DataFrames with error handling.

### Class: `DataLoader`

**Attributes:**
- `data_path`: Where to look for CSV files
- `df`: The loaded DataFrame (starts as `None`)

**Key Methods:**

#### `__init__(self, data_path)`
```python
def __init__(self, data_path: str = "data/raw"):
    self.data_path = data_path
    self.df: Optional[pd.DataFrame] = None
```
- **What it does**: Initializes the loader with a data path
- **Why `Optional[pd.DataFrame]`**: Type hint says `df` can be `None` until data is loaded

#### `load_csv(self, filename)`
```python
def load_csv(self, filename: str = "WorldHappiness.csv") -> pd.DataFrame:
    file_path = os.path.join(self.data_path, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")
    self.df = pd.read_csv(file_path)
    return self.df
```
- **What it does**: 
  1. Builds full file path using `os.path.join()` (works on Windows/Mac/Linux)
  2. Checks if file exists
  3. Reads CSV with `pd.read_csv()`
  4. Stores in `self.df` and returns it
- **Error Handling**: Raises `FileNotFoundError` if file missing, `ValueError` if read fails

#### Helper Methods
- `get_data()`: Returns the loaded DataFrame (with validation)
- `get_columns()`: Returns list of column names
- `get_shape()`: Returns (rows, columns) tuple
- `get_info()`: Prints dataset summary

**Usage Example:**
```python
loader = DataLoader(data_path="data/raw")
df = loader.load_csv("WorldHappiness.csv")  # Loads and returns DataFrame
```

---

## 🧹 **Module 2: data_cleaner.py**

### Purpose
Cleans and preprocesses raw data (handles missing values, standardizes names, etc.)

### Class: `DataCleaner`

**Key Concept: Method Chaining**
Many methods return `self`, allowing you to chain operations:
```python
cleaner.standardize_country_names().handle_missing_values().remove_duplicates()
```

**Key Methods:**

#### `standardize_country_names(self)`
```python
self.df['Country'] = self.df['Country'].str.strip().str.title()
```
- **What it does**: 
  - `.strip()` removes leading/trailing spaces
  - `.title()` converts "united states" → "United States"
- **Returns `self`**: Allows method chaining

#### `handle_missing_values(self, strategy='mean')`
```python
if strategy == 'mean':
    self.df[col].fillna(self.df[col].mean(), inplace=True)
```
- **What it does**: Fills missing values using different strategies
- **Strategies**:
  - `'mean'`: Replace with column average
  - `'median'`: Replace with column median
  - `'zero'`: Replace with 0
  - `'drop'`: Remove rows with missing values
- **`inplace=True`**: Modifies DataFrame directly (no need to assign)

#### `clean(self)`
```python
def clean(self) -> pd.DataFrame:
    self.standardize_country_names()
    self.standardize_region_names()
    self.handle_missing_values(strategy='mean')
    self.standardize_year_format()
    self.remove_duplicates()
    self.cleaned_df = self.df.copy()
    return self.cleaned_df
```
- **What it does**: Runs all cleaning steps in sequence
- **Why `.copy()`**: Creates a separate copy so original isn't modified

**Usage Example:**
```python
cleaner = DataCleaner(raw_df)
cleaned_df = cleaner.clean()  # Does all cleaning steps
```

---

## 📊 **Module 3: analyzer.py**

### Purpose
Performs statistical analyses on the cleaned data.

### Class: `Analyzer`

**Key Methods:**

#### `country_comparison(self, top_n=10)`
```python
result = self.df.nlargest(top_n, 'Happiness Score')[
    ['Country', 'Region', 'Happiness Score']
].copy()
```
- **What it does**: 
  - `nlargest()` gets top N rows by 'Happiness Score'
  - Selects only Country, Region, Happiness Score columns
  - Returns sorted DataFrame
- **`.copy()`**: Prevents modifying original DataFrame

#### `regional_average_happiness(self)`
```python
regional_avg = self.df.groupby('Region')['Happiness Score'].agg([
    'mean', 'std', 'count'
]).round(3)
```
- **What it does**:
  - `groupby('Region')`: Groups rows by region
  - `['Happiness Score']`: Selects the column to analyze
  - `.agg(['mean', 'std', 'count'])`: Calculates mean, standard deviation, and count
  - `.round(3)`: Rounds to 3 decimal places
- **Returns**: DataFrame with one row per region

#### `correlation_analysis(self, method='both')`
```python
numeric_cols = self.df.select_dtypes(include=[np.number]).columns
numeric_df = self.df[numeric_cols]
pearson_corr = numeric_df.corr(method='pearson')
```
- **What it does**:
  - `select_dtypes(include=[np.number])`: Gets only numeric columns
  - `.corr()`: Calculates correlation matrix
  - **Pearson**: Linear relationships
  - **Spearman**: Monotonic relationships (handles non-linear)
- **Returns**: Dictionary with correlation matrices

#### `year_over_year_change(self, country, year_column='Year')`
```python
country_data = self.df[self.df['Country'] == country].sort_values(year_column)
scores = country_data['Happiness Score'].values
change = scores[-1] - scores[0]  # Last minus first
```
- **What it does**: 
  - Filters data for one country
  - Sorts by year
  - Calculates change from first to last year
- **`.values`**: Converts pandas Series to numpy array

**Usage Example:**
```python
analyzer = Analyzer(cleaned_df)
top_10 = analyzer.country_comparison(top_n=10)
regional_stats = analyzer.regional_average_happiness()
```

---

## 🔢 **Module 4: index_calculator.py**

### Purpose
Creates a custom composite happiness index from normalized indicators.

### Class: `IndexCalculator`

**Key Concept: Min-Max Normalization**
Converts all indicators to 0-1 scale so they can be combined:
```
normalized_value = (value - min) / (max - min)
```

**Key Methods:**

#### `normalize_min_max(self)`
```python
for indicator in self.indicators:
    col_data = normalized_data[indicator]
    min_val = col_data.min()
    max_val = col_data.max()
    if max_val - min_val > 0:
        normalized_data[f'{indicator}_normalized'] = (
            (col_data - min_val) / (max_val - min_val)
        )
```
- **What it does**:
  1. For each indicator (GDP, Family, Health, etc.)
  2. Finds min and max values
  3. Applies formula: `(value - min) / (max - min)`
  4. Creates new column with `_normalized` suffix
- **Why normalize?**: Different indicators have different scales (GDP might be 0-2, Family 0-2, etc.). Normalization makes them comparable.

#### `calculate_composite_index(self)`
```python
composite_scores = pd.Series(0.0, index=index_data.index)

for indicator in self.indicators:
    normalized_col = f'{indicator}_normalized'
    weight = self.weights.get(indicator, 0)
    composite_scores += index_data[normalized_col] * weight

composite_scores = composite_scores * 10  # Scale to 0-10
```
- **What it does**:
  1. Creates empty Series (array) of zeros
  2. For each indicator, multiplies normalized value by its weight
  3. Sums all weighted indicators
  4. Scales result to 0-10 range (matches happiness score scale)
- **Weights**: Default is equal weights (1/6 each), but can be customized

#### `set_weights(self, weights)`
```python
total_weight = sum(weights.values())
if abs(total_weight - 1.0) > 0.01:
    weights = {k: v / total_weight for k, v in weights.items()}
```
- **What it does**: Sets custom weights for indicators
- **Validation**: Ensures weights sum to 1.0 (normalizes if needed)
- **Example**: `{'GDP': 0.3, 'Family': 0.2, ...}`

**Usage Example:**
```python
index_calc = IndexCalculator(df)
index_calc.set_weights({'GDP': 0.3, 'Family': 0.2, ...})
index_df = index_calc.calculate_composite_index()
```

---

## 📈 **Module 5: visualizer.py**

### Purpose
Creates matplotlib visualizations (charts and graphs).

### Class: `Visualizer`

**Key Methods:**

#### `plot_country_comparison(self, top_n=15)`
```python
top_countries = self.df.nlargest(top_n, 'Happiness Score')
fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(range(len(top_countries)), top_countries['Happiness Score'])
ax.set_yticks(range(len(top_countries)))
ax.set_yticklabels(top_countries['Country'])
ax.invert_yaxis()  # Top country at top
```
- **What it does**:
  - `plt.subplots()`: Creates figure and axes
  - `ax.barh()`: Horizontal bar chart
  - `ax.set_yticks()`: Sets positions for country labels
  - `ax.invert_yaxis()`: Flips so highest is at top
- **`figsize=(12, 8)`**: Width=12 inches, height=8 inches

#### `plot_gdp_vs_happiness(self)`
```python
scatter = ax.scatter(self.df[gdp_col], self.df['Happiness Score'],
                    alpha=0.6, s=100, c=self.df['Happiness Score'],
                    cmap='viridis')
```
- **What it does**: Creates scatter plot
- **Parameters**:
  - `alpha=0.6`: Transparency (0=invisible, 1=opaque)
  - `s=100`: Size of dots
  - `c=...`: Color based on happiness score
  - `cmap='viridis'`: Color scheme

#### `plot_correlation_heatmap(self)`
```python
corr_matrix = self.df[numeric_cols].corr(method=method)
im = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
```
- **What it does**: Shows correlation as colored grid
- **`cmap='coolwarm'`**: Blue=negative, Red=positive correlation
- **`vmin=-1, vmax=1`**: Correlation ranges from -1 to +1

**Usage Example:**
```python
visualizer = Visualizer(df, output_dir="reports")
visualizer.plot_country_comparison(top_n=15, save=True)
```

---

## 💡 **Module 6: insight_engine.py**

### Purpose
Generates rule-based insights (finds patterns in data).

### Class: `InsightEngine`

**Key Concept: Rule-Based Analysis**
Uses if-then rules instead of machine learning:
- "IF GDP > threshold AND Happiness < threshold THEN insight"

**Key Methods:**

#### `find_high_gdp_low_happiness(self)`
```python
high_gdp_low_happiness = self.df[
    (self.df[gdp_col] >= gdp_threshold) & 
    (self.df['Happiness Score'] <= happiness_threshold)
].copy()
```
- **What it does**: Finds countries with high GDP but low happiness
- **Boolean Indexing**: `df[condition]` filters rows where condition is True
- **`&` operator**: AND condition (both must be true)
- **Why useful**: Identifies "paradox" cases (wealthy but unhappy)

#### `identify_stable_vs_volatile(self)`
```python
for country in self.df['Country'].unique():
    country_data = self.df[self.df['Country'] == country]
    std_dev = country_data['Happiness Score'].std()
    if std_dev <= stability_threshold:
        stable_countries.append(country)
```
- **What it does**: 
  - For each country, calculates standard deviation of happiness scores
  - Low std dev = stable (scores don't change much)
  - High std dev = volatile (scores change a lot)
- **`.std()`**: Standard deviation (measure of variation)

#### `find_happiness_outliers(self, method='iqr')`
```python
Q1 = scores.quantile(0.25)  # 25th percentile
Q3 = scores.quantile(0.75)  # 75th percentile
IQR = Q3 - Q1  # Interquartile Range
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = self.df[(scores < lower_bound) | (scores > upper_bound)]
```
- **What it does**: Finds statistical outliers using IQR method
- **IQR Method**: 
  - Anything below `Q1 - 1.5*IQR` or above `Q3 + 1.5*IQR` is an outlier
  - Standard statistical technique
- **`|` operator**: OR condition

**Usage Example:**
```python
insight_engine = InsightEngine(df)
insights = insight_engine.generate_all_insights()  # Runs all methods
insight_engine.print_insights()  # Displays them
```

---

## 🎯 **Module 7: main.py**

### Purpose
Orchestrates the entire workflow.

### Function: `main()`

**Workflow:**
```python
def main():
    # 1. Load Data
    loader = DataLoader(data_path="data/raw")
    df = loader.load_csv("WorldHappiness.csv")
    
    # 2. Clean Data
    cleaner = DataCleaner(df)
    cleaned_df = cleaner.clean()
    
    # 3. Analyze
    analyzer = Analyzer(cleaned_df)
    top_countries = analyzer.country_comparison(top_n=10)
    
    # 4. Calculate Index
    index_calc = IndexCalculator(cleaned_df)
    index_df = index_calc.calculate_composite_index()
    
    # 5. Visualize
    visualizer = Visualizer(cleaned_df)
    visualizer.plot_country_comparison()
    
    # 6. Generate Insights
    insight_engine = InsightEngine(cleaned_df)
    insights = insight_engine.generate_all_insights()
```

**Key Points:**
- **Sequential Processing**: Each step depends on the previous one
- **Error Handling**: Try-except blocks catch and display errors
- **Path Handling**: Uses `os.path.join()` for cross-platform compatibility

---

## 🌐 **Module 8: streamlit_app.py**

### Purpose
Creates interactive web dashboard.

### Key Concepts:

#### `@st.cache_data` Decorator
```python
@st.cache_data
def load_and_clean_data():
    # ... loading code ...
```
- **What it does**: Caches the result so it only runs once
- **Why**: Prevents reloading data every time user interacts (much faster!)

#### Streamlit Widgets
```python
selected_region = st.sidebar.selectbox("Select Region", regions)
top_n = st.slider("Number of countries", 5, 20, 10)
use_custom_weights = st.checkbox("Use custom weights")
```
- **`st.selectbox()`**: Dropdown menu
- **`st.slider()`**: Slider for numeric input
- **`st.checkbox()`**: Checkbox for boolean
- **`st.sidebar.*`**: Puts widget in sidebar

#### Display Functions
```python
st.header("Title")  # Large heading
st.subheader("Subtitle")  # Medium heading
st.metric("Label", value)  # Key metric display
st.dataframe(df)  # Interactive table
st.pyplot(fig)  # Show matplotlib plot
```

#### Page Navigation
```python
page = st.sidebar.radio("Select Page", ["Overview", "Analysis", ...])
if page == "Overview":
    show_overview()
elif page == "Analysis":
    show_analysis()
```
- **`st.radio()`**: Radio buttons for selection
- **Conditional Rendering**: Shows different content based on selection

**Usage:**
```bash
streamlit run streamlit_app.py
```

---

## 🔑 **Key Python Concepts Used**

### 1. **Type Hints**
```python
def method(self, param: str) -> pd.DataFrame:
```
- Tells you what types to expect (helps with IDE autocomplete)

### 2. **Optional Types**
```python
df: Optional[pd.DataFrame] = None
```
- Can be `DataFrame` or `None`

### 3. **Method Chaining**
```python
return self  # Allows: obj.method1().method2()
```

### 4. **List/Dict Comprehensions**
```python
improving = [r for r, change in trends.items() if change > 0.1]
```
- Compact way to filter/create lists

### 5. **Boolean Indexing**
```python
filtered = df[df['Score'] > 5]  # Rows where Score > 5
```

### 6. **String Formatting**
```python
f"Found {count} countries"  # f-strings (Python 3.6+)
```

### 7. **Error Handling**
```python
try:
    # risky code
except ValueError as e:
    # handle error
```

---

## 📝 **Summary: How Everything Works Together**

1. **DataLoader** reads CSV → pandas DataFrame
2. **DataCleaner** fixes missing values, standardizes names
3. **Analyzer** calculates statistics, correlations, comparisons
4. **IndexCalculator** creates custom composite index
5. **Visualizer** creates charts and graphs
6. **InsightEngine** finds patterns and generates insights
7. **main.py** runs everything in sequence
8. **streamlit_app.py** provides interactive web interface

**Data Flow:**
```
CSV → Load → Clean → Analyze → Visualize → Insights
```

Each module is **independent** but **composable** - you can use them separately or together!

---

## 🎓 **Learning Points**

1. **OOP**: Classes encapsulate related functionality
2. **Modularity**: Each file has one responsibility
3. **Reusability**: Methods can be called multiple times
4. **Error Handling**: Code handles edge cases gracefully
5. **Documentation**: Docstrings explain what each function does
6. **Type Safety**: Type hints help catch errors early

This codebase demonstrates **clean, professional Python code** suitable for a semester project! 🎉

