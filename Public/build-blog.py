#!/usr/bin/env python3
"""Build blog system for doc-inspector.com from articles.json"""
import json, os, re, html as htmlmod

DIR = os.path.dirname(os.path.abspath(__file__))

articles_path = os.path.join(DIR, "articles.json")
if not os.path.exists(articles_path):
    articles_path = os.path.join(os.path.dirname(DIR), "articles.json")

with open(articles_path, encoding='utf-8') as f:
    ARTICLES = json.load(f)

DICT_PATH = os.path.join(DIR, "i18n-dict.json")
if os.path.exists(DICT_PATH):
    with open(DICT_PATH, 'r', encoding='utf-8') as f:
        I18N_DICT = json.load(f)
else:
    I18N_DICT = None

SLUG_MAP = {
    "index.html": {"en": "index.html", "ro": "index.html", "ru": "index.html"},
    "price.html": {"en": "price.html", "ro": "preturi.html", "ru": "tseny.html"},
    "user-guide.html": {"en": "user-guide.html", "ro": "ghid-utilizare.html", "ru": "rukovodstvo.html"},
    "reports.html": {"en": "reports.html", "ro": "rapoarte-feedback.html", "ru": "otchety.html"},
    "contact.html": {"en": "contact.html", "ro": "contact.html", "ru": "kontakty.html"},
    "download.html": {"en": "download.html", "ro": "descarca.html", "ru": "skachat.html"},
    "privacy.html": {"en": "privacy.html", "ro": "politica-de-confidentialitate.html", "ru": "politika-konfidentsialnosti.html"},
    "terms.html": {"en": "terms.html", "ro": "termeni-si-conditii.html", "ru": "usloviya-ispolzovaniya.html"},
    "refund.html": {"en": "refund.html", "ro": "politica-de-rambursare.html", "ru": "politika-vozvrata.html"},
    "user-guide-audit.html": {"en": "user-guide-audit.html", "ro": "ghid-audit.html", "ru": "rukovodstvo-audit.html"},
    "user-guide-pdf-repair.html": {"en": "user-guide-pdf-repair.html", "ro": "ghid-reparare-pdf.html", "ru": "rukovodstvo-remont-pdf.html"},
    "user-guide-reporting.html": {"en": "user-guide-reporting.html", "ro": "ghid-raportare.html", "ru": "rukovodstvo-otchety.html"},
    "history.html": {"en": "history.html", "ro": "istoric-versiuni.html", "ru": "istoriya-versiy.html"},
    "thanks.html": {"en": "thanks.html", "ro": "multumim.html", "ru": "spasibo.html"},
    "blog.html": {"en": "blog.html", "ro": "blog.html", "ru": "blog.html"}
}

CATEGORIES = {
    "how-to": {"en": "How-To", "ro": "Cum se face", "ru": "Инструкция"},
    "security": {"en": "Security", "ro": "Securitate", "ru": "Безопасность"},
    "education": {"en": "Education", "ro": "Educație", "ru": "Обучение"},
    "industry": {"en": "Industry", "ro": "Industrie", "ru": "Отрасль"},
}

# Template updated with new ../ paths for assets as everything is in a lang subfolder
ARTICLE_TEMPLATE = '''<!DOCTYPE html>
<html lang="%(lang)s">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%(title_escaped)s - DocInspector Blog</title>
  <meta name="description" content="%(desc_escaped)s" />
  <link rel="canonical" href="https://doc-inspector.com/%(lang_prefix)sblog/%(curr_slug)s.html" />
  <link rel="alternate" hreflang="en" href="https://doc-inspector.com/en/blog/%(en_slug)s.html" />
  <link rel="alternate" hreflang="ro" href="https://doc-inspector.com/ro/blog/%(ro_slug)s.html" />
  <link rel="alternate" hreflang="ru" href="https://doc-inspector.com/ru/blog/%(ru_slug)s.html" />
  <link rel="alternate" hreflang="x-default" href="https://doc-inspector.com/en/blog/%(en_slug)s.html" />
  <link rel="stylesheet" href="../../style.css?v=9">
  <link rel="icon" href="../../assets/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@700;800;900&display=swap" rel="stylesheet">
</head>
<body style="background:#0a1628;color:#e2e8f0">
<header class="site-header">
  <div class="container">
    <nav class="navbar">
      <a href="../index.html" class="brand">
        <span class="brand-logo"><img src="../../assets/logo.png" alt="DocInspector" width="38" height="38"></span>
        <span>
          <span class="brand-name" data-i18n="brand.name">DocInspector</span><br>
          <span class="brand-subtitle" data-i18n="brand.subtitle">Repair, Batch Manager of Documents & Audit Suite</span>
        </span>
      </a>

      <div class="nav-links">
        <a href="../index.html" data-i18n="nav.home">Home</a>
        <a href="../%(price_slug)s" data-i18n="nav.price">Price</a>
        <a href="../%(guide_slug)s" data-i18n="nav.guide">User Guide</a>
        <a href="../%(reports_slug)s" data-i18n="nav.reports">Reports & Feedback</a>
        <a href="../blog.html" class="active" data-i18n="nav.blog">Blog</a>
        <a href="../%(contact_slug)s" data-i18n="nav.contact">Contact</a>
        <a href="../%(download_slug)s" class="btn btn-primary btn-sm mobile-only" data-i18n="nav.download">Download</a>
      </div>

      <div class="nav-actions">
        <div class="lang-dropdown">
          <button class="lang-btn" aria-label="Language">
            <span class="lang-pill">%(lang_upper)s</span>
            <span class="chev">▾</span>
          </button>
          <div class="lang-menu">
            <a href="../../en/blog/%(en_slug)s.html" class="lang-item%(en_active)s" data-lang="en">EN</a>
            <a href="../../ro/blog/%(ro_slug)s.html" class="lang-item%(ro_active)s" data-lang="ro">RO</a>
            <a href="../../ru/blog/%(ru_slug)s.html" class="lang-item%(ru_active)s" data-lang="ru">RU</a>
          </div>
        </div>
        <a href="../%(download_slug)s" class="btn btn-primary btn-sm desktop-only" data-i18n="nav.download">Download</a>
      </div>

      <button class="nav-toggle" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </nav>
  </div>
</header>
<main class="container article-container section-gap" style="max-width:800px;margin:0 auto;padding-top:120px;">
  <article class="reveal">
    <div class="article-meta" style="margin-bottom:1rem;opacity:0.8;">
       <span class="blog-category" data-i18n="blog.cat.%(category)s">%(cat_display)s</span> | <time datetime="%(date)s">%(date)s</time>
    </div>
    <h1 style="font-family:Outfit,sans-serif;font-size:2.5rem;margin-bottom:2rem;line-height:1.2;">%(title_escaped)s</h1>
    <div class="article-body" style="font-size:1.1rem;line-height:1.7;color:#cbd5e1;">
      %(body)s
    </div>
    <div style="margin-top:4rem;padding-top:2rem;border-top:1px solid rgba(255,255,255,0.1);">
      <a href="../blog.html" data-i18n="blog.backToList">← Back to Blog</a>
    </div>
  </article>
</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-inner">
      <span data-i18n="footer.copyright">© 2025 DocInspector. All rights reserved.</span>
      <div class="footer-links">
        <a href="../%(privacy_slug)s" data-i18n="footer.privacy">Privacy Policy</a>
        <a href="../%(terms_slug)s" data-i18n="footer.terms">Terms of Service</a>
        <a href="../%(refund_slug)s" data-i18n="footer.refund">Refund Policy</a>
        <a href="https://www.tiktok.com/@docinspector" target="_blank" rel="noopener" class="tiktok-link" aria-label="TikTok">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5 2.89 2.89 0 0 1 0-5.78 2.92 2.92 0 0 1 .88.13v-3.5a6.37 6.37 0 0 0-.88-.07A6.26 6.26 0 0 0 3.23 15.2 6.26 6.26 0 0 0 9.49 21.5a6.27 6.27 0 0 0 6.27-6.27V8.77a8.16 8.16 0 0 0 3.83.96V6.28a4.84 4.84 0 0 1-1-.09l1 .5z"/></svg>
        </a>
      </div>
    </div>
  </div>
</footer>
<script src="../../cookies.js"></script>
<script src="../../i18n-dict.js"></script>
<script src="../../i18n.js"></script>
<script src="../../scroll-fx.js?v=9"></script>
</body>
</html>'''

LISTING_HEADER = '''<!DOCTYPE html>
<html lang="%(lang)s">
<head>
  <meta charset="UTF-8"><title>Blog - DocInspector</title>
  <link rel="canonical" href="https://doc-inspector.com/%(lang_prefix)sblog.html" />
  <link rel="alternate" hreflang="en" href="https://doc-inspector.com/en/blog.html" />
  <link rel="alternate" hreflang="ro" href="https://doc-inspector.com/ro/blog.html" />
  <link rel="alternate" hreflang="ru" href="https://doc-inspector.com/ru/blog.html" />
  <link rel="alternate" hreflang="x-default" href="https://doc-inspector.com/en/blog.html" />
  <link rel="stylesheet" href="../style.css?v=9">
  <link rel="icon" href="../assets/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@700;800;900&display=swap" rel="stylesheet">
</head>
<body style="background:#0a1628;color:#e2e8f0">
<header class="site-header">
  <div class="container">
    <nav class="navbar">
      <a href="index.html" class="brand">
        <span class="brand-logo"><img src="../assets/logo.png" alt="DocInspector" width="38" height="38"></span>
        <span>
          <span class="brand-name" data-i18n="brand.name">DocInspector</span><br>
          <span class="brand-subtitle" data-i18n="brand.subtitle">Repair, Batch Manager of Documents & Audit Suite</span>
        </span>
      </a>

      <div class="nav-links">
        <a href="index.html" data-i18n="nav.home">Home</a>
        <a href="%(price_slug)s" data-i18n="nav.price">Price</a>
        <a href="%(guide_slug)s" data-i18n="nav.guide">User Guide</a>
        <a href="%(reports_slug)s" data-i18n="nav.reports">Reports & Feedback</a>
        <a href="blog.html" class="active" data-i18n="nav.blog">Blog</a>
        <a href="%(contact_slug)s" data-i18n="nav.contact">Contact</a>
        <a href="%(download_slug)s" class="btn btn-primary btn-sm mobile-only" data-i18n="nav.download">Download</a>
      </div>

      <div class="nav-actions">
        <div class="lang-dropdown">
          <button class="lang-btn" aria-label="Language">
            <span class="lang-pill">%(lang_upper)s</span>
            <span class="chev">▾</span>
          </button>
          <div class="lang-menu">
            <a href="../en/blog.html" class="lang-item%(en_active)s" data-lang="en">EN</a>
            <a href="../ro/blog.html" class="lang-item%(ro_active)s" data-lang="ro">RO</a>
            <a href="../ru/blog.html" class="lang-item%(ru_active)s" data-lang="ru">RU</a>
          </div>
        </div>
        <a href="%(download_slug)s" class="btn btn-primary btn-sm desktop-only" data-i18n="nav.download">Download</a>
      </div>

      <button class="nav-toggle" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </nav>
  </div>
</header>
<main class="container section-gap">
  <div class="section-header" style="text-align:center;margin-bottom:3rem;">
    <h1 data-i18n="blog.pageTitle">Blog</h1>
    <p data-i18n="blog.pageSubtitle">Tips and insights on document security</p>
  </div>
  <div class="blog-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:2rem;">'''

CARD_TEMPLATE = '''    <a href="blog/%(current_slug)s.html" class="blog-card reveal" style="text-decoration:none;color:inherit;background:rgba(255,255,255,0.03);padding:2rem;border-radius:12px;border:1px solid rgba(255,255,255,0.1);transition:all 0.3s ease;">
      <div class="blog-card-meta" style="margin-bottom:1rem;opacity:0.6;font-size:0.8rem;">
        <span data-i18n="blog.cat.%(category)s">%(cat_display)s</span> | %(date)s
      </div>
      <h3 style="margin-bottom:1rem;font-family:Outfit,sans-serif;">%(title_escaped)s</h3>
      <p style="opacity:0.7;font-size:0.95rem;line-height:1.5;">%(desc_escaped)s</p>
      <div style="margin-top:1.5rem;color:#38bdf8;font-weight:600;" data-i18n="blog.readMore">Read article →</div>
    </a>'''

LISTING_FOOTER = '''  </div>
</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-inner">
      <span data-i18n="footer.copyright">© 2025 DocInspector. All rights reserved.</span>
      <div class="footer-links">
        <a href="%(privacy_slug)s" data-i18n="footer.privacy">Privacy Policy</a>
        <a href="%(terms_slug)s" data-i18n="footer.terms">Terms of Service</a>
        <a href="%(refund_slug)s" data-i18n="footer.refund">Refund Policy</a>
        <a href="https://www.tiktok.com/@docinspector" target="_blank" rel="noopener" class="tiktok-link" aria-label="TikTok">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5 2.89 2.89 0 0 1 0-5.78 2.92 2.92 0 0 1 .88.13v-3.5a6.37 6.37 0 0 0-.88-.07A6.26 6.26 0 0 0 3.23 15.2 6.26 6.26 0 0 0 9.49 21.5a6.27 6.27 0 0 0 6.27-6.27V8.77a8.16 8.16 0 0 0 3.83.96V6.28a4.84 4.84 0 0 1-1-.09l1 .5z"/></svg>
        </a>
      </div>
    </div>
  </div>
</footer>
<script src="../cookies.js"></script>
<script src="../i18n-dict.js"></script>
<script src="../i18n.js"></script>
<script src="../scroll-fx.js?v=9"></script>
</body>
</html>'''

def translate_content(html, lang):
    if not I18N_DICT or lang.upper() not in I18N_DICT: return html
    trans = I18N_DICT[lang.upper()]
    for key, val in trans.items():
        pattern = re.compile(f'(<[^>]+data-i18n="{key}"[^>]*>)(.*?)(</[^>]+>)', re.DOTALL)
        html = pattern.sub(lambda m, v=val: m.group(1) + v + m.group(3), html)
        pattern_html = re.compile(f'(<[^>]+data-i18n-html="{key}"[^>]*>)(.*?)(</[^>]+>)', re.DOTALL)
        html = pattern_html.sub(lambda m, v=val: m.group(1) + v + m.group(3), html)
    return html

def generate_blog():
    print("Generating blog in new symmetric structure (/en/, /ro/, /ru/)...")
    for lang in ["en", "ro", "ru"]:
        lang_dir = os.path.join(DIR, lang)
        os.makedirs(os.path.join(lang_dir, "blog"), exist_ok=True)
        
        # 1. Listing page
        cards = []
        for a in ARTICLES:
            slug = a["slug"] if lang=="en" else (a.get("slug_ro") if lang=="ro" else a.get("slug_ru"))
            if not slug: slug = a["slug"]
            cards.append(CARD_TEMPLATE % {
                "current_slug": slug, "date": a["date"],
                "category": a["category"], "cat_display": CATEGORIES[a["category"]][lang],
                "title_escaped": htmlmod.escape(a[lang]["title"]),
                "desc_escaped": htmlmod.escape(a[lang]["desc"]),
            })
        
        h_vals = {
            "lang": lang, "lang_upper": lang.upper(),
            "lang_prefix": f"{lang}/" if lang != "en" else "",
            "price_slug": SLUG_MAP["price.html"][lang],
            "guide_slug": SLUG_MAP["user-guide.html"][lang],
            "reports_slug": SLUG_MAP["reports.html"][lang],
            "contact_slug": SLUG_MAP["contact.html"][lang],
            "download_slug": SLUG_MAP["download.html"][lang],
            "privacy_slug": SLUG_MAP["privacy.html"][lang],
            "terms_slug": SLUG_MAP["terms.html"][lang],
            "refund_slug": SLUG_MAP["refund.html"][lang],
            "en_active": " active" if lang == "en" else "",
            "ro_active": " active" if lang == "ro" else "",
            "ru_active": " active" if lang == "ru" else ""
        }
        l_html = (LISTING_HEADER % h_vals) + "\n".join(cards) + (LISTING_FOOTER % h_vals)
        l_html = translate_content(l_html, lang)
        with open(os.path.join(lang_dir, "blog.html"), "w", encoding='utf-8') as f: f.write(l_html)
        print(f"  + {lang}/blog.html")

        # 2. Individual articles
        for a in ARTICLES:
            s_en, s_ro, s_ru = a["slug"], a.get("slug_ro", a["slug"]), a.get("slug_ru", a["slug"])
            curr = {"en":s_en, "ro":s_ro, "ru":s_ru}[lang]
            
            vals = {
                "title_escaped": htmlmod.escape(a[lang]["title"]),
                "desc_escaped": htmlmod.escape(a[lang]["desc"]),
                "body": a[lang]["body"], "date": a["date"], "category": a["category"],
                "cat_display": CATEGORIES[a["category"]][lang],
                "lang": lang, "lang_upper": lang.upper(),
                "lang_prefix": f"{lang}/" if lang != "en" else "",
                "curr_slug": curr,
                "en_slug": s_en, "ro_slug": s_ro, "ru_slug": s_ru,
                "price_slug": SLUG_MAP["price.html"][lang],
                "guide_slug": SLUG_MAP["user-guide.html"][lang],
                "reports_slug": SLUG_MAP["reports.html"][lang],
                "contact_slug": SLUG_MAP["contact.html"][lang],
                "download_slug": SLUG_MAP["download.html"][lang],
                "privacy_slug": SLUG_MAP["privacy.html"][lang],
                "terms_slug": SLUG_MAP["terms.html"][lang],
                "refund_slug": SLUG_MAP["refund.html"][lang],
                "en_active": " active" if lang == "en" else "",
                "ro_active": " active" if lang == "ro" else "",
                "ru_active": " active" if lang == "ru" else ""
            }
            page_html = translate_content(ARTICLE_TEMPLATE % vals, lang)
            with open(os.path.join(lang_dir, "blog", curr + ".html"), "w", encoding='utf-8') as f: f.write(page_html)
            print(f"  + {lang}/blog/{curr}.html")

if __name__ == "__main__":
    generate_blog()
    print("\nBLOG BUILD COMPLETE.")
