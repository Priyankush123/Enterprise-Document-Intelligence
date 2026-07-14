"""
Library Page

Displays all indexed documents.
"""

import streamlit as st

from src.services.document_service import DocumentService


st.set_page_config(

    page_title="Document Library",

    page_icon="📚",

    layout="wide",
)

st.title("📚 Document Library")

st.write(
    "Manage indexed enterprise documents."
)

service = DocumentService()

documents = service.get_documents()

# ----------------------------------------------------------

if not documents:

    st.info(
        "No indexed documents found."
    )

    st.stop()

# ----------------------------------------------------------

st.subheader(
    f"Indexed Documents ({len(documents)})"
)

for document in documents:

    with st.container():

        col1, col2, col3, col4, col5 = st.columns(
            [4, 1, 1, 1, 1]
        )

        col1.write(
            f"📄 **{document['document_name']}**"
        )

        col2.metric(
            "Type",
            document["file_type"].upper(),
        )

        col3.metric(
            "Pages",
            document["pages"],
        )

        col4.metric(
            "Chunks",
            document["chunks"],
        )

        if col5.button(
            "🗑 Delete",
            key=document["document_name"],
        ):

            service.delete_document(
                document["document_name"]
            )

            st.success(
                f"{document['document_name']} deleted."
            )

            st.rerun()

        st.divider()