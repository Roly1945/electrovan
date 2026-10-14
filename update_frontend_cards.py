with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Agregamos la sección de tarjetas de vehículos justo después del bloque de reserva y antes del script
cards_container_html = """
<!-- Sección de Tarjetas de Flota Seleccionable -->
<div class="max-w-5xl mx-auto my-8 space-y-4">
  <div class="flex items-center justify-between">
    <h3 class="text-xl font-black text-slate-800 tracking-wide">2. Selecciona tu Vehículo</h3>
    <span class="text-xs font-bold text-slate-400 uppercase">Elige una opción para continuar</span>
  </div>
  <div id="vehiclesGrid" class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <div class="col-span-3 text-center py-8 text-slate-400 font-medium">Cargando flota disponible...</div>
  </div>
</div>
<!-- Input oculto para mantener compatibilidad con la lógica de reserva del ID de vehículo -->
<input type="hidden" id="vehicleSelect" value="">
"""

# Script actualizado para renderizar las tarjetas y manejar la selección visual
new_script = """
<script>
function adjustCount(elementId, delta) {
  const el = document.getElementById(elementId);
  if (!el) return;
  let val = parseInt(el.innerText) + delta;
  if (elementId === "adultsCount" && val < 1) val = 1;
  if (elementId === "childrenCount" && val < 0) val = 0;
  el.innerText = val;
}

let selectedVehicleId = null;

async function loadVehiclesGrid() {
  try {
    const res = await fetch("/api/vehicles");
    if (!res.ok) throw new Error("Error al obtener la flota");
    const vehicles = await res.json();
    const grid = document.getElementById("vehiclesGrid");
    
    if (!vehicles || vehicles.length === 0) {
      grid.innerHTML = '<div class="col-span-3 text-center py-8 text-slate-400">No hay vehículos disponibles en este momento.</div>';
      return;
    }

    grid.innerHTML = vehicles.map(v => `
      <div onclick="selectVehicle(${v.id}, this)" class="vehicle-card bg-white rounded-2xl p-5 border-2 border-slate-200 shadow-sm hover:shadow-lg transition cursor-pointer relative group flex flex-col justify-between">
        ${v.is_offer ? '<span class="absolute top-3 right-3 bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded-full uppercase tracking-wider">🔥 Oferta</span>' : ''}
        <div>
          <h4 class="font-black text-slate-800 text-lg mb-1">${v.name}</h4>
          <div class="text-xs text-slate-500 space-y-1 my-3">
            <div class="flex items-center gap-1.5">⚡ Autonomía: <strong class="text-slate-700">${v.autonomy_km} km</strong></div>
            <div class="flex items-center gap-1.5">🔋 Batería: <strong class="text-slate-700">${v.battery_kwh} kWh</strong></div>
            <div class="flex items-center gap-1.5">👥 Capacidad: <strong class="text-slate-700">${v.capacity || 5} Pax</strong></div>
          </div>
        </div>
        <div class="pt-4 border-t border-slate-100 flex items-center justify-between mt-2">
          <div>
            <span class="text-[10px] uppercase font-bold text-slate-400 block">Tarifa diaria</span>
            <span class="text-xl font-black text-amber-500">$${v.daily_rate} <span class="text-xs font-normal text-slate-500">MXN</span></span>
          </div>
          <div class="select-indicator w-8 h-8 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center font-bold text-sm">
            ✓
          </div>
        </div>
      </div>
    `).join("");
  } catch (err) {
    console.error(err);
    document.getElementById("vehiclesGrid").innerHTML = '<div class="col-span-3 text-center py-8 text-red-400">Error al cargar la flota de vehículos.</div>';
  }
}

function selectVehicle(id, element) {
  selectedVehicleId = id;
  document.getElementById("vehicleSelect").value = id;
  
  // Remover selección visual de todas las tarjetas
  document.querySelectorAll(".vehicle-card").forEach(card => {
    card.classList.remove("border-amber-500", "bg-amber-50/30", "shadow-md");
    card.classList.add("border-slate-200");
    const indicator = card.querySelector(".select-indicator");
    indicator.classList.remove("bg-amber-500", "text-white");
    indicator.classList.add("bg-slate-100", "text-slate-400");
  });

  // Aplicar estilo seleccionado a la tarjeta clickeada
  element.classList.remove("border-slate-200");
  element.classList.add("border-amber-500", "bg-amber-50/30", "shadow-md");
  const activeIndicator = element.querySelector(".select-indicator");
  activeIndicator.classList.remove("bg-slate-100", "text-slate-400");
  activeIndicator.classList.add("bg-amber-500", "text-white");
}

document.addEventListener("DOMContentLoaded", function() {
  loadVehiclesGrid();

  const startInput = document.getElementById("startDate");
  const endInput = document.getElementById("endDate");

  if (!startInput || !endInput) return;

  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  const tomorrowStr = tomorrow.toISOString().split("T")[0];

  startInput.min = tomorrowStr;
  if (!startInput.value || startInput.value < tomorrowStr) {
    startInput.value = tomorrowStr;
  }

  const updateEndMin = function() {
    if (!startInput.value) return;
    const startVal = new Date(startInput.value);
    const minEnd = new Date(startVal);
    minEnd.setDate(minEnd.getDate() + 1);
    const minEndStr = minEnd.toISOString().split("T")[0];

    endInput.min = minEndStr;
    if (!endInput.value || endInput.value <= startInput.value) {
      endInput.value = minEndStr;
    }
  };

  updateEndMin();
  startInput.addEventListener("change", updateEndMin);
  startInput.addEventListener("input", updateEndMin);
});
</script>
"""

# Reemplazamos los scripts anteriores y agregamos las tarjetas en el HTML
import re
# Eliminamos cualquier script previo de validación/carga
html = re.sub(r'<script>[\s\S]*?adjustCount[\s\S]*?</script>', "", html)

# Insertamos el contenedor de tarjetas antes del cierre del body y el nuevo script
html = html.replace("</body>", cards_container_html + "\n" + new_script + "\n</body>")

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("¡Tarjetas de vehículos integradas con éxito en el frontend!")
