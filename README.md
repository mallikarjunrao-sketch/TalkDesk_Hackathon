# PULSE — Proactive Customer Recovery & Assurance Platform

PULSE is a Proactive Customer Recovery & Assurance Platform built for the Talkdesk Hackathon. It identifies operational failures, supports customer interactions through Talkdesk, coordinates authorized recovery actions, and independently verifies customer outcomes.

---

## Current Milestone: B2 – Complete API Stubs

Milestone B2 provides complete, typed, deterministic API stubs for all 18 agreed system endpoints. This allows:
- **Person A (Integration Lead):** Connect Talkdesk AI Agent tools to live backend endpoints.
- **Person C (Frontend Lead):** Connect the React dashboard and incident views.
- **Person B (Backend Lead):** Incrementally implement real business logic in subsequent milestones.

### Stack
- **Language:** Python 3.13
- **Framework:** FastAPI
- **Database / ORM:** SQLite + SQLModel
- **Validation:** Pydantic
- **Testing:** Pytest, HTTPX

---

## Directory Structure

```text
PULSE/
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore patterns
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── run.ps1                   # PowerShell server runner
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py         # Environment configuration
│   │   ├── database.py       # SQLModel engine & health probe
│   │   ├── main.py           # FastAPI app & router registration
│   │   ├── models/           # SQLModel database tables
│   │   │   ├── __init__.py
│   │   │   ├── action.py
│   │   │   ├── case.py
│   │   │   ├── commitment.py
│   │   │   ├── event.py
│   │   │   ├── incident.py
│   │   │   └── policy_decision.py
│   │   ├── routers/          # Person B-owned API routers (B2 Stubs)
│   │   │   ├── __init__.py
│   │   │   ├── admin.py       # POST /admin/*
│   │   │   ├── cases.py       # GET /cases/{case_ref}/context
│   │   │   ├── commitments.py # GET/POST /commitments/*
│   │   │   ├── dashboard.py   # GET /dashboard
│   │   │   ├── events.py      # POST /events/ingest
│   │   │   ├── incidents.py   # GET /incidents/*
│   │   │   ├── mock.py        # POST /mock/refund, GET /mock/settlement/*
│   │   │   ├── payments.py    # GET /payments/{payment_ref}/diagnosis
│   │   │   ├── resolutions.py # POST /resolutions/*
│   │   │   └── verification.py# POST /verification/run
│   │   ├── schemas/          # Typed Pydantic request/response models
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── cases.py
│   │   │   ├── commitments.py
│   │   │   ├── common.py
│   │   │   ├── dashboard.py
│   │   │   ├── events.py
│   │   │   ├── health.py
│   │   │   ├── incidents.py
│   │   │   ├── mock.py
│   │   │   ├── payments.py
│   │   │   ├── resolutions.py
│   │   │   └── verification.py
│   │   └── services/         # Shared services & demo state
│   │       ├── __init__.py
│   │       └── demo_state.py # Demo controls & mode toggles
│   └── tests/
│       ├── test_health.py    # B1 health probe tests
│       └── test_api_stubs.py # B2 complete API stub tests
└── contracts/
    └── API_CONTRACT.md       # Full API contract with wire/model mappings
```

---

## Team Folder Ownership

- **Backend Lead (Person B):** `backend/app/` (core, models, routers, schemas, services), `backend/tests/`, `contracts/`, `main.py`.
- **Integration Lead (Person A):** `backend/app/talkdesk_adapter/`, `docs/`.
- **Frontend & Incident Correlation Lead (Person C):** `backend/app/incidents/`, `frontend/`, `scripts/`.

---

## Quickstart Guide (PowerShell)

### 1. Create Virtual Environment and Install Dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure Environment

```powershell
Copy-Item .env.example .env
```

### 3. Run Tests

```powershell
$env:PYTHONPATH = "."
.\.venv\Scripts\python.exe -m pytest -v backend/tests/
```

### 4. Start the Backend Server

```powershell
.\run.ps1
```

Or via Uvicorn:

```powershell
$env:PYTHONPATH = "."
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

- Interactive OpenAPI Swagger docs: `http://127.0.0.1:8000/docs`
- ReDoc documentation: `http://127.0.0.1:8000/redoc`

---

## Implemented Endpoints Summary (B2)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | System health & live DB connectivity probe |
| `GET` | `/cases/{case_ref}/context` | Case context, customer info & open commitments |
| `GET` | `/payments/{payment_ref}/diagnosis` | Discrepancy diagnosis between payment & order |
| `GET` | `/incidents/active` | Active operational incident (`INC-0042`) |
| `GET` | `/incidents` | Incident history & operational failures |
| `POST` | `/resolutions/propose` | Policy evaluation & resolution proposal |
| `POST` | `/resolutions/execute` | Remediation execution dispatch |
| `POST` | `/verification/run` | Independent outcome verification |
| `GET` | `/commitments` | List all tracked commitments |
| `GET` | `/commitments/{id}` | Retrieve commitment record by ID |
| `POST` | `/commitments/{id}/approve` | Supervisor approval/rejection |
| `POST` | `/events/ingest` | Telemetry event ingestion (maps `type` &rarr; `event_type`) |
| `GET` | `/dashboard` | Aggregated operational metrics for frontend |
| `POST` | `/mock/refund` | Mock payment gateway refund dispatch |
| `GET` | `/mock/settlement/{refund_ref}` | Mock bank settlement status probe |
| `POST` | `/admin/settlement-mode` | Set settlement mode (`NOT_FOUND` / `FOUND`) |
| `POST` | `/admin/seed` | Seed demo data |
| `POST` | `/admin/reset` | Reset demo state |

Full wire payloads and contract specifications are detailed in [contracts/API_CONTRACT.md](contracts/API_CONTRACT.md).
