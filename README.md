# PULSE — Proactive Customer Recovery & Assurance Platform

PULSE is a Proactive Customer Recovery & Assurance Platform built for the Talkdesk Hackathon. It identifies operational failures, supports customer interactions through Talkdesk, coordinates authorized recovery actions, and independently verifies customer outcomes.

---

## Current Milestone: B1 – Backend Foundation

This milestone delivers the initial backend foundation, SQLite database schemas, lifecycle enums, configuration management, health check endpoint with live database verification, and comprehensive test suite.

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
│   │   ├── config.py         # Environment-based configuration
│   │   ├── database.py       # SQLModel engine, session, & health probe
│   │   ├── main.py           # FastAPI app & GET /health endpoint
│   │   ├── models/           # SQLModel table definitions
│   │   │   ├── __init__.py
│   │   │   ├── action.py     # Execution action tracking
│   │   │   ├── case.py       # Customer recovery case
│   │   │   ├── commitment.py # Lifecycle commitment record
│   │   │   ├── event.py      # Ingested operational event
│   │   │   ├── incident.py   # Systemic operational incident
│   │   │   └── policy_decision.py # Policy evaluation record
│   │   ├── schemas/          # Pydantic schemas & shared enums
│   │   │   ├── __init__.py
│   │   │   ├── common.py     # CommitmentStatus & PolicyDecisionEnum
│   │   │   └── health.py     # HealthResponse schema
│   │   └── services/         # Business services (placeholder for B2+)
│   │       └── __init__.py
│   └── tests/
│       └── test_health.py    # Health check & database verification tests
└── contracts/
    └── API_CONTRACT.md       # Team API contract & agreed endpoint specs
```

---

## Team Folder Ownership

- **Backend Lead (Person B):** `backend/app/` (core), `backend/tests/`, `contracts/`, `main.py`, router registration.
- **Integration Lead (Person A):** `backend/app/talkdesk_adapter/`, `docs/`.
- **Frontend & Incident Correlation Lead (Person C):** `backend/app/incidents/`, `frontend/`, `scripts/`.

---

## Quickstart Guide (PowerShell)

### 1. Create Virtual Environment and Install Dependencies

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Upgrade pip and install requirements
pip install -r requirements.txt
```

### 2. Configure Environment

```powershell
Copy-Item .env.example .env
```

### 3. Run Tests

```powershell
$env:PYTHONPATH = "."
pytest -v backend/tests/
```

### 4. Start the Backend Server

```powershell
.\run.ps1
```

Or directly via Uvicorn:

```powershell
$env:PYTHONPATH = "."
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## Endpoints

### Milestone B1
- **`GET /health`**: Live health check with verified database query.
  ```json
  {
    "status": "ok",
    "service": "PULSE Backend",
    "database": "connected"
  }
  ```
- **`GET /docs`**: Interactive Swagger / OpenAPI documentation.
- **`GET /redoc`**: ReDoc alternative API documentation.

Full endpoint contract for upcoming milestones (B2+) is documented in [contracts/API_CONTRACT.md](contracts/API_CONTRACT.md).

