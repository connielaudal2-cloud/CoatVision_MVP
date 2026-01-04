import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_report_status():
    r = client.get("/api/report/status")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "/api/report/demo" in data["demo_endpoint"]

