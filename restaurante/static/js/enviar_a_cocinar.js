document.addEventListener("DOMContentLoaded", () => {
    const tbody = document.getElementById("cuerpo-factura");

    if (tbody) {
        tbody.addEventListener("click", async (event) => {
            const target = event.target.closest(".btnEnviarCocina");
            if (target) {
                const nombreCliente = document.getElementById("nombre-cliente").value.trim();

                if (!nombreCliente) {
                    await Swal.fire({
                        title: "Nombre requerido",
                        text: "Por favor ingresa el nombre del cliente antes de enviar a cocina.",
                        icon: "warning",
                        confirmButtonText: "Entendido"
                    });
                    return;
                }

                const platoId = target.getAttribute("data-id");

                const confirmacion = await Swal.fire({
                    title: "¿Enviar a cocina?",
                    text: `¿Enviar el plato de cliente "${nombreCliente}"?`,
                    icon: "question",
                    showCancelButton: true,
                    confirmButtonText: "Sí, enviar",
                    cancelButtonText: "Cancelar",
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33"
                });

                if (confirmacion.isConfirmed) {
                    const body = { nombreCliente, platoId };

                    fetch("/enviar-a-cocina/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": getCookie("csrftoken")
                        },
                        body: JSON.stringify(body),
                        credentials: "same-origin"
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.status === "success") {
                            Swal.fire("¡Enviado!", "El pedido fue enviado a cocina.", "success");
                        } else {
                            Swal.fire("Error", data.message || "No se pudo enviar el pedido.", "error");
                        }
                    })
                    .catch(err => {
                        console.error("Error:", err);
                        Swal.fire("Error", "Ocurrió un error al enviar el pedido.", "error");
                    });
                }
            }
        });
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
