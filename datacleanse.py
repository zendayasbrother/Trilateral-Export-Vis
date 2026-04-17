import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# implement OOP based data cleaning system 

# 1. Load Data
df = pd.read_csv('DBnomics time series.csv') 

# 2. Clean Whitespace (Crucial for CSV/Database consistency)
df.columns = df.columns.str.strip()

print("Data loaded successfully.")
print(f"Dimensions: {df.shape}")

print(df.columns.tolist())

print("\n--- First 9 Rows ---")
print(df.head(9)) 

# display dimensions of dataframe 
print("\n Dimensions of dataframe")
print(df.shape)  

# display column names 
print("\n Column names")
print(list(df)) 

# display count of missing values#
print("\n Missing values count: ")
print(df.isnull().sum().reset_index(name = 'Missing Values Counted')) 

for col in df.columns:
  print(col, df[col].nunique(), len(df))