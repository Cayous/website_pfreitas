(() => {
  "use strict";

  const dataLayer = window.dataLayer = window.dataLayer || [];
  const header = document.querySelector(".lp-header");
  const year = document.getElementById("current-year");

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  const updateHeader = () => {
    if (header) {
      header.classList.toggle("scrolled", window.scrollY > 24);
    }
  };

  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });

  document.querySelectorAll(".whatsapp-link").forEach((link) => {
    link.addEventListener("click", () => {
      dataLayer.push({
        event: "whatsapp_click",
        cta_location: link.dataset.ctaLocation || "unknown"
      });
    });
  });

  document.querySelectorAll(".faq-list details").forEach((item, index) => {
    item.addEventListener("toggle", () => {
      if (item.open) {
        dataLayer.push({
          event: "faq_open",
          faq_position: index + 1
        });
      }
    });
  });
})();
