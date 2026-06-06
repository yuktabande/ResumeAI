from datetime import datetime
from pydantic import BaseModel


class JobDescriptionCreate(BaseModel):
    title: str
    company: str
    description_text: str


class JobDescriptionResponse(BaseModel):
    id: int
    title: str
    company: str
    description_text: str
    created_at: datetime

    model_config = {"from_attributes": True}


class MatchRequest(BaseModel):
    candidate_id: int
    job_description_id: int


class BulkMatchRequest(BaseModel):
    candidate_id: int
    job_description_ids: list[int]


class MatchResult(BaseModel):
    candidate_id: int
    job_description_id: int
    candidate_name: str
    job_title: str
    company: str
    similarity_score: float
    match_percentage: int
    assessment: str


class BulkMatchResult(BaseModel):
    candidate_id: int
    candidate_name: str
    total_jds_matched: int
    results: list[MatchResult]


class MatchHistoryResponse(BaseModel):
    id: int
    candidate_id: int
    job_description_id: int
    similarity_score: float
    match_percentage: int
    assessment: str
    created_at: datetime

    model_config = {"from_attributes": True}