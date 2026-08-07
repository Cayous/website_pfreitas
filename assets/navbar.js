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

  const closeMenu = () => {
    toggle.classList.remove("open");
    menu.classList.remove("open");
    toggle.setAttribute("aria-label", "Abrir menu");
    toggle.setAttribute("aria-expanded", "false");
  };

  toggle.addEventListener("click", () => {
    const willOpen = !menu.classList.contains("open");
    toggle.classList.toggle("open", willOpen);
    menu.classList.toggle("open", willOpen);
    toggle.setAttribute("aria-label", willOpen ? "Fechar menu" : "Abrir menu");
    toggle.setAttribute("aria-expanded", String(willOpen));
  });

  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menu.classList.contains("open")) {
      closeMenu();
      toggle.focus();
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 1100) {
      closeMenu();
    }
  });
})();
