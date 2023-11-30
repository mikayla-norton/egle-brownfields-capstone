import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import math

plt.rcParams.update({'text.color': "white",
                    'axes.labelcolor': "white",
                    'axes.edgecolor': 'white',
                    'xtick.color': 'white',
                    'ytick.color': 'white',
                    'figure.facecolor': '0F1116',
                    'axes.facecolor': '0F1116'})

st.set_page_config(layout="wide")
st.title("EGLE x MSDS Capstone - Brownfields Reporting")
st.text("Mikayla Norton, Yuhan Zhu, Aditya Lakshmi Narayanan, Graham Diedrich")

col1, col2, col3= st.columns([1,4, 1])

col1.subheader("Project Background")

col1.write("The primary objective of this project is to empower users in evaluating various factors associated with the revitalization of brownfield sites for solar energy purposes. The initiative aims to offer users the ability to assign weights to different variables crucial to the redevelopment process. Through this interactive platform, users will have access to a dynamic map that visually highlights the most \"optimal\" sites based on the weighted variables. This innovative approach not only enhances user engagement but also streamlines the decision-making process, facilitating the identification of prime locations for solar energy projects on brownfield sites.")

col1.subheader("Methods")

col1.write("This interactive dashboard synchronizes the use of ArcGIS data with data narrative techniques to visualize brownfield sites around Michigan by county. The platform utilizes Python packages such as Streamlit, Plotly, Geopandas, Folium, and more to accomplish these goals.")

col1.subheader("Discussion")

col1.subheader("References")

col1.subheader("Acknowledgements")

col1.write("The team would like to thank Sarah Hutchinson and all of the sponsors at EGLE. Recognition is also given to the program administration and Dr. Paul Speaker for mentorship throughout the Data Science master's program.")


########## PRE PROCESSING #########
brownfields = pd.read_csv("Brownfields.csv")
brownfields.dropna(subset=['Latitude', 'Longitude'], inplace=True)
brownfields.fillna(value="None", inplace=True)

brownfields["County"] = brownfields["County"].str.title().str.strip()
brownfields["County"].replace("Genessee", "Genesee", inplace=True)
brownfields["County"].replace("Houghton/ Keweenaw", "Houghton", inplace=True)
brownfields["County"].replace("Safinaw", "Saginaw", inplace=True)
brownfields["County"].replace("St.", "Saint", regex=True, inplace=True)

for i in brownfields.columns:
    combined = '\t'.join(list(brownfields[i].astype('str')))
    if '$' in combined:
        brownfields[i] = brownfields[i].str.replace("$", "")
    if ',' in combined:
        brownfields[i] = brownfields[i].str.replace(",", "")
    if ' ' in combined:
        brownfields[i] = brownfields[i].str.strip()


gpd_file = gpd.read_file("Counties_(v17a)/Counties_(v17a).shp")

# map_and_stats=mi_shp.merge(brownfields, on="NAME")
# map_and_stats["TotalBrownfieldIncentives"] = map_and_stats["TotalBrownfieldIncentives"].replace(np.nan, 0)

########## PLOTTING ###############
opts = brownfields.columns[5:]
opts = opts.drop(["Latitude", "Longitude"])
counties = list(brownfields["County"].unique())
counties.sort()
counties.insert(0, "All")

col3.subheader("Search")
projects = list(brownfields["ProjectName"].unique())
projects.insert(0,'')
proj = col3.selectbox("Please enter the specific project you are searching for", projects, 0)
if proj != '':
    df_filtered = brownfields[brownfields["ProjectName"]==proj]
    selections = None

else:
    
    col3.subheader("Filters")


    selections = col3.multiselect("Please select sub-information to display in data labels", opts, default=['AwardDateYearFunded', 'City', 'SiteAddress'])

    county_pick = col3.multiselect("Select Counties", counties, default=["All"])

    if "All" not in county_pick:
        df_filtered = brownfields[brownfields["County"].isin(list(county_pick))]
    else:
        df_filtered = brownfields


    devs = list(brownfields["DevelopmentType"].unique())
    devs.sort()
    devs.insert(0, "All")
    dev_pick = col3.multiselect("Select Development Type", devs, default=["All"])
    if "All" not in dev_pick:
        df_filtered = df_filtered[df_filtered["DevelopmentType"].isin(list(dev_pick))] #### Clean this??


    ####### INTERVAL METRICS #########    

    col3.divider()

    def roundup(x):
        x_str = str(int(x))
        l = len(x_str)
        exp = l-1
        return int(math.ceil(x / (10**exp))) * 10**exp


    num_cols = ['TotalBrownfieldIncentives', 'F381ApprovedAmount',
            'GrantAwardAmount', 'LoanAwardAmount', 'WaterfrontAwardAmount', 'Acreage']
    binary = col3.checkbox("Would you like to filter the output by a numeric column?")
    if binary:
        col_pick = col3.selectbox("Please select a column to filter by", num_cols, 0)
        if col_pick is not None:
            tail = col3.selectbox("Which direction would you like to apply this filter?", ["Greater than", "Less than"])
            center = col3.slider("Select an endpoint", 0, roundup(np.nanmax((pd.to_numeric(df_filtered[col_pick].unique(), errors='coerce')))), round(np.nanmax((pd.to_numeric(df_filtered[col_pick].unique(), errors='coerce')))/2))
            if tail == 'Greater than':
                df_filtered = df_filtered[pd.to_numeric(df_filtered[col_pick], errors='coerce').notnull()]
                df_filtered = df_filtered[pd.to_numeric(df_filtered[col_pick]) > center]
            elif tail == 'Less than':
                df_filtered = df_filtered[pd.to_numeric(df_filtered[col_pick], errors='coerce').notnull()]
                df_filtered = df_filtered[pd.to_numeric(df_filtered[col_pick]) < center]
        else:
            df_filtered = df_filtered
    else:
        df_filtered = df_filtered



####### PLOTTING ###############
map = folium.Map(location=[44.75, -85], 
                zoom_start=7, 
                control_scale=True, 
                zoom_control=True,
                scrollWheelZoom=False,
                dragging=True)
for index, location_info in df_filtered.iterrows():
    html=f"""
        <h4>Project Name: {location_info['ProjectName']}</h4> """
    if selections is not None:
        for i in selections:
            html = html + f"""
            <p style="font-size:75%;">{i}: {location_info[i]}</p>
            """  
    if col_pick is not None:
        html = html + f"""
        <p style="font-size:75%;">{col_pick}: {location_info[col_pick]}</p>
        """

    iframe = folium.IFrame(html=html, width=200, height=200)
    popup = folium.Popup(iframe, max_width=1000)

    folium.Marker([location_info["Latitude"], location_info["Longitude"]], popup=popup).add_to(map)

folium.raster_layers.ImageOverlay(
    image="mi_map.png",
    name="Michigan County Map",
    bounds=[[41.7, -90.5], [47.45, -82.4]],
    opacity=1,
    interactive=False,
    cross_origin=False,
    zindex=1,
    alt="mi-map.png",
).add_to(map)
map.fit_bounds(map.get_bounds(), padding=(30, 30))

folium.LayerControl().add_to(map)



with col2:
    st_data = st_folium(map, width=1200, height=1200)



########## TABLE ############
col3.divider()
n = col3.select_slider("Please select number of entries for data table", options=list(range(1, len(brownfields["County"].value_counts()))), value=10)
col3.table(pd.DataFrame(brownfields["County"].value_counts()).rename(columns={"count": "Brownfield Quantity"}).head(n))

# df2 = pd.DataFrame(map_and_stats)
# col2.dataframe(df2.head())
