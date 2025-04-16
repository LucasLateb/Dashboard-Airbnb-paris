import os
import pandas as pd
import streamlit as st
import plotly.express as px

# Configuration de l'app
st.set_page_config(page_title="Dashboard Airbnb Paris", layout="wide")

st.title("🏠 Dashboard Airbnb - Paris")

# Chargement des données
URL_RAW = "https://minio.lab.sspcloud.fr/greatisma/Dashboard-Airbnb-paris/data/processed/listings-clean-2025-04-15.csv"
data_path = os.environ.get("data_path", URL_RAW)
df = pd.read_csv(data_path)

st.sidebar.header("🔍 Filtres")

# Filtres interactifs
neighbourhoods = sorted(df["neighbourhood_cleansed"].dropna().unique())
selected_neighbourhoods = st.sidebar.multiselect("Quartiers", neighbourhoods, default=neighbourhoods)

room_types = sorted(df["room_type"].dropna().unique())
selected_room_types = st.sidebar.multiselect("Type de logement", room_types, default=room_types)

min_price, max_price = int(df["price"].min()), int(df["price"].max())
price_range = st.sidebar.slider("Prix (€)", min_price, min(max_price, 1000), (50, 200))

# Application des filtres
filtered_df = df[
    (df["neighbourhood_cleansed"].isin(selected_neighbourhoods)) &
    (df["room_type"].isin(selected_room_types)) &
    (df["price"].between(*price_range))
]

# KPI
st.subheader(f"Résultats filtrés : {len(filtered_df)} logements")
st.dataframe(filtered_df.head(20), use_container_width=True)

st.subheader("📌 Indicateurs clés (données filtrées)")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Prix moyen (€)", f"{filtered_df['price'].mean():.2f}")

with col2:
    dispo_moy = filtered_df['availability_365'].mean()
    st.metric("Disponibilité moyenne (jours/an)", f"{dispo_moy:.0f}")

with col3:
    review_moy = filtered_df['number_of_reviews'].mean()
    st.metric("Nombre moyen de reviews", f"{review_moy:.1f}")

st.subheader("🏙️ Comparaison entre quartiers sélectionnés")

quartier_stats = filtered_df.groupby("neighbourhood_cleansed").agg(
    prix_moyen=("price", "mean"),
    reviews_moy=("number_of_reviews", "mean"),
    dispo_moy=("availability_365", "mean"),
    nb_annonces=("id", "count")
).reset_index()

fig_comp = px.bar(
    quartier_stats.sort_values("prix_moyen", ascending=False),
    x="neighbourhood_cleansed",
    y="prix_moyen",
    color="nb_annonces",
    hover_data=["reviews_moy", "dispo_moy"],
    title="Prix moyen par quartier (taille = nombre d'annonces)"
)
st.plotly_chart(fig_comp, use_container_width=True)

# ➕ Graphique : distribution des prix
st.subheader("📊 Distribution des prix")
fig_price = px.histogram(
    filtered_df, 
    x="price", 
    nbins=40,
    title="Distribution des prix filtrés (€)",
    labels={"price": "Prix (€)"}
)
st.plotly_chart(fig_price, use_container_width=True)

# ➕ Graphique : reviews vs disponibilité
st.subheader("📈 Nombre de reviews vs disponibilité")
scatter_df = filtered_df[
    filtered_df["reviews_per_month"].notna() &
    filtered_df["reviews_per_month"].apply(lambda x: isinstance(x, (int, float)))
]
scatter_df["reviews_per_month"] = pd.to_numeric(scatter_df["reviews_per_month"], errors="coerce")
fig_avail = px.scatter(
    scatter_df,
    x="availability_365",
    y="number_of_reviews",
    size="reviews_per_month",
    color="room_type",
    hover_name="name",
    opacity=0.6,
    title="Disponibilité vs nombre de reviews"
)
st.plotly_chart(fig_avail, use_container_width=True)

# ➕ Carte interactive (mise à jour)
st.subheader("🗺️ Carte interactive des logements filtrés")
fig_map = px.scatter_mapbox(
    filtered_df,
    lat="latitude",
    lon="longitude",
    color="price",
    size="price",
    hover_name="name",
    zoom=11,
    height=600
)
fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)