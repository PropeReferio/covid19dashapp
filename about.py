import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

body = html.Div([
    html.H1('About this project'),
    html.P(['This dashboard is updated daily to show updates in the COVID-19 pandemic. This project was designed and deployed as a partnered effort between two Chicago-based companies, ',
        html.A('Cloudcafe Technologies', href='https://cloudcafe.io/',
            target='_blank', rel='noopener'),
            ' and ',
        html.A('Coding Temple', href='https://codingtemple.com/',
            target='_blank', rel='noopener'),
            '.'
        ]),
    html.H1('Motivation for the Project'),
    html.P('There are already many COVID-19 dashboards online and our teams at Cloudcafe and Coding Temple decided to add another. So what makes our project different? We developed our dashboard as another informational resource for the community, along with highlighting data which we have not seen present in others (i.e. active cases as a % of total population).'),
    html.P('More importantly, this website is used to drive fundraising for organizations and individuals who are on the frontlines fighting this pandemic. 100% of all funds raised here go directly towards the fight. Learn more about our current fundraising partner\'s mission and donate here.'),
    html.H1('Data Sources'),
    html.Ul([
        html.Li(html.A('Johns Hopkins CSSE', href='https://github.com/CSSEGISandData/COVID-19',
        target='_blank', rel='noopener')),
        html.Li(html.A('World Health Organization', href='https://www.who.int/',
        target='_blank', rel='noopener'))
    ]),
    html.H1('Resources for the community'),
    html.Ul([
        html.Li(['COVID-19 testing data: ',
            html.A('https://ourworldindata.org/covid-testing',
            href='https://ourworldindata.org/covid-testing',
            target='_blank', rel='noopener')]),
        html.Li(['Symptoms checker: ',
            html.A('https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/testing.html',
            href='https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/testing.html',
            target='_blank', rel='noopener')]),
        html.Li(['Find COVID-19 testing near you: ',
            html.A('https://findcoronatest.com/',
            href='https://findcoronatest.com/',
            target='_blank', rel='noopener')]),
        html.Li(['Comprehensive guide to financial support: ',
            html.A('https://www.possiblefinance.com/blog/covid-financial-support/',
            href='https://www.possiblefinance.com/blog/covid-financial-support/',
            target='_blank', rel='noopener')]),
        html.Li(['Safety Guide: ',
            html.A('https://www.redcross.org/about-us/news-and-events/news/2020/coronavirus-safety-and-readiness-tips-for-you.html',
            href='https://www.redcross.org/about-us/news-and-events/news/2020/coronavirus-safety-and-readiness-tips-for-you.html',
            target='_blank', rel='noopener')])
        ]),
    html.H1('Any bugs or enhancement requests?'),
    html.P('You may directly contact Arjun Srivastava (arjun@cloudcafe.io) or Ripal Patel (ripalp@codingtemple.com).'),
    html.H1('Developer'),
    html.A('Bo Stevens', href='https://www.linkedin.com/in/bostevens-softwareengineer/',
    target='_blank', rel='noopener')
])

def AboutPage():
    layout = html.Div([
    body],
    className='about')
    return layout