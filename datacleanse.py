import numpy as np
import pandas as pd


class DataCleaner: 
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.df.columns = self.df.columns.str.strip().str.replace(' ', '_').str.replace('–', '_')
        self.df.columns = ['Year', 'GHA_Exports', 'NGA_Exports', 'GHA_EDS', 'GHA_VR', 'NGA_EDS', 'NGA_VR', 'CHN_LPR', 'CHN_RRR']
        
        self.df['Year'] = self.df['Year'].astype(str)
        
        # CRITICAL FIX: Force policy step strings with N/A text into floats at ingestion
        for col in ['CHN_LPR', 'CHN_RRR']:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            
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
        
    def gen_json(self):
        # Generate a JSON object containing the cleaned dataset
        self.json_output = {
            "loaded_data": self.df.to_dict(orient='records'), 
            "cleaned_data": self.df.to_dict(orient='records')
        }
            
