import streamlit as st
from requests.exceptions import HTTPError

from components.sidebar import draw_sidebar
from components.metrics import show_metrics
from services.api_client import APIClient
from utils.styles import load_css

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
)

load_css()
draw_sidebar()

client = APIClient()

st.title("📊 Dashboard")

st.caption(
    "Monitor your Enterprise Document Intelligence Platform."
)

st.divider()

# Refresh button
col1, col2 = st.columns([1, 6])

with col1:

    refresh = st.button("🔄 Refresh")

if refresh or "stats" not in st.session_state:

    try:

        st.session_state.stats = client.get_statistics()

    except HTTPError as e:

        try:

            st.error(
                e.response.json()["detail"]
            )

        except Exception:

            st.error(str(e))

    except Exception as e:

        st.error(str(e))

stats = st.session_state.get("stats", {})

if not stats:

    st.warning("No statistics available.")

    st.stop()

show_metrics(stats)

st.divider()

# System Health
st.subheader("🖥 System Health")

col1, col2, col3 = st.columns(3)

with col1:

    if stats.get("api_status") == "Running":

        st.success("API Running")

    else:

        st.error("API Offline")

with col2:

    if stats.get("database_status") == "Connected":

        st.success("Database Connected")

    else:

        st.error("Database Disconnected")

with col3:

    st.success("Vector Store Connected")

st.divider()

st.subheader("⚙ System Information")

left, right = st.columns(2)

with left:

    st.write(
        "**Embedding Model:**",
        stats["embedding_model"],
    )

    st.write(
        "**LLM Model:**",
        stats["llm_model"],
    )

with right:

    st.write(
        "**Vector Database:**",
        stats["vector_database"],
    )

    st.write(
        "**Indexed Documents:**",
        stats["total_documents"],
    )

st.divider()

st.subheader("📈 Collection Summary")

c1, c2 = st.columns(2)

with c1:

    st.metric(
        "Documents",
        stats["total_documents"],
    )

with c2:

    st.metric(
        "Chunks",
        stats["total_chunks"],
    )

st.divider()

st.info(
    """
The dashboard statistics are fetched directly from the FastAPI backend.
Use the Refresh button whenever new documents are uploaded or removed.
"""
)