import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import branca.colormap as cm
import requests
import zipfile
import io
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.inspection import PartialDependenceDisplay
import shap
import joblib

# Ajouter un style CSS pour personnaliser les couleurs
def add_custom_styles():
    st.markdown(
        """
        <style>
        /* Couleur pour la barre latérale */
        section[data-testid="stSidebar"] {
            background-color: #A8E6A3; /* Vert clair */
            color: black; /* Texte noir */
        }
        /* Alignement des éléments */
        .sidebar-content {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        /* Couleur des titres principaux */
        h1, h2, h3 {
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# Appliquer le style personnalisé
add_custom_styles()


 
# URLs des logos hébergés sur GitHub
logo_isup_url = "https://raw.githubusercontent.com/jeremyxu-pro/BDX_Project/main/DataViz/Logo-ISUP.jpg"
logo_gov_url = "https://raw.githubusercontent.com/jeremyxu-pro/BDX_Project/main/DataViz/gov.png"
 
 
try:
    # Charger le logo gov.br en haut, centré
    st.sidebar.markdown("<div style='text-align: center;'><img src='{}' width='100'></div>".format(logo_gov_url), unsafe_allow_html=True)

    # Ajouter le texte sous le logo gov.br
    st.sidebar.markdown("<h2 style='text-align: center; color: #004C29;'>Projet de Data Visualisation</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<h3 style='text-align: center; color: #004C29;'>Groupe BDX</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; color: #004C29;'>BAENA Miguel</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; color: #004C29;'>DAKPOGAN Paul</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; color: #004C29;'>XU Jérémy</p>", unsafe_allow_html=True)

    # Ajouter le logo ISUP après les noms, centré
    st.sidebar.markdown("<div style='text-align: center;'><img src='{}' width='100'></div>".format(logo_isup_url), unsafe_allow_html=True)

except Exception as e:
    st.sidebar.error(f"Une erreur est survenue avec les logos : {e}")



# Charger les données
# Lien brut (raw)
zip_url = "https://raw.githubusercontent.com/jeremyxu-pro/BDX_Project/main/DataViz/datavis_long_lat_with_grupo.zip"
# Télécharger et décompresser
response = requests.get(zip_url)
zip_file = zipfile.ZipFile(io.BytesIO(response.content))
 
# Lire un fichier CSV spécifique à l'intérieur du ZIP
with zip_file.open('datavis_long_lat_with_grupo.csv') as file:
    data = pd.read_csv(file)
 
try:
    

    # Vérifiez si les colonnes nécessaires existent
    required_columns = ['Region_Name', 'ANO_MODELO_Class', 'COBERTURA', 'INDENIZ', 'AGE_Group', 'COD_MODELO', 'SEXO']
    if not all(col in data.columns for col in required_columns):
        st.error("Certaines colonnes nécessaires sont manquantes dans vos données.")
    else:
        # Configuration des onglets
        tabs = st.tabs(["Introduction", "Composition du Portefeuille", "Analyses", "Cartographie", "Outil de Tarification", "Interprétations des Modèles"])

        # **Onglet 1 : Introduction**
        with tabs[0]:
            st.title("Introduction")
            st.markdown("""
            Bienvenue dans ce projet de **Data Visualisation** développé par le groupe **BDX**. 
            Ce tableau de bord interactif est conçu pour analyser et explorer des données d'assurance au Brésil. 
            Voici un aperçu des différents onglets disponibles dans cette application :

            ### **1. Composition du Portefeuille**
            - Analyse des caractéristiques principales des polices d'assurance, notamment :
                - La répartition des clients par tranche d'âge et sexe.
                - La répartition des types de couverture.
                - Le nombre d'éléments dans chaque groupe de véhicules.

            ### **2. Analyses**
            - Exploration visuelle des données à travers :
                - L'indemnité totale par type de véhicule ou par groupe.
                - Les relations entre les causes de sinistres et les indemnités (boxplot).
                - La distribution des indemnités par type de couverture.

            ### **3. Cartographie**
            - Visualisation dynamique des données géographiques :
                - Carte des nombres de sinistres par région.
                - Carte des coûts d'indemnités par région.

            ### **4. Outil de Tarification**
            - Implémentation de deux modèles **XGBoost** pour prédire la fréquence et la sévérité respectivement.
                        
            ### **5. Interprétations Modèles**
            - Cet onglet fournit une analyse des modèles prédictifs en utilisant des outils tels que :
                - Les graphiques **SHAP** (SHapley Additive exPlanations) pour interpréter les contributions des variables au modèle.
        
            Ce tableau de bord est une démonstration de l'application des outils de **data science**, **modélisation** et **visualisation** dans le domaine des assurances. 
            Prenez le temps d'explorer chaque onglet pour une meilleure compréhension des données et des résultats. 🎉
            """)

        # **Onglet 2 : Composition du Portefeuille**
        with tabs[1]:
            st.title("Composition du Portefeuille")
        # **Onglet 3 : Analyse**
        with tabs[2]:
            st.title("Analyse des indemnités")
        # **Onglet 4 : Cartographie**
        with tabs[3]:
            st.header("Visualisation du coût des sinistres par état")
        # **Onglet 6 : Tarification**
        with tabs[4]:
            st.markdown("""
            Cet onglet fournit un outil réalisant une tarification simplifiée selon une logique de fréquence-sévérité avec deux modèles XGBOOST.
            """)
            # **Onglet 5 : Interpretation Modèle**
        with tabs[5]:
            st.title("Interpretations des Modèles")
            st.markdown("""
            Cet onglet affiche les graphiques SHAP (SHapley Additive exPlanations) permettant d'interpréter les contributions des variables dans nos deux modèles. Nous mettons en avant uniquement les 10 variables ayant les contributions les plus significatives. Veuillez noter ensuite l'outil d'analyse de dépendance SHAP où vous pouvez vous même choisir le couple de classe à étudier. Par ailleurs, il est important de noter que l'analyse est réalisée à l'échelle des classes, afin d'éviter toute compensation qui pourrait survenir en passant à une échelle plus agrégée, soit celle des variables individuelles.
            """)
except FileNotFoundError:
    st.error(f"Fichier introuvable : {file_path}. Vérifiez le chemin.")
except Exception as e:
    st.error(f"Une erreur est survenue : {e}")
