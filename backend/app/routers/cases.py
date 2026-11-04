from fastapi import APIRouter, Path, status
from backend.app.schemas.cases import CaseContextResponse, CommitmentSummary, CustomerInfo

router = APIRouter(prefix="/cases", tags=["Cases"])


@router.get(
    "/{case_ref}/context",
    response_model=CaseContextResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Customer Case Context",
    description="Retrieve synthesized case context, customer profile, and open commitments for Talkdesk integration.",
)
async def get_case_context(
    case_ref: str = Path(..., description="Unique case reference, e.g. CASE-2041 or CASE-1001"),
) -> CaseContextResponse:
    """Return synthesized case context for Talkdesk screen pop / agent assistance."""
    return CaseContextResponse(
        case_ref=case_ref,
        customer=CustomerInfo(
            customer_id="CUST-9011",
            name="Jane Doe",
            phone="+15550192834",
            email="jane.doe@example.com",
        ),
        status="OPEN",
        payment_ref="TX-101",
        incident_id="INC-0042",
        open_commitments=[
            CommitmentSummary(
                id="CMT-001",
                action_type="REFUND",
                status="PROPOSED",
                amount=4299.0,
                currency="INR",
            )
        ],
        simulated=True,
    )

