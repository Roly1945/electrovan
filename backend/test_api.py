from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_vehicles():
    response = client.get("/api/vehicles")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_locations():
    response = client.get("/api/locations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_reservations():
    response = client.get("/api/reservations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
