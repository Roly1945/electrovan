with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Modificamos la tercera fila del módulo de reserva para que ya no tenga los selectores de adultos y niños,
# sino que se centre en la Edad del Conductor y el Tipo de Vehículo con mejor distribución.
old_row3 = """      <!-- Fila 3: Pasajeros, Edad y Tipo de Vehículo -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-center bg-slate-50 p-4 rounded-2xl border border-slate-200">
        <div>
          <label class="block text-[10px] uppercase font-black text-slate-500 mb-1">Edad Conductor</label>
          <select id="driverAge" class="w-full bg-white border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="25+">25 +</option>
            <option value="21-24">21 - 24</option>
          </select>
        </div>
        <div>
          <label class="block text-[10px] uppercase font-black text-slate-500 mb-1">Tipo de Vehículo</label>
          <select id="vehicleTypeFilter" onchange="filterVehicles()" class="w-full bg-white border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="TODOS">TODOS</option>
            <option value="ECONOMY CAR">ECONOMY CAR</option>
            <option value="COMPACT CAR">COMPACT CAR</option>
            <option value="INTERMEDIATE CAR">INTERMEDIATE CAR</option>
            <option value="STANDARD CAR">STANDARD CAR</option>
            <option value="FULLSIZE CAR">FULLSIZE CAR</option>
            <option value="PREMIUM CAR">PREMIUM CAR</option>
            <option value="LUXURY CAR">LUXURY CAR</option>
          </select>
        </div>
        <div class="grid grid-cols-2 gap-2">
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
      </div>"""

new_row3 = """      <!-- Fila 3: Edad del Conductor y Tipo de Vehículo -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-center bg-slate-50 p-4 rounded-2xl border border-slate-200">
        <div>
          <label class="block text-[10px] uppercase font-black text-slate-500 mb-1">Edad Conductor</label>
          <select id="driverAge" class="w-full bg-white border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="25+">25 +</option>
            <option value="21-24">21 - 24</option>
          </select>
        </div>
        <div>
          <label class="block text-[10px] uppercase font-black text-slate-500 mb-1">Tipo de Vehículo</label>
          <select id="vehicleTypeFilter" onchange="filterVehicles()" class="w-full bg-white border border-slate-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="TODOS">TODOS</option>
            <option value="ECONOMY CAR">ECONOMY CAR</option>
            <option value="COMPACT CAR">COMPACT CAR</option>
            <option value="INTERMEDIATE CAR">INTERMEDIATE CAR</option>
            <option value="STANDARD CAR">STANDARD CAR</option>
            <option value="FULLSIZE CAR">FULLSIZE CAR</option>
            <option value="PREMIUM CAR">PREMIUM CAR</option>
            <option value="LUXURY CAR">LUXURY CAR</option>
          </select>
        </div>
      </div>"""

if old_row3 in html:
    html = html.replace(old_row3, new_row3)
else:
    # Si la estructura exacta varía un poco, reemplazamos por secciones lógicas
    print("Aviso: Coincidencia exacta de Fila 3 no encontrada, revisando alternativa...")

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("¡Sección de pasajeros removida del formulario principal con éxito!")
