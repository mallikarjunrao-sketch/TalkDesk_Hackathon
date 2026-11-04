# PULSE Incident Correlator Module

**Owner:** Person C (Incident, Frontend & QA Lead)  
**Contract Reference:** Section 6 (`POST /events/ingest`, `GET /incidents/active`, `GET /incidents`, `GET /dashboard`)

---

## How Person B Wires This Into FastAPI (`backend/app/main.py`)

You can import and use the singleton `correlator_instance` directly:

```python
from app.incidents import correlator_instance

# 1. Ingest event endpoint (POST /events/ingest)
@app.post("/events/ingest")
async def ingest_event(payload: dict):
    accepted, incident, opened = correlator_instance.ingest(payload)
    return {
        "accepted": accepted,
        "incident_id": incident.id if incident else None,
        "incident_opened": opened,
    }

# 2. Talkdesk GUIDE active incident lookup (GET /incidents/active)
@app.get("/incidents/active")
async def get_active_incident(issue_type: str = None, reference: str = None):
    inc = correlator_instance.get_active_incident(issue_type=issue_type, reference=reference)
    if not inc:
        return {"active": False, "incident": None}
    return {
        "active": True,
        "incident_id": inc.id,
        "status": inc.status,
        "affected": inc.affected_count,
        "contacted_support": inc.contacted_count,
        "public_message": inc.public_message,
    }

# 3. All incidents for dashboard (GET /incidents)
@app.get("/incidents")
async def get_incidents():
    inc = correlator_instance.get_active_incident()
    return [inc.to_dict()] if inc else []

# 4. Reset hook (called inside POST /admin/reset)
correlator_instance.reset()
```

## Running Unit Tests
```bash
python -m unittest backend/app/incidents/test_correlator.py
```
Tests pass all 4 cases defined in Section 7 (Task C4).
