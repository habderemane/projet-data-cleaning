# 🧹 API d'Automatisation de Traitement de Données (Data Cleaning)

## 📝 Informations sur le Projet
* **Auteurs** : HANANE Abderemane
*  **Emails** : hananeabderemane@gmail.com

---

## 🚀 Description

Ce projet vise à mettre en place une API (Interface Applicative) graphique permettant d'automatiser le processus de **Data Processing**. L'outil permet aux utilisateurs de charger des jeux de données bruts et d'appliquer des techniques de nettoyage et de normalisation sans écrire de code.

## 📂 Structure du projet

```
projet_data_cleaning/
│
├── app.py                # Point d'entrée de l'application (Interface Streamlit)
├── utils.py              # Fonctions de logique métier (Nettoyage, Calculs, Visualisations)
├── history.py            # Gestion de l'historique des fichiers traités
├── requirements.txt      # Liste des dépendances Python
├── Readme.md             # Documentation du projet
├── LICENSE               # Licence du projet (MIT)
├── .gitignore            # Fichiers à ignorer par Git
├── data/                 # Dossier contenant les fichiers de données
│   ├── customers-1000.csv  # Fichier de données exemple
│   └── test_data.csv       # Fichier de test
├── processing_history.json # Historique des traitements (généré automatiquement)
└── myenv/                # Environnement virtuel (non inclus dans le rendu)
```

### 🎯 Objectifs
L'application automatise les tâches suivantes :
1.  **Gestion des valeurs manquantes :** Suppression ou imputation (Moyenne, Médiane, Mode).
    * Reconnaissance automatique de multiples formats de valeurs nulles (na, NA, null, NULL, N/A, etc.)
    * Traitement intelligent : Mode automatique pour les colonnes catégorielles
2.  **Traitement des doublons :** Identification et suppression.
3.  **Détection des valeurs aberrantes (Outliers) :** Méthode de l'intervalle interquartile (IQR).
    * Visualisation graphique avec Boxplots
    * Statistiques détaillées des outliers par colonne
4.  **Normalisation des données :** MinMax Scaling ou Standard Scaling (Z-Score).
5.  **Exportation :** Téléchargement du jeu de données propre.
6.  **Historique des traitements :** Suivi automatique de tous les fichiers traités avec horodatage.
7.  **Protection contre la duplication :** Empêche le traitement multiple d'un même fichier.

### 🛠 Technologies utilisées
* **Langage :** Python 3.x
* **Interface (Frontend/Backend) :** Streamlit
* **Manipulation de données :** Pandas, NumPy
* **Traitement avancé :** Scikit-learn (pour la normalisation)
* **Visualisation :** Matplotlib, Seaborn (pour les boxplots)
* **Formats supportés :** CSV, Excel (.xlsx, .xls), JSON, XML

---

## ⚙️ Installation et Configuration

Suivez ces instructions pour installer le projet sur votre machine locale.

### 1. Prérequis
Assurez-vous d'avoir **Python** installé sur votre machine.

### 2. Création de l'environnement virtuel
Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances. Ouvrez votre terminal à la racine du projet :

```bash
# Windows
python -m venv myenv

# Mac / Linux
python3 -m venv myenv
```

### 3. Activation de l'environnement virtuel

```bash
# Windows
myenv\Scripts\activate
# Mac / Linux
source myenv/bin/activate
```

### 4. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 5. Lancement de l'application

```bash
streamlit run app.py
```

L'application s'ouvrira dans votre navigateur par défaut à l'adresse indiquée par Streamlit (généralement <http://localhost:8501>).

---

## 🌐 Versionnement

Ce projet est maintenant initialisé avec **Git** et hébergé sur **GitHub**. N'hésitez pas à cloner, forker ou proposer des pull requests !

![GitHub repo](https://img.shields.io/badge/GitHub-Projet%20versionn%C3%A9-blue?logo=github)

---

## 💡 Utilisation de l'application

### Étapes d'utilisation

   * L'application vérifie automatiquement si le fichier a déjà été traité
2. **Visualiser les données brutes** : Consultez l'onglet "📊 Données Brutes" pour voir :
   * Statistiques générales (lignes, colonnes, doublons, valeurs manquantes, outliers)
   * Détails des valeurs manquantes par colonne
   * Aperçu du tableau
3. **Analyser les outliers** : L'onglet "📦 Analyse des Outliers" affiche :
   * Boxplots interactifs pour toutes les colonnes numériques
   * Tableau récapitulatif des outliers détectés avec pourcentages et bornes IQR
4. **Configurer le traitement** : Dans la barre latérale, choisissez vos options :
   * Valeurs Manquantes (suppression, moyenne, médiane, mode)
     * Note : Le mode est automatiquement appliqué aux colonnes catégorielles
   * Suppression des doublons
   * Traitement des valeurs aberrantes (IQR)
   * Normalisation (MinMax ou Z-Score)
5. **Lancer le traitement** : Cliquez sur "LANCER LE TRAITEMENT 🚀"
6. **Consulter les résultats** : L'onglet "⚙️ Traitement & Résultats" affiche :
   * Comparaison avant/après (statistiques)
   * Boxplots comparatifs pour visualiser l'impact du traitement
   * Aperçu des données nettoyées
7. **Exporter les données** : Téléchargez le fichier nettoyé depuis l'onglet "📥 Export"
8. **Consulter l'historique** : Sur la page d'accueil, visualisez tous les fichiers traités avec détailsaison avant/après
6. **Exporter les données** : Téléchargez le fichier nettoyé depuis l'onglet "📥 Export"

### Exemple de workflow

```bash
# 1. Lancer l'application
streamlit run app.py

# 2. Charger le fichier exemple
# Dans l'interface : Browse files → data/customers-1000.csv

# 3. Configurer les options de nettoyage
# - Valeurs Manquantes : Moyenne (Mean)
# - Supprimer les doublons : ✓
# - NorReconnaissance avancée des valeurs manquantes

L'application reconnaît automatiquement les valeurs nulles sous de multiples formats :
* Vides : `''`, `' '` (espaces)
* Variantes "na" : `na`, `NA`, `Na`, `n/a`, `N/A`, `n.a.`, `N.A.`
* Null : `null`, `NULL`, `Null`
* None : `none`, `None`, `NONE`
* NaN : `nan`, `NaN`, `NAN`
* Symboles : `-`, `--`, `?`
* Français : `N/D`, `n/d`
* Autres : `missing`, `Missing`, `undefined`, `Undefined`

Un tableau détaillé affiche pour chaque colonne concernée :
* Type de données
* Nombre et pourcentage de valeurs manquantes
* Nombre de valeurs présentes

### 2. Gestion intelligente des valeurs manquantes

* **Supprimer les lignes** : Élimine toutes les lignes contenant au moins une valeur manquante
* **Moyenne (Mean)** : Remplace les valeurs manquantes par la moyenne de la colonne (colonnes numériques uniquement)
  * Les colonnes catégorielles utilisent automatiquement le Mode
* **Médiane (Median)** : Remplace par la médiane (moins sensible aux valeurs extrêmes)
  * Les colonnes catégorielles utilisent automatiquement le Mode
* **Mode (Fréquence)** : Remplace par la valeur la plus fréquente (fonctionne sur tous types de données)

### 3. Suppression des doublons

Identifie et supprime automatiquement les lignes dupliquées en conservant la première occurrence.

### 4. Détection et visualisation des valeurs aberrantes (Outliers)

**Méthode IQR (Interquartile Range) :**
* Calcule Q1 (25e percentile) et Q3 (75e percentile)
* IQR = Q3 - Q1
* Remplace les valeurs < Q1 - 1.5×IQR par la borne inférieure
* Remplace les valeurs > Q3 + 1.5×IQR par la borne supérieure

**Visualisation graphique :**
* Boxplots colorés pour chaque colonne numérique
* Points rouges indiquant les outliers détectés
* Tableau récapitulatif avec :
  * Nombre d'outliers par colonne
  * Pourcentage d'outliers
  * Bornes de détection (inférieure et supérieure)
  * Valeurs Q1, Q3 et IQR

**Comparaison avant/après :**
* Affichage côte à côte des boxplots avant et après traitement
* Permet de visualiser l'impact du nettoyage

### 5. Normalisation des données

* **MinMax (0-1)** : Transforme les valeurs dans l'intervalle [0, 1]
  * Formula: `x_norm = (x - x_min) / (x_max - x_min)`
* **Standard (Z-Score)** : Standardise avec moyenne=0 et écart-type=1
  * Formula: `x_norm = (x - μ) / σ`

### 6. Historique des traitements

* **Sauvegarde automatique** de chaque traitement dans `processing_history.json`
* **Informations enregistrées :**
  * Date et heure du traitement
  * Nom du fichier
  * Nombre de lignes avant/après traitement
  * Nombre de lignes supprimées
  * Liste détaillée des opérations effectuées
* **Affichage sur la page d'accueil :**
  * Tableau récapitulatif des fichiers traités
  * Détails des 5 derniers traitements
  * Bouton pour effacer l'historique
* **Limite :** Conservation des 100 derniers enregistrements

### 7. Protection contre la duplication

* **Vérification automatique** lors du chargement d'un fichier
* **Si le fichier a déjà été traité :**
  * Message d'erreur avec date du dernier traitement
  * Affichage des détails du traitement précédent
  * Option "Forcer le traitement" pour permettre un nouveau traitement si nécessaire
* **Suggestions :** Renommer le fichier ou supprimer l'historiquele Range) :

* Calcule Q1 (25e percentile) et Q3 (75e percentile)
* IQR = Q3 - Q1
* Remplace les valeurs < Q1 - 1.5×IQR par la borne inférieure
* Remplace les valeurs > Q3 + 1.5×IQR par la borne supérieure

### 4. Normalisation des données

* **MinMax (0-1)** : Transforme les valeurs dans l'intervalle [0, 1]
  * Formula: `x_norm = (x - x_min) / (x_max - x_min)`
* **Standard (Z-Score)** : Standardise avec moyenne=0 et écart-type=1
  * Formula: `x_norm = (x - μ) / σ`

---

## 🔗 Bonnes pratiques Git

* Committez régulièrement vos modifications :
    ```bash
    git add .
    git commit -m "Message explicite"
    git push
    ```
* Utilisez des branches pour les nouvelles fonctionnalités ou corrections.
* Documentez vos changements dans les messages de commit.

---

## 🐛 Résolution de problèmes

### Erreur : "ModuleNotFoundError: No module named 'streamlit'"

```bash
# Solution : Assurez-vous d'activer l'environnement virtuel
myenv\Scripts\activate  # Windows
source myenv/bin/activate  # Mac/Linux

# Puis réinstallez les dépendances
pip install -r requirements.txt
```

### Erreur lors du chargement de fichiers Excel

```bash
# Installez openpyxl si ce n'est pas déjà fait
pip install openpyxl
```

### L'application ne se lance pas

```bash
# Vérifiez que Streamlit est bien installé
streamlit --version

# Si non installé
pip install streamlit
```

---

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 📬 Contact & Contributions

Pour toute suggestion, bug ou contribution, ouvrez une issue ou une pull request sur le dépôt GitHub associé.

---
Développé avec ❤️ pour les étudiants et developpeurs souhaitant automatiser le nettoyage de données !
