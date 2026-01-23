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

## Modes de Démonstration

Ce projet propose **4 modes différents** pour tester le système de sécurité :

### 🎯 Mode 1 : Démo Simple (run_demo.py)

Exécute un scénario de paiement basique prédéfini.

**Linux/Mac :**
```bash
./run_cli.sh
```

**Windows PowerShell :**
```powershell
.\run_cli.ps1
```

**Windows CMD :**
```cmd
set PYTHONPATH=%cd%
python demo/run_demo.py
```

---

### 🧪 Mode 2 : Tests Automatiques (test_scenarios.py)

Exécute automatiquement **5 scénarios de test** pour démontrer le fonctionnement du système de sécurité :

1. ✅ Paiement normal (3 USDC) → AUTORISÉ
2. ❌ Paiement rapide successif (< 10s) → BLOQUÉ
3. ❌ Paiement avec faible cohérence (0.3) → BLOQUÉ
4. ✅ Paiement après délai de sécurité → AUTORISÉ
5. ✅ Paiement avec excellente cohérence (0.95) → AUTORISÉ

**Linux/Mac :**
```bash
./run_tests.sh
```

**Windows PowerShell :**
```powershell
.\run_tests.ps1
```

**Windows CMD :**
```cmd
set PYTHONPATH=%cd%
python demo/test_scenarios.py
```

**Durée :** ~25 secondes (inclut les délais de sécurité)

---

### 🎮 Mode 3 : Démo Interactive CLI (interactive_demo.py)

Mode interactif en ligne de commande où vous pouvez :
- Choisir le montant USDC
- Définir le destinataire
- Ajuster le score de cohérence (0.0 à 1.0)
- Tester plusieurs paiements successifs

**Linux/Mac :**
```bash
./run_interactive.sh
```

**Windows PowerShell :**
```powershell
.\run_interactive.ps1
```

**Windows CMD :**
```cmd
set PYTHONPATH=%cd%
python demo/interactive_demo.py
```

---

### 🌐 Mode 4 : Interface Web Streamlit

#### Version Simple (app.py)

Interface basique avec slider pour le montant.

**Linux/Mac :**
```bash
./run_ui.sh
```

**Windows PowerShell :**
```powershell
.\run_ui.ps1
```

#### Version Améliorée (app_enhanced.py) ⭐ RECOMMANDÉ

Interface complète avec **3 onglets** :

1. **🎮 Mode Interactif**
   - Contrôles personnalisés (montant, destinataire, cohérence)
   - Visualisation des décisions en temps réel

2. **🧪 Tests Automatiques**
   - 5 scénarios prédéfinis cliquables
   - Explication de chaque test

3. **📊 Historique**
   - Tableau de toutes les transactions
   - Statistiques (autorisés/bloqués)
   - Taux d'autorisation

**Linux/Mac :**
```bash
./run_ui_enhanced.sh
```

**Windows PowerShell :**
```powershell
.\run_ui_enhanced.ps1
```

L'interface sera accessible à : `http://localhost:8501`

---

## Comprendre le Système de Sécurité

### Règles de Sécurité

Le système évalue chaque paiement selon **3 critères** :

1. **⏱️ Contrainte Temporelle**
   - Bloque les paiements < 10 secondes après le précédent
   - Objectif : Empêcher le spam et les paiements rapides non intentionnels

2. **🎯 Score de Cohérence**
   - Seuil minimum : **0.6**
   - 1.0 = Action très cohérente et légitime
   - 0.0 = Action suspecte ou incohérente
   - Bloque les actions avec score < 0.6

3. **✅ Validation de l'Action**
   - Vérifie l'intention de l'agent
   - Valide le montant et le destinataire

### Exemples de Scénarios

| Scénario | Montant | Cohérence | Délai | Résultat |
|----------|---------|-----------|-------|----------|
| Paiement API normal | 3 USDC | 1.0 | > 10s | ✅ ALLOW |
| Paiement rapide | 2 USDC | 1.0 | < 10s | ❌ BLOCK |
| Action suspecte | 5 USDC | 0.3 | > 10s | ❌ BLOCK |
| Paiement légitime | 7 USDC | 0.95 | > 10s | ✅ ALLOW |

---

## Configuration (optionnelle)

Pour utiliser une vraie API Arc (au lieu du mode démo simulé), créez un fichier `.env` :

```bash
cp .env.example .env
```

Puis modifiez le fichier `.env` :

```env
ARC_API_KEY=votre_clé_api_ici
ARC_API_URL=https://api.arc.example/pay
```

**Note :** Le mode démo fonctionne sans clé API (paiements simulés).

---

## Résolution des Problèmes

### Erreur "ModuleNotFoundError: No module named 'demo'"

**Cause :** Le `PYTHONPATH` n'est pas configuré correctement.

**Solution :**

1. Utilisez les scripts fournis (`.sh` ou `.ps1`) qui configurent automatiquement le `PYTHONPATH`
2. Ou définissez manuellement :
   - **PowerShell :** `$env:PYTHONPATH = (Get-Location).Path`
   - **CMD :** `set PYTHONPATH=%cd%`
   - **Linux/Mac :** `export PYTHONPATH=$(pwd)`

### Erreur "ARC_API_KEY not set"

**C'est normal !** Le projet fonctionne en **mode démo** par défaut avec des paiements simulés. Vous verrez un avertissement mais la démo continuera.

### Streamlit ne démarre pas

Vérifiez que streamlit est installé :

```bash
pip install streamlit
```

---

## Structure du Projet

```
.
├── demo/
│   ├── __init__.py              # Package Python
│   ├── agent.py                 # Logique de l'agent IA
│   ├── guard_lite.py            # Barrière de sécurité
│   ├── pay_usdc.py              # Module de paiement USDC
│   ├── run_demo.py              # Démo simple
│   ├── test_scenarios.py        # Tests automatiques ⭐
│   └── interactive_demo.py      # Démo interactive CLI ⭐
├── ui/
│   ├── __init__.py              # Package UI
│   ├── app.py                   # Interface Streamlit simple
│   └── app_enhanced.py          # Interface Streamlit améliorée ⭐
├── safety/
│   └── safety_gate.py           # Module de sécurité avancé
├── run_cli.sh / .ps1            # Lancement démo simple
├── run_tests.sh / .ps1          # Lancement tests automatiques ⭐
├── run_interactive.sh / .ps1    # Lancement démo interactive ⭐
├── run_ui.sh / .ps1             # Lancement Streamlit simple
├── run_ui_enhanced.sh / .ps1    # Lancement Streamlit amélioré ⭐
├── requirements.txt             # Dépendances Python
└── README.md                    # Documentation principale
```

⭐ = Nouvelles fonctionnalités

---

## Recommandations

Pour une **démonstration complète** du système :

1. **Commencez par les tests automatiques** pour voir tous les scénarios :
   ```bash
   ./run_tests.sh
   ```

2. **Explorez l'interface Streamlit améliorée** pour une expérience interactive :
   ```bash
   ./run_ui_enhanced.sh
   ```

3. **Testez la démo interactive CLI** pour des expérimentations personnalisées :
   ```bash
   ./run_interactive.sh
   ```

---

## Support

Pour toute question ou problème, consultez le [README.md](./README.md) ou ouvrez une issue sur GitHub.
