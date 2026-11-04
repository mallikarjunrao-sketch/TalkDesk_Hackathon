# PULSE API Contract & System Specifications

**Service:** PULSE (Proactive Customer Recovery & Assurance Platform)  
**Version:** 0.2.0
**Status:** Milestone B2 (Complete API Stubs)

---

## 1. Overview & Architectural Principles

PULSE identifies operational failures, supports customer interactions through Talkdesk, coordinates authorized recovery actions, and independently verifies customer outcomes.

### Core Architecture & Flow
1. **Detect & Ingest:** Events from operational subsystems (e.g. payment failures) and Talkdesk interactions are ingested and correlated into **Incidents** and **Cases**.
2. **Context & Diagnosis:** Agents or automated workflows retrieve synthesized context and diagnostic information for a specific customer case or payment failure.
3. **Policy Decision & Resolution Proposal:** Recovery actions (e.g., refunds, credits, gestures) are proposed and evaluated by the Policy Engine. Decisions are constrained by business thresholds.
4. **Human-in-the-Loop Approval:** When required by policy (`NEEDS_APPROVAL`), supervisor or agent approval transitions the commitment to executable status.
5. **Authorized Execution:** An executor triggers the authorized remediation via downstream services (or mock settlement in test modes).
6. **Independent Outcome Verification:** An automated verifier continuously or on-demand verifies that the customer actually received the remediation, preventing unfulfilled promises.

---

## 2. Shared Enums & Fixed Values

### 2.1 Commitment Lifecycle Statuses
These values are fixed by the team API contract and track the lifecycle of a customer commitment:

| Status | Description |
|---|---|
| `PROPOSED` | Resolution/gesture proposed by agent or automated workflow. |
| `APPROVAL_PENDING` | Policy requires human supervisor authorization before execution. |
| `REQUESTED` | Authorized commitment dispatched for execution. |
| `ACKNOWLEDGED` | Downstream processing system acknowledged receipt of the execution request. |
| `AWAITING_VERIFICATION` | Action executed downstream; awaiting independent verification of outcome. |
| `VERIFIED` | Independent verifier confirmed customer has successfully received remediation. |
| `AT_RISK` | SLA target window breached or settlement deadline elapsed without verification. |
| `ESCALATED` | High-priority escalation triggered due to breach, failure, or customer impact. |
| `DENIED` | Commitment denied by policy or supervisor review. |

### 2.2 Policy Decisions
Evaluated by the policy engine to determine authorization path:

| Decision | Meaning |
|---|---|
| `ALLOW` | Auto-approved; within allowable policy limits and eligibility rules. |
| `DENY` | Ineligible or violates hard business rules. |
| `NEEDS_APPROVAL` | Requires human-in-the-loop review/approval (e.g. amount exceeds threshold). |

### 2.3 Field Mappings & Naming Conventions
To ensure seamless integration between external systems (Talkdesk, React UI) and the internal database without breaking existing models:

| Context | External Wire Name | Internal Model Name | Notes |
|---|---|---|---|
| Telemetry Ingest (`/events/ingest`) | `type` | `event_type` | Wire payload uses `type`, mapped internally to `Event.event_type`. |
| Policy Decision (`/resolutions/propose`) | `rule_id` | `rule_name` | Wire response returns `rule_id` (e.g., `"R3"`), mapped from `PolicyDecision.rule_name`. |
| Case Identification (`/resolutions/propose`) | `case_id` or `case_ref` | `case_ref` | Wire request accepts either `case_id` or `case_ref`. |
| Settlement Modes (`/admin/settlement-mode`) | `mode` | `settlement_mode` | Allowed values strictly: `"NOT_FOUND"` or `"FOUND"`. |

---

## 3. Key Business Rules

1. **Independent Verification:** A commitment cannot transition to `VERIFIED` simply because an execution call succeeded. Verification requires independent query of settlement status.
2. **Deterministic State Transitions:**
   - `PROPOSED` &rarr; (if `ALLOW`) &rarr; `REQUESTED` &rarr; `ACKNOWLEDGED` &rarr; `AWAITING_VERIFICATION` &rarr; `VERIFIED`
   - `PROPOSED` &rarr; (if `NEEDS_APPROVAL`) &rarr; `APPROVAL_PENDING` &rarr; (Approved) &rarr; `REQUESTED`
   - `PROPOSED` &rarr; (if `DENY` or supervisor rejected) &rarr; `DENIED`
   - `AWAITING_VERIFICATION` &rarr; (SLA exceeded or failed settlement) &rarr; `AT_RISK` / `ESCALATED`
3. **Audit Trail & Immutability:** All events, decisions, and action dispatches record UTC timestamps and references.
4. **Mock Settlement Toggle:** A configurable settlement mode allows automated testing (`NOT_FOUND` or `FOUND`) to demonstrate recovery flows.

---

## 4. Complete Implemented Endpoint Specifications (Milestone B2)

All endpoints below are fully implemented as typed API stubs in Milestone B2.

### 4.1 System & Health

#### `GET /health`
- **Description:** System health and live SQLite database connectivity probe.
- **Response `200 OK`:**
  ```json
  {
    "status": "ok",
    "service": "PULSE Backend",
    "database": "connected"
  }
  ```
- **Response `503 Service Unavailable`:**
  ```json
  {
    "status": "degraded",
    "service": "PULSE Backend",
    "database": "disconnected"
  }
  ```

---

### 4.2 Customer Cases & Diagnostics

#### `GET /cases/{case_ref}/context`
- **Description:** Fetches synthesized customer profile, operational status, payment mismatch, and open commitments for Talkdesk screen pop.
- **Path Parameters:** `case_ref` (string, e.g. `CASE-2041`)
- **Response `200 OK`:**
  ```json
  {
    "case_ref": "CASE-2041",
    "customer": {
      "customer_id": "CUST-9011",
      "name": "Jane Doe",
      "phone": "+15550192834",
      "email": "jane.doe@example.com"
    },
    "status": "OPEN",
    "payment_ref": "TX-101",
    "incident_id": "INC-0042",
    "open_commitments": [
      {
        "id": "CMT-001",
        "action_type": "REFUND",
        "status": "PROPOSED",
        "amount": 4299.0,
        "currency": "INR"
      }
    ],
    "simulated": true
  }
  ```

#### `GET /payments/{payment_ref}/diagnosis`
- **Description:** Diagnoses payment gateway vs. order system state discrepancies.
- **Path Parameters:** `payment_ref` (string, e.g. `TX-101`)
- **Response `200 OK`:**
  ```json
  {
    "payment_ref": "TX-101",
    "payment_status": "CAPTURED",
    "order_status": "NOT_CREATED",
    "amount": 4299.0,
    "currency": "INR",
    "mismatch": true,
    "incident_id": "INC-0042",
    "simulated": true
  }
  ```

---

### 4.3 Incident Management

#### `GET /incidents/active`
- **Description:** Returns the active operational incident matching the issue type or reference.
- **Query Parameters:**
  - `issue_type` (optional, string)
  - `reference` (optional, string)
- **Response `200 OK`:**
  ```json
  {
    "incident_id": "INC-0042",
    "status": "ACTIVE",
    "issue_type": "PAYMENT_CAPTURED_ORDER_NOT_CREATED",
    "affected_population": 50,
    "contacted_support": 8,
    "public_message": "We are experiencing a payment processing delay where orders may not immediately show as confirmed. Our team is actively resolving this.",
    "simulated": true
  }
  ```

#### `GET /incidents`
- **Description:** Lists all tracked incidents (active, monitoring, resolved).
- **Response `200 OK`:**
  ```json
  [
    {
      "incident_id": "INC-0042",
      "title": "Payment Captured but Order Not Created",
      "status": "ACTIVE",
      "severity": "HIGH",
      "issue_type": "PAYMENT_CAPTURED_ORDER_NOT_CREATED",
      "affected_count": 50,
      "created_at": "2026-11-04T08:00:00Z",
      "simulated": true
    },
    {
      "incident_id": "INC-0038",
      "title": "SMS OTP Gateway Latency",
      "status": "RESOLVED",
      "severity": "LOW",
      "issue_type": "SMS_DELIVERY_DELAY",
      "affected_count": 12,
      "created_at": "2026-11-03T14:00:00Z",
      "simulated": true
    }
  ]
  ```

---

### 4.4 Resolutions & Policy Evaluation

#### `POST /resolutions/propose`
- **Description:** Proposes an operational resolution for a case and queries policy authorization rules.
- **Request `200 OK`:**
  ```json
  {
    "case_id": "CASE-2041",
    "remedy": "REFUND",
    "amount": 4299.0,
    "currency": "INR"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "decision": "ALLOW",
    "rule_id": "R3",
    "commitment_id": "CMT-001",
    "status": "PROPOSED"
  }
  ```

#### `POST /resolutions/execute`
- **Description:** Dispatches an authorized commitment to downstream execution.
- **Request:**
  ```json
  {
    "commitment_id": "CMT-001"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "commitment_id": "CMT-001",
    "action_ref": "RF-8821",
    "status": "ACKNOWLEDGED",
    "customer_message_hint": "Your refund request has been submitted. We are still checking settlement."
  }
  ```

---

### 4.5 Outcome Verification

#### `POST /verification/run`
- **Description:** Queries independent settlement source for commitment fulfillment.
- **Request:**
  ```json
  {
    "commitment_id": "CMT-001"
  }
  ```
- **Response `200 OK` (when settlement mode is `NOT_FOUND`):**
  ```json
  {
    "commitment_id": "CMT-001",
    "settlement": "NOT_FOUND",
    "status": "AT_RISK",
    "evidence": "Refund API accepted; settlement not found."
  }
  ```
- **Response `200 OK` (when settlement mode is `FOUND`):**
  ```json
  {
    "commitment_id": "CMT-001",
    "settlement": "FOUND",
    "status": "VERIFIED",
    "evidence": "Settlement confirmed via mock bank gateway settlement logs."
  }
  ```

---

### 4.6 Commitments Management

#### `GET /commitments`
- **Description:** Lists all commitments with optional status and case filtering.
- **Query Parameters:**
  - `status` (optional, string: `PROPOSED`, `APPROVAL_PENDING`, etc.)
  - `case_ref` (optional, string)
- **Response `200 OK`:**
  ```json
  [
    {
      "id": "CMT-001",
      "case_ref": "CASE-2041",
      "action_type": "REFUND",
      "amount": 4299.0,
      "currency": "INR",
      "status": "PROPOSED",
      "deadline": "2026-11-05T12:00:00Z",
      "incident_id": "INC-0042",
      "evidence": "Refund API accepted; settlement not found.",
      "created_at": "2026-11-04T08:30:00Z",
      "updated_at": "2026-11-04T08:35:00Z",
      "simulated": true
    }
  ]
  ```

#### `GET /commitments/{id}`
- **Description:** Retrieve a single commitment record.
- **Path Parameters:** `id` (string, e.g. `CMT-001`)
- **Response `200 OK`:**
  ```json
  {
    "id": "CMT-001",
    "case_ref": "CASE-2041",
    "action_type": "REFUND",
    "amount": 4299.0,
    "currency": "INR",
    "status": "PROPOSED",
    "deadline": "2026-11-05T12:00:00Z",
    "incident_id": "INC-0042",
    "evidence": null,
    "created_at": "2026-11-04T08:30:00Z",
    "updated_at": "2026-11-04T08:30:00Z",
    "simulated": true
  }
  ```

#### `POST /commitments/{id}/approve`
- **Description:** Human-in-the-loop supervisor approval or rejection.
- **Path Parameters:** `id` (string, e.g. `CMT-001`)
- **Request:**
  ```json
  {
    "supervisor_id": "SUP-101",
    "approved": true,
    "notes": "Goodwill override approved."
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "commitment_id": "CMT-001",
    "status": "REQUESTED",
    "approved": true,
    "approved_by": "SUP-101",
    "message": "Commitment approved and queued for execution.",
    "simulated": true
  }
  ```

---

### 4.7 Telemetry & Ingestion

#### `POST /events/ingest`
- **Description:** Ingests external webhook/telemetry event and performs correlation. Maps incoming `type` to internal `event_type`.
- **Request:**
  ```json
  {
    "type": "PAYMENT_CAPTURED_ORDER_NOT_CREATED",
    "payment_ref": "TX-107",
    "ts": "2026-11-04T10:33:10Z"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "accepted": true,
    "incident_id": "INC-0042",
    "incident_opened": false
  }
  ```

---

### 4.8 Dashboard & Overview

#### `GET /dashboard`
- **Description:** Aggregated operational metrics for frontend overview.
- **Response `200 OK`:**
  ```json
  {
    "incident": {
      "id": "INC-0042",
      "status": "ACTIVE"
    },
    "affected_transactions": 50,
    "contacted_support": 8,
    "commitments_created": 8,
    "verified": 6,
    "awaiting_or_at_risk": 2,
    "simulated": true
  }
  ```

---

### 4.9 Mock External Services

#### `POST /mock/refund`
- **Description:** Simulates payment gateway refund processing.
- **Request:**
  ```json
  {
    "payment_ref": "TX-101",
    "amount": 4299.0,
    "currency": "INR",
    "reason": "Payment captured without order creation"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "status": "ACCEPTED",
    "refund_ref": "RF-8821",
    "payment_ref": "TX-101",
    "amount": 4299.0,
    "simulated": true
  }
  ```

#### `GET /mock/settlement/{refund_ref}`
- **Description:** Simulates banking network settlement inquiry.
- **Path Parameters:** `refund_ref` (string, e.g. `RF-8821`)
- **Response `200 OK` (when mode is `NOT_FOUND`):**
  ```json
  {
    "refund_ref": "RF-8821",
    "settlement": "NOT_FOUND",
    "status": "PENDING",
    "simulated": true
  }
  ```
- **Response `200 OK` (when mode is `FOUND`):**
  ```json
  {
    "refund_ref": "RF-8821",
    "settlement": "FOUND",
    "status": "SETTLED",
    "simulated": true
  }
  ```

---

### 4.10 Demo Administration

#### `POST /admin/settlement-mode`
- **Description:** Sets mock settlement behavior for live hackathon demos.
- **Request:**
  ```json
  {
    "mode": "NOT_FOUND"
  }
  ```
  *(Allowed values strictly: `"NOT_FOUND"`, `"FOUND"`. All others rejected with HTTP 422)*
- **Response `200 OK`:**
  ```json
  {
    "mode": "NOT_FOUND",
    "message": "Settlement mode set to NOT_FOUND",
    "simulated": true
  }
  ```

#### `POST /admin/seed`
- **Description:** Resets/seeds demonstration incidents, cases, and mock transactions.
- **Response `200 OK`:**
  ```json
  {
    "status": "ok",
    "message": "Demo data successfully seeded (simulated)",
    "simulated": true
  }
  ```

#### `POST /admin/reset`
- **Description:** Resets demo state and toggles back to baseline (`NOT_FOUND`).
- **Response `200 OK`:**
  ```json
  {
    "status": "ok",
    "message": "Database reset to initial demo state (simulated)",
    "simulated": true
  }
  ```
