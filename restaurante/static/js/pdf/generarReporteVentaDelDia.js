document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('generar_reporte_venta_del_dia').addEventListener('click', generarReporteVentaDelDia);
});


function generarReporteVentaDelDia(event) {
    event.preventDefault();

    var productos = [];
    var platos = [];

    var filas = document.querySelectorAll('#datos tbody tr.main-row');
    const hoy = new Date();
    const dia = String(hoy.getDate()).padStart(2, '0');
    const mes = String(hoy.getMonth() + 1).padStart(2, '0');
    const anio = hoy.getFullYear();
    const fechaHoy = `${dia}/${mes}/${anio}`;  // Ej: "26/07/2025"


    filas.forEach(function(fila) {
        if (fila.style.display !== 'none') {
            var celdas = fila.querySelectorAll('td');
            
            // Extraemos el tipo: producto o plato
            const tipo = celdas[1].innerText.trim().toLowerCase();
            const fechaCompleta = celdas[3].innerText.trim();         // "26/07/2025 12:21 PM"
            const fechaSolo = fechaCompleta.split(' ')[0];            // "26/07/2025"
            
            if (fechaSolo !== fechaHoy) return; // Solo procesa los del día actual
            
            const limpiarMoneda = (texto) => texto.replace('C$', '').trim();
            
            let dato = {
                'numero': celdas[0].innerText,
                'tipo': tipo,
                'producto': celdas[2].innerText,
                'fecha':fechaCompleta,
                'precioCompra': limpiarMoneda(celdas[4].innerText),
                'cantidad': celdas[5].innerText,
                'precioVenta': limpiarMoneda(celdas[6].innerText),
                'subtotal': limpiarMoneda(celdas[7].innerText),
            };
            console.log(dato);

            if (tipo === 'producto') {
                productos.push(dato);
            } else if (tipo === 'plato') {
                platos.push(dato);
            }
        }
    });

    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(URL_IMPRIMIR_VENTAS_DEL_DIA, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ productos: productos, platos: platos })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.open(URL_PDF_VENTAS_DEL_DIA, '_blank');
        } else {
            alert('Error al generar registro. Inténtalo de nuevo.');
        }
    })
    .catch(error => {
        console.error('Error al generar registro:', error);
    });
}
