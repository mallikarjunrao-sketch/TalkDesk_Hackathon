from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Query, status
from backend.app.schemas.incidents import ActiveIncidentResponse, IncidentItemResponse

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.get(
    "/active",
    response_model=ActiveIncidentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Active Incident",
    description="Retrieve current active operational incident matching issue type or reference.",
)
async def get_active_incident(
    issue_type: Optional[str] = Query(
        default=None,
        description="Filter by issue type, e.g. PAYMENT_CAPTURED_ORDER_NOT_CREATED",
    ),
    reference: Optional[str] = Query(
        default=None,
        description="Filter by reference code, e.g. TX-101",
    ),
) -> ActiveIncidentResponse:
    """Return active incident INC-0042 details."""
    resolved_issue_type = issue_type or "PAYMENT_CAPTURED_ORDER_NOT_CREATED"
    return ActiveIncidentResponse(
        incident_id="INC-0042",
        status="ACTIVE",
        issue_type=resolved_issue_type,
        affected_population=50,
        contacted_support=8,
        public_message=(
            "We are experiencing a payment processing delay where orders may not immediately show as confirmed. "
            "Our team is actively resolving this."
        ),
        simulated=True,
    )


@router.get(
    "",
    response_model=List[IncidentItemResponse],
    status_code=status.HTTP_200_OK,
    summary="List Operational Incidents",
    description="Retrieve all operational incidents (active and resolved) for correlation and reporting.",
)
async def list_incidents() -> List[IncidentItemResponse]:
    """Return list of active and historical incidents (simulated)."""
    return [
        IncidentItemResponse(
            incident_id="INC-0042",
            title="Payment Captured but Order Not Created",
            status="ACTIVE",
            severity="HIGH",
            issue_type="PAYMENT_CAPTURED_ORDER_NOT_CREATED",
            affected_count=50,
            created_at=datetime(2026, 11, 4, 8, 0, 0, tzinfo=timezone.utc),
            simulated=True,
        ),
        IncidentItemResponse(
            incident_id="INC-0038",
            title="SMS OTP Gateway Latency",
            status="RESOLVED",
            severity="LOW",
            issue_type="SMS_DELIVERY_DELAY",
            affected_count=12,
            created_at=datetime(2026, 11, 3, 14, 0, 0, tzinfo=timezone.utc),
            simulated=True,
        ),
    ]

