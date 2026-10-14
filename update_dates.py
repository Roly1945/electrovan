with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Bloque HTML completo de la sección de reserva (sin tipo de vehículo)
new_section = """<div class="bg-white rounded-2xl shadow-2xl p-6 text-slate-800 border border-slate-100 max-w-5xl mx-auto my-6 space-y-6">
  <div class="text-xl font-black text-amber-500 tracking-wider uppercase border-b pb-3">Reserva Aquí</div>
  
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-center bg-slate-50 p-4 rounded-xl border border-slate-200">
    <div class="text-sm font-bold text-slate-600">Recolección</div>
    <div>
      <select id="pickupLocation" class="w-full bg-white border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400">
        <option value="" disabled selected>¿Dónde necesitas tu auto?</option>
        <option value="Aeropuerto Internacional">Aeropuerto Internacional</option>
        <option value="Oficina Centro Histórico">Oficina Centro Histórico</option>
      </select>
    </div>
    <div class="grid grid-cols-2 gap-2">
      <input type="date" id="startDate" class="bg-white border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400" required>
      <select id="startTime" class="bg-white border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400">
        <option value="10:00">10:00 AM</option>
        <option value="12:00">12:00 PM</option>
        <option value="14:00">02:00 PM</option>
        <option value="16:00">04:00 PM</option>
      </select>
    </div>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-center bg-slate-50 p-4 rounded-xl border border-slate-200">
    <div class="text-sm font-bold text-slate-600">Devolución</div>
    <div>
      <select id="returnLocation" class="w-full bg-white border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400">
        <option value="" disabled selected>¿Dónde termina tu viaje?</option>
        <option value="Aeropuerto Internacional">Aeropuerto Internacional</option>
        <option value="Oficina Centro Histórico">Oficina Centro Histórico</option>
      </select>
    </div>
    <div class="grid grid-cols-2 gap-2">
      <input type="date" id="endDate" class="bg-white border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400" required>
      <select id="endTime" class="bg-white border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400">
        <option value="10:00">10:00 AM</option>
        <option value="12:00">12:00 PM</option>
        <option value="14:00">02:00 PM</option>
        <option value="16:00">04:00 PM</option>
      </select>
    </div>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-center bg-slate-50 p-4 rounded-xl border border-slate-200">
    <div class="text-sm font-bold text-slate-600">Pasajeros</div>
    <div>
      <label class="block text-[10px] uppercase font-bold text-slate-400 mb-1">Edad Conductor</label>
      <select id="driverAge" class="w-full bg-white border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400">
        <option value="25+">25 +</option>
        <option value="21-24">21 - 24</option>
      </select>
    </div>
    <div class="grid grid-cols-2 gap-3">
      <div class="flex items-center justify-between bg-white border border-slate-300 rounded-xl p-2.5">
        <span class="text-xs font-bold text-slate-600 px-1">Adultos</span>
        <div class="flex items-center gap-1">
          <button type="button" onclick="adjustCount('adultsCount', -1)" class="w-6 h-6 bg-slate-100 rounded-lg font-bold text-slate-600 hover:bg-slate-200">-</button>
          <span id="adultsCount" class="text-sm font-bold w-4 text-center">1</span>
          <button type="button" onclick="adjustCount('adultsCount', 1)" class="w-6 h-6 bg-slate-100 rounded-lg font-bold text-slate-600 hover:bg-slate-200">+</button>
        </div>
      </div>
      <div class="flex items-center justify-between bg-white border border-slate-300 rounded-xl p-2.5">
        <span class="text-xs font-bold text-slate-600 px-1">Niños</span>
        <div class="flex items-center gap-1">
          <button type="button" onclick="adjustCount('childrenCount', -1)" class="w-6 h-6 bg-slate-100 rounded-lg font-bold text-slate-600 hover:bg-slate-200">-</button>
          <span id="childrenCount" class="text-sm font-bold w-4 text-center">0</span>
          <button type="button" onclick="adjustCount('childrenCount', 1)" class="w-6 h-6 bg-slate-100 rounded-lg font-bold text-slate-600 hover:bg-slate-200">+</button>
        </div>
      </div>
    </div>
  </div>
</div>"""

validation_script = """
<script>
function adjustCount(elementId, delta) {
  const el = document.getElementById(elementId);
  if (!el) return;
  let val = parseInt(el.innerText) + delta;
  if (elementId === "adultsCount" && val < 1) val = 1;
  if (elementId === "childrenCount" && val < 0) val = 0;
  el.innerText = val;
}

document.addEventListener("DOMContentLoaded", function() {
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

import re
if "Reserva Aquí" in html:
    html = re.sub(r'<div[^>]*>[\s\S]*?Reserva Aquí[\s\S]*?</div>\s*</div>\s*</div>', new_section, html, count=1)

html = re.sub(r'<script>[\s\S]*?adjustCount[\s\S]*?</script>', "", html)
html = html.replace("</body>", validation_script + "\n</body>")

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("¡Actualización completada con éxito!")
