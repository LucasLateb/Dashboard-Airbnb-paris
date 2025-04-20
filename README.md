# 🏠 Dashboard Airbnb Paris

Bienvenue dans **Dashboard Airbnb Paris**, un projet Streamlit de data visualisation interactive permettant d'explorer, comparer et analyser les logements Airbnb à Paris.

Ce dashboard propose deux expériences sur mesure :
- 🎒 **Voyageur / Locataire** : trouver rapidement les meilleurs logements
- 🏛 **Hôte / Collectivité** : analyser l’offre et optimiser son positionnement

🔗 **Lien vers le dashboard déployé** : [https://airbnb-dash.onrender.com](https://airbnb-dash.onrender.com)

---

## 🚀 Objectifs & Usages

Ce dashboard transforme un fichier de données brut en **outil d'aide à la décision**. Il permet :

- ✅ Une exploration **filtrable** de l'offre Airbnb à Paris
- ✅ Une **carte interactive** avec clustering et prix
- ✅ Des **KPI clairs** : prix, reviews, disponibilité
- ✅ Une détection automatique des **bons plans**
- ✅ Une vue concurrentielle éclairée pour les hôtes
- ✅ Une expérience évolutive avec favoris et export

---

## 🧱 Structure du projet

```
Dashboard-Airbnb-paris/
├── Home.py                      # Accueil du dashboard
├── app/
│   ├── assets/
│   │   ├── styles.css           # Design personnalisé
│   │   └── logo_airbnb.png      # Logo du dashboard
│   ├── components/
│   │   ├── charts.py            # Fonctions de graphiques Plotly
│   │   └── maps.py              # Cartes interactives Folium
│   └── utils/
│       ├── load.py              # Chargement des données
│       └── filters.py           # Fonctions de filtrage
├── pages/
│   ├── home.py                  # Choix du profil utilisateur
│   ├── voyageur.py              # Vue 🎒 Voyageur
│   └── hote.py                  # Vue 🏛 Hôte / Collectivité
├── .github/workflows/
│   ├── docker-build.yml         # CI DockerHub
│   └── docker-tagged.yml        # CI/CD via tag
├── Dockerfile                   # Image Docker du projet
├── requirements.txt
├── environment.yml
├── install.sh
├── LICENSE
└── README.md
```

---

## ⚙️ Installation locale

```bash
# 1. Cloner le projet
git clone https://github.com/greatisma/Dashboard-Airbnb-paris.git
cd Dashboard-Airbnb-paris

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate   # ou .\venv\Scripts\activate sur Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer le dashboard
streamlit run Home.py
```

---

## 👥 Fonctionnalités par profil

### 🎒 Vue Voyageur

**Objectif** : trouver des logements pertinents selon ses critères et saisonnalité.

**Fonctionnalités** :
- Filtres : quartier, type, prix, nb nuits, période
- KPIs : prix médian, dispo, reviews, nb logements
- Carte interactive avec clustering
- Bons plans détectés automatiquement
- Graphiques : boxplots, heatmaps, prix par quartier
- Favoris stockés dans `st.session_state["shortlist"]` et exportables

---

### 🏛 Vue Hôte / Collectivité

**Objectif** : comprendre la position d’un hôte dans le marché et ajuster sa stratégie.

**Fonctionnalités** :
- Filtres stratégiques : quartier, type, prix, dispo
- KPIs : comparaison locale vs globale
- Carte des concurrents
- Recommandations dynamiques
- Graphiques avancés : reviews, dispo, dispersion
- Détection des logements surtarifés (Z-score)

---

## 🌍 Données

- Source : [Inside Airbnb](http://insideairbnb.com/get-the-data.html)
- Fichier enrichi : `listings-enriched-2025-04-20.csv`
- Champs utilisés : `name`, `price`, `room_type`, `availability_365`, `latitude`, `longitude`, `neighbourhood_cleansed`, `number_of_reviews`, `listing_url`, etc.

---

## 📦 Librairies utilisées

```txt
streamlit
pandas
numpy
plotly
folium
streamlit-folium
requests
```

---

## 🐳 Déploiement

Le projet est dockerisé et automatiquement publié sur DockerHub.

```bash
docker pull greatisma/airbnb-dash:latest
docker run -p 8501:8501 greatisma/airbnb-dash:latest
```

CI/CD avec GitHub Actions :
- `docker-build.yml` : build automatique sur `push`
- `docker-tagged.yml` : publication sur `DockerHub` lors des tags

---

## 💼 Apport métier

### Pour les voyageurs :
- Trouver un logement **adapté** à ses critères
- Accéder aux **bons plans** filtrés intelligemment
- Explorer l’offre par quartier, par saison, par prix

### Pour les hôtes / collectivités :
- Observer la **concurrence locale**
- Identifier des **ajustements tarifaires**
- Surveiller la **visibilité et saturation** du marché

---

## 📸 Aperçu visuel

- Carte interactive dynamique 🗺️
- Liste des bons plans 💎
- Boxplot des prix 🧺
- KPIs synthétiques 📊

---

## 👨‍🎓 Contexte

Projet développé dans le cadre du cours **Mise en production de projet ML / Data Science**, avec une exigence de **réalisme, modularité, et impact utilisateur**.

---

## 🪪 Licence

- Données : Inside Airbnb — usage non commercial.
- Code source : Licence MIT.