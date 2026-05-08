import numpy as np
import pandas as pd


# 1. Load Data
df = pd.read_csv('DBNomics time series.csv') 
df.columns = df.columns.str.strip()
df.columns = ['Year', 'GHA_Exports', 'NGA_Exports', 'CHN_FDI']

print("Data loaded successfully.")
print(f"Initial Dimensions: {df.shape}")

# 2. Data Overview
print("\n--- First 9 Rows ---")
print(df.head(9)) 

print("\n--- Data Types ---")
print(df.dtypes)

print(df.describe())


# display column names 
print("\n Column names")
print(list(df)) 

# 3. Value Scan and Cleaning
print("\n Missing values count: ")
print(df.isnull().sum())