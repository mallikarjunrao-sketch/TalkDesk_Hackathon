from fastapi import APIRouter, Path, status
from backend.app.schemas.payments import PaymentDiagnosisResponse

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get(
    "/{payment_ref}/diagnosis",
    response_model=PaymentDiagnosisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Payment Failure Diagnosis",
    description="Retrieve diagnosis of operational discrepancies between payment gateway and order management system.",
)
async def get_payment_diagnosis(
    payment_ref: str = Path(..., description="Payment reference code, e.g. TX-101"),
) -> PaymentDiagnosisResponse:
    """Return diagnosis highlighting payment captured vs order creation mismatch."""
    return PaymentDiagnosisResponse(
        payment_ref=payment_ref,
        payment_status="CAPTURED",
        order_status="NOT_CREATED",
        amount=4299.0,
        currency="INR",
        mismatch=True,
        incident_id="INC-0042",
        simulated=True,
    )

