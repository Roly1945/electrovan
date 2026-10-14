from fastapi import FastAPI

app = FastAPI(title="Electrovan API")

@app.get("/api/vehicles")
def get_vehicles():
    return []

@app.get("/api/locations")
def get_locations():
    return []

@app.get("/api/reservations")
def get_reservations():
    return []
