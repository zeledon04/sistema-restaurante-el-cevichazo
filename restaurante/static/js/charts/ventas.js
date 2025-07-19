let grafico = null;

document.addEventListener("DOMContentLoaded", () => {
  const modoSelect = document.getElementById("modoSelect");

  // Establecer "semana" como valor inicial por defecto si no hay otro seleccionado
  if (!modoSelect.value) {
    modoSelect.value = "semana";
  }

  modoSelect.addEventListener("change", actualizarGrafico);
  actualizarGrafico(); // Cargar al entrar
});

// En esta función solo llama a cargarDatos pero si es modo = "rango", antes se muestra un swal para que ingrese el rango de fechas.
function actualizarGrafico() {
  const modo = document.getElementById("modoSelect").value;
  const tipo = document.getElementById('tipo');
  if (modo == "semana") tipo.innerText = "Ventas de la Semana Actual";
  if (modo == "mes") tipo.innerText = "Ventas de los Últimos 6 Meses";

  if (modo === "rango") {
    Swal.fire({
      title: "Selecciona el rango de fechas",
      html: `
        <input type="date" id="inicioFecha" class="swal2-input" placeholder="Inicio">
        <input type="date" id="finFecha" class="swal2-input" placeholder="Fin">
      `,
      focusConfirm: false,
      showCancelButton: true,
      preConfirm: () => {
        const inicio = document.getElementById("inicioFecha").value;
        const fin = document.getElementById("finFecha").value;
        if (!inicio || !fin) {
          Swal.showValidationMessage("Selecciona ambas fechas");
          return false;
        }
        tipo.innerText = `Ventas del ${inicio} al ${fin}`;
        return { inicio, fin };
      }
    }).then(result => {
      if (result.isConfirmed) {
        cargarDatos("rango", result.value.inicio, result.value.fin);
      }
    });
  } else {
    cargarDatos(modo);
  }
}

// acá se reciben los datos del front del select(si es semana, mes o rango y con sus fechas) y se envían al backend
function cargarDatos(modo, inicio = null, fin = null) {
  const body = { modo };
  if (modo === "rango") {
    body.inicio = inicio;
    body.fin = fin;
  }

  // console.log(body);
  fetch("/api/datos-grafico/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify(body)
  })
    .then(res => res.json())
    .then(data => {
      // console.log(data);
      if (grafico) grafico.destroy();
      
      const ctx = document.getElementById("miGrafico").getContext("2d");
      // Crear el degradado vertical (de arriba a abajo)
      const gradient = ctx.createLinearGradient(0, 0, 0, 400);
      gradient.addColorStop(0, "rgba(75, 192, 192, 1)");   // color en la parte superior
      gradient.addColorStop(1, "rgba(75, 192, 192, 0.2)"); // color en la parte inferior

      grafico = new Chart(ctx, {
        type: "bar",
        data: {
          labels: data.labels,
          datasets: [{
            label: "Ventas",
            data: data.datos,
            backgroundColor: gradient
          }]
        },
        options: {
          responsive: true,
          scales: { y: { beginAtZero: true } }
        }
      });

    });
}

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
