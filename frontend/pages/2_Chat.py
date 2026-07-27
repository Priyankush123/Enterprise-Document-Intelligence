import streamlit as st
from requests.exceptions import HTTPError

from components.chat_message import (
    user_message,
    assistant_message,
)
from components.sidebar import draw_sidebar
from services.api_client import APIClient
from utils.session import initialize_session
from utils.styles import load_css

st.set_page_config(
    page_title="Chat",
    page_icon="💬",
    layout="wide",
)

initialize_session()

load_css()

draw_sidebar()

client = APIClient()

st.title("💬 Chat with your Documents")

st.caption(
    "Ask questions about your indexed documents."
)

st.divider()

# Display previous conversation

for chat in st.session_state.chat_history:

    user_message(chat["question"])

    assistant_message(chat["answer"])

    with st.expander("Sources"):

        for source in chat["sources"]:

            st.write(
                f"📄 {source['document_name']} | "
                f"Page {source['page_number']} | "
                f"Chunk {source['chunk_number']}"
            )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Response Time",
        f"{chat['processing_time']} sec"
    )

    c2.metric(
        "Retrieved Chunks",
        chat["retrieval_count"]
    )

    c3.metric(
        "Model",
        chat["model_name"]
    )

question = st.chat_input(
    "Ask something..."
)

if question:

    user_message(question)

    try:

        with st.spinner("Thinking..."):

            response = client.ask_question(
                question
            )

        assistant_message(
            response["answer"]
        )

        with st.expander(
            "Sources"
        ):

            for source in response["sources"]:

                st.write(
                    f"📄 {source['document_name']} | "
                    f"Page {source['page_number']} | "
                    f"Chunk {source['chunk_number']}"
                )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Response Time",
            f"{response['processing_time']} sec"
        )

        col2.metric(
            "Retrieved Chunks",
            response["retrieval_count"]
        )

        col3.metric(
            "Model",
            response["model_name"]
        )

        st.session_state.chat_history.append(
            response
        )

    except HTTPError as e:

        try:

            st.error(
                e.response.json()["detail"]
            )

        except Exception:

            st.error(str(e))

    except Exception as e:

        st.error(str(e))

st.divider()

col1, col2 = st.columns([1, 1])

with col1:

    if st.button("🗑 Clear Conversation"):

        st.session_state.chat_history = []

        st.rerun()

with col2:

    st.download_button(
        "⬇ Download Chat",
        data="\n\n".join(
            [
                f"Q: {c['question']}\nA: {c['answer']}"
                for c in st.session_state.chat_history
            ]
        ),
        file_name="conversation.txt",
    )