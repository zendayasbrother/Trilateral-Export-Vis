import numpy as np
import pandas as pd
import statsmodels
import statsmodels.formula.api as smf
import warnings

warnings.filterwarnings('ignore')

print(f"Statsmodels version: {statsmodels.__version__}")
print("Imports successful!")

class ResearchEngine:
    
    def __init__(self, file_path):
    
        self.df = pd.read_csv(file_path)
        self.df.columns = self.df.columns.str.strip()
        self.df.columns = ['Year', 'GHA_Exports', 'NGA_Exports', 'CHN_FDI']
        
        self.df['Year'] = self.df['Year'].astype(str)
        self.numeric_df = self.df.select_dtypes(include=[np.number])
        
    def get_desc(self):
        stats = self.df.describe()
        stats.loc['median'] = self.df.median(numeric_only=True)
        stats.loc['var'] = self.df.var(numeric_only=True)
        stats.loc['skew'] = self.df.skew(numeric_only=True)
        corr = self.df.corr()
        return stats, corr
    
    def get_model(self): 
        model = smf.ols('CHN_FDI ~ GHA_Exports + NGA_Exports', data=self.df).fit()
        return model.summary().as_text()
    
    def speartests(self):
        spearman_gha = self.df['CHN_FDI'].corr(self.df['GHA_Exports'], method='spearman')
        spearman_nga = self.df['CHN_FDI'].corr(self.df['NGA_Exports'], method='spearman')
        # Elasticity calculations
        elast_gha = spearman_gha * (self.df['GHA_Exports'].std() / self.df['CHN_FDI'].std())
        elast_nga = spearman_nga * (self.df['NGA_Exports'].std() / self.df['CHN_FDI'].std())
        return {
            "Spearman (GHA)": spearman_gha,
            "Spearman (NGA)": spearman_nga, 
            "Elasticity (GHA)": elast_gha, 
            "Elasticity (NGA)": elast_nga
            }
    
    def web_scrape(self):
        pass  # Placeholder for future web scraping functionality
    

if __name__ == "__main__":
    engine = ResearchEngine('DBNomics time series.csv')
    results = engine.get_desc(), engine.get_model(), engine.speartests()
    print(results)
    
    
    
     