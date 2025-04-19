def apply_filters(df, quartiers, types, prix_range):
    return df[
        (df["neighbourhood_cleansed"].isin(quartiers)) &
        (df["room_type"].isin(types)) &
        (df["price"].between(*prix_range))
    ]


def detect_bons_plans(df):
    prix_med = df["price"].median()
    reviews_med = df["number_of_reviews"].median()
    dispo_med = df["availability_365"].median()

    return df[
        (df["price"] <= prix_med) &
        (df["number_of_reviews"] >= reviews_med) &
        (df["availability_365"] >= dispo_med)
    ]


def compare_to_global_median(df_local, df_global):
    prix_moyen_local = df_local["price"].mean()
    prix_median_global = df_global["price"].median()
    return prix_moyen_local - prix_median_global


def detect_annonces_a_revoir(df, prix_seuil=None, reviews_seuil=None, dispo_seuil=None):
    if prix_seuil is None:
        prix_seuil = df["price"].quantile(0.75)
    if reviews_seuil is None:
        reviews_seuil = df["number_of_reviews"].median()
    if dispo_seuil is None:
        dispo_seuil = df["availability_365"].median()

    return df[
        (df["price"] > prix_seuil) &
        (
            (df["number_of_reviews"] < reviews_seuil) |
            (df["availability_365"] < dispo_seuil)
        )
    ]