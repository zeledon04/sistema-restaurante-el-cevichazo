document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".boton");
  const subMenus = document.querySelectorAll(".subMenu");
  const arrows = document.querySelectorAll(".arrow");
  const links = document.querySelectorAll(".subMenu a");
  const directLinks = document.querySelectorAll("a.boton[href]"); // enlaces directos como "Analíticas"

  // Restaurar enlace activo desde localStorage
  const activeHref = localStorage.getItem("activeLinkHref");
  if (activeHref) {
    links.forEach(link => {
      if (link.getAttribute("href") === activeHref) {
        link.classList.add("font-bold", "before:bg-red-500");
        const subMenu = link.closest(".subMenu");
        if (subMenu) {
          subMenu.classList.remove("hidden");
          subMenu.classList.add("open-submenu");
          const arrow = subMenu.previousElementSibling.querySelector(".arrow");
          if (arrow) arrow.classList.add("rotate");
        }
      }
    });

    // Resaltar el enlace directo si fue el último clic
    directLinks.forEach(link => {
      if (link.getAttribute("href") === activeHref) {
        link.classList.add("active-link");
      }
    });
  }

  buttons.forEach(button => {
    button.addEventListener("click", function (e) {
      const isDirectLink = this.tagName.toLowerCase() === "a";
      const subMenu = this.nextElementSibling;
      const arrow = this.querySelector(".arrow");

      if (isDirectLink) {
        // Es un enlace directo como "Analíticas"
        localStorage.setItem("activeLinkHref", this.getAttribute("href"));

        // Remover clases activas previas
        directLinks.forEach(link => link.classList.remove("active-link"));
        this.classList.add("active-link");

        // Cerrar todos los submenús
        subMenus.forEach(sm => sm.classList.add("hidden"));
        arrows.forEach(a => a.classList.remove("rotate"));
      } else if (subMenu && subMenu.classList.contains("subMenu")) {
        // Ver si este submenú está abierto
        const isCurrentlyOpen = !subMenu.classList.contains("hidden");

        // Cerrar todos primero
        subMenus.forEach(sm => sm.classList.add("hidden"));
        arrows.forEach(a => a.classList.remove("rotate"));

        // Si NO estaba abierto, abrirlo
        if (!isCurrentlyOpen) {
          subMenu.classList.remove("hidden");
          if (arrow) arrow.classList.add("rotate");
        }

        e.preventDefault(); // Prevenir comportamiento por defecto del botón
      }
    });

  });

  links.forEach(link => {
    link.addEventListener("click", function () {
      // Guardar en localStorage
      localStorage.setItem("activeLinkHref", this.getAttribute("href"));
    });
  });
});


//! =======================================================================

// Para abrir y cerrar el menú desplegable.
const btnHidden = document.querySelector(".hidden-menu");
const sidebar = document.querySelector(".sidebar"); 

btnHidden.addEventListener("click", () => {
  console.log("¡Botón clickeado!");

  const close = document.querySelector(".close");

  if (!close){
    btnHidden.classList.toggle("close");
    sidebar.classList.add("-left-full");
    const left0 = document.querySelector(".left-0");
    left0?.classList.remove("left-0");

    // bars icon
    btnHidden.innerHTML = `
      <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
      </svg>
    `;
  }
  else if (close){ 
    btnHidden.classList.remove("close");
    const leftFull = document.querySelector(".-left-full");
    leftFull?.classList.remove("-left-full");
    sidebar.classList.add("left-0");

    // close icon
    btnHidden.innerHTML = `
      <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
      </svg>
    `;
  }
});