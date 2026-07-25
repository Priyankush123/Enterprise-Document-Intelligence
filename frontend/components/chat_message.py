import streamlit as st


def user_message(message):

    with st.chat_message("user"):

        st.markdown(message)


def assistant_message(answer):

    with st.chat_message("assistant"):

        st.markdown(answer)