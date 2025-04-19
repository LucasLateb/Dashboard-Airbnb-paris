import streamlit as st
from app.utils.load import load_data, load_css
from app.utils.filters import apply_filters
from app.components.charts import show_quartier_comparison, show_price_distribution, show_availability_vs_reviews
from app.components.maps import render_fast_marker_map
import pandas as pd

# ----------- Setup ----------- #
st.set_page_config(page_title="Vue Hôte / Collectivité", layout="wide")
st.markdown(load_css("app/assets/styles.css"), unsafe_allow_html=True)
df = load_data()

st.title("🏠 Vue Hôte / Collectivité – Analyse de positionnement")

# ----------- Filtres ----------- #
st.sidebar.header("🔍 Filtres")
neigh = sorted(df["neighbourhood_cleansed"].dropna().unique())
selected_neigh = st.sidebar.multiselect("Quartiers", neigh, default=neigh[:5])

types = sorted(df["room_type"].dropna().unique())
selected_types = st.sidebar.multiselect("Type de logement", types, default=types)

price_min, price_max = int(df["price"].min()), int(df["price"].max())
selected_price = st.sidebar.slider("Prix (€)", price_min, min(price_max, 1000), (50, 200))

filtered_df = apply_filters(df, selected_neigh, selected_types, selected_price)

# ----------- KPIs concurrentiels ----------- #
col1, col2 = st.columns(2)
col1.metric("Prix moyen (€)", f"{filtered_df['price'].mean():.2f}")
col2.metric("Avis moyen", f"{filtered_df['number_of_reviews'].mean():.1f}")
# TODO LATER: KPI superhost (variable non conservée)

# ----------- Carte des concurrents ----------- #
st.subheader("🗺️ Localisation des concurrents")
render_fast_marker_map(filtered_df)

# ----------- Recommandations dynamiques ----------- #
st.subheader("🧠 Recommandations automatiques")
prix_75 = df["price"].quantile(0.75)
nb_reviews_med = df["number_of_reviews"].median()
dispo_med = df["availability_365"].median()

a_revoir = filtered_df[
    (filtered_df["price"] > prix_75) &
    ((filtered_df["number_of_reviews"] < nb_reviews_med) |
     (filtered_df["availability_365"] < dispo_med))
]

st.warning(f"{len(a_revoir)} annonces semblent positionnées trop haut en prix")
st.dataframe(a_revoir[["name", "price", "availability_365", "number_of_reviews"]].head(10), use_container_width=True)

# ----------- Comparaison inter-quartiers ----------- #
show_quartier_comparison(filtered_df)

# ----------- Graphiques supplémentaires ----------- #
show_price_distribution(filtered_df)
show_availability_vs_reviews(filtered_df)

# TODO LATER : séries temporelles (calendar.csv), carte tension locative (INSEE)