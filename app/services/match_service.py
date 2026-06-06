from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.match_result import MatchResult as MatchResultModel
from app.schemas.job_description import MatchResult, BulkMatchResult
from app.services import candidate_service, jd_service
from app.services.matcher import match_resume_to_jd


def save_match_result(
    db: Session,
    candidate_id: int,
    job_description_id: int,
    similarity_score: float,
    match_percentage: int,
    assessment: str,
) -> MatchResultModel:
    match = MatchResultModel(
        candidate_id=candidate_id,
        job_description_id=job_description_id,
        similarity_score=similarity_score,
        match_percentage=match_percentage,
        assessment=assessment,
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def get_match_history_for_candidate(
    db: Session,
    candidate_id: int,
) -> list[MatchResultModel]:
    candidate_service.get_candidate_by_id(db, candidate_id)
    return (
        db.query(MatchResultModel)
        .filter(MatchResultModel.candidate_id == candidate_id)
        .order_by(MatchResultModel.created_at.desc())
        .all()
    )


def match_and_save(
    db: Session,
    candidate_id: int,
    job_description_id: int,
) -> MatchResult:
    candidate = candidate_service.get_candidate_by_id(db, candidate_id)
    jd = jd_service.get_job_description_by_id(db, job_description_id)

    if not candidate.resume_text:
        raise HTTPException(
            status_code=400,
            detail="Candidate has no resume uploaded. Upload a resume before matching."
        )

    result = match_resume_to_jd(candidate.resume_text, jd.description_text)

    save_match_result(
        db=db,
        candidate_id=candidate_id,
        job_description_id=job_description_id,
        **result,
    )

    return MatchResult(
        candidate_id=candidate.id,
        job_description_id=jd.id,
        candidate_name=candidate.name,
        job_title=jd.title,
        company=jd.company,
        **result,
    )


def bulk_match_and_save(
    db: Session,
    candidate_id: int,
    job_description_ids: list[int],
) -> BulkMatchResult:
    candidate = candidate_service.get_candidate_by_id(db, candidate_id)

    if not candidate.resume_text:
        raise HTTPException(
            status_code=400,
            detail="Candidate has no resume uploaded. Upload a resume before matching."
        )

    if len(job_description_ids) > 20:
        raise HTTPException(
            status_code=400,
            detail="Maximum 20 job descriptions per bulk match request."
        )

    results = []
    for jd_id in job_description_ids:
        result = match_and_save(db, candidate_id, jd_id)
        results.append(result)

    results.sort(key=lambda x: x.similarity_score, reverse=True)

    return BulkMatchResult(
        candidate_id=candidate.id,
        candidate_name=candidate.name,
        total_jds_matched=len(results),
        results=results,
    )