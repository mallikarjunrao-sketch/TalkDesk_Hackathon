from backend.app.schemas.admin import SettlementModeEnum


class DemoState:
    """In-memory demo control state for hackathon demonstrations."""
    def __init__(self):
        self.settlement_mode: SettlementModeEnum = SettlementModeEnum.NOT_FOUND

    def set_settlement_mode(self, mode: SettlementModeEnum) -> None:
        self.settlement_mode = mode

    def reset(self) -> None:
        self.settlement_mode = SettlementModeEnum.NOT_FOUND


demo_state = DemoState()

