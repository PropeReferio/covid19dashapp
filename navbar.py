import dash_bootstrap_components as dbc


def Navbar():
    navbar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Data", href="/")),
        dbc.NavItem(dbc.NavLink("About", href="/about")),
        dbc.NavItem(dbc.NavLink("Donate(Button)", href="/"))
    ], style={'font-family': 'Montserrat, arial, sans-serif'}
    )
        
    return navbar