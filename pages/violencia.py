import folium
import streamlit as st
import geopandas as gpd
import pandas as pd 
import plotly.express as px

from streamlit_folium import st_folium
from streamlit_option_menu import option_menu   
from folium.plugins import MarkerCluster

st.set_page_config(
    page_title='Monitora',
    layout="wide",
    initial_sidebar_state='expanded'
)

st.sidebar.image('icone.jpeg')

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Feminicídios", "Violência doméstica", "Secretária de saúde"],
        icons=["house", "filter", "info-circle"],
        menu_icon="cast",
        default_index=1,
        orientation="horizontal",
    )

if selected == 'Feminicídios':
    st.switch_page("pages/feminicidio.py")
elif selected == 'Secretária de saúde':
    st.switch_page("pages/saude.py")

df_violencia = pd.read_csv("data/violencia_domestica_policia.csv")
df_violencia['data_fato'] = pd.to_datetime(df_violencia['data_fato'].str.strip(), format="%Y-%m-%d", errors='coerce')

df_municipios = pd.read_csv("data/municipios.csv")
df_municipios['codigo_ibge'] = df_municipios['codigo_ibge'].astype(str).str[:-1]
df_violencia['municipio_cod'] = df_violencia['municipio_cod'].astype(str)

df = df_violencia.merge(
    df_municipios[['codigo_ibge', 'latitude', 'longitude']], 
    left_on='municipio_cod', 
    right_on='codigo_ibge', 
    how='left'
)

mapa = folium.Map(
    location=(-19.9167, -43.9345),
    control_scale=True,
    zoom_start=6
)

gdf = gpd.read_file('data/BR_UF_2021.shp')
mg = gdf[gdf["NM_UF"] == "Minas Gerais"]
folium.GeoJson(
    mg,
    name="Minas Gerais",
    style_function=lambda x: {
        "fillOpacity": 0,  
        "color": "red",
        "weight": 2
    }
).add_to(mapa)

st.title("Casos de Violência Doméstica em Minas Gerais")

ano_selecionado = st.slider('Selecione o ano', min_value=int(df['ano'].min()), max_value=int(df['ano'].max()), value=int(df['ano'].max()))
natureza_selecionada = st.selectbox('Selecione o tipo de crime', df['natureza_delito'].unique().tolist())

df_ano = df[df['ano'] == ano_selecionado]
df_ano = df_ano[df_ano['natureza_delito'] == natureza_selecionada]

marker_cluster = MarkerCluster().add_to(mapa)
for index, row in df_ano.iterrows(): 
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        icon=folium.Icon(color='red' if row['tentado_consumado'] == 'CONSUMADO' else 'blue')
    ).add_to(marker_cluster)

st_data = st_folium(mapa, width='100%')

st.subheader("Tendência temporal de crimes")
df_tendencia = df.groupby('ano').size().reset_index(name='ocorrencias')
fig_tendencia = px.line(df_tendencia, x='ano', y='ocorrencias', labels={'ano': 'Ano', 'ocorrencias': 'Número de Casos'})
st.plotly_chart(fig_tendencia)