// i18n.js
(function () {
  function applyTranslations() {
    let lang = document.documentElement.lang ? document.documentElement.lang.toUpperCase() : null;
    if (!lang) {
      lang = localStorage.getItem('docinsp_lang') || 'EN';
    }
    localStorage.setItem('docinsp_lang', lang);
    const dict = (window.I18N && window.I18N[lang]) ? window.I18N[lang] : (window.I18N ? window.I18N.EN : {});

    if (!dict) return;

    // Plain text
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key]) el.textContent = dict[key];
    });

    // HTML content (for spans, bold text, etc.)
    document.querySelectorAll('[data-i18n-html]').forEach(el => {
      const key = el.getAttribute('data-i18n-html');
      if (dict[key]) el.innerHTML = dict[key];
    });

    // Placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      if (dict[key]) el.setAttribute('placeholder', dict[key]);
    });

    // Update active state in dropdown UI if it exists
    document.querySelectorAll('.lang-pill').forEach(pill => {
      pill.textContent = lang;
    });

    document.querySelectorAll('.lang-item').forEach(item => {
      item.classList.toggle('active', item.getAttribute('data-lang') === lang);
    });
  }

  window.__i18n = {
    setLang: (lang) => {
      document.documentElement.lang = lang.toLowerCase();
      localStorage.setItem('docinsp_lang', lang.toUpperCase());
      applyTranslations();
      // Dispatch event for other components
      window.dispatchEvent(new CustomEvent('langChanged', { detail: lang.toUpperCase() }));
    },
    getLang: () => {
      return (document.documentElement.lang ? document.documentElement.lang.toUpperCase() : null) || localStorage.getItem('docinsp_lang') || 'EN';
    }
  };

  // Run on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      applyTranslations();
    });
  } else {
    applyTranslations();
  }
})();