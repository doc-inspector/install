// i18n.js
(() => {
  const LANG_KEY = "siteLang";
  const allowed = new Set(["EN", "RO", "RU"]);

  function normalizeLang(x) {
    const v = (x || "").toUpperCase();
    return allowed.has(v) ? v : "EN";
  }

  function getLang() {
    return normalizeLang(localStorage.getItem(LANG_KEY) || "EN");
  }

  function setLang(lang) {
    const v = normalizeLang(lang);
    localStorage.setItem(LANG_KEY, v);
    applyLang(v);
    updateLangUI(v);
  }

  function t(lang, key) {
    const dict = (window.I18N && window.I18N[lang]) || {};
    return dict[key];
  }

  function applyLang(lang) {
    document.documentElement.setAttribute("lang", lang === "RO" ? "ro" : (lang === "RU" ? "ru" : "en"));

    // textContent
    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.getAttribute("data-i18n");
      const val = t(lang, key);
      if (typeof val === "string") el.textContent = val;
    });

    // placeholders
    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
      const key = el.getAttribute("data-i18n-placeholder");
      const val = t(lang, key);
      if (typeof val === "string") el.setAttribute("placeholder", val);
    });
  }

  function updateLangUI(lang) {
    document.querySelectorAll(".lang-pill").forEach(p => p.textContent = lang);
    document.querySelectorAll(".lang-menu .lang-item").forEach(btn => {
      const v = normalizeLang(btn.getAttribute("data-lang") || btn.textContent);
      btn.classList.toggle("active", v === lang);
    });
  }

  // Expose for existing dropdown JS to call
  window.__i18n = { getLang, setLang, applyLang };

  document.addEventListener("DOMContentLoaded", () => {
    const lang = getLang();
    applyLang(lang);
    updateLangUI(lang);
  });
})();
