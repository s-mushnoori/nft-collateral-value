# Import dependencies
import pandas as pd
import plotly
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from datetime import date

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read data
df = pd.read_csv("Data/combined_nft_cv.csv")

# App layout ==================================================================

app.layout = html.Div([

    html.H1('NFT Collateral Value Calculator', style={'text-align': 'center'}),

    html.Div([
        html.H6('Select a project:'),

        dcc.Dropdown(
            id='select_project',
            options=[
                {'label': 'Cryptopunks', 'value': 'Cryptopunks'},
                {'label': 'Bored Ape Yacht Club (BAYC)', 'value': 'BoredApeYachtClub'},
                {'label': 'Mutant Ape Yacht Club (MAYC)', 'value': 'MutantApeYachtClub'},
                {'label': 'World of Women (WOW)', 'value': 'World_Of_Women'}],
            multi=False,
            value='Cryptopunks',
            style={'width': '150%'}
            ),
        ], style={'display': 'inline-block', 'margin-left': '10vw','vertical-align': 'top'}),
    
    
    html.Div([
        html.H6('Select a date:'),
    
        dcc.DatePickerSingle(
            id='select_date',
            date=date(2021, 12, 13)
            )
        ], style={'display': 'inline-block', 'margin-left': '40vw', 'vertical-align': 'top'}),
        
    html.Hr(),
    
    html.Div(
        id='collateral_value_print', 
        style = {'text-align': 'center'}),
    
    
    html.Div(
        dcc.Graph(
            id='collateral_value_plot'
            )
    )
])


# Connect Plotly graphs with Dash components ==================================

@app.callback(
    Output('collateral_value_print', 'children'),
    Input('select_project', 'value'),
    Input('select_date', 'date')
    )
def get_collateral_value(selected_project, selected_date):
    
    # Create a copy of the data
    df_copy = df
    
    collateral_val = df_copy['collateral_value'][(df_copy.project_name == selected_project) & (df_copy.date == selected_date)].values[0]
    
    return f'The collateral value for {selected_project} on {selected_date} was {collateral_val: .2f} Eth'


@app.callback(
    Output('collateral_value_plot', 'figure'),
    Input('select_project', 'value'))
def build_graph(selected_project):
    
    # Create a copy of the data
    df_copy = df
    
    # Filter the data to only use the selected project
    df_copy = df_copy[df_copy.project_name == selected_project]
    
    
    fig = px.line(
        df_copy, 
        x = 'date', 
        y = 'collateral_value',
        labels = {
            'date': 'Date',
            'collateral_value': 'Collateral Value (Eth)'})
        
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)