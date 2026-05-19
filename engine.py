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
        
        self.continuous_cols = ['GHA_Exports', 'GHA_EDS', 'GHA_VR', 'NGA_Exports', 'NGA_EDS', 'NGA_VR']
        self.step_cols = ['CHN_LPR', 'CHN_RRR'] 
        self.tgt_cols = self.continuous_cols + self.step_cols
        
        for col in self.tgt_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
    def get_desc(self):
        temp_df = self.df.copy()
        for col in self.step_cols:
            temp_df[col] = temp_df[col].bfill().ffill()
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
    
        step_imputation_log = "\n--- Administrative Policy Step Imputations (Linear Regression Trend) ---\n"
        step_cols_present = [c for c in self.step_cols if c in self.df.columns]
        
        if step_cols_present:
            years_nas = self.df[self.df[step_cols_present].isna().any(axis=1)]['Year'].tolist()
            
            if years_nas:
                self.df['Year'] = pd.to_numeric(self.df['Year'], errors='coerce')
                
                for col in step_cols_present:
                    is_na = self.df[col].isna()
                    if is_na.any():
                        train_step = self.df.dropna(subset=[col])
                        step_trend_model = smf.ols(f'{col} ~ Year', data=train_step).fit()
                        
                        predicted_steps = step_trend_model.predict(self.df[is_na])
                        self.df.loc[is_na, col] = predicted_steps
                
                step_imputation_log += self.df[self.df['Year'].isin(years_nas)][['Year'] + step_cols_present].to_string(index=False)
            else:
                step_imputation_log += "No missing policy step values discovered.\n"
        else:
            step_imputation_log += "No policy step columns matched the dataset index.\n"

        train_df = self.df.dropna(subset=self.step_cols)
        formula = 'GHA_Exports ~ GHA_EDS + GHA_VR + NGA_Exports + NGA_EDS + NGA_VR + CHN_LPR + CHN_RRR'
        self.model = smf.ols(formula, data=train_df).fit()
    
        self.missing_df = self.df[self.df.isna().any(axis=1)]
        predicted_output = ""
    
        if not self.missing_df.empty: 
            self.predicted = self.model.predict(self.missing_df)
            
            for col in tgt_cols:
                if col in self.df.columns:
                    is_na = self.df[col].isna()
                    
                    if is_na.any():
                        if col in self.continuous_cols:
                            predicted_output += f"\n\n--- Market Flow OLS Predictions Applied to [{col}] ---\n"
                            predicted_values = pd.DataFrame({'Year': self.df.loc[is_na, 'Year'], f'Predicted_{col}': self.predicted[is_na]})
                            predicted_output += predicted_values.to_string(index=False)
                            self.df.loc[is_na, col] = self.predicted
                        else:
                            predicted_output += f"\n[System Notice] Skipped OLS imputation for step-policy column: {col}."
        else:
            predicted_output = "\n\nNo missing (continuous) values to predict."
        
        return self.model.summary().as_text() + "\n" + step_imputation_log + predicted_output

    def speartests(self):
        spearman_gha = float(self.df['GHA_Exports'].corr(self.df['GHA_EDS'], method='spearman'))
        spearman_nga = float(self.df['NGA_Exports'].corr(self.df['NGA_EDS'], method='spearman'))
        coeff_gha = float((self.df['GHA_Exports'].std() / self.df['GHA_Exports'].mean()) * 100) 
        coeff_nga = float((self.df['NGA_Exports'].std() / self.df['NGA_Exports'].mean()) * 100)
        vre_gha = float((self.df['GHA_VR'].mean() / self.df['GHA_EDS'].mean()) * 100) 
        vre_nga = float((self.df['NGA_VR'].mean() / self.df['NGA_EDS'].mean()) * 100)
        return {
            "Spearman (GHA)": round(spearman_gha, 4),
            "Spearman (NGA)": round(spearman_nga, 4), 
            "Coefficient of Variation (GHA)": f"{round(coeff_gha, 4)}%",
            "Coefficient of Variation (NGA)": f"{round(coeff_nga, 4)}%",
            "Variable Rate Exposure (GHA)": f"{round(vre_gha, 4)}%",
            "Variable Rate Exposure (NGA)": f"{round(vre_nga, 4)}%"
            }
    
    def gen_json(self):
        self.json_output = {
            "cleaned_data": self.df.to_dict(orient='records'),
            "model_summary": self.model.summary().as_text(),
            "spearman_results": self.speartests()
        }