from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    version: str
    message: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    from app.services.matcher import get_model
    get_model()
    return HealthResponse(
        status="ok",
        version="0.1.0",
        message="Resume Intelligence API is running",
    )