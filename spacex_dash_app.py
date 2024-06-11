# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records', style={'textAlign': 'center', 'color': 'black', 'font-size': 40, 'font-family': 'Arial'}),
    html.H2('by Rishi Rama', style={'textAlign': 'center', 'color': 'black', 'font-size': 16, 'font-family': 'Arial'}),
    html.Br(),
    dcc.Dropdown(id='site-dropdown', 
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'site1'},
                     {'label': 'CCAFS SLC-40', 'value': 'site2'},
                     {'label': 'KSC LC-39A', 'value': 'site3'},
                     {'label': 'VAFB SLC-4E', 'value': 'site4'},
                 ],  
                 value='ALL', 
                 placeholder="Select a Launch Site", 
                 searchable=True,
                 style={'width': '100%', 'font-size': '20px', 'text-align': 'center'}
                ),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                    value=[0, 10000]),
    html.Br(),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def update_pie_chart(selected_site):
    df_filtered = spacex_df
    if selected_site == 'ALL':
        fig = px.pie(df_filtered, values='class', names='Launch Site', title='Total Success Launches By Site')
    else:
        df_filtered = df_filtered[df_filtered['Launch Site'] == selected_site]
        df_grouped = df_filtered.groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        fig = px.pie(df_grouped, values='class count', names='class', title=f'Success Launches for Site {selected_site}')
    return fig

@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'), 
               Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    df_filtered = spacex_df[(spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)]
    if selected_site == 'ALL':
        fig = px.scatter(df_filtered, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
    else:
        site_filtered_df = df_filtered[df_filtered['Launch Site'] == selected_site]
        fig = px.scatter(site_filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {selected_site}')
    return fig

if __name__ == '__main__':
    app.run_server()
