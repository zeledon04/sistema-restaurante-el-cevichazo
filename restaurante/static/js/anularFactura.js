    function anularFactura(id){
        Swal.fire({
            "title": "¿Deseas anular esta Factura?",
            "text": "Esta acción no se puede deshacer",
            "icon": "question",
            "showCancelButton": true,
            "cancelButtonText": "No, Cancelar",
            "confirmButtonText": "Si, Eliminar",
            "reverseButtons":true,
            "confirmButtonColor": "#dc3545"
        })
        .then(function(result){
            if (result.isConfirmed){
                window.location.href = "/Facturas/anularFactura/"+id
            }
        })
    }