# Guide d'Installation et de Lancement

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

### 1. Cloner le repository

```bash
git clone https://github.com/Eaubin08/agentic-commerce-safe-demo-V2-finale-hackathon-2.git
cd agentic-commerce-safe-demo-V2-finale-hackathon-2
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Lancement de la démo

### Option 1 : Interface en ligne de commande (CLI)

**Sur Linux/Mac :**
```bash
./run_cli.sh
```

**Sur Windows :**
```bash
set PYTHONPATH=%cd%
python demo/run_demo.py
```

### Option 2 : Interface web Streamlit

**Sur Linux/Mac :**
```bash
./run_ui.sh
```

**Sur Windows :**
```bash
set PYTHONPATH=%cd%
streamlit run ui/app.py
```

L'interface web sera accessible à l'adresse : `http://localhost:8501`

## Configuration (optionnelle)

Pour utiliser une vraie API Arc (au lieu du mode démo simulé), créez un fichier `.env` à partir de `.env.example` :

```bash
cp .env.example .env
```

Puis modifiez le fichier `.env` pour ajouter votre clé API :

```
ARC_API_KEY=votre_clé_api_ici
ARC_API_URL=https://api.arc.example/pay
```

## Résolution des problèmes

### Erreur "ModuleNotFoundError: No module named 'demo'"

Cette erreur se produit si le `PYTHONPATH` n'est pas configuré correctement. Assurez-vous de :

1. Lancer les scripts depuis le **répertoire racine** du projet
2. Utiliser les scripts `run_cli.sh` ou `run_ui.sh` qui configurent automatiquement le `PYTHONPATH`
3. Ou définir manuellement le `PYTHONPATH` :
   - Linux/Mac : `export PYTHONPATH=$(pwd)`
   - Windows : `set PYTHONPATH=%cd%`

### Erreur "ARC_API_KEY not set"

C'est normal ! Le projet fonctionne en **mode démo** par défaut. Vous verrez un avertissement mais la démo continuera à fonctionner avec des paiements simulés.

## Structure du projet

```
.
├── demo/
│   ├── __init__.py          # Fichier d'initialisation du package
│   ├── agent.py             # Logique de l'agent
│   ├── guard_lite.py        # Barrière de sécurité
│   ├── pay_usdc.py          # Module de paiement USDC
│   └── run_demo.py          # Script CLI principal
├── ui/
│   ├── __init__.py          # Fichier d'initialisation du package UI
│   └── app.py               # Interface Streamlit
├── safety/
│   └── safety_gate.py       # Module de sécurité avancé
├── run_cli.sh               # Script de lancement CLI
├── run_ui.sh                # Script de lancement UI
├── requirements.txt         # Dépendances Python
└── README.md                # Documentation principale
```
