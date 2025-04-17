import os
import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import FastMarkerCluster

# ----------- Configuration de l'app ----------- #
st.set_page_config(page_title="Dashboard Airbnb Paris", layout="wide")

# ----------- Chargement CSS ----------- #
@st.cache_data(show_spinner=False)
def load_css(file_path):
    with open(file_path) as f:
        return f"<style>{f.read()}</style>"

st.markdown(load_css("app/assets/styles.css"), unsafe_allow_html=True)

# ----------- Chargement des données ----------- #
@st.cache_data(show_spinner=False)
def load_data(path):
    return pd.read_csv(path)

URL_RAW = "https://minio.lab.sspcloud.fr/greatisma/Dashboard-Airbnb-paris/data/processed/listings-clean-2025-04-15.csv"
data_path = os.environ.get("data_path", URL_RAW)
df = load_data(data_path)

# ----------- Base map Folium (mise en cache) ----------- #
@st.cache_resource
def get_base_map(center):
    return folium.Map(
        location=center,
        zoom_start=12,
        tiles="CartoDB positron",
        control_scale=True
    )

# ----------- Filtres ----------- #
st.sidebar.header("🔍 Filtres")

neighbourhoods = sorted(df["neighbourhood_cleansed"].dropna().unique())
default_quartiers = neighbourhoods[:2]
selected_neighbourhoods = st.sidebar.multiselect("Quartiers", neighbourhoods, default=default_quartiers)

room_types = sorted(df["room_type"].dropna().unique())
selected_room_types = st.sidebar.multiselect("Type de logement", room_types, default=room_types)

min_price, max_price = int(df["price"].min()), int(df["price"].max())
price_range = st.sidebar.slider("Prix (€)", min_price, min(max_price, 1000), (50, 200))

# ----------- Application des filtres ----------- #
filtered_df = df[
    (df["neighbourhood_cleansed"].isin(selected_neighbourhoods)) &
    (df["room_type"].isin(selected_room_types)) &
    (df["price"].between(*price_range))
]

# ----------- Bloc principal ----------- #
with st.spinner("🔄 Mise à jour des résultats..."):
    st.title("🏠 Dashboard Airbnb - Paris")
    st.subheader(f"Résultats filtrés : {len(filtered_df)} logements")
    st.dataframe(filtered_df.head(20), use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Prix moyen (€)", f"{filtered_df['price'].mean():.2f}")
    c2.metric("Disponibilité moyenne (j/an)", f"{filtered_df['availability_365'].mean():.0f}")
    c3.metric("Nombre moyen de reviews", f"{filtered_df['number_of_reviews'].mean():.1f}")

    # ----------- Comparaison quartiers ----------- #
    st.subheader("🏙️ Comparaison entre quartiers")
    stats = (
        filtered_df.groupby("neighbourhood_cleansed")
        .agg(prix=("price", "mean"), reviews=("number_of_reviews", "mean"), dispo=("availability_365", "mean"), annonces=("id", "count"))
        .reset_index()
    )
    fig = px.bar(stats.sort_values("prix", ascending=False), x="neighbourhood_cleansed", y="prix", color="annonces",
                 hover_data=["reviews", "dispo"], title="Prix moyen par quartier")
    st.plotly_chart(fig, use_container_width=True)

    # ----------- Bons plans ----------- #
    st.subheader("💎 Bons plans Airbnb à Paris")
    prix_med = filtered_df["price"].median()
    reviews_med = filtered_df["number_of_reviews"].median()
    dispo_med = filtered_df["availability_365"].median()

    bons_plans = filtered_df[
        (filtered_df["price"] <= prix_med) &
        (filtered_df["number_of_reviews"] >= reviews_med) &
        (filtered_df["availability_365"] >= dispo_med)
    ]

    st.markdown(f"**{len(bons_plans)} logements repérés** comme bons plans :")
    st.markdown(f"- Prix ≤ {prix_med:.2f} €  ")
    st.markdown(f"- Reviews ≥ {reviews_med:.0f}  ")
    st.markdown(f"- Disponibilité ≥ {dispo_med:.0f} jours/an")
    st.dataframe(bons_plans[["name", "neighbourhood_cleansed", "price", "number_of_reviews", "availability_365"]].head(10), use_container_width=True)

    # ----------- Carte des bons plans ----------- #
    st.subheader("🌟 Carte des bons plans")
    map_bons = bons_plans[["latitude", "longitude", "price", "name", "neighbourhood_cleansed"]].copy()
    center_bons = [map_bons["latitude"].mean(), map_bons["longitude"].mean()]
    base_map_bons = get_base_map(center_bons)

    data_bons = map_bons.values.tolist()
    callback_bons = """
    function(row){
        var m = L.marker(new L.LatLng(row[0], row[1]));
        m.bindTooltip(
            `<b>${row[3]}</b><br/>` +
            `${row[4]}<br/>` +
            `<b>${row[2].toFixed(0)} €</b>`,
            {sticky: true}
        );
        return m;
    }
    """
    FastMarkerCluster(data=data_bons, callback=callback_bons).add_to(base_map_bons)
    map_data_bons = st_folium(base_map_bons, width=1000, height=500)

    if map_data_bons and map_data_bons.get("bounds"):
        sw, ne = map_data_bons["bounds"]["_southWest"], map_data_bons["bounds"]["_northEast"]
        visibles = bons_plans[
            bons_plans["latitude"].between(sw["lat"], ne["lat"]) &
            bons_plans["longitude"].between(sw["lng"], ne["lng"])
        ]
        st.markdown(f"**🏠 {len(visibles)} bons plans visibles dans cette zone**")

    # ----------- Carte interactive globale ----------- #
    st.subheader("📺 Carte interactive des logements")
    map_df = filtered_df[["latitude", "longitude", "price", "name", "neighbourhood_cleansed"]].copy()
    center = [map_df["latitude"].mean(), map_df["longitude"].mean()]
    base_map = get_base_map(center)

    data = map_df.values.tolist()
    callback = """
    function(row){
        var m = L.marker(new L.LatLng(row[0], row[1]));
        m.bindTooltip(
            `<b>${row[3]}</b><br/>` +
            `${row[4]}<br/>` +
            `<b>${row[2].toFixed(0)} €</b>`,
            {sticky: true}
        );
        return m;
    }
    """
    FastMarkerCluster(data=data, callback=callback).add_to(base_map)
    map_data = st_folium(base_map, width=1000, height=600)

    bounds = map_data.get("bounds") if map_data else None
    if bounds and bounds != st.session_state.get("prev_bounds"):
        st.session_state["prev_bounds"] = bounds
        sw, ne = bounds["_southWest"], bounds["_northEast"]
        visible = filtered_df[
            filtered_df["latitude"].between(sw["lat"], ne["lat"]) &
            filtered_df["longitude"].between(sw["lng"], ne["lng"])
        ]
        st.markdown(f"**🏠 {len(visible)} logements visibles dans la zone actuelle**")

    # ----------- Graphiques supplémentaires ----------- #
    st.subheader("📊 Distribution des prix")
    fig_price = px.histogram(filtered_df, x="price", nbins=40, title="Distribution des prix filtrés (€)")
    st.plotly_chart(fig_price, use_container_width=True)

    st.subheader("📈 Reviews vs Disponibilité")
    scatter_df = filtered_df[filtered_df["reviews_per_month"].notna()]
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