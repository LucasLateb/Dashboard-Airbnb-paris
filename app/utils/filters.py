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