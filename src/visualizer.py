import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

class Visualizer:
    def __init__(self, df, output_dir="reports"):
        self.df = df.copy()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        plt.style.use('seaborn-v0_8-darkgrid')

    def plot_country_comparison(self, top_n=15, filename="country_comparison.png"):
        if 'Happiness Score' not in self.df.columns: return
        top_countries = self.df.nlargest(top_n, 'Happiness Score')
        plt.barh(top_countries['Country'], top_countries['Happiness Score'], color='steelblue')
        plt.xlabel('Happiness Score')
        plt.title(f'Top {top_n} Countries by Happiness Score')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=200)
        plt.show()

    def plot_region_comparison(self, filename="region_comparison.png"):
        if 'Region' not in self.df.columns or 'Happiness Score' not in self.df.columns: return
        regional_avg = self.df.groupby('Region')['Happiness Score'].mean().sort_values(ascending=False)
        plt.barh(regional_avg.index, regional_avg.values, color='coral')
        plt.xlabel('Average Happiness Score')
        plt.title('Average Happiness Score by Region')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=200)
        plt.show()

    def plot_gdp_vs_happiness(self, filename="gdp_vs_happiness.png"):
        gdp_col = 'Economy (GDP per Capita)'
        if gdp_col not in self.df.columns or 'Happiness Score' not in self.df.columns: return
        x = self.df[gdp_col]
        y = self.df['Happiness Score']
        plt.scatter(x, y, c=y, cmap='viridis', edgecolors='black', alpha=0.6)
        # z = np.polyfit(x, y, 1)
        # plt.plot(x, np.poly1d(z)(x), "r--")
        plt.xlabel('GDP per Capita')
        plt.ylabel('Happiness Score')
        plt.title('GDP vs Happiness Score')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=200)
        plt.show()

    def plot_correlation_heatmap(self, filename="correlation_heatmap.png"):
        num = self.df.select_dtypes(include=[np.number])
        corr = num.corr()
        plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
        plt.colorbar()
        plt.xticks(range(len(corr)), corr.columns, rotation=45, ha='right')
        plt.yticks(range(len(corr)), corr.columns)
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=200)
        plt.show()

    def plot_top_bottom_comparison(self, top_n=10, bottom_n=10, filename="top_bottom_comparison.png"):
        if 'Happiness Score' not in self.df.columns: return
        top = self.df.nlargest(top_n, 'Happiness Score')
        bottom = self.df.nsmallest(bottom_n, 'Happiness Score')
        fig, axes = plt.subplots(1,2,figsize=(12,6))
        axes[0].barh(top['Country'], top['Happiness Score'], color='green')
        axes[0].set_title(f"Top {top_n}")
        axes[0].invert_yaxis()
        axes[1].barh(bottom['Country'], bottom['Happiness Score'], color='red')
        axes[1].set_title(f"Bottom {bottom_n}")
        axes[1].invert_yaxis()
        plt.suptitle('Top vs Bottom Countries by Happiness Score')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=200)
        plt.show()
