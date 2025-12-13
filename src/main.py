"""
Main Program

This is the main entry point for the World Happiness Report Dashboard.
It orchestrates the complete workflow: loading, cleaning, analysis, visualization, and insights.
"""

import sys
import os
import pandas as pd

# Get the project root directory (parent of src)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add src directory to path for imports
src_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, src_dir)

from data_loader import DataLoader
from data_cleaner import DataCleaner
from analyzer import Analyzer
from index_calculator import IndexCalculator
from visualizer import Visualizer
from insight_engine import InsightEngine


def main():
    """
    Main function that orchestrates the complete data analytics workflow.
    """
    print("="*70)
    print("WORLD HAPPINESS REPORT DASHBOARD")
    print("="*70)
    print("\nStarting data analytics pipeline...\n")
    
    try:
        # Step 1: Load Data
        print("STEP 1: Loading Data")
        print("-" * 70)
        # Use absolute path relative to project root
        data_path = os.path.join(project_root, "data", "raw")
        loader = DataLoader(data_path=data_path)
        df = loader.load_csv("WorldHappiness.csv")
        loader.get_info()
        
        # Step 2: Clean and Preprocess Data
        print("\nSTEP 2: Cleaning and Preprocessing Data")
        print("-" * 70)
        cleaner = DataCleaner(df)
        cleaned_df = cleaner.clean()
        validation_report = cleaner.validate_data()
        print(f"\nValidation Report:")
        print(f"  Total rows: {validation_report['total_rows']}")
        print(f"  Total columns: {validation_report['total_columns']}")
        print(f"  Missing values: {sum(validation_report['missing_values'].values())}")
        
        # Save cleaned data
        processed_path = os.path.join(project_root, "data", "processed", "cleaned_data.csv")
        cleaner.save_cleaned_data(processed_path)
        
        # Step 3: Perform Analysis
        print("\nSTEP 3: Performing Analysis")
        print("-" * 70)
        analyzer = Analyzer(cleaned_df)
        
        # Country comparison
        print("\nTop 10 Countries by Happiness Score:")
        top_countries = analyzer.country_comparison(top_n=10)
        print(top_countries.to_string(index=False))
        
        # Regional analysis
        print("\nAverage Happiness by Region:")
        regional_avg = analyzer.regional_average_happiness()
        print(regional_avg.to_string())
        
        # Top and bottom countries
        top_bottom = analyzer.top_bottom_countries(top_n=5, bottom_n=5)
        print("\nTop 5 Countries:")
        print(top_bottom['top'].to_string(index=False))
        print("\nBottom 5 Countries:")
        print(top_bottom['bottom'].to_string(index=False))
        
        # Correlation analysis
        print("\nCorrelation Analysis (Pearson):")
        correlations = analyzer.correlation_analysis(method='pearson')
        if 'pearson' in correlations:
            print("\nKey Correlations with Happiness Score:")
            happiness_corr = correlations['pearson']['Happiness Score'].sort_values(ascending=False)
            for col, corr in happiness_corr.items():
                if col != 'Happiness Score' and not pd.isna(corr):
                    print(f"  {col}: {corr:.3f}")
        
        # Step 4: Calculate Composite Happiness Index
        print("\nSTEP 4: Calculating Composite Happiness Index")
        print("-" * 70)
        index_calc = IndexCalculator(cleaned_df)
        index_df = index_calc.calculate_composite_index()
        
        # Compare with original
        comparison = index_calc.compare_with_original()
        print("\nTop 10 Countries by Composite Index:")
        print(comparison.head(10)[['Country', 'Happiness Score', 
                                   'Composite_Happiness_Index', 'Composite_Rank']].to_string(index=False))
        
        index_stats = index_calc.get_index_statistics()
        print(f"\nComposite Index Statistics:")
        print(f"  Mean: {index_stats['mean']:.3f}")
        print(f"  Median: {index_stats['median']:.3f}")
        print(f"  Std Dev: {index_stats['std']:.3f}")
        
        # Step 5: Generate Visualizations
        print("\nSTEP 5: Generating Visualizations")
        print("-" * 70)
        reports_dir = os.path.join(project_root, "reports")
        visualizer = Visualizer(cleaned_df, output_dir=reports_dir)
        
        # Generate all visualizations
        print("\nGenerating country comparison chart...")
        visualizer.plot_country_comparison(top_n=15, save=True)
        
        print("\nGenerating region comparison chart...")
        visualizer.plot_region_comparison(save=True)
        
        print("\nGenerating GDP vs Happiness scatter plot...")
        visualizer.plot_gdp_vs_happiness(save=True)
        
        print("\nGenerating correlation heatmap...")
        visualizer.plot_correlation_heatmap(method='pearson', save=True)
        
        print("\nGenerating top vs bottom comparison...")
        visualizer.plot_top_bottom_comparison(top_n=10, bottom_n=10, save=True)
        
        # Step 6: Generate Insights
        print("\nSTEP 6: Generating Rule-Based Insights")
        print("-" * 70)
        insight_engine = InsightEngine(cleaned_df)
        insights = insight_engine.generate_all_insights()
        insight_engine.print_insights()
        insights_path = os.path.join(project_root, "reports", "insights.txt")
        insight_engine.save_insights(insights_path)
        
        # Step 7: Summary
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE!")
        print("="*70)
        print("\nGenerated Outputs:")
        print("  ✓ Cleaned data: data/processed/cleaned_data.csv")
        print("  ✓ Visualizations: reports/*.png")
        print("  ✓ Insights: reports/insights.txt")
        print("\n" + "="*70)
        
    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        print(f"Please ensure the WorldHappiness.csv file is in the {os.path.join(project_root, 'data', 'raw')} directory.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

