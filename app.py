import os

import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(
    page_title="iMammalia App", page_icon="📊" #
)

#main_container=st.container()

st.title('iMammalia App')

#load your data of iMammalia and create the list of species in it
dm = pd.read_csv('imammalia.csv')
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
st.metric('IUCN status', estado_iucn)

st.metric('iMammalia registers', len(dm_specie))
st.metric('GBIF registers', len(gbif_df))

gbif_coords = gbif_df[['lon', 'lat']].dropna()
dm_specie = dm_specie[['lon', 'lat']].dropna()

# st.map(gbif_df)


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



st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=55.5,
         longitude=8,
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
