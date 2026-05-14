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

    def bubble(self): 
        fig = px.scatter(
            self.df, 
            x='GHA_Exports', 
            y='GHA_EDS',
            size='CHN_LPR', 
            color='Year',
            hover_name='Year',
            title="Ghana: Export Resilience vs Debt Burden (Bubble Size = China LPR)",
            labels={'GHA_Exports': 'Total Exports', 'GHA_EDS': 'Total Debt'},
            template='plotly_white'
        )

        self.df_long = self.df.melt(
            id_vars=['Year', 'CHN_LPR'],
            value_vars=['GHA_Exports', 'NGA_Exports'],
            var_name='Country',
            value_name='Exports'
        )
    
    
        self.df_long['Debt'] = self.df.melt(value_vars=['GHA_EDS', 'NGA_EDS'])['value']

        fig = px.scatter(
            self.df_long,
            x="Exports",
            y="Debt",
            animation_frame="Year", 
            animation_group="Country",
            size="CHN_LPR",
            color="Country",
            hover_name="Country",
            log_x=False, 
            size_max=45,
            range_x=[self.df_long['Exports'].min()*0.9, self.df_long['Exports'].max()*1.1],
            range_y=[self.df_long['Debt'].min()*0.9, self.df_long['Debt'].max()*1.1],
            title="Export-to-Debt Efficiency Over Time",
            color_discrete_map={"GHA_Exports": "orange", "NGA_Exports": "green"}
        )

        fig.show()
    
    
    def gen_json(self):
        # Generate a JSON object containing the visualization data and configuration
        self.json_output = {
            "visualization_data": self.df.to_dict(orient='records'),
            "visualization_config": {
                "dual_isb_chart": {
                    "x": "Year",
                    "y": ["GHA_ISB", "NGA_ISB"],
                    "title": "Interest Service Burden (%) over Time",
                    "labels": {"value": 'ISB % of Exports'},
                    "color_discrete_map": {"GHA_ISB": "orange", "NGA_ISB": "green"},
                    "template": 'plotly_white'
                },
                
                "bar_chart": {
                    "x": "Period",
                    "y": "Exports",
                    "color": "Country",
                    "barmode": "group",
                    "color_discrete_map": {'GHA_Exports': 'orange', 'NGA_Exports': 'green'},
                    "labels": {'Exports': 'Average Exports (USD Billions)', 'Country': 'Nation'},
                    "title": 'Export Resilience: Pre-COVID vs. COVID Impact',
                    "category_orders": {'Period': ['Pre-COVID', 'COVID']},
                    "template": 'plotly_white'
                },
                
                "bubble_chart": {
                    "x": "GHA_Exports",
                    "y": "GHA_EDS",
                    "size": "CHN_LPR",
                    "color": "Year",
                    "hover_name": "Year",
                    "title": "Ghana: Export Resilience vs Debt Burden (Bubble Size = China LPR)",
                    "labels": {"GHA_Exports": 'Total Exports', 'GHA_EDS': 'Total Debt'},
                    "template": 'plotly_white'
                }
            }
        }