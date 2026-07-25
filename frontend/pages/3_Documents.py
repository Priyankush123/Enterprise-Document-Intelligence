import streamlit as st
from requests.exceptions import HTTPError
from utils.helpers import format_size
from components.sidebar import draw_sidebar
from services.api_client import APIClient
from utils.styles import load_css

st.set_page_config(
    page_title="Documents",
    page_icon="📄",
    layout="wide",
)

load_css()
draw_sidebar()

client = APIClient()

st.title("📄 Document Library")

st.caption(
    "Manage all indexed enterprise documents."
)

st.divider()

# Refresh Button
col1, col2 = st.columns([1, 6])

with col1:
    refresh = st.button("🔄 Refresh")

if refresh or "documents" not in st.session_state:
    try:
        st.session_state.documents = client.get_documents()
    except Exception as e:
        st.error(str(e))

documents = st.session_state.get("documents", [])

# Search
search = st.text_input(
    "🔍 Search Documents"
)

if search:
    documents = [
        d
        for d in documents
        if search.lower() in d["filename"].lower()
    ]

st.divider()

if not documents:

    st.info("No indexed documents found.")

else:

    st.write(
        f"**Total Documents:** {len(documents)}"
    )

    st.divider()

# Initialize delete state
if "delete_document_id" not in st.session_state:
    st.session_state.delete_document_id = None

    for document in documents:

        with st.container():

            c1, c2 = st.columns([5, 1])

            with c1:

                st.subheader(
                    f"📄 {document['filename']}"
                )

                st.write(
                    f"**Type:** {document['file_type']}"
                )

                st.write(
                    f"**Pages:** {document['total_pages']}"
                )

                st.write(
                    f"**Chunks:** {document['total_chunks']}"
                )

                st.write(
                    f"**Size:** {format_size(document['file_size'])}"
                )

                st.write(
                    f"**Uploaded:** {document['uploaded_at']}"
                )

            with c2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{document['id']}",
                    type="secondary",
                ):
                    st.session_state.delete_document_id = document["id"]

            # Confirmation dialog
            if st.session_state.delete_document_id == document["id"]:

                st.warning(
                    f"Are you sure you want to delete **{document['filename']}**?"
                )

                confirm_col, cancel_col = st.columns(2)

                with confirm_col:

                    if st.button(
                        "✅ Yes, Delete",
                        key=f"confirm_{document['id']}",
                        type="primary",
                    ):

                        try:

                            client.delete_document(document["id"])

                            st.success("Document deleted successfully.")

                            st.session_state.documents = client.get_documents()

                            st.session_state.delete_document_id = None

                            st.rerun()

                        except Exception as e:

                            st.error(str(e))

                with cancel_col:

                    if st.button(
                        "❌ Cancel",
                        key=f"cancel_{document['id']}",
                    ):

                        st.session_state.delete_document_id = None

                        st.rerun()