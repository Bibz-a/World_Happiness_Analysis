"""
Simple Analyzer for World Happiness Data

Simple class to analyze the happiness dataset.
Each method does a specific, common analysis task.
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr

class Analyzer:
    def __init__(self, df: pd.DataFrame):
        # Copy the original DataFrame to avoid changes outside
        self.df = df.copy()

    def get_top_countries(self, n=10):
        # Get the top n countries by happiness score
        return self.df.nlargest(n, 'Happiness Score')[['Country', 'Region', 'Happiness Score']]

    def get_bottom_countries(self, n=10):
        # Get the bottom n countries by happiness score
        return self.df.nsmallest(n, 'Happiness Score')[['Country', 'Region', 'Happiness Score']]

    def country_comparison(self, top_n=10):
        # Get the top n countries by happiness score for comparison
        return self.df.nlargest(top_n, 'Happiness Score')[['Country', 'Region', 'Happiness Score']].copy()

    def top_bottom_countries(self, top_n=5, bottom_n=5):
        # Get top and bottom countries
        top = self.df.nlargest(top_n, 'Happiness Score')[['Country', 'Region', 'Happiness Score']].copy()
        bottom = self.df.nsmallest(bottom_n, 'Happiness Score')[['Country', 'Region', 'Happiness Score']].copy()
        return {'top': top, 'bottom': bottom}

    def average_happiness_by_region(self):
        # Calculate mean happiness per region
        if 'Region' not in self.df.columns:
            raise ValueError("'Region' column missing")
        return self.df.groupby('Region')['Happiness Score'].mean().sort_values(ascending=False)

    def regional_average_happiness(self):
        # Calculate regional statistics including mean, std, and count
        if 'Region' not in self.df.columns:
            raise ValueError("'Region' column missing")
        regional_avg = self.df.groupby('Region')['Happiness Score'].agg(['mean', 'std', 'count']).round(3)
        regional_avg.columns = ['Average Happiness', 'Std Dev', 'Count']
        return regional_avg.sort_values('Average Happiness', ascending=False)

    def correlation_matrix(self):
        # Return Pearson correlation matrix for numeric columns
        return self.df.corr()

    def correlation_analysis(self, method='both'):
        # Return correlation matrices for numeric columns
        # method can be 'pearson', 'spearman', or 'both'
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        numeric_df = self.df[numeric_cols]
        
        result = {}
        
        if method in ['pearson', 'both']:
            result['pearson'] = numeric_df.corr(method='pearson')
        
        if method in ['spearman', 'both']:
            result['spearman'] = numeric_df.corr(method='spearman')
        
        return result

    def correlation_with_happiness(self, column):
        # Pearson and Spearman correlation between a column and happiness score
        data = self.df[[column, 'Happiness Score']].dropna()
        if len(data) < 2:
            return None
        pearson, _ = pearsonr(data[column], data['Happiness Score'])
        spearman, _ = spearmanr(data[column], data['Happiness Score'])
        return {'pearson': pearson, 'spearman': spearman}

    def summary_stats(self):
        # Get summary stats for all numeric columns
        return self.df.describe()

