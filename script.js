// ==========================================
// P-BARBER SHOP
// Sistema de reservas
// ==========================================

const formulario = document.getElementById("formularioCita");
const mensaje = document.getElementById("mensaje");
const fecha = document.getElementById("fecha");

// ==========================================
// URL DE LA API EN RENDER
// ==========================================

const API_URL = "https://p-barber-shop.onrender.com";

// ==========================================
// NO PERMITIR FECHAS ANTERIORES A HOY
// ==========================================

const hoy = new Date();

const año = hoy.getFullYear();

const mes = String(
    hoy.getMonth() + 1
).padStart(2, "0");

const dia = String(
    hoy.getDate()
).padStart(2, "0");

const fechaActual =
    `${año}-${mes}-${dia}`;

fecha.min = fechaActual;

// ==========================================
// CONFIRMAR CITA
// ==========================================

formulario.addEventListener(
    "submit",
    async function (evento) {

        evento.preventDefault();

        // Obtener información
        const nombre =
            document.getElementById("nombre").value.trim();

        const telefono =
            document.getElementById("telefono").value.trim();

        const servicio =
            document.getElementById("servicio").value;

        const fechaSeleccionada =
            document.getElementById("fecha").value;

        const hora =
            document.getElementById("hora").value;

        // Mostrar mensaje mientras se guarda
        mensaje.innerHTML = `
            ⏳ Guardando tu cita...
        `;

        try {

            // Enviar la cita a la API
            const respuesta = await fetch(
                `${API_URL}/citas`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        nombre: nombre,
                        telefono: telefono,
                        servicio: servicio,
                        fecha: fechaSeleccionada,
                        hora: hora
                    })
                }
            );

            const datos = await respuesta.json();

            // Comprobar si hubo error
            if (!respuesta.ok) {
                throw new Error(
                    datos.detail || "No se pudo registrar la cita"
                );
            }

            // Convertir fecha
            const fechaBonita =
                new Date(
                    fechaSeleccionada + "T00:00:00"
                ).toLocaleDateString(
                    "es-CO",
                    {
                        day: "2-digit",
                        month: "2-digit",
                        year: "numeric"
                    }
                );

            // Mostrar confirmación
            mensaje.innerHTML = `
                ✅ ¡Cita registrada correctamente!
                <br><br>

                👤 ${nombre}
                <br>

                ✂️ ${servicio}
                <br>

                📅 ${fechaBonita}
                <br>

                🕐 ${hora}
                <br>

                📱 ${telefono}
            `;

            // Limpiar formulario
            formulario.reset();

            // Mantener la fecha mínima
            fecha.min = fechaActual;

        } catch (error) {

            console.error(error);

            mensaje.innerHTML = `
                ❌ No se pudo registrar la cita.
                <br><br>
                Inténtalo nuevamente.
            `;
        }
    }
);