# 🧹 DataClean Pro — API d'Automatisation de Traitement de Données

## 📝 Informations sur le Projet
* **Auteur** : HANANE Abderemane
* **Email** : hananeabderemane@gmail.com
* **Projet** : Python M1 IAGE — Institut Supérieur d'Informatique (ISI)

---

## 🚀 Description

**DataClean Pro** est une application web complète permettant d'automatiser le processus de **Data Processing** (nettoyage et normalisation de données). Grâce à une interface graphique moderne avec thème sombre, l'outil permet aux utilisateurs de charger des jeux de données bruts et d'appliquer des techniques de nettoyage et de normalisation sans écrire de code.

### ✨ Nouveautés de la dernière version

* **Système d'authentification** : Connexion / inscription avec gestion des utilisateurs
* **Interface sombre (Dark Theme)** : Design moderne inspiré du style Corona
* **Navigation multi-pages** : Dashboard, Upload & Traitement, Historique
* **Dashboard interactif** : Statistiques globales, graphique donut par type de fichier, derniers fichiers traités
* **Détection améliorée des fichiers déjà traités** : Bannière informative non bloquante avec possibilité de re-traitement
* **Export multi-formats** : CSV, Excel (.xlsx), JSON, XML

## 📂 Structure du projet

```
projet_data_cleaning/
│
├── app.py                  # Point d'entrée — Interface Streamlit (auth, pages, UI)
├── utils.py                # Logique métier (nettoyage, calculs, visualisations, exports)
├── history.py              # Gestion de l'historique des fichiers traités
├── users.json              # Base de données des utilisateurs (généré automatiquement)
├── processing_history.json # Historique des traitements (généré automatiquement)
├── requirements.txt        # Dépendances Python
├── Readme.md               # Documentation du projet
├── LICENSE                 # Licence MIT
├── Procfile                # Configuration de déploiement (Render)
├── render.yaml             # Spec de déploiement Render
├── data/                   # Dossier de données exemples
│   ├── customers-1000.csv  # Fichier de données exemple
│   └── test_data.csv       # Fichier de test
└── .venv/                  # Environnement virtuel (non inclus dans le dépôt)
```

### 🎯 Fonctionnalités principales

| # | Fonctionnalité | Description |
|---|----------------|-------------|
| 1 | **Authentification** | Connexion / inscription, profils utilisateurs (Gold, Silver, Member) |
| 2 | **Valeurs manquantes** | Suppression ou imputation (Moyenne, Médiane, Mode) avec détection avancée |
| 3 | **Doublons** | Identification et suppression automatique |
| 4 | **Outliers (IQR)** | Détection, visualisation (boxplots) et traitement |
| 5 | **Normalisation** | MinMax Scaling ou Standard Scaling (Z-Score) |
| 6 | **Export multi-formats** | CSV, Excel, JSON, XML |
| 7 | **Dashboard** | Statistiques globales, graphique donut avec couleurs par type (🔵 CSV, 🟢 Excel, 🟠 JSON, 🔴 XML), fichiers récents |
| 8 | **Historique** | Suivi automatique avec horodatage (100 derniers traitements) |
| 9 | **Protection doublon** | Avertissement si le fichier a déjà été traité |

### 🛠 Technologies utilisées

* **Langage :** Python 3.x
* **Interface (Frontend/Backend) :** Streamlit
* **Manipulation de données :** Pandas, NumPy
* **Traitement avancé :** Scikit-learn (normalisation)
* **Visualisation :** Matplotlib, Seaborn
* **Formats supportés :** CSV, Excel (.xlsx, .xls), JSON, XML

---

## ⚙️ Installation et Configuration

### 1. Prérequis
Assurez-vous d'avoir **Python 3.8+** installé sur votre machine.

### 2. Création de l'environnement virtuel

```bash
# Windows
python -m venv .venv

# Mac / Linux
python3 -m venv .venv
```

### 3. Activation de l'environnement virtuel

```bash
# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 4. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 5. Lancement de l'application

```bash
streamlit run app.py
```

L'application s'ouvrira dans votre navigateur par défaut (généralement <http://localhost:8501>).

---

## 🔐 Authentification

L'application intègre un système de connexion et d'inscription :

* **Comptes par défaut :**
  * `admin` / `admin123` (Gold Member)
  * `user` / `pass123` (Silver Member)
* **Inscription** : Créez un nouveau compte depuis l'onglet "Inscription"
* Les comptes sont stockés dans `users.json`

---

## 🌐 Versionnement

Ce projet est versionné avec **Git** et hébergé sur **GitHub**.

![GitHub repo](https://img.shields.io/badge/GitHub-Projet%20versionn%C3%A9-blue?logo=github)

---

## 💡 Utilisation de l'application

### Étapes d'utilisation

1. **Se connecter** : Entrez vos identifiants ou créez un compte
2. **Dashboard** : Consultez le tableau de bord avec les statistiques globales et les derniers fichiers traités
3. **Charger un fichier** : Naviguez vers "Upload & Traitement" et importez votre fichier
   * L'application affiche un avertissement si le fichier a déjà été traité
4. **Visualiser les données brutes** : Onglet "📊 Données Brutes" :
   * Statistiques générales (lignes, colonnes, doublons, valeurs manquantes, outliers)
   * Détails des valeurs manquantes par colonne
   * Aperçu du tableau
5. **Analyser les outliers** : Onglet "📦 Analyse Outliers" :
   * Boxplots pour toutes les colonnes numériques
   * Tableau récapitulatif des outliers avec pourcentages et bornes IQR
6. **Configurer le traitement** : Dans la barre latérale :
   * Valeurs Manquantes (Ne rien faire, Supprimer, Moyenne, Médiane, Mode)
   * Suppression des doublons
   * Traitement des valeurs aberrantes (IQR)
   * Normalisation (Aucune, MinMax, Z-Score)
7. **Lancer le traitement** : Cliquez sur "🚀 LANCER LE TRAITEMENT"
8. **Consulter les résultats** : Onglet "⚙️ Traitement" :
   * Comparaison avant/après (statistiques descriptives)
   * Boxplots comparatifs côte à côte
   * Aperçu des données nettoyées
9. **Exporter** : Onglet "📥 Export" — téléchargez en CSV, Excel, JSON ou XML
10. **Historique** : Page dédiée avec tableau récapitulatif et détails des traitements

---

## 📖 Détails des fonctionnalités

### 1. Reconnaissance avancée des valeurs manquantes

L'application reconnaît automatiquement les valeurs nulles sous de multiples formats :
* Vides : `''`, `' '` (espaces)
* Variantes "na" : `na`, `NA`, `Na`, `n/a`, `N/A`, `n.a.`, `N.A.`
* Null : `null`, `NULL`, `Null`
* None : `none`, `None`, `NONE`
* NaN : `nan`, `NaN`, `NAN`
* Symboles : `-`, `--`, `?`
* Français : `N/D`, `n/d`
* Autres : `missing`, `Missing`, `undefined`, `Undefined`

### 2. Gestion intelligente des valeurs manquantes

* **Supprimer les lignes** : Élimine toutes les lignes contenant au moins une valeur manquante
* **Moyenne (Mean)** : Remplace par la moyenne (colonnes numériques) ; Mode pour les colonnes catégorielles
* **Médiane (Median)** : Remplace par la médiane (colonnes numériques) ; Mode pour les colonnes catégorielles
* **Mode (Fréquence)** : Remplace par la valeur la plus fréquente (tous types de données)

### 3. Suppression des doublons

Identifie et supprime automatiquement les lignes dupliquées en conservant la première occurrence.

### 4. Détection et traitement des valeurs aberrantes (Outliers)

**Méthode IQR (Interquartile Range) :**
* Calcule Q1 (25e percentile) et Q3 (75e percentile)
* IQR = Q3 - Q1
* Remplace les valeurs < Q1 - 1.5×IQR par la borne inférieure
* Remplace les valeurs > Q3 + 1.5×IQR par la borne supérieure

**Visualisation :**
* Boxplots colorés par colonne numérique
* Tableau récapitulatif (nombre, pourcentage, bornes)
* Comparaison avant/après côte à côte

### 5. Normalisation des données

* **MinMax (0-1)** : `x_norm = (x - x_min) / (x_max - x_min)`
* **Standard (Z-Score)** : `x_norm = (x - μ) / σ`

### 6. Historique des traitements

* Sauvegarde automatique dans `processing_history.json`
* Informations : date/heure, nom du fichier, lignes avant/après, opérations
* Affichage sur la page Historique avec détails extensibles
* Conservation des 100 derniers enregistrements

---

## 🌍 Déploiement

### Streamlit Community Cloud (gratuit)

1. Aller sur [share.streamlit.io](https://share.streamlit.io) et se connecter avec GitHub
2. Cliquer sur **"New app"** → **"Paste GitHub URL"**
3. Coller : `https://github.com/habderemane/projet-data-cleaning/blob/main/app.py`
4. Cliquer sur **Deploy**

> Pour un repo privé : Settings → Manage GitHub permissions → autoriser l'accès au repo.

L'application sera accessible à : `https://projet-data-cleaning-xxxx.streamlit.app`

---

## 🐛 Résolution de problèmes

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError: No module named 'streamlit'` | Activez l'environnement virtuel puis `pip install -r requirements.txt` |
| Erreur chargement Excel | `pip install openpyxl` |
| L'application ne se lance pas | Vérifiez : `streamlit --version` puis `pip install streamlit` |

---

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 📬 Contact & Contributions

Pour toute suggestion, bug ou contribution, ouvrez une issue ou une pull request sur le dépôt GitHub associé.

---

Développé avec ❤️ pour les étudiants et développeurs souhaitant automatiser le nettoyage de données !
