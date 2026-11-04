from enum import Enum


class CommitmentStatus(str, Enum):
    """Agreed lifecycle statuses for commitments."""
    PROPOSED = "PROPOSED"
    APPROVAL_PENDING = "APPROVAL_PENDING"
    REQUESTED = "REQUESTED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    AWAITING_VERIFICATION = "AWAITING_VERIFICATION"
    VERIFIED = "VERIFIED"
    AT_RISK = "AT_RISK"
    ESCALATED = "ESCALATED"
    DENIED = "DENIED"


class PolicyDecisionEnum(str, Enum):
    """Agreed policy evaluation decisions."""
    ALLOW = "ALLOW"
    DENY = "DENY"
    NEEDS_APPROVAL = "NEEDS_APPROVAL"

