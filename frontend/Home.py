import streamlit as st

from components.sidebar import draw_sidebar
from utils.styles import load_css
from utils.session import initialize_session

initialize_session()

load_css()

st.set_page_config(
    page_title="Enterprise RAG",
    page_icon="📚",
    layout="wide",
)

draw_sidebar()

st.title("📚 Enterprise Document Intelligence Platform")

st.write(
    """
A production-ready Retrieval-Augmented Generation (RAG) system for enterprise document intelligence.
"""
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("✨ Features")

    st.markdown("""
- Multi-document upload
- OCR Support
- Semantic Search
- Retrieval-Augmented Generation
- Source Citation
- ChromaDB Vector Database
- Ollama LLM
- FastAPI Backend
""")

with col2:

    st.subheader("🛠 Technology Stack")

    st.markdown("""
- Python
- FastAPI
- Streamlit
- LangChain
- ChromaDB
- SQLAlchemy
- PostgreSQL (planned)
- Docker (planned)
""")

st.divider()

st.info(
    "Use the navigation menu on the left to upload documents, chat with them, manage indexed files, and monitor system statistics."
)