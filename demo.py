import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import io
import requests

# my_url = 'https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv'
# proxy_dict = {
#     'https': 'http://127.0.0.1:10809'
# }
# s = requests.get(my_url, proxies=proxy_dict).text
# csv = pd.read_csv(io.StringIO(s))
# counted = csv.groupby(['Country']).size()
# counted.to_csv("./counted.csv")
df_counted = pd.read_csv('./counted.csv')
df = px.data.gapminder().query("year==2007")
df_merged = pd.merge(df, df_counted, on='country')
fig = px.choropleth(df_merged,
                    locations="iso_alpha",
                    color="num",
                    hover_name="country",
                    hover_data=['num'])
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
