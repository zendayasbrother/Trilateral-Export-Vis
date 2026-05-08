import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Visualizer:
    
    def __init__(self, file_path):
        # Load and clean data immediately upon instantiation
        self.df = pd.read_csv(file_path)
        self.df.columns = self.df.columns.str.strip()
        
        
        self.df.columns = ['Year', 'GHA_Exports', 'NGA_Exports', 'CHN_FDI']
        
        self.df['Year'] = self.df['Year'].astype(str)
        self.numeric_df = self.df.select_dtypes(include=[pd.np.number])
        
    def get_bar(self):
        plt.figure(figsize=(10, 6))
        self.exports_gha = self.df['GHA_Exports'] 
        self.exports_nga = self.df['NGA_Exports'] 
        self.period = self.df['Year'] 
        plt.bar(self.period, self.exports_gha, color='orange', label='Ghana') 
        plt.bar(self.period, self.exports_nga, color='green', label='Nigeria') 
        
        for i in range(len(self.df)):
            year = self.period.iloc[i]
            
            plt.text(i, self.exports_gha.iloc[i], f'{self.exports_gha.iloc[i]:.2f}', 
                     fontsize = 9, ha = 'center', color = 'white') 
            plt.text(i, self.exports_nga.iloc[i], f'{self.exports_nga.iloc[i]:.2f}', 
                    fontsize = 9, ha ='center', color = 'white')

        plt.xlabel('Year')
        plt.ylabel('Exports (% of GDP)')
        plt.title('Year vs. Exports - (% of GDP)')
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
        plt.scatter(self.exports_nig, self.fdi_chn, color='green', label='Nigeria') 
        
        for i in range(len(df)):
            year = self.period.iloc[i]
            
            plt.text(self.exports_gha.iloc[i], self.fdi_chn.iloc[i], f'{int(self.period.iloc[i])}', 
                     fontsize = 9, ha = 'right', color = 'orange') 
            plt.text(self.exports_nig.iloc[i], self.fdi_chn.iloc[i], f'{int(self.period.iloc[i])}', 
                    fontsize = 9, ha ='left', color = 'green')

        plt.xlabel('Exports of goods and services (% of GDP)')
        plt.ylabel('China FDI net inflows (% of GDP)')
        plt.title('FDI CHN vs. Exports - (% of GDP)')
        plt.legend()
        plt.grid(True)
        plt.show() 
        
        
        
if __name__ == "__main__":
    visualizer = Visualizer('DBNomics time series.csv')
    visualizer.scatter()