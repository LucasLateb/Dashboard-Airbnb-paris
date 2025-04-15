import os
import pandas as pd
import streamlit as st
import plotly.express as px

# Configuration de l'app
st.set_page_config(page_title="Dashboard Airbnb Paris", layout="wide")

st.title("🏠 Dashboard Airbnb - Paris")

# Chargement des données
URL_RAW = "https://minio.lab.sspcloud.fr/${greatisma}/Dashboard-Airbnb-paris/Processed/listings-clean-2025-04-15.csv"
data_path = os.environ.get("data_path", URL_RAW)

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(data_path)

# Affichage rapide
st.subheader("Aperçu des données")
st.dataframe(df.head(20), use_container_width=True)

# Carte interactive simple
st.subheader("Carte interactive des logements Airbnb")
fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    color="price",
    size="price",
    hover_name="name",
    hover_data=["neighbourhood", "room_type", "price"],
    zoom=11,
    height=600
)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)