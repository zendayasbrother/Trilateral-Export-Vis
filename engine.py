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
        corr = self.df.corr(numeric_only=True)
        return stats, corr
    
    def get_model(self): 
        model = smf.ols('CHN_FDI ~ GHA_Exports + NGA_Exports', data=self.df).fit()
        return model.summary().as_text()
    
    def speartests(self):
        spearman_gha = float(self.df['CHN_FDI'].corr(self.df['GHA_Exports'], method='spearman'))
        spearman_nga = float(self.df['CHN_FDI'].corr(self.df['NGA_Exports'], method='spearman'))
        # Elasticity calculations
        elast_gha = float(spearman_gha * (self.df['GHA_Exports'].std() / self.df['CHN_FDI'].std()))
        elast_nga = float(spearman_nga * (self.df['NGA_Exports'].std() / self.df['CHN_FDI'].std()))
        return {
            "Spearman (GHA)": round(spearman_gha, 4),
            "Spearman (NGA)": round(spearman_nga, 4), 
            "Elasticity (GHA)": round(elast_gha, 5), 
            "Elasticity (NGA)": round(elast_nga, 5)
            }
    
    def web_scrape(self):
        pass  # Placeholder for future web scraping functionality
    

if __name__ == "__main__":
    engine = ResearchEngine('DBNomics time series.csv')
    (stats, corr), model_text = engine.get_desc(), engine.get_model() 
    print("Descriptive Statistics:\n", stats)
    print("\nCorrelation Matrix:\n", corr)
    print("\nOLS Regression Summary:\n", model_text)
    print("\nSpearman Correlations and Elasticities:\n", engine.speartests())
    
    
    
     