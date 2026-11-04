"""
PULSE Incident Correlator Module
Owned by: Person C (Incident, Frontend and QA Lead)

Specification from PULSE Coordination Plan (Section 6 & Task C4):
- Signature: PAYMENT_CAPTURED_ORDER_NOT_CREATED
- Sliding time window: 120 seconds (configurable)
- Threshold: >= 5 events within sliding window triggers active incident
- Maintains affected payment references (deduplicated)
- Updates active incident on subsequent events
- Provides Talkdesk GUIDE query support (GET /incidents/active?issue_type=&reference=)
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Set, Tuple, Dict, Any


DEFAULT_SIGNATURE = "PAYMENT_CAPTURED_ORDER_NOT_CREATED"
DEFAULT_WINDOW_SECONDS = 120
DEFAULT_THRESHOLD = 5
DEFAULT_INCIDENT_ID = "INC-0042"
DEFAULT_PUBLIC_MESSAGE = "We are aware of a payment-processing issue affecting some recent orders."


@dataclass
class IngestedEvent:
    type: str
    payment_ref: str
    ts: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IngestedEvent":
        ts_val = data.get("ts")
        if isinstance(ts_val, str):
            try:
                # Handle ISO timestamps with Z or offset
                ts_clean = ts_val.replace("Z", "+00:00")
                parsed_ts = datetime.fromisoformat(ts_clean)
            except Exception:
                parsed_ts = datetime.now(timezone.utc)
        elif isinstance(ts_val, datetime):
            parsed_ts = ts_val
        else:
            parsed_ts = datetime.now(timezone.utc)

        return cls(
            type=data.get("type", ""),
            payment_ref=data.get("payment_ref", ""),
            ts=parsed_ts,
        )


@dataclass
class CorrelatedIncident:
    id: str
    status: str
    signature: str
    started_at: str
    affected_payment_refs: List[str] = field(default_factory=list)
    contacted_count: int = 8
    public_message: str = DEFAULT_PUBLIC_MESSAGE

    @property
    def affected_count(self) -> int:
        return len(self.affected_payment_refs)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status,
            "signature": self.signature,
            "started_at": self.started_at,
            "affected_count": self.affected_count,
            "contacted_count": self.contacted_count,
            "public_message": self.public_message,
            "affected_payment_refs": self.affected_payment_refs,
        }


class IncidentCorrelator:
    def __init__(
        self,
        signature: str = DEFAULT_SIGNATURE,
        window_seconds: int = DEFAULT_WINDOW_SECONDS,
        threshold: int = DEFAULT_THRESHOLD,
        incident_id: str = DEFAULT_INCIDENT_ID,
    ):
        self.signature = signature
        self.window_seconds = window_seconds
        self.threshold = threshold
        self.incident_id = incident_id

        # Ingested events history: list of IngestedEvent
        self.events: List[IngestedEvent] = []
        # Active incident instance
        self.active_incident: Optional[CorrelatedIncident] = None
        # Set of unique affected payment refs
        self._affected_refs: Set[str] = set()

    def reset(self):
        """Reset correlator state back to start of demo."""
        self.events.clear()
        self.active_incident = None
        self._affected_refs.clear()

    def _prune_window(self, current_time: datetime) -> List[IngestedEvent]:
        """Returns matching events within the sliding time window."""
        cutoff = current_time - timedelta(seconds=self.window_seconds)
        # Filter matching signature within window
        return [
            e for e in self.events
            if e.type == self.signature and e.ts >= cutoff
        ]

    def ingest(self, event_data: Any) -> Tuple[bool, Optional[CorrelatedIncident], bool]:
        """
        Ingests an operational event.
        Returns:
            (accepted: bool, active_incident: Optional[CorrelatedIncident], incident_opened: bool)
        """
        if isinstance(event_data, dict):
            event = IngestedEvent.from_dict(event_data)
        elif isinstance(event_data, IngestedEvent):
            event = event_data
        else:
            return False, self.active_incident, False

        self.events.append(event)
        incident_just_opened = False

        # Check if matching signature
        if event.type == self.signature:
            if event.payment_ref:
                self._affected_refs.add(event.payment_ref)

            recent_matching = self._prune_window(event.ts)

            if len(recent_matching) >= self.threshold:
                if self.active_incident is None:
                    # Open new incident!
                    self.active_incident = CorrelatedIncident(
                        id=self.incident_id,
                        status="ACTIVE",
                        signature=self.signature,
                        started_at=recent_matching[0].ts.isoformat(),
                        affected_payment_refs=sorted(list(self._affected_refs)),
                    )
                    incident_just_opened = True
                else:
                    # Update existing incident
                    self.active_incident.affected_payment_refs = sorted(list(self._affected_refs))

        return True, self.active_incident, incident_just_opened

    def get_active_incident(
        self,
        issue_type: Optional[str] = None,
        reference: Optional[str] = None
    ) -> Optional[CorrelatedIncident]:
        """
        Used by GET /incidents/active?issue_type=&reference=
        Checks if active incident exists and matches reference or issue type.
        """
        if not self.active_incident or self.active_incident.status != "ACTIVE":
            return None

        # If reference is provided (e.g. TX-101), check if it's affected or matching
        if reference:
            if reference in self.active_incident.affected_payment_refs:
                return self.active_incident

        # If issue type matches signature or no filter, return active incident
        if not issue_type or issue_type == self.signature or issue_type == "PAYMENT_ORDER_MISMATCH":
            return self.active_incident

        return None


# Global singleton instance for easy import by FastAPI app
correlator_instance = IncidentCorrelator()
