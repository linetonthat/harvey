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
path = "/Users/linetonthat/ds_training/projects/2019-05_Harvey_pollution/3_treated_data/"
df = pd.read_csv(path+"largest-emissions-in-lbs.csv")
df.info()

# ---------------------
# analyse data

# count the number of different data
df.nunique()

df['contaminant'].unique()
df['Type(s) of air emissions event'].unique()
# array(['AIR SHUTDOWN', 'AIR STARTUP', 'EMISSIONS EVENT'], dtype=object)
df['Type(s) of air emissions event'].value_counts()
"""
EMISSIONS EVENT    855
AIR STARTUP        341
AIR SHUTDOWN       259
"""
df['units'].unique()
#array(['lbs (est.)', 'lbs'], dtype=object)

sorted_df = df.sort_values(by = ['Regulated entity name', 'contaminant', 'Event began'])

# ---------------------
# assess no of contaminants per event
contaminant_by_event = df.groupby(by=['Regulated entity name',
                          'Event began',
                          'Event ended'])[['contaminant']].count()
contaminant_by_event.columns = ['No of contaminants per event']
#print(contaminant_by_event)

# assess number of events per plant
event_by_plant = contaminant_by_event.groupby(by=['Regulated entity name']).count()
event_by_plant.columns = ['No of events']
#print(event_by_plant.sort_values(by = ['No of events'], ascending = False))

# ---------------------
# create a summary dataframe
by_plant = event_by_plant.copy()
# ---------------------

# assess no of contaminants per plant
emissions_by_plant = df.groupby(by=['Regulated entity name',
                                      'contaminant'])[['contaminant']].count()
emissions_by_plant.columns = ['No of contaminant emissions per plant']
#print(emissions_by_plant)
# NB : The count is sometimes more than the number of events, as there could be
# several sources of emissions on site (a row corresponds to the emission of one source)


# assess number of contaminants per plant
contaminant_by_plant = emissions_by_plant.groupby(by=['Regulated entity name']).count()
contaminant_by_plant.columns = ['No of contaminants']
#print(event_by_plant.sort_values(by = ['No of contaminants'], ascending = False))
"""
Differences between:
Naphta and Naphtalene?
Unspeciated VOCs and VOcs (Unspeciated)
Ethylbenzene and ethyl benzene
PM and Particulate Matter
Oxides of Nitrogen (NOx) , NOX, Nitrogen Oxides
"""

# add the number of contaminants to the by_plant dataframe
by_plant = pd.merge(by_plant, contaminant_by_plant, left_index=True, right_index=True)
# ---------------------


# format data
df["Event began"] = pd.to_datetime(df["Event began"])
df["Event ended"] = pd.to_datetime(df["Event ended"], errors="coerce")

df['duration'] = df["Event ended"]  - df["Event began"]
# convert into number of days 
df['duration'] = df['duration']/ np.timedelta64(1,'D')
df['duration'].describe()

# WHAT TO DO WITH MISSING DATA RE DURACTION?

# Assess the period of events reported and selected
df['Event began'].min() # Timestamp('2017-08-24 06:40:00')
df['Event ended'].max() # Timestamp('2017-10-01 05:00:00')

# ---------------------
# assess duration per event
duration_by_event = df.groupby(by=['Regulated entity name',
                          'Event began',
                          'Event ended'])[['duration']].mean()
duration_by_event.columns = ['duration']
#print(duration_by_event)

# distribution of event duration
plt.figure(figsize=(10,6))
duration_by_event['duration'].hist(alpha=0.5,color='blue', bins=30)
plt.legend()
plt.xlabel('Duration of event (days)')

# assess average event duration per plant
duration_by_plant = duration_by_event.groupby(by=['Regulated entity name']).mean()
duration_by_plant.columns = ['Average duration']
#print(duration_by_plant.sort_values(by = ['Average duration'], ascending = False))

# add the average duration to the by_plant dataframe
by_plant = pd.merge(by_plant, duration_by_plant, left_index=True, right_index=True)

# export to CSV file
by_plant.to_csv(path+'by_plant.csv')


# ---------------------------------------------------------------------------
# bar chart


by_plant.info()
by_plant.sort_values(by = ['No of events', "Average duration"], ascending = False, inplace = True)

#export_filename =  "../6_communication/visuels/variations_consos_globales.html"
overall_title = 'Events and number of contaminants emitted per facility'

trace1 = go.Bar(
    x=by_plant.index,
    y=by_plant['No of events'],
    marker = dict(color = '#D35400'),
    name = "No of events"
)
trace2 = go.Bar(
    x=by_plant.index,
    y=by_plant['Average duration'],
    marker = dict(color = '#2980B9'),
    name = "Average duration"
)
trace3 = go.Bar(
    x=by_plant.index,
    y=by_plant['No of contaminants'],
    marker = dict(color = '#28B463'),
    name = "No of contaminants"
)

fig = tools.make_subplots(rows=3, cols=1)

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 2, 1)
fig.append_trace(trace3, 3, 1)

fig['layout'].update(title=overall_title)
pyo.plot(fig)
#pyo.plot(fig,filename = export_filename)


# ---------------------
# distribution of durations

plt.figure(figsize=(10,6))
df[df['Type(s) of air emissions event'] == 'AIR SHUTDOWN']['duration'].dropna().hist(alpha=0.5,color='blue', bins=10,label='AIR SHUTDOWN')
df[df['Type(s) of air emissions event'] == 'AIR STARTUP']['duration'].dropna().hist(alpha=0.5,color='red', bins=10,label='AIR STARTUP')
df[df['Type(s) of air emissions event'] == 'EMISSIONS EVENT']['duration'].dropna().hist(alpha=0.5,color='green', bins=10,label='EMISSIONS EVENT')
plt.legend()
plt.xlabel('Duration of event (days)')

import seaborn as sns
sns.set_style('darkgrid')
g = sns.FacetGrid(df.dropna(),hue="Type(s) of air emissions event",palette='coolwarm',size=6,aspect=2)
g = g.map(plt.hist,'duration',bins=10,alpha=0.7)


sns.heatmap(df[['Event ended']].dropna().isnull(),yticklabels=False,cbar=False,cmap='viridis')

sns.distplot(df['duration'].dropna(), bins = 10)


# ---------------------

hist_data = [df[df['Type(s) of air emissions event'] == 'AIR SHUTDOWN']['duration'].dropna(),
            df[df['Type(s) of air emissions event'] == 'AIR STARTUP']['duration'].dropna(),
            df[df['Type(s) of air emissions event'] == 'EMISSIONS EVENT']['duration'].dropna()]

group_labels = ['Group 1', 'Group 2', 'Group 3']
colors = ['#835AF1', '#7FA6EE', '#B8F7D4']

# Create distplot with curve_type set to 'normal'
fig = ff.create_distplot(hist_data, group_labels, colors=colors, show_curve=False)

# Add title
fig['layout'].update(title='Hist and Rug Plot')

# Plot!
pyo.plot(fig)