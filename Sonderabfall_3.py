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
# df4 = df3.groupby(['year', 'Unterkategorie']).sum()
# print(df4)
# filtered_df = df3.loc[(df3['year'] == 2022) & (df3['Unterkategorie'] == 'Laugen')]
# print(filtered_df)


app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                df3['Unterkategorie'].unique(),
                'Laugen',
                id='dd',

            )
        ], style={'width': '28%'})
    ]),

    dcc.Graph(id='graph'),
    
    dcc.Slider(15, 22, 1, value=18, id='my-slider')
    
    ,
    html.Div(id='output-container')

])

@app.callback(
    Output('output-container', 'children'),
    Input('my-slider', 'value'),
    Input('dd', 'value')    
)
def update_output(year_value, kat_value):
    filtered_df1 = df3[df3['year'] == year_value]
    filtered_df2 = filtered_df1[filtered_df1['Unterkategorie'] == kat_value]
    

    return f"Current df: {kat_value}, {year_value},{filtered_df1}, {filtered_df2}"
   


@app.callback(
    Output('graph', 'figure'),
    Input('my-slider', 'value'),
    Input('dd', 'value')
)

def update_figure(year_value, kat_value):
    filtered_df = df3.loc[(df3['year'] == year_value) & (df3['Unterkategorie'] == kat_value)]

    fig = px.scatter(filtered_df, x='month', y='Unterkategorie', size='Gewicht in kg', title='huhu')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port = 8055)
