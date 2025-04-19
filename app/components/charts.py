import pandas as pd
import streamlit as st
import plotly.express as px
from app.utils.filters import detect_bons_plans


def show_kpi_block(df_filtered, df_global):
    prix_moyen = df_filtered["price"].mean()
    prix_median_global = df_global["price"].median()
    dispo_moy = df_filtered["availability_365"].mean()
    review_moy = df_filtered["number_of_reviews"].mean()
    nb_annonces = len(df_filtered)

    bons_plans = detect_bons_plans(df_filtered)
    taux_bons_plans = (len(bons_plans) / nb_annonces) * 100 if nb_annonces > 0 else 0

    st.markdown("### 📌 Indicateurs clés du marché sélectionné")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💶 Prix moyen (€)", f"{prix_moyen:.2f}",
                f"{prix_moyen - prix_median_global:+.2f} vs médiane Paris")
    col2.metric("📅 Dispo moyenne (j/an)", f"{dispo_moy:.0f}")
    col3.metric("⭐ Avis moyens", f"{review_moy:.1f}")
    col4.metric("💎 % Bons plans", f"{taux_bons_plans:.1f}%")


def show_quartier_comparison(df):
    st.subheader("🏙️ Comparaison entre quartiers sélectionnés")
    stats = (
        df.groupby("neighbourhood_cleansed")
        .agg(prix=("price", "mean"), reviews=("number_of_reviews", "mean"),
             dispo=("availability_365", "mean"), annonces=("id", "count"))
        .reset_index()
    )
    fig = px.scatter(
        stats.sort_values("prix", ascending=False),
        x="prix", y="neighbourhood_cleansed",
        size="annonces", color="dispo",
        hover_data=["reviews", "dispo"],
        title="Prix moyen par quartier (taille = nb annonces, couleur = dispo)"
    )
    st.plotly_chart(fig, use_container_width=True)


def show_price_distribution(df):
    st.subheader("📊 Distribution des prix")
    fig = px.histogram(df, x="price", nbins=40, title="Distribution des prix filtrés (€)")
    fig.add_vline(x=df["price"].median(), line_dash="dash", line_color="red",
                  annotation_text="Prix médian", annotation_position="top right")
    st.plotly_chart(fig, use_container_width=True)


def show_availability_vs_reviews(df):
    st.subheader("📈 Reviews vs Disponibilité")
    scatter_df = df[df["reviews_per_month"].notna()].copy()
    scatter_df["reviews_per_month"] = pd.to_numeric(scatter_df["reviews_per_month"], errors="coerce")
    fig = px.scatter(
        scatter_df,
        x="availability_365", y="number_of_reviews",
        size="reviews_per_month", color="room_type",
        hover_name="name", opacity=0.6,
        title="Disponibilité vs nombre de reviews"
    )
    st.plotly_chart(fig, use_container_width=True)


def show_room_type_pie(df):
    st.subheader("🏘️ Répartition des types de logement")
    counts = df["room_type"].value_counts().reset_index()
    counts.columns = ["room_type", "count"]
    fig = px.pie(counts, names="room_type", values="count", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)