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
├── utils.py              # Fonctions de logique métier (Nettoyage, Calculs)
├── requirements.txt      # Liste des dépendances Python
├── Readme.md             # Documentation du projet
├── LICENSE               # Licence du projet (MIT)
├── .gitignore            # Fichiers à ignorer par Git
├── data/                 # Dossier contenant les fichiers de données
│   └── customers-1000.csv  # Fichier de données exemple
└── myenv/                # Environnement virtuel (non inclus dans le rendu)
```

### 🎯 Objectifs
L'application automatise les tâches suivantes :
1.  **Gestion des valeurs manquantes :** Suppression ou imputation (Moyenne, Médiane, Mode).
2.  **Traitement des doublons :** Identification et suppression.
3.  **Détection des valeurs aberrantes (Outliers) :** Méthode de l'intervalle interquartile (IQR).
4.  **Normalisation des données :** MinMax Scaling ou Standard Scaling (Z-Score).
5.  **Exportation :** Téléchargement du jeu de données propre.

### 🛠 Technologies utilisées
* **Langage :** Python 3.x
* **Interface (Frontend/Backend) :** Streamlit
* **Manipulation de données :** Pandas, NumPy
* **Traitement avancé :** Scikit-learn (pour la normalisation)
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

1. **Charger un fichier** : Cliquez sur "Browse files" dans la barre latérale et sélectionnez votre fichier de données (CSV, Excel, JSON, XML)
2. **Visualiser les données brutes** : Consultez l'onglet "📊 Données Brutes" pour voir les statistiques et un aperçu de vos données
3. **Configurer le traitement** : Dans la barre latérale, choisissez vos options :
   * Valeurs Manquantes (suppression, moyenne, médiane, mode)
   * Suppression des doublons
   * Traitement des valeurs aberrantes (IQR)
   * Normalisation (MinMax ou Z-Score)
4. **Lancer le traitement** : Cliquez sur "LANCER LE TRAITEMENT 🚀"
5. **Consulter les résultats** : L'onglet "⚙️ Traitement & Résultats" affiche une comparaison avant/après
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
# - Normalisation : MinMax (0-1)

# 4. Cliquer sur "LANCER LE TRAITEMENT 🚀"

# 5. Télécharger le fichier nettoyé
# Export → Télécharger le fichier CSV nettoyé
```

---

## 📊 Fonctionnalités détaillées

### 1. Gestion des valeurs manquantes

* **Supprimer les lignes** : Élimine toutes les lignes contenant au moins une valeur manquante
* **Moyenne (Mean)** : Remplace les valeurs manquantes par la moyenne de la colonne (colonnes numériques uniquement)
* **Médiane (Median)** : Remplace par la médiane (moins sensible aux valeurs extrêmes)
* **Mode (Fréquence)** : Remplace par la valeur la plus fréquente (fonctionne sur tous types de données)

### 2. Suppression des doublons

Identifie et supprime automatiquement les lignes dupliquées en conservant la première occurrence.

### 3. Détection des valeurs aberrantes (Outliers)

Utilise la méthode IQR (Interquartile Range) :

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
