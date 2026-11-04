from backend.app.routers.cases import router as cases_router
from backend.app.routers.payments import router as payments_router
from backend.app.routers.incidents import router as incidents_router
from backend.app.routers.resolutions import router as resolutions_router
from backend.app.routers.verification import router as verification_router
from backend.app.routers.commitments import router as commitments_router
from backend.app.routers.events import router as events_router
from backend.app.routers.dashboard import router as dashboard_router
from backend.app.routers.mock import router as mock_router
from backend.app.routers.admin import router as admin_router

__all__ = [
    "cases_router",
    "payments_router",
    "incidents_router",
    "resolutions_router",
    "verification_router",
    "commitments_router",
    "events_router",
    "dashboard_router",
    "mock_router",
    "admin_router",
]

