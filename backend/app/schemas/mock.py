from typing import Optional
from pydantic import BaseModel, Field


class MockRefundRequest(BaseModel):
    """Request dispatched to simulated payment gateway for refund processing."""
    payment_ref: str = Field(..., examples=["TX-101"], description="Target transaction reference")
    amount: float = Field(..., examples=[4299.0], description="Amount to refund")
    currency: str = Field(default="INR", examples=["INR"], description="Currency code")
    reason: Optional[str] = Field(
        default=None,
        examples=["Payment captured without order creation"],
        description="Reason for refund",
    )


class MockRefundResponse(BaseModel):
    """Acknowledgement from simulated gateway upon refund dispatch."""
    status: str = Field(default="ACCEPTED", examples=["ACCEPTED"], description="Gateway submission status")
    refund_ref: str = Field(default="RF-8821", examples=["RF-8821"], description="Downstream refund reference")
    payment_ref: str = Field(..., examples=["TX-101"], description="Target transaction reference")
    amount: float = Field(..., examples=[4299.0], description="Refunded amount")
    simulated: bool = Field(default=True, description="Indicates simulated stub data")


class MockSettlementResponse(BaseModel):
    """Settlement verification status queried from simulated banking network."""
    refund_ref: str = Field(..., examples=["RF-8821"], description="Refund reference code")
    settlement: str = Field(..., examples=["NOT_FOUND"], description="Settlement status: NOT_FOUND, FOUND")
    status: str = Field(..., examples=["PENDING"], description="Settlement stage: PENDING, SETTLED, FAILED")
    simulated: bool = Field(default=True, description="Indicates simulated stub data")

