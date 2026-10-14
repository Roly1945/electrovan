import os
import sys

# Forzar el directorio actual y el padre al path de Python antes de importar
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, Base, get_db
from fastapi.testclient import TestClient

# Configuración de SQLite en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobrescribir la dependencia get_db para que use SQLite en memoria
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Fixture para crear y destruir las tablas automáticamente en cada ejecución
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
