import os

# 1. Actualizar el modelo y rutas en app/main.py o backend
main_path = "backend/app/main.py"
if not os.path.exists(main_path):
    main_path = "app/main.py"

with open(main_path, "r", encoding="utf-8") as f:
    code = f.read()

# Agregamos el modelo y los endpoints si no existen
location_code = """
class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    city = Column(String, default="Mérida")
    active = Column(Boolean, default=True)

class LocationCreate(BaseModel):
    name: str
    city: Optional[str] = "Mérida"
    active: Optional[bool] = True

@app.get("/api/locations")
def get_locations(db: Session = Depends(get_db)):
    return db.query(Location).all()

@app.post("/api/locations")
def create_location(loc: LocationCreate, db: Session = Depends(get_db)):
    db_loc = Location(name=loc.name, city=loc.city, active=loc.active)
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)
    return db_loc

@app.delete("/api/locations/{loc_id}")
def delete_location(loc_id: int, db: Session = Depends(get_db)):
    db_loc = db.query(Location).filter(Location.id == loc_id).first()
    if not db_loc:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(db_loc)
    db.commit()
    return {"message": "Location deleted successfully"}
"""

if "class Location" not in code:
    # Insertar antes de Base.metadata.create_all o al final
    code = code.replace("Base.metadata.create_all(bind=engine)", location_code + "\n\nBase.metadata.create_all(bind=engine)")
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("¡Modelo y rutas de locations agregados al backend!")

