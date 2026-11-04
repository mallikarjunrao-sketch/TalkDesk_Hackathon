from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.config import settings
from backend.app.database import check_database_connection, init_db
from backend.app.routers import (
    admin_router,
    cases_router,
    commitments_router,
    dashboard_router,
    events_router,
    incidents_router,
    mock_router,
    payments_router,
    resolutions_router,
    verification_router,
)
from backend.app.schemas.health import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup and shutdown events."""
    # Initialize database tables on startup
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check service health and database connectivity.",
    tags=["System"],
)
async def health_check():
    """Verify application health and verify database connectivity."""
    db_connected = check_database_connection()

    if db_connected:
        return HealthResponse(
            status="ok",
            service=settings.PROJECT_NAME,
            database="connected",
        )

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=HealthResponse(
            status="degraded",
            service=settings.PROJECT_NAME,
            database="disconnected",
        ).model_dump(),
    )


# Register all B2 API stub routers
app.include_router(cases_router)
app.include_router(payments_router)
app.include_router(incidents_router)
app.include_router(resolutions_router)
app.include_router(verification_router)
app.include_router(commitments_router)
app.include_router(events_router)
app.include_router(dashboard_router)
app.include_router(mock_router)
app.include_router(admin_router)
