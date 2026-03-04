"""Module pour gérer l'historique des fichiers traités."""
import json
import os
from datetime import datetime


HISTORY_FILE = "processing_history.json"


def save_to_history(filename, original_rows, cleaned_rows, operations, file_type=None, export_format=None):
    """
    Sauvegarde un enregistrement dans l'historique des fichiers traités.
    
    Args:
        filename: Nom du fichier traité
        original_rows: Nombre de lignes avant traitement
        cleaned_rows: Nombre de lignes après traitement
        operations: Liste des opérations effectuées
        file_type: Type du fichier source (csv, xlsx, json, xml)
        export_format: Format d'export choisi
    """
    # Charger l'historique existant
    history = load_history()
    
    # Déduire le type de fichier depuis le nom si non fourni
    if file_type is None:
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'unknown'
        file_type = ext
    
    # Créer un nouvel enregistrement
    record = {
        "filename": filename,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original_rows": original_rows,
        "cleaned_rows": cleaned_rows,
        "rows_removed": original_rows - cleaned_rows,
        "operations": operations,
        "file_type": file_type,
        "export_format": export_format or file_type
    }
    
    # Ajouter au début de la liste (plus récent en premier)
    history.insert(0, record)
    
    # Limiter à 100 derniers enregistrements
    history = history[:100]
    
    # Sauvegarder
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    
    return record


def load_history():
    """Charge l'historique des traitements depuis le fichier JSON."""
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def clear_history():
    """Efface tout l'historique."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    return []


def is_file_already_processed(filename):
    """
    Vérifie si un fichier a déjà été traité.
    
    Args:
        filename: Nom du fichier à vérifier
        
    Returns:
        Tuple (bool, dict or None): (True, dernier_record) si déjà traité, (False, None) sinon
    """
    history = load_history()
    
    for record in history:
        if record['filename'] == filename:
            return True, record
    
    return False, None
