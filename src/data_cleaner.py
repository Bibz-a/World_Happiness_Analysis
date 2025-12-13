import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()
        self.cleaned_df = None

    def standardize_country_names(self):
        if 'Country' in self.df.columns:
            self.df['Country'] = self.df['Country'].str.strip().str.title()
        return self

    def standardize_region_names(self):
        if 'Region' in self.df.columns:
            self.df['Region'] = self.df['Region'].str.strip()
        return self

    def handle_missing_values(self, strategy='mean'):
        cols = self.df.select_dtypes(include=[np.number]).columns
        for col in cols:
            if self.df[col].isnull().any():
                if strategy == 'mean':
                    self.df[col].fillna(self.df[col].mean(), inplace=True)
                elif strategy == 'median':
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                elif strategy == 'zero':
                    self.df[col].fillna(0, inplace=True)
                elif strategy == 'drop':
                    self.df.dropna(subset=[col], inplace=True)
        return self

    def standardize_year_format(self, year_column='Year'):
        if year_column in self.df.columns:
            self.df[year_column] = pd.to_numeric(self.df[year_column], errors='coerce')
        return self

    def remove_duplicates(self):
        self.df = self.df.drop_duplicates()
        return self

    def clean(self):
        self.standardize_country_names()\
            .standardize_region_names()\
            .handle_missing_values()\
            .standardize_year_format()\
            .remove_duplicates()
        self.cleaned_df = self.df.copy()
        return self.cleaned_df

    def get_cleaned_data(self):
        if self.cleaned_df is None:
            raise ValueError("Clean data not available, call .clean() first")
        return self.cleaned_df

    def save_cleaned_data(self, output_path="data/processed/cleaned_data.csv"):
        if self.cleaned_df is None:
            raise ValueError("Clean data not available, call .clean() first")
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.cleaned_df.to_csv(output_path, index=False)
