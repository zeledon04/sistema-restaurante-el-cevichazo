document.addEventListener('DOMContentLoaded', function () {
    const inputCodigo = document.getElementById('input-codigo');
    
    if (inputCodigo){
        inputCodigo.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                const codigo = inputCodigo.value.trim();
                if (!codigo) return;

                fetch(`/buscar-producto-codigo/?codigo=${encodeURIComponent(codigo)}&tipo=restaurante`)
                    .then(response => response.json())
                    .then(data => {
                        if (!data.success) {
                            Swal.fire({
                                icon : 'error',
                                title : data.message
                            });
                        } else {
                            renderProducto(data);  // Aquí se pasa todo el objeto
                        }
                        inputCodigo.value = '';
                    })
                    .catch(error => {
                        console.error('Error en la solicitud:', error);
                        alert('Error del servidor. Intenta de nuevo.');
                        inputCodigo.value = '';
                    });
            }
        });
    }

    function renderProducto(producto) {
        const tbody = document.querySelector('#datos tbody');
        tbody.innerHTML = `
            <tr class="hover:bg-gray-200 rounded-lg transition-colors">
                <td class="p-3 text-xl text-center">1</td>
                <td class="p-3 text-xl text-center">${producto.nombre}</td>
                <td class="text-center"><img src="${producto.imagen}" class="mx-auto block w-16 h-16"></td>
                <td class="p-3 text-xl text-center">${producto.categoria || '-'}</td>
                <td class="p-3 text-xl text-center">${producto.stock}</td>
                <td class="p-3 text-xl text-center">${producto.precio}</td>
                <td class="p-3 text-xl text-center">
                    <div class="grid grid-cols-2 gap-2 w-full">
                        <!-- tus botones aquí -->
                        <a href="#" onclick="window.location.href='actualizarProducto/${producto.productoid}'" class="btn">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-11 rounded-lg text-amber-300 hover:bg-gray-300 p-2  w-full">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                            </svg>
                        </a>   
                        <a href="#" onclick="eliminarProducto(${producto.productoid})" class="btn">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-11 rounded-lg text-red-500 hover:bg-gray-300 p-2 w-full">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                            </svg> 
                        </a>
                            
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-11 rounded-lg text-blue-500 hover:bg-gray-300 p-2 w-full">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        </svg>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-11 rounded-lg text-green-500 hover:bg-gray-300 p-2 w-full">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                        </svg>
                    </div>
                </td>
            </tr>
        `;
    }
});

function filtrarProductos() {
    const nombre = document.getElementById("filtroNombre").value;
    const categoria = document.getElementById("filtroCategoria").value;

    if (!nombre && !categoria) {
        window.location.href = '/productos/listar'
    }

    fetch(`/filtrar_productos/?nombre=${nombre}&categoria=${categoria}`)
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector("#datos tbody");
            tbody.innerHTML = "";

            if (data.length === 0) {
                tbody.innerHTML = `<tr><td colspan="8" class="text-center p-3 text-xl">No se encontraron productos</td></tr>`;
            } else {
                data.forEach(producto => {
                    tbody.innerHTML += `
                        <tr class="hover:bg-gray-200 rounded-lg transition-colors">
                            <td class="p-3 text-xl text-center">${producto.cont}</td>
                            <td class="p-3 text-xl text-center">${producto.nombre}</td>
                            <td class="text-center"><img src="/static/productos/${producto.rutafoto}?v=${producto.updated_at}" class="mx-auto block w-16 h-16"></td>
                            <td class="p-3 text-xl text-center">${producto.categoria}</td>
                            <td class="p-3 text-xl text-center">${producto.stock}</td>
                            <td class="p-3 text-xl text-center">${producto.precio}</td>
                            <td class="p-3 text-xl text-center">
                                <div class="grid grid-cols-2 gap-2 w-full">
                                    <!-- tus botones aquí -->
                                    <a href="#" onclick="window.location.href='actualizarProducto/${producto.productoid}'" class="btn">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-11 rounded-lg text-amber-300 hover:bg-gray-300 p-2  w-full">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                                        </svg>
                                    </a>   
                                    <a href="#" onclick="eliminarProducto(${producto.productoid})" class="btn">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-11 rounded-lg text-red-500 hover:bg-gray-300 p-2 w-full">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                    </svg> 

                                    </a>
                                    
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-11 rounded-lg text-blue-500 hover:bg-gray-300 p-2 w-full">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                    </svg>
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-11 rounded-lg text-green-500 hover:bg-gray-300 p-2 w-full">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                                    </svg>
                                </div>
                            </td>
                        </tr>
                    `;
                });
            }
        });
}

