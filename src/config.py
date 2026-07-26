"""
Application Configuration
"""

# ===========================
# Document Processing
# ===========================

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# ===========================
# Retrieval
# ===========================

# Number of chunks retrieved from ChromaDB
VECTOR_TOP_K = 20

# Number of chunks passed to the LLM after reranking
RERANK_TOP_K = 5

# ===========================
# Embedding Model
# ===========================

EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

# ===========================
# Reranker
# ===========================

RERANKER_MODEL = "BAAI/bge-reranker-base"

# ===========================
# LLM
# ===========================

LLM_MODEL = "qwen2.5:3b"

LLM_TEMPERATURE = 0.2

MAX_TOKENS = 1024