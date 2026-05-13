from datacleanse import DataCleaner
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class Visualizer(DataCleaner):
    
    def __init__(self, file_path):
        super().__init__(file_path)
        # include interest service burden calculations in the visualizations as well as the coefficient of variation for both countries to provide a more comprehensive analysis of the export trends and their implications for economic stability and growth

# Create a dual line chart to simultaneously visualize the trends of Exports over time for both countries
    def dual_exports(self):
        pass
    
# Bar chart shoulld be aggregated in some sort against grouped periods (non-COVID vs. COVID) 
    def bar_exports(self): 
        fig = px.bar(
            self.df, 
            x = 'Year', 
            y = ['GHA_Exports', 'NGA_Exports'],
            barmode='group',
            color_discrete_map={'GHA_Exports': 'orange', 'NGA_Exports': 'green'},
            labels={'value': 'Exports (USD billions)', 'variable': 'Country'},
            title='Exports to China (USD billions) - Ghana vs. Nigeria'
        )
        
        fig.update_layout(xaxis_type='category') 
        fig.show()

# create a 3D SCATTER plot to visualize the relationship between Exports, Total EDS and Variable Rate for both countries
def scatter(self): 
        fig = go.Figure() 
        fig.add_trace(go.Scatter(
            x=self.df['GHA_Exports'], 
            y=self.df[''],
            mode='markers+text',
            name='Ghana',
            text=self.df['Year'],
            textposition='top left',
            marker=dict(color='orange')
        ))

        fig.add_trace(go.Scatter(
            x=self.df['NGA_Exports'], 
            y=self.df[''],
            mode='markers+text',
            name='Nigeria',
            text=self.df['Year'],
            textposition='top right',
            marker=dict(color='green')
        ))

        fig.update_layout(
            
        )
        
        fig.show()
        
    