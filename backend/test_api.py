import os
import sys

# Agregar la raíz del repositorio al path para encontrar la carpeta 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.database import Base, engine
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

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
