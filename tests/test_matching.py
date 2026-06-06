import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def candidate_with_resume(client: TestClient):
    candidate_response = client.post("/api/v1/candidates", json={
        "name": "Yukta Bande",
        "email": "yukta@example.com",
    })
    candidate_id = candidate_response.json()["id"]

    resume_text = """
    Experienced Python developer with strong background in FastAPI,
    machine learning, NLP, and LLM development. Proficient in SQL,
    PostgreSQL, REST API design, and microservices architecture.
    Experience with LangChain, Hugging Face, and generative AI systems.
    """

    client.patch(
        f"/api/v1/candidates/{candidate_id}/resume-text",
        json={"resume_text": resume_text}
    )

    return candidate_id


@pytest.fixture
def job_description(client: TestClient):
    response = client.post("/api/v1/job-descriptions", json={
        "title": "Python Backend Engineer",
        "company": "Tech Corp",
        "description_text": """
        Looking for a Python developer with FastAPI experience.
        Must have strong SQL skills and experience with REST APIs.
        Knowledge of machine learning and NLP is a plus.
        Experience with PostgreSQL and microservices preferred.
        """,
    })
    return response.json()["id"]


def test_create_job_description(client: TestClient):
    response = client.post("/api/v1/job-descriptions", json={
        "title": "Python Developer",
        "company": "Acme Corp",
        "description_text": "Looking for a Python developer with FastAPI skills.",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Python Developer"
    assert data["id"] is not None


def test_list_job_descriptions(client: TestClient):
    client.post("/api/v1/job-descriptions", json={
        "title": "Python Developer",
        "company": "Acme Corp",
        "description_text": "Looking for a Python developer.",
    })
    response = client.get("/api/v1/job-descriptions")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_match_without_resume(client: TestClient, job_description: int):
    candidate_response = client.post("/api/v1/candidates", json={
        "name": "No Resume",
        "email": "noresume@example.com",
    })
    candidate_id = candidate_response.json()["id"]

    response = client.post("/api/v1/match", json={
        "candidate_id": candidate_id,
        "job_description_id": job_description,
    })
    assert response.status_code == 400


def test_match_nonexistent_candidate(client: TestClient, job_description: int):
    response = client.post("/api/v1/match", json={
        "candidate_id": 99999,
        "job_description_id": job_description,
    })
    assert response.status_code == 404