import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import io
import requests

# 获取最新的疫情数据
my_url = 'https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv'
proxy_dict = {
    'https': 'http://127.0.0.1:10809'
}
s = requests.get(my_url, proxies=proxy_dict).text
df = pd.read_csv(io.StringIO(s))

# 处理数据
# df.rename(columns={'Country': 'country'}, inplace=True)
df_grouped = df.groupby(['Country_ISO3', 'Country']).size().reset_index(name='Confirmed & Suspected')
df_grouped.rename(columns={'Country_ISO3': 'iso_alpha', '0': 'Confirmed & Suspected'}, inplace=True)

# 获取地理数据，合并数据
df_geo = px.data.gapminder().query("year==2007")
df_merged = pd.merge(df_geo, df_grouped, on='iso_alpha')
df_merged.sort_values(by=['Confirmed & Suspected'], ascending=False, inplace=True)

# choropleth展示
fig = px.choropleth(df_merged,
                    locations="iso_alpha",
                    color="Confirmed & Suspected",
                    hover_name="country",
                    hover_data=['Confirmed & Suspected'])

import dash
from dash import dcc
from dash import html

app = dash.Dash()


def generate_table(df_grouped, max_rows=200):
    return html.Table([
        html.Thead(
            # html.Tr([html.Th(col) for col in df_grouped.columns])
            html.Tr([html.Th('Country'), html.Th('Numbers')])
        ),
        html.Tbody([
            html.Tr([
                # html.Td(df_grouped.iloc[i][col]) for col in df_grouped.columns
                html.Td(df_grouped.iloc[i][col]) for col in ['Country', 'Confirmed & Suspected']
            ]) for i in range(min(len(df_grouped), max_rows))
        ])
    ])


colors = {
    'background': '#FFF',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='全球猴痘疫情实时数据',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    # html.Div(children='全球猴痘疫情地图', style={
    #     'textAlign': 'center',
    #     'color': colors['text']
    # }),
    html.Div(children=[
        html.Div(
            style={'width': '65%', 'float': 'left'},
            children=[dcc.Graph(figure=fig)]
        ),
        html.Div(
            style={'width': '30%', 'float': 'right'},
            children=[
                html.H4(children='各国猴痘疫情数据'),
                generate_table(df_merged)
            ]
        )
    ])
])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
