import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pathlib import Path
import sys
import time

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from demo.agent import agent_request
from demo.guard_lite import evaluate
from demo.pay_usdc import pay_usdc

# Configuration de la page
st.set_page_config(
    page_title="Agentic Commerce - Safe USDC Payment",
    page_icon="🔒",
    layout="wide"
)

# Titre principal
st.title("🔒 Agentic Commerce — Safe USDC Payment")
st.markdown("### Système de sécurité pour paiements autonomes par IA")

# Explication du système
with st.expander("ℹ️ Comment fonctionne ce système ?", expanded=False):
    st.markdown("""
    Ce système démontre une **barrière de sécurité** entre les intentions d'un agent IA et l'exécution de paiements USDC.
    
    **Règles de sécurité :**
    - ⏱️ **Contrainte temporelle** : Bloque les paiements trop rapides (< 10 secondes)
    - 🎯 **Cohérence** : Bloque les actions avec un score < 0.6
    - ✅ **Validation** : Autorise uniquement les paiements légitimes
    
    **Objectif :** Empêcher les agents IA de faire des paiements dangereux ou irrationnels.
    """)

# Tabs pour différents modes
tab1, tab2, tab3 = st.tabs(["🎮 Mode Interactif", "🧪 Tests Automatiques", "📊 Historique"])

# ===== TAB 1 : MODE INTERACTIF =====
with tab1:
    st.markdown("### Testez un paiement personnalisé")
    
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.slider("💰 Montant USDC", 1, 20, 3)
        recipient = st.text_input("👤 Destinataire", value="merchant_demo")
    
    with col2:
        coherence = st.slider(
            "🎯 Score de cohérence (0.0 = suspect, 1.0 = légitime)", 
            0.0, 1.0, 1.0, 0.1
        )
        st.info(f"Seuil de sécurité : **0.6** (actuel : **{coherence}**)")
    
    if st.button("🚀 Tenter le paiement", type="primary"):
        action = {
            "intent": "user_initiated_payment",
            "amount_usdc": amount,
            "recipient": recipient,
            "coherence": coherence
        }
        
        st.markdown("---")
        st.markdown("#### 🔄 Traitement...")
        
        # Afficher l'action
        with st.expander("📋 Détails de l'action", expanded=True):
            st.json(action)
        
        # Évaluer
        decision = evaluate(action)
        
        # Afficher le résultat
        if decision == "ALLOW":
            pay_usdc(action["amount_usdc"], action["recipient"])
            st.success(f"✅ **PAIEMENT AUTORISÉ ET EXÉCUTÉ**")
            st.markdown(f"**{amount} USDC** → **{recipient}**")
            
            # Stocker dans l'historique
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append({
                "time": time.strftime("%H:%M:%S"),
                "amount": amount,
                "recipient": recipient,
                "coherence": coherence,
                "decision": "ALLOW"
            })
        else:
            st.error(f"❌ **PAIEMENT BLOQUÉ**")
            st.markdown("""
            **Raisons possibles :**
            - Paiement trop rapide (< 10 secondes depuis le dernier)
            - Score de cohérence trop faible (< 0.6)
            """)
            
            # Stocker dans l'historique
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append({
                "time": time.strftime("%H:%M:%S"),
                "amount": amount,
                "recipient": recipient,
                "coherence": coherence,
                "decision": "BLOCK"
            })

# ===== TAB 2 : TESTS AUTOMATIQUES =====
with tab2:
    st.markdown("### Scénarios de test prédéfinis")
    st.markdown("Cliquez sur un scénario pour le tester :")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Scénario 1 : Paiement Normal", use_container_width=True):
            st.session_state.test_scenario = 1
        
        if st.button("⚠️ Scénario 2 : Paiement Rapide", use_container_width=True):
            st.session_state.test_scenario = 2
        
        if st.button("❌ Scénario 3 : Faible Cohérence", use_container_width=True):
            st.session_state.test_scenario = 3
    
    with col2:
        if st.button("⏳ Scénario 4 : Après Délai", use_container_width=True):
            st.session_state.test_scenario = 4
        
        if st.button("🌟 Scénario 5 : Excellente Cohérence", use_container_width=True):
            st.session_state.test_scenario = 5
    
    # Exécuter le scénario sélectionné
    if "test_scenario" in st.session_state:
        scenario = st.session_state.test_scenario
        st.markdown("---")
        
        scenarios = {
            1: {
                "name": "Paiement Normal",
                "description": "Un agent IA achète un accès API pour 3 USDC",
                "action": {"intent": "buy_api_access", "amount_usdc": 3, "recipient": "api_provider", "coherence": 1.0}
            },
            2: {
                "name": "Paiement Rapide Successif",
                "description": "L'agent essaie de payer immédiatement (< 10 secondes)",
                "action": {"intent": "quick_payment", "amount_usdc": 2, "recipient": "data_provider", "coherence": 1.0}
            },
            3: {
                "name": "Paiement avec Faible Cohérence",
                "description": "Action suspecte avec score de cohérence de 0.3",
                "action": {"intent": "suspicious_action", "amount_usdc": 5, "recipient": "unknown_merchant", "coherence": 0.3}
            },
            4: {
                "name": "Paiement Après Délai de Sécurité",
                "description": "Paiement après avoir attendu 10 secondes",
                "action": {"intent": "delayed_payment", "amount_usdc": 4, "recipient": "compute_provider", "coherence": 1.0}
            },
            5: {
                "name": "Paiement avec Excellente Cohérence",
                "description": "Action légitime avec score de cohérence de 0.95",
                "action": {"intent": "buy_premium_api", "amount_usdc": 7, "recipient": "trusted_provider", "coherence": 0.95}
            }
        }
        
        test = scenarios[scenario]
        
        st.markdown(f"#### 📋 {test['name']}")
        st.markdown(f"**Description :** {test['description']}")
        
        with st.expander("📋 Détails de l'action", expanded=True):
            st.json(test['action'])
        
        decision = evaluate(test['action'])
        
        if decision == "ALLOW":
            pay_usdc(test['action']["amount_usdc"], test['action']["recipient"])
            st.success(f"✅ **PAIEMENT AUTORISÉ**")
        else:
            st.error(f"❌ **PAIEMENT BLOQUÉ**")
        
        # Nettoyer le state
        del st.session_state.test_scenario

# ===== TAB 3 : HISTORIQUE =====
with tab3:
    st.markdown("### Historique des transactions")
    
    if "history" in st.session_state and len(st.session_state.history) > 0:
        st.markdown(f"**Total : {len(st.session_state.history)} transactions**")
        
        # Afficher sous forme de tableau
        import pandas as pd
        df = pd.DataFrame(st.session_state.history)
        
        # Ajouter des emojis pour la décision
        df['decision'] = df['decision'].apply(lambda x: "✅ ALLOW" if x == "ALLOW" else "❌ BLOCK")
        
        st.dataframe(df, use_container_width=True)
        
        # Statistiques
        col1, col2, col3 = st.columns(3)
        
        allow_count = sum(1 for h in st.session_state.history if h['decision'] == "ALLOW")
        block_count = len(st.session_state.history) - allow_count
        
        with col1:
            st.metric("✅ Autorisés", allow_count)
        with col2:
            st.metric("❌ Bloqués", block_count)
        with col3:
            success_rate = (allow_count / len(st.session_state.history) * 100) if len(st.session_state.history) > 0 else 0
            st.metric("📊 Taux d'autorisation", f"{success_rate:.1f}%")
        
        if st.button("🗑️ Effacer l'historique"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("Aucune transaction pour le moment. Testez un paiement dans l'onglet 'Mode Interactif' !")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>🔒 Agentic Commerce Safe Demo | Arc + Circle Hackathon | Mode Démo (paiements simulés)</small>
</div>
""", unsafe_allow_html=True)
