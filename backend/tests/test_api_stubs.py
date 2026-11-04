import pytest
from fastapi.testclient import TestClient
from backend.app.database import init_db
from backend.app.main import app
from backend.app.schemas.common import CommitmentStatus, PolicyDecisionEnum
from backend.app.services.demo_state import demo_state


@pytest.fixture(autouse=True)
def setup_test_env():
    """Initialize DB and reset demo state before each test."""
    init_db()
    demo_state.reset()
    yield
    demo_state.reset()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


# 1. Customer Context
def test_get_case_context(client):
    response = client.get("/cases/CASE-2041/context")
    assert response.status_code == 200
    data = response.json()
    assert data["case_ref"] == "CASE-2041"
    assert data["status"] == "OPEN"
    assert data["customer"]["name"] == "Jane Doe"
    assert data["payment_ref"] == "TX-101"
    assert data["incident_id"] == "INC-0042"
    assert len(data["open_commitments"]) > 0
    assert data["open_commitments"][0]["id"] == "CMT-001"
    assert data["simulated"] is True


# 2. Payment Diagnosis
def test_get_payment_diagnosis_tx_101(client):
    response = client.get("/payments/TX-101/diagnosis")
    assert response.status_code == 200
    data = response.json()
    assert data["payment_ref"] == "TX-101"
    assert data["payment_status"] == "CAPTURED"
    assert data["order_status"] == "NOT_CREATED"
    assert data["amount"] == 4299
    assert data["currency"] == "INR"
    assert data["mismatch"] is True
    assert data["incident_id"] == "INC-0042"
    assert data["simulated"] is True


# 3. Active Incident
def test_get_active_incident(client):
    response = client.get("/incidents/active?issue_type=PAYMENT_CAPTURED_ORDER_NOT_CREATED&reference=TX-101")
    assert response.status_code == 200
    data = response.json()
    assert data["incident_id"] == "INC-0042"
    assert data["status"] == "ACTIVE"
    assert data["affected_population"] == 50
    assert data["contacted_support"] == 8
    assert "payment processing delay" in data["public_message"]
    assert data["simulated"] is True


# 4. Incident Listing
def test_list_incidents(client):
    response = client.get("/incidents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["incident_id"] == "INC-0042"
    assert data[0]["status"] == "ACTIVE"
    assert data[0]["simulated"] is True


# 5. Resolution Proposal
def test_propose_resolution(client):
    payload = {
        "case_id": "CASE-2041",
        "remedy": "REFUND",
        "amount": 4299,
    }
    response = client.post("/resolutions/propose", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == PolicyDecisionEnum.ALLOW.value
    assert data["rule_id"] == "R3"
    assert data["commitment_id"] == "CMT-001"
    assert data["status"] == CommitmentStatus.PROPOSED.value


def test_propose_resolution_validation_error(client):
    """Missing case_id/case_ref and remedy should fail with 422."""
    response = client.post("/resolutions/propose", json={})
    assert response.status_code == 422


# 6. Resolution Execution
def test_execute_resolution(client):
    payload = {"commitment_id": "CMT-001"}
    response = client.post("/resolutions/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["commitment_id"] == "CMT-001"
    assert data["action_ref"] == "RF-8821"
    assert data["status"] == CommitmentStatus.ACKNOWLEDGED.value
    assert "submitted" in data["customer_message_hint"]


# 7. Verification
def test_verification_run_default_not_found(client):
    payload = {"commitment_id": "CMT-001"}
    response = client.post("/verification/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["commitment_id"] == "CMT-001"
    assert data["settlement"] == "NOT_FOUND"
    assert data["status"] == CommitmentStatus.AT_RISK.value
    assert "Refund API accepted" in data["evidence"]


# 8. Commitments Listing and Detail
def test_get_commitments_list(client):
    response = client.get("/commitments")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["id"] == "CMT-001"
    assert data[0]["status"] == CommitmentStatus.PROPOSED.value
    assert data[0]["simulated"] is True


def test_get_commitment_by_id(client):
    response = client.get("/commitments/CMT-001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "CMT-001"
    assert data["case_ref"] == "CASE-2041"
    assert data["amount"] == 4299.0
    assert data["currency"] == "INR"
    assert data["status"] == CommitmentStatus.PROPOSED.value
    assert data["incident_id"] == "INC-0042"


# 9. Supervisor Approval
def test_approve_commitment(client):
    payload = {
        "supervisor_id": "SUP-101",
        "approved": True,
        "notes": "Goodwill override approved.",
    }
    response = client.post("/commitments/CMT-001/approve", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["commitment_id"] == "CMT-001"
    assert data["status"] == CommitmentStatus.REQUESTED.value
    assert data["approved"] is True
    assert data["approved_by"] == "SUP-101"
    assert data["simulated"] is True


def test_deny_commitment(client):
    payload = {
        "supervisor_id": "SUP-101",
        "approved": False,
        "notes": "Policy limits exceeded.",
    }
    response = client.post("/commitments/CMT-001/approve", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["commitment_id"] == "CMT-001"
    assert data["status"] == CommitmentStatus.DENIED.value
    assert data["approved"] is False


# 10. Event Ingestion
def test_ingest_event(client):
    payload = {
        "type": "PAYMENT_CAPTURED_ORDER_NOT_CREATED",
        "payment_ref": "TX-107",
        "ts": "2026-11-04T10:33:10Z",
    }
    response = client.post("/events/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["accepted"] is True
    assert data["incident_id"] == "INC-0042"
    assert data["incident_opened"] is False


# 11. Dashboard
def test_get_dashboard(client):
    response = client.get("/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["incident"]["id"] == "INC-0042"
    assert data["incident"]["status"] == "ACTIVE"
    assert data["affected_transactions"] == 50
    assert data["contacted_support"] == 8
    assert data["commitments_created"] == 8
    assert data["verified"] == 6
    assert data["awaiting_or_at_risk"] == 2
    assert data["simulated"] is True


# 12. Mock Refund
def test_mock_refund(client):
    payload = {
        "payment_ref": "TX-101",
        "amount": 4299,
        "reason": "Payment captured without order creation",
    }
    response = client.post("/mock/refund", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ACCEPTED"
    assert data["refund_ref"] == "RF-8821"
    assert data["payment_ref"] == "TX-101"
    assert data["amount"] == 4299.0
    assert data["simulated"] is True


# 13. Mock Settlement Query
def test_mock_settlement_default(client):
    response = client.get("/mock/settlement/RF-8821")
    assert response.status_code == 200
    data = response.json()
    assert data["refund_ref"] == "RF-8821"
    assert data["settlement"] == "NOT_FOUND"
    assert data["status"] == "PENDING"
    assert data["simulated"] is True


# 14. Demo Admin Controls & Toggle Verification
def test_admin_settlement_mode_toggle(client):
    # Set to FOUND
    response = client.post("/admin/settlement-mode", json={"mode": "FOUND"})
    assert response.status_code == 200
    assert response.json()["mode"] == "FOUND"

    # Verify mock settlement reflects FOUND
    settle_resp = client.get("/mock/settlement/RF-8821")
    assert settle_resp.json()["settlement"] == "FOUND"
    assert settle_resp.json()["status"] == "SETTLED"

    # Verify verification/run reflects FOUND -> VERIFIED
    verify_resp = client.post("/verification/run", json={"commitment_id": "CMT-001"})
    assert verify_resp.json()["settlement"] == "FOUND"
    assert verify_resp.json()["status"] == CommitmentStatus.VERIFIED.value

    # Reset
    reset_resp = client.post("/admin/reset")
    assert reset_resp.status_code == 200

    # Verify returned to NOT_FOUND
    settle_resp2 = client.get("/mock/settlement/RF-8821")
    assert settle_resp2.json()["settlement"] == "NOT_FOUND"


def test_admin_settlement_mode_invalid_rejected(client):
    """Invalid mode should be strictly rejected with HTTP 422."""
    response = client.post("/admin/settlement-mode", json={"mode": "INVALID_MODE"})
    assert response.status_code == 422


def test_admin_seed(client):
    response = client.post("/admin/seed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "seeded" in data["message"]
    assert data["simulated"] is True

