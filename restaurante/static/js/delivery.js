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

            let botonExtra = '';
            if (tipo === 'plato') {
                botonExtra = `
                    <button
                        typye="button"
                        data-id="${id}"
                        class="btnEnviarCocina text-blue-600 hover:text-blue-800 p-1 rounded-lg hover:bg-gray-200 ">
                        <svg class="size-6 text-blue-500" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M19 18H19.75H19ZM5 14.584H5.75C5.75 14.2859 5.57345 14.016 5.30028 13.8967L5 14.584ZM19 14.584L18.6997 13.8967C18.4265 14.016 18.25 14.2859 18.25 14.584H19ZM15.75 7C15.75 7.41421 16.0858 7.75 16.5 7.75C16.9142 7.75 17.25 7.41421 17.25 7H15.75ZM6.75 7C6.75 7.41421 7.08579 7.75 7.5 7.75C7.91421 7.75 8.25 7.41421 8.25 7H6.75ZM14 21.25C13.5858 21.25 13.25 21.5858 13.25 22C13.25 22.4142 13.5858 22.75 14 22.75V21.25ZM10 22.75C10.4142 22.75 10.75 22.4142 10.75 22C10.75 21.5858 10.4142 21.25 10 21.25V22.75ZM7 4.25C3.82436 4.25 1.25 6.82436 1.25 10H2.75C2.75 7.65279 4.65279 5.75 7 5.75V4.25ZM17 5.75C19.3472 5.75 21.25 7.65279 21.25 10H22.75C22.75 6.82436 20.1756 4.25 17 4.25V5.75ZM9 21.25C8.03599 21.25 7.38843 21.2484 6.90539 21.1835C6.44393 21.1214 6.24643 21.0142 6.11612 20.8839L5.05546 21.9445C5.51093 22.4 6.07773 22.5857 6.70552 22.6701C7.31174 22.7516 8.07839 22.75 9 22.75V21.25ZM4.25 18C4.25 18.9216 4.24841 19.6883 4.32991 20.2945C4.41432 20.9223 4.59999 21.4891 5.05546 21.9445L6.11612 20.8839C5.9858 20.7536 5.87858 20.5561 5.81654 20.0946C5.75159 19.6116 5.75 18.964 5.75 18H4.25ZM18.25 18C18.25 18.964 18.2484 19.6116 18.1835 20.0946C18.1214 20.5561 18.0142 20.7536 17.8839 20.8839L18.9445 21.9445C19.4 21.4891 19.5857 20.9223 19.6701 20.2945C19.7516 19.6883 19.75 18.9216 19.75 18H18.25ZM15 22.75C15.9216 22.75 16.6883 22.7516 17.2945 22.6701C17.9223 22.5857 18.4891 22.4 18.9445 21.9445L17.8839 20.8839C17.7536 21.0142 17.5561 21.1214 17.0946 21.1835C16.6116 21.2484 15.964 21.25 15 21.25V22.75ZM7 5.75C7.2137 5.75 7.42326 5.76571 7.6277 5.79593L7.84703 4.31205C7.57021 4.27114 7.28734 4.25 7 4.25V5.75ZM12 1.25C9.68949 1.25 7.72942 2.7421 7.02709 4.81312L8.44763 5.29486C8.94981 3.81402 10.3516 2.75 12 2.75V1.25ZM7.02709 4.81312C6.84722 5.34352 6.75 5.91118 6.75 6.5H8.25C8.25 6.07715 8.3197 5.67212 8.44763 5.29486L7.02709 4.81312ZM17 4.25C16.7127 4.25 16.4298 4.27114 16.153 4.31205L16.3723 5.79593C16.5767 5.76571 16.7863 5.75 17 5.75V4.25ZM12 2.75C13.6484 2.75 15.0502 3.81402 15.5524 5.29486L16.9729 4.81312C16.2706 2.7421 14.3105 1.25 12 1.25V2.75ZM15.5524 5.29486C15.6803 5.67212 15.75 6.07715 15.75 6.5H17.25C17.25 5.91118 17.1528 5.34352 16.9729 4.81312L15.5524 5.29486ZM5.75 18V14.584H4.25V18H5.75ZM5.30028 13.8967C3.79769 13.2402 2.75 11.7416 2.75 10H1.25C1.25 12.359 2.6705 14.3846 4.69972 15.2712L5.30028 13.8967ZM18.25 14.584L18.25 18H19.75L19.75 14.584H18.25ZM21.25 10C21.25 11.7416 20.2023 13.2402 18.6997 13.8967L19.3003 15.2712C21.3295 14.3846 22.75 12.359 22.75 10H21.25ZM15.75 6.5V7H17.25V6.5H15.75ZM6.75 6.5V7H8.25V6.5H6.75ZM15 21.25H14V22.75H15V21.25ZM10 21.25H9V22.75H10V21.25Z"/> 
                            <path d="M5 18H13M19 18H17" stroke="#155dfc" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </button>
                `;
            }

            nuevaFila.innerHTML = `
                <td class="text-center px-2 py-1 font-semibold wrap-break-word">1</td>
                <td class="text-center px-2 py-1 font-semibold wrap-break-word">${nombre}</td>
                <td class="text-center px-2 py-1 wrap-break-word">
                    <input type="number" ${maxAttr} min="1" value="1" class="cantidad w-14 text-center border rounded" />
                </td>
                <td class="text-center m-auto wrap-break-word">
                    C$<input type="number" min="1" value="${precio.toFixed(2)}" class="precio w-20 text-center border rounded" />
                </td>
                <td class="text-center px-2 py-1 subtotal font-semibold wrap-break-word p-2">C$ ${precio}</td>
                <td class="text-center px-2 py-1 wrap-break-word">
                
                    ${botonExtra}
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
        efectivo.placeholder = 'Referencia';
        efectivo.value = '';
    }
}