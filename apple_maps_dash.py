import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

#url = "https://covid19-static.cdn-apple.com/covid19-mobility-am_data/2009HotfixDev22/v3/en-us/applemobilitytrends-2020-06-06.csv"
#url = "https://covid19-static.cdn-apple.com/covid19-mobility-am_data/2010HotfixDev17/v3/en-us/applemobilitytrends-2020-06-13.csv"
#url = "https://covid19-static.cdn-apple.com/covid19-mobility-am_data/2010HotfixDev25/v3/en-us/applemobilitytrends-2020-06-20.csv"

#r = requests.get(url)
#url_content = r.content
#csv_file = open('am_downloaded.csv', 'wb')
#csv_file.write(url_content)
#csv_file.close()
#file_folder = '/Users/rosleeb/ny_thruway'
#am_data = pd.read_csv(f'{file_folder}/am_downloaded.csv')

am_url = 'https://raw.githubusercontent.com/ryan-osleeb/Mobility-Dash/master/am_downloaded.csv'
am_data = pd.read_csv(am_url)


am_data["Map"] = am_data["region"] + "_" + am_data["transportation_type"]
am_data = am_data.drop(['geo_type','alternative_name','region','transportation_type', 'sub-region', "country"], axis=1)
maps = am_data['Map']
am_data.drop(labels=['Map'], axis=1,inplace = True)
am_data.insert(0, 'Map', maps)
am_data = am_data.set_index('Map')
am_data = pd.DataFrame(am_data.T)

states = ['Alabama_driving', 'Alaska_driving', 'Arizona_driving', 'Arkansas_driving', 
          'California_driving', 'Colorado_driving', 'Connecticut_driving', 'Delaware_driving',
         'Florida_driving', 'Georgia_driving', 'Hawaii_driving', 'Idaho_driving', 'Illinois_driving',
         'Indiana_driving','Iowa_driving', 'Kansas_driving', 'Kentucky_driving', 'Louisiana_driving',
         'Maine_driving', 'Maryland_driving', 'Massachusetts_driving', 'Michigan_driving', 'Minnesota_driving',
         'Mississippi_driving', 'Missouri_driving', 'Montana_driving', 'Nebraska_driving', 'Nevada_driving',
         'New Hampshire_driving', 'New Jersey_driving', 'New Mexico_driving', 'New York_driving', 'North Dakota_driving',
         'North Carolina_driving', 'Ohio_driving', 'Oklahoma_driving', 'Oregon_driving', 'Pennsylvania_driving',
         'Rhode Island_driving', 'South Carolina_driving', 'South Dakota_driving', 'Tennessee_driving',
         'Texas_driving', 'Utah_driving', 'Vermont_driving', 'Virginia_driving', 'Washington_driving',
         'West Virginia_driving', 'Wisconsin_driving', 'Wyoming_driving']

state_codes = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE','FL', 'GA', 'HI', 'ID', 'IL',
         'IN','IA', 'KS', 'KY', 'LA','ME', 'MD', 'MA', 'MI', 'MN','MS', 'MO', 'MT', 'NE', 'NV',
         'NH', 'NJ', 'NM', 'NY', 'ND','NC', 'OH', 'OK', 'OR', 'PA','RI', 'SC', 'SD', 'TN',
         'TX', 'UT', 'VT', 'VA', 'WA','WV', 'WI', 'WY']

heat_map = []
for i in range(len(states)):
    #heat_map.append([states[i][:-8], am_data[states[i]][-1]])
    #heat_map.append([state_codes[i], np.average(am_data[states[i]][-7:])])
    heat_map.append([state_codes[i], np.average(am_data[states[i]][-7:])-np.average(am_data[states[i]][-14:-7])])

heat_map = pd.DataFrame(heat_map)
heat_map.columns = ['State', "Mobility"]

US_driving = np.array(am_data['United States_driving'])
US_roll_avg = am_data['United States_driving'].rolling(7).mean()
US_roll_avg = np.array(US_roll_avg.fillna(''))
US_walking = np.array(am_data['United States_walking'])
US_transit = np.array(am_data['United States_transit'])

Arizona = am_data['Arizona_driving'].rolling(7).mean()
Arizona = np.array(Arizona.fillna(''))
California = am_data['California_driving'].rolling(7).mean()
California = np.array(California.fillna(''))
Florida = am_data['Florida_driving'].rolling(7).mean()
Florida = np.array(Florida.fillna(''))
Texas = am_data['Texas_driving'].rolling(7).mean()
Texas= np.array(Texas.fillna(''))

us_driving = go.Scatter(
                x = am_data.index,
                y = US_driving,
                name = 'US Driving',
                mode = 'lines'
    )

us_rolling = go.Scatter(
                x = am_data.index,
                y = US_roll_avg,
                name = 'US 7-Day Rolling Avg',
                mode = 'lines'
    )

us_walking = go.Scatter(
                x = am_data.index,
                y = US_walking,
                name = 'US Walking',
                mode = 'lines'
    )

us_transit = go.Scatter(
                x = am_data.index,
                y = US_transit,
                name = 'US Transit',
                mode = 'lines'
    )

AZ_mobility = go.Scatter(
                x = am_data.index,
                y = Arizona,
                name = 'Arizona',
                mode = 'lines'
    )

CA_mobility = go.Scatter(
                x = am_data.index,
                y = California,
                name = 'California',
                mode = 'lines'
    )

FL_mobility = go.Scatter(
                x = am_data.index,
                y = Florida,
                name = 'Florida',
                mode = 'lines'
    )

TX_mobility = go.Scatter(
                x = am_data.index,
                y = Texas,
                name = 'Texas',
                mode = 'lines'
    )

US_am_data = [us_driving, us_rolling, us_walking, us_transit]
Risk_am_data = [AZ_mobility, CA_mobility, FL_mobility, TX_mobility]

am_us = go.Figure(data = US_am_data)

am_us.update_layout(
     title_text = 'Apple Maps Mobility Index',
 )

am_risk = go.Figure(data = Risk_am_data)

am_risk.update_layout(
     title_text = 'Apple Maps Mobility Driving States At-Risk',
 )

am_heat = go.Figure(data=go.Choropleth(
    locations=heat_map['State'], # Spatial coordinates
    z = heat_map['Mobility'], # am_data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Greens',
    colorbar_title = "Mobility Index",
))

am_heat.update_layout(
    title_text = 'Apple Maps Mobility Heat Map',
    geo_scope='usa', # limite map scope to USA
)

app = dash.Dash()
server=app.server


app.layout = html.Div(children=[html.H1(children=''),
                        dcc.Graph(
                                id = 'US Driving',
                                figure=am_us
                            ),
                        html.H2(children=''),
                        dcc.Graph(
                                id = 'At Risk States',
                                figure=am_risk
                            ),
                        html.H3(children=''),
                        dcc.Graph(
                                id = 'US Heat Map',
                                figure=am_heat
                            )
                            ])

if __name__ == '__main__':
    app.run_server(debug=True)
