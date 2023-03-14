from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('entsorgungsstatistik-stadt-stgallen.csv' , sep=";")

df2=df.drop(df.columns[[3, 4, 5, 6, 8]], axis=1)
df3 = df2.drop(df2[df2['Abfallfraktion'] != 'Sonderabfall'].index)
df3[['year', 'month']] = df3['Monat_Jahr'].str.split('-', expand=True).astype(int)
df3.drop(columns=['Monat_Jahr'], inplace=True)
# print(df3)
filtered_df = df3[df3['year'].between(2017, 2019)]
print(filtered_df)


app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Checklist(
                df3['Unterkategorie'].unique(),
                id='xaxis-column',
                inline=False
            )
        ], style={'width': '28%'})
    ]),

    dcc.Graph(id='graph'),
    
    dcc.RangeSlider(15, 22, 1, value=[18, 20], id='my-range-slider')
    
    # ,
    # html.Div(id='output-container')

])

# @app.callback(
#     Output('output-container', 'children'),
#     Input('my-range-slider', 'value')
# )
# def update_output(value):
#     return f"Current values: {value}"

@app.callback(
    Output('graph', 'figure'),
    Input('my-range-slider', 'range')
)

def update_figure(selected_range):
    filtered_df = df3[df3['year'].between(2018, 2020)]

    fig = px.line(filtered_df, x='year', y='Unterkategorie', title='huhu')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
