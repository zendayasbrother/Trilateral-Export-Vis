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
        for self.c in self.df.columns: 
            self.df.columns = self.df.columns.str.strip()
        
    def get_desc(self):
        stats = self.df.describe()
        stats.loc['median'] = self.df.median(numeric_only=True)
        stats.loc['var'] = self.df.var(numeric_only=True)
        stats.loc['skew'] = self.df.skew(numeric_only=True)
        corr = self.df.corr(numeric_only=True)
        return stats, corr
    
    def get_model(self): 
        # OLS Regression Test Summary, Linear Regression Graph + Handing N/A values
        model = smf.ols('CHN_FDI ~ GHA_Exports + NGA_Exports', data=self.df).fit()
        return model.summary().as_text()
    
    def speartests(self):
        # Granger Casuality Tests of some sort below
        # calculate variable rates of new data
        # Spearman Rank Correlations
        spearman_gha = float()
        spearman_nga = float()
        # Elasticity calculations
        elast_gha = float()
        elast_nga = float()
        return {
            "Spearman (GHA)": round(spearman_gha, 4),
            "Spearman (NGA)": round(spearman_nga, 4), 
            "Elasticity (GHA)": round(elast_gha, 5), 
            "Elasticity (NGA)": round(elast_nga, 5)
            }
    
    # Future function(s) for web scraping / generating JSON object 