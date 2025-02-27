import folium
import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu   

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
        default_index=2,
        orientation="horizontal",
    )

if selected == 'Feminicidio':
    st.switch_page("main.py")
elif selected == 'Violência doméstica':
    st.switch_page("pages/violencia.py")

df_violencia = pd.read_csv("data/violencia_domestica_ses.csv")
df_municipios = pd.read_csv("data/municipios.csv")

df_violencia['dt_notific'] = pd.to_datetime(df_violencia['dt_notific'], dayfirst=True)
df_municipios['codigo_ibge'] = df_municipios['codigo_ibge'].astype(str).str[:-1]
df_minas_gerais = df_municipios[df_municipios['codigo_ibge'].str[:2] == '31']  # Filtra municípios de MG (código IBGE começa com '31')

df = df_violencia.merge(
    df_minas_gerais[['nome', 'latitude', 'longitude']],
    left_on='id_mn_resi', right_on='nome', how='left'
)

st.title("Violência Doméstica em Minas Gerais")

fig_ano = px.histogram(df, x='ano', title='Evolução dos Casos por Ano', nbins=len(df['ano'].unique()))
st.plotly_chart(fig_ano, use_container_width=True)

fig_idade = px.histogram(df, x='nu_idade_n', title='Distribuição por Idade', nbins=30)
st.plotly_chart(fig_idade, use_container_width=True)

fig_raca = px.histogram(df, x='cs_raca', title='Distribuição por Raça', color='cs_raca')
st.plotly_chart(fig_raca, use_container_width=True)

fig_local = px.histogram(df, x='local_ocor', title='Locais das Ocorrências', color='local_ocor')
st.plotly_chart(fig_local, use_container_width=True)