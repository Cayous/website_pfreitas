(() => {
  "use strict";

  /* ------------------------------------------------------------------
     Rótulo de conversão do Google Ads para ESTA página.
     Deixe null até criar uma conversão própria em Ads → Metas → Conversões
     ("Retaguarda | WhatsApp | Clique"). Reutilizar o rótulo da campanha de
     plano de saúde misturaria os dados das duas campanhas.
     Formato esperado: "AW-18328884280/XXXXXXXXXXXXXXXXXX"
  ------------------------------------------------------------------ */
  const CONVERSION_SEND_TO = null;

  const dataLayer = window.dataLayer = window.dataLayer || [];
  const year = document.getElementById("current-year");
  const consentBanner = document.getElementById("consent-banner");

  /* ---------------------------- Consentimento --------------------------- */
  const updateConsent = (choice) => {
    try {
      window.localStorage.setItem("rt_ads_consent", choice);
    } catch (error) {
      // Sem localStorage o Consent Mode permanece negado — comportamento seguro.
    }

    if (typeof window.gtag === "function") {
      window.gtag("consent", "update", {
        ad_storage: choice === "accepted" ? "granted" : "denied",
        analytics_storage: choice === "accepted" ? "granted" : "denied",
        ad_user_data: choice === "accepted" ? "granted" : "denied",
        ad_personalization: "denied"
      });
    }

    if (consentBanner) {
      consentBanner.hidden = true;
    }
  };

  if (consentBanner) {
    let saved = null;
    try {
      saved = window.localStorage.getItem("rt_ads_consent");
    } catch (error) {
      saved = null;
    }

    consentBanner.hidden = saved === "accepted" || saved === "rejected";
    consentBanner.querySelectorAll("[data-consent]").forEach((button) => {
      button.addEventListener("click", () => updateConsent(button.dataset.consent));
    });
  }

  /* ------------------------------- Ano ---------------------------------- */
  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  /* --------------------- Rastreio dos cliques no WhatsApp --------------- */
  document.querySelectorAll(".whatsapp-link").forEach((link) => {
    link.addEventListener("click", () => {
      dataLayer.push({
        event: "whatsapp_click",
        cta_location: link.dataset.ctaLocation || "unknown",
        page: "retaguarda"
      });

      if (CONVERSION_SEND_TO && typeof window.gtag === "function") {
        window.gtag("event", "conversion", {
          send_to: CONVERSION_SEND_TO,
          value: 1,
          currency: "BRL",
          event_timeout: 2000
        });
      }
    });
  });

  /* ------------------------ Rastreio de abertura de FAQ ------------------ */
  document.querySelectorAll(".faq-list details").forEach((item, index) => {
    item.addEventListener("toggle", () => {
      if (item.open) {
        dataLayer.push({
          event: "faq_open",
          faq_position: index + 1,
          page: "retaguarda"
        });
      }
    });
  });

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
