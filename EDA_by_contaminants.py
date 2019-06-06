# import libraries
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

import plotly.offline as pyo
import plotly.graph_objs as go
from plotly import tools
import plotly.figure_factory as ff



# load data
path = "/Users/linetonthat/ds_training/projects/2019-06_Harvey_pollution/3_treated_data/"
df = pd.read_csv(path+"largest-emissions-in-lbs.csv")
df.info()

#df.columns
#df['limit'].unique()

#sorted_df = df.sort_values(by = ['contaminant', 'Regulated entity name', 'Event began'])

"""
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
"""
# load categorised list of contaminants
df_conta = pd.read_csv(path+"../4_analyses/contaminants/list_of_contaminants_v2.csv", sep = ";")
drop_question = lambda x: x.replace("?",'')
df_conta['category'] = df_conta['category'].apply(drop_question)
#df_conta.info()

# add the category column to the main dataframe
df = pd.merge(df,df_conta[['contaminant','category']], on = ['contaminant'])

# ---------------------
# assess quantities per contaminant type
df2 = df.groupby(by=['category'])[['quantity']].sum()
df2.columns = ['quantity']
df2.sort_values(by = ['quantity'], ascending = False, inplace = True)

# draw horizontal bar charts of main pollutants emitted
overall_title = "Harvey-related emission from the chemical plants"
x_title = "Quantities (lbs)"
export_filename = path+"../6_communication/plots/by_contaminant_summary.html"
### --------------------------------------------------------

trace= [go.Bar(
        y=df2.index,
        x=df2['quantity'],
        orientation = 'h'
        )]
layout = go.Layout(title = overall_title, 
                   hovermode = 'closest',
                   xaxis=dict(dict(title=x_title,
                                   domain=[0.25, 1.0], anchor='y1')),
                   yaxis=dict(dict(domain=[0.0, 1.0], anchor='x1')))
fig = go.Figure(data = trace, layout = layout)
pyo.plot(fig,filename =  export_filename)
#pyo.plot(fig,filename = export_filename)
### --------------------------------------------------------
#top_10_contaminants = list(df2.head(10).index)

### --------------------------------------------------------
### Regulated entity name
### --------------------------------------------------------
# assess quantities per contaminant type and per facility
"""
df3 = df.groupby(by=['contaminant', 'Regulated entity name'])[['quantity']].sum()
df3 = df3.unstack()
df3 = df3.fillna(0)
"""
df3 = pd.pivot_table(df, values = 'quantity', index = 'category', columns = 'Regulated entity name',
                     aggfunc = 'sum')


# draw horizontal bar charts of pollutants emitted by facility
#df3.columns[1]
#facility = 'BASF BEAUMONT AGRO PLANT'
facility = 'ARKEMA CROSBY PLANT'

for facility in df3.columns:
    ### --------------------------------------------------------
    overall_title = "Contaminants - "+ facility
    x_title = "Quantities (lbs)"
    export_filename = path+"../6_communication/plots/by_contaminant_facility_"+facility+".html"
    ### --------------------------------------------------------
    # select only emitted contaminants to be displayed
    b_df = df3[[facility]].dropna().sort_values(by = [facility], ascending = False)
    ### --------------------------------------------------------
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
    pyo.plot(fig,filename =  export_filename)

### --------------------------------------------------------
### County
### --------------------------------------------------------
# assess quantities per contaminant type and per county
df4 = pd.pivot_table(df, values = 'quantity', index = 'category', columns = 'County',
                     aggfunc = 'sum')


# draw horizontal bar charts of pollutants emitted by county
#df4.columns[0]
county = 'BRAZORIA'
overall_title = "Contaminants - " + county
x_title = "Quantities (lbs)"
#export_filename = "../6_communication/visuels/2018_type_site_pourcent_"+unit+".html"
### --------------------------------------------------------
# select only emitted contaminants to be displayed
b_df = df4[[county]].dropna().sort_values(by = [county], ascending = False)
### --------------------------------------------------------
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

# extract only values from top 10 contaminants
top10 = df5[[c for c in top_10_contaminants]]
#top10.columns[0]]
i = 0
c = top_10_contaminants[i]
overall_title = c
trace= [go.Bar(
        x=top10.index,
        y=top10[c],
        )]
"""
TO BE REVIEWED FOR LAYOUT DEFINITION
    go.Layout = [title = overall_title,
                       yaxis=dict(dict(title="Quantities of pollution (lbs)"))]
fig = go.Figure(data = trace, layout = layout)
pyo.plot(fig)
"""

### --------------------------------------------------------
### Main contributors - facilities
### --------------------------------------------------------
df2c = pd.pivot_table(df, values = 'quantity', index = 'Regulated entity name', columns = 'category',
                     aggfunc = 'sum')

# draw horizontal bar chart of selected contaminant by facility
#contaminant = 'Carbon Monoxide'
#contaminant = 'Hydrocarbons'
contaminant = 'Sulfur dioxide'
overall_title = "Contaminants - " + contaminant
x_title = "Quantities (lbs)"
export_filename = path+"../6_communication/plots/contribution_facility_"+contaminant+"_summary.html"
### --------------------------------------------------------
# sort values to be displayed (descending order)
b_df = df2c[[contaminant]].dropna().sort_values(by = [contaminant], ascending = False)
### --------------------------------------------------------
trace= [go.Bar(
        y=b_df.index,
        x=b_df[contaminant],
        orientation = 'h'
        )]
layout = go.Layout(title = overall_title, 
                   hovermode = 'closest',
                   xaxis=dict(dict(title=x_title,
                                   domain=[0.25, 1.0], anchor='y1')),
                   yaxis=dict(dict(domain=[0.0, 1.0], anchor='x1')))
fig = go.Figure(data = trace, layout = layout)
pyo.plot(fig, filename =  export_filename)

# make the list of main emitting facilities (by changing the contaminant variable)
b_df[contaminant].sum()
most_emitting_facilities = list(b_df[contaminant].iloc[:5].index)
most_emitting_facilities += list(b_df[contaminant].iloc[:5].index)
df_most_emitting_facilities  = pd.DataFrame(most_emitting_facilities)
df_most_emitting_facilities.drop_duplicates(inplace = True)
#del df_most_emitting_facilities['County']
df_most_emitting_facilities.columns = ['Regulated entity name']
df_most_emitting_facilities.sort_values(by='County', inplace = True)
#df_most_emitting_facilities = pd.merge(df_most_emitting_facilities,df[['Regulated entity name','County']].groupby(by = ['Regulated entity name']), how = 'inner', on = ['Regulated entity name'])
df_most_emitting_facilities.to_csv(path+"most_emitting_facilities.csv")
df_most_emitting_facilities['County'].unique()
# array(['BRAZORIA', 'HARRIS', 'JEFFERSON', 'NUECES'], dtype=object)
"""
'Carbon Monoxide'
b_df[contaminant].sum(): 1993715.7523000001
b_df[contaminant].iloc[:5].sum() : 1269686.0
5 plants account for 63.4% of carbon monoxide emissions
Regulated entity name
FLINT HILLS RESOURCES PORT ARTHUR FACILITY               390000.0
CHEVRON PHILLIPS CHEMICAL CEDAR BAYOU PLANT              364966.0
VALERO PORT ARTHUR REFINERY                              191900.0
EQUISTAR CORPUS CHRISTI PLANT                            166000.0
CHEVRON PHILLIPS CHEMICAL SWEENY OLD OCEAN FACILITIES    156820.0
Name: Carbon Monoxide, dtype: float64
"""

"""
'Hydrocarbons'
total: 1611702.4644000002
b_df[contaminant].iloc[:5].sum() :1152103.4822
5 plants account for 71.5% of hydrocarbons emissions
Regulated entity name
FLINT HILLS RESOURCES PORT ARTHUR FACILITY               477500.0000
CHEVRON PHILLIPS CHEMICAL CEDAR BAYOU PLANT              261928.0000
PASADENA TERMINAL                                        147734.3922
CHOCOLATE BAYOU PLANT                                    133759.7400
CHEVRON PHILLIPS CHEMICAL SWEENY OLD OCEAN FACILITIES    131181.3500
Name: Hydrocarbons, dtype: float64
"""

"""
'Sulfur dioxide'
total: 636503.4752000001
b_df[contaminant].iloc[:5].sum() : 539394.42020000005
5 plants account for 84.7% of sulfur dioxide emissions
Regulated entity name
EXXON MOBIL BAYTOWN REFINERY                                 216934.3002
VALERO PORT ARTHUR REFINERY                                  147172.7200
TOTAL PETRO CHEMICALS & REFINING USA PORT ARTHUR REFINERY     67000.0000
FHR CORPUS CHRISTI WEST PLANT                                 60621.4000
SWEENY REFINERY                                               47666.0000
Name: Sulfur dioxide, dtype: float64
"""

### --------------------------------------------------------
### Main contributors - county
### --------------------------------------------------------
df4c = pd.pivot_table(df, values = 'quantity', index = 'County', columns = 'category',
                     aggfunc = 'sum')

# draw horizontal bar chart of selected contaminant by county
#contaminant = 'Carbon Monoxide'
#contaminant = 'Hydrocarbons'
contaminant = 'Sulfur dioxide'
overall_title = "Contaminants - " + contaminant
x_title = "Quantities (lbs)"
export_filename = path+"../6_communication/plots/contribution_county_"+contaminant+"_summary.html"
### --------------------------------------------------------
# sort values to be displayed (descending order)
b_df = df4c[[contaminant]].dropna().sort_values(by = [contaminant], ascending = False)
### --------------------------------------------------------
trace= [go.Bar(
        y=b_df.index,
        x=b_df[contaminant],
        orientation = 'h'
        )]
layout = go.Layout(title = overall_title, 
                   hovermode = 'closest',
                   xaxis=dict(dict(title=x_title,
                                   domain=[0.25, 1.0], anchor='y1')),
                   yaxis=dict(dict(domain=[0.0, 1.0], anchor='x1')))
fig = go.Figure(data = trace, layout = layout)
pyo.plot(fig, filename =  export_filename)

# make the list of main emitting facilities (by changing the contaminant variable)
b_df[contaminant].sum()
most_emitting_counties = list(b_df[contaminant].iloc[:5].index)
most_emitting_counties += list(b_df[contaminant].iloc[:5].index)
df_most_emitting_counties  = pd.DataFrame(most_emitting_counties)
df_most_emitting_counties.drop_duplicates(inplace = True)
#del df_most_emitting_counties['County']
df_most_emitting_counties.columns = ['County']
#df_most_emitting_counties = pd.merge(df_most_emitting_counties,df[['Regulated entity name','County']].groupby(by = ['Regulated entity name']), how = 'inner', on = ['Regulated entity name'])
df_most_emitting_counties.to_csv(path+"most_emitting_counties.csv")
df_most_emitting_counties['County'].unique()
# array(['JEFFERSON', 'HARRIS', 'BRAZORIA', 'NUECES', 'GALVESTON'], dtype=object)

# main locations where highest number of plants