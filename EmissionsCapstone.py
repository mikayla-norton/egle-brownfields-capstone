import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import geopandas as gpd

plt.rcParams.update({'text.color': "white",
                    'axes.labelcolor': "white",
                    'axes.edgecolor': 'white',
                    'xtick.color': 'white',
                    'ytick.color': 'white',
                    'figure.facecolor': '0F1116',
                    'axes.facecolor': '0F1116'})

st.set_page_config(layout="wide")
st.title("EGLE x MSDS Capstone - Brownfields Reporting")

col1, col2= st.columns([1,4])

col1.subheader("Project Background")

col1.write("The primary objective of this project is to empower users in evaluating various factors associated with the revitalization of brownfield sites for solar energy purposes. The initiative aims to offer users the ability to assign weights to different variables crucial to the redevelopment process. Through this interactive platform, users will have access to a dynamic map that visually highlights the most \"optimal\" sites based on the weighted variables. This innovative approach not only enhances user engagement but also streamlines the decision-making process, facilitating the identification of prime locations for solar energy projects on brownfield sites.")

brownfields = pd.read_csv("Brownfields.csv")


mi_shp = gpd.read_file("Counties_(v17a)/Counties_(v17a).shp")

########## PRE PROCESSING #########
brownfields["County"] = brownfields["County"].str.lower().str.replace(" ", "")
brownfields = brownfields.rename(columns={'County': 'NAME'})
mi_shp["NAME"] = mi_shp["NAME"].str.lower().str.replace(" ", "")

map_and_stats=mi_shp.merge(brownfields, on="NAME")
map_and_stats["TotalBrownfieldIncentives"] = map_and_stats["TotalBrownfieldIncentives"].replace(np.nan, 0)

########## PLOTTING ###############
# st.write(map_and_stats)

fig =px.scatter_geo(map_and_stats,
                    lat=map_and_stats.Latitude,
                    lon=map_and_stats.Longitude,
                    hover_name="ProjectName", scope="usa", size="TotalBrownfieldIncentives",color="PENINSULA", width=900, height=900)
fig.update_geos(showcoastlines=True, coastlinecolor="white", coastlinewidth=1)

lat_foc = 44.3148
lon_foc = -85.6024
fig.update_layout(geo=dict(projection_scale=5, center=dict(lat=lat_foc, lon=lon_foc), 
                        bgcolor='rgba(15, 17, 22,1)'))

col2.plotly_chart(fig)

st.write(map_and_stats)

#col2.header("Annual Per Capita Emissions")
#y = col2.slider("Year Selection", min(df["Year"]), max(df["Year"]), step = 1, value=2021)

# df = df.rename(columns={'Alpha-3 code': 'alpha-3'})
# regions_df = df.merge(regions, on="alpha-3")

# regions_df = regions_df.rename(columns={'alpha-3': 'iso3'})
# dfyear = regions_df.loc[regions_df["Year"] == y]

# map_and_stats=world_map.merge(dfyear, on="iso3")
# map_and_stats = map_and_stats.rename(columns={'region_y': 'Major Region'})
# map_and_stats = map_and_stats.rename(columns={'name_x': 'Country'})

# ########### WORLD MAP ############
# fig = px.scatter_geo(map_and_stats, locations="iso3",
#                     size="Per Capita",hover_name="Country",color="Major Region", width=900)
# fig.update_geos(showcoastlines=True, coastlinecolor="white", coastlinewidth=1)

# fig.update_layout(geo=dict(bgcolor='rgba(15, 17, 22,1)'))

# col2.plotly_chart(fig)
# col2.divider()