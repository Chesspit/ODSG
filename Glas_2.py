import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = pd.read_csv('entsorgungsstatistik-stadt-stgallen.csv' , sep=";")
df=df.drop(df.columns[3:8], axis=1)
df=df[df['Abfallfraktion'] == 'Glas']
df=df[df['Unterkategorie'].isna()]
df.sort_values('Monat_Jahr', inplace=True)
df['Jahr'] = df['Monat_Jahr'].str.split('-').str[0].astype(int)
df['Monat'] = df['Monat_Jahr'].str.split('-').str[1].astype(int)

# print(df)
# print(df.dtypes)

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody("Hier gehts los...")
            )
        )
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody("This is some text within a card body"), className="mb-8",
            ),
            dcc.RangeSlider(min=2015, max=2023, step=1, value=[2018, 2021], id='my-range-slider', marks={ i: f"{i:.0f}" for i in range(2015, 2023, 1)})
        ], width = 4),
        dbc.Col([
            dbc.Card(
                dbc.CardBody("This is some other text within a card body"), className="mb-3",
            ),
            dcc.Graph(id="line")
            ], width = 8
        )
    ])
])

@app.callback(
    Output("line", "figure"),
    Input("my-range-slider", "value"),
)
def update_chart(slider_range):
    low, high = slider_range
    mask = (df["Jahr"] >= low) & (df["Jahr"] <= high)
    fig = px.bar(
        df[mask],
        x="Monat_Jahr",
        y="Gewicht in t",
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port = 8055)