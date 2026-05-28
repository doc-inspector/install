// cookies.js - Simple cookie banner logic without translation dependency
(function() {
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

    const lang = document.documentElement.lang || 'en';
    const texts = {
        en: { 
            msg: 'We use cookies to improve your experience and analyze site traffic.', 
            btn: 'Accept All', 
            privacy: 'Privacy Policy' 
        },
        ro: { 
            msg: 'Folosim cookie-uri pentru a vă îmbunătăți experiența și pentru a analiza traficul site-ului.', 
            btn: 'Acceptă tot', 
            privacy: 'Politica de confidențialitate' 
        },
        ru: { 
            msg: 'Мы используем файлы cookie для улучшения вашего опыта и анализа трафика сайта.', 
            btn: 'Принять все', 
            privacy: 'Политика конфиденциальности' 
        }
    };

    const t = texts[lang] || texts.en;

    banner.innerHTML = `
      <div class="cookie-text">${t.msg}</div>
      <div class="cookie-btns">
        <button class="cookie-accept" id="acceptCookies">${t.btn}</button>
        <a href="${lang === 'en' ? '' : lang + '/'}privacy.html" class="cookie-privacy">${t.privacy}</a>
      </div>
    `;

    document.body.appendChild(banner);

    setTimeout(() => banner.classList.add('show'), 1000);

    document.getElementById('acceptCookies').onclick = () => {
        localStorage.setItem('docinsp_cookies_accepted', 'true');
        banner.classList.remove('show');
        setTimeout(() => banner.remove(), 600);
    };
})();
