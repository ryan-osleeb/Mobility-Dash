import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html


# #url = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=6d352e35dcffafce"
# url = 'https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=7d0cb7d254d29111'

# r = requests.get(url)
# url_content = r.content
# csv_file = open('go_downloaded.csv', 'wb')
# csv_file.write(url_content)
# csv_file.close()
#file_folder = '/Users/rosleeb/google_mobility'
data = pd.read_csv('go_downloaded.csv', dtype={'country_region_code': 'str',
																'country_region': 'str',
																'sub_region_1': 'str',
																'sub_region_2': 'str',
																'date': 'str',
																'retail_and_recreation_percent_change_from_baseline': 'float',
																'grocery_and_pharmacy_percent_change_from_baseline': 'float',
																'parks_percent_change_from_baseline': 'float',
																'transit_stations_percent_change_from_baseline': 'float',
																'workplaces_percent_change_from_baseline': 'float',
																'residential_percent_change_from_baseline': 'float'})

data = data.rename({"retail_and_recreation_percent_change_from_baseline":"retail_and_recreation",
					"grocery_and_pharmacy_percent_change_from_baseline":"grocery_and_pharmacy",
					"parks_percent_change_from_baseline":"parks",
					"transit_stations_percent_change_from_baseline":"transit",
					"workplaces_percent_change_from_baseline":"workplace",
					"residential_percent_change_from_baseline":"residential"}, axis="columns")



states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 
          'California', 'Colorado', 'Connecticut', 'Delaware',
         'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois',
         'Indiana','Iowa', 'Kansas', 'Kentucky', 'Louisiana',
         'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
         'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
         'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Dakota',
         'North Carolina', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
         'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
         'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
         'West Virginia', 'Wisconsin', 'Wyoming']

state_codes = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE','FL', 'GA', 'HI', 'ID', 'IL',
         'IN','IA', 'KS', 'KY', 'LA','ME', 'MD', 'MA', 'MI', 'MN','MS', 'MO', 'MT', 'NE', 'NV',
         'NH', 'NJ', 'NM', 'NY', 'ND','NC', 'OH', 'OK', 'OR', 'PA','RI', 'SC', 'SD', 'TN',
         'TX', 'UT', 'VT', 'VA', 'WA','WV', 'WI', 'WY']


def get_state_mobility(dataset, location):
    state_mobility = []

    for i in range(len(states)):
        st = dataset[dataset['country_region'] == 'United States']
        st = st[st['sub_region_1'] == states[i]]
        st = st[st['sub_region_2'].isnull()]
        state_mobility.append([state_codes[i], np.average(st[location][-7:])-np.average(st[location][-14:-7])])
    
    state_mobility = pd.DataFrame(state_mobility)
    state_mobility.columns = ['State', 'Mobility']

    return state_mobility

go_parks_heat_map = get_state_mobility(data,'parks')
go_workplace_heat_map = get_state_mobility(data,'workplace')
go_residential_heat_map = get_state_mobility(data,'residential')

US_mobility = data[data['country_region'] == 'United States']
US_mobility = US_mobility[US_mobility['sub_region_1'].isnull()]

us_retail = US_mobility['retail_and_recreation'].rolling(7).mean()
us_grocery = US_mobility['grocery_and_pharmacy'].rolling(7).mean()
us_parks = US_mobility['parks'].rolling(7).mean()
us_transit = US_mobility['transit'].rolling(7).mean()
us_workplace = US_mobility['workplace'].rolling(7).mean()
us_residential = US_mobility['residential'].rolling(7).mean()

us_retail_plt = go.Scatter(
                x = data['date'],
                y = us_retail,
                name = 'US Retail',
                mode = 'lines'
    )

us_grocery_plt = go.Scatter(
                x = data['date'],
                y = us_grocery,
                name = 'US Grocery',
                mode = 'lines'
    )

us_parks_plt = go.Scatter(
                x = data['date'],
                y = us_parks,
                name = 'US Parks',
                mode = 'lines'
    )

us_transit_plt = go.Scatter(
                x = data['date'],
                y = us_transit,
                name = 'US Transit',
                mode = 'lines'
    )

us_workplace_plt = go.Scatter(
                x = data['date'],
                y = us_workplace,
                name = 'US Workplace',
                mode = 'lines'
    )

us_residential_plt = go.Scatter(
                x = data['date'],
                y = us_residential,
                name = 'US Residential',
                mode = 'lines'
    )

us_google_plt = [us_retail_plt, us_grocery_plt, us_parks_plt, us_transit_plt, us_workplace_plt, us_residential_plt]

us_fig = go.Figure(data = us_google_plt)

us_fig.update_layout(
     title_text = 'US Google Mobility',
 )

parks_fig = go.Figure(data=go.Choropleth(
    locations=go_parks_heat_map['State'], # Spatial coordinates
    z = go_parks_heat_map['Mobility'], # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Greys',
    colorbar_title = "Mobility Index",
))

parks_fig.update_layout(
    title_text = 'Google Mobility Weekly Change - Parks',
    geo_scope='usa', # limite map scope to USA
)

workplace_fig = go.Figure(data=go.Choropleth(
    locations=go_workplace_heat_map['State'], # Spatial coordinates
    z = go_workplace_heat_map['Mobility'], # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Blues',
    colorbar_title = "Mobility Index",
))

workplace_fig.update_layout(
    title_text = 'Google Mobility Weekly Change - Workplace',
    geo_scope='usa', # limite map scope to USA
)

residential_fig = go.Figure(data=go.Choropleth(
    locations=go_residential_heat_map['State'], # Spatial coordinates
    z = go_residential_heat_map['Mobility'], # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Oranges',
    colorbar_title = "Mobility Index",
))

residential_fig.update_layout(
    title_text = 'Google Mobility Weekly Change - Residential',
    geo_scope='usa', # limite map scope to USA
)

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1(children=''),
                        dcc.Graph(
                                id = 'US Google Mobility',
                                figure=us_fig
                            ),
                        html.H2(children=''),
                        dcc.Graph(
                                id = 'Parks Mobility Heat Map',
                                figure=parks_fig
                            ),
                        html.H3(children=''),
                        dcc.Graph(
                                id = 'Workplace Mobility Heat Map',
                                figure=workplace_fig
                            ),
                        html.H4(children=''),
                        dcc.Graph(
                                id = 'Residential Mobility Heat Map',
                                figure=residential_fig
                            ),
                            ])

if __name__ == '__main__':
    app.run_server(debug=True)
