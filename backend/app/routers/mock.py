from fastapi import APIRouter, Path, status
from backend.app.schemas.admin import SettlementModeEnum
from backend.app.schemas.mock import (
    MockRefundRequest,
    MockRefundResponse,
    MockSettlementResponse,
)
from backend.app.services.demo_state import demo_state

router = APIRouter(prefix="/mock", tags=["Mock Services"])


@router.post(
    "/refund",
    response_model=MockRefundResponse,
    status_code=status.HTTP_200_OK,
    summary="Mock Payment Gateway Refund",
    description="Simulates downstream payment provider accepting a refund execution request.",
)
async def mock_refund(request: MockRefundRequest) -> MockRefundResponse:
    """Simulate refund dispatch to payment processor."""
    return MockRefundResponse(
        status="ACCEPTED",
        refund_ref="RF-8821",
        payment_ref=request.payment_ref,
        amount=request.amount,
        simulated=True,
    )


@router.get(
    "/settlement/{refund_ref}",
    response_model=MockSettlementResponse,
    status_code=status.HTTP_200_OK,
    summary="Mock Banking Settlement Query",
    description="Simulates banking network endpoint queried by independent verifier to check fund settlement.",
)
async def mock_settlement(
    refund_ref: str = Path(..., description="Refund reference code, e.g. RF-8821"),
) -> MockSettlementResponse:
    """Return settlement status based on active demo control mode."""
    if demo_state.settlement_mode == SettlementModeEnum.FOUND:
        return MockSettlementResponse(
            refund_ref=refund_ref,
            settlement="FOUND",
            status="SETTLED",
            simulated=True,
        )

    return MockSettlementResponse(
        refund_ref=refund_ref,
        settlement="NOT_FOUND",
        status="PENDING",
        simulated=True,
    )

