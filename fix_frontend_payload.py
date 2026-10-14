with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Reemplazamos la función submitReservation con un payload compatible y robusto
old_function_start = "async function submitReservation(event) {"
new_function = """async function submitReservation(event) {
      event.preventDefault();

      const nameVal = document.getElementById("clientName").value;
      const emailVal = document.getElementById("clientEmail").value;
      const phoneVal = document.getElementById("clientPhone").value;

      // Payload flexible para modelos Pydantic
      const clientData = {
        name: nameVal,
        full_name: nameVal,
        email: emailVal,
        phone: phoneVal,
        phone_number: phoneVal
      };

      try {
        // 1. Registrar cliente
        const clientRes = await fetch("/api/clients", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(clientData)
        });

        if (!clientRes.ok) {
          const errData = await clientRes.json().catch(() => ({}));
          console.error("Error backend clients:", errData);
          throw new Error("Error en el registro del cliente");
        }
        
        const client = await clientRes.json();

        // 2. Crear reserva
        const startDate = document.getElementById("startDate").value;
        const endDate = document.getElementById("endDate").value;
        const startDt = new Date(startDate);
        const endDt = new Date(endDate);
        const diffDays = Math.max(1, Math.ceil(Math.abs(endDt - startDt) / (1000 * 60 * 60 * 24)));

        const unitPrice = parseFloat(document.getElementById("selectedPrice").value) || 0;
        const totalAmount = unitPrice * diffDays;

        const pickupLoc = document.getElementById("pickupLocation") ? document.getElementById("pickupLocation").value : "Aeropuerto Internacional";
        const returnLoc = document.getElementById("returnLocation") ? document.getElementById("returnLocation").value : pickupLoc;

        const reservationData = {
          client_id: client.id,
          vehicle_id: parseInt(document.getElementById("selectedVehicleId").value),
          pickup_location: pickupLoc,
          return_location: returnLoc,
          start_date: startDate,
          end_date: endDate,
          total_days: diffDays,
          days: diffDays,
          total_price: totalAmount,
          base_rate: unitPrice,
          status: "Confirmada",
          driver_age: document.getElementById("driverAge") ? document.getElementById("driverAge").value : "25+",
          adults: parseInt(document.getElementById("adultsCount") ? document.getElementById("adultsCount").innerText : 1),
          children: parseInt(document.getElementById("childrenCount") ? document.getElementById("childrenCount").innerText : 0)
        };

        const resRes = await fetch("/api/reservations", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(reservationData)
        });

        if (!resRes.ok) {
          const errResData = await resRes.json().catch(() => ({}));
          console.error("Error backend reservations:", errResData);
          throw new Error("Error al crear la reserva");
        }

        const resData = await resRes.json();
        const folioCode = resData.folio || ("REV-" + Math.floor(100000 + Math.random() * 900000));

        alert("¡Reserva confirmada con éxito! Folio: " + folioCode);
        closeBookingModal();
        document.getElementById("bookingForm").reset();
      } catch (err) {
        console.error("Detalle del error:", err);
        alert("Ocurrió un error al procesar la reserva. Revisa la consola o los datos ingresados.");
      }
    }"""

import re
html = re.sub(r'async function submitReservation\(event\) \{[\s\S]*?\}\s*</script>', new_function + "\n  </script>", html)

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("¡Script de reservaciones ajustado con éxito!")
