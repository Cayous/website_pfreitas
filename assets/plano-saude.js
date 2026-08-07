(() => {
  "use strict";

  const dataLayer = window.dataLayer = window.dataLayer || [];
  const year = document.getElementById("current-year");
  const consentBanner = document.getElementById("consent-banner");

  const updateConsent = (choice) => {
    try {
      window.localStorage.setItem("pf_ads_consent", choice);
    } catch (error) {
      // O Consent Mode continua negado caso o armazenamento local esteja indisponível.
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
    let savedConsent = null;
    try {
      savedConsent = window.localStorage.getItem("pf_ads_consent");
    } catch (error) {
      savedConsent = null;
    }

    consentBanner.hidden = savedConsent === "accepted" || savedConsent === "rejected";
    consentBanner.querySelectorAll("[data-consent]").forEach((button) => {
      button.addEventListener("click", () => updateConsent(button.dataset.consent));
    });
  }

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  document.querySelectorAll(".whatsapp-link").forEach((link) => {
    link.addEventListener("click", () => {
      dataLayer.push({
        event: "whatsapp_click",
        cta_location: link.dataset.ctaLocation || "unknown"
      });

      if (typeof window.gtag === "function") {
        window.gtag("event", "conversion", {
          send_to: "AW-18328884280/stTUCP6_mdIcELio8qNE",
          value: 1,
          currency: "BRL",
          event_timeout: 2000
        });
      }
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
