function cerrarLote(id){
            Swal.fire({
                "title": "¿Ya no quedan productos para este lote?",
                "icon": "question",
                "showCancelButton": true,
                "cancelButtonText": "No, Cancelar",
                "confirmButtonText": "Si, Cerrar Lote",
                "reverseButtons":true,
                "confirmButtonColor": "#dc3545"
            })
            .then(function(result){
                if (result.isConfirmed){
                    window.location.href = "/productos/cerrarLote/"+id
                }
            })
        }