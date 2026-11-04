from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ActiveIncidentResponse(BaseModel):
    """Details of an active operational incident."""
    incident_id: str = Field(..., examples=["INC-0042"], description="Unique incident identifier")
    status: str = Field(..., examples=["ACTIVE"], description="Current incident operational status")
    issue_type: str = Field(..., examples=["PAYMENT_CAPTURED_ORDER_NOT_CREATED"], description="Classified issue type")
    affected_population: int = Field(..., examples=[50], description="Number of affected customers/transactions")
    contacted_support: int = Field(..., examples=[8], description="Number of customers who contacted support")
    public_message: str = Field(
        ...,
        examples=[
            "We are experiencing a payment processing delay where orders may not immediately show as confirmed. "
            "Our team is actively resolving this."
        ],
        description="Public/agent guidance message",
    )
    simulated: bool = Field(default=True, description="Indicates simulated stub data")


class IncidentItemResponse(BaseModel):
    """Item in incident listing."""
    incident_id: str = Field(..., examples=["INC-0042"], description="Unique incident identifier")
    title: str = Field(..., examples=["Payment Captured but Order Not Created"], description="Incident title")
    status: str = Field(..., examples=["ACTIVE"], description="Incident status: ACTIVE, RESOLVED, MONITORING")
    severity: str = Field(..., examples=["HIGH"], description="Severity: LOW, MEDIUM, HIGH, CRITICAL")
    issue_type: str = Field(..., examples=["PAYMENT_CAPTURED_ORDER_NOT_CREATED"], description="Operational issue type")
    affected_count: int = Field(..., examples=[50], description="Estimated number of affected transactions")
    created_at: datetime = Field(..., description="Incident registration timestamp")
    simulated: bool = Field(default=True, description="Indicates simulated stub data")

