import gzip
import shutil
import pandas as pd
from pathlib import Path
from datetime import datetime

def decompress_csv_gz(input_path: Path, output_path: Path):
    with gzip.open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Fichier décompressé : {output_path}")

def clean_listings(df: pd.DataFrame) -> pd.DataFrame:
    # Colonnes utiles (peut évoluer selon ton besoin de dashboard)
    keep_cols = [
        "id", "name", "host_id", "host_name", "neighbourhood_cleansed", 
        "latitude", "longitude", "room_type", "price", 
        "minimum_nights", "number_of_reviews", "last_review", 
        "reviews_per_month", "calculated_host_listings_count", 
        "availability_365", "listing_url"
    ]
    df = df[keep_cols]

    # Conversion types
    df.loc[:, "price"] = df["price"].replace(r'[\$,]', '', regex=True).astype(float)
    df.loc[:, "last_review"] = pd.to_datetime(df["last_review"], errors='coerce')

    # Nettoyage basique : coordonnées valides & prix raisonnables
    df = df.dropna(subset=["latitude", "longitude", "price"])
    df = df[df["price"] < 1000]  # exclure prix aberrants

    return df

if __name__ == "__main__":
    # Récupérer le fichier le plus récent automatiquement
    raw_dir = Path("data/raw")
    latest_gz = max(raw_dir.glob("listings.csv.gz"), key=lambda p: p.stat().st_mtime)

    # Décompression dans le même dossier temporairement
    decompressed_path = raw_dir / latest_gz.with_suffix("").name
    decompress_csv_gz(latest_gz, decompressed_path)

    # Chargement et nettoyage
    df = pd.read_csv(decompressed_path)
    df_clean = clean_listings(df)

    # Sauvegarde du fichier traité
    today = datetime.today().strftime('%Y-%m-%d')
    processed_path = Path(f"data/processed/listings-clean-{today}.csv")
    df_clean.to_csv(processed_path, index=False)
    print(f"Fichier nettoyé sauvegardé : {processed_path}")