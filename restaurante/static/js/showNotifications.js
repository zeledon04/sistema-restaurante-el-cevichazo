const btnCampana = document.getElementById('btnCampana');
const overlay = document.getElementById('overlay');

// Abrir/cerrar ventana con el botón campana
btnCampana.addEventListener('click', () => {
  if (overlay.classList.contains('hidden')) {
    overlay.classList.remove('hidden');
  } else {
    overlay.classList.add('hidden');
  }
});

// Cerrar al hacer clic fuera del contenido (overlay)
overlay.addEventListener('click', () => {
  overlay.classList.add('hidden');
});