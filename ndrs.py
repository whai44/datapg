import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
from app import app
import plotly.graph_objects as go


df = pd.read_csv(r'C:/Users/whai/Desktop/Senior Project/dataplayground/ndrs9-10_2022.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['day_of_week'] = df['timestamp'].dt.day_of_week
car_type_data = df.groupby(df['timestamp'].dt.day_name())[['car']].sum()
car_type_data['percentage'] = car_type_data['car'] / car_type_data['car'].sum() * 100
vehicle_types = ['7up',	'bus',	'car',	'motorcycle',	'pickup'	,'trailer'	,'truck'	] 


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
        html.Div([
            # dcc.Input(),
            html.Br(),
             ])
    ]),

    dbc.Row(
        dbc.Col(html.H3("Mean Car Count by Hour",
                        className='text-center text-primary mb-4'),
                width=12)
    ),
    
    dbc.Row([
    
    
    
    dcc.Dropdown(
        id='day-dropdown',
        options=[{'label': days_map[num], 'value': num} for num in days_map],
        value=[0],  # Set default value to 'Monday'
        multi=True  # Allow multiple inputs
    )]),
    
    dbc.Row([
    
    
    dcc.Graph(id='line-chart')
    ]),


    dbc.Row([

        dcc.Dropdown(
            id='vehicle-dropdown',
            options=[{'label': vehicle, 'value': vehicle} for vehicle in vehicle_types],
            value=vehicle_types[0],  # Set default value to the first vehicle type
            multi=False  # Allow single selection
        )
    ]),

    dbc.Row([

        dcc.Dropdown(
            id='day-dropdown2',
            options=[
                {'label': 'Monday', 'value': 'Monday'},
                {'label': 'Tuesday', 'value': 'Tuesday'},
                {'label': 'Wednesday', 'value': 'Wednesday'},
                {'label': 'Thursday', 'value': 'Thursday'},
                {'label': 'Friday', 'value': 'Friday'},
                {'label': 'Saturday', 'value': 'Saturday'},
                {'label': 'Sunday', 'value': 'Sunday'}
            ],
            value='Monday'  # Set default value to Monday
        ),
    ]),
    dbc.Row([

        dcc.Graph(id='bar-chart')
    ])


    
    












])

@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('day-dropdown', 'value')]
)


def update_line_chart(days):
    # Filter the data for the selected day of the week
    df_selected_days = df[df['day_of_week'].isin(days)]

    # Group the data by hour and calculate the mean of the total car count
    df_selected_days_by_day_hour = df_selected_days.groupby(['day_of_week', df_selected_days['timestamp'].dt.hour]).mean().reset_index()
    df_selected_days_by_day_hour['day_of_week'] = df_selected_days_by_day_hour['day_of_week'].map(days_map)


    # Create a line chart with Plotly Express
    fig = px.line(df_selected_days_by_day_hour, x='timestamp', y='total',
                  color='day_of_week', labels={'timestamp': 'Hour of Day', 'total': 'Mean Car Count'},
                  title='Mean Car Count by Hour on Selected Days of the Week')

    return fig
        

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('day-dropdown2', 'value'),
     Input('vehicle-dropdown', 'value')]
)
def update_bar_chart(selected_day, selected_vehicle):
    # Filter data by selected day and vehicle type
    filtered_df = df[(df['day_of_week'] == selected_day) & (df['type'] == selected_vehicle)]
    
    # Group filtered data by type and sum the total count
    grouped_df = filtered_df.groupby('type').sum(numeric_only=True).reset_index()
    
    # Create bar chart
    fig = px.bar(grouped_df, x='type', y='total', title=f'{selected_vehicle} Count on {selected_day}')
    return fig
