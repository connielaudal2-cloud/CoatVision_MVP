import sys
import os
import base64

# Add backend directory to path for imports
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_analyze_endpoint_exists():
    """Test that the analyze endpoint is accessible"""
    # Create a simple 1x1 red image
    import cv2
    import numpy as np
    
    # Create a small test image
    test_image = np.zeros((100, 100, 3), dtype=np.uint8)
    test_image[:, :] = [0, 0, 255]  # Red image
    
    # Encode to PNG and then base64
    _, buffer = cv2.imencode('.png', test_image)
    base64_str = base64.b64encode(buffer).decode('utf-8')
    
    # Test the base64 endpoint
    response = client.post("/api/analyze/base64", json={"image": base64_str})
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "metrics" in data
    assert "cvi" in data["metrics"]
    assert "cqi" in data["metrics"]
    assert "coverage" in data["metrics"]


def test_analyze_missing_image():
    """Test analyze endpoint with missing image field"""
    response = client.post("/api/analyze/base64", json={})
    assert response.status_code == 400
    assert "Missing 'image'" in response.json()["detail"]


def test_analyze_invalid_base64():
    """Test analyze endpoint with invalid base64 data"""
    response = client.post("/api/analyze/base64", json={"image": "not-valid-base64"})
    assert response.status_code == 400


if __name__ == "__main__":
    print("Running analyze tests...")
    test_analyze_endpoint_exists()
    print("✓ test_analyze_endpoint_exists passed")
    test_analyze_missing_image()
    print("✓ test_analyze_missing_image passed")
    test_analyze_invalid_base64()
    print("✓ test_analyze_invalid_base64 passed")
    print("\nAll tests passed!")
