"""
Enterprise Document Intelligence Platform

Main Streamlit entry point.
"""

import streamlit as st
from streamlit_app.components.theme import load_css


st.set_page_config(
    page_title="Enterprise Document Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)
load_css()

# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "documents" not in st.session_state:
    st.session_state.documents = []

# ---------------------------------------------------
# Home Screen
# ---------------------------------------------------

st.title("🧠 Enterprise Document Intelligence Platform")

st.markdown(
    """
Welcome to the **Enterprise Document Intelligence Platform**.

This application allows you to:

- 📂 Upload enterprise documents
- 💬 Chat with your documents using RAG
- 📚 Manage indexed documents
- 📊 Monitor retrieval statistics
- ⚙️ Configure retrieval settings

Use the navigation menu in the sidebar to get started.
"""
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("🚀 Features")

    st.markdown(
        """
- PDF, DOCX, PPTX and Image support
- OCR for scanned documents
- Recursive chunking
- BGE embeddings
- ChromaDB vector search
- CrossEncoder reranking
- Local LLM with Ollama
- Source citations
"""
    )

with col2:

    st.subheader("📌 Current Models")

    st.markdown(
        """
**Embedding**

BAAI/bge-base-en-v1.5

**Reranker**

BAAI/bge-reranker-base

**LLM**

Qwen2.5
"""
    )

st.divider()

st.info(
    "Select a page from the sidebar to begin."
)