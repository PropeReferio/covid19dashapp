import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output
import plotly
import plotly.graph_objects as go
from plotly.colors import n_colors
from pandas import DataFrame as df
import pandas as pd
import numpy as np


#These are CSVs turned Pandas Dataframes
confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
global_pop = pd.read_csv('population_by_country_2020.csv')
latest_date = confirmed.columns[-1]



def names_column(frame):
    lst = []
    '''Makes a new column called 'Name' '''
    for i in range(len(frame)):
        if type(frame['Province/State'][i]) is str:
            lst.append(frame['Province/State'][i])
        else:
            lst.append(frame['Country/Region'][i])
    frame.insert(0, 'Name', lst)

names_column(confirmed)
names_column(deaths)
names_column(recovered)

#Colors by gradation for table values
colors_flat = n_colors('rgb(168, 234, 250)', 'rgb(0, 68, 85)', 10, colortype='rgb')
colors_steep = n_colors('rgb(255, 200, 200)', 'rgb(200, 0, 0)', 10, colortype='rgb')
all_colors = colors_flat + colors_steep

def trend_colors(frame):
    '''Makes a list of indices that correspond to colors in all_colors
    which apply to tables'''
    colors = []
    for i in range(len(frame)):
        if frame.iloc[i]['Percent Change'] == -100:
            colors.append(9)
        elif frame.iloc[i]['Percent Change'] >= 0:
            value = int(frame.iloc[i]['Percent Change']//10)+10
            if value <= 19:
                colors.append(value)
            else:
                colors.append(19)
        else:
            value = int(frame.iloc[i]['Percent Change']//-10)
            if value <= 9:
                colors.append(value)
            else:
                colors.append(9)
    return colors

# State Data Cleaning Starts
state_conf = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
state_deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')
state_list = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

clean_state_deaths = pd.DataFrame(columns=['State', state_deaths.columns[-1]])
for state in state_list:
    new_row = {'State': state,
               state_deaths.columns[-1]: state_deaths[state_deaths['Province_State'] == state].iloc[:,-1].sum()}
    clean_state_deaths = clean_state_deaths.append(new_row, ignore_index=True)
state_text = [clean_state_deaths['State'][i] + '<br>' + str(clean_state_deaths.iloc[i][-1]) + ' Deaths' for i in range(50)]
# Above is the text that goes into the map tooltip

state_codes = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

clean_state_conf = pd.DataFrame(columns=['State',state_conf.columns[-3],
state_conf.columns[-2], state_conf.columns[-1]])
for state in state_list:
    new_row = {'State': state,
               state_conf.columns[-3]: state_conf[state_conf['Province_State'] == state].iloc[:,-3].sum(),
               state_conf.columns[-2]: state_conf[state_conf['Province_State'] == state].iloc[:,-2].sum(),
               state_conf.columns[-1]: state_conf[state_conf['Province_State'] == state].iloc[:,-1].sum()}
    clean_state_conf = clean_state_conf.append(new_row, ignore_index=True)

clean_state_conf.insert(0, 'new_latest', clean_state_conf.iloc[:,-1] - clean_state_conf.iloc[:,-2])
clean_state_conf.insert(0, 'new_second_latest', clean_state_conf.iloc[:,-2] - clean_state_conf.iloc[:,-3])
state_map = clean_state_conf # Data for MAP is cleaned no further beyond this line.
state_trend = clean_state_conf[clean_state_conf['new_second_latest'] > 0]
state_trend[latest_date] = state_trend.apply(lambda x: "{:,}".format(x[latest_date]), axis=1)
state_trend.insert(0, 'Percent Change', (state_trend['new_latest'] / state_trend['new_second_latest'] - 1) * 100)
state_trend = state_trend.sort_values(by=['Percent Change'])
st_colors = trend_colors(state_trend)

# Round here
state_trend['Percent Change'] = [str(round(state_trend.iloc[i]['Percent Change'], 1)) + '%' for i in range(len(state_trend))]
#State Data Cleaning Ends

def new_cases_columns(frame): #Makes 2 columns of new cases
    new_yest = frame.iloc[:,-1] - frame.iloc[:,-2]
    new_2_ago = frame.iloc[:,-2] - frame.iloc[:,-3]
    frame.insert(0, 'new_yest', new_yest) #Could change names to latest and 2nd latest,
    frame.insert(0, 'new_2_ago', new_2_ago) #but seems prone to causing errors.
# A list comprehension like on the line below may be the key to rounding values
    frame.insert(0, 'Percent Change', [round((confirmed.iloc[i]['new_yest'] / confirmed.iloc[i]['new_2_ago'] - 1)*100, 1) for i in range(len(confirmed))])


new_cases_columns(confirmed)
new_cases_columns(deaths)
global_trends = confirmed[confirmed[latest_date] > 1000][['Name', 'Percent Change', latest_date]].dropna().sort_values(by='Percent Change')
global_trends = global_trends[global_trends['Percent Change'].between(-100,100, inclusive=False)]
#This adds commas to data
global_trends[latest_date] = global_trends.apply(lambda x: "{:,}".format(x[latest_date]), axis=1)
#Add table colors before adding percent sign:

gt_colors = trend_colors(global_trends)
global_trends['Percent Change'] = global_trends['Percent Change'].astype(str) + '%'
flattening_curve = confirmed[confirmed[latest_date]>1000].sort_values(by=['Percent Change'])[['Name','Percent Change']]
#This adds commas to data: 
recovered[latest_date] = recovered.apply(lambda x: "{:,}".format(x[latest_date]), axis=1)
conf_recov = confirmed.join(recovered.set_index('Name')[latest_date],
on=['Name'], rsuffix='_recoveries').sort_values(by=latest_date,
ascending=False)
#This adds commas to data: 
conf_recov[latest_date] = conf_recov.apply(lambda x: "{:,}".format(x[latest_date]), axis=1)
# conf_recov[latest_date+'_recoveries'] = conf_recov.apply(lambda x: "{:,}".format(x[latest_date+'_recoveries']), axis=1)
conf_pop = confirmed.join(global_pop.set_index('Country')['Population'],
on=['Name']).sort_values(by=latest_date, ascending=False)
conf_pop['Percent Infected'] = round(conf_pop[latest_date]/conf_pop['Population']*100, 3)
conf_pop = conf_pop[conf_pop['Percent Infected'] > 0]
conf_pop['Percent Infected'] = conf_pop['Percent Infected'].astype(str) + '%'
# df['Percent'] = df['Grade'].astype(str) + '%'
us_only_conf = confirmed[confirmed['Name'] == 'US']
us_only_deaths = deaths[deaths['Name'] == 'US']

#US Chloropleth Map a
fig = go.Figure(data=go.Choropleth(
    locations=state_codes,
    z=state_map[latest_date].astype(float), # The column that color codes
    locationmode='USA-states',
    colorscale='Reds',
    autocolorscale=False,
    text=state_text, # hover text... Tried to put state names here, but 
    #2 letter state codes remain, which is awkward
    marker_line_color='black', # line markers between states
    colorbar_title="Confirmed Cases"
))

fig.update_layout(
    autosize=True,
    # width=1800,
    # height=1200,
    margin=dict(
        l=4,
        r=0,
        b=80,
        t=30,
        pad=4
    ),
    title_text='Confirmed Cases by State',
    title={
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        },
    titlefont=dict(
        family='Montserrat',
        size=26,
        color='#7f7f7f'
    ),
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='rgb(255, 255, 255)'),
)

fig2 = go.Figure(data=[go.Table(
    header=dict(values=['<b>Country/Region</b>','<b>Confirmed Cases</b>',
     '<b>Recoveries</b>', '<b>% of Total Population Infected</b>'],
                line_color='darkslategray',
                fill_color='rgb(46, 162, 190)',
                align='center',
                font=dict(family='Montserrat', color='black', size=16)),
    cells=dict(values=[conf_recov['Name'],
                       conf_recov[latest_date], # 1st column
                       conf_recov[latest_date+'_recoveries'],
                       conf_pop['Percent Infected']],
               line_color='darkslategray',
               fill_color=['lightcyan','lightcyan','lightcyan','lightcyan'],
               align='center',
               font=dict(family='Montserrat', color='black', size=20),
               height=30,
               ))
])
fig2.update_layout(
    height=600,
    margin=dict(l=0, r=0, t=10, b=30),
    )
#Figure of Percent change in new cases by Nation
fig3 = go.Figure(data=[go.Table(
    header=dict(values=['<b>Country/Region</b>','<b>Confirmed Cases</b>',
    '<b>% Change of New Daily Cases</b>'],
                line_color='darkslategray',
                fill_color='rgb(46, 162, 190)',
                align='center',
                font=dict(family='Montserrat', color='black', size=16)),
    cells=dict(values=[global_trends['Name'],
                       global_trends.iloc[:,-1],
                       global_trends['Percent Change']],
               line_color='darkslategray',
               fill_color=['lightcyan','lightcyan',
               np.array(all_colors)[gt_colors]],
               align='center',
               font=dict(family='Montserrat', color='black', size=20),
               height=30))])

fig3.update_layout(height=600,
                   margin=dict(l=0, r=0, t=10, b=30),
                   plot_bgcolor='lightcyan')
#Figure of Percent change in new cases by State
fig4 = go.Figure(data=[go.Table(
    header=dict(values=['<b>State</b>','<b>Confirmed Cases</b>',
    '<b>% Change of New Daily Cases</b>'],
                line_color='darkslategray',
                fill_color='rgb(46, 162, 190)',
                align='center',
                font=dict(family='Montserrat', color='black', size=16)),
    cells=dict(values=[state_trend['State'],
                       state_trend.iloc[:,-1],
                       state_trend['Percent Change']], # 2nd column
               line_color='darkslategray',
               fill_color=['lightcyan','lightcyan',
               np.array(all_colors)[st_colors]],
               align='center',
               font=dict(family='Montserrat', color='black', size=20),
               height=30))])

fig4.update_layout(height=600,
                   margin=dict(l=0, r=0, t=10, b=30),
                )

def App():
    layout = html.Div(children=[ # was app.layout
        html.Div([
        #Cards Start
            html.Div(children=[
            #Card 1
                    html.H4('Global Confirmed Cases: '),
                    html.H3(format(confirmed[latest_date].sum(), ',d')),
                    html.H4('New today: '),
                    html.H3(format(confirmed.iloc[:,-1].sum() - confirmed.iloc[:,-2].sum(), ',d')),
                    ],
            className='card'),
            html.Div(children=[
            #Card 2
                    html.H4('Global Deaths: '),
                    html.H3(format(deaths[latest_date].sum(), ',d')),
                    html.H4('New today: '),
                    html.H3(format(deaths.iloc[:,-1].sum() - deaths.iloc[:,-2].sum(), ',d'))
                    ],
            className='card'),
            html.Div(children=[
            #Card 3
                    html.H4('US Confirmed Cases: '),
                    html.H3(format(us_only_conf.iloc[0,-1], ',d')),
                    html.H4('New today: '),
                    html.H3(format(us_only_conf.iloc[0,-1] - us_only_conf.iloc[0,-2], ',d')),
                    ],
            className='card'),
            html.Div(children=[
            #Card 4
                    html.H4('US Deaths: '),
                    html.H3(format(us_only_deaths.iloc[0,-1], ',d')),
                    html.H4('New today: '),
                    html.H3(format(us_only_deaths.iloc[0,-1] - us_only_deaths.iloc[0,-2], ',d')),
                    ],
            className='card'),
            ], className='row justify-content-center card-wrapper'),
    #End all Cards

    dcc.Graph(id='COVID-19 Map',
            figure=fig),
    html.H3('Percentage of Populations Infected by Country'),
    dcc.Graph(figure=fig2),
    html.H3('Percentage Change in New Daily Cases by Country'),
    dcc.Graph(figure=fig3),
    html.H3('Percentage of Populations Infected by US State'),
    dcc.Graph(figure=fig4),
    ])

    return layout