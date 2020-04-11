import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

body = html.Div([
    html.H1('Fundraiser: Supplying PPE for Frontline Healthcare Professionals'),
    html.H3('Overview'),
    html.P(['Our teams at Cloudcafe and Coding Temple are raising funds here to donate directly to the following campaign: ',
    html.A('PPE for Frontline Healthcare Professionals', href='https://www.gofundme.com/f/ppe-for-frontline-healthcare-professionals',
        target='blank', rel='noopener')]),
    html.P(['This fundraiser has been organized by Sonny Tai, the CEO of ',
    html.A('Actuate AI', href='https://actuate.ai/',
        target='blank', rel='noopener'),
        '. Sonny is a former Marine and University of Chicago Booth grad. He describes his mission for his fundraiser as the following:']),
    html.Blockquote([
        html.P('"Healthcare workers are the front line fighters against the COVID-19 pandemic. However, they are now facing desperate shortages of Personal Protective Equipment (PPE) nationwide.'),
        html.P('President John F. Kennedy famously said: "Ask not what your country can do for you, ask what you can do for your country". My friends - if there was ever a point in our lifetimes that required national mobilization, for every single American to do their part, that time is now. Our actions may be small and insignificant, but seemingly small and insignificant efforts multiplied by 320 million can move mountains.'),
        html.P('We are a team of regular, passionate Americans who believe that we can help to move mountains. We may not be doctors and nurses, but we\'ve heard the outcry from healthcare professionals across the country, and they\'ve made it quite clear what they need."'),
    ]),
    html.H3('Plan of Action'),
    html.P(['1. Identify and collect quotes from suppliers that can manufacture high quality N-95 masks and ship to the United States in a cost-effective manner. ',
        html.Strong("Sonny's team has identified a primary supplier and will be placing their first order on Monday, April 13th.")
    ]),
    html.P(['2. Identify hospitals that have the most urgent need for PPE. One of the resources we will use to identify these hospitals is the list from #GetUsPPE.org. ',
        html.Strong("Sonny's team has coordinated with multiple hospitals who are in urgent need and they will receive N95 masks from this initial order.")
    ]),
    html.P(['3. Purchase the PPE and ship it to the hospitals. ',
        html.Strong("First shipment order is being placed this Monday, April 13th. ")
    ]),
    html.P('The fundraiser operates completely on a non-profit basis and is committed to complete transparency, which means that:',
    style={'text-decoration': 'underline'}),
    html.P('1. We will track spending and upload invoices for all of our purchases, and any left over funds will be donated to a to-be-designated 501(c)3 charity that helps those impacted by COVID-19.'),
    html.P('2. None of us who are involved in this campaign will draw a salary from the campaign or appropriate any of its funds for personal use.'),
    html.P('3. The email addresses, phone numbers, and LinkedIn profiles for all of the campaign\'s organizers will be posted on the GoFundMe to ensure accountability.'),



])

def AboutPage():
    layout = html.Div([
    body],
    className='about')
    return layout