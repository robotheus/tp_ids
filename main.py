import folium
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd 

from streamlit_folium import st_folium
from streamlit_option_menu import option_menu   
from folium.plugins import MarkerCluster
from collections import defaultdict

st.set_page_config(
        page_title='Monitora',
        layout="wide",
        initial_sidebar_state='expanded'
    )

st.sidebar.image('icone.jpeg')

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Feminicídios", "Violência doméstica", "Secretária de saúde",],
        icons=["house", "filter", "info-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

if selected == 'Feminicídios':
    st.switch_page("pages/feminicidio.py")
elif selected == 'Violência doméstica':
    st.switch_page("pages/violencia.py")
elif selected == 'Secretária de saúde':
    st.switch_page("pages/violencia.py")
