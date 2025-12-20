import numpy as np 
import pandas as pd


df = pd.read_csv('') 

print("Column names")
print(df.columns.tolist())


# display first six rows 
print("\n First nine rows (2012-2020)")
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
