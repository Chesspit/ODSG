import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash
import plotly.express as px
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = pd.read_csv('entsorgungsstatistik-stadt-stgallen.csv' , sep=";")
df=df.drop(df.columns[3:8], axis=1)

# # Die Verwendung von .index erzeugt eine Liste mit den Reihennummer, die nicht 'Glas' sind
# help_i=df[df['Abfallfraktion'] != 'Glas'].index
# print('index : ', help_i)


df = df.drop(df[df['Abfallfraktion'] != 'Glas'].index)
# df[['year', 'month']] = df['Monat_Jahr'].str.split('-', expand=True).astype(int)
# df.drop(columns=['Monat_Jahr'], inplace=True)
df = df.reset_index(drop=True)

print(df.head())

fig = px.line(df, x="Monat_Jahr", y="Gewicht in t")

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody("This is some text within a card body"), className="mb-8",
            ),
            dcc.RangeSlider(2015, 2023, 1, value=[2018, 2021], id='my-range-slider')
        ], width = 4),
        dbc.Col([
            dbc.Card(
                dbc.CardBody("This is some other text within a card body"), className="mb-3",
            ),
            dcc.Graph(figure=fig)
            ], width = 8
        )
    ])
])



if __name__ == '__main__':
    app.run_server(debug=True, port = 8055)
