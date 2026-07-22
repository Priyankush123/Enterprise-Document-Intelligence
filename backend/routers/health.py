from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Enterprise Document Intelligence API"
    }


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }