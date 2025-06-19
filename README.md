# Option Pricing and Greeks Calculator

Ce projet est une application interactive construite avec Streamlit pour calculer les prix des options (modèle Black-Scholes) et leurs Grecs associés.

**➡️ Accéder à l'application en direct ici : [Mon Outil de Calcul d'Options](https://option-pricing-and-greeks-calculator-ffwsqnmhpy93pyrmbjbgeo.streamlit.app/)**

---

## Installation et Utilisation Locale (pour les développeurs)
Si vous souhaitez exécuter cette application localement :

1. Clonez ce dépôt :
   ```bash
   git clone [https://github.com/Primo09-bingo/option-pricing-and-greeks-calculator.git](https://github.com/Primo09-bingo/option-pricing-and-greeks-calculator.git)
# Calculateur d'Options Black-Scholes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Une application web interactive pour calculer les prix des options et les grecques en utilisant le modèle Black-Scholes.

## Fonctionnalités

- Calcul des prix des options d'achat (call) et de vente (put)
- Affichage des grecques : Delta, Gamma, Theta, Vega, Rho
- Visualisation interactive des sensibilités
- Interface utilisateur intuitive avec Streamlit
- Graphiques interactifs avec Plotly

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/option-pricing-calculator.git
   cd option-pricing-calculator
   ```

2. Créez un environnement virtuel (recommandé) :
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Sur Windows
   # OU
   source venv/bin/activate  # Sur macOS/Linux
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

Lancez l'application avec la commande :
```bash
streamlit run options_calculator.py
```

L'application s'ouvrira automatiquement dans votre navigateur par défaut à l'adresse `http://localhost:8501`.

## Fonctionnalités de l'interface

- **Paramètres de l'option** (dans la barre latérale) :
  - Prix du sous-jacent (S)
  - Prix d'exercice (K)
  - Temps à expiration (années)
  - Taux sans risque (%)
  - Volatilité (%)
  - Type d'option (Call/Put)

- **Onglets principaux** :
  1. **Calculateur** : Prix de l'option, valeur intrinsèque et valeur temps
  2. **Greeks** : Analyse détaillée des grecques
  3. **Sensibilité** : Graphiques interactifs de sensibilité
  4. **Stratégies** : Analyse de stratégies d'options

## Captures d'écran

[Insérez ici des captures d'écran de votre application]

## Structure du projet

```
option-pricing-calculator/
├── options_calculator.py     # Application principale
├── requirements.txt          # Dépendances
├── README.md                 # Ce fichier
└── .gitignore               # Fichiers à ignorer par Git
```

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteur

Laabidate Akram 

## Remerciements

- Modèle Black-Scholes
- Bibliothèques Python : Streamlit, Plotly, NumPy, SciPy
