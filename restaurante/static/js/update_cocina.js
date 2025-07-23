let ultimaData = "";
const timestartMap = {}; // clave: cocinaid, valor: Date

function actualizarVistaCocina(data) {
   const nuevaData = JSON.stringify(data.datos);
    if (nuevaData === ultimaData) return; // No hay cambios, no actualizamos la vista
    
    ultimaData = nuevaData; // Actualizamos la última data

    const contenedor = document.getElementById("lista-pedidos");
    contenedor.innerHTML = ""; // Limpia antes de renderizar

    // console.log("Actualizando vista cocina con datos:", data.datos);

    data.datos.forEach(cocina => {
        // Si no hemos registrado una hora de inicio para esta cocina, la agregamos
        if (!timestartMap[cocina.cocinaid]) {
            timestartMap[cocina.cocinaid] = new Date(); // Marca hora de aparición
        }

        const div = document.createElement("div");
        div.classList.add("flex",  "flex-col", "justify-between", "rounded-lg");
        div.innerHTML = `

            <div class="flex-1 object-contain relative bg-gradient-to-tr from-gray-100 via-gray-300/90 to-gray-100 text-gray-800 rounded-lg rounded-b-none">
                <img src="${cocina.imagen}" alt="defaultImage" class="object-contain w-full h-32 rounded-lg rounded-b-none" />
                
                <button class="ver-detalles flex items-center justify-center px-2 py-1 font-medium gap-1 absolute top-2 right-2 bg-opacity-90 bg-yellow-100 text-yellow-800 border border-yellow-200 rounded-full cursor-pointer transition-all duration-200 hover:scale-110">
                    
                    <svg class="size-3" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                    
                    ${
                        cocina.estado === 1
                            ? `<span class="text-xs">Listo</span>`
                            : cocina.estado === 2
                                ? `<span class="text-xs">En Proceso</span>`
                                : `<span class="text-xs">Pendiente</span>`
                    }
                </button>

                <div class="absolute top-2 left-2">
                    <div class="bg-black/60 rounded-full px-2 text-white border-0">
                      ${cocina.mesa ? "# "+cocina.mesa : "Sin Mesa"}
                    </div>
                </div>

                <div class="absolute bottom-2 right-3">
                    <i>
                        <div class="font-semibold text-yellow-800">
                            ${cocina.plato}
                        </div>
                    </i>
                </div>

            </div>



            <div class="flex items-center justify-between w-full p-2 bg-white rounded-lg rounded-t-none shadow-md">

                <div class="flex w-full items-center justify-between mt-2">
                    
                    <div class="rounded-lg p-3  w-full bg-yellow-50 border border-gray-200 text-gray-800">
                        
                        <div class="flex items-center justify-between">
                            
                            <div class="flex items-center gap-2">
                                <svg class="size-3 w-4 h-4 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                </svg>
                                ${
                                    cocina.estado === 1
                                        ? `<span class="text-xs">Listo</span>`
                                        : cocina.estado === 2
                                            ? `<span class="text-xs">En Proceso</span>`
                                            : `<span class="text-xs">Pendiente</span>`
                                }
                            </div>

                            <div class="flex items-center gap-1 text-sm text-muted-foreground">
                                <svg class="size-3 w-3 h-3 " fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                </svg>
                                <span class="hora-viva" data-id="${cocina.cocinaid}">00:00:00</span>
                            </div>

                        </div>

                    </div>

                </div>

            </div>


        `;
        contenedor.appendChild(div);
    });
}


function actualizarHora() {
    const ahora = new Date();

    // Actualiza cada span con la clase 'hora-viva'
    // usando el timestartMap para calcular la diferencia de tiempo
    document.querySelectorAll('.hora-viva').forEach(span => {
        const id = span.dataset.id;
        const inicio = timestartMap[id];
        if (!inicio) return;

        const diff = Math.floor((ahora - inicio) / 1000); // segundos
        const horas = Math.floor(diff / 3600).toString().padStart(2, '0');
        const minutos = Math.floor((diff % 3600) / 60).toString().padStart(2, '0');
        const segundos = (diff % 60).toString().padStart(2, '0');

        span.textContent = `${horas}:${minutos}:${segundos}`;
    });
}

// Inicia hora viva actualizada
setInterval(actualizarHora, 1000);
actualizarHora(); // llamar al principio

// Polling cada 1 segundo
setInterval(() => {
    fetch('/cocina/estado/')
        .then(res => res.json())
        .then(data => 
            // console.log("Datos recibidos:", data)
            actualizarVistaCocina(data)
        )
        .catch(err => console.error('Error al cargar pedidos:', err));
}, 500); 