import os

admin_path = "frontend/admin.html"
with open(admin_path, "r", encoding="utf-8") as f:
    html = f.read()

# Limpiar cualquier bloque anterior de locations para evitar duplicados o mal posicionamiento
if "<!-- Sección de Gestión de Lugares de Entrega y Devolución -->" in html:
    # Cortar desde el inicio del bloque hasta el cierre del script de locations
    parts = html.split("<!-- Sección de Gestión de Lugares de Entrega y Devolución -->")
    # Tomar la primera parte y buscar dónde terminaba el script asociado para conservar el resto
    rest_parts = parts[1].split("</script>")
    html = parts[0] + ("</script>".join(rest_parts[1:]) if len(rest_parts) > 1 else "")

locations_section = """
      <!-- Sección de Gestión de Lugares de Entrega y Devolución -->
      <div class="bg-white/10 backdrop-blur-md rounded-2xl shadow-lg border border-white/10 p-6 mb-8 text-white">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-lg font-bold text-white">Lugares de Entrega y Devolución</h2>
        </div>
        <form id="locationForm" onsubmit="createLocation(event)" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <input type="text" id="locName" placeholder="Nombre del lugar (Ej. Sucursal Norte)" required class="bg-slate-900/60 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-400">
          <input type="text" id="locCity" placeholder="Ciudad (Ej. Mérida)" required value="Mérida" class="bg-slate-900/60 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-400">
          <button type="submit" class="bg-blue-600 text-white font-bold rounded-xl p-3 text-sm hover:bg-blue-500 transition shadow-lg">Agregar Lugar</button>
        </form>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-slate-700 text-xs text-slate-400 uppercase">
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
                <tr class="border-b border-slate-800/60 text-sm text-slate-200">
                  <td class="py-3 px-4 font-bold">#${loc.id}</td>
                  <td class="py-3 px-4 font-semibold">${loc.name}</td>
                  <td class="py-3 px-4">${loc.city || 'Mérida'}</td>
                  <td class="py-3 px-4"><span class="bg-emerald-500/20 text-emerald-400 text-xs px-2.5 py-1 rounded-full font-bold">Activo</span></td>
                  <td class="py-3 px-4 text-right">
                    <button onclick="deleteLocation(${loc.id})" class="text-rose-400 hover:text-rose-300 font-bold text-xs bg-rose-500/10 px-3 py-1.5 rounded-lg">Eliminar</button>
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

# Insertar justo antes del contenedor de "Reservaciones Recibidas" para que quede perfectamente ubicado en medio
target_marker = '<!-- Reservaciones Recibidas -->' # o buscamos "Reservaciones Recibidas"
if "Reservaciones Recibidas" in html:
    parts = html.split("Reservaciones Recibidas")
    # Buscamos el inicio del bloque contenedor anterior
    html = parts[0] + locations_section + "\n\n      <!-- Reservaciones Recibidas -->" + parts[1]
else:
    # Si no encuentra el marcador exacto, lo ponemos antes del cierre body
    idx = html.rfind("</body>")
    html = html[:idx] + locations_section + "\n" + html[idx:]

with open(admin_path, "w", encoding="utf-8") as f:
    f.write(html)

print("¡Sección de lugares posicionada correctamente en el panel admin!")
