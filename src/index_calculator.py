import pandas as pd

class IndexCalculator:
    def __init__(self, df, indicators=None):
        self.df = df.copy()
        if indicators is None:
            self.indicators = [
                'Economy (GDP per Capita)',
                'Family',
                'Health (Life Expectancy)',
                'Freedom',
                'Trust (Government Corruption)',
                'Generosity'
            ]
        else:
            self.indicators = indicators
        n = len(self.indicators)
        self.weights = {ind: 1.0/n for ind in self.indicators}
        self.index_df = None

    def set_weights(self, weights):
        total = sum(weights.values())
        if abs(total - 1.0) > 0.01:
            weights = {k: v / total for k, v in weights.items()}
        self.weights = weights

    def normalize_min_max(self):
        df = self.df.copy()
        for ind in self.indicators:
            if ind in df.columns:
                x = df[ind]
                mn, mx = x.min(), x.max()
                if mx - mn > 0:
                    df[ind + '_normalized'] = (x-mn)/(mx-mn)
                else:
                    df[ind + '_normalized'] = 0.5
        self.index_df = df
        return df

    def calculate_composite_index(self):
        if self.index_df is None:
            self.normalize_min_max()
        df = self.index_df.copy()
        score = 0
        for ind in self.indicators:
            col = ind + '_normalized'
            if col in df.columns:
                score += df[col] * self.weights.get(ind, 0)
        df['Composite_Happiness_Index'] = score * 10
        df['Composite_Rank'] = df['Composite_Happiness_Index'].rank(ascending=False, method='min').astype(int)
        self.index_df = df
        return df

    def compare_with_original(self):
        if self.index_df is None:
            self.calculate_composite_index()
        df = self.index_df
        cols = ['Country', 'Region', 'Happiness Score', 'Composite_Happiness_Index', 'Composite_Rank']
        result = df[cols].copy()
        if 'Happiness Rank' in df.columns:
            result['Original_Rank'] = df['Happiness Rank']
            result['Rank_Difference'] = result['Original_Rank'] - result['Composite_Rank']
        result['Score_Difference'] = result['Composite_Happiness_Index'] - result['Happiness Score']
        return result.sort_values('Composite_Happiness_Index', ascending=False)

    def get_index_statistics(self):
        if self.index_df is None:
            self.calculate_composite_index()
        x = self.index_df['Composite_Happiness_Index']
        return {
            'mean': x.mean(),
            'median': x.median(),
            'std': x.std(),
            'min': x.min(),
            'max': x.max(),
            'q25': x.quantile(0.25),
            'q75': x.quantile(0.75)
        }

    def get_index_data(self):
        if self.index_df is None:
            self.calculate_composite_index()
        return self.index_df
