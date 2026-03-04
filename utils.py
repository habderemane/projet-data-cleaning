import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import io
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

def load_data(uploaded_file):
    """Charge le fichier selon son extension avec gestion d'erreurs.
    
    Reconnaît automatiquement les valeurs nulles sous différentes formes:
    'na', 'NA', 'N/A', 'n/a', 'null', 'NULL', 'None', 'NaN', '', ' ', etc.
    """
    if uploaded_file is None:
        return None
    
    # Définir toutes les variantes de valeurs nulles à reconnaître
    na_values = [
        '', ' ', 'na', 'NA', 'Na', 'n/a', 'N/A', 'n.a.', 'N.A.',
        'null', 'NULL', 'Null', 'none', 'None', 'NONE',
        'nan', 'NaN', 'NAN', '-', '--', '?', 'N/D', 'n/d',
        'missing', 'Missing', 'MISSING', 'undefined', 'Undefined'
    ]
    
    filename = uploaded_file.name
    try:
        if filename.endswith('.csv'):
            return pd.read_csv(uploaded_file, na_values=na_values, keep_default_na=True)
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            return pd.read_excel(uploaded_file, na_values=na_values, keep_default_na=True)
        elif filename.endswith('.json'):
            df = pd.read_json(uploaded_file)
            # Remplacer manuellement les valeurs nulles pour JSON
            return df.replace(na_values, np.nan)
        elif filename.endswith('.xml'):
            df = pd.read_xml(uploaded_file)
            # Remplacer manuellement les valeurs nulles pour XML
            return df.replace(na_values, np.nan)
        else:
            return "Format non supporté"
    except Exception as e:
        return str(e)

def handle_missing_values(df, strategy):
    """
    Gère les valeurs manquantes selon la stratégie choisie.
    
    Pour les colonnes catégorielles (non numériques), utilise automatiquement 
    le mode (valeur la plus fréquente) quelle que soit la stratégie choisie.
    """
    df_clean = df.copy()
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    categorical_cols = df_clean.select_dtypes(exclude=[np.number]).columns

    if strategy == 'Supprimer les lignes':
        df_clean = df_clean.dropna()
    elif strategy == 'Moyenne (Mean)':
        # Appliquer la moyenne aux colonnes numériques
        if len(numeric_cols) > 0:
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
        # Appliquer le mode aux colonnes catégorielles
        for col in categorical_cols:
            if df_clean[col].isnull().sum() > 0:
                mode_values = df_clean[col].mode()
                if len(mode_values) > 0:
                    df_clean[col] = df_clean[col].fillna(mode_values.iloc[0])
    elif strategy == 'Médiane (Median)':
        # Appliquer la médiane aux colonnes numériques
        if len(numeric_cols) > 0:
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
        # Appliquer le mode aux colonnes catégorielles
        for col in categorical_cols:
            if df_clean[col].isnull().sum() > 0:
                mode_values = df_clean[col].mode()
                if len(mode_values) > 0:
                    df_clean[col] = df_clean[col].fillna(mode_values.iloc[0])
    elif strategy == 'Mode (Fréquence)':
        # Appliquer le mode à toutes les colonnes
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


def convert_df_to_excel(df):
    """Convertit un DataFrame en format Excel (.xlsx)."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Données Nettoyées')
    return output.getvalue()


def convert_df_to_json(df):
    """Convertit un DataFrame en format JSON encodé en UTF-8."""
    return df.to_json(orient='records', force_ascii=False, indent=2).encode('utf-8')


def convert_df_to_xml(df):
    """Convertit un DataFrame en format XML encodé en UTF-8."""
    try:
        return df.to_xml(index=False).encode('utf-8')
    except Exception:
        # Fallback manuel si to_xml n'est pas disponible
        lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<data>']
        for _, row in df.iterrows():
            lines.append('  <row>')
            for col in df.columns:
                safe_col = str(col).replace(' ', '_')
                lines.append(f'    <{safe_col}>{row[col]}</{safe_col}>')
            lines.append('  </row>')
        lines.append('</data>')
        return '\n'.join(lines).encode('utf-8')


def create_donut_chart(data_dict, total):
    """
    Crée un graphique en anneau (donut) pour visualiser la répartition des fichiers par type.

    Args:
        data_dict: Dictionnaire {label: count}
        total: Nombre total pour affichage central
    Returns:
        Figure matplotlib
    """
    if not data_dict:
        return None

    labels = list(data_dict.keys())
    sizes = list(data_dict.values())
    palette = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
    colors = palette[:len(labels)]

    fig, ax = plt.subplots(figsize=(5, 5), facecolor='#1e2139')
    ax.set_facecolor('#1e2139')

    wedges, _ = ax.pie(
        sizes, labels=None, colors=colors, startangle=90,
        wedgeprops=dict(width=0.55, edgecolor='#1e2139', linewidth=3)
    )

    # Texte central
    ax.text(0, 0.08, str(total), ha='center', va='center',
            fontsize=28, fontweight='bold', color='white')
    ax.text(0, -0.22, 'Total', ha='center', va='center',
            fontsize=11, color='#a0a9c0')

    # Légende
    legend_patches = [
        mpatches.Patch(color=colors[i], label=f'{labels[i].upper()}  {sizes[i]}')
        for i in range(len(labels))
    ]
    ax.legend(
        handles=legend_patches, loc='lower center',
        bbox_to_anchor=(0.5, -0.18), ncol=2,
        frameon=False, labelcolor='white', fontsize=9,
        handlelength=1.2, handleheight=1.2
    )

    plt.tight_layout()
    return fig


def create_boxplot(df, title="Distribution des données numériques"):
    """
    Crée des boxplots pour toutes les colonnes numériques du DataFrame.
    
    Args:
        df: DataFrame pandas
        title: Titre du graphique
        
    Returns:
        Figure matplotlib
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        return None
    
    # Créer une figure avec plusieurs sous-graphiques si nécessaire
    n_cols = len(numeric_cols)
    n_rows = (n_cols + 2) // 3  # 3 colonnes par ligne
    n_subplot_cols = min(3, n_cols)
    
    fig, axes = plt.subplots(n_rows, n_subplot_cols, figsize=(5*n_subplot_cols, 4*n_rows))
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    # S'assurer que axes est toujours un tableau 1D
    if n_cols == 1:
        axes = np.array([axes])
    else:
        axes = np.array(axes).flatten()
    
    # Créer un boxplot pour chaque colonne
    for idx, col in enumerate(numeric_cols):
        ax = axes[idx]
        
        # Créer le boxplot
        bp = ax.boxplot(df[col].dropna(), patch_artist=True, vert=True)
        
        # Colorer les boxplots
        for patch in bp['boxes']:
            patch.set_facecolor('#3498db')
            patch.set_alpha(0.7)
        
        for whisker in bp['whiskers']:
            whisker.set(color='#2c3e50', linewidth=1.5)
        
        for cap in bp['caps']:
            cap.set(color='#2c3e50', linewidth=1.5)
        
        for median in bp['medians']:
            median.set(color='#e74c3c', linewidth=2)
        
        for flier in bp['fliers']:
            flier.set(marker='o', color='#e74c3c', alpha=0.5)
        
        ax.set_title(col, fontweight='bold')
        ax.set_ylabel('Valeur')
        ax.grid(True, alpha=0.3)
    
    # Masquer les axes non utilisés
    for idx in range(n_cols, len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    return fig


def detect_outliers_info(df):
    """
    Détecte et retourne les informations sur les valeurs aberrantes (outliers) 
    pour chaque colonne numérique.
    
    Args:
        df: DataFrame pandas
        
    Returns:
        Dict avec les statistiques des outliers par colonne
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers_info = {}
    
    for col in numeric_cols:
        if df[col].notna().sum() > 0:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[col][(df[col] < lower_bound) | (df[col] > upper_bound)]
            
            outliers_info[col] = {
                'count': len(outliers),
                'percentage': (len(outliers) / len(df[col].dropna())) * 100,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'Q1': Q1,
                'Q3': Q3,
                'IQR': IQR
            }
    
    return outliers_info


def get_missing_values_info(df):
    """
    Analyse détaillée des valeurs manquantes dans le DataFrame.
    
    Args:
        df: DataFrame pandas
        
    Returns:
        DataFrame avec les statistiques des valeurs manquantes par colonne
    """
    missing_info = []
    
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            missing_info.append({
                'Colonne': col,
                'Type': str(df[col].dtype),
                'Valeurs Manquantes': missing_count,
                'Pourcentage': f"{(missing_count / len(df)) * 100:.2f}%",
                'Valeurs Présentes': len(df) - missing_count
            })
    
    return pd.DataFrame(missing_info) if missing_info else None
