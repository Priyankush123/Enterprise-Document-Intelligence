import streamlit as st


def show_metrics(stats):

    c1, c2 = st.columns(2)

    c3, c4 = st.columns(2)

    with c1:

        st.metric(
            "📄 Documents",
            stats["total_documents"],
        )

    with c2:

        st.metric(
            "🧩 Chunks",
            stats["total_chunks"],
        )

    with c3:

        st.metric(
            "🧠 Embedding",
            stats["embedding_model"],
        )

    with c4:

        st.metric(
            "🤖 LLM",
            stats["llm_model"],
        )

    st.write("Vector DB:", stats["vector_database"])