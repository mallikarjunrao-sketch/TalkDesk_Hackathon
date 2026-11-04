from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Case(SQLModel, table=True):
    """Represents a customer case or operational recovery scenario."""
    id: Optional[int] = Field(default=None, primary_key=True)
    case_ref: str = Field(index=True, unique=True, description="Unique reference code, e.g. CASE-1001")
    customer_id: str = Field(index=True, description="Customer identifier")
    title: Optional[str] = Field(default=None, description="Brief summary of the issue")
    status: str = Field(default="OPEN", index=True, description="Status of the case (OPEN, RESOLVED, CLOSED)")
    channel: str = Field(default="VOICE", description="Primary interaction channel (VOICE, DIGITAL)")
    talkdesk_interaction_id: Optional[str] = Field(default=None, index=True, description="Talkdesk interaction ID")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

