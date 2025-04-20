#!/bin/bash

# Installer Python

apt-get -y update

apt-get install -y python3-pip python3-venv

# Créer un environnement virtuel

python3 -m venv env

source env/bin/activate

# Installer les dépendances du projet

pip install -r requirements.txt