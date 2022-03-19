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

###Define color theme
##libraries for define theme
#import requests
#from pathlib import Path
#import random
#import utils
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