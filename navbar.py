import dash_html_components as html
import dash_bootstrap_components as dbc

def Navbar():
    navbar = html.Div(
        [
        html.Ul(
            [
                html.Li(html.A("Data", href='/')),
                html.Li(html.A('About', href='/about')),
                html.Li(html.A('Donate', href="https://cloudcafe.io/covid-19-fundraiser"))
            ],
        )
        ],
    className='nav')
    
    
    
    
    # dbc.Nav(
    # [
    #     dbc.NavItem(dbc.NavLink("Data", href="/")),
    #     dbc.NavItem(dbc.NavLink("About", href="/about")),
    #     dbc.NavItem(dbc.NavLink("Donate", href="https://cloudcafe.io/covid-19-fundraiser"))
    # ], style={'font-family': 'Montserrat, arial, sans-serif'}
    # )
        
    return navbar