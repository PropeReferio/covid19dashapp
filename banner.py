import dash_html_components as html

def Banner():
    banner = html.Div(
    [
        html.P(
            "COVID Live Tracking Tool, Project developed in partnership between Cloudcafe Technologies and Coding Temple",
            className="lead"
        )
    ], className="banner"
    )

    return banner