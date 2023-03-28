import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import pandas as pd
from app import app

bt_layout = html.Div(
    [

    dbc.Row(
        dbc.Col(html.H1("Information about the bluetooth sensor.........",
                        className='text-center text-primary mb-4'),
                width=12)
    ),
])
