import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 1. Load data and clean column names (removes the trailing spaces in your CSV)
df = pd.read_csv('DBnomics time series.csv')
df.columns = df.columns.str.strip()

print("Data loaded successfully.") 

# 2. Assign columns directly (No 'Country' column exists in your CSV)
# We use the exact names from your file
exports_gha = df['GHA – Exports of goods and services (% of GDP)']
exports_nig = df['NIG – Exports of goods and services (% of GDP)']

fdi_chn = df['CHN – Annual Foreign direct investment, net inflows (% of GDP)']
period = df['period']

# 3. Plotting
plt.figure(figsize=(10, 6))

plt.scatter(exports_gha, fdi_chn, color='orange', label='Ghana')
plt.scatter(exports_nig, fdi_chn, color='green', label='Nigeria')

# 4. Adding labels (Using .iloc to avoid index errors)
for i in range(len(df)):
    plt.text(exports_gha.iloc[i], fdi_chn.iloc[i], f'{int(period.iloc[i])}', 
             fontsize = 9, ha = 'right', color = 'orange')
    plt.text(exports_nig.iloc[i], fdi_chn.iloc[i], f'{int(period.iloc[i])}', 
             fontsize = 9, ha ='left', color = 'green')

plt.xlabel('Exports of goods and services (% of GDP)')
plt.ylabel('China FDI net inflows (% of GDP)')
plt.title('FDI CHN vs. Exports - (% of GDP)')
plt.legend()
plt.grid(True)
plt.show()