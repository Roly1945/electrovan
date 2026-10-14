import os

frontend_index = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Electrovan | Renta de Autos Eléctricos e Híbridos</title>
    <style>
        html { scroll-behavior: smooth; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; }
        .navbar { background: #0f172a; padding: 18px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #00E5FF; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .nav-left { display: flex; align-items: center; gap: 30px; }
        .brand { background: #00E5FF; color: #0f172a; font-weight: 900; font-size: 1.3em; padding: 6px 16px; text-decoration: none; letter-spacing: 1px; border-radius: 4px; text-transform: uppercase; }
        .nav-links { display: flex; gap: 20px; list-style: none; margin: 0; padding: 0; }
        .nav-links a { color: #f8fafc; text-decoration: none; font-size: 0.95em; font-weight: 600; transition: color 0.2s; }
        .nav-links a:hover { color: #00E5FF; }
        .lang-select { background: #1e293b; color: #00E5FF; border: 1px solid #00E5FF; padding: 6px 12px; border-radius: 6px; font-weight: 700; cursor: pointer; font-size: 0.85em; }
        
        .hero-banner { background: #0f172a; color: #ffffff; padding: 40px 20px 30px 20px; text-align: center; border-bottom: 1px solid #1e293b; }
        .hero-banner h1 { font-size: 2.2em; font-weight: 900; margin: 0 0 10px 0; color: #ffffff; }
        .hero-banner p { font-size: 1.05em; color: #94a3b8; margin: 0; font-weight: 500; }

        .container { max-width: 1100px; margin: 30px auto 50px auto; padding: 0 20px; }
        .booking-widget { background: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; margin-bottom: 40px; }
        .booking-title { font-size: 1.2em; font-weight: 800; color: #0f172a; text-align: center; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; border-bottom: 2px solid #10b981; padding-bottom: 10px; }
        
        .engine-row { display: grid; grid-template-columns: 140px 2fr 1.2fr 1fr; gap: 15px; align-items: center; margin-bottom: 20px; }
        .engine-row-title { font-weight: 800; font-size: 1.1em; color: #0f172a; }
        
        .input-group { display: flex; flex-direction: column; }
        .input-group label { font-size: 0.78em; font-weight: 700; color: #64748b; margin-bottom: 6px; text-transform: uppercase; }
        input, select { padding: 12px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.95em; background: #f8fafc; color: #0f172a; width: 100%; box-sizing: border-box; }
        input:focus, select:focus { outline: none; border-color: #00E5FF; background: #ffffff; }
        
        .checkbox-group { display: flex; align-items: center; gap: 8px; margin-top: 20px; font-size: 0.9em; font-weight: 600; color: #334155; }
        .checkbox-group input { width: auto; margin: 0; accent-color: #10b981; }
        
        .btn-reserve { background: #00E5FF; color: #0f172a; font-weight: 900; padding: 14px; border: none; border-radius: 6px; font-size: 1.05em; cursor: pointer; text-transform: uppercase; letter-spacing: 1px; width: 100%; margin-top: 20px; transition: background 0.2s; }
        .btn-reserve:hover { background: #00b8cc; }
        
        h2 { color: #0f172a; font-size: 1.6em; font-weight: 800; margin-bottom: 25px; border-left: 6px solid #10b981; padding-left: 12px; }
        .grid { display: flex; gap: 25px; flex-wrap: wrap; justify-content: center; margin-bottom: 40px; }
        
        .card { background: #ffffff; padding: 25px; border-radius: 12px; width: 330px; border: 1px solid #e2e8f0; box-shadow: 0 4px 15px rgba(0,0,0,0.04); display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s; }
        .card:hover { transform: translateY(-4px); }
        
        .badge { background: #d1fae5; color: #047857; font-size: 0.75em; font-weight: 800; padding: 5px 12px; border-radius: 20px; display: inline-block; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
        .badge::before { content: "🟢 "; }
        
        .card h3 { color: #0f172a; margin: 0 0 10px 0; font-size: 1.4em; font-weight: 800; }
        .card p { color: #64748b; font-size: 0.9em; margin: 6px 0; }
        .price { font-size: 1.4em; color: #0f172a; font-weight: 900; margin: 18px 0; text-align: center; }
        .price span { font-size: 0.6em; color: #64748b; font-weight: 600; }
        
        .btn-card { background: #00E5FF; color: #0f172a; font-weight: 900; padding: 12px; border: none; border-radius: 6px; cursor: pointer; text-transform: uppercase; width: 100%; font-size: 0.9em; letter-spacing: 0.5px; transition: background 0.2s; }
        .btn-card:hover { background: #00b8cc; }

        @media (max-width: 850px) {
            .engine-row { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="navbar">
        <div class="nav-left">
            <a href="#" class="brand">ELECTROVAN</a>
            <ul class="nav-links">
                <li><a href="#fleet-section" id="nav-fleet">Flota</a></li>
                <li><a href="#booking-section" id="nav-reserve">Reservar</a></li>
            </ul>
        </div>
        <div class="nav-right">
            🌐 <select id="lang-selector" class="lang-select">
                <option value="es">ESPAÑOL</option>
                <option value="en">ENGLISH</option>
            </select>
        </div>
    </div>

    <div class="hero-banner">
        <h1><span id="hero-title-prefix">Renta Movilidad </span><span id="hero-span" style="color:#10b981;">Ecológica e Inteligente</span></h1>
        <p id="hero-desc">⚡ Autos 100% Eléctricos e Híbridos disponibles para renta inmediata.</p>
    </div>

    <div class="container">
        <!-- PASO 1: DATOS DEL CONDUCTOR -->
        <div class="booking-widget" style="margin-bottom: 25px; padding: 22px 30px;">
            <div class="booking-title" id="step1-title" style="margin-bottom: 15px; border-bottom-color: #00E5FF;">1. DATOS DEL CONDUCTOR</div>
            <form id="client-form" style="display: flex; gap: 15px; flex-wrap: wrap;">
                <input type="text" id="client-name" placeholder="Nombre completo" required style="flex:1;">
                <input type="email" id="client-email" placeholder="Correo electrónico" required style="flex:1;">
                <input type="text" id="client-phone" placeholder="Teléfono" required style="flex:1;">
                <button type="submit" id="btn-continue" class="btn-card" style="width: auto; padding: 0 25px;">Continuar</button>
            </form>
            <p id="client-status" style="color: #10b981; font-weight: bold; text-align: center; margin: 12px 0 0 0;"></p>
        </div>

        <!-- PASO 2: MOTOR DE RESERVAS -->
        <div id="booking-section" class="booking-widget">
            <div class="booking-title" id="step2-title">2. SELECCIONA FECHAS Y UBICACIÓN</div>
            <form id="reservation-form">
                
                <div class="input-group" style="margin-bottom: 25px;">
                    <label id="lbl-vehicle">VEHÍCULO A RENTAR</label>
                    <select id="res-vehicle" required><option value="">Seleccione vehículo</option></select>
                </div>

                <div class="engine-row">
                    <div class="engine-row-title" id="title-pickup">Recolección</div>
                    <div class="input-group">
                        <label id="lbl-pickup-loc">Ubicación</label>
                        <select id="pickup-location" required>
                            <option value="Oficina Principal / Aeropuerto">¿Dónde necesitas tu auto?</option>
                            <option value="Aeropuerto Internacional (MID / CUN)">Aeropuerto Internacional</option>
                            <option value="Oficina Centro Historico">Oficina Centro Histórico</option>
                            <option value="Entrega a Domicilio / Hotel">Entrega a Domicilio / Hotel</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label id="lbl-pickup-date">Fecha de recolección</label>
                        <input type="date" id="start-date" required>
                    </div>
                    <div class="input-group">
                        <label id="lbl-pickup-time">Hora de recolección</label>
                        <select id="pickup-time">
                            <option value="08:00 AM">08:00 AM</option>
                            <option value="10:00 AM" selected>10:00 AM</option>
                            <option value="12:00 PM">12:00 PM</option>
                            <option value="02:00 PM">02:00 PM</option>
                            <option value="04:00 PM">04:00 PM</option>
                            <option value="06:00 PM">06:00 PM</option>
                        </select>
                    </div>
                </div>

                <div class="engine-row">
                    <div class="engine-row-title" id="title-return">Devolución</div>
                    <div class="input-group">
                        <label id="lbl-return-loc">Ubicación</label>
                        <select id="return-location" required>
                            <option value="Oficina Principal / Aeropuerto">¿Dónde termina tu viaje?</option>
                            <option value="Aeropuerto Internacional (MID / CUN)">Aeropuerto Internacional</option>
                            <option value="Oficina Centro Historico">Oficina Centro Histórico</option>
                            <option value="Recolección a Domicilio / Hotel">Recolección a Domicilio / Hotel</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label id="lbl-return-date">Fecha de devolución</label>
                        <input type="date" id="end-date" required>
                    </div>
                    <div class="input-group">
                        <label id="lbl-return-time">Hora de devolución</label>
                        <select id="return-time">
                            <option value="08:00 AM">08:00 AM</option>
                            <option value="10:00 AM" selected>10:00 AM</option>
                            <option value="12:00 PM">12:00 PM</option>
                            <option value="02:00 PM">02:00 PM</option>
                            <option value="04:00 PM">04:00 PM</option>
                            <option value="06:00 PM">06:00 PM</option>
                        </select>
                    </div>
                </div>

                <div class="checkbox-group">
                    <input type="checkbox" id="include-chubb" checked>
                    <label for="include-chubb" id="lbl-chubb">Incluir cobertura Travel Care+ by Chubb ($250 MXN / día)</label>
                </div>
                <button type="submit" id="btn-confirm" class="btn-reserve">Confirmar Renta</button>
            </form>
            <p id="res-status" style="font-weight: bold; text-align: center; margin-top: 15px;"></p>
        </div>

        <!-- FLOTA -->
        <h2 id="fleet-section">🚗 Flota Disponible</h2>
        <div id="fleet-container" class="grid">Cargando vehículos ecológicos...</div>
    </div>

    <script>
        let currentLang = "es";
        let currentClientId = null;
        let vehiclesCache = [];

        const i18n = {
            es: {
                nav_fleet: "Flota",
                nav_reserve: "Reservar",
                hero_prefix: "Renta Movilidad ",
                hero_span: "Ecológica e Inteligente",
                hero_desc: "⚡ Autos 100% Eléctricos e Híbridos disponibles para renta inmediata.",
                step1_title: "1. DATOS DEL CONDUCTOR",
                placeholder_name: "Nombre completo",
                placeholder_email: "Correo electrónico",
                placeholder_phone: "Teléfono",
                btn_continue: "Continuar",
                step2_title: "2. SELECCIONA FECHAS Y UBICACIÓN",
                lbl_vehicle: "VEHÍCULO A RENTAR",
                title_pickup: "Recolección",
                title_return: "Devolución",
                lbl_loc: "Ubicación",
                lbl_pickup_date: "Fecha de recolección",
                lbl_pickup_time: "Hora de recolección",
                lbl_return_date: "Fecha de devolución",
                lbl_return_time: "Hora de devolución",
                placeholder_pickup_loc: "¿Dónde necesitas tu auto?",
                placeholder_return_loc: "¿Dónde termina tu viaje?",
                lbl_chubb: "Incluir cobertura Travel Care+ by Chubb ($250 MXN / día)",
                btn_confirm: "CONFIRMAR RENTA",
                fleet_title: "🚗 Flota Disponible",
                select_vehicle_default: "Seleccione vehículo",
                badge_available: "DISPONIBLE",
                autonomy_text: "Autonomía",
                per_charge: "por carga",
                battery_text: "Batería",
                plates_text: "Placas",
                per_day: "/día",
                confirm_rent_btn: "CONFIRMAR RENTA",
                welcome_msg: "¡Bienvenido {name}! Por favor selecciona tu vehículo y fechas.",
                err_conductor: "Completa primero tus datos de conductor en el Paso 1.",
                err_date_order: "❌ Error: La fecha de devolución debe ser posterior a la fecha de recolección.",
                success_rent: "¡Renta #{id} confirmada! Total final: ${total} MXN"
            },
            en: {
                nav_fleet: "Fleet",
                nav_reserve: "Book Now",
                hero_prefix: "Rent Smart ",
                hero_span: "Eco-Friendly Mobility",
                hero_desc: "⚡ 100% Electric & Hybrid Vehicles available for immediate rental.",
                step1_title: "1. DRIVER DETAILS",
                placeholder_name: "Full Name",
                placeholder_email: "Email Address",
                placeholder_phone: "Phone Number",
                btn_continue: "Continue",
                step2_title: "2. SELECT DATES AND LOCATION",
                lbl_vehicle: "VEHICLE TO RENT",
                title_pickup: "Pickup",
                title_return: "Return",
                lbl_loc: "Location",
                lbl_pickup_date: "Pickup date",
                lbl_pickup_time: "Pickup time",
                lbl_return_date: "Return date",
                lbl_return_time: "Return time",
                placeholder_pickup_loc: "Where do you need your car?",
                placeholder_return_loc: "Where does your trip end?",
                lbl_chubb: "Include Travel Care+ coverage by Chubb ($250 MXN / day)",
                btn_confirm: "CONFIRM RENTAL",
                fleet_title: "🚗 Available Fleet",
                select_vehicle_default: "Select a vehicle",
                badge_available: "AVAILABLE",
                autonomy_text: "Range",
                per_charge: "per charge",
                battery_text: "Battery",
                plates_text: "License Plate",
                per_day: "/day",
                confirm_rent_btn: "CONFIRM RENTAL",
                welcome_msg: "Welcome {name}! Please select your vehicle and dates.",
                err_conductor: "Please complete step 1 (driver info) first.",
                err_date_order: "❌ Error: Return date must be after pickup date.",
                success_rent: "Rental #{id} confirmed! Final total: ${total} MXN"
            }
        };

        function changeLanguage(lang) {
            currentLang = lang;
            const t = i18n[lang];

            document.getElementById("nav-fleet").innerText = t.nav_fleet;
            document.getElementById("nav-reserve").innerText = t.nav_reserve;
            
            document.getElementById("hero-title-prefix").innerText = t.hero_prefix;
            document.getElementById("hero-span").innerText = t.hero_span;
            document.getElementById("hero-desc").innerText = t.hero_desc;

            document.getElementById("step1-title").innerText = t.step1_title;
            document.getElementById("client-name").placeholder = t.placeholder_name;
            document.getElementById("client-email").placeholder = t.placeholder_email;
            document.getElementById("client-phone").placeholder = t.placeholder_phone;
            document.getElementById("btn-continue").innerText = t.btn_continue;

            document.getElementById("step2-title").innerText = t.step2_title;
            document.getElementById("lbl-vehicle").innerText = t.lbl_vehicle;
            
            document.getElementById("title-pickup").innerText = t.title_pickup;
            document.getElementById("title-return").innerText = t.title_return;
            document.getElementById("lbl-pickup-loc").innerText = t.lbl_loc;
            document.getElementById("lbl-return-loc").innerText = t.lbl_loc;
            document.getElementById("lbl-pickup-date").innerText = t.lbl_pickup_date;
            document.getElementById("lbl-pickup-time").innerText = t.lbl_pickup_time;
            document.getElementById("lbl-return-date").innerText = t.lbl_return_date;
            document.getElementById("lbl-return-time").innerText = t.lbl_return_time;

            document.getElementById("pickup-location").options[0].text = t.placeholder_pickup_loc;
            document.getElementById("return-location").options[0].text = t.placeholder_return_loc;

            document.getElementById("lbl-chubb").innerText = t.lbl_chubb;
            document.getElementById("btn-confirm").innerText = t.btn_confirm;
            document.getElementById("fleet-section").innerText = t.fleet_title;

            renderFleet(vehiclesCache);
        }

        document.getElementById("lang-selector").addEventListener("change", (e) => {
            changeLanguage(e.target.value);
        });

        const todayStr = new Date().toISOString().split("T")[0];
        const startDateInput = document.getElementById("start-date");
        const endDateInput = document.getElementById("end-date");

        startDateInput.min = todayStr;
        endDateInput.min = todayStr;

        startDateInput.addEventListener("change", () => {
            if (startDateInput.value) {
                const sDate = new Date(startDateInput.value);
                sDate.setDate(sDate.getDate() + 1);
                const minEnd = sDate.toISOString().split("T")[0];
                endDateInput.min = minEnd;

                if (endDateInput.value && endDateInput.value <= startDateInput.value) {
                    endDateInput.value = minEnd;
                }
            }
        });

        function loadData() {
            fetch("/api/vehicles")
                .then(res => res.json())
                .then(data => {
                    vehiclesCache = data;
                    renderFleet(data);
                })
                .catch(err => {
                    document.getElementById("fleet-container").innerHTML = "<p>Cargando vehículos...</p>";
                });
        }

        function renderFleet(data) {
            const t = i18n[currentLang];
            const container = document.getElementById("fleet-container");
            const selectV = document.getElementById("res-vehicle");

            if (!data || data.length === 0) {
                container.innerHTML = "<p>No hay vehículos disponibles.</p>";
                return;
            }

            container.innerHTML = data.map(v => `
                <div class="card">
                    <div>
                        <span class="badge">${t.badge_available}</span>
                        <h3>${v.name}</h3>
                        <p>🏷️ ${t.plates_text}: ${v.plate || "N/A"} | 📅 ${v.year || 2026}</p>
                        <p>⚡ ${t.autonomy_text}: <strong>${v.autonomy_km} km</strong> ${t.per_charge}</p>
                        <p>🔋 ${t.battery_text}: ${v.battery_kwh} kWh</p>
                    </div>
                    <div>
                        <div class="price">$${v.daily_rate.toLocaleString("es-MX", {minimumFractionDigits: 2})} MXN <span>${t.per_day}</span></div>
                        <button class="btn-card" onclick="selectVehicle(${v.id})">${t.confirm_rent_btn}</button>
                    </div>
                </div>
            `).join("");

            const currentSelected = selectV.value;
            selectV.innerHTML = `<option value="">${t.select_vehicle_default}</option>` + data.map(v => `<option value="${v.id}">${v.name} ($${v.daily_rate} MXN${t.per_day})</option>`).join("");
            selectV.value = currentSelected;
        }

        function selectVehicle(id) {
            document.getElementById("res-vehicle").value = id;
            window.scrollTo({top: document.getElementById("booking-section").offsetTop - 20, behavior: "smooth"});
        }

        document.getElementById("client-form").addEventListener("submit", e => {
            e.preventDefault();
            const t = i18n[currentLang];
            fetch("/api/clients", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    full_name: document.getElementById("client-name").value,
                    email: document.getElementById("client-email").value,
                    phone: document.getElementById("client-phone").value
                })
            })
            .then(res => res.json())
            .then(data => {
                currentClientId = data.id;
                document.getElementById("client-status").innerText = t.welcome_msg.replace("{name}", data.full_name);
            });
        });

        document.getElementById("reservation-form").addEventListener("submit", e => {
            e.preventDefault();
            const t = i18n[currentLang];
            const statusElem = document.getElementById("res-status");
            statusElem.innerText = "";

            if (!currentClientId) {
                alert(t.err_conductor);
                return;
            }

            const sDate = startDateInput.value;
            const eDate = endDateInput.value;

            if (eDate <= sDate) {
                statusElem.style.color = "#ef4444";
                statusElem.innerText = t.err_date_order;
                return;
            }

            fetch("/api/reservations", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    client_id: currentClientId,
                    vehicle_id: parseInt(document.getElementById("res-vehicle").value),
                    pickup_location: document.getElementById("pickup-location").value,
                    start_date: sDate,
                    pickup_time: document.getElementById("pickup-time").value,
                    return_location: document.getElementById("return-location").value,
                    end_date: eDate,
                    return_time: document.getElementById("return-time").value,
                    include_chubb: document.getElementById("include-chubb").checked
                })
            })
            .then(async res => {
                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || "Error");
                }
                return data;
            })
            .then(data => {
                statusElem.style.color = "#10b981";
                statusElem.innerText = t.success_rent.replace("{id}", data.id).replace("{total}", data.total_price.toLocaleString("es-MX", {minimumFractionDigits: 2}));
            })
            .catch(err => {
                statusElem.style.color = "#ef4444";
                statusElem.innerText = "❌ Error al procesar la reserva";
            });
        });

        loadData();
    </script>
</body>
</html>
"""

with open("frontend/index.html", "w") as f:
    f.write(frontend_index)

print("¡Archivo frontend/index.html actualizado correctamente!")
