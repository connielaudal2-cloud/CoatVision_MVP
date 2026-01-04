import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_analyze_base64_missing_image():
    r = client.post("/api/analyze/base64", json={})
    assert r.status_code == 400
    assert "Missing 'image'" in r.json()["detail"]
