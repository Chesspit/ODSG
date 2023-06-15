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

heading = html.H4(
    "Abfallmengen in der Stadt St. Gallen", className="bg-primary text-white p-2"
)

control_des = dbc.CardBody("This is some text within a card body")

control = dcc.RangeSlider(min=2015, max=2023, step=1, value=[2018, 2021], id='my-range-slider', marks={ i: f"{i:.0f}" for i in range(2015, 2023, 1)})

gesamt_des = dbc.CardBody("This is again some text within a card body")

graph_gesamt = dcc.Graph(id="bar")

saison_des = dbc.CardBody("This is once again some text within a card body")

graph_saison = dcc.Graph(id="lines")



app.layout = html.Div(
    [heading, 
     html.Hr(), 
     dbc.Row([dbc.Col(control_des, md=4), dbc.Col(control, md=8)]),
     dbc.Row([dbc.Col(gesamt_des, md=4), dbc.Col(graph_gesamt, md=8)]),
     dbc.Row([dbc.Col(saison_des, md=4), dbc.Col(graph_saison, md=8)])]
)


@app.callback(
    Output("bar", "figure"),
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