import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pathlib import Path
import sys

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from demo.agent import agent_request
from demo.guard_lite import evaluate
from demo.pay_usdc import pay_usdc

st.title("Agentic Commerce — Safe USDC Payment")

amount = st.slider("USDC amount", 1, 10, 3)

if st.button("Agent tries to pay"):
    action = agent_request({"amount": amount, "recipient": "merchant_demo"})
    decision = evaluate(action)

    if decision == "ALLOW":
        pay_usdc(action["amount_usdc"], action["recipient"])
        st.success("Payment allowed and sent")
    else:
        st.error("Payment blocked (unsafe / ambiguous)")
