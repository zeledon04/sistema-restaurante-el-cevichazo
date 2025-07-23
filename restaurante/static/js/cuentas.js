document.addEventListener("DOMContentLoaded", function () {

    document.getElementById('buscador').addEventListener('input', function () {
        buscarProductos(this.value);
    });

    document.addEventListener('click', function (e) {
        const target = e.target.closest('.ver-detalles');
        if (target) {
            e.preventDefault();
            e.stopPropagation();

            const nombre = target.getAttribute('data-nombre');
            const categoria = target.getAttribute('data-categoria');
            const descripcion = target.getAttribute('data-descripcion');
            const imagen = target.getAttribute('data-imagen');

            Swal.fire({
                title: nombre,
                text: descripcion,
                html: `<img src="${imagen}" alt="${nombre}" class="w-40 h-40 object-contain mx-auto mb-4 rounded" />
                    <p><strong>Categoria:</strong> ${categoria}</p>
                    <p><strong>Descripción:</strong> ${descripcion}</p>
                `,
                confirmButtonText: 'Cerrar',
                width: '400px',
            });

        }

    });

    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.agregar-btn');

        if (!btn) {
            return;
        }

        const id = btn.getAttribute('data-id');
        const nombre = btn.getAttribute('data-nombre');
        const precio = parseFloat(btn.getAttribute('data-precio'));
        let stock = parseInt(btn.getAttribute('data-stock'));
        const tipo = btn.getAttribute('data-tipo');

        const tbody = document.getElementById('cuerpo-factura');

        const filaExistente = tbody.querySelector(`tr[data-id="${id}"][data-tipo="${tipo}"]`);

        if (filaExistente) {
            const cantidadInput = filaExistente.querySelector('.cantidad');
            let cantidad = parseInt(cantidadInput.value);
            if (tipo === 'plato') {
                stock = Infinity; // Para platos, no hay stock limitado
            }
            if (cantidad < stock) {
                cantidad++;
                cantidadInput.value = cantidad;

                const precioInput = filaExistente.querySelector('.precio');
                const nuevoPrecio = parseFloat(precioInput.value);
                const nuevoSubtotal = (cantidad * nuevoPrecio).toFixed(2);
                filaExistente.querySelector('.subtotal').textContent = `C$ ${nuevoSubtotal}`;

                actualizarTotal();

            } else {
                Swal.fire({
                    icon: 'warning',
                    title: 'Stock insuficiente',
                    text: `No hay suficiente stock de ${nombre}.`,
                });
            }
        } else {
            
            if (tipo === 'producto' && stock <= 0) {
                Swal.fire({
                    icon: 'warning',
                    title: 'Stock insuficiente',
                    text: `No hay suficiente stock de ${nombre}.`,
                });
                return;
            }

            const nuevaFila = document.createElement('tr');
            
            nuevaFila.classList.add('table', 'w-[100%]', 'table-fixed');
            nuevaFila.setAttribute('data-id', id);
            nuevaFila.setAttribute('data-nombre', nombre);
            nuevaFila.setAttribute('data-tipo', tipo);

            if (tipo === 'producto') {
                nuevaFila.setAttribute('data-stock', stock);
            }
            const maxAttr = tipo === 'producto' ? `max="${stock}"` : '';

            nuevaFila.innerHTML = `
                <td class="text-center px-2 py-1 font-semibold wrap-break-word">1</td>
                <td class="text-center px-2 py-1 font-semibold wrap-break-word">${nombre}</td>
                <td class="text-center px-2 py-1 wrap-break-word">
                    <input type="number" ${maxAttr} min="1" value="1" class="cantidad w-14 text-center border rounded" />
                </td>
                <td class="text-center m-auto wrap-break-word">
                    C$<input type="number" min="1" value="${precio}" class="precio w-20 text-center border rounded" />
                </td>
                <td class="text-center px-2 py-1 subtotal font-semibold wrap-break-word p-2">C$ ${precio}</td>
                <td class="text-center px-2 py-1 wrap-break-word">
                    <button class="text-red-600 hover:text-red-800 eliminar-item p-2 rounded-lg hover:bg-gray-200">
                        <svg fill="none" viewBox="0 0 24 24"
                            stroke-width="1.5" stroke="currentColor" class="size-6 text-red-500">
                            <path stroke-linecap="round" stroke-linejoin="round" 
                            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 
                            1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 
                            1-2.244 2.077H8.084a2.25 2.25 0 0 
                            1-2.244-2.077L4.772 5.79m14.456 
                            0a48.108 48.108 0 0 0-3.478-.397m-12 
                            .562c.34-.059.68-.114 1.022-.165m0 
                            0a48.11 48.11 0 0 1 3.478-.397m7.5 
                            0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 
                            51.964 0 0 0-3.32 0c-1.18.037-2.09 
                            1.022-2.09 2.201v.916m7.5 
                            0a48.667 48.667 0 0 0-7.5 0" />
                        </svg>  
                    </button>
                </td>
                `;
            tbody.appendChild(nuevaFila);

            const botonEliminar = nuevaFila.querySelector('.eliminar-item');
            botonEliminar.addEventListener('click', () => {
                // Añadir clases para la transición
                nuevaFila.classList.add('transition-opacity', 'duration-300', 'opacity-0');

                // Esperar a que termine la animación y luego eliminar el elemento
                setTimeout(() => {
                    nuevaFila.remove();
                    actualizarTotal(); // si tienes lógica para actualizar el total
                }, 500); // igual a duration-300 (300ms)
            });
        }
        
        actualizarTotal();

    });

    document.addEventListener('click', function (e) {
        if (!e.target.classList.contains('cantidad') && !e.target.classList.contains('precio')) {
            return;
        }

        const fila = e.target.closest('tr');
        if (!fila) {
            return;
        }
        const cantidadInput = fila.querySelector('.cantidad');
        const precioInput = fila.querySelector('.precio');

        const cantidad = parseFloat(cantidadInput?.value) || 1;
        const precio = parseFloat(precioInput?.value) || 0;

        const subtotal = (cantidad * precio).toFixed(2);
        const subtotalElem = fila.querySelector('.subtotal');
        if (subtotalElem) {
            subtotalElem.textContent = `C$ ${subtotal}`;
        }

        actualizarTotal();

    });

});

function actualizarTotal() {
    let total = 0;
    const filas = document.querySelectorAll('#cuerpo-factura tr');
    
    filas.forEach(fila => {
        const cantidadInput = fila.querySelector('.cantidad');
        const precioInput = fila.querySelector('.precio');
        
        const cantidad = cantidadInput ? parseFloat(cantidadInput.value) || 0 : 0;
        const precio = precioInput ? parseFloat(precioInput.value) || 0 : 0;
        
        total += cantidad * precio;
    });

    const totalFinal = document.getElementById('total-final');
    if (totalFinal) {
        totalFinal.textContent = `C$${total.toFixed(2)}`;
    }
}

function buscarProductos(query) {
    fetch(`/buscar_productos?q=${encodeURIComponent(query)}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        const contenedor = document.getElementById('productos-container');
        contenedor.innerHTML = ''; // Limpiar el contenedor

        data.productos.forEach((producto, index) => {
            const elemento = crearProducto(producto);
            elemento.classList.add('opacity-0', 'translate-y-5', 'transition-all', 'duration-500');
            contenedor.appendChild(elemento);

            void elemento.offsetHeight;

            setTimeout(() => {
                elemento.classList.remove('opacity-0', 'translate-y-5');
            }, index * 100); 
        });
    })

}

function crearProducto(producto) {
    const tempalte = document.createElement('template');
    tempalte.innerHTML = `
    <div class="flex flex-col justify-between rounded-lg shadow-sm h-auto max-h-[17rem] transition-all">
                
                <div class="flex-1 object-contain relative bg-gradient-to-tr from-gray-100 via-gray-300/90 to-gray-100 text-gray-800 rounded-lg rounded-b-none">
                    <img src="${producto.imagen}" alt="Toña" class="object-contain w-full h-32 rounded-lg rounded-b-none" />

                    <!-- Ícono de ojo -->
                    <button class="ver-detalles absolute top-2 right-2 p-1 bg-opacity-90 rounded-full cursor-pointer transition-all duration-200 hover:scale-110"
                            data-nombre="${producto.nombre}" 
                            data-categoria="${producto.categoria}"  
                            data-descripcion="${producto.descripcion}"
                            data-imagen="${producto.imagen}">
                        <svg fill="none" class="w-5 h-5" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                d="M2.458 12C3.732 7.943 7.523 5 12 5s8.268 2.943 9.542 7c-1.274 4.057-5.065 7-9.542 7s-8.268-2.943-9.542-7z" />
                        </svg>
                    </button>
                </div>

                <div class="flex flex-col items-center justify-between p-2 bg-white rounded-lg rounded-t-none shadow-md">
                    <div class="w-full flex items-center justify-center">
                        <h1 class="font-black">${producto.nombre}</h1>
                    </div>

                    <div class=" flex flex-col w-full items-center justify-between">
                        
                        <div class="flex flex-col items-center w-full justify-between">
                            <span class="font-bold text-green-600">C$ ${producto.precio}</span>
                        </div>

                        <div class="flex justify-between items-center w-full">

                            <p class="text-sm text-muted-foreground font-bold">${producto.tipo === "producto" ? `Stock: ${producto.stock}` : `Disponible`}</p>
                            
                            <button class="cursor-pointer agregar-btn flex justify-center items-center text-gray-900 py-2 hover:bg-gray-200 p-2 rounded-lg" data-id="${producto.id}" data-nombre="${producto.nombre}" data-precio="${producto.precio}" data-stock="${producto.stock}" data-tipo="${producto.tipo}">
                                <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5 flex mr-2">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                                </svg>
                                Agregar
                            </button>
                        </div>
                    </div>

                </div>
            </div>
    `.trim();
    return tempalte.content.firstChild;
}


function handleTipoPago() {
    const tipo = document.getElementById('tipo').value;
    const efectivo = document.getElementById('efectivo');
    const container = document.getElementById('extra-efectivo');

    // Limpiar el input mixto si existe
    container.innerHTML = '';

    if (tipo == '1') {
        efectivo.placeholder = 'Cordobas';
        efectivo.style.display = 'block';
    } else if (tipo == '2') {
        efectivo.placeholder = 'Dolares';
        efectivo.style.display = 'block';
    } else if (tipo == '3') {
        efectivo.placeholder = 'Cordobas';
        efectivo.style.display = 'block';

        const nuevoInput = document.createElement('input');
        nuevoInput.type = 'text';
        nuevoInput.id = 'efectivo-mixto';
        nuevoInput.placeholder = 'Dolares';
        efectivo.classList.remove('w-45');
        efectivo.classList.add('w-24');
        nuevoInput.className = 'p-2 dark:bg-secondary-900 bg-gray-300 outline-none rounded-lg w-24 mr-1';
        container.appendChild(nuevoInput);
    } else if (tipo == '4') {
        efectivo.style.display = 'none';
        efectivo.value = '';
    }
}