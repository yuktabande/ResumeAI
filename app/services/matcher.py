from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    return SentenceTransformer("paraphrase-MiniLM-L3-v2")


def generate_embedding(text: str) -> np.ndarray:
    model = get_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding


def compute_similarity(text_a: str, text_b: str) -> float:
    embedding_a = generate_embedding(text_a)
    embedding_b = generate_embedding(text_b)

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