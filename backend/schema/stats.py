from pydantic import BaseModel


class StatsResponse(BaseModel):
    total_documents: int
    total_chunks: int
    embedding_model: str
    llm_model: str
    vector_database: str
    api_status: str
    database_status: str