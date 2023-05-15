from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

import math

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = pd.read_csv("entsorgungsstatistik-stadt-stgallen.csv", sep=";")

df2 = df.drop(df.columns[[3, 4, 5, 6, 8]], axis=1)
df3 = df2.drop(df2[df2["Abfallfraktion"] != "Sonderabfall"].index)
df3[["year", "month"]] = df3["Monat_Jahr"].str.split("-", expand=True).astype(int)
df3.drop(columns=["Monat_Jahr"], inplace=True)
df4 = df3.groupby(["year", "Unterkategorie"], as_index=False)["Gewicht in kg"].agg(
    "sum"
)
# print("df4", df4)

app.layout = dbc.Container(
    [dbc.Row
     ([dbc.Col(html.H2("Huhu, hier bin ich!",    
                       className='test-center text-danger, mb-4'),
                       width=12)
    ]), 
     dbc.Row([
         dbc.Col([
             dcc.Dropdown(id='dd', multi=False, value='Laugen',
                          options=[{'label': x, 'value': x} 
                                   for x in sorted(df4['Unterkategorie'].unique())]),
             dcc.Graph(id='line_fig', figure={})
         ], width={'size':5, 'offset':1}),
          dbc.Col([
             dcc.Dropdown(id='dd2', multi=True, value=['Hg Bruch', 'Laugen'],
                          options=[{'label': x, 'value': x} 
                                   for x in sorted(df4['Unterkategorie'].unique())]),
             dcc.Graph(id='line_fig2', figure={})
         ], width={'size':5, 'offset':1})        
     ]), 
     dbc.Row([
         
     ])
], fluid=True)


if __name__ == "__main__":
    app.run_server(debug=True, port=8055)
