from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Path, Query, status
from backend.app.schemas.commitments import (
    ApproveCommitmentRequest,
    ApproveCommitmentResponse,
    CommitmentResponse,
)
from backend.app.schemas.common import CommitmentStatus

router = APIRouter(prefix="/commitments", tags=["Commitments"])

SAMPLE_COMMITMENTS = [
    CommitmentResponse(
        id="CMT-001",
        case_ref="CASE-2041",
        action_type="REFUND",
        amount=4299.0,
        currency="INR",
        status=CommitmentStatus.PROPOSED,
        deadline="2026-11-05T12:00:00Z",
        incident_id="INC-0042",
        evidence="Refund API accepted; settlement not found.",
        created_at=datetime(2026, 11, 4, 8, 30, 0, tzinfo=timezone.utc),
        updated_at=datetime(2026, 11, 4, 8, 35, 0, tzinfo=timezone.utc),
        simulated=True,
    ),
    CommitmentResponse(
        id="CMT-002",
        case_ref="CASE-2038",
        action_type="CREDIT",
        amount=500.0,
        currency="INR",
        status=CommitmentStatus.VERIFIED,
        deadline="2026-11-04T18:00:00Z",
        incident_id="INC-0042",
        evidence="Store wallet credit balance increment confirmed.",
        created_at=datetime(2026, 11, 4, 7, 15, 0, tzinfo=timezone.utc),
        updated_at=datetime(2026, 11, 4, 7, 45, 0, tzinfo=timezone.utc),
        simulated=True,
    ),
]


@router.get(
    "",
    response_model=List[CommitmentResponse],
    status_code=status.HTTP_200_OK,
    summary="List Commitments",
    description="Retrieve all tracked customer commitments, with optional status and case filtering.",
)
async def list_commitments(
    status_filter: Optional[CommitmentStatus] = Query(default=None, alias="status", description="Filter by status"),
    case_ref: Optional[str] = Query(default=None, description="Filter by case reference"),
) -> List[CommitmentResponse]:
    """Return list of structured commitment records."""
    commitments = SAMPLE_COMMITMENTS
    if status_filter:
        commitments = [c for c in commitments if c.status == status_filter]
    if case_ref:
        commitments = [c for c in commitments if c.case_ref == case_ref]
    return commitments


@router.get(
    "/{id}",
    response_model=CommitmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Commitment Details",
    description="Retrieve single commitment record by identifier.",
)
async def get_commitment(
    id: str = Path(..., description="Commitment identifier, e.g. CMT-001"),
) -> CommitmentResponse:
    """Return commitment by ID (or matching sample)."""
    for c in SAMPLE_COMMITMENTS:
        if c.id == id:
            return c

    # Fallback simulated record if arbitrary id requested
    return CommitmentResponse(
        id=id,
        case_ref="CASE-2041",
        action_type="REFUND",
        amount=4299.0,
        currency="INR",
        status=CommitmentStatus.PROPOSED,
        deadline="2026-11-05T12:00:00Z",
        incident_id="INC-0042",
        evidence=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        simulated=True,
    )


@router.post(
    "/{id}/approve",
    response_model=ApproveCommitmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Approve or Reject Commitment",
    description="Human-in-the-loop authorization endpoint for supervisor to approve or deny a commitment.",
)
async def approve_commitment(
    id: str = Path(..., description="Commitment identifier to approve"),
    request: ApproveCommitmentRequest = ...,
) -> ApproveCommitmentResponse:
    """Process simulated supervisor approval."""
    new_status = CommitmentStatus.REQUESTED if request.approved else CommitmentStatus.DENIED
    action_word = "approved and queued for execution" if request.approved else "denied"
    return ApproveCommitmentResponse(
        commitment_id=id,
        status=new_status,
        approved=request.approved,
        approved_by=request.supervisor_id,
        message=f"Commitment {action_word}.",
        simulated=True,
    )

