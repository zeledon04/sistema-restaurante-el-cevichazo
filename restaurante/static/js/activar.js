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

function activarProveedor(id) {
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
                window.location.href = "/Proveedores/activarProveedor/" + id
            }
        })
}

function activarUnidadMedida(id) {
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
                window.location.href = "/UnidadMedidas/activarUnidadMedida/" + id
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
                window.location.href = "/Usuarios/activarUsuario/" + id
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