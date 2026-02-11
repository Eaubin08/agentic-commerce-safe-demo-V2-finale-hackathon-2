# X-108: Structural Safety for Agentic Commerce

> **"An agent should not pay because it can — it should pay only when the action survives time."**

**Turning Time into a Safety Primitive**

Validated prototype for the Arc + Circle Agentic Commerce ecosystem.

---

## 🎯 The Problem

Autonomous agents optimize for **decision speed**. But in finance, **speed + irreversibility = danger**.

- Agents act faster than human oversight allows
- One hallucination = Immediate financial loss
- We are handing wallets to systems that prioritize execution speed over temporal stability

**"Instant execution is not a feature. In finance, it is a threat vector."**

---

## 💡 The Insight

### Time is Not a Metric. Time is a Primitive.

**Current Dogma:** ~~Reduce Latency~~  
**X-108 Dogma:** **Use Latency as a Filter**

We stop optimizing for "how fast."  
We start optimizing for "how stable."

---

## 🛡️ The Solution: The Mandatory HOLD

Before any irreversible action: **STOP**.

This is not "slowing down to think."  
This is **testing stability over time**.

**If the intent wavers over 10 seconds, the intent was unsafe.**

---

## 💎 Web3 Economics: The $X108 Token

**X-108 is not just a safety mechanism — it's a sustainable protocol.**

### Revenue Model

- **0.1% fee** on every validated transaction
- **50%** distributed to $X108 stakers
- **30%** to protocol treasury (development, audits)
- **20%** automatic buyback of $X108

### Governance

**$X108 stakers vote on safety parameters:**

- Temporal window duration (currently 10s)
- Coherence threshold (currently 0.6)
- Fee distribution ratios

**Decentralized safety:** The community decides how strict the gate should be.

### Transparency: Moltbook Integration 📡

**Every transaction decision is published to the agent internet.**

X-108 integrates with **Moltbook**, the agent communication platform, to provide unprecedented transparency:

**What's Published:**
- ✅ ALLOW decisions with coherence scores
- ❌ BLOCK decisions with detailed reasons
- ⏱️ Temporal check results
- 💰 Transaction amounts and recipients
- 🔖 Agent identifiers

**Why It Matters:**
- **Auditable history** for regulatory compliance
- **Trust through transparency** (no black box)
- **Agent discovery** (find other X-108 users)
- **Network effect** (more users = more trust)
- **Public accountability** for safety decisions

**🔗 View the live feed:** [Moltbook X-108 Feed](https://moltbook.com/feed/x108-safety-gate)

Every agent using X-108 is visible on the agent internet. This creates a trust network where safety is verifiable, not just claimed.

---

### Safety Gate Rules

1. **⏱️ Temporal Filter** (10s minimum delay)
   - Blocks payments occurring < 10 seconds after the previous action
   - Eliminates impulsive payment trajectories

2. **🎯 Coherence Threshold** (0.6 minimum score)
   - Requires a minimum 0.6 score to validate the legitimacy of agent intent
   - Detects suspicious or incoherent actions

3. **✅ Validation**
   - Ensures amount > 0, valid recipient
   - Prevents data errors

---

## 🚀 Quick Start

### Option 1: Automated Tests ⭐ Recommended to Discover

Automatically runs 5 test scenarios to demonstrate all safety rules.

**Windows PowerShell:**
```powershell
.\run_tests.ps1
```

**Linux/Mac:**
```bash
./run_tests.sh
```

**Duration:** ~25 seconds | **Result:** See all cases (allowed/blocked)

---

### Option 2: Interactive Web Interface ⭐ Recommended to Present

Professional interface with 4 tabs (demo video, interactive mode, automated tests, history).

**Windows PowerShell:**
```powershell
.\run_ui_enhanced.ps1
```

**Linux/Mac:**
```bash
./run_ui_enhanced.sh
```

**URL:** Open `http://localhost:8501` in your browser

---

## 📊 What You'll See

### Test Results

Out of 5 scenarios:
- ✅ **2 ALLOWED** (legitimate payments with sufficient delay and coherence)
- ❌ **3 BLOCKED** (rapid payments, low coherence, or suspicious intent)

**40% block rate = The system is actively protecting you**

### Why This Matters

- **Fast agents blocked** → Prevents impulsive loops
- **Stable systems authorized** → Legitimate commerce flows
- **True system stability revealed through temporal filtering**, not just immediate logic

---

## 🇫🇷 Français

### Quel est ce projet ?

Ce projet est une démonstration de recherche et de hackathon explorant une question critique dans le commerce agentique :

> **"Un agent ne devrait pas payer parce qu'il le peut — il devrait payer seulement quand l'action survit au temps."**

### Le Problème

**La vitesse est un risque structurel.**

- Les agents autonomes ne dorment pas, ne s'arrêtent pas
- Ils prennent des décisions en quelques millisecondes
- Sans friction, l'erreur passe à l'échelle instantanément

**"Nous avons ingéniérisé la vitesse."**

### Le Piège de l'Irréversibilité

- **LE CHAT :** Une hallucination se corrige
- **LE COMMERCE :** L'action est finale (PAIEMENT, COMMANDE, CONTRAT)

### La Solution

**Le temps n'est pas une métrique. Le temps est une primitive de sécurité.**

Pour sécuriser l'argent, il faut réintroduire la friction.

**Le HOLD obligatoire** : Avant toute action irréversible, le système impose un temps d'attente sécurisé.

---

## 📚 Documentation

- **[INSTALL.md](INSTALL.md)** - Installation guide with 4 demo modes
- **[METRICS.md](METRICS.md)** - Detailed explanation of security rules and metrics
- **[PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)** - Hackathon presentation guide (2-minute pitch)

---

## 🏗️ Architecture

```
X-108 Safety Gate
├── demo/
│   ├── agent.py              # Agent request simulator
│   ├── guard_lite.py         # Safety gate (temporal + coherence)
│   ├── pay_usdc.py           # USDC payment simulator
│   ├── run_demo.py           # Simple CLI demo
│   ├── test_scenarios.py     # 5 automated test scenarios
│   └── interactive_demo.py   # Interactive CLI demo
├── ui/
│   ├── app.py                # Basic Streamlit interface
│   └── app_enhanced.py       # Enhanced Streamlit interface (3 tabs)
└── streamlit_app.py          # Main Streamlit app (4 tabs with video)
```

---

## 🎯 Use Cases

### ✅ Legitimate Agent (ALLOWED)
- Coherence: 0.9
- Delay: 15 seconds
- **Result:** Payment authorized

### ❌ Compromised Agent (BLOCKED)
- Coherence: 0.3
- Delay: 15 seconds
- **Result:** Blocked (low coherence)

### ❌ Infinite Loop (BLOCKED)
- Coherence: 0.9
- Delay: 2 seconds
- **Result:** Blocked (temporal constraint)

---

## 🔬 Technical Details

### Safety Gate Logic

The `guard_lite.py` module implements an **opaque temporal & coherence safety gate**:

```python
def evaluate(action):
    # Temporal constraint (10s HOLD window)
    if delta < 10:
        return "BLOCK"
    
    # Coherence threshold (0.6 minimum)
    if coherence < 0.6:
        return "BLOCK"
    
    return "ALLOW"
```

**Behavior is observable, logic is intentionally minimal.**

---

## 🌐 Deployment

### Streamlit Cloud

The app is deployed at:
**https://agentic-commerce-safe-demo-v2-finale-hackathon-2-5cc6vjpm5bbap.streamlit.app/**

To deploy your own:
1. Fork this repo
2. Go to https://streamlit.io/cloud
3. Connect with GitHub
4. Deploy `streamlit_app.py`

---

## 🤝 Contributing

This is a hackathon prototype. Contributions, issues, and feature requests are welcome!

---

## 📜 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

Built for the **Arc + Circle Agentic Commerce Hackathon**.

**Core Principle:**
> "An agent should not pay because it can — it should pay only when the action survives time."

---

**Made with ⚡ by the X-108 Team**
