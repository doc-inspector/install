/* ============================================================
   DocInspector — scroll-fx.js
   WOW effects · IntersectionObserver · 3D tilt · Document rain
   ============================================================ */
(function () {
  'use strict';

  /* ── 1. PROGRESS BAR ───────────────────────────────────── */
  const bar = document.getElementById('progress-bar');
  function updateProgress() {
    if (!bar) return;
    const h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = h > 0 ? ((window.scrollY / h) * 100) + '%' : '0%';
  }

  /* ── 2. HEADER SCROLL STATE ────────────────────────────── */
  const header = document.querySelector('.site-header');
  function updateHeader() {
    if (!header) return;
    header.classList.toggle('scrolled', window.scrollY > 40);
  }

  /* Combined scroll handler */
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => { updateProgress(); updateHeader(); ticking = false; });
      ticking = true;
    }
  }, { passive: true });
  updateProgress();
  updateHeader();

  /* ── 3. INTERSECTION OBSERVER — REVEALS ────────────────── */
  const revealEls = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger');
  if (revealEls.length) {
    const revealObs = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); revealObs.unobserve(e.target); } });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(el => revealObs.observe(el));
  }

  /* ── 4. WORKFLOW PIPELINE ──────────────────────────────── */
  const workflowSteps = document.querySelector('.workflow-steps');
  if (workflowSteps) {
    const wObs = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); wObs.unobserve(e.target); } });
    }, { threshold: 0.25 });
    wObs.observe(workflowSteps);
  }

  /* ── 5. SHIELD SVG DRAW ────────────────────────────────── */
  const shieldWrap = document.querySelector('.shield-wrap');
  if (shieldWrap) {
    const sObs = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); sObs.unobserve(e.target); } });
    }, { threshold: 0.3 });
    sObs.observe(shieldWrap);
  }

  /* ── 6. STATS COUNTER ANIMATION ────────────────────────── */
  function animateCounter(el) {
    const target = parseInt(el.getAttribute('data-target'), 10);
    const suffix = el.getAttribute('data-suffix') || '';
    const prefix = el.getAttribute('data-prefix') || '';
    const duration = 2000;
    const start = performance.now();
    function step(now) {
      const t = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - t, 4); // easeOutQuart
      el.textContent = prefix + Math.round(target * ease).toLocaleString() + suffix;
      if (t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  const statNums = document.querySelectorAll('.stat-number[data-target]');
  if (statNums.length) {
    const cObs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { animateCounter(e.target); cObs.unobserve(e.target); }
      });
    }, { threshold: 0.5 });
    statNums.forEach(el => cObs.observe(el));
  }

  /* ── 7. HERO 3D TILT ON MOUSE MOVE ────────────────────── */
  const heroFrame = document.querySelector('.hero-app-frame');
  const heroSection = document.querySelector('.hero');
  if (heroFrame && heroSection && window.innerWidth > 1024) {
    heroSection.addEventListener('mousemove', (e) => {
      const rect = heroSection.getBoundingClientRect();
      const cx = (e.clientX - rect.left) / rect.width - 0.5;
      const cy = (e.clientY - rect.top) / rect.height - 0.5;
      heroFrame.style.transform = `rotateY(${cx * 12}deg) rotateX(${cy * -8}deg)`;
    });
    heroSection.addEventListener('mouseleave', () => {
      heroFrame.style.transform = 'rotateY(-5deg) rotateX(2deg)';
    });
  }

  /* ── 8. FEATURE CARD — MOUSE FOLLOW GLOW ───────────────── */
  document.querySelectorAll('.feature-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width * 100).toFixed(1) + '%';
      const y = ((e.clientY - rect.top) / rect.height * 100).toFixed(1) + '%';
      card.style.setProperty('--mouse-x', x);
      card.style.setProperty('--mouse-y', y);
    });
  });

  /* ── 9. DOCUMENT RAIN — Desktop-shortcut-style file icons (no text) ── */
  const rainContainer = document.querySelector('.doc-rain');
  if (rainContainer) {
    const count = window.innerWidth < 768 ? 10 : 22;

    /* Unique IDs per icon to avoid SVG filter/gradient clashes */
    let uid = 0;
    function mkId() { return 'r' + (uid++); }

    /* PDF icon — white page, folded corner, red accent stripe at bottom (no text) */
    function svgPDF() {
      const g = mkId(), f = mkId();
      return `<svg viewBox="0 0 32 40" xmlns="http://www.w3.org/2000/svg">
        <defs><linearGradient id="${g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#f1f5f9"/><stop offset="100%" stop-color="#cbd5e1"/></linearGradient></defs>
        <rect x="1" y="1" width="30" height="38" rx="2.5" fill="url(#${g})" stroke="rgba(100,116,139,0.35)" stroke-width="0.7"/>
        <path d="M22 1 L31 10 L22 10 Z" fill="rgba(148,163,184,0.45)"/>
        <path d="M22 1 L22 10 L31 10" fill="none" stroke="rgba(100,116,139,0.3)" stroke-width="0.5"/>
        <line x1="5" y1="15" x2="19" y2="15" stroke="rgba(100,116,139,0.22)" stroke-width="1"/>
        <line x1="5" y1="19" x2="24" y2="19" stroke="rgba(100,116,139,0.18)" stroke-width="1"/>
        <line x1="5" y1="23" x2="21" y2="23" stroke="rgba(100,116,139,0.14)" stroke-width="1"/>
        <line x1="5" y1="27" x2="16" y2="27" stroke="rgba(100,116,139,0.10)" stroke-width="1"/>
        <rect x="1" y="32" width="30" height="7" rx="0 0 2.5 2.5" fill="rgba(220,38,38,0.75)"/>
      </svg>`;
    }

    /* DOCX icon — white page, folded corner, blue accent stripe (no text) */
    function svgDOC() {
      const g = mkId();
      return `<svg viewBox="0 0 32 40" xmlns="http://www.w3.org/2000/svg">
        <defs><linearGradient id="${g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#f1f5f9"/><stop offset="100%" stop-color="#cbd5e1"/></linearGradient></defs>
        <rect x="1" y="1" width="30" height="38" rx="2.5" fill="url(#${g})" stroke="rgba(100,116,139,0.35)" stroke-width="0.7"/>
        <path d="M22 1 L31 10 L22 10 Z" fill="rgba(148,163,184,0.45)"/>
        <path d="M22 1 L22 10 L31 10" fill="none" stroke="rgba(100,116,139,0.3)" stroke-width="0.5"/>
        <line x1="5" y1="15" x2="24" y2="15" stroke="rgba(100,116,139,0.22)" stroke-width="1"/>
        <line x1="5" y1="19" x2="22" y2="19" stroke="rgba(100,116,139,0.18)" stroke-width="1"/>
        <line x1="5" y1="23" x2="18" y2="23" stroke="rgba(100,116,139,0.14)" stroke-width="1"/>
        <line x1="5" y1="27" x2="24" y2="27" stroke="rgba(100,116,139,0.10)" stroke-width="1"/>
        <rect x="1" y="32" width="30" height="7" rx="0 0 2.5 2.5" fill="rgba(37,99,235,0.8)"/>
      </svg>`;
    }

    /* XLSX icon — white page, folded corner, green accent + mini grid cells (no text) */
    function svgXLS() {
      const g = mkId();
      return `<svg viewBox="0 0 32 40" xmlns="http://www.w3.org/2000/svg">
        <defs><linearGradient id="${g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#f1f5f9"/><stop offset="100%" stop-color="#cbd5e1"/></linearGradient></defs>
        <rect x="1" y="1" width="30" height="38" rx="2.5" fill="url(#${g})" stroke="rgba(100,116,139,0.35)" stroke-width="0.7"/>
        <path d="M22 1 L31 10 L22 10 Z" fill="rgba(148,163,184,0.45)"/>
        <path d="M22 1 L22 10 L31 10" fill="none" stroke="rgba(100,116,139,0.3)" stroke-width="0.5"/>
        <rect x="5" y="14" width="9" height="5" rx="0.5" fill="none" stroke="rgba(34,197,94,0.3)" stroke-width="0.6"/>
        <rect x="14" y="14" width="9" height="5" rx="0.5" fill="none" stroke="rgba(34,197,94,0.25)" stroke-width="0.6"/>
        <rect x="5" y="19" width="9" height="5" rx="0.5" fill="none" stroke="rgba(34,197,94,0.2)" stroke-width="0.6"/>
        <rect x="14" y="19" width="9" height="5" rx="0.5" fill="none" stroke="rgba(34,197,94,0.18)" stroke-width="0.6"/>
        <rect x="5" y="24" width="9" height="5" rx="0.5" fill="none" stroke="rgba(34,197,94,0.15)" stroke-width="0.6"/>
        <rect x="14" y="24" width="9" height="5" rx="0.5" fill="none" stroke="rgba(34,197,94,0.12)" stroke-width="0.6"/>
        <rect x="1" y="32" width="30" height="7" rx="0 0 2.5 2.5" fill="rgba(22,163,74,0.8)"/>
      </svg>`;
    }

    const docTypes = [svgPDF, svgPDF, svgPDF, svgDOC, svgDOC, svgXLS, svgXLS];

    for (let i = 0; i < count; i++) {
      const drop = document.createElement('div');
      drop.className = 'raindrop';
      drop.innerHTML = docTypes[i % docTypes.length]();
      drop.style.left = Math.random() * 100 + '%';
      drop.style.animationDuration = (14 + Math.random() * 18) + 's';
      drop.style.animationDelay = (Math.random() * 20) + 's';
      drop.style.opacity = (0.04 + Math.random() * 0.08).toFixed(3);
      drop.style.width = (18 + Math.random() * 12) + 'px';
      rainContainer.appendChild(drop);
    }
  }

  /* ── 10. SHOWCASE TABS ─────────────────────────────────── */
  const tabs = document.querySelectorAll('.showcase-tab');
  const panels = document.querySelectorAll('.showcase-panel');
  const dots = document.querySelectorAll('.slide-dot');
  function switchShowcase(idx) {
    tabs.forEach((t, i) => t.classList.toggle('active', i === idx));
    panels.forEach((p, i) => p.classList.toggle('active', i === idx));
    dots.forEach((d, i) => d.classList.toggle('active', i === idx));
  }
  tabs.forEach((t, i) => t.addEventListener('click', () => switchShowcase(i)));
  dots.forEach((d, i) => d.addEventListener('click', () => switchShowcase(i)));

  /* ── 11. HORIZONTAL SCROLL DRAG ────────────────────────── */
  document.querySelectorAll('.hscroll-track').forEach(track => {
    let isDown = false, startX, scrollL;
    track.addEventListener('mousedown', (e) => { isDown = true; startX = e.pageX - track.offsetLeft; scrollL = track.scrollLeft; track.style.cursor = 'grabbing'; });
    track.addEventListener('mouseleave', () => { isDown = false; track.style.cursor = 'grab'; });
    track.addEventListener('mouseup', () => { isDown = false; track.style.cursor = 'grab'; });
    track.addEventListener('mousemove', (e) => { if (!isDown) return; e.preventDefault(); track.scrollLeft = scrollL - (e.pageX - track.offsetLeft - startX) * 1.5; });
  });

  /* ── 12. MOBILE NAV TOGGLE ─────────────────────────────── */
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navToggle.classList.toggle('open');
      navLinks.classList.toggle('open');
    });
    // Close on link click
    navLinks.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        navToggle.classList.remove('open');
        navLinks.classList.remove('open');
      });
    });
  }

  /* ── 13. LANGUAGE DROPDOWN ─────────────────────────────── */
  document.querySelectorAll('.lang-dropdown').forEach(dd => {
    const btn = dd.querySelector('.lang-btn');
    const menu = dd.querySelector('.lang-menu');
    if (!btn || !menu) return;
    btn.addEventListener('click', (e) => { e.stopPropagation(); menu.classList.toggle('open'); });
    menu.querySelectorAll('.lang-item').forEach(item => {
      item.addEventListener('click', () => {
        const lang = item.getAttribute('data-lang');
        if (window.__i18n) window.__i18n.setLang(lang);
        menu.classList.remove('open');
      });
    });
    document.addEventListener('click', () => menu.classList.remove('open'));
  });

  /* ── 14. PARALLAX FLOAT on SCROLL ──────────────────────── */
  const parallaxEls = document.querySelectorAll('[data-parallax]');
  if (parallaxEls.length && window.innerWidth > 768) {
    window.addEventListener('scroll', () => {
      const sy = window.scrollY;
      parallaxEls.forEach(el => {
        const speed = parseFloat(el.getAttribute('data-parallax')) || 0.1;
        const rect = el.getBoundingClientRect();
        const center = rect.top + rect.height / 2;
        const offset = (center - window.innerHeight / 2) * speed;
        el.style.transform = `translateY(${offset}px)`;
      });
    }, { passive: true });
  }

  /* ── 15. COOKIE BANNER (simple) ────────────────────────── */
  const cookieBar = document.getElementById('cookie-bar');
  const cookieBtn = document.getElementById('cookie-accept');
  if (cookieBar && cookieBtn) {
    if (!localStorage.getItem('docinsp_cookies')) {
      cookieBar.style.display = 'flex';
    }
    cookieBtn.addEventListener('click', () => {
      localStorage.setItem('docinsp_cookies', '1');
      cookieBar.style.display = 'none';
    });
  }

  /* ── 16. SMOOTH ANCHOR SCROLL ──────────────────────────── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      if (id === '#') return;
      const target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ── 17. NEW 3D REVEAL OBSERVERS ───────────────────────── */
  const reveal3d = document.querySelectorAll('.reveal-flip, .reveal-zoom, .stagger-3d');
  if (reveal3d.length) {
    const obs3d = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('visible'); obs3d.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -30px 0px' });
    reveal3d.forEach(el => obs3d.observe(el));
  }

  /* ── 18. HEX-PARTICLE SPAWNER ──────────────────────────── */
  document.querySelectorAll('.hex-particles').forEach(container => {
    const count = window.innerWidth < 768 ? 8 : 18;
    for (let i = 0; i < count; i++) {
      const hex = document.createElement('div');
      hex.className = 'hex-dot';
      hex.style.cssText = `
        position:absolute;
        width:${6 + Math.random() * 14}px;
        height:${6 + Math.random() * 14}px;
        left:${Math.random() * 100}%;
        top:${Math.random() * 100}%;
        background:rgba(6,182,212,${(0.06 + Math.random() * 0.12).toFixed(2)});
        clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
        animation:hexFloat ${5 + Math.random() * 8}s ease-in-out infinite;
        animation-delay:${(Math.random() * 5).toFixed(1)}s;
        pointer-events:none;
      `;
      container.appendChild(hex);
    }
  });

  /* ── 19. 3D TILT CARDS — MOUSE FOLLOW ──────────────────── */
  if (window.innerWidth > 1024) {
    document.querySelectorAll('.tilt-card').forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const cx = (e.clientX - rect.left) / rect.width - 0.5;
        const cy = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = `perspective(600px) rotateY(${cx * 10}deg) rotateX(${cy * -8}deg) scale(1.02)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(600px) rotateY(0) rotateX(0) scale(1)';
        card.style.transition = 'transform 0.5s ease';
      });
      card.addEventListener('mouseenter', () => {
        card.style.transition = 'transform 0.15s ease';
      });
    });
  }

  /* ── 20. LIGHTBOX FOR SHOWCASE IMAGES ──────────────────── */
  const lbOverlay = document.getElementById('lightbox-overlay');
  if (lbOverlay) {
    const lbImg = lbOverlay.querySelector('.lightbox-img');
    const lbClose = lbOverlay.querySelector('.lightbox-close');
    const lbPrev = lbOverlay.querySelector('.lightbox-prev');
    const lbNext = lbOverlay.querySelector('.lightbox-next');
    let lbImages = [];
    let lbIdx = 0;

    document.querySelectorAll('.showcase-img-wrap img').forEach((img, i) => {
      lbImages.push(img.src);
      img.style.cursor = 'zoom-in';
      img.addEventListener('click', () => openLightbox(i));
    });

    function openLightbox(i) {
      lbIdx = i;
      lbImg.src = lbImages[lbIdx];
      lbOverlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
    function closeLightbox() {
      lbOverlay.classList.remove('active');
      document.body.style.overflow = '';
    }
    function lbNav(dir) {
      lbIdx = (lbIdx + dir + lbImages.length) % lbImages.length;
      lbImg.src = lbImages[lbIdx];
    }

    if (lbClose) lbClose.addEventListener('click', closeLightbox);
    if (lbPrev) lbPrev.addEventListener('click', () => lbNav(-1));
    if (lbNext) lbNext.addEventListener('click', () => lbNav(1));
    lbOverlay.addEventListener('click', (e) => { if (e.target === lbOverlay) closeLightbox(); });

    document.addEventListener('keydown', (e) => {
      if (!lbOverlay.classList.contains('active')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') lbNav(-1);
      if (e.key === 'ArrowRight') lbNav(1);
    });
  }

})();
