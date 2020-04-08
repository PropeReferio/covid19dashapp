import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import plotly
import plotly.graph_objects as go
from plotly.colors import n_colors
from pandas import DataFrame as df
import pandas as pd
import numpy as np
import flask


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
        if frame.iloc[i]['Percent Change'] >= 0:
            colors.append(int(frame.iloc[i]['Percent Change']//10)+10)
        else:
            colors.append(int(frame.iloc[i]['Percent Change']//-10))
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
#Add table colors before adding percent sign:

gt_colors = trend_colors(global_trends)
global_trends['Percent Change'] = global_trends['Percent Change'].astype(str) + '%'
flattening_curve = confirmed[confirmed[latest_date]>1000].sort_values(by=['Percent Change'])[['Name','Percent Change']]
##flattening_curve = flattening_curve[(flattening_curve['Percent Change']<100) & (flattening_curve['Percent Change']>-100)]
# The line above only shows percent changes between 100% and -100%   I think this isn't being used anywhere
conf_recov = confirmed.join(recovered.set_index('Name')[latest_date],
on=['Name'], rsuffix='_recoveries').sort_values(by=latest_date,
ascending=False)
conf_pop = confirmed.join(global_pop.set_index('Country')['Population'],
on=['Name']).sort_values(by=latest_date, ascending=False)
conf_pop['Percent Infected'] = round(conf_pop[latest_date]/conf_pop['Population']*100, 3)
conf_pop = conf_pop[conf_pop['Percent Infected'] > 0]
conf_pop['Percent Infected'] = conf_pop['Percent Infected'].astype(str) + '%'
# df['Percent'] = df['Grade'].astype(str) + '%'
us_only_conf = confirmed[confirmed['Name'] == 'US']
us_only_deaths = deaths[deaths['Name'] == 'US']

fig2 = go.Figure(data=[go.Table(
    header=dict(values=['<b>Country/Region</b>','<b>Confirmed Cases</b>',
     '<b>Recoveries</b>', '<b>% of Total Population Infected</b>'],
                line_color='darkslategray',
                fill_color='rgb(46, 162, 190)',
                align='center',
                font=dict(color='black', size=28)),
    cells=dict(values=[conf_recov['Name'],
                       conf_recov[latest_date], # 1st column
                       conf_recov[latest_date+'_recoveries'],
                       conf_pop['Percent Infected']],
               line_color='darkslategray',
               fill_color=['lightcyan','lightcyan','lightcyan','lightcyan'],
               align='center',
               font=dict(color='black', size=20),
               height=30,
               ))
])
fig2.update_layout(height=600)
#Figure of Percent change in new cases by Nation
fig3 = go.Figure(data=[go.Table(
    header=dict(values=['<b>Country</b>','<b>Confirmed Cases</b>',
    '<b>% Change of New Daily Cases</b>'],
                line_color='darkslategray',
                fill_color='rgb(46, 162, 190)',
                align='center',
                font=dict(color='black', size=28)),
    cells=dict(values=[global_trends['Name'],
                       global_trends.iloc[:,-1],
                       global_trends['Percent Change']],
               line_color='darkslategray',
               fill_color=['lightcyan','lightcyan',
               np.array(all_colors)[gt_colors]],
               align='center',
               font=dict(color='black', size=20),
               height=30))])

fig3.update_layout(height=600, plot_bgcolor='lightcyan')
#Figure of Percent change in new cases by State
fig4 = go.Figure(data=[go.Table(
    header=dict(values=['<b>State</b>','<b>Confirmed Cases</b>',
    '<b>% Change of New Daily Cases</b>'],
                line_color='darkslategray',
                fill_color='rgb(46, 162, 190)',
                align='center',
                font=dict(color='black', size=28)),
    cells=dict(values=[state_trend['State'],
                       state_trend.iloc[:,-1],
                       state_trend['Percent Change']], # 2nd column
               line_color='darkslategray',
               fill_color=['lightcyan','lightcyan','lightcyan'],
            #    np.array(all_colors)[st_colors]], Index error
               align='center',
               font=dict(color='black', size=20),
               height=30))])

fig4.update_layout(height=600)

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
    autosize=False,
    width=1800,
    height=1200,
    margin=dict(
        l=4,
        r=0,
        b=80,
        t=30,
        pad=4
    ),
    title_text='Confirmed Cases by State',
    title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        },
    titlefont=dict(
        family='Montserrat',
        size=50,
        color='#7f7f7f'
    ),
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='rgb(255, 255, 255)'),
)

nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Logo", active=True, href="#")),
        dbc.NavItem(dbc.NavLink("Data", href="#")),
        dbc.NavItem(dbc.NavLink("About", href="/about/")),
        dbc.NavItem(dbc.NavLink("Donate(Button)", href="#"))
    ], style={'font-family': 'Montserrat, arial, sans-serif'}
)

banner = html.Div(
    [
        html.P(
            "COVID Live Tracking Tool, Project developed in partnership between Cloudcafe Technologies and Coding Temple",
            className="lead"
        )
    ], className="banner"
)


server = flask.Flask(__name__)
app = dash.Dash(name=__name__, server=server, url_base_pathname='/',
external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(children=[
    nav, 
    banner,
    #Global Card Start
    html.Div(children=[
        html.Div(children=[
            html.Img(src=app.get_asset_url('global_300x300.jpg')),
            html.Div([
                html.H5('Global Data'),
                html.Div(children=[
                    html.H4(children=['Confirmed Cases: ',
                    format(confirmed[latest_date].sum(), ',d')]
                    ),
                    html.H4(children=[
                    'New today: ',
                    format(confirmed.iloc[:,-1].sum() - confirmed.iloc[:,-2].sum(), ',d'),
                    ])
                ]),
                html.Div(children=[
                    html.H4(children=['Deaths: ', 
                    format(deaths[latest_date].sum(), ',d')]
                    ),
                    html.H4(children=[
                    'New today: ',
                    format(deaths.iloc[:,-1].sum() - deaths.iloc[:,-2].sum(), ',d'),
                    ],
                    )
                    ])
                ],
                className='container')],
            className='card'),
        #Global Card End
        #US Card Start
        html.Div(children=[
            html.Img(src=app.get_asset_url('usa_flag_300x300.jpg')),
            html.Div([
                html.H5('US Data'),
                html.Div(children=[
                    html.H4(children=['Confirmed Cases: ',
                    format(us_only_conf.iloc[0,-1], ',d')],
                    ),
                    html.H4(children=[
                    'New today: ',
                    format(us_only_conf.iloc[0,-1] - us_only_conf.iloc[0,-2], ',d'),
                    ],
                    )
                    ]),
                html.Div(children=[
                    html.H4(children=['Deaths: ', 
                    format(us_only_deaths.iloc[0,-1], ',d')],
                    ),
                    html.H4(children=[
                    'New today: ',
                    format(us_only_deaths.iloc[0,-1] - us_only_deaths.iloc[0,-2], ',d'),
                    ],
                    )])
                ], className='container')
            ], className='card'
            ),
        #US Card End
    ], className='row justify-content-center'),
    dcc.Graph(id='COVID-19 Map',
            figure=fig),
    html.H3('Percentage of Populations Infected by Country'),
    dcc.Graph(figure=fig2),
    html.H3('Percentage Change in New Daily Cases by Country'),
    dcc.Graph(figure=fig3),
    html.H3('Percentage of Populations Infected by US State'),
    dcc.Graph(figure=fig4),
    html.Div(children='Footer', className='footer'),
])
@server.route('/about/')
def about():
    return '''
<html>
<h1>Fundraiser: Supplying PPE for Frontline Healthcare Professionals</h1>
<h3>Overview</h3>
<p>Our teams at Cloudcafe and Coding Temple are raising funds here to donate directly to the following campaign: <a href="https://www.gofundme.com/f/ppe-for-frontline-healthcare-professionals" target="_blank" rel="noopener">PPE for Frontline Healthcare Professionals</a>.</p>
<p>This fundraiser has been organized by Sonny Tai, the CEO of&nbsp;<a href="https://actuate.ai/" target="_blank" rel="noopener">Actuate AI</a>. Sonny is a former Marine and University of Chicago Booth grad. He describes his mission for his fundraiser as the following:</p>
<blockquote>
<p>"Healthcare workers are the front line fighters against the COVID-19 pandemic. However, they are now facing desperate shortages of Personal Protective Equipment (PPE) nationwide.</p>
<p>President John F. Kennedy famously said: "Ask not what your country can do for you, ask what you can do for your country". My friends - if there was ever a point in our lifetimes that required national mobilization, for every single American to do their part, that time is now. Our actions may be small and insignificant, but seemingly small and insignificant efforts multiplied by 320 million can move mountains.</p>
<p>We are a team of regular, passionate Americans who believe that we can help to move mountains. We may not be doctors and nurses, but we've heard the outcry from healthcare professionals across the country, and they've made it quite clear what they need."</p>
</blockquote>
<h3>Plan of Action</h3>
<p>1. Identify and collect quotes from suppliers that can manufacture high quality N-95 masks and ship to the United States in a cost-effective manner. <strong>Sonny's team has identified a primary supplier and will be placing their first order on Monday, April 13th.</strong></p>
<p>2. Identify hospitals that have the most urgent need for PPE. One of the resources we will use to identify these hospitals is the list from #GetUsPPE.org. <strong>Sonny's team has coordinated with multiple hospitals who are in urgent need and they will receive N95 masks from this initial order.</strong></p>
<p>3. Purchase the PPE and ship it to the hospitals. <strong>First shipment order is being placed this Monday, April 13th.&nbsp;</strong></p>
<p><span style="text-decoration: underline;">The fundraiser operates completely on a non-profit basis and is committed to complete transparency, which means that: </span></p>
<p>1. We will track spending and upload invoices for all of our purchases, and any left over funds will be donated to a to-be-designated 501(c)3 charity that helps those impacted by COVID-19.</p>
<p>2. None of us who are involved in this campaign will draw a salary from the campaign or appropriate any of its funds for personal use.</p>
<p>3. The email addresses, phone numbers, and LinkedIn profiles for all of the campaign's organizers will be posted on the GoFundMe to ensure accountability.</p>
<p>&nbsp;</p>
</html>
'''

# if __name__ == "__main__":
#     app.run_server(debug=True)

if __name__ == "__main__":
    server.run() # turned off debug=True to see if pages would load automatically
    #in navigation