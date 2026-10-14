with open("backend/main.py", "r", encoding="utf-8") as f:
    code = f.read()

# Remover los bloques mal ubicados de locations si existen
if "# --- MODELOS Y ENDPOINTS DE LOCATIONS ---" in code:
    parts = code.split("# --- MODELOS Y ENDPOINTS DE LOCATIONS ---")
    # Buscar dónde terminan los endpoints de locations y conservar el resto
    rest = parts[1].split("Base.metadata.create_all")
    code = parts[0] + ("Base.metadata.create_all" + rest[1] if len(rest) > 1 else "")

# Nuevo bloque completo y bien ubicado de Locations que se colocará al final (después de app = FastAPI())
locations_block = """

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

# Añadir al final del archivo asegurando que app ya existe
code = code.strip() + locations_block

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(code)

print("¡Backend corregido correctamente!")
