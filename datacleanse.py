import numpy as np
import pandas as pd


class DataCleaner: 
    
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.df.columns = self.df.columns.str.strip()
        self.df.columns = ['Year', 'GHA_Exports', 'NGA_Exports', 'CHN_FDI']
        
        self.df['Year'] = self.df['Year'].astype(str)
        self.numeric_df = self.df.select_dtypes(include=[np.number])
        df = pd.read_csv('DBNomics time series.csv')  
        
        print("Data loaded successfully.")
        print(f"Initial Dimensions: {df.shape}")


        print("\n--- First 9 Rows ---")
        print(df.head(9)) 

        print("\n--- Data Types ---")
        print(df.dtypes)

        print(df.describe())

        print("\n Column names")
        print(list(df)) 

        print("\n Missing values count: ")
        print(df.isnull().sum())
        
        return self.df