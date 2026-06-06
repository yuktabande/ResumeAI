# Resume Intelligence Platform

An AI-powered platform that semantically matches resumes to job descriptions using sentence transformers and cosine similarity scoring.


**Live App:** [https://resume-intelligence-ui.vercel.app ](https://resume-ai-interface.vercel.app/) 

**API Docs:** https://your-render-url.onrender.com/docs

---

## Screenshot

![Resume Intelligence Dashboard](resume-intelligence-ui/src/assets/demo.jpeg)

## What It Does

- Upload a resume PDF — text is extracted and stored automatically
- Add job descriptions from any JD text
- Match your resume against a single JD and get a semantic similarity score
- Bulk match your resume against up to 20 JDs at once, ranked by relevance
- View full match history for any candidate

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI, Pydantic |
| Database | PostgreSQL, SQLAlchemy 2.0, Alembic |
| AI / ML | sentence-transformers (all-MiniLM-L6-v2), scikit-learn |
| PDF Parsing | pdfplumber |
| Testing | pytest, pytest-cov, pytest-asyncio |
| CI/CD | GitHub Actions |
| Containerization | Docker, Docker Compose |
| Deployment | Render (backend), Vercel (frontend) |

---


## Local Setup

### Prerequisites
- Python 3.13+
- PostgreSQL 15+
- Node.js 18+ (for frontend)

### Backend — Without Docker

```bash
git clone https://github.com/YOUR_USERNAME/resume-intelligence
cd resume-intelligence

python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"

cp .env.example .env
# Edit .env and set DATABASE_URL

createdb resume_intelligence
python3 -m alembic upgrade head

python3 -m uvicorn app.main:app --reload
```

API available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

### Backend — With Docker

```bash
git clone https://github.com/YOUR_USERNAME/resume-intelligence
cd resume-intelligence

docker compose up --build
```

API available at `http://localhost:8000`

### Frontend

```bash
git clone https://github.com/YOUR_USERNAME/resume-intelligence-ui
cd resume-intelligence-ui

npm install
cp .env.example .env.local
# Set VITE_API_URL=http://localhost:8000

npm run dev
```

Frontend available at `http://localhost:5173`

---

## Running Tests

```bash
python3 -m pytest -v --cov=app --cov-report=term-missing
```

Tests use an in-memory SQLite database — no PostgreSQL required to run the test suite.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/health | Health check |
| POST | /api/v1/candidates | Create candidate |
| GET | /api/v1/candidates | List all candidates |
| GET | /api/v1/candidates/{id} | Get candidate by ID |
| POST | /api/v1/candidates/{id}/resume | Upload resume PDF |
| GET | /api/v1/candidates/{id}/matches | Match history |
| POST | /api/v1/job-descriptions | Create job description |
| GET | /api/v1/job-descriptions | List all job descriptions |
| GET | /api/v1/job-descriptions/{id} | Get JD by ID |
| POST | /api/v1/match | Match resume to single JD |
| POST | /api/v1/match/bulk | Bulk match resume to multiple JDs |

---

## Project Structure
```bash
resume-intelligence/
├── app/
│   ├── api/routes/          # FastAPI route handlers
│   ├── core/                # Config, database engine, session management
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   └── services/            # Business logic layer
├── alembic/                 # Database migrations
├── tests/                   # pytest test suite
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://localhost/resume_intelligence` |
| `DEBUG` | Enable SQLAlchemy query logging | `false` |
| `APP_NAME` | API title shown in docs | `Resume Intelligence API` |

---

## Deployment

### Backend — Render
Configured via `render.yaml`. Connect your GitHub repo to Render and it deploys automatically on every push to `main`.

### Frontend — Vercel
Connect your `resume-intelligence-ui` GitHub repo to Vercel. Set `VITE_API_URL` to your Render backend URL as an environment variable in the Vercel dashboard.
