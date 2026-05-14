import numpy as np
import pandas as pd


class DataCleaner: 
    # append a native Chinese indicator to dataset for variety and fair calculations and to avoid any potential bias in the data
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.df.columns = self.df.columns.str.strip()
        self.df.columns = ['Year', 'GHA_Exports', 'NGA_Exports', 'GHA_EDS', 'GHA_VR', 'NGA_EDS', 'NGA_VR', 'CHN_LPR']
        
        self.df['Year'] = self.df['Year'].astype(str)
        self.numeric_df = self.df.select_dtypes(include=[np.number])
        print("Data loaded successfully.")
        
    def clean_data(self, df):
        self.df = df.copy()
        print(f"Initial Dimensions: {self.df.shape}")


        print("\n--- First 9 Rows ---")
        print(self.df.head(9)) 

        print("\n--- Data Types ---")
        print(self.df.dtypes)

        print(self.df.describe())

        print("\n Column names")
        print(list(self.df)) 

        print("\n Missing values count: ")
        print(self.df.isnull().sum()) 
