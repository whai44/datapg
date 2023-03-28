import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input, State
import pandas as pd
from app import app


info_layout = html.Div(
    [

    dbc.Row(
        dbc.Col(html.H1("Information about the project.........",
                        className='text-center text-primary mb-4'),
                width=12)
    ),
])