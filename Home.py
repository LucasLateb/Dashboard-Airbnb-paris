import streamlit as st
from app.utils.load import load_css

# ----------- CONFIG ----------- #
st.set_page_config(page_title="Accueil - Dashboard Airbnb Paris", layout="wide")
st.markdown(load_css("app/assets/styles.css"), unsafe_allow_html=True)

st.sidebar.header("Changer de 🎨 Thème -> en Haut à droite")

# ----------- LOGO DANS SIDEBAR ----------- #   
with st.sidebar:
    st.image("app/assets/logo_airbnb.png", width=250)  # Assure-toi que ce logo existe
    st.markdown("---")

# ----------- TITRE ----------- #
st.title("🏠 Dashboard Airbnb Paris")
st.markdown("#### *Un outil interactif pour comprendre, comparer et choisir intelligemment sur le marché Airbnb à Paris.*")

# ----------- PRÉSENTATION GLOBALE ----------- #
with st.container():
    st.markdown("### ✨ Pourquoi ce dashboard ?")
    st.markdown("""
Ce tableau de bord vous donne accès à une **analyse interactive et visuelle** de l'offre de logements sur Airbnb à Paris.  
Que vous soyez un **voyageur** à la recherche du meilleur logement, ou un **propriétaire / hôte** souhaitant optimiser vos performances, ce dashboard vous offre :

- 📍 **Une carte dynamique** des logements avec clustering
- 📊 **Des indicateurs clés** (prix, avis, disponibilité)
- 💎 **Des suggestions intelligentes** : bons plans pour voyageurs, recommandations stratégiques pour hôtes
- 📈 **Des visualisations claires** pour prendre des décisions rapidement
    """)

# ----------- MODE D’EMPLOI ----------- #
with st.container():
    st.markdown("### 🧭 Comment ça fonctionne ?")
    st.markdown("""
1. **Choisissez votre profil** pour accéder à une interface personnalisée
2. **Filtrez** selon vos critères (quartier, prix, type, etc.)
3. **Explorez les résultats** avec des cartes interactives et graphiques
4. **Ajoutez des logements en favoris** (voyageur) ou **comparez-vous à la concurrence** (hôte)
5. **Exportez vos choix** ou recommandations si besoin
    """)

# ----------- SÉLECTEUR DE PROFIL ----------- #
st.markdown("### 👤 Et vous, qui êtes-vous ?")
st.markdown("_Choisissez votre profil pour accéder à la vue qui vous correspond._")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎒 Je suis un voyageur")
    st.markdown("Je cherche à **trouver un logement optimal** selon mon budget, mes préférences et les bons plans du moment.")
    if st.button("🔍 Accéder à la vue Voyageur"):
        st.switch_page("pages/voyageur.py")

with col2:
    st.markdown("#### 🏛️ Je suis un hôte / collectivité")
    st.markdown("Je veux **analyser mon positionnement** sur le marché, **comprendre la concurrence**, et optimiser mes décisions.")
    if st.button("📈 Accéder à la vue Hôte"):
        st.switch_page("pages/hote.py")

# ----------- FOOTER (optionnel) ----------- #
st.markdown("---")
st.caption("💡 Données issues de InsideAirbnb. Développé dans le cadre d'un projet pédagogique.")