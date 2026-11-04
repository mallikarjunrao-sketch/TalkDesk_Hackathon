from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Action(SQLModel, table=True):
    """Represents an execution action initiated to fulfill a commitment."""
    id: Optional[int] = Field(default=None, primary_key=True)
    commitment_id: Optional[int] = Field(default=None, foreign_key="commitment.id", index=True)
    action_type: str = Field(description="Action name, e.g. EXECUTE_REFUND, ISSUE_CREDIT")
    status: str = Field(default="PENDING", index=True, description="PENDING, IN_PROGRESS, COMPLETED, FAILED")
    payload: Optional[str] = Field(default=None, description="Serialized JSON payload dispatched to downstream")
    external_ref: Optional[str] = Field(default=None, index=True, description="External transaction or settlement ref")
    executed_at: Optional[datetime] = Field(default=None, description="Execution completion timestamp")
    error_message: Optional[str] = Field(default=None, description="Failure details if action failed")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

