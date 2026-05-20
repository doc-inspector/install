import re

with open('en/index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# Extract header
header_match = re.search(r'(<header class="site-header">.*?</header>)', index_html, re.DOTALL)
header_html = header_match.group(1)

# Extract footer
footer_match = re.search(r'(<footer class="site-footer">.*?</footer>)', index_html, re.DOTALL)
footer_html = footer_match.group(1)

# We need to correctly map the language links for LISTING_HEADER
new_listing_header = '''<!DOCTYPE html>
<html lang="%(lang)s">
<head>
  <meta charset="UTF-8"><title>Blog - DocInspector</title>
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

new_listing_footer = '''  </div>
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

new_article_template = '''<!DOCTYPE html>
<html lang="%(lang)s">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%(title_escaped)s - DocInspector Blog</title>
  <meta name="description" content="%(desc_escaped)s" />
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

with open('build-blog.py', 'r', encoding='utf-8') as f:
    build_script = f.read()

build_script = re.sub(r'ARTICLE_TEMPLATE = \'\'\'.*?</html>\'\'\'', 'ARTICLE_TEMPLATE = \'\'\'' + new_article_template + '\'\'\'', build_script, flags=re.DOTALL)
build_script = re.sub(r'LISTING_HEADER = \'\'\'.*?<div class="blog-grid".*?>\'\'\'', 'LISTING_HEADER = \'\'\'' + new_listing_header + '\'\'\'', build_script, flags=re.DOTALL)
build_script = re.sub(r'LISTING_FOOTER = \'\'\'.*?</html>\'\'\'', 'LISTING_FOOTER = \'\'\'' + new_listing_footer + '\'\'\'', build_script, flags=re.DOTALL)

with open('build-blog.py', 'w', encoding='utf-8') as f:
    f.write(build_script)

print('Updated build-blog.py successfully.')
