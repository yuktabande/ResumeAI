import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def generate_embedding(text: str) -> np.ndarray:
    model = get_model()
    embedding = model.encode(text[:512], convert_to_numpy=True)
    return np.array(embedding)


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