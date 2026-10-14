import os

# 1. ACTUALIZAR BACKEND (main.py) CON CORS PERMISIVO Y VALIDACIÓN ROBUSTA DE JSON
backend_code = """from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://electrovan_user:electrovan_password@db:5432/electrovan_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class VehicleModel(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    model = Column(String)
    category = Column(String)
    autonomy_km = Column(Integer)
    battery_kwh = Column(Integer)
    daily_rate = Column(Float)
    plate = Column(String, default="YXX-452-D")
    year = Column(Integer, default=2024)
    status = Column(String, default="Disponible")

class ClientModel(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)

class ReservationModel(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    pickup_location = Column(String, nullable=True, default="Oficina Principal")
    start_date = Column(String)
    pickup_time = Column(String, nullable=True, default="10:00 AM")
    return_location = Column(String, nullable=True, default="Oficina Principal")
    end_date = Column(String)
    return_time = Column(String, nullable=True, default="10:00 AM")
    days = Column(Integer)
    base_rate = Column(Float)
    chubb_insurance = Column(Float)
    total_price = Column(Float)
    status = Column(String, default="Confirmada")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Electrovan Booking Engine API", version="7.0")

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

class VehicleCreate(BaseModel):
    name: str
    model: str
    category: str
    autonomy_km: int
    battery_kwh: int
    daily_rate: float
    plate: str
    year: int

class VehicleOut(VehicleCreate):
    id: int
    status: str
    class Config:
        from_attributes = True

class ClientCreate(BaseModel):
    full_name: str
    email: str
    phone: str

class ClientOut(ClientCreate):
    id: int
    class Config:
        from_attributes = True

class ReservationCreate(BaseModel):
    client_id: int
    vehicle_id: int
    pickup_location: Optional[str] = "Oficina Principal"
    start_date: str
    pickup_time: Optional[str] = "10:00 AM"
    return_location: Optional[str] = "Oficina Principal"
    end_date: str
    return_time: Optional[str] = "10:00 AM"
    include_chubb: bool = True

class ReservationOut(BaseModel):
    id: int
    client_id: int
    vehicle_id: int
    pickup_location: Optional[str] = "Oficina Principal"
    start_date: str
    pickup_time: Optional[str] = "10:00 AM"
    return_location: Optional[str] = "Oficina Principal"
    end_date: str
    return_time: Optional[str] = "10:00 AM"
    days: int
    base_rate: float
    chubb_insurance: float
    total_price: float
    status: str
    class Config:
        from_attributes = True

class AdminLogin(BaseModel):
    username: str
    password: str

CHUBB_DAILY_FEE = 250.0

@app.get("/api/health")
def health():
    return {"status": "ok", "system": "Electrovan Active"}

@app.get("/api/vehicles", response_model=List[VehicleOut])
def get_vehicles(db: Session = Depends(get_db)):
    return db.query(VehicleModel).all()

@app.post("/api/clients", response_model=ClientOut)
def create_client(c: ClientCreate, db: Session = Depends(get_db)):
    db_c = db.query(ClientModel).filter(ClientModel.email == c.email).first()
    if db_c:
        return db_c
    db_c = ClientModel(**c.dict())
    db.add(db_c)
    db.commit()
    db.refresh(db_c)
    return db_c

@app.post("/api/reservations", response_model=ReservationOut)
def create_reservation(r: ReservationCreate, db: Session = Depends(get_db)):
    vehicle = db.query(VehicleModel).filter(VehicleModel.id == r.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    try:
        d1 = datetime.strptime(r.start_date, "%Y-%m-%d")
        d2 = datetime.strptime(r.end_date, "%Y-%m-%d")
        if d2 <= d1:
            raise HTTPException(status_code=400, detail="La fecha de devolución debe ser posterior a la fecha de recolección")
        days = (d2 - d1).days
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido (YYYY-MM-DD)")

    subtotal_v = vehicle.daily_rate * days
    chubb_total = (CHUBB_DAILY_FEE * days) if r.include_chubb else 0.0
    total = subtotal_v + chubb_total

    db_res = ReservationModel(
        client_id=r.client_id,
        vehicle_id=r.vehicle_id,
        pickup_location=r.pickup_location or "Oficina Principal",
        start_date=r.start_date,
        pickup_time=r.pickup_time or "10:00 AM",
        return_location=r.return_location or "Oficina Principal",
        end_date=r.end_date,
        return_time=r.return_time or "10:00 AM",
        days=days,
        base_rate=subtotal_v,
        chubb_insurance=chubb_total,
        total_price=total,
        status="Confirmada"
    )
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return db_res

@app.post("/api/admin/login")
def admin_login(creds: AdminLogin):
    if creds.username == "admin" and creds.password == "Electrovan2026!":
        return {"authenticated": True, "token": "electrovan-secure-admin-token-2026"}
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

@app.post("/api/vehicles", response_model=VehicleOut)
def create_vehicle(v: VehicleCreate, db: Session = Depends(get_db)):
    db_v = VehicleModel(**v.dict(), status="Disponible")
    db.add(db_v)
    db.commit()
    db.refresh(db_v)
    return db_v

@app.delete("/api/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    v = db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    db.delete(v)
    db.commit()
    return {"status": "success", "message": f"Vehículo #{vehicle_id} eliminado"}

@app.put("/api/vehicles/{vehicle_id}/rate", response_model=VehicleOut)
def update_vehicle_rate(vehicle_id: int, new_rate: float, db: Session = Depends(get_db)):
    v = db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    v.daily_rate = new_rate
    db.commit()
    db.refresh(v)
    return v

@app.put("/api/vehicles/{vehicle_id}/status")
def update_vehicle_status(vehicle_id: int, status_str: str, db: Session = Depends(get_db)):
    v = db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    v.status = status_str
    db.commit()
    return {"status": "success", "vehicle_id": vehicle_id, "new_status": status_str}

@app.get("/api/clients", response_model=List[ClientOut])
def get_clients(db: Session = Depends(get_db)):
    return db.query(ClientModel).all()

@app.get("/api/reservations", response_model=List[ReservationOut])
def get_reservations(db: Session = Depends(get_db)):
    return db.query(ReservationModel).all()

@app.put("/api/reservations/{res_id}/status")
def update_reservation_status(res_id: int, new_status: str, db: Session = Depends(get_db)):
    r = db.query(ReservationModel).filter(ReservationModel.id == res_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    r.status = new_status
    db.commit()
    return {"status": "success", "reservation_id": res_id, "new_status": new_status}
"""

with open("backend/main.py", "w") as f:
    f.write(backend_code)

print("✅ Backend actualizado con soporte CORS universal.")
