function actualizarVistaCocina(data) {
    const contenedor = document.getElementById("lista-pedidos");
    contenedor.innerHTML = ""; // Limpia antes de renderizar

    data.forEach(pedido => {
        const div = document.createElement("div");
        div.classList.add("flex",  "flex-col", "justify-between", "rounded-lg");
        div.innerHTML = `
            <div style="background:#ffeaa7; padding:10px; margin-bottom:5px; border-radius:8px;">
                <strong>Mesa:</strong> ${pedido.mesa}<br>
                <strong>Plato:</strong> ${pedido.plato}<br>
                <strong>Hora:</strong> ${pedido.hora}
            </div>

                <div class="flex-1 object-contain relative bg-gradient-to-tr from-gray-100 via-gray-300/90 to-gray-100 text-gray-800 rounded-lg rounded-b-none">
                    <img src="{% static 'image/pulpo.avif' %}" alt="defaultImage" class="object-contain w-full h-32 rounded-lg rounded-b-none" />
                    {% comment %} <img src="{% static 'productos/' %}{{ plato.rutafoto }}?v={{ plato.updated_at.timestamp }}" class="object-contain w-full h-32 rounded-lg rounded-b-none"> {% endcomment %}

                    <!-- Ícono de ojo -->
                    <button class="ver-detalles flex items-center justify-center px-2 py-1 font-medium gap-1 absolute top-2 right-2 bg-opacity-90 bg-yellow-100 text-yellow-800 border border-yellow-200 rounded-full cursor-pointer transition-all duration-200 hover:scale-110"
                            data-nombre="${plato.nombre}" 
                            data-categoria="${plato.categoria || ''}" 
                            data-descripcion="${plato.descripcion || 'Sin descripción'}"
                            data-imagen="${plato.imagen}">
                        
                        <svg class="size-3" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                        </svg>

                        <span class="text-xs">Pendiente</span>
                    </button>

                    <div class="absolute top-2 left-2">
                        <div class="bg-black/60 rounded-full px-2 text-white border-0">
                            # 1
                        </div>
                    </div>

                    <div class="absolute bottom-2 right-3">
                        <i>
                            <div class="font-semibold text-yellow-800">
                                Ceviche
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
                                    <span class="text-sm font-medium">Pendiente</span>
                                </div>

                                <div class="flex items-center gap-1 text-sm text-muted-foreground">
                                    <svg class="size-3 w-3 h-3 " fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                    </svg>
                                    <span>25 min</span>
                                </div>
                            
                                {% comment %} <span class="text-sm font-medium text-green-600">¡Servir ahora!</span> {% endcomment %}
                            </div>

                        </div>

                    </div>

                </div>


        `;
        contenedor.appendChild(div);
    });
}

// Polling cada 3 segundos
setInterval(() => {
    fetch('/cocina/estado/')
        .then(res => res.json())
        .then(data => actualizarVistaCocina(data))
        .catch(err => console.error('Error al cargar pedidos:', err));
}, 1000);