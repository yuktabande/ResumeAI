import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def candidate_with_resume(client: TestClient):
    response = client.post("/api/v1/candidates", json={
        "name": "Yukta Bande",
        "email": "yukta@example.com",
    })
    candidate_id = response.json()["id"]
    client.patch(
        f"/api/v1/candidates/{candidate_id}/resume-text",
        json={"resume_text": "Python developer with FastAPI, SQL, NLP, and LLM experience."},
    )
    return candidate_id


@pytest.fixture
def multiple_jds(client: TestClient):
    jd_ids = []
    jds = [
        {"title": "Python Engineer", "company": "Corp A", "description_text": "Python FastAPI REST APIs SQL"},
        {"title": "Data Scientist", "company": "Corp B", "description_text": "Machine learning NLP Python data analysis"},
        {"title": "Java Developer", "company": "Corp C", "description_text": "Java Spring Boot microservices enterprise"},
    ]
    for jd in jds:
        response = client.post("/api/v1/job-descriptions", json=jd)
        jd_ids.append(response.json()["id"])
    return jd_ids


def test_bulk_match(client: TestClient, candidate_with_resume: int, multiple_jds: list):
    response = client.post("/api/v1/match/bulk", json={
        "candidate_id": candidate_with_resume,
        "job_description_ids": multiple_jds,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["total_jds_matched"] == 3
    assert len(data["results"]) == 3
    scores = [r["similarity_score"] for r in data["results"]]
    assert scores == sorted(scores, reverse=True)


def test_bulk_match_limit(client: TestClient, candidate_with_resume: int, multiple_jds: list):
    response = client.post("/api/v1/match/bulk", json={
        "candidate_id": candidate_with_resume,
        "job_description_ids": list(range(1, 22)),
    })
    assert response.status_code == 400


def test_match_history(client: TestClient, candidate_with_resume: int, multiple_jds: list):
    client.post("/api/v1/match/bulk", json={
        "candidate_id": candidate_with_resume,
        "job_description_ids": multiple_jds,
    })
    response = client.get(f"/api/v1/candidates/{candidate_with_resume}/matches")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_bulk_match_no_resume(client: TestClient, multiple_jds: list):
    response = client.post("/api/v1/candidates", json={
        "name": "No Resume",
        "email": "noresume@example.com",
    })
    candidate_id = response.json()["id"]

    response = client.post("/api/v1/match/bulk", json={
        "candidate_id": candidate_id,
        "job_description_ids": multiple_jds,
    })
    assert response.status_code == 400