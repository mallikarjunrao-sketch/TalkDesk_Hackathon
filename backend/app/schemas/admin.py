from enum import Enum
from pydantic import BaseModel, Field


class SettlementModeEnum(str, Enum):
    """Permitted simulated settlement modes."""
    NOT_FOUND = "NOT_FOUND"
    FOUND = "FOUND"


class SettlementModeRequest(BaseModel):
    """Request to configure the mock settlement behavior for demos."""
    mode: SettlementModeEnum = Field(
        ...,
        examples=["NOT_FOUND"],
        description="Configured settlement outcome: strictly 'NOT_FOUND' or 'FOUND'",
    )


class SettlementModeResponse(BaseModel):
    """Confirmation of updated settlement mode."""
    mode: SettlementModeEnum = Field(..., examples=["NOT_FOUND"], description="Active settlement mode")
    message: str = Field(..., examples=["Settlement mode set to NOT_FOUND"], description="Status confirmation")
    simulated: bool = Field(default=True, description="Indicates simulated stub data")


class AdminActionResponse(BaseModel):
    """Response returned for administrative actions such as seed or reset."""
    status: str = Field(default="ok", examples=["ok"], description="Operation status")
    message: str = Field(..., examples=["Demo data successfully seeded (simulated)"], description="Summary message")
    simulated: bool = Field(default=True, description="Indicates simulated stub data")

