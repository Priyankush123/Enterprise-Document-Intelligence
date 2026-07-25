import streamlit as st


def draw_sidebar():

    with st.sidebar:

        st.title("📚 Enterprise RAG")

        st.divider()

        st.markdown(
            """
### Navigation

🏠 Home

📤 Upload

💬 Chat

📄 Documents

📊 Dashboard
"""
        )

        st.divider()

        st.info(
            "Powered by FastAPI + ChromaDB + Ollama"
        )