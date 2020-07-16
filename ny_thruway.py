import csv
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
# import dash
# import dash_core_components as dcc
# import dash_html_components as html

url_2019 = 'https://raw.githubusercontent.com/ryan-osleeb/Mobility-Dash/master/ny_car_average_2019.csv'
url_2020 = 'https://raw.githubusercontent.com/ryan-osleeb/Mobility-Dash/master/ny_car_average_2020.csv'
#download files
data_2019 = pd.read_csv(url_2019)
data_2020 = pd.read_csv(url_2020)
   
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

# app = dash.Dash(__name__)

# app.layout = html.Div(children=[html.H1(children=''),
#                         dcc.Graph(
#                                 id = 'NY Thruway',
#                                 figure=ny_cars_rolling
#                             )
#                             ])

# if __name__ == '__main__':
#     app.run_server(debug=True)
