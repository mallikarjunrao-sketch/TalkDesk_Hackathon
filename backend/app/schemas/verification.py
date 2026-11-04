from pydantic import BaseModel, Field
from backend.app.schemas.common import CommitmentStatus


class RunVerificationRequest(BaseModel):
    """Request to run independent outcome verification for a commitment."""
    commitment_id: str = Field(..., examples=["CMT-001"], description="Target commitment identifier")


class RunVerificationResponse(BaseModel):
    """Result of independent outcome verification."""
    commitment_id: str = Field(..., examples=["CMT-001"], description="Commitment identifier")
    settlement: str = Field(..., examples=["NOT_FOUND"], description="Settlement state: NOT_FOUND, FOUND, PENDING")
    status: CommitmentStatus = Field(..., examples=["AT_RISK"], description="Updated status: AT_RISK or VERIFIED")
    evidence: str = Field(
        ...,
        examples=["Refund API accepted; settlement not found."],
        description="Independent evidence collected",
    )

