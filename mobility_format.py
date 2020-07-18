import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

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

#get google mobility data
url = 'https://raw.githubusercontent.com/ryan-osleeb/Mobility-Dash/master/go_downloaded.csv'
data = pd.read_csv(url, dtype={'country_region_code': 'str',
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

#get apple driving data
am_url = 'https://raw.githubusercontent.com/ryan-osleeb/Mobility-Dash/master/am_downloaded.csv'
am_data = pd.read_csv(am_url)
am_data["Map"] = am_data["region"] + "_" + am_data["transportation_type"]
am_data = am_data.drop(['geo_type','alternative_name','region','transportation_type', 'sub-region', "country"], axis=1)
maps = am_data['Map']
am_data.drop(labels=['Map'], axis=1,inplace = True)
am_data.insert(0, 'Map', maps)
am_data = am_data.set_index('Map')
am_data = pd.DataFrame(am_data.T)

#get ny thruway formatted data
url_2019 = 'https://raw.githubusercontent.com/ryan-osleeb/Mobility-Dash/master/ny_car_average_2019.csv'
url_2020 = 'https://raw.githubusercontent.com/ryan-osleeb/Mobility-Dash/master/ny_car_average_2020.csv'
#download files
data_2019 = pd.read_csv(url_2019)
data_2020 = pd.read_csv(url_2020)

#construct google mobility charts/maps
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

#construct apple mobility charts/maps
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

#construct ny thruway chart
rolling19 = go.Scatter(
                y = data_2019['2019'],
                name = '2019',
                mode = 'lines'
    )

rolling20 = go.Scatter(
                y = data_2020['2020'],
                name = '2020',
                mode = 'lines'
    )

rolling_avgs = [rolling19, rolling20]


ny_cars_rolling = go.Figure(data = rolling_avgs)

ny_cars_rolling.update_layout(
     title_text = 'New York Thruway 7-Day Rolling Average',
 )
