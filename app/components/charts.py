import pandas as pd
import streamlit as st
import plotly.express as px

def show_quartier_comparison(df):
    st.subheader("🏙️ Comparaison entre quartiers")
    stats = (
        df.groupby("neighbourhood_cleansed")
        .agg(prix=("price", "mean"), reviews=("number_of_reviews", "mean"),
             dispo=("availability_365", "mean"), annonces=("id", "count"))
        .reset_index()
    )
    fig = px.bar(
        stats.sort_values("prix", ascending=False),
        x="neighbourhood_cleansed", y="prix", color="annonces",
        hover_data=["reviews", "dispo"],
        title="Prix moyen par quartier"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_price_distribution(df):
    st.subheader("📊 Distribution des prix")
    fig = px.histogram(df, x="price", nbins=40, title="Distribution des prix filtrés (€)")
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