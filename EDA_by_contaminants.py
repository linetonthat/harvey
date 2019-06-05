import plotly.offline as pyo
import plotly.graph_objs as go
from plotly import tools
import plotly.plotly as py
import plotly.figure_factory as ff

import numpy as np

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load data
path = "/Users/linetonthat/ds_training/projects/2019-06_Harvey_pollution/3_treated_data/"
df = pd.read_csv(path+"largest-emissions-in-lbs.csv")
df.info()

sorted_df = df.sort_values(by = ['contaminant', 'Regulated entity name', 'Event began'])

### --------------------------------------------------------
### Analyse contaminants
### --------------------------------------------------------

df['contaminant'].unique()
list_of_contaminants = list(df['contaminant'].unique())
list_of_contaminants.sort()
list_of_contaminants = pd.DataFrame(list_of_contaminants)
list_of_contaminants.to_csv(path+"list_of_contaminants.csv")

df['units'].unique()
# only pounds (lbs) used as unit

# ---------------------
# assess quantities per contaminant
df2 = df.groupby(by=['contaminant'])[['quantity']].sum()
df2.columns = ['quantity']
df2.sort_values(by = ['quantity'], ascending = False, inplace = True)

# draw horizontal bar charts of main pollutants emitted
overall_title = "20 most emitted contaminants"
x_title = "Quantities (lbs)"
#export_filename = "../6_communication/visuels/2018_type_site_pourcent_"+unit+".html"
### --------------------------------------------------------

trace= [go.Bar(
        y=df2.head(20).index,
        x=df2.head(20)['quantity'],
        orientation = 'h'
        )]
layout = go.Layout(title = overall_title, 
                   hovermode = 'closest',
                   xaxis=dict(dict(title=x_title,
                                   domain=[0.25, 1.0], anchor='y1')),
                   yaxis=dict(dict(domain=[0.0, 1.0], anchor='x1')))
fig = go.Figure(data = trace, layout = layout)
pyo.plot(fig)
#pyo.plot(fig,filename = export_filename)

top_10_contaminants = list(df2.head(10).index)

### --------------------------------------------------------
### Regulated entity name
### --------------------------------------------------------
# assess quantities per contaminant et per facility
"""
df3 = df.groupby(by=['contaminant', 'Regulated entity name'])[['quantity']].sum()
df3 = df3.unstack()
df3 = df3.fillna(0)
"""
df3 = pd.pivot_table(df, values = 'quantity', index = 'contaminant', columns = 'Regulated entity name',
                     aggfunc = 'sum')


# draw horizontal bar charts of pollutants emitted by facility
#df3.columns[1]
#facility = 'BASF BEAUMONT AGRO PLANT'
facility = 'ARKEMA CROSBY PLANT'
overall_title = "Contaminants - "+ facility
x_title = "Quantities (lbs)"
#export_filename = "../6_communication/visuels/2018_type_site_pourcent_"+unit+".html"
### --------------------------------------------------------

b_df = df3[[facility]].dropna().sort_values(by = [facility], ascending = False)

trace= [go.Bar(
        y=b_df.index,
        x=b_df[facility],
        orientation = 'h'
        )]
layout = go.Layout(title = overall_title, 
                   hovermode = 'closest',
                   xaxis=dict(dict(title=x_title,
                                   domain=[0.25, 1.0], anchor='y1')),
                   yaxis=dict(dict(domain=[0.0, 1.0], anchor='x1')))
fig = go.Figure(data = trace, layout = layout)
pyo.plot(fig)

### --------------------------------------------------------
### County
### --------------------------------------------------------
df4 = pd.pivot_table(df, values = 'quantity', index = 'contaminant', columns = 'County',
                     aggfunc = 'sum')


# draw horizontal bar charts of pollutants emitted by county
#df4.columns[0]
county = 'BRAZORIA'
overall_title = "Contaminants - " + county
x_title = "Quantities (lbs)"
#export_filename = "../6_communication/visuels/2018_type_site_pourcent_"+unit+".html"
### --------------------------------------------------------

b_df = df4[[county]].dropna().sort_values(by = [county], ascending = False)

trace= [go.Bar(
        y=b_df.index,
        x=b_df[county],
        orientation = 'h'
        )]
layout = go.Layout(title = overall_title, 
                   hovermode = 'closest',
                   xaxis=dict(dict(title=x_title,
                                   domain=[0.25, 1.0], anchor='y1')),
                   yaxis=dict(dict(domain=[0.0, 1.0], anchor='x1')))
fig = go.Figure(data = trace, layout = layout)
pyo.plot(fig)



"""
df['County'].nunique()
by_county = pd.DataFrame()
for c in df['County'].unique():
    new_column = df4[[c]].dropna()
    by_county = pd.merge(by_county, new_column, how = 'outer', left_index=True, right_index=True)
"""    
df5 = pd.pivot_table(df, values = 'quantity', index = 'County', columns = 'contaminant',
                     aggfunc = 'sum')

top10 = df5[[c for c in top_10_contaminants]]
for c in top_10_contaminants:
    new_column = df5[[c]].dropna()
    top10 = pd.merge(top10, new_column, how = 'outer', left_index=True, right_index=True)

trace= [go.Bar(
        y=df4.columns,
        x=df4['quantity'],
        orientation = 'h'
        )]
layout = go.Layout(title = overall_title, 
                   hovermode = 'closest',
                   xaxis=dict(dict(title=x_title,
                                   domain=[0.25, 1.0], anchor='y1')),
                   yaxis=dict(dict(domain=[0.0, 1.0], anchor='x1')))
fig = go.Figure(data = trace, layout = layout)
pyo.plot(fig)
