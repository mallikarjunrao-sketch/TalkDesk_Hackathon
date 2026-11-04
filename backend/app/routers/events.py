from fastapi import APIRouter, status
from backend.app.schemas.events import EventIngestRequest, EventIngestResponse

router = APIRouter(prefix="/events", tags=["Events"])


@router.post(
    "/ingest",
    response_model=EventIngestResponse,
    status_code=status.HTTP_200_OK,
    summary="Ingest External Telemetry Event",
    description="Ingest operational event from external webhook or telemetry system. Maps wire field 'type' to internal 'event_type'.",
)
async def ingest_event(request: EventIngestRequest) -> EventIngestResponse:
    """Ingest operational failure event and correlate with active incident (simulated)."""
    # Explicit mapping: wire field `request.type` is accessible internally as `request.event_type`
    _internal_event_type = request.event_type

    return EventIngestResponse(
        accepted=True,
        incident_id="INC-0042",
        incident_opened=False,
    )

