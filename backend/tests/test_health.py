from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from backend.app.database import check_database_connection, init_db
from backend.app.main import app


@pytest.fixture(autouse=True)
def setup_database():
    """Ensure database tables exist before running tests."""
    init_db()
    yield


def test_health_check_success():
    """Test that GET /health returns HTTP 200 with ok and connected database."""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "PULSE Backend"
        assert data["database"] == "connected"


def test_health_check_live_database_query():
    """Test the real database connection query directly."""
    assert check_database_connection() is True


def test_health_check_database_failure():
    """Test that GET /health handles database connectivity failure gracefully."""
    with patch("backend.app.main.check_database_connection", return_value=False):
        with TestClient(app) as client:
            response = client.get("/health")
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "degraded"
            assert data["service"] == "PULSE Backend"
            assert data["database"] == "disconnected"

