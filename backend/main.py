from fastapi import FastAPI
from backend.routers import health, upload, chat, documents
from backend.database import Base, engine
from backend.models.document import Document
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Enterprise Document Intelligence API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(documents.router)