from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)
server = app.server

df = pd.read_csv('entsorgungsstatistik-stadt-stgallen.csv' , sep=";")

df2=df.drop(df.columns[[3, 4, 5, 6, 8]], axis=1)
df3 = df2.drop(df2[df2['Abfallfraktion'] != 'Sonderabfall'].index)
df3[['year', 'month']] = df3['Monat_Jahr'].str.split('-', expand=True).astype(int)
df3.drop(columns=['Monat_Jahr'], inplace=True)
df4 = df3.groupby(['year', 'Unterkategorie'], as_index=False)['Gewicht in kg'].agg('sum')
print('df4', df4)



app.layout = html.Div([
    html.Div([

        html.Div([
            html.P('Bitte Kategorien auswählen'),
            dcc.Dropdown(
                df3['Unterkategorie'].unique(),
                multi = True,
                value = ['Laugen', 'Säuren'],
                id='dd',

            )
        ], style={'width': '28%'})
    ]),

    dcc.Graph(id='graph'),
    
    dcc.RangeSlider(2015, 2023, 1, value=[2018, 2021], id='my-range-slider')
    
    ,
    html.Div(id='output-container')

])

# @app.callback(
#     Output('output-container', 'children'),
#     Input('my-slider', 'value'),
#     Input('dd', 'value')    
# )
# def update_output(year_value, kat_value):
#     filtered_df = df3.loc[(df3['year'] == 2022) & (df3['Unterkategorie'] == kat_value)]
#     return f"Current df: {kat_value}, {year_value}, {filtered_df}"


@app.callback(
    Output('graph', 'figure'),
    Output('output-container', 'children'),    
    Input('my-range-slider', 'value'),
    Input('dd', 'value')
)

def update_figure(year_value, kat_value):
    # f_df = df3[df3['year'] == year_value]
    # filtered_df = f_df[f_df['Unterkategorie'].isin(kat_value)] 
    # filtered_df = df4.loc[(df4['year'].isin(year_value)) & (df4['Unterkategorie'].isin(kat_value))]
    filtered_df = df4.loc[(df4['year'] >= (year_value[0])) & (df4['year'] <= (year_value[1])) & (df4['Unterkategorie'].isin(kat_value))]

    fig = px.scatter(filtered_df, x='year', y='Gewicht in kg', size='Gewicht in kg', 
                  color='Unterkategorie', hover_data=['Gewicht in kg'])
    return fig, f"Current df: {year_value}, {kat_value}, {filtered_df}"



if __name__ == '__main__':
    app.run_server(debug=True, port = 8055)
