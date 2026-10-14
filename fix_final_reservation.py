with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

new_function = """async function submitReservation(event) {
      event.preventDefault();

      const nameVal = document.getElementById("clientName").value;
      const emailVal = document.getElementById("clientEmail").value;
      const phoneVal = document.getElementById("clientPhone").value;

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

        if (!clientRes.ok) throw new Error("Error en el registro del cliente");
        const client = await clientRes.json();

        // 2. Crear reserva con todos los campos requeridos por el modelo Pydantic
        const startDate = document.getElementById("startDate").value;
        const endDate = document.getElementById("endDate").value;
        const startDt = new Date(startDate);
        const endDt = new Date(endDate);
        const diffDays = Math.max(1, Math.ceil(Math.abs(endDt - startDt) / (1000 * 60 * 60 * 24)));

        const unitPrice = parseFloat(document.getElementById("selectedPrice").value) || 2500;
        const totalAmount = unitPrice * diffDays;

        const pickupLoc = document.getElementById("pickupLocation") ? document.getElementById("pickupLocation").value : "Aeropuerto Internacional";
        const returnLoc = document.getElementById("returnLocation") ? document.getElementById("returnLocation").value : pickupLoc;
        const vehicleTypeVal = document.getElementById("vehicleTypeFilter") ? document.getElementById("vehicleTypeFilter").value : "ECONOMY CAR";

        const reservationData = {
          client_id: client.id,
          vehicle_id: parseInt(document.getElementById("selectedVehicleId").value),
          pickup_location: pickupLoc,
          start_date: startDate,
          return_location: returnLoc,
          end_date: endDate,
          days: diffDays,
          base_rate: unitPrice,
          chubb_insurance: false,
          total_price: totalAmount,
          status: "Confirmada",
          driver_age: document.getElementById("driverAge") ? document.getElementById("driverAge").value : "25+",
          adults: parseInt(document.getElementById("adultsCount") ? document.getElementById("adultsCount").innerText : 1),
          children: parseInt(document.getElementById("childrenCount") ? document.getElementById("childrenCount").innerText : 0),
          vehicle_type: vehicleTypeVal
        };

        const resRes = await fetch("/api/reservations", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(reservationData)
        });

        if (!resRes.ok) {
          const errBody = await resRes.text();
          console.error("Detalle error reservas:", errBody);
          throw new Error("Error al crear la reserva en el servidor");
        }

        const resData = await resRes.json();
        const folioCode = resData.folio || ("REV-" + Math.floor(100000 + Math.random() * 900000));

        alert("¡Reserva confirmada con éxito! Folio: " + folioCode);
        closeBookingModal();
        document.getElementById("bookingForm").reset();
      } catch (err) {
        console.error("Error general:", err);
        alert("Ocurrió un error al procesar la reserva. Por favor intenta de nuevo.");
      }
    }"""

import re
html = re.sub(r'async function submitReservation\(event\) \{[\s\S]*?\}\s*</script>', new_function + "\n  </script>", html)

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("¡Frontend actualizado con el modelo exacto de reservas!")
