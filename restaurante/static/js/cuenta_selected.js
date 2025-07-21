// Referencia al contenedor de todas las cuentas
const cuentasContainer = document.querySelector('.cuentas-container');

// Variable para almacenar la cuenta seleccionada actualmente
let cuentaSeleccionada = null;

cuentasContainer.addEventListener('click', function (e) {
  // Busca el div con clase 'cuenta' más cercano al lugar donde se hizo clic
  const divCuenta = e.target.closest('.cuenta');

  if (divCuenta) {
    // Desmarcar la cuenta anterior, si existe
    if (cuentaSeleccionada) {
      cuentaSeleccionada.classList.remove('seleccionada');
    }

    // Marcar esta nueva cuenta como seleccionada
    divCuenta.classList.add('seleccionada');
    cuentaSeleccionada = divCuenta;

    // Puedes guardar el ID o cualquier otra info
    const idCuenta = divCuenta.dataset.id;
    console.log('Cuenta seleccionada:', idCuenta);
  }
});
