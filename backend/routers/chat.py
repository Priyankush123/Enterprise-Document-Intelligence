from fastapi import APIRouter
from backend.schema.chat import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):

    return ChatResponse(
        answer=f"You asked: {request.question}",
        sources=["Sample.pdf"]
    )