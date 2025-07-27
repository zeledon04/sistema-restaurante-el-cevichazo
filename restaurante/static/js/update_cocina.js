let ultimaData = "";
const timestartMap = {}; // clave: cocinaid, valor: Date

function actualizarVistaCocina(data) {
   const nuevaData = JSON.stringify(data.datos);
    if (nuevaData === ultimaData) return; // No hay cambios, no actualizamos la vista
    
    ultimaData = nuevaData; // Actualizamos la última data

    const contPendientes = document.getElementById("pedidos-pendientes");
    const contProceso = document.getElementById("pedidos-proceso");
    const contListos = document.getElementById("pedidos-listos");

    contPendientes.innerHTML = "";
    contProceso.innerHTML = "";
    contListos.innerHTML = ""; // Limpia antes de renderizar

    
    // console.log("Actualizando vista cocina con datos:", data.datos);
    
    data.datos.forEach(cocina => {
        // Si no hemos registrado una hora de inicio para esta cocina, la agregamos

        const fechaLocal = new Date(cocina.hora.replace(' ', 'T'));  // -> Date válido
        const hora = fechaLocal.toISOString();

        const estilo = obtenerEstilosPorEstado(cocina.estado);
        const card  = document.createElement("div");
        card .classList.add("flex",  "flex-col", "justify-between", "rounded-lg");
        card .innerHTML = `

            <div class="flex-1 object-contain relative bg-gradient-to-tr from-gray-100 via-gray-300/90 to-gray-100 text-gray-800 rounded-lg rounded-b-none">
                <img src="${cocina.imagen}" alt="defaultImage" class="object-contain w-full h-32 rounded-lg rounded-b-none" />
                
                <button data-id="${cocina.cocinaid}" class="ver-detalles flex items-center justify-center px-2 py-1 font-medium gap-1 absolute top-2 right-2 bg-opacity-90 ${estilo.bg} ${estilo.text} border ${estilo.border} rounded-full cursor-pointer transition-all duration-200 hover:scale-110">
                    
                    ${cocina.estado === 0
                        ?
                        `<svg class="size-3" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                        </svg>`
                        : cocina.estado === 2
                        ?
                        `<svg class="size-3" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M19 18H19.75H19ZM5 14.584H5.75C5.75 14.2859 5.57345 14.016 5.30028 13.8967L5 14.584ZM19 14.584L18.6997 13.8967C18.4265 14.016 18.25 14.2859 18.25 14.584H19ZM15.75 7C15.75 7.41421 16.0858 7.75 16.5 7.75C16.9142 7.75 17.25 7.41421 17.25 7H15.75ZM6.75 7C6.75 7.41421 7.08579 7.75 7.5 7.75C7.91421 7.75 8.25 7.41421 8.25 7H6.75ZM14 21.25C13.5858 21.25 13.25 21.5858 13.25 22C13.25 22.4142 13.5858 22.75 14 22.75V21.25ZM10 22.75C10.4142 22.75 10.75 22.4142 10.75 22C10.75 21.5858 10.4142 21.25 10 21.25V22.75ZM7 4.25C3.82436 4.25 1.25 6.82436 1.25 10H2.75C2.75 7.65279 4.65279 5.75 7 5.75V4.25ZM17 5.75C19.3472 5.75 21.25 7.65279 21.25 10H22.75C22.75 6.82436 20.1756 4.25 17 4.25V5.75ZM9 21.25C8.03599 21.25 7.38843 21.2484 6.90539 21.1835C6.44393 21.1214 6.24643 21.0142 6.11612 20.8839L5.05546 21.9445C5.51093 22.4 6.07773 22.5857 6.70552 22.6701C7.31174 22.7516 8.07839 22.75 9 22.75V21.25ZM4.25 18C4.25 18.9216 4.24841 19.6883 4.32991 20.2945C4.41432 20.9223 4.59999 21.4891 5.05546 21.9445L6.11612 20.8839C5.9858 20.7536 5.87858 20.5561 5.81654 20.0946C5.75159 19.6116 5.75 18.964 5.75 18H4.25ZM18.25 18C18.25 18.964 18.2484 19.6116 18.1835 20.0946C18.1214 20.5561 18.0142 20.7536 17.8839 20.8839L18.9445 21.9445C19.4 21.4891 19.5857 20.9223 19.6701 20.2945C19.7516 19.6883 19.75 18.9216 19.75 18H18.25ZM15 22.75C15.9216 22.75 16.6883 22.7516 17.2945 22.6701C17.9223 22.5857 18.4891 22.4 18.9445 21.9445L17.8839 20.8839C17.7536 21.0142 17.5561 21.1214 17.0946 21.1835C16.6116 21.2484 15.964 21.25 15 21.25V22.75ZM7 5.75C7.2137 5.75 7.42326 5.76571 7.6277 5.79593L7.84703 4.31205C7.57021 4.27114 7.28734 4.25 7 4.25V5.75ZM12 1.25C9.68949 1.25 7.72942 2.7421 7.02709 4.81312L8.44763 5.29486C8.94981 3.81402 10.3516 2.75 12 2.75V1.25ZM7.02709 4.81312C6.84722 5.34352 6.75 5.91118 6.75 6.5H8.25C8.25 6.07715 8.3197 5.67212 8.44763 5.29486L7.02709 4.81312ZM17 4.25C16.7127 4.25 16.4298 4.27114 16.153 4.31205L16.3723 5.79593C16.5767 5.76571 16.7863 5.75 17 5.75V4.25ZM12 2.75C13.6484 2.75 15.0502 3.81402 15.5524 5.29486L16.9729 4.81312C16.2706 2.7421 14.3105 1.25 12 1.25V2.75ZM15.5524 5.29486C15.6803 5.67212 15.75 6.07715 15.75 6.5H17.25C17.25 5.91118 17.1528 5.34352 16.9729 4.81312L15.5524 5.29486ZM5.75 18V14.584H4.25V18H5.75ZM5.30028 13.8967C3.79769 13.2402 2.75 11.7416 2.75 10H1.25C1.25 12.359 2.6705 14.3846 4.69972 15.2712L5.30028 13.8967ZM18.25 14.584L18.25 18H19.75L19.75 14.584H18.25ZM21.25 10C21.25 11.7416 20.2023 13.2402 18.6997 13.8967L19.3003 15.2712C21.3295 14.3846 22.75 12.359 22.75 10H21.25ZM15.75 6.5V7H17.25V6.5H15.75ZM6.75 6.5V7H8.25V6.5H6.75ZM15 21.25H14V22.75H15V21.25ZM10 21.25H9V22.75H10V21.25Z"/>
                            <path d="M5 18H13M19 18H17" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>`
                        :` <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-3">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                        </svg>`
                        
                    }
                    <span class="text-xs">${estilo.label}</span>
                </button>

                <div class="absolute top-2 left-2">
                    <div class="bg-black/60 rounded-full px-2 text-white border-0">
                      ${cocina.mesa ? "# " + cocina.mesa : "Sin Mesa"}
                    </div>
                </div>

                <div class="absolute bottom-2 right-3">
                    <i>
                        <div class="font-semibold ${estilo.text}">
                            ${cocina.plato}
                        </div>
                    </i>
                </div>

            </div>



            <div class="flex items-center justify-between w-full p-2 bg-white rounded-lg rounded-t-none shadow-md">

                <div class="flex w-full items-center justify-between">
                    
                    <div class="rounded-lg p-2 w-full ${estilo.bg} border border-gray-200 text-gray-800">
                        
                        <div class="flex items-center justify-between">
                            
                            <div class="flex items-center gap-2">
                                
                                ${cocina.estado === 0
                                    ?
                                    `<svg class="size-3 w-4 h-4 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                    </svg>`
                                    : cocina.estado === 2
                                    ?
                                    `<svg class="size-3 w-4 h-4 text-muted-foreground" viewBox="0 0 24 24" fill="currentColor">
                                        <path d="M19 18H19.75H19ZM5 14.584H5.75C5.75 14.2859 5.57345 14.016 5.30028 13.8967L5 14.584ZM19 14.584L18.6997 13.8967C18.4265 14.016 18.25 14.2859 18.25 14.584H19ZM15.75 7C15.75 7.41421 16.0858 7.75 16.5 7.75C16.9142 7.75 17.25 7.41421 17.25 7H15.75ZM6.75 7C6.75 7.41421 7.08579 7.75 7.5 7.75C7.91421 7.75 8.25 7.41421 8.25 7H6.75ZM14 21.25C13.5858 21.25 13.25 21.5858 13.25 22C13.25 22.4142 13.5858 22.75 14 22.75V21.25ZM10 22.75C10.4142 22.75 10.75 22.4142 10.75 22C10.75 21.5858 10.4142 21.25 10 21.25V22.75ZM7 4.25C3.82436 4.25 1.25 6.82436 1.25 10H2.75C2.75 7.65279 4.65279 5.75 7 5.75V4.25ZM17 5.75C19.3472 5.75 21.25 7.65279 21.25 10H22.75C22.75 6.82436 20.1756 4.25 17 4.25V5.75ZM9 21.25C8.03599 21.25 7.38843 21.2484 6.90539 21.1835C6.44393 21.1214 6.24643 21.0142 6.11612 20.8839L5.05546 21.9445C5.51093 22.4 6.07773 22.5857 6.70552 22.6701C7.31174 22.7516 8.07839 22.75 9 22.75V21.25ZM4.25 18C4.25 18.9216 4.24841 19.6883 4.32991 20.2945C4.41432 20.9223 4.59999 21.4891 5.05546 21.9445L6.11612 20.8839C5.9858 20.7536 5.87858 20.5561 5.81654 20.0946C5.75159 19.6116 5.75 18.964 5.75 18H4.25ZM18.25 18C18.25 18.964 18.2484 19.6116 18.1835 20.0946C18.1214 20.5561 18.0142 20.7536 17.8839 20.8839L18.9445 21.9445C19.4 21.4891 19.5857 20.9223 19.6701 20.2945C19.7516 19.6883 19.75 18.9216 19.75 18H18.25ZM15 22.75C15.9216 22.75 16.6883 22.7516 17.2945 22.6701C17.9223 22.5857 18.4891 22.4 18.9445 21.9445L17.8839 20.8839C17.7536 21.0142 17.5561 21.1214 17.0946 21.1835C16.6116 21.2484 15.964 21.25 15 21.25V22.75ZM7 5.75C7.2137 5.75 7.42326 5.76571 7.6277 5.79593L7.84703 4.31205C7.57021 4.27114 7.28734 4.25 7 4.25V5.75ZM12 1.25C9.68949 1.25 7.72942 2.7421 7.02709 4.81312L8.44763 5.29486C8.94981 3.81402 10.3516 2.75 12 2.75V1.25ZM7.02709 4.81312C6.84722 5.34352 6.75 5.91118 6.75 6.5H8.25C8.25 6.07715 8.3197 5.67212 8.44763 5.29486L7.02709 4.81312ZM17 4.25C16.7127 4.25 16.4298 4.27114 16.153 4.31205L16.3723 5.79593C16.5767 5.76571 16.7863 5.75 17 5.75V4.25ZM12 2.75C13.6484 2.75 15.0502 3.81402 15.5524 5.29486L16.9729 4.81312C16.2706 2.7421 14.3105 1.25 12 1.25V2.75ZM15.5524 5.29486C15.6803 5.67212 15.75 6.07715 15.75 6.5H17.25C17.25 5.91118 17.1528 5.34352 16.9729 4.81312L15.5524 5.29486ZM5.75 18V14.584H4.25V18H5.75ZM5.30028 13.8967C3.79769 13.2402 2.75 11.7416 2.75 10H1.25C1.25 12.359 2.6705 14.3846 4.69972 15.2712L5.30028 13.8967ZM18.25 14.584L18.25 18H19.75L19.75 14.584H18.25ZM21.25 10C21.25 11.7416 20.2023 13.2402 18.6997 13.8967L19.3003 15.2712C21.3295 14.3846 22.75 12.359 22.75 10H21.25ZM15.75 6.5V7H17.25V6.5H15.75ZM6.75 6.5V7H8.25V6.5H6.75ZM15 21.25H14V22.75H15V21.25ZM10 21.25H9V22.75H10V21.25Z"/>
                                        <path d="M5 18H13M19 18H17" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                                    </svg>`
                                    :` <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-3 w-4 h-4 text-muted-foreground">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                    </svg>`
                                    
                                }

                                <span class="text-sm font-semibold">${estilo.label}</span>
                            </div>

                            ${cocina.estado != 1 ?
                            `<div class="flex items-center gap-1 text-sm text-muted-foreground">
                                <svg class="size-3 w-3 h-3" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                </svg>
                                <span class="hora-viva" data-hora="${hora}"></span>
                            </div>`
                            : `<span class="text-sm font-medium text-green-600">¡Servir ahora!</span>`
                            }

                        </div>

                    </div>

                </div>

            </div>


        `;

        if (cocina.estado === 0) {
            contPendientes.appendChild(card);
        } else if (cocina.estado === 2) {
            contProceso.appendChild(card);
        } else if (cocina.estado === 1) {
            contListos.appendChild(card);
        }

    });

    // Agrega el evento a los botones de ver detalles
    // para cambiar el estado de la cocina
    document.querySelectorAll(".ver-detalles").forEach(boton => {
        boton.addEventListener("click", async (e) => {
            const cocinaId = e.currentTarget.dataset.id;

            let nuevoEstado;
            if (e.currentTarget.innerText.includes("Pendiente")) {
                nuevoEstado = 2;
            } else if (e.currentTarget.innerText.includes("En Proceso")) {
                nuevoEstado = 1;
            } else if (e.currentTarget.innerText.includes("Listo")) {
                nuevoEstado = 3
            }

            await fetch(`/cambiar-estado-cocina/${cocinaId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({ estado: nuevoEstado })
            });

            // Ya que el polling actualiza cada 0.5s, no necesitas esto,
            // pero si quieres forzar la actualización inmediata:
            fetch('/cocina/estado/')
                .then(res => res.json())
                .then(data => actualizarVistaCocina(data));
        });
    });
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
    const elementos = document.querySelectorAll('.hora-viva');
    elementos.forEach(el => {
      const hora = el.dataset.hora;
      el.textContent = calcularTiempoDesde(hora);
    });
  }

  // Actualiza cada segundo
  setInterval(actualizarTiempos, 1000);
  // Llama inmediatamente al cargar
  actualizarTiempos();


// Polling cada 1 segundo
setInterval(() => {
    fetch('/cocina/estado/')
        .then(res => res.json())
        .then(data => 
            actualizarVistaCocina(data),
            // console.log("Datos recibidos:", data)
        )
        .catch(err => console.error('Error al cargar pedidos:', err));
}, 2500); 

// Función para obtener estilos según el estado, solo para eso.
function obtenerEstilosPorEstado(estado) {
    switch (estado) {
        case 0: // Pendiente
            return {
                color: "yellow",
                bg: "bg-yellow-50",
                border: "border-yellow-200",
                text: "text-yellow-800",
                label: "Pendiente",
            };
        case 2: // En Proceso
            return {
                color: "blue",
                bg: "bg-blue-50",
                border: "border-blue-200",
                text: "text-blue-800",
                label: "En Proceso",
            };
        case 1: // Listo
            return {
                color: "green",
                bg: "bg-green-50",
                border: "border-green-200",
                text: "text-green-800",
                label: "Listo",
            };
    }
}

// Esto para la seguridad, el crf normal de los formularios.
function getCookie(name) {
  const cookieString = document.cookie;
  const cookies = cookieString.split("; ");
  for (let c of cookies) {
    const [k, v] = c.split("=");
    if (k === name) return v;
  }
  return "";
}