document.getElementById("btnEnviarCocina").addEventListener("click", () => {
    const btn = document.getElementById("btnEnviarCocina");
    const mesaId = btn.getAttribute("data-mesa");
    const platoId = btn.getAttribute("data-plato");
    const detalleId = btn.getAttribute("data-detalle");
    const body = {
        mesaId,
        platoId,
        detalleId
    };
    console.log("Enviando a cocina:", body);
    fetch("/enviar-a-cocina/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken":getCookie("csrftoken") 
        },
        body: JSON.stringify(body),
        credentials: "same-origin" // Asegura que la cookie CSRF se envíe
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === "ok"){
            alert("Pedido enviado a cocina");
        } else {
            alert("Error al enviar");
        }
    })
    .catch(err => console.error("Error:", err));
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