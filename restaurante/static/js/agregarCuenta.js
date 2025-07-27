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
          window.location.reload(); // Recargar la página para reflejar los cambios
        } else {
          alert("Error al crear la cuenta");
        }
      })
      .catch(err => {
        console.error("Error al hacer la petición:", err);
        alert("Error en la comunicación con el servidor");
      });
  });


  document.addEventListener('click', async function (e) {
      const btn = e.target.closest(".mandar-cocina");
      if (!btn) return;

      const mesaId = btn.getAttribute("data-mesa");
      const platoId = btn.getAttribute("data-plato");
      const front = btn.getAttribute("data-front");

      const confirmacion = await Swal.fire({
          title: "¿Enviar a cocina?",
          text: "¿Estás seguro que quieres enviar este plato a cocina?",
          icon: "question",
          showCancelButton: true,
          confirmButtonText: "Sí, enviar",
          cancelButtonText: "Cancelar",
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33"
      });

      if (confirmacion.isConfirmed) {
          const body = { mesaId, platoId, front};
          console.log("Enviando a cocina:", body);

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
                  Swal.fire({
                      title: "Enviado",
                      text: "El pedido fue enviado a cocina.",
                      icon: "success",
                      timer: 2000,
                      showConfirmButton: false
                  });
              } else {
                  Swal.fire("Error", data.message || "No se pudo enviar a cocina.", "error");
              }
          })
          .catch(err => {
              console.error("Error:", err);
              Swal.fire("Error", "Error de red al enviar a cocina.", "error");
          });
      }
  });


  // Esto para la seguridad, el crf normal de los formularios.
  function getCookie(name) {
    const cookieString = document.cookie;
    const cookies = cookieString.split("; ");
    for (let c of cookies) {
      const [k, v] = c.split("=");
      if (k === name) return v;
    }
    return "";
  }
  
  document.querySelectorAll(".imprimir").forEach(boton => {
        boton.addEventListener("click", () => {
            const filas = boton.closest(".cuenta").querySelectorAll("tbody.cuerpo-factura tr");
            const datosFactura = [];
            const total = boton.closest(".cuenta").querySelector(".total-final")?.textContent.replace("C$", "").trim();

            filas.forEach(fila => {
                const nombre = fila.querySelector("td:nth-child(2)")?.textContent.trim();
                const cantidad = fila.querySelector("input.cantidad")?.value;
                const precio = fila.querySelector("input.precio")?.value;
                const subtotal = fila.querySelector(".subtotal")?.textContent.replace("C$", "").trim();

                if (nombre && cantidad && precio) {
                    datosFactura.push({
                        nombre,
                        cantidad: parseInt(cantidad),
                        precio: parseFloat(precio),
                        subtotal: parseFloat(subtotal),
                    });
                }
            });

            if (datosFactura.length === 0) {
                Swal.fire("Error", "Agregue productos a la factura", "error");
                return;
            }

            console.log("Datos para imprimir:", datosFactura);

            // Envío al backend (ajusta la URL)
            fetch("/imprimir-precuenta/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")  // Asegúrate de tener esta función
                },
                body: JSON.stringify({ platos: datosFactura, total: total }),
                credentials: "same-origin"
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === "success") {
                    Swal.fire("Éxito", "Pre-cuenta generada correctamente", "success");
                } else {
                    Swal.fire("Error", "No se pudo generar la cuenta", "error");
                }
            })
            .catch(err => {
                console.error("Error al enviar datos:", err);
                Swal.fire("Error", "Error en la solicitud", "error");
            });
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


// Función CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Coincide el nombre
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


