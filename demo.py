import plotly.graph_objects as go

import pandas as pd
import io
import requests

import plotly.express as px
import matplotlib.pyplot as plt

# my_url = 'https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv'
# proxy_dict = {
#     'https': 'http://127.0.0.1:10809'
# }
# s = requests.get(my_url, proxies=proxy_dict).text
# csv = pd.read_csv(io.StringIO(s))
# counted = csv.groupby(['Country']).size()
# counted.to_csv("./counted.csv")
df_num = pd.read_csv('./counted.csv')

# import seaborn as sns
# sns.set(style="darkgrid")
# sns.histplot(data=df, x="0")
# plt.show();

df = px.data.gapminder()
df_merged = pd.merge(df, df_num, on='country')

fig = px.choropleth(df_merged,
                    locations="iso_alpha",
                    color="num",
                    hover_name="country")
fig.show()

# fig = px.choropleth(df, locations='', color='unemp',
#                            color_continuous_scale="Viridis",
#                            range_color=(0, 12),
#                            scope="usa",
#                            labels={'unemp':'unemployment rate'}
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()


fig.show()
