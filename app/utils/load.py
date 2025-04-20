import os
import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def load_data():
    URL_RAW = "https://minio.lab.sspcloud.fr/greatisma/Dashboard-Airbnb-paris/data/processed/listings-enriched-2025-04-20.csv"
    data_path = os.environ.get("data_path", URL_RAW)
    return pd.read_csv(data_path)

@st.cache_data(show_spinner=False)
def load_css(file_path):
    with open(file_path) as f:
        return f"<style>{f.read()}</style>"