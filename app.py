import streamlit as st
import pandas as pd
import time
from utils import (load_data, handle_missing_values, remove_duplicates, 
                   handle_outliers_iqr, normalize_data, convert_df_to_csv,
                   create_boxplot, detect_outliers_info, get_missing_values_info)
from history import save_to_history, load_history, clear_history, is_file_already_processed

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
        st.caption("ℹ️ Pour les colonnes catégorielles, le Mode sera toujours utilisé automatiquement")
        dup_val = st.checkbox("Supprimer les doublons", value=True)
        out_val = st.checkbox("Traiter les Aberrants (IQR)", value=False)
        norm_val = st.selectbox("Normalisation", ['Aucune', 'MinMax (0-1)', 'Standard (Z-Score)'])

        st.markdown("---")
        process_btn = st.button("LANCER LE TRAITEMENT 🚀")

# --- CORPS PRINCIPAL ---
if uploaded_file is not None:
    # Vérifier si le fichier a déjà été traité
    already_processed, last_record = is_file_already_processed(uploaded_file.name)
    
    if already_processed:
        st.error(f"⛔ **Fichier déjà traité !**")
        st.warning(f"Le fichier **{uploaded_file.name}** a déjà été traité le **{last_record['timestamp']}**.")
        
        with st.expander("📋 Détails du traitement précédent"):
            st.write(f"**Lignes traitées:** {last_record['original_rows']} → {last_record['cleaned_rows']}")
            st.write(f"**Lignes supprimées:** {last_record['rows_removed']}")
            st.write("**Opérations effectuées:**")
            for op in last_record['operations']:
                st.write(f"  - {op}")
        
        st.info("💡 **Suggestions:** Renommez le fichier ou supprimez l'historique pour pouvoir le traiter à nouveau.")
        
        # Bouton pour permettre quand même le traitement (forcer)
        col1, col2 = st.columns([3, 1])
        with col2:
            force_process = st.button("🔓 Forcer le traitement")
        
        if not force_process:
            st.stop()
    
    # Chargement
    df = load_data(uploaded_file)
    
    if isinstance(df, str):
        st.error(f"Erreur : {df}")
    else:
        # Création des onglets pour organiser l'affichage
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Données Brutes", "📦 Analyse des Outliers", "⚙️ Traitement & Résultats", "📥 Export"])
        
        with tab1:
            st.info(f"Fichier chargé : **{uploaded_file.name}**")
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Lignes", df.shape[0])
            col2.metric("Colonnes", df.shape[1])
            col3.metric("Doublons", df.duplicated().sum())
            col4.metric("Valeurs Manquantes", df.isnull().sum().sum())
            col5.metric("Valeures abererantes (IQR)", sum([df[col].apply(lambda x: x < (df[col].quantile(0.25) - 1.5 * (df[col].quantile(0.75) - df[col].quantile(0.25))) or x > (df[col].quantile(0.75) + 1.5 * (df[col].quantile(0.75) - df[col].quantile(0.25))) if pd.notnull(x) else False).sum() for col in df.select_dtypes(include=['number']).columns]))

            # Détails sur les valeurs manquantes
            missing_df = get_missing_values_info(df)
            if missing_df is not None:
                with st.expander("🔍 Détails des Valeurs Manquantes (NA, null, etc.)", expanded=False):
                    st.dataframe(missing_df, use_container_width=True)
                    st.caption("✅ Les valeurs reconnues comme nulles: '', 'na', 'NA', 'N/A', 'null', 'NULL', 'None', 'NaN', '-', '--', '?', 'N/D', 'missing', etc.")
            
            with st.expander("Voir l'aperçu du tableau", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)

        with tab2:
            st.subheader("📦 Analyse des Valeurs Aberrantes (Outliers)")
            
            # Détecter les outliers
            outliers_info = detect_outliers_info(df)
            
            if outliers_info:
                # Afficher un résumé des outliers
                st.write("### Résumé des valeurs aberrantes")
                
                summary_data = []
                for col, info in outliers_info.items():
                    summary_data.append({
                        "Colonne": col,
                        "Nombre d'outliers": info['count'],
                        "Pourcentage": f"{info['percentage']:.2f}%",
                        "Borne inférieure": f"{info['lower_bound']:.2f}",
                        "Borne supérieure": f"{info['upper_bound']:.2f}"
                    })
                
                st.dataframe(pd.DataFrame(summary_data), use_container_width=True)
                
                # Créer et afficher les boxplots
                st.write("### Visualisation des Boxplots")
                st.info("Les points rouges représentent les valeurs aberrantes détectées par la méthode IQR (Interquartile Range)")
                
                fig = create_boxplot(df, "Distribution et Détection des Outliers")
                if fig:
                    st.pyplot(fig)
                else:
                    st.warning("Aucune colonne numérique à afficher.")
            else:
                st.info("Aucune colonne numérique trouvée dans ce fichier.")

        with tab3:
            # Logique de traitement au clic
            if process_btn:
                with st.spinner('Nettoyage en cours...'):
                    time.sleep(1) # Petit effet visuel
                    df_clean = df.copy()
                    
                    # Enregistrer les opérations pour l'historique
                    operations_performed = []

                    # Pipeline de traitement
                    # 1. Manquantes
                    if miss_val != 'Ne rien faire':
                        df_clean = handle_missing_values(df_clean, miss_val)
                        operations_performed.append(f"Valeurs manquantes: {miss_val}")

                    # 2. Doublons
                    if dup_val:
                        df_clean = remove_duplicates(df_clean)
                        operations_performed.append("Suppression des doublons")

                    # 3. Outliers
                    if out_val:
                        df_clean = handle_outliers_iqr(df_clean)
                        operations_performed.append("Traitement des outliers (IQR)")

                    # 4. Normalisation
                    if norm_val != 'Aucune':
                        df_clean = normalize_data(df_clean, norm_val)
                        operations_performed.append(f"Normalisation: {norm_val}")

                    st.success("Traitement terminé avec succès !")
                    
                    # Sauvegarder dans l'historique
                    save_to_history(
                        filename=uploaded_file.name,
                        original_rows=len(df),
                        cleaned_rows=len(df_clean),
                        operations=operations_performed
                    )

                    # Affichage Comparatif
                    col_a, col_b = st.columns(2)
                    col_a.info("Avant Traitement")
                    col_a.write(df.describe())

                    col_b.success("Après Traitement")
                    col_b.write(df_clean.describe())

                    st.write("### Aperçu des données nettoyées")
                    st.dataframe(df_clean.head(10), use_container_width=True)
                    
                    # Afficher les boxplots comparatifs
                    st.write("### Comparaison des Outliers - Avant vs Après")
                    col_box1, col_box2 = st.columns(2)
                    
                    with col_box1:
                        st.write("**Avant traitement**")
                        fig_before = create_boxplot(df, "Avant Traitement")
                        if fig_before:
                            st.pyplot(fig_before)
                    
                    with col_box2:
                        st.write("**Après traitement**")
                        fig_after = create_boxplot(df_clean, "Après Traitement")
                        if fig_after:
                            st.pyplot(fig_after)

                    # Sauvegarde dans la session pour l'export
                    st.session_state['df_clean'] = df_clean
            else:
                st.info("⚙️ Configurez les options dans la barre latérale et cliquez sur 'LANCER LE TRAITEMENT' pour commencer.")

        with tab4:
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
    * ✅ Visualisation des outliers avec Boxplots
    * ✅ Historique des fichiers traités
    """)
    
    # Afficher l'historique des traitements
    st.markdown("---")
    st.subheader("📜 Historique des Fichiers Traités")
    
    history = load_history()
    
    if history:
        # Bouton pour effacer l'historique
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("🗑️ Effacer l'historique"):
                clear_history()
                st.rerun()
        
        # Afficher l'historique sous forme de tableau
        history_df = pd.DataFrame(history)
        
        # Reformater pour l'affichage
        display_df = history_df[['timestamp', 'filename', 'original_rows', 'cleaned_rows', 'rows_removed']].copy()
        display_df.columns = ['Date & Heure', 'Fichier', 'Lignes Initiales', 'Lignes Finales', 'Lignes Supprimées']
        
        st.dataframe(display_df, use_container_width=True, height=300)
        
        # Afficher les détails des opérations dans des expanders
        st.write("### Détails des traitements")
        for idx, record in enumerate(history[:5]):  # Afficher les 5 derniers
            with st.expander(f"📄 {record['filename']} - {record['timestamp']}"):
                st.write(f"**Lignes traitées:** {record['original_rows']} → {record['cleaned_rows']}")
                st.write("**Opérations effectuées:**")
                for op in record['operations']:
                    st.write(f"  - {op}")
    else:
        st.info("Aucun fichier n'a encore été traité. L'historique apparaîtra ici après le premier traitement.")