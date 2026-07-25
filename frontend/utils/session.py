import streamlit as st


def initialize_session():

    defaults = {
        "chat_history": [],
        "documents": [],
        "stats": {},
        "current_document": None,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value