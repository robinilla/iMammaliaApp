import os

import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

st.set_page_config(
    page_title="iMammalia App", page_icon="📊" #
)



st.title('iMammalia App')
st.write('Comparing data collected from citizen science versus data available in the Global Biodiversity Information Facilities (GBIF)')

#load your data of iMammalia and create the list of species in it
dm = pd.read_csv('imammalia.csv')
dm = dm.loc[(dm['Record.status'] == 'V')]
unique_species = dm['Taxon.accepted.name'].sort_values().unique()

dm = dm.rename(columns={'long': 'lon'})
unique_species = dm['Taxon.accepted.name'].sort_values().unique()
unique_species = [s for s in unique_species if len(s.split(' ')) == 2]

specie = st.selectbox('Select a species registered in Mammalnet', unique_species)
dm_specie = dm.loc[dm['Taxon.accepted.name'] == specie]

#load your data of iMammalia and create the list of species in it
gbif_specie = [f for f in os.listdir('species') if f.startswith(specie.lower().replace(' ', '_'))][0]
gbif_df = pd.read_csv(os.path.join('species', gbif_specie))

estado_iucn = gbif_df['iucnRedListCategory'].unique()[0]

st.markdown('[Information related with the species](https://www.google.com/search?q='+specie.replace(" ", "+")+'+species)')
st.markdown('[Contribute with more observation of the species](https://mammalnet.net/es/imammalia)')
st.markdown('[Share your camera traps photos](https://www.mammalweb.org/en/login)')


with st.container():
    st.write('Species registers')
    col1, col2, col3 = st.columns(3)
    col1.metric('iMammalia registers', len(dm_specie))
    col2.metric('GBIF registers (in the world)', len(gbif_df))
    col3.metric('IUCN status', estado_iucn)
    

gbif_coords = gbif_df[['lon', 'lat']].dropna()
dm_specie = dm_specie[['lon', 'lat']].dropna()


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


st.subheader('Distribution of the '+specie)
slider_range=st.slider('Select year for GBIF observed data', min_value=1900, max_value=2022, 
                       value=[2018, 2022])
year_min=slider_range[0]
year_max=slider_range[1]

st.write(year_min)
st.write(year_max)

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=56.5,
         longitude=9,
         zoom=2.5
     ),
     layers=[
         pdk.Layer(
            'ScatterplotLayer',
           # type='IconLayer',
            data=gbif_coords,
            #get_icon="gbif_icon",
            #get_size=4,
            #size_scale=15,
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
     ]
 ))

st.markdown('_GBIF data showed correspond to a dataset downloaded the 2022-03-10, which doi is_ '+'download1[1,2]'+' _and has been filtered to a coordinate precision equal or below to 2000m_.')