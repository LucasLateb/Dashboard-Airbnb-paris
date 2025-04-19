import streamlit as st
from app.utils.load import load_data, load_css
from app.utils.filters import apply_filters, detect_bons_plans
from app.components.charts import show_price_distribution
from app.components.maps import render_fast_marker_map
import plotly.express as px

# ----------- Setup ----------- #
st.set_page_config(page_title="Vue Voyageur", layout="wide")
st.markdown(load_css("app/assets/styles.css"), unsafe_allow_html=True)
df = load_data()

st.title("🎒 Vue Voyageur – Rechercher un logement à Paris")

# ----------- Filtres ----------- #
st.sidebar.header("🔍 Filtres")
neigh = sorted(df["neighbourhood_cleansed"].dropna().unique())
selected_neigh = st.sidebar.multiselect("Quartiers", neigh, default=neigh[:3])

types = sorted(df["room_type"].dropna().unique())
selected_types = st.sidebar.multiselect("Type de logement", types, default=types)

price_min, price_max = int(df["price"].min()), int(df["price"].max())
selected_price = st.sidebar.slider("Prix (€)", price_min, min(price_max, 1000), (50, 200))

# TODO LATER: ajouter nombre de nuits, disponibilité sur période (requiert calendar.csv)

# ----------- Application des filtres ----------- #
filtered_df = apply_filters(df, selected_neigh, selected_types, selected_price)

# ----------- Bandeau KPIs ----------- #
col1, col2, col3, col4 = st.columns(4)
col1.metric("Prix médian (€)", f"{filtered_df['price'].median():.2f}")
col2.metric("Avis moyen", f"{filtered_df['number_of_reviews'].mean():.1f}")
col3.metric("Dispo. moyenne (j/an)", f"{filtered_df['availability_365'].mean():.0f}")
col4.metric("Nb logements", len(filtered_df))

# ----------- Carte interactive ----------- #
st.subheader("📍 Logements disponibles")
render_fast_marker_map(filtered_df)

# ----------- Bons plans ----------- #
st.subheader("💎 Bons plans (automatiques)")
bons_plans = detect_bons_plans(filtered_df)
st.success(f"{len(bons_plans)} logements sélectionnés comme bons plans")
st.dataframe(bons_plans[["name", "neighbourhood_cleansed", "price", "availability_365", "number_of_reviews"]].head(10), use_container_width=True)

st.markdown("🗺️ Localisation des bons plans")
render_fast_marker_map(bons_plans)

# ----------- Boxplot des prix par quartier ----------- #
st.subheader("📦 Prix par quartier")
fig_box = px.box(
    filtered_df,
    x="neighbourhood_cleansed",
    y="price",
    points="outliers",
    title="Distribution des prix par quartier"
)
st.plotly_chart(fig_box, use_container_width=True)

# ----------- Favoris (session_state) ----------- #
st.subheader("🧺 Vos favoris (WIP)")
if "shortlist" not in st.session_state:
    st.session_state["shortlist"] = []

st.markdown("*Fonction ‘Ajouter aux favoris’ à venir – les favoris seront exportables.*")

# TODO LATER: ajouter heatmap calendrier + boutons ‘favoris’