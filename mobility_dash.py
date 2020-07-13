import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from apple_maps_dash import am_us, am_risk, am_heat
from google_mobility import us_fig, parks_fig, workplace_fig
from ny_thruway import ny_cars_rolling


app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1(children=''),
                        dcc.Graph(
                                id = 'US Driving',
                                figure=am_us
                            ),
                        html.H2(children=''),
                        dcc.Graph(
                                id = 'US Heat Map',
                                figure=am_heat
                            ),
                        html.H3(children=''),
                        dcc.Graph(
                                id = 'US Google Mobility',
                                figure=us_fig
                            ),
                        html.H4(children=''),
                        dcc.Graph(
                                id = 'Parks Mobility Heat Map',
                                figure=parks_fig
                            ),
                        html.H5(children=''),
                        dcc.Graph(
                                id = 'Workplace Mobility Heat Map',
                                figure=workplace_fig
                            ),
                        html.H6(children=''),
                        dcc.Graph(
                                id = 'NY Thruway',
                                figure=ny_cars_rolling
                            )
                            ])

if __name__ == '__main__':
    app.run_server(debug=True)
