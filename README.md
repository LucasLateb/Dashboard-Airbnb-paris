# 🏠 Dashboard Airbnb Paris

Bienvenue dans **Dashboard Airbnb Paris**, un projet Streamlit de data visualisation interactive permettant d'explorer, comparer et analyser les logements Airbnb à Paris.

Ce dashboard propose deux expériences sur mesure :
- 🎒 **Voyageur / Locataire** : trouver rapidement les meilleurs logements
- 🏛 **Hôte / Collectivité** : analyser l’offre et optimiser son positionnement

---

## 🚀 Objectifs & Usages

Ce dashboard transforme un fichier de données brut en outil d'aide à la décision. Il permet :

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
├── Home.py                      # Point d'entrée du projet (accueil Streamlit)
├── app/
│   ├── assets/                 # Fichiers CSS et logo
│   ├── components/            # Cartes et graphiques personnalisés
│   │   ├── charts.py
│   │   └── maps.py
│   └── utils/                 # Chargement et logique métier
│       ├── load.py
│       └── filters.py
├── pages/
│   ├── home.py                # Choix du profil utilisateur
│   ├── voyageur.py            # Vue 1 : voyageur
│   └── hote.py                # Vue 2 : hôte / collectivité
├── requirements.txt
```

---

## ⚙️ Installation rapide

```bash
# 1. Cloner le projet
$ git clone https://github.com/toncompte/Dashboard-Airbnb-paris.git
$ cd Dashboard-Airbnb-paris

# 2. Créer un environnement virtuel
$ python -m venv venv
$ source venv/bin/activate  # ou .\venv\Scripts\activate sous Windows

# 3. Installer les dépendances
$ pip install -r requirements.txt

# 4. Lancer le dashboard
$ streamlit run Home.py
```

---

## 📊 Fonctionnalités par profil

### 🎒 Vue Voyageur
Objectif : aider les utilisateurs à trouver des logements pertinents selon leurs critères et saisonnalité.

Fonctionnalités :
- Filtres : quartier, type, prix max
- KPIs : prix médian, dispo, reviews, nb logements
- Carte interactive avec clustering
- Bons plans détectés automatiquement (prix bas, bons avis, dispo haute)
- Graphiques : boxplots, score qualité/prix, barplot de saisonnalité
- Favoris cliquables et stockés dans `st.session_state["shortlist"]`

### 🏛 Vue Hôte / Collectivité
Objectif : comprendre la position d’un hôte dans le marché et ajuster sa stratégie.

Fonctionnalités :
- Filtres : quartier, type, plage de prix
- KPIs : comparaison locale vs médiane globale
- Carte des concurrents
- Recommandations dynamiques (prix élevés / peu d’avis)
- Graphiques avancés : reviews, dispo, prix, type, dispersion, boxplot
- Système de détection des logements surtarifés (Z-score)

---

## 🌐 Données utilisées

- Fichier enrichi : `listings-enriched-2025-04-20.csv`
- Colonnes clés : `name`, `price`, `room_type`, `availability_365`, `latitude`, `longitude`, `neighbourhood_cleansed`, `number_of_reviews`, etc.
- Source : [Inside Airbnb](http://insideairbnb.com/get-the-data.html)

---

## 📦 Librairies principales

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

## 💼 Apport métier

### Pour les voyageurs :
- Trouver un logement **adapté à ses critères** et son budget
- Découvrir les **meilleures affaires** de manière automatisée
- Favoriser les quartiers au **meilleur rapport qualité/prix**

### Pour les hôtes et collectivités :
- Evaluer la **visibilité et attractivité** des logements
- Repérer les logements **sur ou sous-performants**
- Ajuster son **tarif de manière stratégique**
- Visualiser l’**offre concurrente** et sa dispersion territoriale

---

## 🖼 Aperçus visuels
- Carte interactive avec clustering dynamique 🗺️
- Tableau de bons plans 💎
- Boxplots et scores qualitatifs 📊
- KPIs explicites avec délta vs Paris 🔍

---

## 🧠 Pourquoi ce projet est différent ?

- Architecture modulaire, réutilisable
- Focalisé sur l’**utilisateur final**
- Dashboard **actionnable, esthétique, et fluide**
- Mise en valeur des **bonnes pratiques de Streamlit**

---

## 👨‍💻 Auteur & contexte
Projet réalisé dans le cadre d’une évaluation de fin de cours en **mise en production de projet ML / dataviz**. Pensé pour être réaliste, pertinent, et utile en situation professionnelle ou d’analyse marché.

---

## 🪪 Licence
Données Inside Airbnb — usage non commercial. Code distribué sous licence MIT.