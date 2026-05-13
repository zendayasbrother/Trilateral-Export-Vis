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
        tgt_cols = ['GHA_Exports', 'GHA_EDS', 'GHA_VR', 'NGA_Exports', 'NGA_EDS', 'NGA_VR']
        
    def get_desc(self):
        stats = self.df.describe()
        stats.loc['median'] = self.df.median(numeric_only=True)
        stats.loc['var'] = self.df.var(numeric_only=True)
        stats.loc['skew'] = self.df.skew(numeric_only=True)
        corr = self.df.corr(numeric_only=True)
        return stats, corr
    
    def get_model(self, tgt_cols): 
        # OLS Regression Test Summary to fill in N/A values
        # identify and handle outliers in the dataset
        for col in tgt_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
    
        # Train the OLS regression model using the cleaned dataset
        train_df = self.df.dropna(subset=tgt_cols)
    
        formula = 'GHA_Exports ~ GHA_EDS + GHA_VR + NGA_Exports + NGA_EDS + NGA_VR'
        self.model = smf.ols(formula, data=train_df).fit()
    
        # Handle N/A and missing values and predict missing values using the trained model
        self.missing_df = self.df[self.df['GHA_Exports'].isna()]
    
        if not self.missing_df.empty: 
            self.predicted = self.model.predict(self.missing_df)
            
            self.predicted_values = pd.DataFrame({'Year': self.missing_df['Year'], 'Predicted_GHA_Exports': self.predicted})
            predicted_output = "\n\n--- Predictions ---\n" + self.predicted_values.to_string(index=False)
        else:
            predicted_output = "\n\nNo missing values to predict."
        
        return self.model.summary().as_text() + predicted_output # Predicted the GHA_Exports values as 2.067 for 2020 and 1.361 for 2024
    
    def speartests(self):
        # Spearman Rank Correlations
        spearman_gha = float(self.df['GHA_Exports'].corr(self.df['GHA_EDS'], method='spearman'))
        spearman_nga = float(self.df['NGA_Exports'].corr(self.df['NGA_EDS'], method='spearman'))
        # Coefficint of Variation for both countries 
        coeff_gha = self.df['GHA_Exports'].std() / self.df['GHA_Exports'].mean()
        coeff_nga = self.df['NGA_Exports'].std() / self.df['NGA_Exports'].mean()
        #Calculate the Variable Rate Exposure (VRE) for both countries
        vre_gha = self.df['GHA_VR'] / self.df['GHA_EDS']
        vre_nga = self.df['NGA_VR'] / self.df['NGA_EDS']
        return {
            "Spearman (GHA)": round(spearman_gha, 4),
            "Spearman (NGA)": round(spearman_nga, 4), 
            "Coefficient of Variation (GHA)": round(coeff_gha, 4),
            "Coefficient of Variation (NGA)": round(coeff_nga, 4),
            "Variable Rate Exposure (GHA)": round(vre_gha, 4),
            "Variable Rate Exposure (NGA)": round(vre_nga, 4)
            }
    
    # Future function(s) for web scraping / generating JSON object 