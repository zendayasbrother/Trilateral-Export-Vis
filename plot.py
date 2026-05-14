from datacleanse import DataCleaner
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class Visualiser(DataCleaner):
    
    def __init__(self, file_path):
        super().__init__(file_path)
        # include interest service burden calculations in the dual line chart

# Create a dual line chart to simultaneously visualize the trends of ISBs over time for both countries
    def dual_exports(self):
        pass
    
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

# create a 3D SCATTER plot to visualize the relationship between Exports, Total EDS and Variable Rate for both countries
def scatter(self): 
    pass