# PULSE API Contract & System Specifications

**Service:** PULSE (Proactive Customer Recovery & Assurance Platform)  
**Version:** 0.1.0  
**Status:** B1 Milestone Base (Foundation)  

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

---

## 3. Key Business Rules

1. **Independent Verification:** A commitment cannot transition to `VERIFIED` simply because an execution call succeeded. Verification requires independent query of settlement status.
2. **Deterministic State Transitions:**
   - `PROPOSED` &rarr; (if `ALLOW`) &rarr; `REQUESTED` &rarr; `ACKNOWLEDGED` &rarr; `AWAITING_VERIFICATION` &rarr; `VERIFIED`
   - `PROPOSED` &rarr; (if `NEEDS_APPROVAL`) &rarr; `APPROVAL_PENDING` &rarr; (Approved) &rarr; `REQUESTED`
   - `PROPOSED` &rarr; (if `DENY` or supervisor rejected) &rarr; `DENIED`
   - `AWAITING_VERIFICATION` &rarr; (SLA exceeded or failed settlement) &rarr; `AT_RISK` / `ESCALATED`
3. **Audit Trail & Immutability:** All events, decisions, and action dispatches record UTC timestamps and references.
4. **Mock Settlement Toggle:** A configurable settlement mode allows automated testing (instant settlement, delayed settlement, or failed settlement) to demonstrate recovery flows.

---

## 4. Complete Agreed API Endpoints Specification

### Implemented in B1 (Foundation)

#### `GET /health`
- **Description:** System health and database connectivity probe.
- **Query Params:** None
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

### Future Endpoints (Milestones B2+)

#### Diagnostics & Case Context
- **`GET /cases/{case_ref}/context`**
  - **Purpose:** Fetches synthesized case context for Talkdesk screen pop / agent assistance.
  - **Returns:** Customer details, linked incidents, recent interactions, and active commitments.

- **`GET /payments/{payment_ref}/diagnosis`**
  - **Purpose:** Diagnoses a failed payment transaction, error codes, and suggested remediation.

#### Incidents
- **`GET /incidents/active`**
  - **Purpose:** List ongoing active operational incidents correlated across customers.
- **`GET /incidents`**
  - **Purpose:** Paginated list of all incidents (active and resolved).

#### Resolutions & Policy Engine
- **`POST /resolutions/propose`**
  - **Purpose:** Proposes a resolution (e.g., refund or goodwill credit) for a case. Evaluates policy (`ALLOW`, `DENY`, `NEEDS_APPROVAL`).
  - **Request Body:** `{ "case_ref": "CASE-1001", "action_type": "REFUND", "amount": 49.99, "currency": "USD", "reason": "System outage" }`

- **`POST /resolutions/execute`**
  - **Purpose:** Dispatches an approved resolution to the executor service. Transitions status to `REQUESTED`.

#### Commitments Management
- **`GET /commitments`**
  - **Purpose:** List all commitments with optional status, case_ref, or date filtering.
- **`GET /commitments/{id}`**
  - **Purpose:** Retrieve status and history of a single commitment.
- **`POST /commitments/{id}/approve`**
  - **Purpose:** Human-in-the-loop endpoint for supervisor to approve or reject a commitment in `APPROVAL_PENDING`.

#### Verification Engine
- **`POST /verification/run`**
  - **Purpose:** Triggers verification checks across all pending commitments or a specific commitment. Updates statuses to `VERIFIED` or `AT_RISK`.

#### Telemetry & Ingestion
- **`POST /events/ingest`**
  - **Purpose:** Ingests external events (Talkdesk webhooks, payment failure notifications, mock alerts).

#### Dashboard & Reporting
- **`GET /dashboard`**
  - **Purpose:** Aggregated metrics for frontend overview (active incidents, pending approvals, SLA compliance, verified recoveries).

#### Mock Services & Test Harness
- **`POST /mock/refund`**
  - **Purpose:** Simulates third-party payment gateway refund processing.
- **`GET /mock/settlement/{refund_ref}`**
  - **Purpose:** Mock bank/gateway endpoint queried by the independent verifier.
- **`POST /admin/settlement-mode`**
  - **Purpose:** Configure mock behavior (`instant`, `delayed`, `fail`).
- **`POST /admin/seed`**
  - **Purpose:** Seeds demo incidents, cases, and test customers.
- **`POST /admin/reset`**
  - **Purpose:** Resets database state for clean demo restarts.

