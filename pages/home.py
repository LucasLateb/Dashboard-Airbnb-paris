import streamlit as st

st.set_page_config(page_title="Accueil - Dashboard Airbnb", layout="wide")
st.title("Bienvenue sur le Dashboard Airbnb Paris")

st.markdown("""
### Qui êtes-vous ?
Choisissez un profil utilisateur pour accéder à une vue personnalisée :
""")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎒 Je suis un voyageur"):
        st.switch_page("pages/voyageur.py")

with col2:
    if st.button("🏛️ Je suis un hôte / collectivité"):
        st.switch_page("pages/hote.py")