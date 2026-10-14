#!/bin/bash
set -e

echo "🚀 Iniciando despliegue automatizado de Electrovan..."

echo "1️⃣ Deteniendo contenedores actuales..."
docker compose -f electrovan.yml down

echo "2️⃣ Compilando contenedores sin caché..."
docker compose -f electrovan.yml build --no-cache

echo "3️⃣ Levantando servicios en segundo plano..."
docker compose -f electrovan.yml up -d

echo "4️⃣ Esperando a que la API esté lista..."
sleep 5

# Verificación de salud (Health Check)
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/vehicles || echo "000")

if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "✅ ¡Despliegue exitoso! La API responde correctamente (Código 200)."
else
    echo "❌ ¡Atención! La API respondió con el código HTTP: $HTTP_STATUS. Revisa los logs con 'docker compose logs api'."
    exit 1
fi
