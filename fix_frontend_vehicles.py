with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Verificamos si existe el elemento vehicleSelect o agregamos un contenedor seguro para la flota
# Si el script busca vehicleSelect, aseguramos que exista o adaptamos la función para evitar el bloqueo.
print("Revisando estructura del frontend...")
