document.addEventListener("DOMContentLoaded", function () {

    document.getElementById('buscador').addEventListener('input', function () {
        buscarProductos(this.value);
    });

});

function buscarProductos(query) {

    fetch(`/buscar-productos?query=${encodeURIComponent(query)}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        const contenedor = document.getElementById('productos-container');
        contenedor.innerHTML = ''; // Limpiar el contenedor
        data.productos.forEach(producto => {
            contenedor.appendChild(crearProducto(producto));
        });
    })

}

function crearProducto(producto) {
    const tempalte = document.createElement('template');
    tempalte.innerHTML = `
    <div class="flex flex-col justify-between rounded-lg shadow-sm h-auto max-h-[16rem]">
                
                <div class="flex-1 object-contain relative bg-gradient-to-tr from-gray-100 via-gray-300/90 to-gray-100 text-gray-800 rounded-lg rounded-b-none">
                    <img src="${producto.imagen}" alt="Toña" class="object-contain w-full h-32 rounded-lg rounded-b-none" />

                    <!-- Ícono de ojo -->
                    <button class="absolute top-2 right-2 p-1 bg-opacity-90 rounded-full cursor-pointer transition-all duration-200 hover:scale-110"
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
                        <h1 class="font-black text-xl">Photo</h1>
                    </div>

                    <div class=" flex flex-col w-full items-center justify-between mt-2">
                        
                        <div class="flex flex-col items-center w-full justify-between">
                            <span class="font-bold text-2xl text-green-600">C$ 343.2</span>
                        </div>

                        <div class="flex justify-between items-center w-full mt-2">
                            <p class="text-sm text-muted-foreground font-bold">Stock: 100</p>
                            <button class="cursor-pointer agregar-btn flex justify-center items-center text-gray-900 py-2 hover:bg-gray-200 p-4 rounded-lg" data-id="${producto.id}" data-nombre="${producto.nombre}" data-precio="${producto.precio}" data-stock="${producto.stock}">
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