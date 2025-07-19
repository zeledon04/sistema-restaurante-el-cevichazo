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

function eliminarCategoriaRopa(id){
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
                 window.location.href = "/CategoriasRopa/eliminarCategoriaRopa/"+id
            }
        })
}

function eliminarPresentacion(id){
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
                 window.location.href = "/Presentaciones/eliminarPresentacion/"+id
            }
        })
}

function eliminarProveedor(id){
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
                 window.location.href = "/Proveedores/eliminarProveedor/"+id
            }
        })
}

function eliminarUnidadMedida(id){
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
                 window.location.href = "/UnidadMedidas/eliminarUnidadMedida/"+id
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
                 window.location.href = "/Usuarios/eliminarUsuario/"+id
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