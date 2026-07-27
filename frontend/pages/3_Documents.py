import streamlit as st

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
st.caption("Manage all indexed enterprise documents.")

st.divider()

# ----------------------------
# Refresh Documents
# ----------------------------
col1, col2 = st.columns([1, 6])

with col1:
    refresh = st.button("🔄 Refresh")

if refresh or "documents" not in st.session_state:
    try:
        st.session_state.documents = client.get_documents()
    except Exception as e:
        st.error(f"Failed to load documents:\n\n{e}")
        st.stop()

documents = st.session_state.get("documents", [])

# ----------------------------
# Search
# ----------------------------
search = st.text_input(
    "🔍 Search Documents",
    placeholder="Search by filename..."
)

if search:
    documents = [
        doc
        for doc in documents
        if search.lower() in doc["filename"].lower()
    ]

st.divider()

# ----------------------------
# No Documents
# ----------------------------
if not documents:
    st.info("No indexed documents found.")
    st.stop()

st.write(f"### Total Documents: {len(documents)}")
st.divider()

# ----------------------------
# Delete State
# ----------------------------
if "delete_document_id" not in st.session_state:
    st.session_state.delete_document_id = None

# ----------------------------
# Display Documents
# ----------------------------
for document in documents:

    with st.container(border=True):

        col1, col2 = st.columns([5, 1])

        with col1:

            st.subheader(f"📄 {document['filename']}")

            st.write(f"**Type:** {document['file_type']}")
            st.write(f"**Pages:** {document['total_pages']}")
            st.write(f"**Chunks:** {document['total_chunks']}")
            st.write(f"**Size:** {format_size(document['file_size'])}")
            st.write(f"**Uploaded:** {document['uploaded_at']}")

        with col2:

            if st.button(
                "🗑 Delete",
                key=f"delete_{document['id']}",
                type="secondary",
            ):
                st.session_state.delete_document_id = document["id"]

        # ----------------------------
        # Delete Confirmation
        # ----------------------------
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

    st.divider()