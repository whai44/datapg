import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input, State
import pandas as pd
from app import app


date = ['MON','TUE','WED','THU','FRI','SAT','SUN']

ndrs_layout = html.Div(
    [
        dbc.Row([

        dbc.Col([
            html.H5("Data from CCTV",
                        className='text-center text-secondary mb-4'),
                
            
            dcc.Dropdown(id='my-dpdn1', multi=True, value=['MON','TUE'],
                         options=[{'label':x, 'value':x}
                                  for x in date],
                         ),
            dcc.Graph(id='line-fig1', figure={})
        ], #width={'size':5, 'offset':0, 'order':2},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),
        

        dbc.Col([
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H5("insights from the data",
                        className='text-center text-secondary mb-4'),
            html.H5("insights from the data",
                        className='text-center text-secondary mb-4'),
            html.H5("insights from the data",
                        className='text-center text-secondary mb-4'),
            html.H5("insights from the data",
                        className='text-center text-secondary mb-4'),
                 
                  ])

    ], justify='start'),
    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
            html.Br(),
        ])
    ]),
         ]
)


