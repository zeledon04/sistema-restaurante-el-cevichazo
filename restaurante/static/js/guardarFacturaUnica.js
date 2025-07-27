async function guardarFactura() {
    const filas = document.querySelectorAll('#tabla-factura tbody tr');
    const productos = [];

    let hayError = false;
    let stockError = false;
    let tasaCambio = 0;

    try {
        const response = await fetch('/api/tasa-cambio/');
        const data = await response.json();

        if (data.tasaCambio != null && data.tasaCambio !== undefined) {
            tasaCambio = data.tasaCambio;
        } else {
            Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo obtener la tasa de cambio.' });
            return;
        }
    } catch (error) {
        Swal.fire({ icon: 'error', title: 'Error', text: 'Error al obtener la tasa de cambio.' });
        return;
    }

    filas.forEach(fila => {
        const tipo = fila.getAttribute('data-tipo');
        const cantidad = parseInt(fila.querySelector('.cantidad').value);
        const precio = parseFloat(fila.querySelector('.precio').value);

        if (tipo === 'producto') {
            const stock = parseInt(fila.getAttribute('data-stock')) || 0;
            if (cantidad > stock) {
                stockError = true;
                return;
            }
        }

        if (isNaN(cantidad) || isNaN(precio) || cantidad <= 0 || precio <= 0) {
            hayError = true;
            return;
        }

        productos.push({
            id: parseInt(fila.getAttribute('data-id')),
            nombre: fila.getAttribute('data-nombre'),
            cantidad: cantidad,
            precio: precio,
            tipo: tipo
        });
    });

    if (stockError) {
        Swal.fire({ icon: 'warning', title: 'Stock Insuficiente' });
        return;
    }

    if (productos.length === 0) {
        Swal.fire({ icon: 'warning', title: 'Agregue productos a la factura' });
        return;
    }

    if (hayError) {
        Swal.fire({ icon: 'error', title: 'Error', text: 'Por favor, revise los campos de cantidad y precio.' });
        return;
    }

    const totalTexto = document.getElementById('total-final').textContent.trim();
    const total = parseFloat(totalTexto.replace("C$", "").replace(",", ""));

    let cliente = document.getElementById('nombre-cliente').value.trim();
    if (!cliente) {
        cliente = 'Generico';
    }

    const tipoPago = document.getElementById('tipo').value;
    let efectivoCordoba = 0;
    let efectivoDolar = 0;
    let cambio = 0;

    if (tipoPago === '1') {
        efectivoCordoba = parseFloat(document.getElementById('efectivo').value) || 0;
        if (efectivoCordoba == 0) {
            efectivoCordoba = total;
            cambio = 0;
        } else {
            if (efectivoCordoba < total) {
                Swal.fire({ icon: 'error', title: 'Error', text: 'Monto insuficiente em córdobas' });
                return;
            }
            cambio = efectivoCordoba - total;
        }
    } else if (tipoPago === '2') {
        efectivoDolar = parseFloat(document.getElementById('efectivo').value.trim()) || 0;
        const totalEnCordoba = efectivoDolar * tasaCambio;
        if (efectivoDolar === 0 || totalEnCordoba < total) {
            Swal.fire({ icon: 'error', title: 'Error', text: 'Monto insuficiente en dólares' });
            return;
        }
        cambio = totalEnCordoba - total;
    } else if (tipoPago === '3') {
        efectivoCordoba = parseFloat(document.getElementById('efectivo').value.trim()) || 0;
        efectivoDolar = parseFloat(document.getElementById('efectivo-mixto').value.trim()) || 0;
        const totalEnCordoba = efectivoCordoba + (efectivoDolar * tasaCambio);
        if (efectivoCordoba === 0 || efectivoDolar === 0 || totalEnCordoba < total) {
            Swal.fire({ icon: 'error', title: 'Error', text: 'Monto insuficiente' });
            return;
        }
        cambio = totalEnCordoba - total;
    } else if (tipoPago === '4') {
        efectivoCordoba = document.getElementById('efectivo').value.trim();
        if (!efectivoCordoba) {
            Swal.fire({ icon: 'error', title: 'Error', text: 'Ingrese el numero de referencia' });
            return;
        }   
        cambio = 0;
    }

    const datos = {
        productos,
        total,
        cliente,
        tipoPago: tipoPago,
        efectivo_cordoba: efectivoCordoba,
        efectivo_dolar: efectivoDolar,
    };

    console.log("Datos a enviar:", datos);
    fetch('/guardar-factura-unica/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(datos)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Factura Guardada Correctamente',
                    text: `Cambio: C$ ${cambio.toFixed(2)}`
                }).then(() => {
                    window.location.reload();
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error al guardar',
                    text: data.message || 'Error al guardar la factura.'
                });
            }
        });
}