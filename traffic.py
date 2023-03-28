import requests
import json
import matplotlib.pyplot as plt
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import pandas as pd
from app import app


#########################Traffic signal sensor at kasemrad junction###############################
date = ['MON','TUE','WED','THU','FRI','SAT','SUN']
jsonks = pd.read_json(r'C:\Users\whai\Desktop\Senior Project\dataplayground\dataplaygroundprototype\Signalkasem.json')['data']
data_ks = []
for i in range (len(jsonks)):
    data_ks.append({'timestamp':jsonks[i]['timestamp'],
            'phase_1':jsonks[i]['data']['phase_1'],
            'phase_2':jsonks[i]['data']['phase_2'],
            'phase_3':jsonks[i]['data']['phase_3'],
            'phase_4':jsonks[i]['data']['phase_4'],
            'phase_5':jsonks[i]['data']['phase_5'],
            'phase_6':jsonks[i]['data']['phase_6'],
            'phase_7':jsonks[i]['data']['phase_7'],
            'phase_8':jsonks[i]['data']['phase_8']})
df_ks = pd.DataFrame(data_ks)
df_ks.timestamp = pd.to_datetime(df_ks.timestamp)
df_ks['day_name']=df_ks['timestamp'].dt.day_name()
df_ks.set_index('timestamp',inplace = True)
df_ksm = df_ks.between_time('7:00','10:00').groupby(by=['day_name']).mean()
df_kse = df_ks.between_time('16:00','19:00').groupby(by=['day_name']).mean()
df_ksm = df_ksm.reset_index()
df_kse = df_kse.reset_index()
dfm = df_ksm.set_index('day_name')
dfe = df_kse.set_index('day_name')

#######################################Layout##############################################
tf_layout = html.Div(
    [

    dbc.Row(
        dbc.Col(html.H3("Traffic Signal Phase",
                        className='text-center text-primary mb-4'),
                width=12)
    ),



    dbc.Row([
        html.Img(src='https://i.ibb.co/d6vvqbg/2565-11-03-01-22-06.png', alt='image',height="300",width="9")
    ]),
    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            ])
    ]),
    dbc.Row([

       dcc.Dropdown(id='my-dpdn4', multi=False, value=['MON'],
                         options=[{'label':x, 'value':x}
                                  for x in df_ksm['day_name'].to_list()],
                         )
]),
    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            ])
    ]),

    dbc.Row([
        dbc.Col(html.H4("mornig rush hour",
                        className='text-center text-warning mb-4'),
                width=6),


        dbc.Col(html.H4("evening rush hour",
                        className='text-center text-warning mb-4'),
                width=6),

        ]),


    dbc.Row([
        dbc.Col([
            
            dcc.Graph(id='line-fig3')
        ],width=6#width={'size':5, 'offset':0, 'order':2},
           
        ),
        dbc.Col([
           
            dcc.Graph(id='line-fig4', figure={})
        ], #width={'size':5, 'offset':0, 'order':2},
           width=6),
    
    ]),
])

##########################callback##########################################

@app.callback(
    Output(component_id='line-fig3', component_property='figure'),
    [Input(component_id='my_dpdn4', component_property='value')]
)

def update_graph(my_dpdn4):
    dfmm = dfm.transpose()
    dfmm = dfmm.reset_index()
    

    piechart=px.pie(dfmm , names = 'index' , values = 'my_dpdn4')

    return (piechart)
