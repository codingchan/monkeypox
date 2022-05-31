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
df_grouped = df.groupby('Country_ISO3').size().reset_index(name='num')
df_grouped.rename(columns={'Country_ISO3': 'iso_alpha', '0': 'num'}, inplace=True)

# 获取地理数据，合并数据
df_geo = px.data.gapminder().query("year==2007")
df_merged = pd.merge(df_geo, df_grouped, on='iso_alpha')

# choropleth展示
fig = px.choropleth(df_merged,
                    locations="iso_alpha",
                    color="num",
                    hover_name="country",
                    hover_data=['num'])

import dash
from dash import dcc
from dash import html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter