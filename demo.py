import plotly.graph_objects as go

import pandas as pd
import io
import requests

my_url = 'https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv'
proxy_dict = {
    'https': 'http://127.0.0.1:10809'
}
s = requests.get(my_url, proxies=proxy_dict).text
csv = pd.read_csv(io.StringIO(s))
counted = csv.groupby(['Country']).size()
counted.to_csv("./counted.csv")
df = pd.read_csv('./counted.csv')

df = px.data.gapminder()
fig = px.choropleth(df, locations="iso_alpha", color="lifeExp", hover_name="country", animation_frame="year", range_color=[20,80])
fig.show()

import plotly.express as px

fig = px.choropleth(df, geojson=counties, locations='', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           scope="usa",
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
