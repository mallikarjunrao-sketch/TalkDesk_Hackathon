from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from backend.app.schemas.common import CommitmentStatus


class CommitmentResponse(BaseModel):
    """Structured record of a customer recovery commitment."""
    id: str = Field(..., examples=["CMT-001"], description="Commitment identifier")
    case_ref: str = Field(..., examples=["CASE-2041"], description="Associated case reference")
    action_type: str = Field(..., examples=["REFUND"], description="Action type: REFUND, CREDIT, APOLOGY")
    amount: Optional[float] = Field(default=None, examples=[4299.0], description="Monetary value if applicable")
    currency: str = Field(default="INR", examples=["INR"], description="Currency code")
    status: CommitmentStatus = Field(..., examples=["PROPOSED"], description="Lifecycle commitment status")
    deadline: Optional[str] = Field(default=None, examples=["2026-11-05T12:00:00Z"], description="SLA target deadline")
    incident_id: Optional[str] = Field(default=None, examples=["INC-0042"], description="Correlated incident")
    evidence: Optional[str] = Field(default=None, examples=["Refund API accepted; settlement not found."], description="Outcome verification evidence")
    created_at: datetime = Field(..., description="Timestamp of commitment creation")
    updated_at: datetime = Field(..., description="Timestamp of last update")
    simulated: bool = Field(default=True, description="Indicates simulated stub data")


class ApproveCommitmentRequest(BaseModel):
    """Supervisor approval or rejection for a pending commitment."""
    supervisor_id: str = Field(..., examples=["SUP-101"], description="Supervisor ID authorizing the action")
    approved: bool = Field(default=True, description="True to approve and proceed, False to deny")
    notes: Optional[str] = Field(default=None, examples=["Authorized goodwill refund."], description="Approval notes")


class ApproveCommitmentResponse(BaseModel):
    """Result of supervisor approval evaluation."""
    commitment_id: str = Field(..., examples=["CMT-001"], description="Commitment identifier")
    status: CommitmentStatus = Field(..., examples=["REQUESTED"], description="New commitment status")
    approved: bool = Field(..., examples=[True], description="Approval decision outcome")
    approved_by: str = Field(..., examples=["SUP-101"], description="Supervisor ID who processed approval")
    message: str = Field(..., examples=["Commitment approved and queued for execution."], description="Status summary")
    simulated: bool = Field(default=True, description="Indicates simulated stub data")

