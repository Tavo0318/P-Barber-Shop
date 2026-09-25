// ==========================================
// P-BARBER SHOP
// Sistema inicial de reservas
// ==========================================

const formulario = document.getElementById("formularioCita");
const mensaje = document.getElementById("mensaje");
const fecha = document.getElementById("fecha");


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
    function (evento) {

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

    }
);