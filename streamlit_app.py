"""
X-108 Safety Gate Demo - Streamlit Application
Agentic Commerce: Securing Autonomous Payments
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from demo.agent import agent_request
from demo.guard_lite import evaluate
from demo.pay_usdc import pay_usdc
import time
import pandas as pd

# Web3 and Moltbook integration (optional layers)
try:
    from web3_integration.x108_token_layer import create_token_layer
    from web3_integration.moltbook_integration import create_moltbook_integration
    token_layer = create_token_layer()
    moltbook = create_moltbook_integration()
    WEB3_ENABLED = True
except ImportError:
    WEB3_ENABLED = False
    print("Warning: Web3 layers not available. Running in core mode only.")

# Page configuration
st.set_page_config(
    page_title="X-108 Safety Gate Demo",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .danger-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'transaction_history' not in st.session_state:
    st.session_state.transaction_history = []
if 'last_payment_time' not in st.session_state:
    st.session_state.last_payment_time = None

# Header
st.markdown('<div class="main-header">🔒 X-108: Structural Safety for Agentic Commerce</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Turning Time into a Safety Primitive</div>', unsafe_allow_html=True)

# Signature Quote
st.markdown("""
<div style="text-align: center; font-size: 1.1rem; font-style: italic; color: #ff6b35; margin: 1.5rem 0; padding: 1rem; background-color: #fff5f2; border-left: 4px solid #ff6b35;">
    “An agent should not pay because it can — it should pay only when the action survives time.”
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📚 About X-108")
    st.markdown("""
    **X-108** is a structural safety primitive for agentic commerce.
    
    **The Problem:**
    > “Instant execution is not a feature. In finance, it is a threat vector.”
    
    Agents act faster than human oversight allows. One hallucination = immediate financial loss.
    
    **The Solution: The Mandatory HOLD**
    
    Before any irreversible action: **STOP**.
    
    This is not “slowing down to think.”  
    This is **testing stability over time**.
    
    **Safety Rules:**
    - ⏱️ **Temporal Filter** (10s HOLD): Blocks rapid payments
    - 🎯 **Coherence Threshold** (0.6 min): Validates intent legitimacy
    - ✅ **Validation**: Ensures data integrity
    
    **If the intent wavers over 10 seconds, the intent was unsafe.**
    
    ---
    
    **📡 Public Transparency:**
    
    Every transaction is published to [Moltbook](https://moltbook.com/feed/x108-safety-gate) for full transparency.
    """)
    
    st.divider()
    
    st.header("📊 Statistics")
    if st.session_state.transaction_history:
        total = len(st.session_state.transaction_history)
        allowed = sum(1 for t in st.session_state.transaction_history if t['decision'] == 'ALLOW')
        blocked = total - allowed
        st.metric("Total Transactions", total)
        st.metric("✅ Allowed", allowed)
        st.metric("❌ Blocked", blocked)
        if total > 0:
            st.metric("Block Rate", f"{(blocked/total)*100:.1f}%")
    else:
        st.info("No transactions yet")

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎬 Demo Video", "🎮 Interactive Mode", "🧪 Automated Tests", "📊 Transaction History", "💎 Token Economics"])

# Tab 1: Demo Video
with tab1:
    st.header("🎬 Demo Video")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🇬🇧 English Version")
        if os.path.exists("assets/Building_Trust_in_AI.mp4"):
            st.video("assets/Building_Trust_in_AI.mp4")
        else:
            st.info("Video file not found. Please ensure 'Building_Trust_in_AI.mp4' is in the assets folder.")
    
    with col2:
        st.subheader("🇫🇷 Version Française")
        if os.path.exists("assets/Structurer_la_Confiance.mp4"):
            st.video("assets/Structurer_la_Confiance.mp4")
        else:
            st.info("Video file not found. Please ensure 'Structurer_la_Confiance.mp4' is in the assets folder.")
    
    st.divider()
    
    st.header("📊 Visual Explanations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🇬🇧 Safety Gate Mechanism")
        if os.path.exists("assets/safety_gate_en.png"):
            st.image("assets/safety_gate_en.png", use_container_width=True)
    
    with col2:
        st.subheader("🇫🇷 Mécanisme de Filtrage")
        if os.path.exists("assets/safety_gate_fr.png"):
            st.image("assets/safety_gate_fr.png", use_container_width=True)

# Tab 2: Interactive Mode
with tab2:
    st.header("🎮 Interactive Payment Test")
    st.markdown("Test custom payment scenarios with your own parameters.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Payment Parameters")
        amount = st.slider("💰 Amount (USDC)", min_value=1, max_value=100, value=5, step=1)
        recipient = st.text_input("👤 Recipient", value="api_provider")
        coherence = st.slider("🎯 Coherence Score", min_value=0.0, max_value=1.0, value=0.8, step=0.05)
        intent = st.selectbox("📋 Intent", ["buy_api_access", "buy_premium_api", "subscribe_service", "pay_invoice"])
    
    with col2:
        st.subheader("Safety Information")
        st.info(f"""
        **Current Parameters:**
        - Amount: {amount} USDC
        - Recipient: {recipient}
        - Coherence: {coherence}
        - Intent: {intent}
        
        **Safety Thresholds:**
        - Minimum coherence: 0.6
        - Temporal window: 10 seconds
        """)
    
    if st.button("🚀 Execute Payment", type="primary", use_container_width=True):
        with st.spinner("Evaluating payment request..."):
            # Create action
            action = {
                'intent': intent,
                'amount_usdc': amount,
                'recipient': recipient,
                'coherence': coherence
            }
            
            # Get current time
            now = time.time()
            
            # Evaluate with safety gate
            decision_result = evaluate(action)
            
            # Display result
            st.divider()
            
            if decision_result == 'ALLOW':
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success(f"✅ **PAYMENT ALLOWED**")
                st.markdown(f"**Reason:** Payment passed all safety checks")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Execute payment
                result = pay_usdc(amount, recipient)
                st.info(f"💳 {result}")
                
                # Update last payment time
                st.session_state.last_payment_time = now
            else:
                st.markdown('<div class="danger-box">', unsafe_allow_html=True)
                st.error(f"❌ **PAYMENT BLOCKED**")
                st.markdown(f"**Reason:** Safety gate blocked this payment")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Add to history
            st.session_state.transaction_history.append({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'amount': amount,
                'recipient': recipient,
                'coherence': coherence,
                'intent': intent,
                'decision': decision_result,
                'reason': 'Passed safety checks' if decision_result == 'ALLOW' else 'Blocked by safety gate'
            })

# Tab 3: Automated Tests
with tab3:
    st.header("🧪 Automated Test Scenarios")
    st.markdown("Run predefined scenarios to demonstrate all safety rules.")
    
    scenarios = [
        {
            'name': "✅ Normal Payment",
            'description': "Legitimate payment with good coherence (3 USDC)",
            'action': {'intent': 'buy_api_access', 'amount_usdc': 3, 'recipient': 'api_provider', 'coherence': 0.8},
            'delay': 0
        },
        {
            'name': "❌ Rapid Payment",
            'description': "Payment too soon after previous one (< 10s)",
            'action': {'intent': 'buy_api_access', 'amount_usdc': 2, 'recipient': 'api_provider', 'coherence': 0.75},
            'delay': 2
        },
        {
            'name': "❌ Low Coherence",
            'description': "Suspicious action with coherence score of 0.3",
            'action': {'intent': 'unknown_action', 'amount_usdc': 10, 'recipient': 'unknown', 'coherence': 0.3},
            'delay': 12
        },
        {
            'name': "✅ Payment After Delay",
            'description': "Valid payment after respecting temporal constraint",
            'action': {'intent': 'subscribe_service', 'amount_usdc': 5, 'recipient': 'service_provider', 'coherence': 0.85},
            'delay': 12
        },
        {
            'name': "✅ Excellent Coherence",
            'description': "High-confidence action with coherence of 0.95",
            'action': {'intent': 'buy_premium_api', 'amount_usdc': 7, 'recipient': 'trusted_provider', 'coherence': 0.95},
            'delay': 12
        }
    ]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("▶️ Run All Scenarios", type="primary", use_container_width=True):
            st.session_state.last_payment_time = None  # Reset
            results = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, scenario in enumerate(scenarios):
                status_text.text(f"Running: {scenario['name']}")
                
                # Apply delay
                if scenario['delay'] > 0 and st.session_state.last_payment_time:
                    time.sleep(scenario['delay'])
                
                # Evaluate
                now = time.time()
                decision_result = evaluate(scenario['action'])
                
                # Update last payment time if allowed
                if decision_result == 'ALLOW':
                    st.session_state.last_payment_time = now
                
                results.append({
                    'Scenario': scenario['name'],
                    'Result': '✅ ALLOW' if decision_result == 'ALLOW' else '❌ BLOCK',
                    'Reason': 'Passed safety checks' if decision_result == 'ALLOW' else 'Blocked by safety gate'
                })
                
                # Add to history
                st.session_state.transaction_history.append({
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'amount': scenario['action']['amount_usdc'],
                    'recipient': scenario['action']['recipient'],
                    'coherence': scenario['action']['coherence'],
                    'intent': scenario['action']['intent'],
                    'decision': decision_result,
                    'reason': 'Passed safety checks' if decision_result == 'ALLOW' else 'Blocked by safety gate'
                })
                
                progress_bar.progress((i + 1) / len(scenarios))
            
            status_text.text("✅ All scenarios completed!")
            
            # Display results
            st.divider()
            st.subheader("📊 Test Results")
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
            
            # Summary
            allowed = sum(1 for r in results if '✅' in r['Result'])
            blocked = len(results) - allowed
            
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Total Tests", len(results))
            col_b.metric("✅ Allowed", allowed)
            col_c.metric("❌ Blocked", blocked)
    
    with col2:
        st.info("""
        **Test Duration:**
        ~30 seconds
        
        **Expected Results:**
        - 2-3 allowed
        - 2-3 blocked
        
        **Demonstrates:**
        - Temporal filtering
        - Coherence threshold
        - Action validation
        """)
    
    st.divider()
    
    st.subheader("Individual Scenarios")
    for i, scenario in enumerate(scenarios):
        with st.expander(scenario['name']):
            st.markdown(f"**Description:** {scenario['description']}")
            st.json(scenario['action'])
            if st.button(f"Run this scenario", key=f"scenario_{i}"):
                # Apply delay if needed
                if scenario['delay'] > 0 and st.session_state.last_payment_time:
                    with st.spinner(f"Waiting {scenario['delay']}s..."):
                        time.sleep(scenario['delay'])
                
                # Evaluate
                now = time.time()
                decision_result = evaluate(scenario['action'])
                
                # Display result
                if decision_result == 'ALLOW':
                    st.success(f"✅ ALLOW: Passed safety checks")
                    st.session_state.last_payment_time = now
                else:
                    st.error(f"❌ BLOCK: Blocked by safety gate")
                
                # Add to history
                st.session_state.transaction_history.append({
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'amount': scenario['action']['amount_usdc'],
                    'recipient': scenario['action']['recipient'],
                    'coherence': scenario['action']['coherence'],
                    'intent': scenario['action']['intent'],
                    'decision': decision_result,
                    'reason': 'Passed safety checks' if decision_result == 'ALLOW' else 'Blocked by safety gate'
                })

# Tab 4: Transaction History
with tab4:
    st.header("📊 Transaction History")
    
    if st.session_state.transaction_history:
        # Create DataFrame
        df = pd.DataFrame(st.session_state.transaction_history)
        
        # Display statistics
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(df)
        allowed = len(df[df['decision'] == 'ALLOW'])
        blocked = total - allowed
        
        col1.metric("Total Transactions", total)
        col2.metric("✅ Allowed", allowed)
        col3.metric("❌ Blocked", blocked)
        col4.metric("Block Rate", f"{(blocked/total)*100:.1f}%")
        
        st.divider()
        
        # Display table
        st.subheader("Transaction Log")
        st.dataframe(df, use_container_width=True)
        
        # Clear history button
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.transaction_history = []
            st.session_state.last_payment_time = None
            st.rerun()
    else:
        st.info("No transactions yet. Try the Interactive Mode or run Automated Tests!")

# Tab 5: Token Economics
with tab5:
    st.header("💎 X-108 Token Economics")
    
    st.markdown("""
    The **$X108 token** powers the governance and economics of the X-108 Safety Gate.
    
    **Revenue Model:**
    - Every validated transaction → 0.1% fee
    - 50% distributed to $X108 stakers
    - 30% to treasury for development
    - 20% automatic buyback of $X108
    """)
    
    st.divider()
    
    # Metrics
    st.subheader("📊 Key Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Transactions", "1,247")
        st.metric("Total Fees Collected", "12.47 USDC")
    
    with col2:
        st.metric("$X108 Stakers", "89")
        st.metric("APY for Stakers", "14.3%")
    
    with col3:
        st.metric("$X108 Price", "$0.23")
        st.metric("Market Cap", "$2.3M")
    
    st.divider()
    
    # Governance
    st.subheader("⚙️ Governance Parameters")
    
    st.markdown("""
    **$X108 stakers can vote to adjust safety parameters:**
    
    These parameters directly control the behavior of the Safety Gate.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_temporal = st.slider(
            "Temporal Window (seconds)",
            min_value=5,
            max_value=30,
            value=10,
            help="Minimum delay between payments. Lower = faster but riskier."
        )
    
    with col2:
        new_coherence = st.slider(
            "Coherence Threshold",
            min_value=0.3,
            max_value=0.9,
            value=0.6,
            step=0.05,
            help="Minimum coherence score to validate intent. Higher = stricter."
        )
    
    if st.button("🗳️ Submit Governance Vote", type="primary"):
        st.success("✅ Vote recorded on-chain! (Demo mode)")
        st.info(f"📊 Proposed changes:\n- Temporal Window: {new_temporal}s\n- Coherence Threshold: {new_coherence}")
    
    st.divider()
    
    # Fee Distribution
    st.subheader("💰 Fee Distribution")
    
    st.markdown("""
    **How transaction fees are distributed:**
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🏆 Stakers (50%)**
        
        Distributed proportionally to all $X108 stakers based on their stake.
        """)
    
    with col2:
        st.markdown("""
        **🏛️ Treasury (30%)**
        
        Used for protocol development, security audits, and ecosystem growth.
        """)
    
    with col3:
        st.markdown("""
        **🔄 Buyback (20%)**
        
        Automatic buyback of $X108 tokens to support price stability.
        """)
    
    st.divider()
    
    # Moltbook Integration
    st.subheader("📡 Moltbook Integration: Public Transparency")
    
    st.markdown("""
    **Every transaction decision is published to the agent internet.**
    
    X-108 integrates with **Moltbook** to provide full transparency on Safety Gate behavior.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📊 What's Published:**
        
        - ✅ ALLOW decisions with coherence score
        - ❌ BLOCK decisions with reason
        - ⏱️ Temporal check results
        - 💰 Transaction amounts
        - 🔖 Agent identifiers
        """)
    
    with col2:
        st.markdown("""
        **🎯 Why It Matters:**
        
        - **Auditable history** for compliance
        - **Trust through transparency**
        - **Agent discovery** (find X-108 users)
        - **Public accountability**
        - **No black box**
        """)
    
    st.markdown("""
    🔗 **View the live feed:** [Moltbook X-108 Feed](https://moltbook.com/feed/x108-safety-gate)
    
    Every agent using X-108 is visible on the agent internet. This creates a network effect:
    the more agents use X-108, the more trust is built in the ecosystem.
    """)
    
    if WEB3_ENABLED:
        try:
            stats = moltbook.get_stats()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Posts", stats.get('total_posts', 0))
            with col2:
                st.metric("Allowed", stats.get('allowed_posts', 0))
            with col3:
                st.metric("Blocked", stats.get('blocked_posts', 0))
        except:
            st.info("🚧 Moltbook stats will be available when connected to the live feed.")
    else:
        st.info("🚧 Moltbook integration is in demo mode. Connect to see live stats.")
    
    st.divider()
    
    # Smart Contract Info
    st.subheader("🔗 Smart Contract")
    
    st.markdown("""
    **Contract Address:** `0x0000...0000` (Demo mode)
    
    **Network:** Base (Ethereum L2)
    
    **Audit Status:** ⚠️ Not audited (Hackathon prototype)
    
    **Source Code:** Available in `contracts/X108Token.sol`
    """)
    
    st.info("""
    🚧 **Note:** This is a hackathon prototype. The token economics are designed for demonstration purposes.
    In production, the smart contract would be audited and deployed on mainnet.
    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p><strong>X-108 Safety Gate Demo</strong> | Arc + Circle Agentic Commerce Hackathon</p>
    <p>"An agent should not pay because it can — it should pay only when the action survives time."</p>
</div>
""", unsafe_allow_html=True)
