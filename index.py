import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from newapp import App
from about import AboutPage

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

server = app.server

app.config.suppress_callback_exceptions = True
#The above is simply for interactive layouts, can probably remove it

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return App()
    elif pathname == '/about':
        return AboutPage()

if __name__ == '__main__':
    app.run_server(debug=True)