
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("btn-agregar-mesa").addEventListener("click", () => {

        // Primero verificar si hay caja abierta
        fetch('/verificar_caja/')
            .then(res => res.json())
            .then(data => {
                if (data.estado === 'cerrada') {
                    Swal.fire({
                        title: 'Caja cerrada',
                        text: 'No se puede agregar una mesa porque la caja está cerrada.',
                        icon: 'warning',
                        confirmButtonText: 'Aceptar'
                    });
                    return; // detener ejecución
                }

                // Si hay caja abierta, continuar
                fetch('/api/meseros/')
                    .then(res => res.json())
                    .then(meseros => {
                        Swal.fire({
                            title: 'Agregar Mesa',
                            html: `
                                <div id="agregarMesa-container">
                                    ${agregarMesaFormHTML(meseros)}
                                </div>
                                <div class="flex items-center justify-center">
                                    <button id="confirmAgregarMesa" class="bg-amber-500 hover:bg-amber-600 text-white font-semibold p-2 w-[40%] flex items-center justify-center rounded gap-2" style="margin: 8px 0;">
                                        <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 w-6 h-6 mr-2">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                                        </svg>
                                        Agregar Mesa
                                    </button>
                                </div>
                            `,
                            showConfirmButton: false
                        });

                        // Delegación para botón dentro de Swal
                        document.getElementById("confirmAgregarMesa").addEventListener("click", () => {
                            const numero = document.getElementById("numeroMesa").value;
                            const mesero = document.getElementById("nombreMesero").value;
                            const cliente = document.getElementById("nombreCliente").value;

                            if (!numero || !cliente) {
                                Swal.fire("Campos requeridos", "Completa todos los campos obligatorios", "warning");
                                return;
                            }

                            fetch('/mesas/agregar/', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': getCookie('csrftoken')
                                },
                                body: JSON.stringify({
                                    numero,
                                    mesero,
                                    cliente
                                })
                            })
                            .then(res => res.json())
                            .then(data => {
                                if (data.message) {
                                    Swal.fire('Éxito', data.message, 'success')
                                    .then(() => {
                                        window.location.reload();
                                    }); // Recargar la página para ver la nueva mesa
                                } else {
                                    Swal.fire('Error', data.error || 'No se pudo agregar la mesa', 'error');
                                }
                            })
                            .catch(() => {
                                Swal.fire('Error', 'Error de red o servidor', 'error');
                            });
                        });
                    });
            });
    });
});


document.getElementById("btn-nueva-factura").addEventListener("click", () => {
    fetch('/verificar_caja/')
        .then(res => res.json())
        .then(data => {
            if (data.estado === 'cerrada') {
                Swal.fire({
                    title: 'Caja cerrada',
                    text: 'No se puede iniciar una nueva factura porque la caja está cerrada.',
                    icon: 'warning',
                    confirmButtonText: 'Aceptar'
                });
                return; // detener ejecución
            }

            // Si hay caja abierta, redirigir a la página de facturación
            window.location.href = '/cuentas/facturaUnica/';
        });
});


// Formulario en HTML con meseros
function agregarMesaFormHTML(meseros = []) {
    let opcionesMeseros = meseros.map(m => `<option value="${m.usuarioid}">${m.nombre}</option>`).join('');
    return `
    <div class='dark:bg-secondary-100 p-8 px-4 pt-2 rounded-xl'>
        <hr class='my-8 mt-2 border-gray-500/30' />
        <div class='flex items-center justify-between mb-8'>
            <div class='w-1/2'><p>N° Mesa <span class='text-red-600'>*</span></p></div>
            <div class='flex-1 flex items-center gap-4'>
                <input id="numeroMesa" type="number" required class='w-full py-2 px-4 outline-none rounded-lg dark:bg-secondary-900 bg-gray-300' placeholder='N° de Mesa' />
            </div>
        </div>
        <div class='flex items-center mb-8'>
            <div class='w-1/2'><p>Mesero <span class='text-red-600'>*</span></p></div>
            <div class='flex-1 flex items-center gap-4'>
                <select id="nombreMesero" class="w-full py-2 px-4 outline-none rounded-lg dark:bg-secondary-900 bg-gray-300">
                    ${opcionesMeseros}
                </select>
            </div>
        </div>
        <div class='flex items-center mb-8'>
            <div class='w-1/2'><p>Nombre Cliente <span class='text-red-600'>*</span></p></div>
            <div class='flex-1 flex items-center gap-4'>
                <input id="nombreCliente" type="text" required class='w-full py-2 px-4 outline-none rounded-lg dark:bg-secondary-900 bg-gray-300' placeholder='Nombre Cliente' />
            </div>
        </div>
        <hr class='my-8 mb-2 border-gray-500/30' />
    </div>`;
}

// Función CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        for (let cookie of document.cookie.split(';')) {
            const trimmed = cookie.trim();
            if (trimmed.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function calcularTiempoDesde(fechaStr) {
    const fecha = new Date(fechaStr);
    const ahora = new Date();
    const diff = Math.floor((ahora - fecha) / 1000); // diferencia en segundos

    const horas = Math.floor(diff / 3600);
    const minutos = Math.floor((diff % 3600) / 60);
    const segundos = diff % 60;

    if (horas > 0) {
      return `${horas}h ${minutos}m ${segundos}s`;
    } else if (minutos > 0) {
      return `${minutos}m ${segundos}s`;
    } else {
      return `${segundos}s`;
    }
  }

  function actualizarTiempos() {
    const elementos = document.querySelectorAll('.tiempo-activo');
    elementos.forEach(el => {
      const hora = el.dataset.hora;
      el.textContent = calcularTiempoDesde(hora);
    });
  }

  // Actualiza cada segundo
  setInterval(actualizarTiempos, 1000);
  // Llama inmediatamente al cargar
  actualizarTiempos();

