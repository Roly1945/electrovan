import os
admin_path = "frontend/admin.html"
if not os.path.exists(admin_path):
    # Buscar si está en otra ruta
    for root, dirs, files in os.walk("."):
        if "admin.html" in files:
            admin_path = os.path.join(root, "admin.html")

with open(admin_path, "r", encoding="utf-8") as f:
    admin_html = f.read()

# Añadir pestaña o sección de Lugares en el panel de administración
locations_ui = """
      <!-- Sección de Gestión de Lugares de Entrega -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-8">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-lg font-bold text-slate-800">Lugares de Entrega y Devolución</h2>
        </div>
        <form id="locationForm" onsubmit="createLocation(event)" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <input type="text" id="locName" placeholder="Nombre del lugar (Ej. Aeropuerto Internacional)" required class="border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
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
"""

script_logic = """
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

  // Cargar al iniciar
  window.addEventListener("DOMContentLoaded", () => {
    loadLocations();
  });
</script>
"""

if "locationsTableBody" not in admin_html:
    # Insertar antes del cierre de body
    admin_html = admin_html.replace("</body>", locations_ui + "\n" + script_logic + "\n</body>")
    with open(admin_path, "w", encoding="utf-8") as f:
        f.write(admin_html)
    print("¡Panel de administración actualizado con la gestión de lugares!")

