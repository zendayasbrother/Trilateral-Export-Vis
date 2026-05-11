from datacleanse import DataCleaner 
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import warnings

warnings.filterwarnings('ignore')

class ResearchEngine(DataCleaner):
    
    def __init__(self, file_path):
        super().__init__(file_path)
        
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
        # Granger Casuality Tests of some sort below
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
    
    # Future function(s) for web scraping / generating JSON object 