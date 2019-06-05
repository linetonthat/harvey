"""
What I've learned:
* defining a Viridis colorscale with custom number of items
* apply label encoder to display a specific color palette
* customize labels by concatenating several columns of a dataframe
* build a summary dataframe with different aggregation features (sum, count)
* display an horizontal bar chart
* offset the graph to give enough space for axis text
"""


import plotly.offline as pyo
import plotly.graph_objs as go
from plotly import tools


import pandas as pd
import numpy as np


# load data
path = "/Users/linetonthat/ds_training/projects/2019-05_Harvey_pollution/3_treated_data/"
df = pd.read_csv(path+"facilities-with-most-emissions-lbs.csv")
df.info()

# count the number of different counties
df['Regulated entity name'].nunique()

# provide a code for each county (used for colouring)
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(df['County'].unique())
df['County_color'] = le.transform(df['County'])

colour_list = [int(x) for x in np.linspace(0, 9, num = 10)]
county_list = list(le.inverse_transform(colour_list))


#color_list = df['County'].map(site_color)

### --------------------------------------------------------

overall_title = "Quantities of pollution emitted by facilities"
x_title = "Quantities (1000 lbs)"
#export_filename = "../6_communication/visuels/2018_type_site_pourcent_"+unit+".html"
### --------------------------------------------------------

trace= [go.Bar(
        y=df['Regulated entity name'],
        x=df['quantity_1000s'],
        marker = dict(
                    cmax = 9,
                    cmin = 0,
                    color=df['County_color'] ,
                    colorbar = dict(
                                    title = 'County',
                                    titleside = 'top',
                                    tickmode = 'array',
                                    tickvals = colour_list,
                                    ticktext = county_list,
                                    ticks = 'outside'
                                ),
                    colorscale='Viridis'
                ),
        text = df['quantity_1000s'].apply(str) + ' - ' + df['County'],
        hoverinfo = 'text',            
        #textposition = 'auto',
        textfont = dict(
                size = 14
                ),
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



"""
cited in the article
Port Arthur refinery run by Total Petrochemicals & Refining USA
Harris County, the Galena Park Terminal
Many of the reports mentioned emissions caused by rain damage to the “floating roofs” that typically cover petroleum tanks.
"""

### --------------------------------------------------------

# Analysis by county
byCounty = df.groupby(by=['County']).sum()[['quantity_1000s']].sort_values(by='quantity_1000s', ascending = False)
df.groupby(by=['County'])['quantity_1000s'].count()
byCounty['Count'] = df['County'].value_counts()

byCounty['County_color'] = le.transform(byCounty.index)

# show quantities per county
overall_title = "Counties with most emissions"

trace1 = go.Bar(
            x=byCounty.index,
            y=byCounty['quantity_1000s'],
            marker = dict(
                        cmax = 9,
                        cmin = 0,
                        color=byCounty['County_color'],
                        colorscale='Viridis',
                        ),
            name = 'quantity_1000s'
    )
trace2 = go.Bar(
            x=byCounty.index,
            y=byCounty['Count'],
            marker = dict(color = "#AAB7B8"),
            name = 'Count'
    )
fig = tools.make_subplots(rows=2, cols=1)

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 2, 1)

# define layout
fig['layout'].update(title = overall_title, 
              showlegend=False,
                       yaxis1=dict(dict(title="Quantities of pollution (lbs)")),  
                       yaxis2=dict(dict(title="Count of facilities")))

pyo.plot(fig)
#pyo.plot(fig,filename = export_filename)
