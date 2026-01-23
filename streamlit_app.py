import streamlit as st

st.set_page_config(page_title="ObsidiaShell Demo", page_icon="🛡️")

st.title("🛡️ ObsidiaShell — Unified AI Safety & Intelligence")

st.markdown("""
### Welcome to the ObsidiaShell Demonstration
This application serves as the public endpoint for the **ObsidiaShell** project. 
ObsidiaShell unifies **FastGPT**, **Onyx (Danswer)**, and **Graphiti** into a single, secure, and automated intelligence dashboard.

#### 📺 Project Demonstration
The full capabilities of the system, including the automated pipelines and safety protocols, are demonstrated in the video below:
""")

# REMPLACEZ PAR L'URL DE VOTRE VIDÉO (YouTube, Vimeo, etc.)
st.video("https://www.youtube.com/watch?v=votre_id_video" )

st.markdown("""
#### 🚀 Key Features
- **Unified Dashboard**: Single interface for multiple AI agents.
- **Automated Ingestion**: Seamless data processing across 24 domains.
- **Knowledge Graph**: Visual intelligence powered by Graphiti.
- **Semantic Search**: RAG-powered discovery with Onyx.
- **Safety First**: Structural safety principles for agentic workflows.
""")

st.info("Note: This is a demonstration interface. The full backend is hosted on private infrastructure.")
