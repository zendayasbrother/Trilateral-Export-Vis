from engine import ResearchEngine
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import numpy as np
import json

class Visualiser(ResearchEngine):
    
    def __init__(self, file_path):
        super().__init__(file_path)
        pio.renderers.default = "browser"
        tgt_cols = self.continuous_cols + self.step_cols
        for col in tgt_cols:
            if col in self.df.columns:
                if self.df[col].dtype == 'object':
                    self.df[col] = self.df[col].astype(str).str.replace(r'[^\d\.]', '', regex=True)
                    
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                

    # Create a dual line chart to simultaneously visualize Chinese closing inds. trends over time
    def dual_isb(self):
        isb_gha = 'GHA_ISB'
        isb_nga = 'NGA_ISB'
        
        fig = px.line(
            self.df, 
            x='Year', 
            y={isb_gha: "GHA", isb_nga: "NGA"},
            title="Interest Service Burden (%) over Time",
            labels={'value': 'ISB % of Exports'},
            color_discrete_map = {"GHA": "orange", "NGA": "green"}
        )
        
        # Shade GHA (Orange)
        fig.add_trace(
            go.Scatter(
                x = self.df['Year'], 
                y = self.df[isb_gha],
                fill='tozeroy', 
                mode='none', 
                name='GHA Shading', 
                fillcolor='rgba(255, 165, 0, 0.3)',
                showlegend=False))

        # Shade NGA (Green)
        fig.add_trace(
            go.Scatter(
                x = self.df['Year'], 
                y = self.df[isb_nga], 
                fill='tozeroy', 
                mode='none', 
                name='NGA Shading', 
                fillcolor='rgba(0, 128, 0, 0.3)',
                showlegend=False))
        
        fig.update_layout(
            title_x=0.5, 
            template='plotly_white', 
            autosize=True
        )
        
        fig.show()
        
# Bar chart shoulld be aggregated in some sort against grouped periods (non-COVID vs. COVID) 
    def bar_exports(self): 
        # COVID grouping logic 
        self.df_plot = self.df.copy()
        self.df_plot['Period'] = self.df_plot['Year'].apply(lambda x: 'COVID' if x >= '2020' else 'Pre-COVID')#
        
        self.agg_df = self.df_plot.groupby('Period')[['GHA_Exports', 'NGA_Exports']].mean().reset_index()
        
        self.melted_df = self.agg_df.melt(
            id_vars=['Period'], 
            value_vars=['GHA_Exports', 'NGA_Exports'],
            var_name='Country', 
            value_name='Exports'
        )
        
        fig = px.bar(
            self.melted_df, 
            x = 'Period', 
            y = 'Exports',
            color = 'Country', 
            barmode='group',      
            color_discrete_map={'GHA_Exports': 'orange', 'NGA_Exports': 'green'},
            labels = {'Exports': 'Average Exports (USD Billions)', 'Country': 'Nation'},
            title = 'Export Resilience: Pre-COVID vs. COVID Impact',
            category_orders={'Period': ['Pre-COVID', 'COVID']}
        )

        fig.update_layout(
            title_x = 0.5, 
            template='plotly_white', 
            bargap=0.5,
            autosize = True
           )
    
        fig.show()

    # Combination scatterplot visual of Chinese indicator(s) against West African with a regression trendline
    def lpr_impact_facets(self): 
        # Correctly capture your newly created ratio properties
        df_long = self.df.melt(
            id_vars=['Year', 'CHN_LPR'],
            value_vars=['GHA_Ratio', 'NGA_Ratio'],
            var_name='Country', value_name='Leverage'
        )
        
        # Clean up labels for presentation view
        df_long['Country'] = df_long['Country'].replace({'GHA_Ratio': 'Ghana', 'NGA_Ratio': 'Nigeria'})
        
        df_clean = df_long.replace([np.inf, -np.inf], np.nan).dropna(subset=['Leverage', 'CHN_LPR'])

        # 4. Plot
        fig = px.scatter(
                df_clean, 
                x='CHN_LPR', 
                y='Leverage',
                color='Country',
                facet_col='Country',
                trendline="ols",
                hover_name='Year',           
                 hover_data={
                    'Year': False,           
                    'CHN_LPR': ':.2f',       
                    'Leverage': ':.3f',      
                    'Country': True
                },
                title="West African Debt Leverage vs. China LPR",
                labels={'CHN_LPR': 'China LPR (%)', 'Leverage': 'Debt Stock / Exports'},
                template='plotly_white'
            )
        
        fig.show()
    
    
    def gen_json(self):
        stats_summary = self.speartests()
    
        self.json_output = {
        "metadata": {
            "source": "Trilateral-Export-Vis",
            "last_updated": "2026-05-15",
            "observations": len(self.df)
        },
        "statistical_insights": stats_summary,
        "visualization_data": self.df.to_dict(orient='records'),
        "visualization_config": {
            "dual_isb_chart": {
                "x": "Year",
                "y": ["GHA_ISB", "NGA_ISB"],
                "title": "Interest Service Burden (%) over Time",
                "labels": {"value": "ISB % of Exports"},
                "color_discrete_map": {"GHA_ISB": "orange", "NGA_ISB": "green"},
                "template": "plotly_white"
            },
            "bar_chart": {
                "x": "Period",
                "y": "Exports",
                "color": "Country",
                "barmode": "group",
                "color_discrete_map": {"GHA_Exports": "orange", "NGA_Exports": "green"},
                "labels": {"Exports": "Average Exports (USD Billions)", "Country": "Nation"},
                "title": "Export Resilience: Pre-COVID vs. COVID Impact",
                "category_orders": {"Period": ["Pre-COVID", "COVID"]},
                "template": "plotly_white"
            },
            "lpr_impact_facets": {
                "x": "CHN_LPR",
                "y": "Leverage",
                "facet_col": "Country",
                "color": "Country",
                "trendline": "ols",
                "hover_data": ["Year"],
                "title": "Leverage Sensitivity: West African Debt Ratios vs. Chinese LPR",
                "labels": {
                    "CHN_LPR": "China Loan Prime Rate (%)",
                    "Leverage": "Debt Stock per $1 Export",
                    "Country": "Nation"
                },
                "template": "plotly_white",
                "notes": "Facetted view highlights why GHA (-0.53) and NGA (0.53) Spearman ranks diverge."
            }
        }
    }
    
        with open('viz_output.json', 'w') as f:
            json.dump(self.json_output, f, indent=4)
        
        return self.json_output