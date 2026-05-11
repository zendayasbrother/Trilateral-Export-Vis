from datacleanse import DataCleaner
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class Visualizer(DataCleaner):
    
    def __init__(self, file_path):
        super().__init__(file_path)

    def bar_exports(self): 
        fig = px.bar(
            self.df, 
            x='Year', 
            y=['GHA_Exports', 'NGA_Exports'],
            barmode='group',
            color_discrete_map={'GHA_Exports': 'orange', 'NGA_Exports': 'green'},
            labels={'value': 'Exports (% of GDP)', 'variable': 'Country'},
            title='Exports of goods and services (% of GDP) - Ghana vs. Nigeria'
        )
        
        fig.update_layout(xaxis_type='category') # Ensures years aren't treated as continuous numbers
        fig.show()

    def scatter(self): 
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.df['GHA_Exports'], 
            y=self.df['CHN_FDI'],
            mode='markers+text',
            name='Ghana',
            text=self.df['Year'],
            textposition='top left',
            marker=dict(color='orange')
        ))

        fig.add_trace(go.Scatter(
            x=self.df['NGA_Exports'], 
            y=self.df['CHN_FDI'],
            mode='markers+text',
            name='Nigeria',
            text=self.df['Year'],
            textposition='top right',
            marker=dict(color='green')
        ))

        fig.update_layout(
            title='FDI CHN vs. Exports - (% of GDP)',
            xaxis_title='Exports of goods and services (% of GDP)',
            yaxis_title='China FDI net inflows (% of GDP)',
            template='plotly_white'
        )
        
        fig.show()