from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
from backend.app.schemas.common import PolicyDecisionEnum


class PolicyDecision(SQLModel, table=True):
    """Represents an automated or manual policy decision record."""
    __tablename__ = "policy_decision"

    id: Optional[int] = Field(default=None, primary_key=True)
    commitment_id: Optional[int] = Field(default=None, foreign_key="commitment.id", index=True)
    decision: PolicyDecisionEnum = Field(index=True, description="Decision result: ALLOW, DENY, NEEDS_APPROVAL")
    rule_name: Optional[str] = Field(default=None, description="Name or code of the policy rule evaluated")
    reason: Optional[str] = Field(default=None, description="Reasoning or failure explanation")
    assessed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

