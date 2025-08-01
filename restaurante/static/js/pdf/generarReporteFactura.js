document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('generar_reporte_factura').addEventListener('click', generarReporteFactura);
    });
    
    function generarReporteFactura(event) {
        event.preventDefault();
    
        var datos = [];
        var filas = document.querySelectorAll('#datos tbody tr.main-row');
    
        filas.forEach(function(fila) {
            if (fila.style.display !== 'none') {
                var celdas = fila.querySelectorAll('td');
                const limpiarMoneda = (texto) => texto.replace('C$', '').trim();
                var dato = {
                    'numero': celdas[0].innerText,
                    'numFactura': celdas[1].innerText,
                    'vendedor': celdas[2].innerText,
                    'cliente': celdas[3].innerText,
                    'fecha': celdas[4].innerText,
                    'hora': celdas[5].innerText,
                    'productos': celdas[6].innerText,
                    'subtotal': limpiarMoneda(celdas[7].innerText),
                };
                console.log(dato);
                datos.push(dato);
            }
        });
    
        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        console.log(csrfToken);
    
        fetch(URL_IMPRIMIR_FACTURAS, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ items: datos })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.open(URL_PDF_FACTURA, '_blank');
            } else {
                alert('Error al generar registro. Inténtalo de nuevo.');
            }
        })
        .catch(error => {
            console.error('Error al generar registro:', error);
        });
    }