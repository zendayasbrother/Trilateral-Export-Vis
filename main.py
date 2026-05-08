from datacleanse import df
from plot import Visualizer
from engine import ResearchEngine
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels
import statsmodels.formula.api as smf
import warnings 

warnings.filterwarnings('ignore')

if __name__ == "__main__":
    engine = ResearchEngine('DBNomics time series.csv')
    (stats, corr), model_text = engine.get_desc(), engine.get_model() 
    print("Descriptive Statistics:\n", stats)
    print("\nCorrelation Matrix:\n", corr)
    print("\nOLS Regression Summary:\n", model_text)
    print("\nSpearman Correlations and Elasticities:\n", engine.speartests()) 
    
    visualizer = Visualizer('DBNomics time series.csv')
    visualizer.scatter()