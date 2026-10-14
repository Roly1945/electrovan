import os

main_path = "backend/main.py"
with open(main_path, "r", encoding="utf-8") as f:
    code = f.read()

# Verificar si ya tiene el modelo de Location
if "class Location" not in code:
    location_code = """
# --- MODELOS Y ENDPOINTS DE LOCATIONS ---
class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
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

@app.delete("/api/locations/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_loc = db.query(Location).filter(Location.id == location_id).first()
    if not db_loc:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(db_loc)
    db.commit()
    return {"ok": True}
"""
    # Insertar antes de Base.metadata.create_all
    if "Base.metadata.create_all" in code:
        code = code.replace("Base.metadata.create_all(bind=engine)", location_code + "\n\nBase.metadata.create_all(bind=engine)")
    else:
        code += "\n" + location_code

    with open(main_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("¡Backend actualizado con soporte para Locations!")
else:
    print("El backend ya cuenta con el modelo de Locations.")
