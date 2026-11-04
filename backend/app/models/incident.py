from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Incident(SQLModel, table=True):
    """Represents an ongoing operational outage or systemic failure."""
    id: Optional[int] = Field(default=None, primary_key=True)
    incident_ref: str = Field(index=True, unique=True, description="Unique incident identifier, e.g. INC-501")
    title: str = Field(description="Headline summary of the incident")
    description: Optional[str] = Field(default=None, description="Detailed explanation of the failure")
    severity: str = Field(default="MEDIUM", description="Severity level: LOW, MEDIUM, HIGH, CRITICAL")
    is_active: bool = Field(default=True, index=True, description="Active status of incident")
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = Field(default=None, description="Timestamp when incident was resolved")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

