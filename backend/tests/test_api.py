import os
import sys

# Forzar el directorio actual y el padre al path de Python antes de importar
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from main import app
from fastapi.testclient import TestClient

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
