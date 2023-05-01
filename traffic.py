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
import plotly.graph_objs as go
import dash_table

#########################Traffic signal sensor at kasemrad junction###############################
date = ['MON','TUE','WED','THU','FRI','SAT','SUN']
jsonks = pd.read_json(r'C:\Users\whai\Desktop\Senior Project\dataplayground\dataplaygroundprototype\Signalkasem.json')['data']
jsonkt = pd.read_json(r'C:\Users\whai\Desktop\Senior Project\dataplayground\dataplaygroundprototype\Signalkt.json')['data']
jsonnr = pd.read_json(r'C:\Users\whai\Desktop\Senior Project\dataplayground\dataplaygroundprototype\Signalnara.json')['data']
data_ks = []
data_kt = []
data_nr = []
#kasemrad
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
df_ks['day']=df_ks['timestamp'].dt.day_name()
df_ks.set_index('timestamp',inplace = True)
df_ksm = df_ks.between_time('7:00','10:00').groupby(by=['day']).mean()
df_kse = df_ks.between_time('16:00','19:00').groupby(by=['day']).mean()
df_ksm = df_ksm.reset_index()
df_kse = df_kse.reset_index()
# naranong
for i in range (len(jsonnr)):
    data_nr.append({'timestamp':jsonnr[i]['timestamp'],
            'phase_1':jsonnr[i]['data']['phase_1'],
            'phase_2':jsonnr[i]['data']['phase_2'],
            'phase_3':jsonnr[i]['data']['phase_3'],
            'phase_4':jsonnr[i]['data']['phase_4'],
            'phase_5':jsonnr[i]['data']['phase_5'],
            'phase_6':jsonnr[i]['data']['phase_6'],
            'phase_7':jsonnr[i]['data']['phase_7'],
            'phase_8':jsonnr[i]['data']['phase_8']})
df_nr = pd.DataFrame(data_nr)
df_nr.timestamp = pd.to_datetime(df_nr.timestamp)
df_nr['day']=df_nr['timestamp'].dt.day_name()
df_nr.set_index('timestamp',inplace = True)
df_nrm = df_nr.between_time('7:00','10:00').groupby(by=['day']).mean()
df_nre = df_nr.between_time('16:00','19:00').groupby(by=['day']).mean()
df_nrm = df_nrm.reset_index()
df_nre = df_nre.reset_index()
# klongtoey
for i in range (len(jsonkt)):
    data_kt.append({'timestamp':jsonkt[i]['timestamp'],
            'phase_1':jsonkt[i]['data']['phase_1'],
            'phase_2':jsonkt[i]['data']['phase_2'],
            'phase_3':jsonkt[i]['data']['phase_3'],
            'phase_4':jsonkt[i]['data']['phase_4'],
            'phase_5':jsonkt[i]['data']['phase_5'],
            'phase_6':jsonkt[i]['data']['phase_6'],
            'phase_7':jsonkt[i]['data']['phase_7'],
            'phase_8':jsonkt[i]['data']['phase_8']})
df_kt = pd.DataFrame(data_kt)
df_kt.timestamp = pd.to_datetime(df_kt.timestamp)
df_kt['day']=df_kt['timestamp'].dt.day_name()
df_kt.set_index('timestamp',inplace = True)
df_ktm = df_kt.between_time('7:00','10:00').groupby(by=['day']).mean()
df_kte = df_kt.between_time('16:00','19:00').groupby(by=['day']).mean()
df_ktm = df_ktm.reset_index()
df_kte = df_kte.reset_index()

#######################################Layout##############################################
tf_layout = html.Div(
    [
    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
             ])
    ]),

    dbc.Row(
        dbc.Col(html.H2("Traffic Signal Phase",
                        className='text-center text-primary mb-4'),
                width=12)
    ),
    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
            html.Br(),
            html.Br(),
             ])
    ]),
    dbc.Row([
        html.H3('At Kasemrad Intersection',className='text-center text-primary mb-4'),
    ]),
     

    dbc.Row([
      
        html.Img(src='https://i.ibb.co/d6vvqbg/2565-11-03-01-22-06.png', alt='image',height="240",width="6")
    ]),
    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
            html.Br(),
        ])
    ]),
    dbc.Row([

       dcc.Dropdown(
        id='day-dropdown',
        options=[{'label': day, 'value': day} for day in df_ksm['day'].unique()],
        value=df_ksm['day'].unique()[0]
    )]),
    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
            html.Br(),
            ])
    ]),

    dbc.Row([
        dbc.Col(html.H4("Morning rush hour",
                        className='text-center text-warning mb-4'),
                width=6),
        dbc.Col(html.H4("Evening rush hour",
                        className='text-center text-warning mb-4'),
                width=6),
                ]),


    dbc.Row([
        dbc.Col([
            
            dcc.Graph(id='bar-chart-1')
        ],width=6#width={'size':5, 'offset':0, 'order':2},
           
        ),
        dbc.Col([
           
            dcc.Graph(id='bar-chart-2', figure={})
        ], #width={'size':5, 'offset':0, 'order':2},
           width=6),
    
    ]),

    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
            html.Br(),
            html.Br(),
             ])
    ]),
     
    dbc.Row([
        html.H3('At Na Ranong Intersection',className='text-center text-primary mb-4'),
    ]), 
     
     
    dbc.Row([
       html.Img(src='https://sv1.picz.in.th/images/2023/05/01/yEM5K0.png', alt='image',height="480",width="6")
    ]),
    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
            html.Br(),
        ])
    ]),
    dbc.Row([

       dcc.Dropdown(
        id='day-dropdown2',
        options=[{'label': day, 'value': day} for day in df_nrm['day'].unique()],
        value=df_nrm['day'].unique()[0]
    )]),
    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
            html.Br(),
            ])
    ]),

    dbc.Row([
        dbc.Col(html.H4("Morning rush hour",
                        className='text-center text-warning mb-4'),
                width=6),
        dbc.Col(html.H4("Evening rush hour",
                        className='text-center text-warning mb-4'),
                width=6),
                ]),


    dbc.Row([
        dbc.Col([
            
            dcc.Graph(id='bar-chart-3')
        ],width=6#width={'size':5, 'offset':0, 'order':2},
           
        ),
        dbc.Col([
           
            dcc.Graph(id='bar-chart-4', figure={})
        ], #width={'size':5, 'offset':0, 'order':2},
           width=6),
    
    ]),
     
      dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
            html.Br(),
            html.Br(),
             ])
    ]),
     
    dbc.Row([
        html.H3('At Khlong Toei Intersection',className='text-center text-primary mb-4'),
    ]), 
     
     
     
     
     
     
     dbc.Row([
       
       
        html.Img(src='https://sv1.picz.in.th/images/2023/05/01/yEMoat.jpg', alt='image',height="480",width="6")
    ]),
    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
            html.Br(),
        ])
    ]),
    dbc.Row([

       dcc.Dropdown(
        id='day-dropdown3',
        options=[{'label': day, 'value': day} for day in df_ktm['day'].unique()],
        value=df_ktm['day'].unique()[0]
    )]),
    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
            html.Br(),
            ])
    ]),

    dbc.Row([
        dbc.Col(html.H4("Morning rush hour",
                        className='text-center text-warning mb-4'),
                width=6),
        dbc.Col(html.H4("Evening rush hour",
                        className='text-center text-warning mb-4'),
                width=6),
                ]),


    dbc.Row([
        dbc.Col([
            
            dcc.Graph(id='bar-chart-5')
        ],width=6#width={'size':5, 'offset':0, 'order':2},
           
        ),
        dbc.Col([
           
            dcc.Graph(id='bar-chart-6', figure={})
        ], #width={'size':5, 'offset':0, 'order':2},
           width=6),
    
    ]),
])

##########################callback##########################################

@app.callback(
    dash.dependencies.Output('bar-chart-1', 'figure'),
    [dash.dependencies.Input('day-dropdown', 'value')])

def update_bar_chart(selected_day):
    filtered_data = df_ksm[df_ksm['day'] == selected_day]
    values = filtered_data.iloc[0, 1:].tolist()
    bar_chart = go.Bar(x=['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'], y=values)
    return {'data': [bar_chart]}
    
    
@app.callback(
    dash.dependencies.Output('bar-chart-2', 'figure'),
    [dash.dependencies.Input('day-dropdown', 'value')])
def update_bar_chart_2(selected_day):
    filtered_data = df_kse[df_kse['day'] == selected_day]
    values = filtered_data.iloc[0, 1:].tolist()
    bar_chart = go.Bar(x=['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'], y=values)
    return {'data': [bar_chart]}

###
@app.callback(
    dash.dependencies.Output('bar-chart-3', 'figure'),
    [dash.dependencies.Input('day-dropdown2', 'value')])

def update_bar_chart3(selected_day):
    filtered_data = df_nrm[df_nrm['day'] == selected_day]
    values = filtered_data.iloc[0, 1:].tolist()
    bar_chart = go.Bar(x=['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4','Phase 5','Phase 6','Phase 7','Phase 8'], y=values)
    return {'data': [bar_chart]}
    
    
@app.callback(
    dash.dependencies.Output('bar-chart-4', 'figure'),
    [dash.dependencies.Input('day-dropdown2', 'value')])
def update_bar_chart4(selected_day):
    filtered_data = df_nre[df_nre['day'] == selected_day]
    values = filtered_data.iloc[0, 1:].tolist()
    bar_chart = go.Bar(x=['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4','Phase 5','Phase 6','Phase 7','Phase 8'], y=values)
    return {'data': [bar_chart]}



####
@app.callback(
    dash.dependencies.Output('bar-chart-5', 'figure'),
    [dash.dependencies.Input('day-dropdown3', 'value')])

def update_bar_chart5(selected_day):
    filtered_data = df_ktm[df_ktm['day'] == selected_day]
    values = filtered_data.iloc[0, 1:].tolist()
    bar_chart = go.Bar(x=['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4','Phase 5','Phase 6','Phase 7','Phase 8'], y=values)
    return {'data': [bar_chart]}
    
    
@app.callback(
    dash.dependencies.Output('bar-chart-6', 'figure'),
    [dash.dependencies.Input('day-dropdown3', 'value')])
def update_bar_chart6(selected_day):
    filtered_data = df_kte[df_kte['day'] == selected_day]
    values = filtered_data.iloc[0, 1:].tolist()
    bar_chart = go.Bar(x=['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4','Phase 5','Phase 6','Phase 7','Phase 8'], y=values)
    return {'data': [bar_chart]}