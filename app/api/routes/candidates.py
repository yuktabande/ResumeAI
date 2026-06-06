from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.candidate import CandidateCreate, CandidateResponse, ResumeUploadResponse
from app.services import candidate_service

router = APIRouter()


class ResumeTextUpdate(BaseModel):
    resume_text: str


@router.post("/candidates", response_model=CandidateResponse, status_code=201)
async def create_candidate(
    candidate_in: CandidateCreate,
    db: Session = Depends(get_db),
):
    return candidate_service.create_candidate(db, candidate_in)


@router.get("/candidates", response_model=list[CandidateResponse])
async def list_candidates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return candidate_service.get_all_candidates(db, skip=skip, limit=limit)


@router.get("/candidates/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
):
    return candidate_service.get_candidate_by_id(db, candidate_id)


@router.post("/candidates/{candidate_id}/resume", response_model=ResumeUploadResponse)
async def upload_resume(
    candidate_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    file_bytes = await file.read()
    candidate = candidate_service.upload_resume(db, candidate_id, file_bytes)

    return ResumeUploadResponse(
        message="Resume uploaded and parsed successfully",
        candidate_id=candidate.id,
        extracted_characters=len(candidate.resume_text or ""),
    )


@router.patch("/candidates/{candidate_id}/resume-text", response_model=CandidateResponse)
async def update_resume_text(
    candidate_id: int,
    update: ResumeTextUpdate,
    db: Session = Depends(get_db),
):
    candidate = candidate_service.get_candidate_by_id(db, candidate_id)
    candidate.resume_text = update.resume_text
    db.commit()
    db.refresh(candidate)
    return candidate