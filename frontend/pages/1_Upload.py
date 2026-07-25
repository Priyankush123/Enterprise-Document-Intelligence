import streamlit as st
from requests.exceptions import HTTPError

from components.sidebar import draw_sidebar
from components.cards import success, error, info
from components.loading import spinner
from services.api_client import APIClient
from utils.constants import SUPPORTED_FILES, MAX_FILE_SIZE_MB
from utils.styles import load_css

st.set_page_config(
    page_title="Upload Documents",
    page_icon="📤",
    layout="wide",
)

load_css()
draw_sidebar()

client = APIClient()

st.title("📤 Upload Documents")

st.write(
    """
Upload one or more enterprise documents for indexing into the RAG system.
Supported documents are automatically processed, chunked,
embedded and stored inside ChromaDB.
"""
)

st.divider()

uploaded_files = st.file_uploader(
    "Choose Documents",
    type=SUPPORTED_FILES,
    accept_multiple_files=True,
)

if uploaded_files:

    st.subheader("Selected Files")

    for file in uploaded_files:

        st.write(
            f"📄 **{file.name}** "
            f"({round(file.size/1024/1024,2)} MB)"
        )

st.divider()

if st.button(
    "🚀 Start Upload",
    type="primary",
):

    if not uploaded_files:

        error("Please select at least one document.")

    else:

        progress = st.progress(0)

        status = st.empty()

        results = []

        total = len(uploaded_files)

        for index, uploaded_file in enumerate(uploaded_files):

            status.info(
                f"Uploading {uploaded_file.name}..."
            )

            try:

                with spinner(
                    f"Processing {uploaded_file.name}"
                ):

                    response = client.upload_document(
                        uploaded_file
                    )

                results.append(response)

            except HTTPError as e:

                try:
                    detail = e.response.json()["detail"]
                except Exception:
                    detail = str(e)

                results.append(
                    {
                        "status": "FAILED",
                        "message": detail,
                        "filename": uploaded_file.name,
                    }
                )

            except Exception as e:

                results.append(
                    {
                        "status": "FAILED",
                        "message": str(e),
                        "filename": uploaded_file.name,
                    }
                )

            progress.progress((index + 1) / total)

        status.empty()

        st.success("Upload Completed")

        st.divider()

        st.subheader("Upload Summary")

        for result in results:

            status_value = result.get(
                "status",
                ""
            ).upper()

            if status_value == "SUCCESS":

                success(
                    f"""
**{result['filename']}**

Pages : {result['pages']}

Chunks : {result['chunks']}

Embeddings : {result['embedding_count']}

Processing Time : {result['processing_time']} sec
"""
                )

            elif status_value == "SKIPPED":

                info(
                    f"""
**{result['filename']}**

{result['message']}
"""
                )

            else:

                error(
                    f"""
**{result.get('filename','Unknown')}**

{result.get('message')}
"""
                )