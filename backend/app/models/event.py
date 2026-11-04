from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    """Represents an ingested event from webhooks, telemetry, or Talkdesk."""
    id: Optional[int] = Field(default=None, primary_key=True)
    event_type: str = Field(index=True, description="Event name, e.g. PAYMENT_FAILED, CALL_DISCONNECTED")
    source: str = Field(description="Event source system (e.g. STRIPE, TALKDESK, CORE_BANKING)")
    payload: Optional[str] = Field(default=None, description="Raw event payload serialized as JSON")
    case_ref: Optional[str] = Field(default=None, index=True, description="Correlated case reference if resolved")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Event occurrence time")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

