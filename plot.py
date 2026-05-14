from datacleanse import DataCleaner
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class Visualiser(DataCleaner):
    
    def __init__(self, file_path):
        super().__init__(file_path)
        # include interest service burden calculations in the dual line chart
        self.df['GHA_ISB'] = ((self.df['GHA_EDS'] - self.df['GHA_VR']) * 0.05 + (self.df['GHA_VR'] * self.df['CHN_LPR'] / 100)) / self.df['GHA_Exports'] * 100
        self.df['NGA_ISB'] = ((self.df['NGA_EDS'] - self.df['NGA_VR']) * 0.05 + (self.df['NGA_VR'] * self.df['CHN_LPR'] / 100)) / self.df['NGA_Exports'] * 100

# Create a dual line chart to simultaneously visualize the trends of ISBs over time for both countries
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

    def scatter(self): 
        # Create a 'Melted' dataframe for side-by-side 3D comparison
        self.df_long = self.df.melt(
            id_vars=['Year', 'CHN_LPR'], 
            value_vars=['GHA_Exports', 'NGA_Exports', 'GHA_EDS', 'NGA_EDS', 'GHA_VR', 'NGA_VR'],
            var_name='Metric', 
            value_name = 'Value'
        )

        # Plotting logic using columns that actually exist in self.df_long
        fig = px.scatter_3d(
            self.df_long, 
            x='Year',      
            y='Value',     
            z='CHN_LPR',   
            color='Metric', 
            size = 'Value',   
            opacity = 0.8, 
            title = "West African Export-to-Debt Efficiency vs. China LPR"
        ) 
        
        fig.update_layout(
            title_x = 0.5, 
            template = 'plotly_white', 
            autosize = True
        )
        
        fig.show()