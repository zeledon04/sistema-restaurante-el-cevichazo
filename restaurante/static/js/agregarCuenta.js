// Referencia al contenedor de todas las cuentas
document.addEventListener("DOMContentLoaded", () => {
  const btnAgregarCuenta = document.getElementById("btn-agregar-mesa");
  const cuentasContainer = document.querySelector(".cuentas-container");

  btnAgregarCuenta.addEventListener("click", async () => {
    const mesaId = cuentasContainer.getAttribute("data-mesa");

    if (!mesaId) {
      alert("No se encontró el ID de la mesa.");
      return;
    }

    const { value: nombreCliente } = await Swal.fire({
      title: "Nombre del cliente",
      input: "text",
      inputPlaceholder: "Ingrese el nombre (opcional)",
      showCancelButton: true,
      confirmButtonText: "Crear cuenta"
    });

    // Si el usuario canceló
    if (nombreCliente === undefined) {
      return;
    }

    fetch("/cuentas/crearCuenta/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken")
      },
      body: JSON.stringify({
        mesaid: mesaId,
        clientenombre: nombreCliente.trim()
      })
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          const cuentaOriginal = cuentasContainer.querySelector(".cuenta");
          const nuevaCuenta = cuentaOriginal.cloneNode(true);
          nuevaCuenta.classList.remove("seleccionada", "bg-[#e0f7fa]");

          // Asignar nuevo ID y limpiar campos
          nuevaCuenta.setAttribute("data-id", data.cuenta_id);

          const inputNombre = nuevaCuenta.querySelector('input[name="nombre_cliente"]');
          if (inputNombre) inputNombre.value = nombreCliente.trim();

          const efectivo = nuevaCuenta.querySelector('input[name="efectivo"]');
          if (efectivo) efectivo.value = "";

          const extra = nuevaCuenta.querySelector(".extra-efectivo");
          if (extra) extra.innerHTML = "";

          const tipo = nuevaCuenta.querySelector('select[name="tipo"]');
          if (tipo) tipo.value = "1";

          const totalFinal = nuevaCuenta.querySelector(".total-final");
          if (totalFinal) totalFinal.textContent = "C$0.00";

          // Eliminar IDs duplicados si los hay
          nuevaCuenta.querySelectorAll("[id]").forEach(el => el.removeAttribute("id"));

          cuentasContainer.appendChild(nuevaCuenta);
        } else {
          alert("Error al crear la cuenta");
        }
      })
      .catch(err => {
        console.error("Error al hacer la petición:", err);
        alert("Error en la comunicación con el servidor");
      });
  });

});

// Función para obtener el token CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

