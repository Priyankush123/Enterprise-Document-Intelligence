"""
Dashboard
"""

import streamlit as st

from src.services.document_service import DocumentService


st.set_page_config(

    page_title="Dashboard",

    page_icon="📊",

    layout="wide",
)

st.title("📊 Dashboard")

service = DocumentService()

stats = service.get_statistics()

col1, col2 = st.columns(2)

col1.metric(
    "Indexed Documents",
    stats["documents"],
)

col2.metric(
    "Total Chunks",
    stats["chunks"],
)

st.divider()

st.subheader("Current Models")

st.write("Embedding Model")

st.code("BAAI/bge-base-en-v1.5")

st.write("Reranker")

st.code("BAAI/bge-reranker-base")

st.write("LLM")

st.code("Qwen2.5")