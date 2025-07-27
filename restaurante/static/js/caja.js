
document.getElementById("btn-abrir-caja").addEventListener("click", function () {
    fetch('/verificar_caja/')
        .then(res => res.json())
        .then(data => {
            if (data.estado === 'abierta') {
                Swal.fire("Caja ya abierta", `Hora de apertura: ${data.hora_apertura}`, "warning");
            } else {
                Swal.fire({
                    title: "Abrir Caja",
                    html: `
                        <div id="billetes-container">
                            ${generarFilaBillete()}
                        </div>
                        <button onclick="agregarFilaBillete()" class="swal2-confirm swal2-styled" style="margin: 10px 0;">+ Agregar Billete</button>
                        <hr>
                        <p><strong>Total Córdobas:</strong> <span id="total-cordobas">0</span></p>
                        <p><strong>Total Dólares:</strong> <span id="total-dolares">0</span></p>
                    `,
                    focusConfirm: false,
                    preConfirm: () => {
                        const filas = document.querySelectorAll(".fila-billete");
                        const datos = [];

                        filas.forEach(fila => {
                            const denominacion = parseFloat(fila.querySelector(".denominacion").value);
                            const cantidad = parseInt(fila.querySelector(".cantidad").value);
                            const tipo = fila.querySelector(".tipo").value;

                            if (!isNaN(denominacion) && !isNaN(cantidad)) {
                                datos.push({ denominacion, cantidad, tipo });
                            }
                        });

                        return fetch('/abrir_caja/', {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken'),
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ billetes: datos })
                        }).then(res => res.json());
                    }
                }).then(result => {
                    if (result.value && result.value.success) {
                        document.getElementById("hora-apertura").textContent = result.value.hora_apertura;
                        window.location.href = '/dashboard';
                    } else if (result.value && result.value.error) {
                        Swal.fire("Error", result.value.error, "error");
                    }
                });

                // Escuchar eventos para actualizar los totales dinámicamente
                setTimeout(() => {
                    document.getElementById("billetes-container").addEventListener("input", actualizarTotales);
                }, 100);
            }
        });
});

// 🧩 Función para generar una fila de inputs
function generarFilaBillete() {
    return `
        <div class="fila-billete" style="margin-bottom: 10px; display: flex; gap: 5px;">
            <input type="number" class="denominacion swal2-input" placeholder="Denominación" style="width: 100px;" />
            <select class="tipo swal2-input" style="width: 120px;">
                <option value="cordobas">Córdobas</option>
                <option value="dolares">Dólares</option>
            </select>
            <input type="number" class="cantidad swal2-input" placeholder="Cantidad" style="width: 100px;" />
        </div>
    `;
}


// ➕ Agrega una nueva fila
function agregarFilaBillete() {
    const container = document.getElementById("billetes-container");
    container.insertAdjacentHTML('beforeend', generarFilaBillete());
    actualizarTotales(); // recalcula totales cuando se agrega
}

// 🧮 Calcula totales en tiempo real
function actualizarTotales() {
    let totalCordobas = 0;
    let totalDolares = 0;

    document.querySelectorAll(".fila-billete").forEach(fila => {
        const denominacion = parseFloat(fila.querySelector(".denominacion").value);
        const cantidad = parseInt(fila.querySelector(".cantidad").value);
        const tipo = fila.querySelector(".tipo").value;

        if (!isNaN(denominacion) && !isNaN(cantidad)) {
            const subtotal = denominacion * cantidad;
            if (tipo === "cordobas") {
                totalCordobas += subtotal;
            } else if (tipo === "dolares") {
                totalDolares += subtotal;
            }
        }
    });

    document.getElementById("total-cordobas").textContent = totalCordobas.toFixed(2);
    document.getElementById("total-dolares").textContent = totalDolares.toFixed(2);
}

// 🍪 Función auxiliar CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


let contadorInterval = null;

document.getElementById("btnCerrarCaja").addEventListener("click", function () {
    fetch('/verificar_caja/')
        .then(res => res.json())
        .then(data => {
            if (data.estado === 'cerrada') {
                Swal.fire('No hay una caja abierta actualmente');
            } else {
                Swal.fire({
                    title: 'Cerrar Caja',
                    html: `
                        <div id="billetes-cierre-container">
                            ${generarFilaBilleteCierre()}
                        </div>
                        <button onclick="agregarFilaBilleteCierre()" class="swal2-confirm swal2-styled" style="margin: 10px 0;">+ Agregar Billete</button>
                        <hr>
                        <p><strong>Total Córdobas:</strong> <span id="total-cordobas-cierre">0</span></p>
                        <p><strong>Total Dólares:</strong> <span id="total-dolares-cierre">0</span></p>
                    `,
                    showCancelButton: true,
                    confirmButtonText: 'Cerrar Caja',
                    preConfirm: () => {
                        const filas = document.querySelectorAll(".fila-billete-cierre");
                        const datos = [];

                        filas.forEach(fila => {
                            const denominacion = parseFloat(fila.querySelector(".denominacion").value);
                            const cantidad = parseInt(fila.querySelector(".cantidad").value);
                            const tipo = fila.querySelector(".tipo").value;

                            if (!isNaN(denominacion) && !isNaN(cantidad)) {
                                datos.push({ denominacion, cantidad, tipo });
                            }
                        });

                        if (datos.length === 0) {
                            Swal.showValidationMessage('Debe agregar al menos un billete válido');
                            return false;
                        }

                        return datos;
                    }
                }).then(result => {
                    if (result.isConfirmed) {
                        fetch('/cerrar_caja/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCookie('csrftoken')
                            },
                            body: JSON.stringify({ billetes: result.value })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire('Caja cerrada correctamente').then(() => {
                                    clearInterval(contadorInterval);
                                    document.getElementById("tiempo-abierta").textContent = "0m";
                                    window.location.href = '/dashboard';
                                });
                            } else {
                                Swal.fire('Error al cerrar la caja');
                            }
                        });
                    }
                });

                // Activar el cálculo automático de totales
                setTimeout(() => {
                    document.getElementById("billetes-cierre-container").addEventListener("input", actualizarTotalesCierre);
                }, 100);
            }
        });
});

// Función para generar una fila
function generarFilaBilleteCierre() {
    return `
        <div class="fila-billete-cierre" style="margin-bottom: 10px; display: flex; gap: 5px;">
            <input type="number" class="denominacion swal2-input" placeholder="Denominación" style="width: 100px;" />
            <select class="tipo swal2-input" style="width: 120px;">
                <option value="cordobas">Córdobas</option>
                <option value="dolares">Dólares</option>
            </select>
            <input type="number" class="cantidad swal2-input" placeholder="Cantidad" style="width: 100px;" />
        </div>
    `;
}

// Función para agregar más filas
function agregarFilaBilleteCierre() {
    const container = document.getElementById("billetes-cierre-container");
    container.insertAdjacentHTML('beforeend', generarFilaBilleteCierre());
    actualizarTotalesCierre();
}

// Calcula los totales de cierre
function actualizarTotalesCierre() {
    let totalCordobas = 0;
    let totalDolares = 0;

    document.querySelectorAll(".fila-billete-cierre").forEach(fila => {
        const denominacion = parseFloat(fila.querySelector(".denominacion").value);
        const cantidad = parseInt(fila.querySelector(".cantidad").value);
        const tipo = fila.querySelector(".tipo").value;

        if (!isNaN(denominacion) && !isNaN(cantidad)) {
            const subtotal = denominacion * cantidad;
            if (tipo === "cordobas") {
                totalCordobas += subtotal;
            } else if (tipo === "dolares") {
                totalDolares += subtotal;
            }
        }
    });

    document.getElementById("total-cordobas-cierre").textContent = totalCordobas.toFixed(2);
    document.getElementById("total-dolares-cierre").textContent = totalDolares.toFixed(2);
}


// Función auxiliar para CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // ¿Es el token que buscamos?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
    fetch('/verificar_caja/')
        .then(res => res.json())
        .then(data => {
            if (data.estado === 'abierta') {
                iniciarContadorDesde(data.hora_apertura);
                console.log(data.hora_apertura)
            }
        });
});

let contadorInte = null;

function iniciarContadorDesde(hora_apertura) {
    const apertura = new Date(hora_apertura);
    let ahora = new Date();
    let diferencia = Math.floor((ahora - apertura) / 1000);

    actualizarContador(diferencia);
    contadorInte = setInterval(() => {
        diferencia++;
        actualizarContador(diferencia);
    }, 1000);
}
function actualizarContador(segundos) {
    const horas = Math.floor(segundos / 3600).toString().padStart(2, '0');
    const minutos = Math.floor((segundos % 3600) / 60).toString().padStart(2, '0');
    const seg = (segundos % 60).toString().padStart(2, '0');
    document.getElementById("tiempo-abierta").textContent = `${horas}:${minutos}:${seg}`;
}