import streamlit as st

from streamlit_app.services.chat_service import ChatService


st.set_page_config(
    page_title="Chat",
    page_icon="💬",
    layout="wide",
)

st.title("💬 Chat with your Documents")

st.write(
    "Ask questions about your indexed documents."
)

# ------------------------------------------
# Session State
# ------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------
# Display Chat History
# ------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ------------------------------------------
# User Input
# ------------------------------------------

question = st.chat_input(
    "Ask something about your documents..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            service = ChatService()

            response, elapsed = service.ask(question)

        st.markdown(response.answer)

        st.caption(
            f"⏱ Response Time: {elapsed:.2f} sec"
        )

        st.markdown("### 📚 Supporting References")

        for i, source in enumerate(response.sources, start=1):

            with st.expander(
                f"[{i}] {source.metadata.document_name} "
                f"(Page {source.metadata.page_number})"
            ):

                st.write(
                    f"**Similarity Score:** {source.score:.4f}"
                )

                st.write(source.text)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.answer,
        }
    )