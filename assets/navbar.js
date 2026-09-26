(() => {
  "use strict";

  const toggle = document.getElementById("navbar-toggle");
  const menu = document.getElementById("navbar-menu");
  const page = window.location.pathname.split("/").pop() || "index.html";

  document.querySelectorAll(".navbar-menu a").forEach((link) => {
    const isCurrentPage = link.getAttribute("href") === page;
    link.classList.toggle("active", isCurrentPage);

    if (isCurrentPage) {
      link.setAttribute("aria-current", "page");
    } else {
      link.removeAttribute("aria-current");
    }
  });

  if (!toggle || !menu) {
    return;
  }

  // O hambúrguer abre uma cópia do menu; no estágio parcial ela mostra só os
  // itens que saíram da barra (ver navbar.css).
  const navbar = menu.closest(".navbar");
  const inner = menu.closest(".navbar-inner");
  const drawer = document.createElement("ul");
  drawer.className = "navbar-drawer";
  drawer.id = "navbar-drawer";
  menu.querySelectorAll(":scope > li").forEach((item) => {
    drawer.appendChild(item.cloneNode(true));
  });
  navbar.appendChild(drawer);
  toggle.setAttribute("aria-controls", drawer.id);

  const closeMenu = () => {
    toggle.classList.remove("open");
    drawer.classList.remove("open");
    toggle.setAttribute("aria-label", "Abrir menu");
    toggle.setAttribute("aria-expanded", "false");
  };

  toggle.addEventListener("click", () => {
    const willOpen = !drawer.classList.contains("open");
    toggle.classList.toggle("open", willOpen);
    drawer.classList.toggle("open", willOpen);
    toggle.setAttribute("aria-label", willOpen ? "Fechar menu" : "Abrir menu");
    toggle.setAttribute("aria-expanded", String(willOpen));
  });

  drawer.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && drawer.classList.contains("open")) {
      closeMenu();
      toggle.focus();
    }
  });

  // Escolhe o primeiro estágio em que o cabeçalho cabe na largura disponível.
  const fitMenu = () => {
    const fits = () => inner.scrollWidth <= inner.clientWidth;
    navbar.classList.remove("is-partial", "is-compact");
    if (!fits()) {
      navbar.classList.add("is-partial");
      if (!fits()) {
        navbar.classList.replace("is-partial", "is-compact");
      }
    }

    if (getComputedStyle(toggle).display === "none") {
      closeMenu();
    }
  };

  fitMenu();
  window.addEventListener("resize", fitMenu);
  if (document.fonts) {
    document.fonts.ready.then(fitMenu);
  }
})();
