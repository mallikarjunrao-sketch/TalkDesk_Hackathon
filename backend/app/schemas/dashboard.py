from typing import Optional
from pydantic import BaseModel, Field


class DashboardIncidentSummary(BaseModel):
    """High-level summary of active incident for dashboard."""
    id: str = Field(..., examples=["INC-0042"], description="Incident ID")
    status: str = Field(..., examples=["ACTIVE"], description="Incident status")


class DashboardResponse(BaseModel):
    """Aggregated operational and recovery metrics for the frontend dashboard."""
    incident: Optional[DashboardIncidentSummary] = Field(..., description="Primary active incident")
    affected_transactions: int = Field(..., examples=[50], description="Total transactions affected")
    contacted_support: int = Field(..., examples=[8], description="Number of customers contacting support")
    commitments_created: int = Field(..., examples=[8], description="Number of customer recovery commitments")
    verified: int = Field(..., examples=[6], description="Commitments successfully verified")
    awaiting_or_at_risk: int = Field(..., examples=[2], description="Commitments awaiting verification or breached SLA")
    simulated: bool = Field(default=True, description="Indicates simulated stub data")

