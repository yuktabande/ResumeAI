from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.job_description import JobDescription
from app.schemas.job_description import JobDescriptionCreate


def create_job_description(db: Session, jd_in: JobDescriptionCreate) -> JobDescription:
    jd = JobDescription(
        title=jd_in.title,
        company=jd_in.company,
        description_text=jd_in.description_text,
    )
    db.add(jd)
    db.commit()
    db.refresh(jd)
    return jd


def get_job_description_by_id(db: Session, jd_id: int) -> JobDescription:
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not jd:
        raise HTTPException(status_code=404, detail=f"Job description {jd_id} not found")
    return jd


def get_all_job_descriptions(db: Session, skip: int = 0, limit: int = 100) -> list[JobDescription]:
    return db.query(JobDescription).offset(skip).limit(limit).all()