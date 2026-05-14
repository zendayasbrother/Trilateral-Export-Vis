from datacleanse import DataCleaner
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class Visualiser(DataCleaner):
    
    def __init__(self, file_path):
        super().__init__(file_path)
        # include interest service burden calculations in the dual line chart
        self.isb_gha = ((self.df['GHA_EDS'] - self.df['GHA_VR']) * 0.05 + (self.df['GHA_VR'] * self.df['CHN_LPR'] / 100)) / self.df['GHA_Exports'] * 100
        self.isb_nga = ((self.df['NGA_EDS'] - self.df['NGA_VR']) * 0.05 + (self.df['NGA_VR'] * self.df['CHN_LPR'] / 100)) / self.df['NGA_Exports'] * 100

# Create a dual line chart to simultaneously visualize the trends of ISBs over time for both countries
    def dual_isb(self):
        fig = px.line(
            self.df, 
            x='Year', 
            y = [self.isb_gha, self.isb_nga], 
            title="Interest Service Burden (%) over Time",
            labels={'value': 'ISB % of Exports'} 
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

# 3D SCATTER plot to visualize the relationship between Total Exports (by country), Total EDS and Variable Rate for both countries
def scatter(self): 
    # Create a 'Melted' dataframe for side-by-side 3D comparison
    self.df_long = self.df.melt(
        id_vars=['Year', 'CHN_LPR'], 
        value_vars=['GHA_Exports', 'NGA_Exports', 'GHA_EDS', 'NGA_EDS', 'GHA_VR', 'NGA_VR'],
        var_name='Metric', 
        value_name='Exports'
    )
    # # Plotting the 'Middle Ground'
    fig = px.scatter_3d(
        self.df_long, 
        x='Exports', 
        y='Debt', 
        z='LPR', 
        color='Country', 
        size='Debt', 
        opacity=0.8, 
        title="West African Export-to-Debt Efficiency vs. China LPR"
        ) 
