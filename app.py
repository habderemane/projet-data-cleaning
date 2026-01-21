import streamlit as st
import pandas as pd
import time
from utils import load_data, handle_missing_values, remove_duplicates, handle_outliers_iqr, normalize_data, convert_df_to_csv

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="DataClean Pro | ISI",
    page_icon="🧹",
    layout="wide"
)

# --- CSS PERSONNALISÉ (Pour le point 2 : HTML/CSS) ---
st.markdown("""
<style>
    /* En-tête principal */
    .main-header {
        font-size: 2.5rem;
        color: #ffffff;
        text-align: center;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #cccccc;
        text-align: center;
        margin-bottom: 2rem;
    }
    /* CORRECTION ICI : Fond sombre pour les métriques */
    div[data-testid="stMetric"] {
        background-color: #262730; /* Gris foncé au lieu de blanc */
        border: 1px solid #464b5c;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    /* Texte des métriques en blanc */
    div[data-testid="stMetric"] label {
        color: #ffffff;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #ffffff;
    }
    
    /* Bouton principal */
    div.stButton > button:first-child {
        background-color: #007bff;
        color: white;
        font-size: 18px;
        border-radius: 8px;
        padding: 10px 20px;
        width: 100%;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

# --- EN-TÊTE ---
st.markdown('<div class="main-header">🧹 Data Processing API</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Projet Python M1 IAGE - Institut Supérieur d’Informatique (ISI)</div>', unsafe_allow_html=True)

# --- SIDEBAR (PARAMÈTRES) ---
with st.sidebar:
    st.title("Paramètres")
    st.markdown("---")

    # 1. Import
    st.subheader("1. Fichier Source")
    uploaded_file = st.file_uploader("Formats : CSV, Excel, JSON, XML", type=['csv', 'xlsx', 'xls', 'json', 'xml'])

    # 2. Options de nettoyage
    miss_val = None
    dup_val = False
    out_val = False
    norm_val = None
    process_btn = False

    if uploaded_file:
        st.markdown("---")
        st.subheader("2. Configuration")

        miss_val = st.selectbox("Valeurs Manquantes", ['Ne rien faire', 'Supprimer les lignes', 'Moyenne (Mean)', 'Médiane (Median)', 'Mode (Fréquence)'])
        dup_val = st.checkbox("Supprimer les doublons", value=True)
        out_val = st.checkbox("Traiter les Aberrants (IQR)", value=False)
        norm_val = st.selectbox("Normalisation", ['Aucune', 'MinMax (0-1)', 'Standard (Z-Score)'])

        st.markdown("---")
        process_btn = st.button("LANCER LE TRAITEMENT 🚀")

# --- CORPS PRINCIPAL ---
if uploaded_file is not None:
    # Chargement
    df = load_data(uploaded_file)
    
    if isinstance(df, str):
        st.error(f"Erreur : {df}")
    else:
        # Création des onglets pour organiser l'affichage
        tab1, tab2, tab3 = st.tabs(["📊 Données Brutes", "⚙️ Traitement & Résultats", "📥 Export"])
        
        with tab1:
            st.info(f"Fichier chargé : **{uploaded_file.name}**")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Lignes", df.shape[0])
            col2.metric("Colonnes", df.shape[1])
            col3.metric("Doublons", df.duplicated().sum())
            col4.metric("Valeurs Nulles", df.isnull().sum().sum())

            with st.expander("Voir l'aperçu du tableau", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)

        with tab2:
            # Logique de traitement au clic
            if process_btn:
                with st.spinner('Nettoyage en cours...'):
                    time.sleep(1) # Petit effet visuel
                    df_clean = df.copy()

                    # Pipeline de traitement
                    # 1. Manquantes
                    if miss_val != 'Ne rien faire':
                        df_clean = handle_missing_values(df_clean, miss_val)

                    # 2. Doublons
                    if dup_val:
                        df_clean = remove_duplicates(df_clean)

                    # 3. Outliers
                    if out_val:
                        df_clean = handle_outliers_iqr(df_clean)

                    # 4. Normalisation
                    if norm_val != 'Aucune':
                        df_clean = normalize_data(df_clean, norm_val)

                    st.success("Traitement terminé avec succès !")

                    # Affichage Comparatif
                    col_a, col_b = st.columns(2)
                    col_a.info("Avant Traitement")
                    col_a.write(df.describe())

                    col_b.success("Après Traitement")
                    col_b.write(df_clean.describe())

                    st.write("### Aperçu des données nettoyées")
                    st.dataframe(df_clean.head(10), use_container_width=True)

                    # Sauvegarde dans la session pour l'export
                    st.session_state['df_clean'] = df_clean
            else:
                st.info("⚙️ Configurez les options dans la barre latérale et cliquez sur 'LANCER LE TRAITEMENT' pour commencer.")

        with tab3:
            st.write("### Téléchargement")
            if 'df_clean' in st.session_state:
                csv_data = convert_df_to_csv(st.session_state['df_clean'])
                st.download_button(
                    label="💾 Télécharger le fichier CSV nettoyé",
                    data=csv_data,
                    file_name=f"clean_{uploaded_file.name}.csv",
                    mime='text/csv',
                )
            else:
                st.warning("Veuillez d'abord lancer le traitement dans l'onglet précédent.")

else:
    # Message d'accueil quand rien n'est chargé
    st.info("👋 Bienvenue ! Veuillez charger un fichier dans la barre latérale gauche pour commencer.")
    st.markdown("""
    #### Fonctionnalités supportées :
    * ✅ Détection et suppression des doublons
    * ✅ Imputation des valeurs manquantes
    * ✅ Gestion des outliers (Méthode IQR)
    * ✅ Normalisation (MinMax, Z-Score)
    """)