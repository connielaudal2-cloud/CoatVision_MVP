import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_jobs_crud():
    # List initially empty
    r = client.get("/api/jobs/")
    assert r.status_code == 200
    assert r.json()["jobs"] == []

    # Create job (no admin token required in demo)
    job = {"name": "Test Job"}
    r = client.post("/api/jobs/", json=job)
    assert r.status_code == 200
    created = r.json()["job"]
    assert created["name"] == "Test Job"
    assert created["id"].startswith("job_")

    # Get job
    r = client.get(f"/api/jobs/{created['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created["id"]
