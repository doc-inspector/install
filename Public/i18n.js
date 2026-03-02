// i18n.js
(function () {
  function applyTranslations() {
    const lang = localStorage.getItem('docinsp_lang') || 'EN';
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
    const pill = document.querySelector('.lang-pill');
    if (pill) pill.textContent = lang;

    document.querySelectorAll('.lang-item').forEach(item => {
      item.classList.toggle('active', item.getAttribute('data-lang') === lang);
    });
  }

  window.__i18n = {
    setLang: (lang) => {
      localStorage.setItem('docinsp_lang', lang);
      applyTranslations();
      // Dispatch event for other components
      window.dispatchEvent(new CustomEvent('langChanged', { detail: lang }));
    },
    getLang: () => localStorage.getItem('docinsp_lang') || 'EN'
  };

  // Run on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyTranslations);
  } else {
    applyTranslations();
  }
})();