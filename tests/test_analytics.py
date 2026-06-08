import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_top_locations_pm25():
    response = client.get("/analytics/top?parameter=pm25&top_n=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5
    for entry in data:
        assert "location" in entry and "avg_value" in entry