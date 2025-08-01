function activarCategoria(id) {
    Swal.fire({
        "title": "¿Estás seguro?",
        "text": "¿Desea Activar?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Activar",
        "reverseButtons": true,
        "confirmButtonColor": "#28a745"
    })
        .then(function (result) {
            if (result.isConfirmed) {
                window.location.href = "/categorias/activarCategoria/" + id
            }
        })
}

function activarPlato(id) {
    Swal.fire({
        "title": "¿Estás seguro?",
        "text": "¿Desea Activar?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Activar",
        "reverseButtons": true,
        "confirmButtonColor": "#28a745"
    })
        .then(function (result) {
            if (result.isConfirmed) {
                window.location.href = "/platos/activarPlato/" + id
            }
        })
}



function activarUsuario(id) {
    Swal.fire({
        "title": "¿Estás seguro?",
        "text": "¿Desea Activar?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Activar",
        "reverseButtons": true,
        "confirmButtonColor": "#28a745"
    })
        .then(function (result) {
            if (result.isConfirmed) {
                window.location.href = "/usuarios/activarUsuario/" + id
            }
        })
}

function activarProducto(id) {
    Swal.fire({
        "title": "¿Estás seguro?",
        "text": "¿Desea Activar?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Activar",
        "reverseButtons": true,
        "confirmButtonColor": "#28a745"
    })
        .then(function (result) {
            if (result.isConfirmed) {
                window.location.href = "/productos/activarProducto/" + id
            }
        })
}