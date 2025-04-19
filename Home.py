import pandas as pd
import streamlit as st
from app.utils.load import load_data, load_css
from app.utils.filters import apply_filters, detect_bons_plans
from app.components.charts import (
    show_quartier_comparison,
    show_price_distribution,
    show_availability_vs_reviews
)
from app.components.maps import render_fast_marker_map

# ----------- Configuration de l'app ----------- #
st.set_page_config(page_title="Dashboard Airbnb Paris", layout="wide")
st.markdown(load_css("app/assets/styles.css"), unsafe_allow_html=True)

# ----------- Chargement des données ----------- #
df = load_data()

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
filtered_df = apply_filters(df, selected_neighbourhoods, selected_room_types, price_range)

# ----------- Affichage des résultats ----------- #
st.title("🏠 Dashboard Airbnb - Paris")
st.subheader(f"Résultats filtrés : {len(filtered_df)} logements")
st.dataframe(filtered_df.head(20), use_container_width=True)

c1, c2, c3 = st.columns(3)
c1.metric("Prix moyen (€)", f"{filtered_df['price'].mean():.2f}")
c2.metric("Disponibilité moyenne (j/an)", f"{filtered_df['availability_365'].mean():.0f}")
c3.metric("Nombre moyen de reviews", f"{filtered_df['number_of_reviews'].mean():.1f}")

# ----------- Comparaison quartiers ----------- #
show_quartier_comparison(filtered_df)

# ----------- Bons plans ----------- #
st.subheader("💎 Bons plans Airbnb à Paris")
bons_plans = detect_bons_plans(filtered_df)
st.markdown(f"**{len(bons_plans)} logements repérés** comme bons plans.")
st.dataframe(bons_plans[[
    "name", "neighbourhood_cleansed", "price", "number_of_reviews", "availability_365"
]].head(10), use_container_width=True)

# ----------- Carte interactive globale ----------- #
st.subheader("📍 Carte interactive des logements")
map_data = render_fast_marker_map(filtered_df)

if map_data and map_data.get("bounds"):
    sw, ne = map_data["bounds"]["_southWest"], map_data["bounds"]["_northEast"]
    visible = filtered_df[
        filtered_df["latitude"].between(sw["lat"], ne["lat"]) &
        filtered_df["longitude"].between(sw["lng"], ne["lng"])
    ]
    st.markdown(f"**🏠 {len(visible)} logements visibles dans la zone actuelle**")

# ----------- Graphiques supplémentaires ----------- #
show_price_distribution(filtered_df)
show_availability_vs_reviews(filtered_df)