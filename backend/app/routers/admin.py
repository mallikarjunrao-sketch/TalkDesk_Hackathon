from fastapi import APIRouter, status
from backend.app.schemas.admin import (
    AdminActionResponse,
    SettlementModeRequest,
    SettlementModeResponse,
)
from backend.app.services.demo_state import demo_state

router = APIRouter(prefix="/admin", tags=["Demo Administration"])


@router.post(
    "/settlement-mode",
    response_model=SettlementModeResponse,
    status_code=status.HTTP_200_OK,
    summary="Set Mock Settlement Mode",
    description="Configure settlement mode for live demonstrations. Strictly accepts 'NOT_FOUND' or 'FOUND'.",
)
async def set_settlement_mode(request: SettlementModeRequest) -> SettlementModeResponse:
    """Set the mock settlement verification mode for demo scenarios."""
    demo_state.set_settlement_mode(request.mode)
    return SettlementModeResponse(
        mode=request.mode,
        message=f"Settlement mode set to {request.mode.value}",
        simulated=True,
    )


@router.post(
    "/seed",
    response_model=AdminActionResponse,
    status_code=status.HTTP_200_OK,
    summary="Seed Demo Scenarios",
    description="Populate demo data (incidents, transactions, cases) for testing and demonstrations.",
)
async def seed_demo_data() -> AdminActionResponse:
    """Simulate seeding of demo scenarios."""
    return AdminActionResponse(
        status="ok",
        message="Demo data successfully seeded (simulated)",
        simulated=True,
    )


@router.post(
    "/reset",
    response_model=AdminActionResponse,
    status_code=status.HTTP_200_OK,
    summary="Reset Demo State",
    description="Reset mock state and controls back to initial baseline for clean demo replays.",
)
async def reset_demo_state() -> AdminActionResponse:
    """Reset demo state back to default NOT_FOUND."""
    demo_state.reset()
    return AdminActionResponse(
        status="ok",
        message="Database reset to initial demo state (simulated)",
        simulated=True,
    )

