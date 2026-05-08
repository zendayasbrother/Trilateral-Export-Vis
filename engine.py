from datacleanse import DataCleaner 
import numpy as np
import pandas as pd
import json
import statsmodels
import statsmodels.formula.api as smf
import warnings

warnings.filterwarnings('ignore')

print(f"Statsmodels version: {statsmodels.__version__}")
print("Imports successful!")

class ResearchEngine(DataCleaner):
    
    def __init__(self, file_path):
        DataCleaner().__init__(file_path)
        
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
    
    def gen_json(self): 
        self.time_series = self.df.to_dict(orient='records')
        (stats, corr) = self.get_desc()
        self.model_summary = self.get_model()
        self.spearman = self.speartests()
        
        self.master_dict = {
            "metadata": {
                "source": "DBNomics",
                "description": "Time series data on Ghana and Nigeria exports and China FDI inflows",
                "variables": {
                    "Year": "Year of observation",
                    "GHA_Exports": "Ghana exports of goods and services (% of GDP)",
                    "NGA_Exports": "Nigeria exports of goods and services (% of GDP)",
                    "CHN_FDI": "China FDI net inflows (% of GDP)"
                }
            },
            "statistics": {
            "descriptive_stats": stats.to_dict(),
            "correlation_matrix": corr.to_dict(),
            "spearman_results": self.spearman
        } 
            }
        
        with open('data.json', 'w') as f:
            json.dump(self.master_data, f, indent=4)
        print("Master JSON generated for Web App.")