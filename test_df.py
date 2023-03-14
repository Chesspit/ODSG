
import plotly.express as px
import pandas as pd


df = pd.read_csv('entsorgungsstatistik-stadt-stgallen.csv' , sep=";")

df2=df.drop(df.columns[[3, 4, 5, 6, 8]], axis=1)
df3 = df2.drop(df2[df2['Abfallfraktion'] != 'Sonderabfall'].index)
df3[['year', 'month']] = df3['Monat_Jahr'].str.split('-', expand=True).astype(int)
df3.drop(columns=['Monat_Jahr'], inplace=True)
print('df3', df3)
filtered_df = df3.loc[(df3['year'] == 2022) & (df3['Unterkategorie'] == 'Laugen')]
print(filtered_df)


