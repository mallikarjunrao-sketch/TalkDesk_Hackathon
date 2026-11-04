from fastapi import APIRouter, status
from backend.app.schemas.admin import SettlementModeEnum
from backend.app.schemas.common import CommitmentStatus
from backend.app.schemas.verification import RunVerificationRequest, RunVerificationResponse
from backend.app.services.demo_state import demo_state

router = APIRouter(prefix="/verification", tags=["Verification"])


@router.post(
    "/run",
    response_model=RunVerificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Run Independent Outcome Verification",
    description="Query independent banking/settlement channels to confirm whether remediation reached the customer.",
)
async def run_verification(request: RunVerificationRequest) -> RunVerificationResponse:
    """Return simulated outcome verification based on active demo settlement mode."""
    if demo_state.settlement_mode == SettlementModeEnum.FOUND:
        return RunVerificationResponse(
            commitment_id=request.commitment_id,
            settlement="FOUND",
            status=CommitmentStatus.VERIFIED,
            evidence="Settlement confirmed via mock bank gateway settlement logs.",
        )

    return RunVerificationResponse(
        commitment_id=request.commitment_id,
        settlement="NOT_FOUND",
        status=CommitmentStatus.AT_RISK,
        evidence="Refund API accepted; settlement not found.",
    )

