import pandas as pd
import numpy as np

class InsightEngine:
    def __init__(self, df):
        self.df = df.copy()
        self.insights = []

    def find_high_gdp_low_happiness(self, gdp_threshold=1.0, happiness_threshold=5.0):
        if 'Economy (GDP per Capita)' not in self.df or 'Happiness Score' not in self.df:
            return pd.DataFrame()
        sel = self.df[
            (self.df['Economy (GDP per Capita)'] >= gdp_threshold) &
            (self.df['Happiness Score'] <= happiness_threshold)
        ]
        if len(sel) > 0:
            text = f"High GDP (≥{gdp_threshold}) but Low Happiness (≤{happiness_threshold}): {', '.join(sel['Country'].head(5))}"
        else:
            text = f"No countries with GDP ≥{gdp_threshold} & Happiness ≤{happiness_threshold}."
        self.insights.append(text)
        return sel

    def analyze_regional_trends(self, year_column='Year'):
        if year_column not in self.df or 'Region' not in self.df or 'Happiness Score' not in self.df:
            return {'improving': [], 'declining': []}
        improving, declining = [], []
        for reg in self.df['Region'].unique():
            d = self.df[self.df['Region'] == reg].sort_values(year_column)
            if len(d) > 1:
                diff = d.iloc[-1]['Happiness Score'] - d.iloc[0]['Happiness Score']
                if diff > 0.1:
                    improving.append(reg)
                elif diff < -0.1:
                    declining.append(reg)
        if improving:
            self.insights.append(f"Regions improving: {', '.join(improving)}")
        if declining:
            self.insights.append(f"Regions declining: {', '.join(declining)}")
        return {'improving': improving, 'declining': declining}

    def identify_stable_vs_volatile(self, year_column='Year', stability_threshold=0.2):
        if year_column not in self.df or 'Country' not in self.df or 'Happiness Score' not in self.df:
            return {'stable': [], 'volatile': []}
        stable, volatile = [], []
        for c in self.df['Country'].unique():
            d = self.df[self.df['Country'] == c].sort_values(year_column)
            if len(d) > 1:
                std = d['Happiness Score'].std()
                if std <= stability_threshold:
                    stable.append(c)
                elif std >= stability_threshold * 2:
                    volatile.append(c)
        if stable:
            self.insights.append(f"Stable happiness (std ≤ {stability_threshold}): {', '.join(stable[:5])}")
        if volatile:
            self.insights.append(f"Volatile happiness (std ≥ {stability_threshold*2}): {', '.join(volatile[:5])}")
        return {'stable': stable, 'volatile': volatile}

    def find_happiness_outliers(self, method='iqr'):
        if 'Happiness Score' not in self.df:
            return pd.DataFrame()
        s = self.df['Happiness Score']
        if method == 'iqr':
            Q1, Q3 = s.quantile(0.25), s.quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.df[(s < Q1-1.5*IQR) | (s > Q3+1.5*IQR)]
        else:
            z = np.abs((s - s.mean())/s.std())
            outliers = self.df[z > 2]
        if len(outliers) > 0:
            self.insights.append(f"Happiness outliers: {', '.join(outliers['Country'].head(5))}")
        return outliers

    def analyze_freedom_happiness_correlation(self):
        if 'Freedom' not in self.df or 'Happiness Score' not in self.df:
            return {}
        corr = self.df['Freedom'].corr(self.df['Happiness Score'])
        if corr > 0.7:
            msg = f"Strong positive Freedom-Happiness correlation ({corr:.2f})"
        elif corr > 0.4:
            msg = f"Moderate positive Freedom-Happiness correlation ({corr:.2f})"
        else:
            msg = f"Weak Freedom-Happiness correlation ({corr:.2f})"
        self.insights.append(msg)
        return {'correlation': corr}

    def find_high_generosity_low_happiness(self, generosity_threshold=0.3, happiness_threshold=5.0):
        if 'Generosity' not in self.df or 'Happiness Score' not in self.df:
            return pd.DataFrame()
        sel = self.df[
            (self.df['Generosity'] >= generosity_threshold) &
            (self.df['Happiness Score'] <= happiness_threshold)
        ]
        if len(sel) > 0:
            self.insights.append(
                f"High generosity (≥{generosity_threshold}) & low happiness (≤{happiness_threshold}): {', '.join(sel['Country'].head(5))}"
            )
        return sel

    def generate_all_insights(self):
        self.insights = []
        self.find_high_gdp_low_happiness()
        # Removed analyze_regional_trends() - not needed in insights
        self.identify_stable_vs_volatile()
        self.find_happiness_outliers()
        self.analyze_freedom_happiness_correlation()
        self.find_high_generosity_low_happiness()
        return self.insights

    def print_insights(self):
        print("\n=== DATA-DRIVEN INSIGHTS ===")
        if not self.insights:
            print("No insights generated.")
            return
        for i, t in enumerate(self.insights, 1):
            print(f"\n{i}. {t}")
        print("="*30)

    def save_insights(self, filename="reports/insights.txt"):
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            for i, t in enumerate(self.insights, 1):
                f.write(f"{i}. {t}\n")
        print(f"Insights saved to {filename}")
