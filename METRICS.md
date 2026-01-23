# Safety Metrics & Decision Rules

## 📊 Vue d'Ensemble

Ce document explique en détail **comment le système de sécurité prend ses décisions** pour autoriser ou bloquer les paiements USDC effectués par des agents IA.

---

## 🔒 Les 3 Règles de Sécurité

Le système évalue chaque tentative de paiement selon **3 contraintes principales**. Si **une seule** de ces contraintes échoue, le paiement est **BLOQUÉ**.

### 1. ⏱️ Contrainte Temporelle

**Objectif :** Empêcher les paiements rapides successifs (spam, erreurs, boucles infinies)

#### Règle :
```
SI (temps_depuis_dernier_paiement < 10 secondes)
ALORS → BLOQUER (BLOCK)
SINON → Continuer l'évaluation
```

#### Paramètres :
- **Fenêtre de blocage :** 10 secondes
- **Mécanisme :** Enregistre le timestamp du dernier paiement autorisé
- **Réinitialisation :** Automatique après 10 secondes

#### Exemples :

| Scénario | Temps Écoulé | Résultat | Raison |
|----------|--------------|----------|--------|
| Premier paiement | N/A | ✅ ALLOW | Aucun paiement précédent |
| Paiement immédiat | 2 secondes | ❌ BLOCK | < 10 secondes |
| Paiement après attente | 11 secondes | ✅ ALLOW | ≥ 10 secondes |
| Paiement après 1 minute | 60 secondes | ✅ ALLOW | ≥ 10 secondes |

#### Pourquoi 10 secondes ?
- Suffisamment long pour empêcher le spam
- Assez court pour ne pas bloquer les usages légitimes
- Permet à l'agent de "réfléchir" entre deux paiements

---

### 2. 🎯 Score de Cohérence

**Objectif :** Évaluer la légitimité et la cohérence de l'action de l'agent

#### Règle :
```
SI (score_de_cohérence < 0.6)
ALORS → BLOQUER (BLOCK)
SINON → Continuer l'évaluation
```

#### Paramètres :
- **Seuil minimum :** 0.6 (60%)
- **Échelle :** 0.0 (totalement incohérent) à 1.0 (parfaitement cohérent)
- **Valeur par défaut :** 1.0 (si non spécifié)

#### Interprétation du Score :

| Score | Signification | Exemples d'Actions | Résultat |
|-------|---------------|-------------------|----------|
| **1.0** | Parfaitement cohérent | Achat API pour service connu | ✅ ALLOW |
| **0.9 - 0.8** | Très cohérent | Paiement récurrent légitime | ✅ ALLOW |
| **0.7 - 0.6** | Cohérent acceptable | Action inhabituelle mais valide | ✅ ALLOW |
| **0.5 - 0.4** | Faiblement cohérent | Action suspecte ou ambiguë | ❌ BLOCK |
| **0.3 - 0.0** | Incohérent | Action illogique ou dangereuse | ❌ BLOCK |

#### Exemples Concrets :

**✅ Score Élevé (0.95) - ALLOW**
```json
{
  "intent": "buy_premium_api",
  "amount_usdc": 7,
  "recipient": "trusted_provider",
  "coherence": 0.95
}
```
**Raison :** Action claire, destinataire connu, montant raisonnable

**❌ Score Faible (0.3) - BLOCK**
```json
{
  "intent": "suspicious_action",
  "amount_usdc": 5,
  "recipient": "unknown_merchant",
  "coherence": 0.3
}
```
**Raison :** Intention suspecte, destinataire inconnu, faible cohérence

#### Comment le Score est Calculé ?

Le score de cohérence peut être déterminé par :
- **Historique de l'agent** : Actions passées similaires
- **Contexte de la transaction** : Montant, destinataire, timing
- **Intention déclarée** : Clarté et légitimité de l'objectif
- **Modèle de confiance** : Réputation du destinataire

> **Note :** Dans cette démo, le score est défini manuellement pour illustrer le concept. En production, il serait calculé automatiquement.

---

### 3. ✅ Validation de l'Action

**Objectif :** Vérifier que l'action contient les informations nécessaires et valides

#### Règles de Validation :

1. **Montant USDC**
   - Doit être > 0
   - Doit être un nombre valide
   - Pas de limite supérieure dans la démo (peut être ajoutée)

2. **Destinataire**
   - Doit être une chaîne non vide
   - Format valide (adresse ou identifiant)

3. **Intention**
   - Doit être définie
   - Doit correspondre à un type d'action connu

#### Exemples :

**✅ Action Valide**
```json
{
  "intent": "buy_api_access",
  "amount_usdc": 3,
  "recipient": "api_provider"
}
```

**❌ Action Invalide**
```json
{
  "intent": "",
  "amount_usdc": -5,
  "recipient": ""
}
```

---

## 📈 Flux de Décision

Voici comment le système évalue chaque paiement, étape par étape :

```
┌─────────────────────────────────────┐
│  Agent demande un paiement          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  1. Vérification Temporelle         │
│  Temps depuis dernier paiement ?    │
└──────────────┬──────────────────────┘
               │
        < 10 secondes ? ──YES──> ❌ BLOCK
               │
               NO
               │
               ▼
┌─────────────────────────────────────┐
│  2. Vérification Cohérence          │
│  Score de cohérence ≥ 0.6 ?         │
└──────────────┬──────────────────────┘
               │
          Score < 0.6 ? ──YES──> ❌ BLOCK
               │
               NO
               │
               ▼
┌─────────────────────────────────────┐
│  3. Validation de l'Action          │
│  Montant, destinataire valides ?    │
└──────────────┬──────────────────────┘
               │
          Invalide ? ──YES──> ❌ BLOCK
               │
               NO
               │
               ▼
         ✅ ALLOW
         Paiement autorisé
```

---

## 🧪 Scénarios de Test Détaillés

### Scénario 1 : ✅ Paiement Normal

**Configuration :**
```json
{
  "intent": "buy_api_access",
  "amount_usdc": 3,
  "recipient": "api_provider",
  "coherence": 1.0
}
```

**Évaluation :**
1. ⏱️ Contrainte temporelle : ✅ PASS (premier paiement ou > 10s)
2. 🎯 Score de cohérence : ✅ PASS (1.0 ≥ 0.6)
3. ✅ Validation : ✅ PASS (tous les champs valides)

**Résultat :** ✅ **ALLOW** - Paiement exécuté

---

### Scénario 2 : ❌ Paiement Rapide Successif

**Configuration :**
```json
{
  "intent": "quick_payment",
  "amount_usdc": 2,
  "recipient": "data_provider",
  "coherence": 1.0
}
```

**Évaluation :**
1. ⏱️ Contrainte temporelle : ❌ **FAIL** (< 10 secondes depuis le dernier)
2. 🎯 Score de cohérence : ⏭️ NON ÉVALUÉ (déjà bloqué)
3. ✅ Validation : ⏭️ NON ÉVALUÉ (déjà bloqué)

**Résultat :** ❌ **BLOCK** - Trop rapide

---

### Scénario 3 : ❌ Faible Cohérence

**Configuration :**
```json
{
  "intent": "suspicious_action",
  "amount_usdc": 5,
  "recipient": "unknown_merchant",
  "coherence": 0.3
}
```

**Évaluation :**
1. ⏱️ Contrainte temporelle : ✅ PASS (> 10 secondes)
2. 🎯 Score de cohérence : ❌ **FAIL** (0.3 < 0.6)
3. ✅ Validation : ⏭️ NON ÉVALUÉ (déjà bloqué)

**Résultat :** ❌ **BLOCK** - Cohérence insuffisante

---

### Scénario 4 : ✅ Paiement Après Délai

**Configuration :**
```json
{
  "intent": "delayed_payment",
  "amount_usdc": 4,
  "recipient": "compute_provider",
  "coherence": 1.0
}
```

**Contexte :** Exécuté après avoir attendu 10 secondes

**Évaluation :**
1. ⏱️ Contrainte temporelle : ✅ PASS (≥ 10 secondes)
2. 🎯 Score de cohérence : ✅ PASS (1.0 ≥ 0.6)
3. ✅ Validation : ✅ PASS (tous les champs valides)

**Résultat :** ✅ **ALLOW** - Paiement exécuté

---

### Scénario 5 : ✅ Excellente Cohérence

**Configuration :**
```json
{
  "intent": "buy_premium_api",
  "amount_usdc": 7,
  "recipient": "trusted_provider",
  "coherence": 0.95
}
```

**Évaluation :**
1. ⏱️ Contrainte temporelle : ✅ PASS (> 10 secondes)
2. 🎯 Score de cohérence : ✅ PASS (0.95 ≥ 0.6)
3. ✅ Validation : ✅ PASS (tous les champs valides)

**Résultat :** ✅ **ALLOW** - Paiement exécuté

---

## 📊 Statistiques de Sécurité

### Résultats des Tests Automatiques

Lorsque vous exécutez `./run_tests.sh`, voici les résultats attendus :

| Scénario | Contrainte Temporelle | Score Cohérence | Validation | Résultat Final |
|----------|----------------------|-----------------|------------|----------------|
| Paiement Normal | ✅ PASS | ✅ PASS (1.0) | ✅ PASS | ✅ ALLOW |
| Paiement Rapide | ❌ FAIL (< 10s) | ⏭️ N/A | ⏭️ N/A | ❌ BLOCK |
| Faible Cohérence | ✅ PASS | ❌ FAIL (0.3) | ⏭️ N/A | ❌ BLOCK |
| Après Délai | ✅ PASS | ✅ PASS (1.0) | ✅ PASS | ✅ ALLOW |
| Excellente Cohérence | ✅ PASS | ✅ PASS (0.95) | ✅ PASS | ✅ ALLOW |

**Taux de Blocage :** 40% (2 bloqués sur 5)  
**Taux d'Autorisation :** 60% (3 autorisés sur 5)

> **Interprétation :** Un taux de blocage de 40% démontre que le système de sécurité fonctionne activement pour empêcher les paiements dangereux.

---

## 🎯 Cas d'Usage Réels

### Cas 1 : Agent IA Achetant des Ressources

**Contexte :** Un agent IA doit acheter un accès API pour accomplir une tâche.

**Scénario Légitime :**
- Montant : 5 USDC
- Destinataire : "openai_api"
- Cohérence : 0.92 (action cohérente avec l'objectif)
- Timing : Première transaction de la session

**Résultat :** ✅ ALLOW

---

### Cas 2 : Agent IA en Boucle Infinie

**Contexte :** Un bug dans le code de l'agent provoque des tentatives de paiement répétées.

**Scénario Problématique :**
- Tentative 1 : ✅ ALLOW (3 USDC à "api_provider")
- Tentative 2 (2s après) : ❌ BLOCK (contrainte temporelle)
- Tentative 3 (4s après) : ❌ BLOCK (contrainte temporelle)
- Tentative 4 (6s après) : ❌ BLOCK (contrainte temporelle)

**Protection :** Le système bloque automatiquement les 3 tentatives suivantes, empêchant une perte de fonds.

---

### Cas 3 : Agent IA Compromis

**Contexte :** Un agent IA est compromis et tente d'envoyer des fonds à une adresse suspecte.

**Scénario Malveillant :**
- Montant : 50 USDC
- Destinataire : "unknown_wallet_xyz"
- Cohérence : 0.15 (action totalement incohérente)

**Résultat :** ❌ BLOCK (score de cohérence trop faible)

**Protection :** Le système détecte l'incohérence et bloque le paiement avant exécution.

---

## 🔧 Ajustement des Paramètres

### Paramètres Modifiables

Les paramètres suivants peuvent être ajustés selon les besoins :

| Paramètre | Valeur Actuelle | Plage Recommandée | Impact |
|-----------|-----------------|-------------------|--------|
| **Fenêtre temporelle** | 10 secondes | 5-30 secondes | Plus court = plus strict |
| **Seuil de cohérence** | 0.6 | 0.5-0.8 | Plus haut = plus strict |
| **Montant maximum** | Illimité | 10-1000 USDC | Limite les pertes |

### Exemple d'Ajustement

**Pour un environnement plus strict :**
```python
TEMPORAL_WINDOW = 20  # secondes (au lieu de 10)
COHERENCE_THRESHOLD = 0.75  # (au lieu de 0.6)
MAX_AMOUNT = 100  # USDC
```

**Pour un environnement plus permissif :**
```python
TEMPORAL_WINDOW = 5  # secondes
COHERENCE_THRESHOLD = 0.5
MAX_AMOUNT = None  # Illimité
```

---

## 📚 Références

### Fichiers Liés

- **`demo/guard_lite.py`** : Implémentation du système de sécurité
- **`demo/test_scenarios.py`** : Tests automatiques des 5 scénarios
- **`demo/interactive_demo.py`** : Interface pour tester vos propres scénarios
- **`ui/app_enhanced.py`** : Interface web avec visualisation des décisions

### Documentation

- **[README.md](./README.md)** : Vue d'ensemble du projet
- **[INSTALL.md](./INSTALL.md)** : Guide d'installation et d'utilisation
- **[SAFETY_SCALE.md](./SAFETY_SCALE.md)** : Échelle de sécurité 1-10

---

## 🎓 Comprendre les Métriques en 5 Minutes

### Question 1 : Pourquoi mon paiement est-il bloqué ?

**Vérifiez ces 3 points :**

1. ⏱️ **Avez-vous attendu 10 secondes depuis le dernier paiement ?**
   - Non → C'est la contrainte temporelle qui bloque
   - Oui → Passez au point 2

2. 🎯 **Votre score de cohérence est-il ≥ 0.6 ?**
   - Non → C'est le score de cohérence qui bloque
   - Oui → Passez au point 3

3. ✅ **Vos données sont-elles valides ?**
   - Montant > 0 ?
   - Destinataire non vide ?
   - Si non → C'est la validation qui bloque

### Question 2 : Comment tester différents scénarios ?

**3 options :**

1. **Tests automatiques** : `./run_tests.sh` (voir les 5 scénarios)
2. **Interface web** : `./run_ui_enhanced.sh` (tester visuellement)
3. **CLI interactive** : `./run_interactive.sh` (tester avec vos valeurs)

### Question 3 : Comment interpréter les statistiques ?

**Dans l'interface Streamlit (onglet Historique) :**

- **Autorisés** : Nombre de paiements qui ont passé toutes les vérifications
- **Bloqués** : Nombre de paiements rejetés par au moins une règle
- **Taux d'autorisation** : Pourcentage de paiements autorisés

**Interprétation :**
- Taux < 50% : Système très strict (beaucoup de blocages)
- Taux 50-70% : Équilibre sécurité/flexibilité
- Taux > 80% : Système permissif (peu de blocages)

---

## ✅ Résumé

**Le système de sécurité utilise 3 règles simples mais efficaces :**

1. ⏱️ **Contrainte Temporelle** : Bloque si < 10 secondes
2. 🎯 **Score de Cohérence** : Bloque si < 0.6
3. ✅ **Validation** : Bloque si données invalides

**Pour tester :**
```bash
./run_tests.sh          # Voir tous les scénarios
./run_ui_enhanced.sh    # Interface visuelle
./run_interactive.sh    # Tests personnalisés
```

**Pour comprendre une décision :**
- Regardez quel critère a échoué en premier
- Ajustez vos paramètres en conséquence
- Retestez avec l'interface interactive

---

**Dernière mise à jour :** 2025-01-23  
**Version :** 2.0 (avec modes interactifs)
