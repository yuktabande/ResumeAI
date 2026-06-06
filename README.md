# Resume Intelligence Platform

An AI-powered platform that matches resumes to job descriptions using semantic embeddings and LLM-based scoring.

[![CI](https://github.com/YOUR_USERNAME/resume-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/resume-intelligence/actions/workflows/ci.yml)

**Live API:** https://your-render-url.onrender.com/docs

---

## What It Does

- Upload a resume PDF and extract text automatically
- Create job descriptions from any JD text
- Match a resume against a single JD and get a semantic similarity score
- Bulk match a resume against up to 20 JDs at once, ranked by relevance
- View full match history for any candidate

## Tech Stack

| Layer       | Technology                          |
| ----------- | ----------------------------------- |
| API         | FastAPI, Pydantic                   |
| Database    | PostgreSQL, SQLAlchemy, Alembic     |
| AI/ML       | sentence-transformers, scikit-learn |
| PDF Parsing | pdfplumber                          |
| Testing     | pytest, pytest-cov                  |
| CI/CD       | GitHub Actions                      |
| Deployment  | Docker, Render                      |

## Architecture
