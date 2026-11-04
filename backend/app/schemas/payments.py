from typing import Optional
from pydantic import BaseModel, Field


class PaymentDiagnosisResponse(BaseModel):
    """Diagnosis of transaction failure and operational mismatch."""
    payment_ref: str = Field(..., examples=["TX-101"], description="Payment transaction reference")
    payment_status: str = Field(..., examples=["CAPTURED"], description="Status in payment gateway")
    order_status: str = Field(..., examples=["NOT_CREATED"], description="Status in order management system")
    amount: float = Field(..., examples=[4299.0], description="Transaction amount")
    currency: str = Field(..., examples=["INR"], description="Currency code")
    mismatch: bool = Field(..., examples=[True], description="Whether a discrepancy exists between payment and order")
    incident_id: Optional[str] = Field(default=None, examples=["INC-0042"], description="Correlated incident ID")
    simulated: bool = Field(default=True, description="Indicates simulated stub data")

