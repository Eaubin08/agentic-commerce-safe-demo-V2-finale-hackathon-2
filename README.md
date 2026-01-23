# Agentic Commerce — Safe USDC Payments (Arc)

---

## 🇬🇧 English

### What is this project?

This project is a research and hackathon demo exploring a critical question in agentic commerce:

> **How can AI agents pay in USDC without making unsafe, premature, or incoherent decisions?**

Instead of optimizing how fast an agent can pay, this demo focuses on **when an agent should NOT pay**.

---

### Core idea

In agentic commerce, AI agents may soon autonomously pay for APIs, compute, data, and digital services.  
The primary risk is not technical execution, but **irreversible money movement without sufficient judgment**.

This demo introduces an **opaque safety gate** placed between:

```
Agent intent → Safety Gate → USDC payment
```

- If the action is deemed safe, payment is allowed  
- If the action is unsafe, premature, or ambiguous, payment is blocked (**HOLD**)

---

### What this demo demonstrates

This demo demonstrates that safe agentic payments do not require intelligence or optimization, but **structural constraints**.

Specifically, it shows that:

- Payment decisions can be blocked by design, not by learning  
- Safety can emerge from temporal and coherence constraints, even with simple agents  
- A system can reliably say "NO" without exposing internal decision logic  

The decision logic is intentionally opaque and non-explainable, focusing on observable behavior, not reasoning disclosure.

---

### 🎯 Demo Modes

This project provides **4 different modes** to explore and test the safety system:

#### 1. 🧪 Automated Test Scenarios
Run 5 predefined test scenarios automatically to demonstrate all safety rules.

```bash
./run_tests.sh          # Linux/Mac
.\run_tests.ps1         # Windows PowerShell
```

**Duration:** ~25 seconds | **Scenarios:** 5 automatic tests

#### 2. 🎮 Interactive CLI Demo
Test custom payment scenarios with your own parameters (amount, recipient, coherence score).

```bash
./run_interactive.sh    # Linux/Mac
.\run_interactive.ps1   # Windows PowerShell
```

**Duration:** Variable | **Scenarios:** Unlimited custom tests

#### 3. 🌐 Enhanced Streamlit UI ⭐ Recommended
Professional web interface with 3 tabs:
- **Interactive Mode:** Visual controls for custom tests
- **Automated Tests:** 5 clickable predefined scenarios
- **Transaction History:** Table + statistics (allowed/blocked/rate)

```bash
./run_ui_enhanced.sh    # Linux/Mac
.\run_ui_enhanced.ps1   # Windows PowerShell
```

**URL:** `http://localhost:8501`

#### 4. 📜 Simple Demo
Basic single-scenario demo for quick testing.

```bash
./run_cli.sh            # Linux/Mac
.\run_cli.ps1           # Windows PowerShell
```

---

### 🔒 Safety Rules Demonstrated

The system evaluates each payment using **3 core constraints**:

1. **⏱️ Temporal Constraint**
   - Blocks payments < 10 seconds after the previous one
   - Prevents spam and rapid unintentional payments

2. **🎯 Coherence Score**
   - Minimum threshold: **0.6**
   - Evaluates action legitimacy
   - Blocks suspicious actions with low coherence

3. **✅ Action Validation**
   - Verifies agent intent
   - Validates amount and recipient

**For detailed metrics and examples, see [METRICS.md](./METRICS.md)**

---

### Architecture overview

```
Agent → Safety Gate → Arc USDC Settlement (mocked)
```

- The USDC settlement layer is mocked  
- No real funds are moved  
- The focus is strictly on decision gating, not execution  

---

### What this demo is (and is not)

- ✅ A conceptual safety pattern for agentic commerce  
- ✅ A behavioral proof of safe refusal (HOLD)  
- ✅ Interactive testing environment with multiple modes
- ✅ Complete demonstration of safety constraints
- ❌ Not a production payment system  
- ❌ Not an AI optimization model  
- ❌ Not a disclosed safety algorithm  

---

### Quick Start

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Run automated tests (recommended for first use):**
```bash
./run_tests.sh          # Linux/Mac
.\run_tests.ps1         # Windows PowerShell
```

**3. Launch enhanced web interface:**
```bash
./run_ui_enhanced.sh    # Linux/Mac
.\run_ui_enhanced.ps1   # Windows PowerShell
```

**For complete installation and usage instructions, see [INSTALL.md](./INSTALL.md)**

---

### Demo behavior note

See [SAFETY_SCALE.md](./SAFETY_SCALE.md) for a short explanation of the 1–10 safety scale and why:

- A payment may be allowed in CLI  
- But blocked in the UI  

This is intentional and demonstrates context-sensitive safety gating.

---

### 📊 Example Test Results

```
Scenario                            Result  
----------------------------------------------------------------------
Paiement Normal (3 USDC)            ✅ ALLOW   
Paiement Rapide (< 10s)             ❌ BLOCK   
Faible Cohérence (0.3)              ❌ BLOCK   
Paiement Après Délai                ✅ ALLOW   
Excellente Cohérence (0.95)         ✅ ALLOW   
----------------------------------------------------------------------
Total : 3 allowed, 2 blocked
```

---

### Hackathon context

Designed for the **Arc + Circle Agentic Commerce Hackathon**.

This project intentionally limits disclosure to demonstrate safety outcomes, not internal mechanisms.

---

### 📚 Documentation

- **[INSTALL.md](./INSTALL.md)** - Complete installation and usage guide
- **[METRICS.md](./METRICS.md)** - Detailed explanation of safety metrics and rules
- **[SAFETY_SCALE.md](./SAFETY_SCALE.md)** - Safety scale explanation
- **[DISCLAIMER.md](./DISCLAIMER.md)** - Legal disclaimer

---

### Intellectual Property & Usage Notice

This repository contains a demonstration and conceptual prototype.

Underlying decision logic, structural constraints, and extended safety mechanisms remain proprietary and undisclosed.

Reuse or production deployment requires explicit authorization.

---

---

## 🇫🇷 Français

### De quoi s'agit-il ?

Ce projet est une démo de recherche / hackathon explorant une question centrale de l'agentic commerce :

> **Comment permettre à des agents IA de payer en USDC sans prendre de décisions dangereuses, prématurées ou incohérentes ?**

La démo ne cherche pas à montrer comment payer vite, mais quand il ne faut pas payer.

---

### Idée centrale

Dans l'agentic commerce, les agents IA pourraient bientôt payer de manière autonome des APIs, du calcul, des données ou des services numériques.  
Le risque principal n'est pas technique, mais décisionnel : déplacer de l'argent sans jugement suffisant.

Cette démo introduit une barrière de sécurité opaque entre :

```
Intention de l'agent → Barrière de sécurité → Paiement USDC
```

- Action sûre → paiement autorisé  
- Action dangereuse, prématurée ou ambiguë → blocage (HOLD)

---

### Ce que la démo démontre réellement

Cette démo montre que la sécurité des paiements agentiques ne dépend pas de l'intelligence, mais de la structure.

Elle démontre que :

- Un paiement peut être bloqué par conception, sans apprentissage  
- La sécurité peut émerger de contraintes temporelles et de cohérence  
- Un système peut dire « NON » de manière fiable, sans expliquer sa logique  

La logique décisionnelle est volontairement opaque, afin de se concentrer sur le comportement observable, pas sur l'explication interne.

---

### 🎯 Modes de Démonstration

Ce projet propose **4 modes différents** pour explorer et tester le système de sécurité :

#### 1. 🧪 Tests Automatiques
Exécute 5 scénarios de test prédéfinis automatiquement pour démontrer toutes les règles de sécurité.

```bash
./run_tests.sh          # Linux/Mac
.\run_tests.ps1         # Windows PowerShell
```

**Durée :** ~25 secondes | **Scénarios :** 5 tests automatiques

#### 2. 🎮 Démo Interactive CLI
Testez des scénarios de paiement personnalisés avec vos propres paramètres (montant, destinataire, score de cohérence).

```bash
./run_interactive.sh    # Linux/Mac
.\run_interactive.ps1   # Windows PowerShell
```

**Durée :** Variable | **Scénarios :** Tests personnalisés illimités

#### 3. 🌐 Interface Streamlit Améliorée ⭐ Recommandé
Interface web professionnelle avec 3 onglets :
- **Mode Interactif :** Contrôles visuels pour tests personnalisés
- **Tests Automatiques :** 5 scénarios prédéfinis cliquables
- **Historique des Transactions :** Tableau + statistiques (autorisés/bloqués/taux)

```bash
./run_ui_enhanced.sh    # Linux/Mac
.\run_ui_enhanced.ps1   # Windows PowerShell
```

**URL :** `http://localhost:8501`

#### 4. 📜 Démo Simple
Démo basique à scénario unique pour test rapide.

```bash
./run_cli.sh            # Linux/Mac
.\run_cli.ps1           # Windows PowerShell
```

---

### 🔒 Règles de Sécurité Démontrées

Le système évalue chaque paiement selon **3 contraintes principales** :

1. **⏱️ Contrainte Temporelle**
   - Bloque les paiements < 10 secondes après le précédent
   - Empêche le spam et les paiements rapides non intentionnels

2. **🎯 Score de Cohérence**
   - Seuil minimum : **0.6**
   - Évalue la légitimité de l'action
   - Bloque les actions suspectes avec faible cohérence

3. **✅ Validation de l'Action**
   - Vérifie l'intention de l'agent
   - Valide le montant et le destinataire

**Pour les métriques détaillées et exemples, voir [METRICS.md](./METRICS.md)**

---

### Architecture

```
Agent → Barrière de sécurité → Paiement USDC Arc (simulé)
```

- La couche de paiement est simulée  
- Aucun fonds réel n'est déplacé  
- L'objectif est uniquement la barrière décisionnelle

---

### Ce que cette démo est (et n'est pas)

- ✅ Un prototype conceptuel de sécurité  
- ✅ Une preuve comportementale du HOLD  
- ✅ Environnement de test interactif avec plusieurs modes
- ✅ Démonstration complète des contraintes de sécurité
- ❌ Pas un système de paiement réel  
- ❌ Pas un modèle d'IA optimisé  
- ❌ Pas une divulgation de mécanismes internes

---

### Démarrage Rapide

**1. Installer les dépendances :**
```bash
pip install -r requirements.txt
```

**2. Lancer les tests automatiques (recommandé pour première utilisation) :**
```bash
./run_tests.sh          # Linux/Mac
.\run_tests.ps1         # Windows PowerShell
```

**3. Lancer l'interface web améliorée :**
```bash
./run_ui_enhanced.sh    # Linux/Mac
.\run_ui_enhanced.ps1   # Windows PowerShell
```

**Pour les instructions complètes, voir [INSTALL.md](./INSTALL.md)**

---

### Note sur le comportement

Voir [SAFETY_SCALE.md](./SAFETY_SCALE.md) pour une explication courte (EN/FR) de l'échelle de sécurité (1–10) et pourquoi :

- Un paiement peut passer en CLI  
- Mais être bloqué dans l'UI  

Ce comportement est intentionnel.

---

### 📊 Exemple de Résultats de Tests

```
Scénario                            Résultat  
----------------------------------------------------------------------
Paiement Normal (3 USDC)            ✅ ALLOW   
Paiement Rapide (< 10s)             ❌ BLOCK   
Faible Cohérence (0.3)              ❌ BLOCK   
Paiement Après Délai                ✅ ALLOW   
Excellente Cohérence (0.95)         ✅ ALLOW   
----------------------------------------------------------------------
Total : 3 autorisés, 2 bloqués
```

---

### Contexte hackathon

Projet conçu pour le **Arc + Circle Agentic Commerce Hackathon**.

Le niveau de divulgation est volontairement limité afin de montrer les effets, pas les mécanismes internes.

---

### 📚 Documentation

- **[INSTALL.md](./INSTALL.md)** - Guide complet d'installation et d'utilisation
- **[METRICS.md](./METRICS.md)** - Explication détaillée des métriques et règles de sécurité
- **[SAFETY_SCALE.md](./SAFETY_SCALE.md)** - Explication de l'échelle de sécurité
- **[DISCLAIMER.md](./DISCLAIMER.md)** - Avertissement légal

---

### Propriété intellectuelle & conditions d'usage

Ce dépôt contient une démo conceptuelle.

Les mécanismes avancés, contraintes structurelles et extensions restent propriétaires et non divulgués.

Toute réutilisation ou déploiement en production nécessite une autorisation explicite.
