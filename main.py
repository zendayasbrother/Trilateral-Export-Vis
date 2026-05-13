from datacleanse import DataCleaner
from plot import Visualizer
from engine import ResearchEngine
import numpy as np
import pandas as pd
import plotly.express as px
import warnings 

warnings.filterwarnings('ignore')


if __name__ == "__main__":
    data_cleaner = DataCleaner('Exports time series.csv')
    engine = ResearchEngine('Exports time series.csv')
    (stats, corr), model = engine.get_desc(), engine.get_model()
    print("Descriptive Statistics:\n", stats)
    print("\nCorrelation Matrix:\n", corr)
    print("\nOLS Regression Summary and Linear Regression Graph:\n", model)
    print("\nSpearman Correlations and Sensitivities:\n", engine.speartests())