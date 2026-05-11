from datacleanse import DataCleaner
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Visualizer(DataCleaner):
    
    def __init__(self, file_path):
        super().__init__(file_path)

        
    def bar_exports(self):
        plt.figure(figsize=(10, 6))
        self.exports_gha = self.df['GHA_Exports'] 
        self.exports_nga = self.df['NGA_Exports'] 
        self.period = self.df['Year'] 
        width = 0.35
        x = np.arange(len(self.period))
        plt.bar(x - width/2, self.period, self.exports_gha, color='orange', label='Ghana') 
        plt.bar(x + width/2, self.period, self.exports_nga, color='green', label='Nigeria') 
        
        for i in range(len(self.df)):
            year = self.period.iloc[i]
            
            plt.text(x[i] - width/2, self.exports_gha.iloc[i], f'{int(self.period.iloc[i])}', 
                     fontsize = 9, ha = 'center', color = 'orange')
            plt.text(x[i] + width/2, self.exports_nga.iloc[i], f'{int(self.period.iloc[i])}',
                    fontsize = 9, ha ='center', color = 'green')
            
        plt.xlabel('Year')
        plt.ylabel('Exports of goods and services (% of GDP)')
        plt.title('Exports of goods and services (% of GDP) - Ghana vs. Nigeria')
        plt.legend()
        plt.grid(True)
        plt.show()

    def scatter(self): 
        plt.figure(figsize=(10, 6))
        
        self.exports_gha = self.df['GHA_Exports'] 
        self.exports_nga = self.df['NGA_Exports'] 
        self.fdi_chn = self.df['CHN_FDI'] 
        self.period = self.df['Year'] 
        plt.scatter(self.exports_gha, self.fdi_chn, color='orange', label='Ghana') 
        plt.scatter(self.exports_nga, self.fdi_chn, color='green', label='Nigeria') 
        
        for i in range(len(self.df)):
            plt.text(self.exports_gha.iloc[i], self.fdi_chn.iloc[i], f'{int(self.period.iloc[i])}', 
                     fontsize = 9, ha = 'right', color = 'orange') 
            plt.text(self.exports_nga.iloc[i], self.fdi_chn.iloc[i], f'{int(self.period.iloc[i])}', 
                    fontsize = 9, ha ='left', color = 'green')

        plt.xlabel('Exports of goods and services (% of GDP)')
        plt.ylabel('China FDI net inflows (% of GDP)')
        plt.title('FDI CHN vs. Exports - (% of GDP)')
        plt.legend()
        plt.grid(True)
        plt.show() 
        
    