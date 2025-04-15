import os
import requests
from datetime import datetime
from pathlib import Path

def download_airbnb_data(url: str, save_path: Path):
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Téléchargement du fichier
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Téléchargement réussi : {save_path}")
    else:
        print(f"Erreur lors du téléchargement : {response.status_code}")

if __name__ == "__main__":
    # URL à actualiser selon les mises à jour Inside Airbnb
    url = "https://data.insideairbnb.com/france/ile-de-france/paris/2024-12-06/data/listings.csv.gz"

    # Sauvegarde avec date du jour pour historique
    today = datetime.today().strftime('%Y-%m-%d')
    save_path = Path(f"./data/raw/listings-{today}.csv.gz")
    
    download_airbnb_data(url, save_path)