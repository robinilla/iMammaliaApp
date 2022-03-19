import os

#general libraries for the package
import streamlit as st
import pandas as pd
import pydeck as pdk
#import numpy as np

from PIL import Image, ImageOps

st.set_page_config(
    page_title="Mammalnet", page_icon="🐾"
)

##Define color theme
##libraries for define theme
#import requests
#from pathlib import Path
#import random
#
#
#import utils
#
#
#utils.local_css("local_styles.css")
#
## Init state. This is only run whenever a new session starts (i.e. each time a new
## browser tab is opened).
#if not st.session_state:
#    st.session_state.primaryColor = "#27a5da"
#    st.session_state.backgroundColor = "#f7fbfd"
#    st.session_state.secondaryBackgroundColor = "#d6dcde"
#    st.session_state.textColor = "#171b29"
#    st.session_state.is_dark_theme = True
#    st.session_state.first_time = True
#

st.image('https://mammalnet.net/wp-content/uploads/2021/04/cropped-logo.png', width=400)
st.write('Comparing data collected from citizen science _versus_ data available in the Global Biodiversity Information Facilities (','[GBIF](https://www.gbif.org/)', ').')

#"---"

#load your data of iMammalia and create the list of species in it
dm = pd.read_csv('imammalia.csv', encoding='latin-1')
dm = dm.loc[(dm['Record.status'] == 'V')]
dm=dm.loc[(dm['Taxon.accepted.name'] != 'Sciurus meridionalis') & (dm['Taxon.accepted.name'] != 'Arvicola terrestris') & (dm['Taxon.accepted.name'] != 'Herpestes auropunctatus') & (dm['Taxon.accepted.name'] != 'Clethrionomys glareolus')]
dm.loc[dm['Taxon.accepted.name'] == 'Mus domesticus', 'Taxon.accepted.name'] = 'Mus musculus'
unique_species = dm['Taxon.accepted.name'].sort_values().unique()

dm = dm.rename(columns={'long': 'lon'})
unique_species = dm['Taxon.accepted.name'].sort_values().unique()
unique_species = [s for s in unique_species if len(s.split(' ')) == 2]

specie = st.selectbox('Select a species registered in Mammalnet', unique_species)
dm_specie = dm.loc[dm['Taxon.accepted.name'] == specie]

#load your data of iMammalia and create the list of species in it
gb_path = pd.read_csv('gbif_path.csv')

gbif_specie = [f for f in os.listdir('species') if f.startswith(specie.lower().replace(' ', '_'))][0]
gbif_df = pd.read_csv(os.path.join('species', gbif_specie))

estado_iucn = gbif_df['iucnRedListCategory'].unique()[0]

st.markdown('[Information related with the species](https://www.google.com/search?q='+specie.replace(" ", "+")+'+species)')
st.markdown('[Contribute with more observation of the species](https://mammalnet.net/es/imammalia)')
st.markdown('[Share your camera traps photos](https://www.mammalweb.org/en/login)')

"---"

with st.container():
    st.write('Species registers')
    col1, col2, col3 = st.columns(3)
    col1.metric('iMammalia registers', len(dm_specie))
    
"---"

#gbif_icon = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
 #   "url": "https://www.gbif.org/favicon.ico",
  #  "width": 25,
   # "height": 25,
    #"anchorY": 25,
#}

#gbif_coords["gbif_icon"] = None
#for i in gbif_coords.index:
#   gbif_coords["gbif_icon"][i] = gbif_icon


st.subheader('Distribution of '+specie)
slider_range=st.slider('Select year for GBIF observed data', min_value=1900, max_value=2022, 
                       value=[1993, 2022])
year_min=slider_range[0]
year_max=slider_range[1]

gbif_df['year']=pd.to_numeric(gbif_df['year'])
gbif_df = gbif_df.loc[(gbif_df['year'] >= year_min) & (gbif_df['year'] <= year_max)]

coords_options=['coordinateUncertaintyInMeters', 'coordinatePrecision']
page=st.radio('Select field for GBIF coordinate precision:', coords_options)
if page == 'coordinatePrecision':
    gbif_df = gbif_df.loc[gbif_df['coordinatePrecision'] <= 2000]
else:
    gbif_df = gbif_df.loc[gbif_df['coordinateUncertaintyInMeters'] <= 2000]

gbif_coords = gbif_df[['lon', 'lat']].dropna()
dm_specie = dm_specie.dropna(subset=['lon', 'lat'])
dm_specie=dm_specie[['lon', 'lat', 'Recorded.by', 'Date.end']]
#st.write(dm_specie)

col2.metric('GBIF registers (total in the world)', len(gbif_coords))
col3.metric('IUCN status', estado_iucn)

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=56.5,
         longitude=9.5,
         zoom=2.25
     ),
     layers=[
           pdk.Layer(
              'ScatterplotLayer',
              data=gbif_coords,
             pickable=True,
             opacity=0.1,
             stroked=True,
             filled=True,
             radius_scale=6,
             radius_min_pixels=5,
             radius_max_pixels=100,
             line_width_min_pixels=1,
             get_line_color=[0, 0, 0],
             get_fill_color=[22, 175, 78],
             get_position='[lon, lat]'
          ),
         pdk.Layer(
            'ScatterplotLayer',
            data=dm_specie,
            pickable=True,
            opacity=0.2,
            stroked=True,
            filled=True,
            radius_scale=5,
            radius_min_pixels=5,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_line_color=[0, 0, 0],
            get_fill_color=[235, 235, 66],
            get_position='[lon, lat]'
         )
     ],
    tooltip={"html": "<b>Date: </b> {Date.end} <br /> "
                  "<b>Recorded by: </b> {Recorded.by} <br /> "}
 ))




col4, col5 = st.columns([0.35, 0.65])
img4 = Image.new(mode = "RGB", size = (10, 10), color = (22, 175, 78))
img5 = Image.new(mode = "RGB", size = (10, 10), color =(235, 235, 66))
col4.write('GBIF data')
col4.image(img4, width=10)
col5.write('MammalNet data')
col5.image(img5, width=10)


doi=gb_path.loc[gb_path['spMammalnet']==specie]
doi2=doi['doi']

st.markdown('_GBIF data showed correspond to a dataset downloaded the 2022-03-15, which doi is_ '+doi2.iloc[0]+'. _They have been filtered to a coordinate precision or coordinate uncertainity in meters equal or below to 2000m. NA decimal Longitude/Latitude values cannot be shown and are not considered in the register count. The GBIF register count comprends between year_ '+str(year_min)+' _and year_ '+str(year_max)+' _selected in the slidebar._')

""
""

st.markdown('Aknowledges to [Álvaro Arredondo](https://github.com/arredond) for helping in the app development.')

