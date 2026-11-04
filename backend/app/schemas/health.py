from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Structured response for the health check endpoint."""
    status: str = Field(..., examples=["ok"], description="Overall health status of service")
    service: str = Field(..., examples=["PULSE Backend"], description="Service identifier")
    database: str = Field(..., examples=["connected"], description="Database connection status")
