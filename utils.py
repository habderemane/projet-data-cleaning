import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import io

def load_data(uploaded_file):
    """Charge le fichier selon son extension avec gestion d'erreurs."""
    if uploaded_file is None:
        return None
    
    filename = uploaded_file.name
    try:
        if filename.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            return pd.read_excel(uploaded_file)
        elif filename.endswith('.json'):
            return pd.read_json(uploaded_file)
        elif filename.endswith('.xml'):
            return pd.read_xml(uploaded_file)
        else:
            return "Format non supporté"
    except Exception as e:
        return str(e)

def handle_missing_values(df, strategy):
    """Gère les valeurs manquantes selon la stratégie choisie."""
    df_clean = df.copy()
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns

    if strategy == 'Supprimer les lignes':
        df_clean = df_clean.dropna()
    elif strategy == 'Moyenne (Mean)':
        if len(numeric_cols) > 0:
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
    elif strategy == 'Médiane (Median)':
        if len(numeric_cols) > 0:
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
    elif strategy == 'Mode (Fréquence)':
        for col in df_clean.columns:
            if df_clean[col].isnull().sum() > 0:
                mode_values = df_clean[col].mode()
                if len(mode_values) > 0:
                    df_clean[col] = df_clean[col].fillna(mode_values.iloc[0])

    return df_clean

def remove_duplicates(df):
    """Supprime les lignes dupliquées du DataFrame."""
    return df.drop_duplicates()

def handle_outliers_iqr(df):
    """Traite les valeurs aberrantes en utilisant la méthode IQR (Interquartile Range)."""
    df_clean = df.copy()
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        if df_clean[col].notna().sum() > 0:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            df_clean[col] = np.where(df_clean[col] < lower_bound, lower_bound, df_clean[col])
            df_clean[col] = np.where(df_clean[col] > upper_bound, upper_bound, df_clean[col])

    return df_clean

def normalize_data(df, method):
    """Normalise les données numériques selon la méthode choisie."""
    df_norm = df.copy()
    numeric_cols = df_norm.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) == 0:
        return df_norm

    if method == 'MinMax (0-1)':
        scaler = MinMaxScaler()
        df_norm[numeric_cols] = scaler.fit_transform(df_norm[numeric_cols])
    elif method == 'Standard (Z-Score)':
        scaler = StandardScaler()
        df_norm[numeric_cols] = scaler.fit_transform(df_norm[numeric_cols])

    return df_norm

def convert_df_to_csv(df):
    """Convertit un DataFrame en format CSV encodé en UTF-8."""
    return df.to_csv(index=False).encode('utf-8')