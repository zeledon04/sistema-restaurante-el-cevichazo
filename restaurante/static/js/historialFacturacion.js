function asignarEventosVerDetalle() {
    document.querySelectorAll('.ver-detalle').forEach(boton => {
        boton.addEventListener('click', function () {
            const facturaId = this.dataset.id;

            fetch(`/factura/detalle/${facturaId}/`)
                .then(res => res.json())
                .then(data => {
                    let html = `
                        <div style="text-align:left; font-family: monospace;">
                            <strong>Factura No:</strong> ${data.nofactura}<br>
                            <strong>Cliente:</strong> ${data.cliente}<br>
                            <strong>Fecha:</strong> ${data.fecha}<br><br>
                            <table style="width:100%; border-collapse: collapse; font-size:13px;">
                                <thead>
                                    <tr>
                                        <th style="border-bottom:1px solid #000;">Producto</th>
                                        <th style="border-bottom:1px solid #000;">Uds</th>
                                        <th style="border-bottom:1px solid #000;">Precio</th>
                                        <th style="border-bottom:1px solid #000;">SubT</th>
                                    </tr>
                                </thead>
                                <tbody>`;

                    const renderFila = (p) => `
                        <tr>
                            <td>${p.nombre}</td>
                            <td>${p.cantidad}</td>
                            <td>C$${p.precio.toFixed(2)}</td>
                            <td>C$${p.subtotal.toFixed(2)}</td>
                        </tr>`;

                    data.productos.forEach(p => html += renderFila(p));
                    data.platos.forEach(p => html += renderFila(p));

                    html += `
                                </tbody>
                            </table>
                            <br>
                            <strong>Total:</strong> C$${data.total.toFixed(2)}<br>`;

                    if (data.tipopago == 4) {
                        html += `<strong>Pago con:</strong> Tarjeta de Crédito<br>`;
                    } else {
                        html += `
                            <strong>Tasa de Cambio:</strong> C$${data.tasacambio.toFixed(2)}<br>
                            <strong>Efectivo Dólares:</strong> $${data.efectivodolares.toFixed(2)}<br>
                            <strong>Efectivo Córdobas:</strong> C$${data.efectivocordobas.toFixed(2)}<br>
                            <strong>Cambio:</strong> C$${data.cambio.toFixed(2)}`;
                    }

                    html += `</div>`;

                    Swal.fire({
                        title: 'Detalle de Factura',
                        html: html,
                        width: 600,
                        confirmButtonText: 'Cerrar',
                        customClass: {
                            popup: 'swal-wide'
                        }
                    });
                })
                .catch(err => {
                    console.error('Error al cargar el detalle de la factura:', err);
                    Swal.fire('Error', 'No se pudo cargar el detalle de la factura.', 'error');
                });
        });
    });
}



document.addEventListener('DOMContentLoaded', function () {
    asignarEventosVerDetalle(); // evento inicial

    const filtroVendedor = document.getElementById('filtroVendedor');
    const filtroFecha = document.getElementById('filtroFecha');

    function obtenerFacturas(usuario_id = '', filtro_fecha = '', fecha_inicio = '', fecha_fin = '') {
        const params = new URLSearchParams();
        if (usuario_id) params.append('usuario_id', usuario_id);
        if (filtro_fecha) params.append('filtro_fecha', filtro_fecha);
        if (fecha_inicio) params.append('fecha_inicio', fecha_inicio);
        if (fecha_fin) params.append('fecha_fin', fecha_fin);

        fetch(`/filtrar_facturas/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                const tbody = document.querySelector('#datos tbody');
                tbody.innerHTML = '';
                data.facturas.forEach((factura, index) => {
                    const row = document.createElement('tr');
                    row.classList.add('main-row');
                    row.innerHTML = `
                        <td class="p-2 text-xl text-center">${index + 1}</td>
                        <td class="p-2 text-xl text-center">${factura.facturaid}</td>
                        <td class="p-2 text-xl text-center">${factura.usuario}</td>
                        <td class="p-2 text-xl text-center">${factura.cliente}</td>
                        <td class="p-2 text-xl text-center">${factura.fecha}</td>
                        <td class="p-2 text-xl text-center">${factura.hora}</td>
                        <td class="p-2 text-xl text-center">${factura.cantProductos}</td>
                        <td class="p-2 text-xl text-center">C$ ${factura.total.toFixed(2)}</td>
                        <td class="p-2 text-xl text-center">
                        <div class="grid grid-cols-3 gap-2 w-full">
                            <svg onclick="anularFactura(${factura.facturaid})" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="cursor-pointer size-12 rounded-lg text-red-500 hover:bg-gray-300 p-1 w-full">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                            </svg>

                            <svg xmlns="http://www.w3.org/2000/svg" data-id="${factura.facturaid}" style="cursor:pointer;" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-12 rounded-lg text-blue-950 hover:bg-gray-300 p-1 w-full ver-detalle">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                            </svg>

                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-12 rounded-lg text-green-500 hover:bg-gray-300 p-1 w-full">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6.72 13.829c-.24.03-.48.062-.72.096m.72-.096a42.415 42.415 0 0 1 10.56 0m-10.56 0L6.34 18m10.94-4.171c.24.03.48.062.72.096m-.72-.096L17.66 18m0 0 .229 2.523a1.125 1.125 0 0 1-1.12 1.227H7.231c-.662 0-1.18-.568-1.12-1.227L6.34 18m11.318 0h1.091A2.25 2.25 0 0 0 21 15.75V9.456c0-1.081-.768-2.015-1.837-2.175a48.055 48.055 0 0 0-1.913-.247M6.34 18H5.25A2.25 2.25 0 0 1 3 15.75V9.456c0-1.081.768-2.015 1.837-2.175a48.041 48.041 0 0 1 1.913-.247m10.5 0a48.536 48.536 0 0 0-10.5 0m10.5 0V3.375c0-.621-.504-1.125-1.125-1.125h-8.25c-.621 0-1.125.504-1.125 1.125v3.659M18 10.5h.008v.008H18V10.5Zm-3 0h.008v.008H15V10.5Z" />
                            </svg>
                        </div>
                    </td>
                    `;
                    tbody.appendChild(row);
                });

                asignarEventosVerDetalle();
            });
        

    }

    filtroVendedor.addEventListener('change', function () {
        const usuario_id = this.value;
        const filtro_fecha = filtroFecha.value;

        if (!filtro_fecha && !usuario_id) {
            window.location.href = '/Factura/historial';
            return;
        }
        obtenerFacturas(usuario_id, filtro_fecha);
    });

    filtroFecha.addEventListener('change', function () {
        const filtro_fecha = this.value;
        const usuario_id = filtroVendedor.value;
        console.log(filtro_fecha);
        console.log(usuario_id);
        if (!filtro_fecha && !usuario_id) {
            window.location.href = '/Factura/historial';
            return;
        }
        if (filtro_fecha === 'rango') {
            Swal.fire({
                title: 'Seleccionar Rango de Fechas',
                html:
                    '<h3>Fecha Inicio</h3>' +
                    '<input type="date" id="fechaInicio" class="swal2-input" placeholder="Desde">' +
                    '<h3 style="margin-top: 20px;">Fecha Fin</h3>' +
                    '<input type="date" id="fechaFin" class="swal2-input" placeholder="Hasta">',
                confirmButtonText: 'Filtrar',
                focusConfirm: false,
                preConfirm: () => {
                    const inicio = document.getElementById('fechaInicio').value;
                    const fin = document.getElementById('fechaFin').value;
                    if (!inicio || !fin) {
                        Swal.showValidationMessage('Debes ingresar ambas fechas');
                        return false;
                    }
                    
                    obtenerFacturas(usuario_id, filtro_fecha, inicio, fin, 5);
                },
                didClose: () => {
                    
                    filtroFecha.value = '';
                }
            });
        } else {
            obtenerFacturas(usuario_id, filtro_fecha);
        }
    });

    
});

