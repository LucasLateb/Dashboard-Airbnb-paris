import streamlit as st


def apply_filters(df, quartiers, types, prix_range):
    return df[
        (df["neighbourhood_cleansed"].isin(quartiers)) &
        (df["room_type"].isin(types)) &
        (df["price"].between(*prix_range))
    ]


def render_sidebar_filters(df, default_quartiers=5):
    st.sidebar.header("🔍 Filtres")

    neigh = sorted(df["neighbourhood_cleansed"].dropna().unique())
    selected_neigh = st.sidebar.multiselect("Quartiers", neigh, default=neigh[:default_quartiers])

    types = sorted(df["room_type"].dropna().unique())
    selected_types = st.sidebar.multiselect("Type de logement", types, default=types)

    price_min, price_max = int(df["price"].min()), int(df["price"].max())
    selected_price = st.sidebar.slider("Prix (€)", price_min, min(price_max, 1000), (50, 200))

    return selected_neigh, selected_types, selected_price


def detect_bons_plans(df):
    prix_med = df["price"].median()
    reviews_med = df["number_of_reviews"].median()
    dispo_med = df["availability_365"].median()
    recent_booking = df["total_booked_6m"].median() if "total_booked_6m" in df else 0

    return df[
        (df["price"] <= prix_med) &
        (df["number_of_reviews"] >= reviews_med) &
        (df["availability_365"] >= dispo_med) &
        (df.get("total_booked_6m", 0) >= recent_booking)
    ]


def compare_to_global_median(df_local, df_global):
    prix_moyen_local = df_local["price"].mean()
    prix_median_global = df_global["price"].median()
    return prix_moyen_local - prix_median_global
