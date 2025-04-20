import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from app.utils.filters import detect_bons_plans


def render_title_with_info(title: str, info_text: str):
    """Affiche un titre avec une infobulle au survol, sans débordement."""
    st.markdown(f"""
    <style>
    /* Container général du tooltip */
    .tooltip {{
        position: relative;
        display: inline-block;
        margin-left: 8px;
        cursor: help;
    }}
    /* Texte de l'infobulle, caché par défaut */
    .tooltip .tooltiptext {{
        visibility: hidden;
        width: 260px;
        background-color: #f9f9f9;
        color: #333;
        text-align: left;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 10;
        bottom: 125%;  /* place la bulle au-dessus de l'icône */
        left: 50%;
        transform: translateX(-50%);
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
        font-size: 0.85rem;
        line-height: 1.2;
    }}
    /* Au survol, on affiche la bulle */
    .tooltip:hover .tooltiptext {{
        visibility: visible;
    }}
    </style>

    <div style="display:flex; align-items:center;">
        <h3 style="margin:0;">{title}</h3>
        <div class="tooltip">ℹ️
            <span class="tooltiptext">{info_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


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

    col1.metric(
        label="💶 Prix moyen (€)",
        value=f"{prix_moyen:.2f}",
        delta=f"{prix_moyen - prix_median_global:+.2f} vs médiane Paris",
        help="Prix moyen des logements sélectionnés. Comparé ici à la médiane sur tout Paris."
    )
    col2.metric(
        label="📅 Dispo moyenne (j/an)",
        value=f"{dispo_moy:.0f}",
        help="Nombre de jours moyens où les logements sont disponibles à la réservation dans l’année."
    )
    col3.metric(
        label="⭐ Avis moyens",
        value=f"{review_moy:.1f}",
        help="Nombre moyen d’avis laissés par les voyageurs. Utile pour évaluer la crédibilité ou l’attractivité."
    )
    col4.metric(
        label="💎 % Bons plans",
        value=f"{taux_bons_plans:.1f}%",
        help="Part des annonces avec un excellent équilibre entre prix, avis et disponibilité (top recommandations automatiques)."
    )


def show_quartier_comparison(df):
    render_title_with_info(
        "🏙️ Comparaison entre quartiers sélectionnés",
        "Ce graphique permet de comparer les prix moyens entre quartiers. La taille des bulles représente le nombre d’annonces, et la couleur indique la disponibilité moyenne."
    )
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
        title=""
    )
    st.plotly_chart(fig, use_container_width=True)


def show_price_distribution(df):
    render_title_with_info(
        "📊 Distribution des prix",
        "Histogramme des prix des logements filtrés. La ligne rouge verticale représente le prix médian observé sur la sélection."
    )
    fig = px.histogram(df, x="price", nbins=40, title="")
    fig.add_vline(x=df["price"].median(), line_dash="dash", line_color="red",
                  annotation_text="Prix médian", annotation_position="top right")
    st.plotly_chart(fig, use_container_width=True)


def show_availability_vs_reviews(df):
    render_title_with_info(
        "📈 Reviews vs Disponibilité",
        "Chaque point représente un logement. L’axe des x indique la disponibilité sur l’année, l’axe des y montre le nombre total de reviews. La taille reflète les reviews mensuels, et la couleur le type de logement."
    )
    scatter_df = df[df["reviews_per_month"].notna()].copy()
    scatter_df["reviews_per_month"] = pd.to_numeric(scatter_df["reviews_per_month"], errors="coerce")
    fig = px.scatter(
        scatter_df,
        x="availability_365", y="number_of_reviews",
        size="reviews_per_month", color="room_type",
        hover_name="name", opacity=0.6,
        title=""
    )
    st.plotly_chart(fig, use_container_width=True)


def show_price_boxplot(df):
    render_title_with_info(
        "📦 Dispersion des prix par quartier",
        "Boxplot : médiane, étendue, et outliers des prix dans chaque quartier. Cela permet de voir la variabilité des tarifs dans une même zone."
    )
    fig = px.box(
        df, x="neighbourhood_cleansed", y="price", color="room_type",
        points="all"
    )
    st.plotly_chart(fig, use_container_width=True)


def show_tarif_suggestion(df):
    st.subheader("💡 Suggestions d'ajustement tarifaire", help=(
        "Ce tableau repère les **logements dont le tarif est anormalement élevé** dans leur "
        "**quartier et type de logement**. Utile pour détecter des anomalies statistiques via le Z-score."
    ))
    seuil = 2  # z-score
    grouped = df.groupby(["neighbourhood_cleansed", "room_type"])["price"]
    mean_std = grouped.agg(["mean", "std"]).reset_index()
    df_merged = df.merge(mean_std, on=["neighbourhood_cleansed", "room_type"])
    df_merged["zscore"] = (df_merged["price"] - df_merged["mean"]) / df_merged["std"]
    suspects = df_merged[df_merged["zscore"] > seuil]
    st.markdown(f"🔍 **{len(suspects)} logements au prix atypique détectés** (z > {seuil})")
    st.dataframe(
        suspects[["name", "neighbourhood_cleansed", "room_type", "price", "zscore"]]
        .sort_values("zscore", ascending=False),
        use_container_width=True,
        height=400
    )


def show_automatic_reco_table(df):
    st.subheader("🧠 Recommandations automatiques", help=(
        "Ce tableau liste les annonces avec un **prix élevé**, mais des **performances faibles** "
        "(peu de reviews ou faible disponibilité). Elles sont potentiellement à revoir pour gagner "
        "en visibilité ou taux de réservation."
    ))
    prix_75 = df["price"].quantile(0.75)
    nb_reviews_med = df["number_of_reviews"].median()
    dispo_med = df["availability_365"].median()
    a_revoir = df[
        (df["price"] > prix_75) &
        (
            (df["number_of_reviews"] < nb_reviews_med) |
            (df["availability_365"] < dispo_med)
        )
    ]
    st.warning(f"⚠️ {len(a_revoir)} annonces semblent positionnées trop haut en prix")
    # ← Here we include listing_url alongside the other columns
    st.dataframe(
        a_revoir[
            ["name", "neighbourhood_cleansed", "price",
             "availability_365", "number_of_reviews", "listing_url"]
        ].drop_duplicates(),
        use_container_width=True,
        height=400
    )


def show_room_type_pie(df):
    render_title_with_info(
        "🏘️ Répartition des types de logement",
        "Ce diagramme circulaire montre la proportion de chaque type de logement (entier, chambre privée, etc.) dans votre sélection. Utile pour comprendre l’offre dominante."
    )
    counts = df["room_type"].value_counts().reset_index()
    counts.columns = ["room_type", "count"]
    fig = px.pie(counts, names="room_type", values="count", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)


def show_price_summary_bar(df):
    render_title_with_info(
        "📉 Prix moyen par quartier",
        "Visualisation combinée : prix moyen par quartier, écart-type (barres d’erreur) et médiane (valeurs affichées). Permet d’apprécier la stabilité ou dispersion des tarifs."
    )
    summary = (
        df.groupby("neighbourhood_cleansed")["price"]
        .agg(["mean", "median", "std"])
        .reset_index()
        .rename(columns={"mean": "Prix moyen", "median": "Prix médian", "std": "Écart-type"})
    )
    fig = px.bar(
        summary,
        x="neighbourhood_cleansed",
        y="Prix moyen",
        error_y="Écart-type",
        text="Prix médian",
        labels={"neighbourhood_cleansed": "Quartier"},
        title=""
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)


def show_bons_plans_table(df):
    render_title_with_info(
        "💎 Bons plans (automatiques)",
        "Ces logements ont un excellent compromis entre prix bas, bonne disponibilité et bon nombre d’avis. "
        "Sélectionnez ceux que vous souhaitez enregistrer comme favoris."
    )

    # Initialisation de la shortlist si besoin
    if "shortlist" not in st.session_state:
        st.session_state["shortlist"] = []

    if df.empty:
        st.info("Aucun bon plan ne correspond actuellement à vos filtres.")
        return

    # ▶️ On retire les éventuels doublons (ici basé sur le nom, 
    #    ou remplacez 'name' par l'identifiant unique si vous en avez un)
    df_unique = df.drop_duplicates(subset=["name"])

    # 1️⃣ Affichage de la table scrollable sans doublons
    st.dataframe(
        df_unique[["name", "neighbourhood_cleansed", "price", "availability_365", "number_of_reviews"]],
        use_container_width=True,
        height=400
    )

    # 2️⃣ Multi-select pour ajouter aux favoris
    noms = df_unique["name"].tolist()
    selection = st.multiselect("➕ Ajouter aux favoris", options=noms)

    # 3️⃣ Pour chaque sélection non encore dans la shortlist, on ajoute
    for nom in selection:
        if nom not in [item["name"] for item in st.session_state["shortlist"]]:
            row = df_unique[df_unique["name"] == nom].iloc[0]
            st.session_state["shortlist"].append(row.to_dict())

    if selection:
        st.success(f"{len(selection)} logement(s) ajouté(s) aux favoris ✅")


def show_boxplot_quartiers(df):
    render_title_with_info(
        "📦 Prix par quartier",
        "Chaque boîte représente la distribution des prix dans un quartier donné : médiane, étendue et valeurs extrêmes. Permet d’observer les zones les plus stables ou variables."
    )
    fig = px.box(df, x="neighbourhood_cleansed", y="price", points="outliers")
    st.plotly_chart(fig, use_container_width=True)


def show_summary_bar_chart(df):
    render_title_with_info(
        "📉 Prix moyens par quartier",
        "Ce graphique simplifie la lecture des tarifs moyens par quartier, en indiquant aussi leur variabilité (écart-type) et la médiane (valeur affichée)."
    )
    stats = (
        df.groupby("neighbourhood_cleansed")["price"]
        .agg(["mean", "median", "std"])
        .reset_index()
        .rename(columns={"mean": "Prix moyen", "median": "Prix médian", "std": "Écart-type"})
    )
    fig = px.bar(stats, x="neighbourhood_cleansed", y="Prix moyen", error_y="Écart-type", text="Prix médian")
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


def show_top_deals_score(df):
    render_title_with_info(
        "🏅 Meilleurs rapports qualité/prix",
        "Classement des quartiers selon un score qualité/prix (avis / prix). "
        "Idéal pour identifier les zones où les logements bien notés sont abordables."
    )
    df = df[df["price"] > 0].copy()
    df["score_qp"] = df["number_of_reviews"] / df["price"]
    df["score_qp"] = df["score_qp"].replace([np.inf, -np.inf], np.nan).fillna(0)

    top_deals = df.groupby("neighbourhood_cleansed").apply(
        lambda g: g.sort_values("score_qp", ascending=False).head(3)
    ).reset_index(drop=True)

    summary = top_deals.groupby("neighbourhood_cleansed")["score_qp"].mean().reset_index()

    fig = px.bar(
        summary.sort_values("score_qp", ascending=False),
        x="neighbourhood_cleansed",
        y="score_qp",
        title="",
        labels={"neighbourhood_cleansed": "Quartier", "score_qp": "Score qualité/prix moyen"}
    )
    st.plotly_chart(fig, use_container_width=True)


def show_top_deals_score(df):
    render_title_with_info(
        "🏅 Meilleurs rapports qualité/prix",
        "Classement des quartiers selon un score qualité/prix (avis / prix). "
        "Idéal pour identifier les zones où les logements bien notés sont abordables."
    )
    df = df[df["price"] > 0].copy()
    df["score_qp"] = df["number_of_reviews"] / df["price"]
    df["score_qp"] = df["score_qp"].replace([np.inf, -np.inf], np.nan).fillna(0)

    top_deals = df.groupby("neighbourhood_cleansed").apply(
        lambda g: g.sort_values("score_qp", ascending=False).head(3)
    ).reset_index(drop=True)

    summary = top_deals.groupby("neighbourhood_cleansed")["score_qp"].mean().reset_index()

    fig = px.bar(
        summary.sort_values("score_qp", ascending=False),
        x="neighbourhood_cleansed",
        y="score_qp",
        title="",
        labels={"neighbourhood_cleansed": "Quartier", "score_qp": "Score qualité/prix moyen"}
    )
    st.plotly_chart(fig, use_container_width=True)


def show_kpi_block_voyageur(df_filtered):
    prix_median = df_filtered["price"].median()
    avis_moyens = df_filtered["number_of_reviews"].mean()
    dispo_moyenne = df_filtered["availability_365"].mean()
    nb_annonces = len(df_filtered)

    st.markdown("### 📌 Résumé de votre sélection")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="💰 Prix médian (€)",
        value=f"{prix_median:.2f}",
        help="Prix médian des logements disponibles après application de vos filtres. Moins sensible aux extrêmes que la moyenne."
    )
    col2.metric(
        label="⭐ Avis moyens",
        value=f"{avis_moyens:.1f}",
        help="Nombre moyen d’avis laissés par les précédents voyageurs sur les logements affichés."
    )
    col3.metric(
        label="📅 Dispo moyenne (j/an)",
        value=f"{dispo_moyenne:.0f}",
        help="Nombre moyen de jours par an où les logements sont disponibles à la réservation."
    )
    col4.metric(
        label="🏘️ Nb logements",
        value=str(nb_annonces),
        help="Nombre total d’annonces correspondant à vos filtres actuels."
    )


def show_seasonality_bar(df):
    render_title_with_info(
        "📆 Saisonnalité des logements",
        "Cette visualisation montre le **nombre moyen de jours disponibles par mois**, "
        "pour les annonces sélectionnées. Cela permet d’identifier les saisons les plus actives ou creuses."
    )

    if "month" not in df.columns or "nb_jours_dispos" not in df.columns:
        st.info("Les données de saisonnalité ne sont pas disponibles.")
        return

    # Regrouper par mois (format YYYY-MM)
    month_summary = (
        df.groupby("month")["nb_jours_dispos"]
        .mean()
        .reset_index()
        .sort_values("month")
    )

    # Affichage
    fig = px.bar(
        month_summary,
        x="month",
        y="nb_jours_dispos",
        labels={"month": "Mois", "nb_jours_dispos": "Jours disponibles (moyenne)"},
        title=""
    )
    st.plotly_chart(fig, use_container_width=True)