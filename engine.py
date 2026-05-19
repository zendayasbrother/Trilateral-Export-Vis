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
        self.df.columns = self.df.columns.str.strip()
        
        # Categorized targets from Ver. 1 for dynamic data management
        self.continuous_cols = ['GHA_Exports', 'GHA_EDS', 'GHA_VR', 'NGA_Exports', 'NGA_EDS', 'NGA_VR']
        self.step_cols = ['CHN_LPR', 'CHN_RRR', 'CHN_FAI', 'CHN_FX']
        self.tgt_cols = self.continuous_cols + self.step_cols
        
        for col in self.tgt_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
    def get_desc(self):
        temp_df = self.df.copy()
        for col in self.step_cols:
            if col in temp_df.columns:
                temp_df[col] = temp_df[col].bfill().ffill()
            
        for col in self.continuous_cols:
            if col in temp_df.columns:
                temp_df[col] = temp_df[col].interpolate(method='linear').bfill().ffill()
                
        stats = temp_df.describe()
        stats.loc['median'] = temp_df.median(numeric_only=True)
        stats.loc['var'] = temp_df.var(numeric_only=True)
        stats.loc['skew'] = temp_df.skew(numeric_only=True)
        corr = temp_df.corr(numeric_only=True)
        return stats, corr
    
    def get_model(self, tgt_cols=None): 
        if tgt_cols is None: 
            tgt_cols = self.tgt_cols
        else:
            for col in tgt_cols:
                if col in self.df.columns:
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                    
        self.df['Year'] = pd.to_numeric(self.df['Year'], errors='coerce')
    
        train_df = self.df.dropna(subset=tgt_cols)
    
        formula = 'GHA_Exports ~ GHA_EDS + GHA_VR + NGA_Exports + NGA_EDS + NGA_VR + CHN_LPR + CHN_RRR + CHN_FAI + CHN_FX'
        self.model = smf.ols(formula, data=train_df).fit()
        
        return self.model.summary().as_text() 
    
    def speartests(self):
        spearman_gha = float(self.df['GHA_Exports'].corr(self.df['GHA_EDS'], method='spearman'))
        spearman_nga = float(self.df['NGA_Exports'].corr(self.df['NGA_EDS'], method='spearman'))
        
        coeff_gha = float((self.df['GHA_Exports'].std() / self.df['GHA_Exports'].mean()) * 100) 
        coeff_nga = float((self.df['NGA_Exports'].std() / self.df['NGA_Exports'].mean()) * 100)
        
        vre_gha = float((self.df['GHA_VR'].mean() / self.df['GHA_EDS'].mean()) * 100) 
        vre_nga = float((self.df['NGA_VR'].mean() / self.df['NGA_EDS'].mean()) * 100)
        
        isb_gha = float(((self.df['GHA_EDS'] - self.df['GHA_VR']) * 0.05 + (self.df['GHA_VR'] * self.df['CHN_LPR'] / 100)) / self.df['GHA_Exports'] * 100)
        isb_nga = float(((self.df['NGA_EDS'] - self.df['NGA_VR']) * 0.05 + (self.df['NGA_VR'] * self.df['CHN_LPR'] / 100)) / self.df['NGA_Exports'] * 100)

        
        return {
            "Spearman (GHA)": round(spearman_gha, 4),
            "Spearman (NGA)": round(spearman_nga, 4), 
            "Coefficient of Variation (GHA)": f"{round(coeff_gha, 4)}%",
            "Coefficient of Variation (NGA)": f"{round(coeff_nga, 4)}%",
            "Variable Rate Exposure (GHA)": f"{round(vre_gha, 4)}%",
            "Variable Rate Exposure (NGA)": f"{round(vre_nga, 4)}%",
            "Interest Service Burden (GHA)": f"£{round(isb_gha, 4)}",
            "Interest Service Burden (NGA)": f"£{round(isb_nga, 4)}%"
        }
    
    def gen_json(self):
        self.json_output = {
            "cleaned_data": self.df.to_dict(orient='records'),
            "model_summary": self.model.summary().as_text(),
            "spearman_results": self.speartests()
        }