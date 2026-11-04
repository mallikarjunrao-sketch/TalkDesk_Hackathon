from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class EventIngestRequest(BaseModel):
    """External telemetry or webhook event ingestion payload."""
    type: str = Field(
        ...,
        examples=["PAYMENT_CAPTURED_ORDER_NOT_CREATED"],
        description="Agreed external event type field (mapped internally to Event.event_type)",
    )
    payment_ref: Optional[str] = Field(
        default=None,
        examples=["TX-107"],
        description="Associated payment reference",
    )
    ts: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        examples=["2026-11-04T10:33:10Z"],
        description="Timestamp of event occurrence",
    )

    @property
    def event_type(self) -> str:
        """Internal mapping from external wire field `type` to model field `event_type`."""
        return self.type


class EventIngestResponse(BaseModel):
    """Result of event ingestion and initial triage."""
    accepted: bool = Field(default=True, examples=[True], description="Whether event ingestion succeeded")
    incident_id: Optional[str] = Field(default="INC-0042", examples=["INC-0042"], description="Correlated incident ID")
    incident_opened: bool = Field(default=False, examples=[False], description="Whether a new incident was declared")

