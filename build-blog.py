#!/usr/bin/env python3
"""Build blog system for doc-inspector.com from articles.json"""
import json, os, re, html as htmlmod

DIR = "/home/user/doc-inspector-redesign/Public"
BLOG_DIR = os.path.join(DIR, "blog")
os.makedirs(BLOG_DIR, exist_ok=True)

with open("/home/user/doc-inspector-redesign/articles.json") as f:
    ARTICLES = json.load(f)
print(f"Loaded {len(ARTICLES)} articles")

CATEGORIES = {
    "how-to": {"en": "How-To", "ro": "Cum se face", "ru": "Инструкция"},
    "security": {"en": "Security", "ro": "Securitate", "ru": "Безопасность"},
    "education": {"en": "Education", "ro": "Educație", "ru": "Обучение"},
    "industry": {"en": "Industry", "ro": "Industrie", "ru": "Отрасль"},
}

# ── Article HTML template ──
ARTICLE_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%(title_escaped)s — DocInspector Blog</title>
  <meta name="description" content="%(desc_escaped)s" />
  <link rel="canonical" href="https://doc-inspector.com/blog/%(slug)s.html" />
  <meta name="keywords" content="DocInspector, PDF, document, %(category)s, %(slug_keywords)s" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://doc-inspector.com/blog/%(slug)s.html" />
  <meta property="og:title" content="%(title_escaped)s" />
  <meta property="og:description" content="%(desc_escaped)s" />
  <meta property="og:image" content="https://doc-inspector.com/assets/logo.png" />
  <meta property="og:site_name" content="DocInspector" />
  <meta property="article:published_time" content="%(date)sT00:00:00+03:00" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="%(title_escaped)s" />
  <meta name="twitter:description" content="%(desc_escaped)s" />
  <meta name="twitter:image" content="https://doc-inspector.com/assets/logo.png" />
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "%(title_json)s",
    "description": "%(desc_json)s",
    "datePublished": "%(date)sT00:00:00+03:00",
    "dateModified": "%(date)sT00:00:00+03:00",
    "author": {"@type": "Organization", "name": "DocInspector", "url": "https://doc-inspector.com"},
    "publisher": {"@type": "Organization", "name": "DocInspector", "logo": {"@type": "ImageObject", "url": "https://doc-inspector.com/assets/logo.png"}},
    "mainEntityOfPage": {"@type": "WebPage", "@id": "https://doc-inspector.com/blog/%(slug)s.html"},
    "url": "https://doc-inspector.com/blog/%(slug)s.html",
    "inLanguage": "en",
    "articleSection": "%(category)s"
  }
  </script>
  <link rel="icon" href="../assets/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css?v=9">
  <style>
    .blog-article { max-width:780px; margin:0 auto; padding:3rem 1.5rem 4rem; }
    .blog-back { display:inline-flex; align-items:center; gap:.4rem; color:#60a5fa; text-decoration:none; font-size:.95rem; margin-bottom:2rem; transition:color .2s; }
    .blog-back:hover { color:#93c5fd; }
    .blog-meta { display:flex; align-items:center; gap:1rem; margin-bottom:1.5rem; font-size:.85rem; color:#94a3b8; }
    .blog-category { background:rgba(59,130,246,.15); color:#60a5fa; padding:.2rem .7rem; border-radius:999px; font-size:.78rem; font-weight:600; text-transform:uppercase; letter-spacing:.04em; }
    .blog-article h1 { font-family:'Outfit',sans-serif; font-size:clamp(1.7rem,4vw,2.4rem); font-weight:800; line-height:1.2; margin-bottom:1.5rem; background:linear-gradient(135deg,#fff 0%%,#60a5fa 100%%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
    .blog-body h2 { font-family:'Outfit',sans-serif; font-size:1.35rem; font-weight:700; margin:2rem 0 .8rem; color:#f1f5f9; }
    .blog-body p { font-size:1.05rem; line-height:1.75; color:#cbd5e1; margin-bottom:1rem; }
    .blog-body ul,.blog-body ol { margin:.5rem 0 1.2rem 1.5rem; color:#cbd5e1; }
    .blog-body li { margin-bottom:.5rem; font-size:1.02rem; line-height:1.6; }
    .blog-body strong { color:#f1f5f9; }
    .blog-cta { margin-top:3rem; padding:2rem; background:linear-gradient(135deg,rgba(59,130,246,.1) 0%%,rgba(139,92,246,.1) 100%%); border:1px solid rgba(59,130,246,.2); border-radius:1rem; text-align:center; }
    .blog-cta p { font-size:1.1rem; color:#e2e8f0; margin-bottom:1rem; }
    .blog-cta .btn { display:inline-flex; }
  </style>
</head>
<body style="background:#0a1628;color:#e2e8f0">
<div class="page">
<div id="progress-bar"></div>
<header class="site-header">
  <div class="container">
    <nav class="nav-bar">
      <a href="../index.html" class="nav-logo">
        <img src="../assets/logo.png" alt="DocInspector" width="38" height="38">
        <span data-i18n="brand.name">DocInspector</span>
      </a>
      <div class="nav-links">
        <a href="../index.html" data-i18n="nav.home">Home</a>
        <a href="../price.html" data-i18n="nav.price">Price</a>
        <a href="../user-guide.html" data-i18n="nav.guide">User Guide</a>
        <a href="../reports.html" data-i18n="nav.reports">Reports & Feedback</a>
        <a href="../blog.html" class="active" data-i18n="nav.blog">Blog</a>
        <a href="../contact.html" data-i18n="nav.contact">Contact</a>
        <a href="../download.html" class="btn btn-primary btn-sm mobile-only" data-i18n="nav.download">Download</a>
      </div>
      <div class="nav-actions">
        <div class="lang-dropdown">
          <button class="lang-btn" aria-label="Language"><span class="lang-pill">EN</span><span class="chev">▾</span></button>
          <div class="lang-menu">
            <button class="lang-item active" data-lang="EN">EN</button>
            <button class="lang-item" data-lang="RO">RO</button>
            <button class="lang-item" data-lang="RU">RU</button>
          </div>
        </div>
        <a href="../download.html" class="btn btn-primary btn-sm desktop-only" data-i18n="nav.download">Download</a>
      </div>
      <button class="nav-toggle" aria-label="Menu"><span></span><span></span><span></span></button>
    </nav>
  </div>
</header>
<article class="blog-article">
  <a href="../blog.html" class="blog-back" data-i18n="blog.backToList">← Back to all articles</a>
  <div class="blog-meta">
    <span class="blog-category" data-i18n="blog.cat.%(category)s">%(cat_display)s</span>
    <time datetime="%(date)s">%(date)s</time>
  </div>
  <h1 data-i18n="blog.%(slug)s.title">%(title_escaped)s</h1>
  <div class="blog-body" data-i18n-html="blog.%(slug)s.body">
    %(body)s
  </div>
  <div class="blog-cta">
    <p data-i18n="blog.ctaText">Ready to try DocInspector? Download the free 3-day trial.</p>
    <a href="../download.html" class="btn btn-primary" data-i18n="btn.download">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      Download 3-Day Trial
    </a>
  </div>
</article>
<footer class="site-footer">
  <div class="container">
    <div class="footer-inner">
      <span>© 2025 DocInspector. All rights reserved.</span>
      <div class="footer-links">
        <a href="../privacy.html" data-i18n="footer.privacy">Privacy Policy</a>
        <a href="../terms.html" data-i18n="footer.terms">Terms of Use</a>
        <a href="../refund.html" data-i18n="footer.refund">Refund Policy</a>
        <a href="https://www.tiktok.com/@docinspector" target="_blank" rel="noopener" class="tiktok-link" aria-label="TikTok">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5 2.89 2.89 0 0 1 0-5.78 2.92 2.92 0 0 1 .88.13v-3.5a6.37 6.37 0 0 0-.88-.07A6.26 6.26 0 0 0 3.23 15.2 6.26 6.26 0 0 0 9.49 21.5a6.27 6.27 0 0 0 6.27-6.27V8.77a8.16 8.16 0 0 0 3.83.96V6.28a4.84 4.84 0 0 1-1-.09l1 .5z"/></svg>
        </a>
      </div>
    </div>
  </div>
</footer>
</div>
<script src="../i18n-dict.js"></script>
<script src="../i18n.js"></script>
<script src="../scroll-fx.js?v=9"></script>
</body>
</html>'''


# ── Blog listing page template ──
LISTING_HEADER = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog — DocInspector</title>
  <meta name="description" content="Tips, guides, and insights on document security, PDF repair, batch processing, and digital compliance from DocInspector." />
  <link rel="canonical" href="https://doc-inspector.com/blog.html" />
  <meta name="keywords" content="DocInspector blog, PDF tips, document security, batch processing guide, metadata removal" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://doc-inspector.com/blog.html" />
  <meta property="og:title" content="Blog — DocInspector" />
  <meta property="og:description" content="Tips, guides, and insights on document security, PDF repair, batch processing, and digital compliance." />
  <meta property="og:image" content="https://doc-inspector.com/assets/logo.png" />
  <meta property="og:site_name" content="DocInspector" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Blog — DocInspector" />
  <meta name="twitter:description" content="Tips, guides, and insights on document security, PDF repair, batch processing, and digital compliance." />
  <meta name="twitter:image" content="https://doc-inspector.com/assets/logo.png" />
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Blog",
    "name": "DocInspector Blog",
    "description": "Tips, guides, and insights on document security, PDF repair, batch processing, and digital compliance.",
    "url": "https://doc-inspector.com/blog.html",
    "publisher": {"@type": "Organization", "name": "DocInspector", "logo": {"@type": "ImageObject", "url": "https://doc-inspector.com/assets/logo.png"}}
  }
  </script>
  <link rel="icon" href="assets/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css?v=9">
  <style>
    .blog-hero { text-align:center; padding:4rem 1.5rem 2rem; }
    .blog-hero h1 { font-family:'Outfit',sans-serif; font-size:clamp(2rem,5vw,3rem); font-weight:900; background:linear-gradient(135deg,#fff 0%,#60a5fa 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:.5rem; }
    .blog-hero p { color:#94a3b8; font-size:1.1rem; max-width:600px; margin:0 auto; }
    .blog-filter { display:flex; justify-content:center; gap:.5rem; flex-wrap:wrap; padding:0 1.5rem 2rem; }
    .blog-filter-btn { background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.1); color:#94a3b8; padding:.45rem 1rem; border-radius:999px; font-size:.85rem; cursor:pointer; transition:all .2s; }
    .blog-filter-btn:hover,.blog-filter-btn.active { background:rgba(59,130,246,.15); border-color:rgba(59,130,246,.3); color:#60a5fa; }
    .blog-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(340px,1fr)); gap:1.5rem; max-width:1100px; margin:0 auto; padding:0 1.5rem 4rem; }
    .blog-card { background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.06); border-radius:1rem; padding:1.5rem; text-decoration:none; color:inherit; transition:all .25s; display:flex; flex-direction:column; }
    .blog-card:hover { background:rgba(59,130,246,.06); border-color:rgba(59,130,246,.2); transform:translateY(-2px); }
    .blog-card-meta { display:flex; align-items:center; gap:.7rem; margin-bottom:.8rem; font-size:.82rem; color:#64748b; }
    .blog-category { background:rgba(59,130,246,.15); color:#60a5fa; padding:.18rem .6rem; border-radius:999px; font-size:.72rem; font-weight:600; text-transform:uppercase; letter-spacing:.04em; }
    .blog-card h3 { font-family:'Outfit',sans-serif; font-size:1.15rem; font-weight:700; color:#f1f5f9; margin-bottom:.5rem; line-height:1.3; }
    .blog-card p { font-size:.92rem; color:#94a3b8; line-height:1.55; flex:1; margin-bottom:.8rem; }
    .blog-read-more { font-size:.88rem; color:#60a5fa; font-weight:500; }
    @media(max-width:600px) { .blog-grid { grid-template-columns:1fr; } }
  </style>
</head>
<body style="background:#0a1628;color:#e2e8f0">
<div class="page">
<div id="progress-bar"></div>
<header class="site-header">
  <div class="container">
    <nav class="nav-bar">
      <a href="index.html" class="nav-logo">
        <img src="assets/logo.png" alt="DocInspector" width="38" height="38">
        <span data-i18n="brand.name">DocInspector</span>
      </a>
      <div class="nav-links">
        <a href="index.html" data-i18n="nav.home">Home</a>
        <a href="price.html" data-i18n="nav.price">Price</a>
        <a href="user-guide.html" data-i18n="nav.guide">User Guide</a>
        <a href="reports.html" data-i18n="nav.reports">Reports & Feedback</a>
        <a href="blog.html" class="active" data-i18n="nav.blog">Blog</a>
        <a href="contact.html" data-i18n="nav.contact">Contact</a>
        <a href="download.html" class="btn btn-primary btn-sm mobile-only" data-i18n="nav.download">Download</a>
      </div>
      <div class="nav-actions">
        <div class="lang-dropdown">
          <button class="lang-btn" aria-label="Language"><span class="lang-pill">EN</span><span class="chev">▾</span></button>
          <div class="lang-menu">
            <button class="lang-item active" data-lang="EN">EN</button>
            <button class="lang-item" data-lang="RO">RO</button>
            <button class="lang-item" data-lang="RU">RU</button>
          </div>
        </div>
        <a href="download.html" class="btn btn-primary btn-sm desktop-only" data-i18n="nav.download">Download</a>
      </div>
      <button class="nav-toggle" aria-label="Menu"><span></span><span></span><span></span></button>
    </nav>
  </div>
</header>

<div class="blog-hero">
  <h1 data-i18n="blog.pageTitle">Blog</h1>
  <p data-i18n="blog.pageSubtitle">Tips, guides, and insights on document security and batch processing</p>
</div>

<div class="blog-filter">
  <button class="blog-filter-btn active" data-filter="all" data-i18n="blog.filterAll">All</button>
  <button class="blog-filter-btn" data-filter="how-to" data-i18n="blog.cat.how-to">How-To</button>
  <button class="blog-filter-btn" data-filter="security" data-i18n="blog.cat.security">Security</button>
  <button class="blog-filter-btn" data-filter="education" data-i18n="blog.cat.education">Education</button>
  <button class="blog-filter-btn" data-filter="industry" data-i18n="blog.cat.industry">Industry</button>
</div>

<div class="blog-grid">
'''

LISTING_FOOTER = '''</div>

<footer class="site-footer">
  <div class="container">
    <div class="footer-inner">
      <span>© 2025 DocInspector. All rights reserved.</span>
      <div class="footer-links">
        <a href="privacy.html" data-i18n="footer.privacy">Privacy Policy</a>
        <a href="terms.html" data-i18n="footer.terms">Terms of Use</a>
        <a href="refund.html" data-i18n="footer.refund">Refund Policy</a>
        <a href="https://www.tiktok.com/@docinspector" target="_blank" rel="noopener" class="tiktok-link" aria-label="TikTok">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5 2.89 2.89 0 0 1 0-5.78 2.92 2.92 0 0 1 .88.13v-3.5a6.37 6.37 0 0 0-.88-.07A6.26 6.26 0 0 0 3.23 15.2 6.26 6.26 0 0 0 9.49 21.5a6.27 6.27 0 0 0 6.27-6.27V8.77a8.16 8.16 0 0 0 3.83.96V6.28a4.84 4.84 0 0 1-1-.09l1 .5z"/></svg>
        </a>
      </div>
    </div>
  </div>
</footer>
</div>
<script src="i18n-dict.js"></script>
<script src="i18n.js"></script>
<script src="scroll-fx.js?v=9"></script>
<script>
document.querySelectorAll('.blog-filter-btn').forEach(function(btn){
  btn.addEventListener('click',function(){
    document.querySelectorAll('.blog-filter-btn').forEach(function(b){b.classList.remove('active')});
    btn.classList.add('active');
    var filter=btn.dataset.filter;
    document.querySelectorAll('.blog-card').forEach(function(card){
      var cat=card.dataset.category||'';
      card.style.display=(filter==='all'||cat===filter)?'':'none';
    });
  });
});
</script>
</body>
</html>'''

CARD_TEMPLATE = '''    <a href="blog/%(slug)s.html" class="blog-card reveal" data-category="%(category)s">
      <div class="blog-card-meta">
        <span class="blog-category" data-i18n="blog.cat.%(category)s">%(cat_display)s</span>
        <time datetime="%(date)s">%(date)s</time>
      </div>
      <h3 data-i18n="blog.%(slug)s.title">%(title_escaped)s</h3>
      <p data-i18n="blog.%(slug)s.desc">%(desc_escaped)s</p>
      <span class="blog-read-more" data-i18n="blog.readMore">Read article →</span>
    </a>'''


# ══════════════════════════════════════
# GENERATE FILES
# ══════════════════════════════════════

# 1. Article pages
print("Generating article pages...")
for a in ARTICLES:
    vals = {
        "slug": a["slug"],
        "date": a["date"],
        "category": a["category"],
        "cat_display": CATEGORIES[a["category"]]["en"],
        "title_escaped": htmlmod.escape(a["en"]["title"]),
        "desc_escaped": htmlmod.escape(a["en"]["desc"]),
        "title_json": a["en"]["title"].replace('"', '\\"'),
        "desc_json": a["en"]["desc"].replace('"', '\\"'),
        "slug_keywords": a["slug"].replace("-", ", "),
        "body": a["en"]["body"],
    }
    page_html = ARTICLE_TEMPLATE % vals
    path = os.path.join(BLOG_DIR, a["slug"] + ".html")
    with open(path, "w") as f:
        f.write(page_html)
    print(f"  + blog/{a['slug']}.html")

# 2. Blog listing page
print("\nGenerating blog.html...")
cards = []
for a in ARTICLES:
    vals = {
        "slug": a["slug"],
        "date": a["date"],
        "category": a["category"],
        "cat_display": CATEGORIES[a["category"]]["en"],
        "title_escaped": htmlmod.escape(a["en"]["title"]),
        "desc_escaped": htmlmod.escape(a["en"]["desc"]),
    }
    cards.append(CARD_TEMPLATE % vals)

listing_html = LISTING_HEADER + "\n".join(cards) + "\n" + LISTING_FOOTER
with open(os.path.join(DIR, "blog.html"), "w") as f:
    f.write(listing_html)
print("  + blog.html")

# 3. Patch navbar on existing pages
print("\nPatching navbar...")
existing_pages = [f for f in os.listdir(DIR) if f.endswith(".html") and f != "blog.html"]
blog_link_html = '        <a href="blog.html" data-i18n="nav.blog">Blog</a>\n'
contact_re = re.compile(r'([ \t]*<a href="contact\.html"[^>]*data-i18n="nav\.contact"[^>]*>)')

for page in sorted(existing_pages):
    path = os.path.join(DIR, page)
    with open(path) as f:
        content = f.read()
    if 'data-i18n="nav.blog"' in content:
        print(f"  = {page} (already done)")
        continue
    new_content, n = contact_re.subn(blog_link_html + r'\1', content)
    if n > 0:
        with open(path, "w") as f:
            f.write(new_content)
        print(f"  + {page}")
    else:
        print(f"  ! {page} (no contact link found)")

# 4. i18n keys
print("\nUpdating i18n-dict.js...")
with open(os.path.join(DIR, "i18n-dict.js")) as f:
    i18n = f.read()

if '"nav.blog"' in i18n:
    print("  = i18n blog keys already present, skipping")
else:
    # Build blocks for each language
    def build_block(lang):
        lines = []
        lines.append('    // BLOG')
        nav_blog = {"en": "Blog", "ro": "Blog", "ru": "Блог"}
        lines.append('    "nav.blog": "%s",' % nav_blog[lang])
        page_title = {"en": "Blog", "ro": "Blog", "ru": "Блог"}
        lines.append('    "blog.pageTitle": "%s",' % page_title[lang])
        page_sub = {
            "en": "Tips, guides, and insights on document security and batch processing",
            "ro": "Sfaturi, ghiduri și perspective despre securitatea documentelor",
            "ru": "Советы, руководства и аналитика по безопасности документов"
        }
        lines.append('    "blog.pageSubtitle": "%s",' % page_sub[lang])
        back = {"en": "\\u2190 Back to all articles", "ro": "\\u2190 \\u00cenapoi la toate articolele", "ru": "\\u2190 \\u041d\\u0430\\u0437\\u0430\\u0434 \\u043a\\u043e \\u0432\\u0441\\u0435\\u043c \\u0441\\u0442\\u0430\\u0442\\u044c\\u044f\\u043c"}
        back_text = {"en": "← Back to all articles", "ro": "← Înapoi la toate articolele", "ru": "← Назад ко всем статьям"}
        lines.append('    "blog.backToList": "%s",' % back_text[lang])
        read = {"en": "Read article →", "ro": "Citește articolul →", "ru": "Читать статью →"}
        lines.append('    "blog.readMore": "%s",' % read[lang])
        filt = {"en": "All", "ro": "Toate", "ru": "Все"}
        lines.append('    "blog.filterAll": "%s",' % filt[lang])
        cta = {
            "en": "Ready to try DocInspector? Download the free 3-day trial.",
            "ro": "Gata să încerci DocInspector? Descarcă trialul gratuit de 3 zile.",
            "ru": "Готовы попробовать DocInspector? Скачайте бесплатную 3-дневную пробную версию."
        }
        lines.append('    "blog.ctaText": "%s",' % cta[lang])
        for ck, cv in CATEGORIES.items():
            lines.append('    "blog.cat.%s": "%s",' % (ck, cv[lang]))
        for a in ARTICLES:
            t = a[lang]["title"].replace('"', '\\"')
            d = a[lang]["desc"].replace('"', '\\"')
            lines.append('    "blog.%s.title": "%s",' % (a["slug"], t))
            lines.append('    "blog.%s.desc": "%s",' % (a["slug"], d))
            # Body as HTML string (escaped for JS string literal)
            b = a[lang]["body"].replace("\\", "\\\\").replace('"', '\\"').replace("\n", "")
            lines.append('    "blog.%s.body": "%s",' % (a["slug"], b))
        return "\n".join(lines)
    
    lang_map = [("EN", "en"), ("RO", "ro"), ("RU", "ru")]
    i18n_lines = i18n.split('\n')
    
    for lang_code, lang_key in lang_map:
        block = build_block(lang_key)
        # Find cookies.message in the right section
        section_start = None
        for i, line in enumerate(i18n_lines):
            stripped = line.strip()
            if stripped.startswith(lang_code + ':') or stripped.startswith(lang_code + ' :'):
                section_start = i
                break
        if section_start is None:
            print(f"  ! {lang_code} section not found")
            continue
        
        # Find cookies.message after section start
        cookies_line = None
        for i in range(section_start, len(i18n_lines)):
            if '"cookies.message"' in i18n_lines[i]:
                cookies_line = i
                break
        
        if cookies_line:
            i18n_lines.insert(cookies_line, block)
            print(f"  + {lang_code} blog keys inserted")
        else:
            print(f"  ! {lang_code} no cookies.message found")
    
    i18n = '\n'.join(i18n_lines)
    with open(os.path.join(DIR, "i18n-dict.js"), "w") as f:
        f.write(i18n)
    print("  + i18n-dict.js saved")

# 5. Update sitemap
print("\nUpdating sitemap.xml...")
with open(os.path.join(DIR, "sitemap.xml")) as f:
    sitemap = f.read()

if "blog.html" in sitemap:
    print("  = blog URLs already in sitemap")
else:
    new_urls = []
    new_urls.append('  <url>\n    <loc>https://doc-inspector.com/blog.html</loc>\n    <lastmod>2026-05-09</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>')
    for a in ARTICLES:
        new_urls.append('  <url>\n    <loc>https://doc-inspector.com/blog/%s.html</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>' % (a["slug"], a["date"]))
    
    insert = "\n".join(new_urls)
    sitemap = sitemap.replace("</urlset>", insert + "\n</urlset>")
    with open(os.path.join(DIR, "sitemap.xml"), "w") as f:
        f.write(sitemap)
    print(f"  + Added {len(new_urls)} URLs")

print("\n" + "="*50)
print("BLOG SYSTEM COMPLETE")
print(f"  {len(ARTICLES)} article pages")
print(f"  1 listing page (blog.html)")
print(f"  Navbar patched on existing pages")
print(f"  i18n keys for EN/RO/RU")
print(f"  Sitemap updated")
print("="*50)
