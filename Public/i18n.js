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
    document.querySelectorAll('.lang-pill').forEach(pill => {
      pill.textContent = lang;
    });

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
    document.addEventListener('DOMContentLoaded', () => {
      applyTranslations();
      initCookieBanner();
    });
  } else {
    applyTranslations();
    initCookieBanner();
  }

  function initCookieBanner() {
    if (localStorage.getItem('docinsp_cookies_accepted')) return;

    const style = document.createElement('style');
    style.innerHTML = `
      .cookie-banner {
        position: fixed; bottom: 2rem; left: 50%;
        transform: translateX(-50%) translateY(100px);
        width: 90%; max-width: 600px;
        background: rgba(13, 25, 41, 0.85); backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 210, 255, 0.2); border-radius: 16px;
        padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem;
        z-index: 9999; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
        transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1); opacity: 0;
      }
      .cookie-banner.show { transform: translateX(-50%) translateY(0); opacity: 1; }
      .cookie-text { font-size: 0.95rem; line-height: 1.5; color: rgba(255,255,255,0.9); }
      .cookie-btns { display: flex; gap: 1rem; align-items: center; }
      .cookie-accept {
        background: #00d2ff; color: #0d1929; border: none;
        padding: 0.6rem 1.5rem; border-radius: 50px; font-weight: bold;
        cursor: pointer; transition: all 0.2s ease;
      }
      .cookie-accept:hover { transform: scale(1.05); box-shadow: 0 0 15px rgba(0, 210, 255, 0.4); }
      .cookie-privacy { color: #00d2ff; text-decoration: none; font-size: 0.9rem; opacity: 0.8; }
      .cookie-privacy:hover { opacity: 1; text-decoration: underline; }
      @media (max-width: 480px) {
        .cookie-banner { padding: 1.2rem; bottom: 1rem; }
        .cookie-btns { flex-direction: column; align-items: stretch; }
        .cookie-accept { width: 100%; text-align: center; }
      }
    `;
    document.head.appendChild(style);

    const banner = document.createElement('div');
    banner.className = 'cookie-banner';
    banner.id = 'cookieBanner';

    function updateBannerContent() {
      const lang = localStorage.getItem('docinsp_lang') || 'EN';
      const dict = (window.I18N && window.I18N[lang]) ? window.I18N[lang] : (window.I18N ? window.I18N.EN : {});
      
      const msg = dict["cookies.message"] || "We use cookies to ensure you get the best experience on our website.";
      const acc = dict["cookies.accept"] || "Accept";
      const priv = dict["cookies.privacy"] || "Privacy Policy";

      banner.innerHTML = `
        <div class="cookie-text">${msg}</div>
        <div class="cookie-btns">
          <button class="cookie-accept" id="acceptCookies">${acc}</button>
          <a href="privacy.html" class="cookie-privacy">${priv}</a>
        </div>
      `;
      const acceptBtn = banner.querySelector('#acceptCookies');
      if (acceptBtn) {
        acceptBtn.onclick = () => {
          localStorage.setItem('docinsp_cookies_accepted', 'true');
          banner.classList.remove('show');
          setTimeout(() => banner.remove(), 600);
        };
      }
    }
    updateBannerContent();
    document.body.appendChild(banner);
    setTimeout(() => banner.classList.add('show'), 1000);
    window.addEventListener('langChanged', updateBannerContent);
  }
})();