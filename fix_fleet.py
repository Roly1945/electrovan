import urllib.request
import json
import os
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://electrovan_user:electrovan_password@127.0.0.1:5432/electrovan_db"

print("--- 1. INSERTANDO / VERIFICANDO VEHÍCULOS EN POSTGRES ---")
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM vehicles;")).scalar()
        print(f"Vehículos actuales en BD: {count}")
        
        if count == 0:
            vehicles = [
                ("Tesla Model Y", "Long Range 2026", "SUV EV", 533, 75, 1850.0, "YXX-452-D", 2026, "Disponible"),
                ("BYD Seal", "AWD Excellence 2026", "Sedán EV", 520, 82, 1600.0, "ZAB-891-C", 2026, "Disponible"),
                ("Toyota Prius Hybrid", "Premium 2026", "Híbrido HEV", 950, 14, 1100.0, "WTR-312-A", 2026, "Disponible"),
                ("Nissan Leaf", "Tekna 2025", "Compacto EV", 385, 60, 950.0, "XKP-104-B", 2025, "Disponible")
            ]
            for v in vehicles:
                conn.execute(text("""
                    INSERT INTO vehicles (name, model, category, autonomy_km, battery_kwh, daily_rate, plate, year, status)
                    VALUES (:n, :m, :c, :a, :b, :r, :p, :y, :s)
                """), {"n": v[0], "m": v[1], "c": v[2], "a": v[3], "b": v[4], "r": v[5], "p": v[6], "y": v[7], "s": v[8]})
            conn.commit()
            print("✅ 4 vehículos insertados correctamente.")
except Exception as e:
    print("❌ Error de Base de Datos:", e)

