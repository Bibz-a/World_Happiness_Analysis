"""
Streamlit Interactive Dashboard

Interactive web application for the World Happiness Report Dashboard.
Provides a user-friendly GUI to explore and analyze happiness data.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Try to import seaborn, fallback to matplotlib if not available
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# Get the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Add src directory to path for imports
src_dir = os.path.join(project_root, "src")
sys.path.insert(0, src_dir)

from data_loader import DataLoader
from data_cleaner import DataCleaner
from analyzer import Analyzer
from index_calculator import IndexCalculator
from visualizer import Visualizer
from insight_engine import InsightEngine

# Basic theme - just use Streamlit defaults
PRIMARY_COLOR = "#0066cc"
ACCENT_COLOR = "#0066cc"
TEXT_COLOR = "#000000"

st.set_page_config(
    page_title="World Happiness Dashboard",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def load_and_clean_data():
    """
    Load and clean data with caching for performance.
    """
    try:
        data_path = os.path.join(project_root, "data", "raw")
        loader = DataLoader(data_path=data_path)
        df = loader.load_csv("WorldHappiness.csv")
        
        cleaner = DataCleaner(df)
        cleaned_df = cleaner.clean()
        
        return cleaned_df, None
    except Exception as e:
        return None, str(e)


def main():
    """
    Main Streamlit application function.
    """
    # Header
    st.title("🌍 World Happiness Report Dashboard")
    
    # Load data
    with st.spinner("Loading and processing data..."):
        df, error = load_and_clean_data()
    
    if error:
        st.error(f"Error loading data: {error}")
        st.info("Please ensure WorldHappiness.csv is in the data/raw directory.")
        return
    
    if df is None or df.empty:
        st.error("No data available. Please check your data file.")
        return
    
    # Sidebar for navigation and filters
    st.sidebar.markdown("### 📊 Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["🏠 Overview", "📈 Country Analysis", "🌎 Regional Analysis", 
         "📊 Correlation Analysis", "🔍 Composite Index", "💡 Insights", "🔬 Data Explorer"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Filters")
    
    # Region filter
    regions = ['All'] + sorted(df['Region'].unique().tolist())
    selected_region = st.sidebar.selectbox("Select Region", regions)
    
    # Filter data based on region
    filtered_df = df if selected_region == 'All' else df[df['Region'] == selected_region]
    
    # Country selector
    countries = sorted(filtered_df['Country'].unique().tolist())
    selected_country = st.sidebar.selectbox("Select Country (for detailed view)", 
                                           ['None'] + countries)
    
    # Display selected page
    if page == "🏠 Overview":
        show_overview(filtered_df, df)
    elif page == "📈 Country Analysis":
        show_country_analysis(filtered_df, selected_country)
    elif page == "🌎 Regional Analysis":
        show_regional_analysis(df)
    elif page == "📊 Correlation Analysis":
        show_correlation_analysis(df)
    elif page == "🔍 Composite Index":
        show_composite_index(df)
    elif page == "💡 Insights":
        show_insights(df)
    elif page == "🔬 Data Explorer":
        show_data_explorer(filtered_df)


def show_overview(filtered_df, full_df):
    """
    Display overview dashboard with key metrics and visualizations.
    """
    st.header("📊 Dashboard Overview")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_happiness = filtered_df['Happiness Score'].mean()
        st.metric("Average Happiness", f"{avg_happiness:.2f}")
    with col2:
        total_countries = len(filtered_df)
        st.metric("Total Countries", total_countries)
    with col3:
        max_happiness = filtered_df['Happiness Score'].max()
        st.metric("Highest Score", f"{max_happiness:.2f}")
    with col4:
        min_happiness = filtered_df['Happiness Score'].min()
        st.metric("Lowest Score", f"{min_happiness:.2f}")

    st.markdown("")

    # Top Countries Chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 10 Countries")
        top_n = st.slider("Number of countries", 5, 20, 10, key="top_n")
        top_countries = filtered_df.nlargest(top_n, 'Happiness Score')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(
            range(len(top_countries)), top_countries['Happiness Score'], 
            color=ACCENT_COLOR, alpha=0.75,
            edgecolor=PRIMARY_COLOR, linewidth=2
        )
        ax.set_yticks(range(len(top_countries)))
        ax.set_yticklabels(top_countries['Country'], fontsize=11)
        ax.set_xlabel('Happiness Score', fontweight='bold', color=TEXT_COLOR)
        ax.set_title(f'Top {top_n} Countries by Happiness Score', fontweight='bold', color=TEXT_COLOR)
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("📉 Bottom 10 Countries")
        bottom_n = st.slider("Number of countries", 5, 20, 10, key="bottom_n")
        bottom_countries = filtered_df.nsmallest(bottom_n, 'Happiness Score')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(
            range(len(bottom_countries)), bottom_countries['Happiness Score'], 
            color=PRIMARY_COLOR, alpha=0.69,
            edgecolor=ACCENT_COLOR, linewidth=2
        )
        ax.set_yticks(range(len(bottom_countries)))
        ax.set_yticklabels(bottom_countries['Country'], fontsize=11)
        ax.set_xlabel('Happiness Score', fontweight='bold', color=TEXT_COLOR)
        ax.set_title(f'Bottom {bottom_n} Countries by Happiness Score', fontweight='bold', color=TEXT_COLOR)
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    # GDP vs Happiness
    st.markdown("---")
    st.subheader("💰 GDP per Capita vs Happiness Score")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    scatter = ax.scatter(
        filtered_df['Economy (GDP per Capita)'], 
        filtered_df['Happiness Score'],
        alpha=0.7, s=120, 
        c=filtered_df['Happiness Score'],
        cmap='mako' if HAS_SEABORN else 'plasma', 
        edgecolors=ACCENT_COLOR, linewidth=1.1
    )
    ax.set_xlabel('GDP per Capita', fontweight='bold', color=TEXT_COLOR)
    ax.set_ylabel('Happiness Score', fontweight='bold', color=TEXT_COLOR)
    ax.set_title('GDP per Capita vs Happiness Score', fontweight='bold', color=TEXT_COLOR)
    cbar = plt.colorbar(scatter, ax=ax, label='Happiness Score')
    cbar.ax.tick_params(labelsize=10)
    ax.grid(True, alpha=0.23)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


def show_country_analysis(filtered_df, selected_country):
    """
    Display detailed country analysis.
    """
    st.header("📈 Country Analysis")
    
    if selected_country and selected_country != 'None':
        # Single country detailed view
        country_data = filtered_df[filtered_df['Country'] == selected_country]
        
        if not country_data.empty:
            st.subheader(f"🇺🇳 {selected_country}")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Happiness Score", 
                         f"{country_data['Happiness Score'].values[0]:.2f}")
            with col2:
                st.metric("GDP per Capita", 
                         f"{country_data['Economy (GDP per Capita)'].values[0]:.2f}")
            with col3:
                st.metric("Life Expectancy", 
                         f"{country_data['Health (Life Expectancy)'].values[0]:.2f}")
            with col4:
                st.metric("Freedom", 
                         f"{country_data['Freedom'].values[0]:.2f}")

            # Prettier radar or bar chart (keep bar for simplicity, but with accent color)
            st.markdown("---")
            st.subheader("📊 Indicators Breakdown")
            
            indicators = {
                'Economy (GDP per Capita)': country_data['Economy (GDP per Capita)'].values[0],
                'Family': country_data['Family'].values[0],
                'Health (Life Expectancy)': country_data['Health (Life Expectancy)'].values[0],
                'Freedom': country_data['Freedom'].values[0],
                'Trust (Government Corruption)': country_data['Trust (Government Corruption)'].values[0],
                'Generosity': country_data['Generosity'].values[0]
            }
            
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = [PRIMARY_COLOR, ACCENT_COLOR, "#54d1db", "#9d7ef7", "#fab1ce", "#dbb953"]
            ax.barh(
                range(len(indicators)), list(indicators.values()), 
                color=colors[:len(indicators)], alpha=0.84, edgecolor="#222", linewidth=1.2
            )
            ax.set_yticks(range(len(indicators)))
            ax.set_yticklabels(list(indicators.keys()), fontsize=12)
            ax.set_xlabel('Score', fontweight='bold', color=TEXT_COLOR)
            ax.set_title(f'{selected_country} - Happiness Indicators', fontweight='bold', color=TEXT_COLOR)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
    
    # Country comparison table
    st.markdown("---")
    st.subheader("📋 Country Comparison Table")
    
    analyzer = Analyzer(filtered_df)
    top_n = st.slider("Show top N countries", 5, 50, 20, key="country_table")
    top_countries = analyzer.country_comparison(top_n=top_n)
    
    display_cols = ['Country', 'Region', 'Happiness Score', 
                   'Economy (GDP per Capita)', 'Health (Life Expectancy)', 
                   'Freedom', 'Generosity']
    available_cols = [col for col in display_cols if col in filtered_df.columns]
    
    display_df = filtered_df.nlargest(top_n, 'Happiness Score')[available_cols]
    st.dataframe(display_df, use_container_width=True, height=430)


def show_regional_analysis(df):
    """
    Display regional analysis.
    """
    st.header("🌎 Regional Analysis")
    
    analyzer = Analyzer(df)
    regional_avg = analyzer.regional_average_happiness()
    
    # Regional comparison chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Average Happiness by Region")
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(
            range(len(regional_avg)), regional_avg['Average Happiness'], 
            color=[ACCENT_COLOR if i%2==0 else PRIMARY_COLOR for i in range(len(regional_avg))], 
            alpha=0.85, edgecolor="#fff", linewidth=2.0
        )
        ax.set_yticks(range(len(regional_avg)))
        ax.set_yticklabels(regional_avg.index, fontsize=12)
        ax.set_xlabel('Average Happiness Score', fontweight='bold', color=TEXT_COLOR)
        ax.set_title('Average Happiness Score by Region', fontweight='bold', color=TEXT_COLOR)
        ax.invert_yaxis()
        
        # Add value labels
        for i, val in enumerate(regional_avg['Average Happiness']):
            ax.text(val + 0.05, i, f"{val:.2f}", va='center', fontsize=11, color=TEXT_COLOR, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("📈 Regional Statistics")
        st.dataframe(regional_avg, use_container_width=True)
    
    # Regional distribution
    st.markdown("---")
    st.subheader("📉 Happiness Distribution by Region")
    
    selected_regions = st.multiselect(
        "Select regions to compare",
        df['Region'].unique().tolist(),
        default=df['Region'].unique().tolist()[:5]
    )
    
    if selected_regions:
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = [
            "#2e86ab", "#f6ab6c", "#7fd1b9", "#be7be7", "#fd4c86", "#f9c846", "#4d9de0"
        ]
        for i, region in enumerate(selected_regions):
            region_data = df[df['Region'] == region]['Happiness Score']
            ax.hist(region_data, alpha=0.60, label=region, bins=15, color=colors[i%len(colors)])
        ax.set_xlabel('Happiness Score', fontweight='bold', color=TEXT_COLOR)
        ax.set_ylabel('Frequency', fontweight='bold', color=TEXT_COLOR)
        ax.set_title('Happiness Score Distribution by Region', fontweight='bold', color=TEXT_COLOR)
        ax.legend()
        ax.grid(True, alpha=0.21)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()


def show_correlation_analysis(df):
    """
    Display correlation analysis.
    """
    st.header("📊 Correlation Analysis")
    
    analyzer = Analyzer(df)
    correlations = analyzer.correlation_analysis(method='both')
    
    # Correlation method selector
    method = st.radio("Correlation Method", ['Pearson', 'Spearman'], horizontal=True)
    corr_key = method.lower()
    
    if corr_key in correlations:
        corr_matrix = correlations[corr_key]
        
        # Heatmap
        st.subheader(f"{method} Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(12, 10))
        
        if HAS_SEABORN:
            sns.heatmap(
                corr_matrix, annot=True, fmt='.2f', 
                cmap='Spectral', center=0, square=True, linewidths=1.75, 
                cbar_kws={"shrink": 0.8}, ax=ax,
                annot_kws={"fontsize":11,"fontweight":"bold","color":TEXT_COLOR}
            )
        else:
            im = ax.imshow(corr_matrix, cmap='Spectral', aspect='auto', vmin=-1, vmax=1)
            ax.set_xticks(range(len(corr_matrix.columns)))
            ax.set_yticks(range(len(corr_matrix.columns)))
            ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right', fontsize=11)
            ax.set_yticklabels(corr_matrix.columns, fontsize=11)
            for i in range(len(corr_matrix.columns)):
                for j in range(len(corr_matrix.columns)):
                    text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                 ha="center", va="center", color=TEXT_COLOR, fontsize=9)
            plt.colorbar(im, ax=ax, label='Correlation Coefficient')
        
        ax.set_title(f'{method} Correlation Matrix', fontweight='bold', pad=20, color=TEXT_COLOR)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Top correlations with Happiness Score
        st.markdown("---")
        st.subheader("🔗 Correlations with Happiness Score")
        
        if 'Happiness Score' in corr_matrix.columns:
            happiness_corr = corr_matrix['Happiness Score'].sort_values(ascending=False)
            happiness_corr = happiness_corr[happiness_corr.index != 'Happiness Score']
            happiness_corr = happiness_corr.dropna()
            
            fig, ax = plt.subplots(figsize=(10, 7))
            barcolors = [PRIMARY_COLOR if x > 0 else ACCENT_COLOR for x in happiness_corr.values]
            ax.barh(range(len(happiness_corr)), happiness_corr.values, color=barcolors, alpha=0.85, edgecolor=PRIMARY_COLOR, linewidth=1.25)
            ax.set_yticks(range(len(happiness_corr)))
            ax.set_yticklabels(happiness_corr.index, fontsize=12)
            ax.set_xlabel('Correlation Coefficient', fontweight='bold', color=TEXT_COLOR)
            ax.set_title(f'{method} Correlation with Happiness Score', fontweight='bold', color=TEXT_COLOR)
            ax.axvline(x=0, color='#bdbdbd', linestyle='--', linewidth=1.3)
            ax.grid(True, alpha=0.17, axis='x')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            
            # Correlation table
            st.dataframe(
                happiness_corr.to_frame('Correlation'),
                use_container_width=True
            )


def show_composite_index(df):
    """
    Display composite happiness index analysis.
    """
    st.header("🔍 Composite Happiness Index")
    
    st.markdown("""
    <div style="background-color: #e7f3ff; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #2196F3; margin: 1rem 0;">
    ℹ️ The Composite Happiness Index is calculated using <b style="color:#5390d9">Min-Max normalization</b> of key indicators:<br>
    <b>Economy</b>, <b>Family</b>, <b>Health</b>, <b>Freedom</b>, <b>Trust</b>, and <b>Generosity</b>.
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate index
    index_calc = IndexCalculator(df)
    
    # Custom weights option
    st.subheader("⚙️ Index Configuration")
    use_custom_weights = st.checkbox("Use custom weights")
    
    if use_custom_weights:
        st.write("Set weights for each indicator (must sum to 1.0):")
        col1, col2 = st.columns(2)
        
        weights = {}
        with col1:
            weights['Economy (GDP per Capita)'] = st.slider("GDP Weight", 0.0, 1.0, 0.2, 0.05)
            weights['Family'] = st.slider("Family Weight", 0.0, 1.0, 0.15, 0.05)
            weights['Health (Life Expectancy)'] = st.slider("Health Weight", 0.0, 1.0, 0.2, 0.05)
        
        with col2:
            weights['Freedom'] = st.slider("Freedom Weight", 0.0, 1.0, 0.15, 0.05)
            weights['Trust (Government Corruption)'] = st.slider("Trust Weight", 0.0, 1.0, 0.15, 0.05)
            weights['Generosity'] = st.slider("Generosity Weight", 0.0, 1.0, 0.15, 0.05)
        
        total_weight = sum(weights.values())
        if abs(total_weight - 1.0) > 0.01:
            st.warning(f"⚠️ Weights sum to {total_weight:.2f}. Normalizing to 1.0")
            weights = {k: v / total_weight for k, v in weights.items()}
        
        index_calc.set_weights(weights)
    
    # Calculate and display
    index_df = index_calc.calculate_composite_index()
    comparison = index_calc.compare_with_original()
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    stats = index_calc.get_index_statistics()
    
    with col1:
        st.metric("Mean Index", f"{stats['mean']:.2f}")
    with col2:
        st.metric("Median Index", f"{stats['median']:.2f}")
    with col3:
        st.metric("Std Deviation", f"{stats['std']:.2f}")
    with col4:
        st.metric("Range", f"{stats['min']:.2f} - {stats['max']:.2f}")
    
    # Comparison chart
    st.markdown("---")
    st.subheader("📊 Original vs Composite Index")
    
    top_n = st.slider("Show top N countries", 10, 30, 15, key="index_top")
    top_comparison = comparison.head(top_n)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    x = np.arange(len(top_comparison))
    width = 0.35
    
    ax.bar(x - width/2, top_comparison['Happiness Score'], width, 
          label='Original Score', alpha=0.69, color=PRIMARY_COLOR, edgecolor=ACCENT_COLOR, linewidth=2)
    ax.bar(x + width/2, top_comparison['Composite_Happiness_Index'], width, 
          label='Composite Index', alpha=0.7, color=ACCENT_COLOR, edgecolor=PRIMARY_COLOR, linewidth=2)
    
    ax.set_xlabel('Country', fontweight='bold', color=TEXT_COLOR)
    ax.set_ylabel('Score', fontweight='bold', color=TEXT_COLOR)
    ax.set_title('Original Happiness Score vs Composite Index (Top Countries)', 
                fontweight='bold', color=TEXT_COLOR)
    ax.set_xticks(x)
    ax.set_xticklabels(top_comparison['Country'], rotation=45, ha='right', fontsize=10)
    ax.legend()
    ax.grid(True, alpha=0.21, axis='y')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Comparison table
    st.markdown("---")
    st.subheader("📋 Detailed Comparison")
    display_cols = ['Country', 'Region', 'Happiness Score', 
                    'Composite_Happiness_Index', 'Composite_Rank']
    if 'Happiness Rank' in comparison.columns:
        display_cols.insert(3, 'Happiness Rank')
    if 'Rank_Difference' in comparison.columns:
        display_cols.append('Rank_Difference')
    
    st.dataframe(comparison[display_cols], use_container_width=True, height=430)


def show_insights(df):
    """
    Display rule-based insights.
    """
    st.header("💡 Data-Driven Insights")

    insight_engine = InsightEngine(df)
    
    # Generate insights
    if st.button("🔄 Generate Insights", type="primary"):
        with st.spinner("Analyzing data and generating insights..."):
            insights = insight_engine.generate_all_insights()
        
        st.markdown("---")
        
        for i, insight in enumerate(insights, 1):
            st.info(f"**Insight {i}:** {insight}")
        
        # Additional visualizations for insights
        st.markdown("---")
        st.subheader("📊 Insight Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**High GDP, Low Happiness Countries**")
            high_gdp_low_hap = insight_engine.find_high_gdp_low_happiness()
            if not high_gdp_low_hap.empty:
                st.dataframe(high_gdp_low_hap[['Country', 'Region', 
                                               'Economy (GDP per Capita)', 
                                               'Happiness Score']], 
                           use_container_width=True)
            else:
                st.write("No countries found matching this criteria.")
        
        with col2:
            st.write("**Happiness Outliers**")
            outliers = insight_engine.find_happiness_outliers()
            if not outliers.empty:
                st.dataframe(outliers[['Country', 'Region', 'Happiness Score']], 
                           use_container_width=True)
            else:
                st.write("No significant outliers found.")
        


def show_data_explorer(df):
    """
    Display interactive data explorer.
    """
    st.header("🔬 Data Explorer")
    
    st.subheader("📋 Raw Data Table")
    
    # Column selector
    all_columns = df.columns.tolist()
    selected_columns = st.multiselect(
        "Select columns to display",
        all_columns,
        default=['Country', 'Region', 'Happiness Score', 'Happiness Rank']
    )
    
    if selected_columns:
        # Search/filter
        search_term = st.text_input("🔍 Search countries", "")
        
        display_df = df[selected_columns].copy()
        
        if search_term:
            display_df = display_df[
                display_df['Country'].str.contains(search_term, case=False, na=False)
            ]
        
        # Sort options
        if 'Happiness Score' in selected_columns:
            sort_by = st.selectbox("Sort by", 
                                  ['Happiness Score (High to Low)', 
                                   'Happiness Score (Low to High)',
                                   'Country (A-Z)'])
            
            if 'High to Low' in sort_by:
                display_df = display_df.sort_values('Happiness Score', ascending=False)
            elif 'Low to High' in sort_by:
                display_df = display_df.sort_values('Happiness Score', ascending=True)
            else:
                display_df = display_df.sort_values('Country')
        
        st.dataframe(display_df, use_container_width=True, height=520)
        
        # Download button
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download filtered data as CSV",
            data=csv,
            file_name="filtered_happiness_data.csv",
            mime="text/csv"
        )
    
    # Summary statistics
    st.markdown("---")
    st.subheader("📊 Summary Statistics")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    selected_stat_cols = st.multiselect(
        "Select columns for statistics",
        numeric_cols,
        default=numeric_cols[:5]
    )
    
    if selected_stat_cols:
        st.dataframe(df[selected_stat_cols].describe(), use_container_width=True)


if __name__ == "__main__":
    main()

