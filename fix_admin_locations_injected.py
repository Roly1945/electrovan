import os

admin_path = "frontend/admin.html"
with open(admin_path, "r", encoding="utf-8") as f:
    content = f.read()

locations_block = """
      <!-- Sección de Gestión de Lugares de Entrega y Devolución -->
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
    const city = document.getElementById("locCity5") ? document.getElementById("locCity5").value : document.getElementById("locCity").value;
    try {
      const res = await fetch("/api/locations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, city: "Mérida", active: true })
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

# Limpiar si ya se había agregado antes parcialmente para evitar duplicados
if "Lugares de Entrega y Devolución" in content:
    # Remover bloque anterior para reinsertar limpio
    parts = content.split("<!-- Sección de Gestión de Lugares de Entrega y Devolución -->")
    content = parts[0]

# Insertar antes de la última etiqueta de cierre body o al final
if "</body>" in content.lower():
    idx = content.lower().rfind("</body>")
    content = content[:idx] + locations_block + "\n" + content[idx:]
else:
    content += "\n" + locations_block

with open(admin_path, "w", encoding="utf-8") as f:
    f.write(content)

print("¡Panel admin.html actualizado correctamente con los lugares!")
