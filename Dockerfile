# 📦 Étape 1 : base image officielle légère
FROM python:3.11-slim

# 🧱 Étape 2 : création du dossier de travail
WORKDIR /app

# 🗃 Étape 3 : copie des fichiers nécessaires
COPY . .

# 📚 Étape 4 : installation des dépendances
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# 🌍 Étape 5 : exposition du port
EXPOSE 8501

# 🚀 Étape 6 : commande de lancement
CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]