import pandas as pd
import os

class DataLoader:
    def __init__(self, data_path="data/raw"):
        self.data_path = data_path
        self.df = None

    def load_csv(self, filename="WorldHappiness.csv"):
        path = os.path.join(self.data_path, filename)
        if not os.path.isfile(path):
            print(f"File not found: {path}")
            return None
        try:
            self.df = pd.read_csv(path)
            print(f"Loaded {len(self.df)} rows from {filename}")
            return self.df
        except Exception as e:
            print(f"Failed to read csv: {e}")
            return None

    def get_data(self):
        return self.df

    def get_columns(self):
        if self.df is not None:
            return list(self.df.columns)
        return []

    def get_shape(self):
        if self.df is not None:
            return self.df.shape
        return (0, 0)

    def get_info(self):
        if self.df is None:
            print("No data loaded.")
            return
        print("="*30)
        print(f"Shape: {self.df.shape}")
        print(f"Columns: {list(self.df.columns)}")
        print("Missing values:\n", self.df.isnull().sum())
        print("="*30)
