from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate
from app.services.pdf_parser import extract_text_from_pdf, clean_text


def get_candidate_by_email(db: Session, email: str) -> Candidate | None:
    return db.query(Candidate).filter(Candidate.email == email).first()


def get_candidate_by_id(db: Session, candidate_id: int) -> Candidate:
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found")
    return candidate


def get_all_candidates(db: Session, skip: int = 0, limit: int = 100) -> list[Candidate]:
    return db.query(Candidate).offset(skip).limit(limit).all()


def create_candidate(db: Session, candidate_in: CandidateCreate) -> Candidate:
    existing = get_candidate_by_email(db, candidate_in.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Candidate with email {candidate_in.email} already exists"
        )

    candidate = Candidate(
        name=candidate_in.name,
        email=candidate_in.email,
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate


def upload_resume(db: Session, candidate_id: int, file_bytes: bytes) -> Candidate:
    candidate = get_candidate_by_id(db, candidate_id)

    try:
        raw_text = extract_text_from_pdf(file_bytes)
        cleaned = clean_text(raw_text)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    candidate.resume_text = cleaned
    db.commit()
    db.refresh(candidate)
    return candidate