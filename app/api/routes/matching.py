from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.job_description import (
    BulkMatchRequest,
    BulkMatchResult,
    JobDescriptionCreate,
    JobDescriptionResponse,
    MatchHistoryResponse,
    MatchRequest,
    MatchResult,
)
from app.services import jd_service, match_service

router = APIRouter()


@router.post("/job-descriptions", response_model=JobDescriptionResponse, status_code=201)
async def create_job_description(
    jd_in: JobDescriptionCreate,
    db: Session = Depends(get_db),
):
    return jd_service.create_job_description(db, jd_in)


@router.get("/job-descriptions", response_model=list[JobDescriptionResponse])
async def list_job_descriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return jd_service.get_all_job_descriptions(db, skip=skip, limit=limit)


@router.get("/job-descriptions/{jd_id}", response_model=JobDescriptionResponse)
async def get_job_description(
    jd_id: int,
    db: Session = Depends(get_db),
):
    return jd_service.get_job_description_by_id(db, jd_id)


@router.post("/match", response_model=MatchResult)
async def match_candidate_to_jd(
    match_request: MatchRequest,
    db: Session = Depends(get_db),
):
    return match_service.match_and_save(
        db,
        match_request.candidate_id,
        match_request.job_description_id,
    )


@router.post("/match/bulk", response_model=BulkMatchResult)
async def bulk_match_candidate(
    bulk_request: BulkMatchRequest,
    db: Session = Depends(get_db),
):
    return match_service.bulk_match_and_save(
        db,
        bulk_request.candidate_id,
        bulk_request.job_description_ids,
    )


@router.get("/candidates/{candidate_id}/matches", response_model=list[MatchHistoryResponse])
async def get_candidate_match_history(
    candidate_id: int,
    db: Session = Depends(get_db),
):
    return match_service.get_match_history_for_candidate(db, candidate_id)