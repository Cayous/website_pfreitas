(() => {
  "use strict";

  /* ------------------------------- Ano ---------------------------------- */
  const year = document.getElementById("current-year");
  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  /* ------- Uma seção de FAQ aberta por vez, para leitura mais limpa ------ */
  const faqItems = Array.from(document.querySelectorAll(".faq-list details"));
  faqItems.forEach((item) => {
    item.addEventListener("toggle", () => {
      if (!item.open) return;
      faqItems.forEach((other) => {
        if (other !== item) other.open = false;
      });
    });
  });
})();
