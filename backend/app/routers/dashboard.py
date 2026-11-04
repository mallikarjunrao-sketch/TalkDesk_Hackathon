from fastapi import APIRouter, status
from backend.app.schemas.dashboard import DashboardIncidentSummary, DashboardResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "",
    response_model=DashboardResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Overview Dashboard Metrics",
    description="Retrieve high-level operational metrics, active incident stats, and commitment recovery tracking.",
)
async def get_dashboard() -> DashboardResponse:
    """Return simulated dashboard metrics for frontend overview."""
    return DashboardResponse(
        incident=DashboardIncidentSummary(
            id="INC-0042",
            status="ACTIVE",
        ),
        affected_transactions=50,
        contacted_support=8,
        commitments_created=8,
        verified=6,
        awaiting_or_at_risk=2,
        simulated=True,
    )

