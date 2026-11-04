from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
from backend.app.schemas.common import CommitmentStatus, PolicyDecisionEnum


class Commitment(SQLModel, table=True):
    """Represents a customer commitment made during an operational failure."""
    id: Optional[int] = Field(default=None, primary_key=True)
    case_ref: str = Field(index=True, description="Associated case reference")
    action_type: str = Field(description="Action to execute, e.g. REFUND, CREDIT, APOLOGY")
    amount: Optional[float] = Field(default=None, description="Monetary value if applicable")
    currency: str = Field(default="USD", description="Currency code")
    status: CommitmentStatus = Field(
        default=CommitmentStatus.PROPOSED,
        index=True,
        description="Agreed lifecycle status of the commitment",
    )
    policy_decision: Optional[PolicyDecisionEnum] = Field(
        default=None,
        description="Evaluated policy engine decision",
    )
    target_date: Optional[datetime] = Field(default=None, description="Expected SLA resolution deadline")
    verified_at: Optional[datetime] = Field(default=None, description="Timestamp when verification succeeded")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

