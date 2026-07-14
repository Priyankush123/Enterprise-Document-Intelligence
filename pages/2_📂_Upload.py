import os
import tempfile

import streamlit as st

from streamlit_app.services.upload_service import UploadService


st.set_page_config(
    page_title="Upload Documents",
    page_icon="📂",
    layout="wide",
)

st.title("📂 Upload Documents")

st.write(
    "Upload one or more documents to build your knowledge base."
)

uploaded_files = st.file_uploader(
    "Choose documents",
    type=["pdf", "docx", "pptx", "xlsx", "png", "jpg", "jpeg"],
    accept_multiple_files=True,
)

if uploaded_files:

    service = UploadService()

    for uploaded_file in uploaded_files:

        st.divider()

        st.subheader(uploaded_file.name)

        progress = st.progress(0)

        status = st.empty()

        def update(message, percent):

            progress.progress(percent)

            status.write(message)

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(uploaded_file.name)[1],
        ) as temp:

            temp.write(uploaded_file.read())

            temp_path = temp.name

        result = service.upload(
            temp_path,
            progress_callback=update,
        )

        os.remove(temp_path)

        progress.progress(100)

        if result.success:

            st.success(result.message)

        elif result.status.name == "SKIPPED":

            st.warning(result.message)

        else:

            st.error(result.message)

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Pages",
            len(result.document.pages)
            if result.document
            else 0,
        )

        col2.metric(
            "Chunks",
            result.total_chunks,
        )

        col3.metric(
            "Processing Time",
            f"{result.processing_time:.2f}s",
        )