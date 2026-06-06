from datetime import datetime
from pydantic import BaseModel, EmailStr


class CandidateCreate(BaseModel):
    name: str
    email: str


class CandidateResponse(BaseModel):
    id: int
    name: str
    email: str
    resume_text: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ResumeUploadResponse(BaseModel):
    message: str
    candidate_id: int
    extracted_characters: int