from datacleanse import DataCleaner
from plot import Visualiser
from engine import ResearchEngine
import numpy as np
import pandas as pd
import plotly.express as px
import warnings 

warnings.filterwarnings('ignore')


if __name__ == "__main__":
    data_cleaner = DataCleaner('Trade Int. time series.csv')
    engine = ResearchEngine('Trade Int. time series.csv')
    (stats, corr), model = engine.get_desc(), engine.get_model(engine.tgt_cols)
    spear_results = engine.speartests()
    print("Descriptive Statistics:\n", stats)
    print("\nCorrelation Matrix:\n", corr)
    print("\nOLS Regression Summary and Linear Regression Graph:\n", model)
    print("\nSpearman Correlations and Sensitivities:\n")
    for key, value in spear_results.items():
        print(f"{key}: {value}")
    
    visualiser = Visualiser('Trade Int. time series.csv')
    visualiser.lpr_impact_facets()