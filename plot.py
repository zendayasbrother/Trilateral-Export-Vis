import plotly.express as px
import pandas as pd
from dbnomics import fetch_series

dfs = []

# Exports of goods and services (% of GDP) - Ghana
df1 = fetch_series("AFDB/bbkawjf/NE.EXPO.GNFS.ZS.GHA")
df1["series_id"] = df1[["provider_code", "dataset_code", "series_code"]].agg('/'.join, axis=1)
dfs.append(df1)
px.line(df1, x="period", y="value", title=df1.series_id[0]).show()

# Exports of goods and services (% of GDP) - Nigeria
df2 = fetch_series("AFDB/bbkawjf/NE.EXPO.GNFS.ZS.NGA")
df2["series_id"] = df2[["provider_code", "dataset_code", "series_code"]].agg('/'.join, axis=1)
dfs.append(df2)
px.line(df2, x="period", y="value", title=df2.series_id[0]).show()

# Annual – Foreign direct investment, net inflows (% of GDP) – China
df3 = fetch_series("WB/JOB/A-BX.KLT.DINV.WD.GD.ZS-CHN")
df3["series_id"] = df3[["provider_code", "dataset_code", "series_code"]].agg('/'.join, axis=1)
dfs.append(df3)
px.line(df3, x="period", y="value", title=df3.series_id[0]).show()

# Combine all data and plot
df_all = pd.concat(dfs)
fig = px.line(df_all, x="period", y="value", color="series_code", title="NUM EXPORTS VS FDI INFLOWS")
fig.update_layout(legend={"xanchor": "right", "yanchor": "bottom"})
fig.show()
