function eliminarProducto(id){
    Swal.fire({
        "title": "¿Estás seguro?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                 window.location.href = "/productos/eliminarProducto/"+id
            }
        })
}

function eliminarPlato(id){
    Swal.fire({
        "title": "¿Estás seguro?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                window.location.href = "/platos/eliminarPlato/"+id
            }
        })
}

function eliminarCategoria(id){
    Swal.fire({
        "title": "¿Estás seguro?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                 window.location.href = "/categorias/eliminarCategoria/"+id
            }
        })
}


function eliminarUsuario(id){
    Swal.fire({
        "title": "¿Estás seguro?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                 window.location.href = "/usuarios/eliminarUsuario/"+id
            }
        })
}

function eliminarLote(id){
    Swal.fire({
        "title": "¿Estás seguro?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                 window.location.href = "/productos/eliminarLote/"+id
            }
        })
}