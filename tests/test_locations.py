import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_locations_pe():
    response = client.get("/locations/?country_code=PE")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("country_code" in loc and loc["country_code"]=="PE" for loc in data)