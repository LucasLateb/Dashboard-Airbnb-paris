import streamlit as st
import plotly.express as px
import pandas as pd
from app.utils.load import load_data, load_css
from app.utils.filters import render_sidebar_filters, apply_filters, detect_bons_plans
from app.components.maps import render_fast_marker_map
from app.components.charts import (
    show_price_distribution,
    show_boxplot_quartiers,
    show_summary_bar_chart,
    show_top_deals_score,
    show_kpi_block_voyageur,
    show_seasonality_bar,
    show_bons_plans_table
)

# ----------- Setup ----------- #
st.set_page_config(page_title="Vue Voyageur", layout="wide")
st.markdown(load_css("app/assets/styles.css"), unsafe_allow_html=True)
df = load_data()

st.title("🎒 Vue Voyageur – Rechercher un logement à Paris")
st.markdown("""
<div style='font-size: 1rem; margin-bottom: 1.5em;'>
Bienvenue dans la vue <strong>Voyageur</strong> 👋<br><br>

Cette interface vous aide à trouver rapidement des logements adaptés à vos besoins à Paris. Elle est structurée autour de plusieurs blocs :
<ul>
  <li>📊 Des <strong>indicateurs clés</strong> pour résumer le marché actuel</li>
  <li>📍 Une <strong>carte interactive</strong> des logements disponibles</li>
  <li>💎 Une sélection de <strong>bons plans automatiques</strong> selon vos filtres</li>
  <li>📦 Des <strong>graphiques analytiques</strong> pour comparer les prix, la saisonnalité, et plus</li>
  <li>🧺 Une section pour <strong>gérer vos favoris</strong></li>
</ul>

ℹ️ <em>N’hésitez pas à survoler les petites icônes d’information</em> <span style='background:#eee; padding:0.1em 0.3em; border-radius:3px;'>ℹ️</span> à côté des titres pour obtenir des explications détaillées sur chaque graphique ou tableau.
</div>
""", unsafe_allow_html=True)

# ----------- Filtres ----------- #
selected_neigh, selected_types, selected_price = render_sidebar_filters(df, default_quartiers=3)
filtered_df = apply_filters(df, selected_neigh, selected_types, selected_price)

# ----------- Bandeau KPIs ----------- #
show_kpi_block_voyageur(filtered_df)

# ----------- Carte interactive ----------- #
st.subheader("📍 Logements disponibles selon vos filtres")
render_fast_marker_map(filtered_df)

# ----------- Bons plans ----------- #
bons_plans = detect_bons_plans(filtered_df)
show_bons_plans_table(bons_plans)

# Saison

# ----------- Boxplot des prix par quartier ----------- #
col1, col2 = st.columns(2)
with col1:
    show_boxplot_quartiers(filtered_df)
with col2:
    show_summary_bar_chart(filtered_df)

col3, col4 = st.columns(2)
with col3:
    show_seasonality_bar(filtered_df)
with col4:
    show_top_deals_score(filtered_df)

# ✅ Graphe des meilleurs rapports qualité/prix


# ----------- Favoris (session_state) ----------- #
st.subheader("🧺 Vos favoris")

if st.session_state["shortlist"]:
    favs_df = pd.DataFrame(st.session_state["shortlist"])
    st.dataframe(
        favs_df[["name", "neighbourhood_cleansed", "price", "availability_365", "number_of_reviews"]],
        use_container_width=True
    )
else:
    st.info("Aucun favori sélectionné pour le moment.")

# TODO LATER: ajouter heatmap calendrier + boutons ‘favoris’