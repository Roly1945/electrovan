import re

with open("frontend/admin.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remover cualquier sección previa de locations para evitar duplicados o scripts sueltos
content = re.sub(r'<!-- Sección de Gestión de Lugares de Entrega y Devolución -->[\s\S]*?</script>', '', content)

# 2. Definir el bloque completo y limpio de la sección de lugares con su propio script
locations_block = """
      <!-- Sección de Gestión de Lugares de Entrega y Devolución -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-8">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-lg font-bold text-slate-800">Lugares de Entrega y Devolución</h2>
        </div>
        <form id="locationForm" onsubmit="createLocation(event)" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <input type="text" id="locName" placeholder="Nombre del lugar (Ej. Sucursal Norte)" required class="border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
          <input type="text" id="locCity" placeholder="Ciudad (Ej. Mérida)" required value="Mérida" class="border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
          <button type="submit" class="bg-blue-600 text-white font-bold rounded-xl p-3 text-sm hover:bg-blue-700 transition">Agregar Lugar</button>
        </form>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-slate-200 text-xs text-slate-500 uppercase">
                <th class="py-3 px-4">ID</th>
                <th class="py-3 px-4">Lugar / Sucursal</th>
                <th class="py-3 px-4">Ciudad</th>
                <th class="py-3 px-4">Estado</th>
                <th class="py-3 px-4 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody id="locationsTableBody">
              <!-- Cargado dinámicamente -->
            </tbody>
          </table>
        </div>
      </div>

      <script>
        async function loadLocations() {
          try {
            const res = await fetch("/api/locations");
            const locations = await res.json();
            const tbody = document.getElementById("locationsTableBody");
            if (!tbody) return;
            tbody.innerHTML = "";
            locations.forEach(loc => {
              tbody.innerHTML += `
                <tr class="border-b border-slate-100 text-sm text-slate-700">
                  <td class="py-3 px-4 font-bold">#${loc.id}</td>
                  <td class="py-3 px-4 font-semibold">${loc.name}</td>
                  <td class="py-3 px-4">${loc.city || 'Mérida'}</td>
                  <td class="py-3 px-4"><span class="bg-emerald-100 text-emerald-800 text-xs px-2.5 py-1 rounded-full font-bold">Activo</span></td>
                  <td class="py-3 px-4 text-right">
                    <button onclick="deleteLocation(${loc.id})" class="text-rose-600 hover:text-rose-800 font-bold text-xs bg-rose-50 px-3 py-1.5 rounded-lg">Eliminar</button>
                  </td>
                </tr>
              `;
            });
          } catch (e) {
            console.error("Error cargando lugares:", e);
          }
        }

        async function createLocation(event) {
          event.preventDefault();
          const name = document.getElementById("locName").value;
          const city = document.getElementById("locCity").value;
          try {
            const res = await fetch("/api/locations", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ name, city, active: true })
            });
            if (res.ok) {
              document.getElementById("locationForm").reset();
              loadLocations();
            } else {
              alert("Error al crear el lugar");
            }
          } catch (e) {
            console.error(e);
          }
        }

        async function deleteLocation(id) {
          if (!confirm("¿Estás seguro de eliminar este lugar?")) return;
          try {
            await fetch(`/api/locations/${id}`, { method: "DELETE" });
            loadLocations();
          } catch (e) {
            console.error(e);
          }
        }

        window.addEventListener("DOMContentLoaded", () => {
          loadLocations();
        });
      </script>
"""

# 3. Insertar justo antes del bloque de Reservaciones Recibidas
if "Reservaciones Recibidas" in content:
    content = content.replace('<!-- Reservaciones Recibidas -->', locations_block + '\n\n      <!-- Reservaciones Recibidas -->')
elif "Reservaciones" in content:
    # Búsqueda alternativa por texto común
    pos = content.find("Reservaciones")
    content = content[:pos] + locations_block + "\n\n" + content[pos:]
else:
    # Si no lo encuentra, lo insertamos antes del cierre del body
    content = content.replace("</body>", locations_block + "\n</body>")

with open("frontend/admin.html", "w", encoding="utf-8") as f:
    f.write(content)

print("¡Panel de administración limpiado e injertado correctamente!")
