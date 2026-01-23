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
st.markdown('<div class="main-header">🔒 X-108 Safety Gate Demo</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Agentic Commerce: Securing Autonomous USDC Payments</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📚 About X-108")
    st.markdown("""
    **X-108** is a temporal safety middleware that prevents unsafe, premature, 
    or incoherent autonomous payments by AI agents.
    
    **Core Principle:**
    > "Coherence is not decided. It survives time."
    
    **Safety Rules:**
    - ⏱️ **Temporal Constraint**: Block payments < 10s apart
    - 🎯 **Coherence Threshold**: Minimum score of 0.6
    - ✅ **Action Validation**: Verify intent and parameters
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
tab1, tab2, tab3, tab4 = st.tabs(["🎬 Demo Video", "🎮 Interactive Mode", "🧪 Automated Tests", "📊 Transaction History"])

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
            decision = evaluate(
                action=action,
                now_ts=now,
                last_signal_ts=st.session_state.last_payment_time
            )
            
            # Display result
            st.divider()
            
            if decision['action'] == 'ALLOW':
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success(f"✅ **PAYMENT ALLOWED**")
                st.markdown(f"**Reason:** {decision['reason']}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Execute payment
                result = pay_usdc(amount, recipient)
                st.info(f"💳 {result}")
                
                # Update last payment time
                st.session_state.last_payment_time = now
            else:
                st.markdown('<div class="danger-box">', unsafe_allow_html=True)
                st.error(f"❌ **PAYMENT BLOCKED**")
                st.markdown(f"**Reason:** {decision['reason']}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Add to history
            st.session_state.transaction_history.append({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'amount': amount,
                'recipient': recipient,
                'coherence': coherence,
                'intent': intent,
                'decision': decision['action'],
                'reason': decision['reason']
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
                decision = evaluate(
                    action=scenario['action'],
                    now_ts=now,
                    last_signal_ts=st.session_state.last_payment_time
                )
                
                # Update last payment time if allowed
                if decision['action'] == 'ALLOW':
                    st.session_state.last_payment_time = now
                
                results.append({
                    'Scenario': scenario['name'],
                    'Result': '✅ ALLOW' if decision['action'] == 'ALLOW' else '❌ BLOCK',
                    'Reason': decision['reason']
                })
                
                # Add to history
                st.session_state.transaction_history.append({
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'amount': scenario['action']['amount_usdc'],
                    'recipient': scenario['action']['recipient'],
                    'coherence': scenario['action']['coherence'],
                    'intent': scenario['action']['intent'],
                    'decision': decision['action'],
                    'reason': decision['reason']
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
                decision = evaluate(
                    action=scenario['action'],
                    now_ts=now,
                    last_signal_ts=st.session_state.last_payment_time
                )
                
                # Display result
                if decision['action'] == 'ALLOW':
                    st.success(f"✅ ALLOW: {decision['reason']}")
                    st.session_state.last_payment_time = now
                else:
                    st.error(f"❌ BLOCK: {decision['reason']}")
                
                # Add to history
                st.session_state.transaction_history.append({
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'amount': scenario['action']['amount_usdc'],
                    'recipient': scenario['action']['recipient'],
                    'coherence': scenario['action']['coherence'],
                    'intent': scenario['action']['intent'],
                    'decision': decision['action'],
                    'reason': decision['reason']
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

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p><strong>X-108 Safety Gate Demo</strong> | Arc + Circle Agentic Commerce Hackathon</p>
    <p>Coherence is not decided. It survives time.</p>
</div>
""", unsafe_allow_html=True)
