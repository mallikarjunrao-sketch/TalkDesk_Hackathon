from typing import Optional
from pydantic import BaseModel, Field, model_validator
from backend.app.schemas.common import CommitmentStatus, PolicyDecisionEnum


class ProposeResolutionRequest(BaseModel):
    """Request to propose an operational resolution/remedy for a customer case."""
    case_id: Optional[str] = Field(default=None, examples=["CASE-2041"], description="Target case ID")
    case_ref: Optional[str] = Field(default=None, examples=["CASE-2041"], description="Alternative case reference")
    remedy: str = Field(..., examples=["REFUND"], description="Remedy action type: REFUND, CREDIT, APOLOGY")
    amount: Optional[float] = Field(default=None, examples=[4299.0], description="Amount proposed if applicable")
    currency: str = Field(default="INR", examples=["INR"], description="Currency code")

    @model_validator(mode="after")
    def validate_case_identifier(self):
        if not self.case_id and not self.case_ref:
            raise ValueError("Either case_id or case_ref must be provided")
        # Normalize so case_id or case_ref can be used interchangeably
        if not self.case_id:
            self.case_id = self.case_ref
        if not self.case_ref:
            self.case_ref = self.case_id
        return self


class ProposeResolutionResponse(BaseModel):
    """Response returned by the policy engine for proposed resolution."""
    decision: PolicyDecisionEnum = Field(..., examples=["ALLOW"], description="Policy decision: ALLOW, DENY, NEEDS_APPROVAL")
    rule_id: str = Field(..., examples=["R3"], description="Policy rule identifier evaluated")
    commitment_id: str = Field(..., examples=["CMT-001"], description="Identifier of created commitment")
    status: CommitmentStatus = Field(..., examples=["PROPOSED"], description="Lifecycle status of commitment")


class ExecuteResolutionRequest(BaseModel):
    """Request to execute an approved commitment."""
    commitment_id: str = Field(..., examples=["CMT-001"], description="Identifier of commitment to execute")


class ExecuteResolutionResponse(BaseModel):
    """Response indicating execution has been acknowledged downstream."""
    commitment_id: str = Field(..., examples=["CMT-001"], description="Commitment identifier")
    action_ref: str = Field(..., examples=["RF-8821"], description="Execution transaction/refund reference")
    status: CommitmentStatus = Field(..., examples=["ACKNOWLEDGED"], description="Commitment status")
    customer_message_hint: str = Field(
        ...,
        examples=["Your refund request has been submitted. We are still checking settlement."],
        description="Suggested customer update hint",
    )

