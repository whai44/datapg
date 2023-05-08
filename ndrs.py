import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
from app import app
import plotly.graph_objects as go
import dash_table
df1 = pd.read_csv(r'C:/Users/whai/Desktop/Senior Project/dataplayground/top5max.csv')
df2 = pd.read_csv(r'C:/Users/whai/Desktop/Senior Project/dataplayground/top5min.csv')
df = pd.read_csv(r'C:/Users/whai/Desktop/Senior Project/dataplayground/ndrs9-10_2022.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['day of week'] = df['timestamp'].dt.day_of_week
df['hour_of_day'] = df['timestamp'].dt.hour
car_type_data = df.groupby(df['timestamp'].dt.day_name())[['car']].sum()
car_type_data['percentage'] = car_type_data['car'] / car_type_data['car'].sum() * 100
vehicle_types = ['7up',	'bus',	'car',	'motorcycle',	'pickup'	,'trailer'	,'truck'	] 
ndrslo = {'Location': ['1', '2', '3','4','5'],
        'Name': ['Soi Ari, BigC Rama4','Ratchadaphisek Road, Ocean Tower 1',
                 'Khlong Toei Intersection ',
                 'Rama 3 Road, Soi 85','the Port Authority of Thailand Building'],
        }
dfndrslo = pd.DataFrame(ndrslo)
dfndrslo.style.set_properties(**{'text-align': 'center'})

days_map = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}


print(df.head())


ndrs_layout = html.Div([
    
  
    dbc.Row([
         dbc.Col([
            
            html.Img(src='https://sv1.picz.in.th/images/2023/05/01/yETCa2.jpg',  style={"float": "left", "margin-right": "20px","display": "block", "margin": "0 auto", "width": "550px", "height": "400px"})
        ],
         style={"margin-top": "30px", "margin-bottom": "60px"}
           
        ),
        dbc.Col([
         
         html.Br(),
         html.Br(),
         html.Br(),
         html.Br(),
         html.Br(),
          html.H3('Sensor Locations'),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in dfndrslo.columns],
            data=dfndrslo.to_dict('records'),
        ),
           
        ], #width={'size':5, 'offset':0, 'order':2},
           ),
       
       
       
       
       
       
    ]),
    
    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
             ])
    ]),

    
    
    dbc.Row([
        html.H3('Location 1: Kasemrad Intersection'),
        dbc.Col([
    
    
    
    dcc.Dropdown(
        id='day-dropdown',
        options=[{'label': days_map[num], 'value': num} for num in days_map],
        value=[0],  # Set default value to 'Monday'
        multi=True  # Allow multiple inputs
    ),]),
    dbc.Col([
dcc.Dropdown(
    id='day-of-week-dropdown',
    options=[
        {'label': 'Monday', 'value': 0},
        {'label': 'Tuesday', 'value': 1},
        {'label': 'Wednesday', 'value': 2},
        {'label': 'Thursday', 'value': 3},
        {'label': 'Friday', 'value': 4},
        {'label': 'Saturday', 'value': 5},
        {'label': 'Sunday', 'value': 6}
    ],
    value=0,  # Set initial value
    placeholder='Select a day of the week'
)
,

    ])
    
    
    
    
    ]),
    
    dbc.Row([
    dbc.Col([
    
    dcc.Graph(id='line-chart')
    ]),
    dbc.Col([

dcc.Graph(id='vehicle-counts-chart')

    ])
    ]),


    

   
   
    
    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
             ])
    ]),
    
    
    
    
    
    
    dbc.Row([
         html.Br(),
          html.Br(),
    
     html.H3('Top 5 days with the most number of vehicles'),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df1.columns],
            data=df1.to_dict('records'),
        ),
    ], className='row'),

    dbc.Row([
        html.Div([
            # dcc.Input(),
            html.Br(),
             html.Br(),
             ])
    ]),
    
    
    dbc.Row([
     html.H3('Top 5 days with the least number of vehicles'),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df2.columns],
            data=df2.to_dict('records')
        ),
         html.Br(),
          html.Br()
    ], className='row')

    ])


  
    














@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('day-dropdown', 'value')]
)


def update_line_chart(days):
    # Filter the data for the selected day of the week
    df_selected_days = df[df['day of week'].isin(days)]

    # Group the data by hour and calculate the mean of the total car count
    df_selected_days_by_day_hour = df_selected_days.groupby(['day of week', df_selected_days['timestamp'].dt.hour]).mean().reset_index()
    df_selected_days_by_day_hour['day of week'] = df_selected_days_by_day_hour['day of week'].map(days_map)


    # Create a line chart with Plotly Express
    fig = px.line(df_selected_days_by_day_hour, x='timestamp', y='total',
                  color='day of week', labels={'timestamp': 'Hour of Day (6:00AM - 20:00PM)', 'total': 'Number of vehicles'},
                  title='Mean vehicles count per minute on selected days')

    return fig
        

@app.callback(
    Output('vehicle-counts-chart', 'figure'),
    [Input('day-of-week-dropdown', 'value')]
)

def update_chart(day_of_week):
    # Filter data for selected day of week
    filtered_data = df[df['day of week'] == day_of_week]
    
    # Group by hour of day and calculate mean counts
    mean_counts = filtered_data.groupby('hour_of_day').mean().reset_index()
    
    # Exclude the 'total' column from the mean counts
    mean_counts = mean_counts.drop(columns=['total'])
    mean_counts = mean_counts.drop(columns=['day of week'])
    # Create a stacked area chart
    fig = go.Figure()
    for col in mean_counts.columns[1:]:
        fig.add_trace(go.Scatter(
            x=mean_counts['hour_of_day'],
            y=mean_counts[col],
            mode='lines',
            stackgroup='one',
            name=col
        ))
    
    # Update chart layout
    fig.update_layout(
        title='Mean types of vehicle counts per minute on selected days'.format(day_of_week),
        xaxis=dict(title='Hour of Day (6:00AM - 20:00PM)'),
        yaxis=dict(title='Number of vehicles'),
        showlegend=True
    )
    return fig