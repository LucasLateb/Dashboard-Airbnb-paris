import streamlit as st
from app.utils.load import load_data, load_css
from app.utils.filters import apply_filters, render_sidebar_filters
from app.components.charts import (
    show_kpi_block,
    show_quartier_comparison,
    show_price_distribution,
    show_availability_vs_reviews,
    show_room_type_pie,
    show_price_boxplot,
    show_price_summary_bar,
    show_automatic_reco_table
)
from app.components.maps import render_fast_marker_map

# ----------- Setup ----------- #
st.set_page_config(page_title="Vue Hôte / Collectivité", layout="wide")
st.markdown(load_css("app/assets/styles.css"), unsafe_allow_html=True)
df = load_data()

st.sidebar.header("Changer de 🎨 Thème, dans les paramètres (en Haut a droite)")

st.title("🏠 Vue Hôte / Collectivité – Analyse de positionnement")
st.markdown("""
<div style='font-size: 1rem; margin-bottom: 1.5em;'>
Cette interface est conçue pour les <strong>hôtes</strong> ou les <strong>collectivités"
locales</strong> 👩‍💼👨‍💼 souhaitant analyser le marché Airbnb à Paris.<br><br>

Elle est structurée autour de plusieurs éléments clés :
<ul>
  <li>📌 Des <strong>indicateurs clés</strong> pour situer votre positionnement</li>
  <li>🗺️ Une <strong>carte</strong> des annonces concurrentes</li>
  <li>🧠 Un tableau de <strong>recommandations automatiques</strong> pour ajuster vos tarifs</li>
  <li>📊 Des <strong>graphiques analytiques</strong> comparant quartiers, prix, disponibilités</li>
  <li>💡 Une <strong>détection des tarifs à revoir</strong> via une analyse statistique</li>
</ul>

ℹ️ <em>Pensez à survoler les icônes</em> <span style='background:#eee; padding:0.1em 0.3em;
border-radius:3px;'>ℹ️</span> <em>placées à côté des titres pour comprendre chaque graphique ou
tableau</em>.
</div>
""", unsafe_allow_html=True)

# ----------- Filtres ----------- #
selected_neigh, selected_types, selected_price = render_sidebar_filters(df, default_quartiers=3)
filtered_df = apply_filters(df, selected_neigh, selected_types, selected_price)

# ----------- KPIs concurrentiels ----------- #
show_kpi_block(filtered_df, df)

# ----------- Carte des concurrents ----------- #
st.subheader("🗺️ Localisation des concurrents selon vos filtres")
render_fast_marker_map(filtered_df)

# ----------- Recommandations automatiques ----------- #
show_automatic_reco_table(filtered_df)

# ----------- Graphiques analytiques (2 par 2) ----------- #
col1, col2 = st.columns(2)
with col1:
    show_room_type_pie(filtered_df)
with col2:
    show_price_distribution(filtered_df)

col3, col4 = st.columns(2)
with col3:
    show_availability_vs_reviews(filtered_df)
with col4:
    show_price_summary_bar(filtered_df)

col5, col6 = st.columns(2)
with col5:
    show_quartier_comparison(filtered_df)
with col6:
    show_price_boxplot(filtered_df)
