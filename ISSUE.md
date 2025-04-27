# 🏠 Dashboard Airbnb Paris

## Contexte

Le projet **Dashboard Airbnb Paris** est une application Streamlit qui transforme les données publiques d’Inside Airbnb en un véritable outil d’aide à la décision. Deux parcours sont prévus :
	•	**Voyageur / locataire** – trouver les meilleurs logements selon ses critères ;
	•	**Hôte / collectivité** – analyser l’offre locale et affiner son positionnement.
Cartes interactives, filtres avancés et indicateurs synthétiques rendent l’exploration des annonces parisiennes à la fois simple et ludique.

## Reproductibilité

Le dépôt fournit tout le nécessaire pour relancer le projet :
	1.	**Installation locale**: le README décrit pas à pas le clonage, la création d’un environnement virtuel, l’installation des dépendances via requirements.txt, puis l’exécution du dashboard avec streamlit run Home.py. Testé : l’application démarre sans friction.
	2.	**Conteneur Docker** : le Dockerfile et le workflow GitHub Actions compilent et publient automatiquement une image sur Docker Hub ; un simple docker run -p 8501:8501 … recrée l’environnement à l’identique.
	3.	**CI/CD** : la build se déclenche à chaque push, garantissant que le code reste déployable à tout moment.

Ces éléments offrent une reproductibilité quasi-immédiate, tant pour un développeur local que pour un déploiement cloud.

## Bonnes pratiques observées
	•	**Versioning Git** : historique clair, usage des branches et pull requests.
	•	**.gitignore complet** : exclusion du dossier virtuel, des caches et des données volumineuses.
	•	**README riche** : contexte, objectifs, démo en ligne, instructions locales + Docker.
	•	**LICENSE (MIT)** : conditions d’utilisation explicites.
	•	**Gestion des dépendances** : requirements.txt et environment.yml.
	•	**Architecture modulaire** : séparations src/, pages/, components/, facilitant la maintenance.
	•	**Docker + GitHub Actions** : pipeline d’intégration et de déploiement continu prêt à l’emploi.

## Pistes d’amélioration

La seule vraie marge de progression concerne la qualité automatique du code :
	•	**Linter / Formatter** (par ex. ruff ou black) : ils garantissent un style homogène, attrapent les petites erreurs avant qu’elles n’entrent dans le dépôt, et simplifient les revues de code.
	•	**Tests unitaires** (pytest) : même un jeu de tests minimal (ex. chargement des données, calcul de quelques KPI) sécurise les évolutions futures et renforce la confiance lors du déploiement automatique.

Ces ajouts s’intègrent facilement à la CI existante et ne demandent qu’un faible surcoût initial pour un bénéfice durable.

⸻

En résumé, le projet est solide, bien structuré et immédiatement exploitable ; il ne lui manque qu’une petite couche de tests et de linting pour atteindre le sans-faute. **Bravo pour ce travail** !