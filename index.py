import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from newapp import App
from about import AboutPage
from banner import Banner
from navbar import Navbar

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED, "https://fonts.googleapis.com/css2?family=Montserrat&display=swap"],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'}])

server = app.server

def Logo():
    logo = html.Div(
        [
        html.A(
            href='https://cloudcafe.io/skorboard-bi',
            children=[
                html.Img(src=app.get_asset_url('logo.png'))
            ]
        ),
        html.P('     COVID-19 Dashboard')
        ],
        className='logo-banner')
    return logo

logo = Logo()
banner = Banner()
navbar = Navbar()

app.config.suppress_callback_exceptions = True
#The above is simply for interactive layouts, can probably remove it

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    logo,
    navbar,
    html.Div(id = 'page-content'),
    banner
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return App()
    elif pathname == '/about':
        return AboutPage()

if __name__ == '__main__':
    app.run_server()