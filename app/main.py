from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.routes import health, candidates, matching


@asynccontextmanager
async def lifespan(app: FastAPI):
    # runs on startup before accepting requests
    print("Loading sentence transformer model...")
    from app.services.matcher import get_model
    get_model()
    print("Model loaded and ready.")
    yield
    # runs on shutdown


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health.router, prefix="/api/v1", tags=["Health"])
    application.include_router(candidates.router, prefix="/api/v1", tags=["Candidates"])
    application.include_router(matching.router, prefix="/api/v1", tags=["Matching"])

    return application


app = create_application()