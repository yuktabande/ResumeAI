import io
import pytest
from fastapi.testclient import TestClient


def test_create_candidate(client: TestClient):
    response = client.post("/api/v1/candidates", json={
        "name": "Yukta Bande",
        "email": "yukta@example.com",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Yukta Bande"
    assert data["email"] == "yukta@example.com"
    assert data["id"] is not None


def test_create_duplicate_candidate(client: TestClient):
    client.post("/api/v1/candidates", json={
        "name": "Yukta Bande",
        "email": "yukta@example.com",
    })
    response = client.post("/api/v1/candidates", json={
        "name": "Yukta Bande",
        "email": "yukta@example.com",
    })
    assert response.status_code == 400


def test_get_candidate(client: TestClient):
    create_response = client.post("/api/v1/candidates", json={
        "name": "Yukta Bande",
        "email": "yukta@example.com",
    })
    candidate_id = create_response.json()["id"]

    response = client.get(f"/api/v1/candidates/{candidate_id}")
    assert response.status_code == 200
    assert response.json()["id"] == candidate_id


def test_get_nonexistent_candidate(client: TestClient):
    response = client.get("/api/v1/candidates/99999")
    assert response.status_code == 404


def test_list_candidates(client: TestClient):
    client.post("/api/v1/candidates", json={
        "name": "Yukta Bande",
        "email": "yukta@example.com",
    })
    response = client.get("/api/v1/candidates")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_upload_non_pdf(client: TestClient):
    create_response = client.post("/api/v1/candidates", json={
        "name": "Yukta Bande",
        "email": "yukta@example.com",
    })
    candidate_id = create_response.json()["id"]

    response = client.post(
        f"/api/v1/candidates/{candidate_id}/resume",
        files={"file": ("resume.txt", b"some text content", "text/plain")},
    )
    assert response.status_code == 400