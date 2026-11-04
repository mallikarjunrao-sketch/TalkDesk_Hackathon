from fastapi import APIRouter, status
from backend.app.schemas.common import CommitmentStatus, PolicyDecisionEnum
from backend.app.schemas.resolutions import (
    ExecuteResolutionRequest,
    ExecuteResolutionResponse,
    ProposeResolutionRequest,
    ProposeResolutionResponse,
)

router = APIRouter(prefix="/resolutions", tags=["Resolutions"])


@router.post(
    "/propose",
    response_model=ProposeResolutionResponse,
    status_code=status.HTTP_200_OK,
    summary="Propose Resolution Remedy",
    description="Evaluate policy rules for a proposed recovery remedy (e.g. refund) and register commitment.",
)
async def propose_resolution(request: ProposeResolutionRequest) -> ProposeResolutionResponse:
    """Return simulated policy engine evaluation and proposal commitment."""
    return ProposeResolutionResponse(
        decision=PolicyDecisionEnum.ALLOW,
        rule_id="R3",
        commitment_id="CMT-001",
        status=CommitmentStatus.PROPOSED,
    )


@router.post(
    "/execute",
    response_model=ExecuteResolutionResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute Resolution Action",
    description="Dispatch an authorized resolution commitment to execution subsystem.",
)
async def execute_resolution(request: ExecuteResolutionRequest) -> ExecuteResolutionResponse:
    """Return simulated execution dispatch acknowledgement."""
    return ExecuteResolutionResponse(
        commitment_id=request.commitment_id,
        action_ref="RF-8821",
        status=CommitmentStatus.ACKNOWLEDGED,
        customer_message_hint="Your refund request has been submitted. We are still checking settlement.",
    )

