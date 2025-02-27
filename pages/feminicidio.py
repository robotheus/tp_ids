import folium
import streamlit as st
import geopandas as gpd
import pandas as pd 

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
        options=["Feminicídios", "Violência doméstica", "Secretária de saúde",],
        icons=["house", "filter", "info-circle"],
        menu_icon="cast",
        default_index=3,
        orientation="horizontal",
    )

if selected == 'Violência doméstica':
    st.switch_page("pages/violencia.py")
elif selected == 'Secretária de saúde':
    st.switch_page("pages/saude.py")

df_feminicidio = pd.read_csv("data/feminicidio_policia.csv")
df_feminicidio['data_fato'] = pd.to_datetime(df_feminicidio['data_fato'])

df_municipios = pd.read_csv("data/municipios.csv")

df_municipios['codigo_ibge'] = df_municipios['codigo_ibge'].astype(str).str[:-1]
df_feminicidio['municipio_cod'] = df_feminicidio['municipio_cod'].astype(str)

df = df_feminicidio.merge(
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

st.title("Feminicídios em Minas Gerais")
ano_selecionado = st.slider('Selecione o ano', min_value=int(df['ano'].min()), max_value=int(df['ano'].max()), value=int(df['ano'].max()))
df_ano = df[df['ano'] == ano_selecionado]

marker_cluster = MarkerCluster().add_to(mapa)
for index, row in df_ano.iterrows(): 
    if pd.notnull(row['latitude']) and pd.notnull(row['longitude']): 
        popup_content = f"""
        <b>Município:</b> {row['municipio_fato']}<br>
        <b>Status:</b> {row['tentado_consumado']}<br>
        <b>Número de vítimas:</b> {row['qtde_vitimas']}<br>
        <b>Data:</b> {row['data_fato'].strftime('%d/%m/%Y')}<br>
        """
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color='red' if row['tentado_consumado'] == 'CONSUMADO' else 'blue')
        ).add_to(marker_cluster)

tentados = df_ano[df_ano['tentado_consumado'] == 'TENTADO']
consumados = df_ano[df_ano['tentado_consumado'] == 'CONSUMADO']
st.write(f"**Tentativas de feminicídio:** {len(tentados)}")
st.write(f"**Feminicídios consumados:** {len(consumados)}")

st_data = st_folium(mapa, width='100%')