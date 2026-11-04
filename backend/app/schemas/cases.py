from typing import List, Optional
from pydantic import BaseModel, Field


class CustomerInfo(BaseModel):
    """Customer identity information."""
    customer_id: str = Field(..., examples=["CUST-9011"], description="Customer identifier")
    name: str = Field(..., examples=["Jane Doe"], description="Customer full name")
    phone: Optional[str] = Field(default=None, examples=["+15550192834"], description="Contact phone")
    email: Optional[str] = Field(default=None, examples=["jane.doe@example.com"], description="Contact email")


class CommitmentSummary(BaseModel):
    """Summary of commitment associated with a case."""
    id: str = Field(..., examples=["CMT-001"], description="Commitment identifier")
    action_type: str = Field(..., examples=["REFUND"], description="Action type")
    status: str = Field(..., examples=["PROPOSED"], description="Current commitment status")
    amount: Optional[float] = Field(default=None, examples=[4299.0], description="Amount")
    currency: str = Field(default="INR", examples=["INR"], description="Currency code")


class CaseContextResponse(BaseModel):
    """Synthesized case context for Talkdesk screen pop / agent assistance."""
    case_ref: str = Field(..., examples=["CASE-2041"], description="Case reference code")
    customer: CustomerInfo = Field(..., description="Customer details")
    status: str = Field(..., examples=["OPEN"], description="Case lifecycle status")
    payment_ref: Optional[str] = Field(default=None, examples=["TX-101"], description="Associated payment reference")
    incident_id: Optional[str] = Field(default=None, examples=["INC-0042"], description="Correlated operational incident")
    open_commitments: List[CommitmentSummary] = Field(default_factory=list, description="List of open commitments")
    simulated: bool = Field(default=True, description="Indicates simulated stub data")

