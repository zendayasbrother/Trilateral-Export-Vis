import numpy as np
import matplotlib.pyplot as plt

# Provided data (maybe the csv file)
exports_gha = [0.627, 0.458, 0.83, 1.11, 0.942, 2.38, 2.03, 2.81, 0, 1.39, 2.2]

exports_nig = [8.04, 1.11, 
               1.67, 0.795, 0.471, 0.721, 
              1.04, 1.67, 1.77, 1.85, 0.834]

fdi_chn = [64.96, 72.97, 123.13, 174.39, 216.42, 138.29, 143.03, 136.91, 153.72, 178.8, 149.69]

# Ensure all lists are the same length for simplicity
period = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]


# Plot the scatter plots
plt.figure(figsize = (10, 6))

plt.scatter(exports_gha, fdi_chn, color = 'orange', label = 'Ghana')
plt.scatter(exports_nig, fdi_chn, color ='green', label = 'Nigeria')

# Adding labels for each point for clarity
for i in range(len(exports_gha)):
    plt.text(exports_gha[i], fdi_chn[i], f'{period[i]}', fontsize = 11, ha ='right', color = 'orange')
    plt.text(exports_nig[i], fdi_chn[i], f'{period[i]}', fontsize = 11, ha = 'left', color = 'green')

plt.xlabel('Exports to CHN (billions USD)')
plt.ylabel('FDI outflows CHN (billions USD)')
plt.title('FDI CHN vs. Exports to CHN - (in billions USD)')
plt.legend()
plt.grid(True)
plt.show()