import os
import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity

HF_API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"


def get_headers():
    token = os.environ.get("HF_API_TOKEN")
    return {"Authorization": f"Bearer {token}"}


def generate_embedding(text: str) -> np.ndarray:
    response = requests.post(
        HF_API_URL,
        headers=get_headers(),
        json={"inputs": text[:512]},
    )
    response.raise_for_status()
    return np.array(response.json())


def compute_similarity(text_a: str, text_b: str) -> float:
    embedding_a = generate_embedding(text_a)
    embedding_b = generate_embedding(text_b)

    if embedding_a.ndim > 1:
        embedding_a = embedding_a[0]
    if embedding_b.ndim > 1:
        embedding_b = embedding_b[0]

    score = cosine_similarity(
        embedding_a.reshape(1, -1),
        embedding_b.reshape(1, -1)
    )[0][0]
    return float(score)


def get_assessment(score: float) -> str:
    if score >= 0.75:
        return "Strong Match"
    elif score >= 0.55:
        return "Moderate Match"
    elif score >= 0.35:
        return "Weak Match"
    else:
        return "Poor Match"


def match_resume_to_jd(resume_text: str, jd_text: str) -> dict:
    score = compute_similarity(resume_text, jd_text)
    percentage = round(score * 100)
    assessment = get_assessment(score)
    return {
        "similarity_score": score,
        "match_percentage": percentage,
        "assessment": assessment,
    }