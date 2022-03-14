import os

import streamlit as st
import pandas as pd
import pydeck as pdk


st.set_page_config(
    page_title="GBIF vs Imammalia", page_icon="📊"
)

st.title('GBIF')

#load your data of iMammalia and create the list of species in it
dm = pd.read_csv('imammalia.csv')
unique_species = dm['Taxon.accepted.name'].sort_values().unique()

dm = dm.rename(columns={'long': 'lon'})
unique_species = dm['Taxon.accepted.name'].sort_values().unique()
unique_species = [s for s in unique_species if len(s.split(' ')) == 2]

specie = st.selectbox('Select a species', unique_species)
dm_specie = dm.loc[dm['Taxon.accepted.name'] == specie]

gbif_specie = [f for f in os.listdir('species') if f.startswith(specie.lower().replace(' ', '_'))][0]
gbif_df = pd.read_csv(os.path.join('species', gbif_specie))


st.dataframe(gbif_df)
# st.map(gbif_df)

gbif_coords = gbif_df[['lon', 'lat']].dropna()
dm_specie = dm_specie[['lon', 'lat']].dropna()

# st.map(gbif_df)


st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=40,
         longitude=-3,
         zoom=6
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
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position='[lon, lat]'
         ),
         pdk.Layer(
            'ScatterplotLayer',
            data=dm_specie,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=5,
            radius_min_pixels=10,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_line_color=[255, 0, 0],
            get_fill_color=[255, 0, 0],
            get_position='[lon, lat]'
         )
     ]
 ))
