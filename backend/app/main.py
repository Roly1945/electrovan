from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://electrovan_user:electrovan_password@db:5432/electrovan_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELOS DE BASE DE DATOS ---
class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    range = Column(Integer, nullable=False)
    battery = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    is_offer = Column(Boolean, default=False)

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, default="Mérida")
    active = Column(Boolean, default=True)

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    folio = Column(String, nullable=True)
    client_id = Column(Integer, default=1)
    vehicle_id = Column(Integer, nullable=False)
    pickup_location = Column(String, nullable=False)
    return_location = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    days = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="Confirmada")

# Limpiar y recrear tablas para asegurar que tengan la estructura correcta
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# --- INICIALIZACIÓN DE LA APLICACIÓN FASTAPI ---
app = FastAPI(title="Electrovan API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- SCHEMAS PYDANTIC ---
class VehicleCreate(BaseModel):
    name: str
    range: int
    battery: int
    capacity: int
    price: float
    image_url: str = None

class LocationCreate(BaseModel):
    name: str
    city: str = "Mérida"
    active: bool = True

# --- ENDPOINTS: VEHÍCULOS ---
@app.get("/api/vehicles")
def get_vehicles(db: Session = Depends(get_db)):
    return db.query(Vehicle).all()

@app.post("/api/vehicles")
def create_vehicle(v: VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = Vehicle(**v.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.post("/api/vehicles/{vehicle_id}/toggle-offer")
def toggle_offer(vehicle_id: int, db: Session = Depends(get_db)):
    v = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    v.is_offer = not v.is_offer
    db.commit()
    return v

@app.delete("/api/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    v = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    db.delete(v)
    db.commit()
    return {"ok": True}

# --- ENDPOINTS: LUGARES (LOCATIONS) ---
@app.get("/api/locations")
def get_locations(db: Session = Depends(get_db)):
    return db.query(Location).all()

@app.post("/api/locations")
def create_location(loc: LocationCreate, db: Session = Depends(get_db)):
    db_loc = Location(**loc.dict())
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)
    return db_loc

@app.delete("/api/locations/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_loc = db.query(Location).filter(Location.id == location_id).first()
    if not db_loc:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(db_loc)
    db.commit()
    return {"ok": True}

# --- ENDPOINTS: RESERVACIONES ---
@app.get("/api/reservations")
def get_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()

@app.delete("/api/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    r = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(r)
    db.commit()
    return {"ok": True}
