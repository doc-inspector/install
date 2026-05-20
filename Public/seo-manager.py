#!/usr/bin/env python3
"""Unified SEO Manager for doc-inspector.com"""
import os, json, datetime, re

DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://doc-inspector.com"
TODAY = datetime.date.today().isoformat()

# Languages to support
LANGS = ["en", "ro", "ru"]

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
    "thanks.html": {"en": "thanks.html", "ro": "multumim.html", "ru": "spasibo.html"}
}

def get_pages():
    """Get all static pages and blog posts"""
    pages = []
    
    # 1. Main pages (EN, RO, RU)
    for p_en, langs in SLUG_MAP.items():
        if not os.path.exists(os.path.join(DIR, "en", p_en)): continue
        
        # EN version
        pages.append({
            "url": f"{BASE_URL}/en/{p_en}",
            "lastmod": TODAY,
            "changefreq": "weekly",
            "priority": "1.0" if p_en == "index.html" else "0.8",
            "slugs": langs,
            "type": "main",
            "lang": "en"
        })
        
        # RO version
        pages.append({
            "url": f"{BASE_URL}/ro/{langs['ro']}",
            "lastmod": TODAY,
            "changefreq": "weekly",
            "priority": "0.7",
            "slugs": langs,
            "type": "main",
            "lang": "ro"
        })
        
        # RU version
        pages.append({
            "url": f"{BASE_URL}/ru/{langs['ru']}",
            "lastmod": TODAY,
            "changefreq": "weekly",
            "priority": "0.7",
            "slugs": langs,
            "type": "main",
            "lang": "ru"
        })

    # 2. Blog listing pages
    pages.append({"url": f"{BASE_URL}/en/blog.html", "lastmod": TODAY, "changefreq": "weekly", "priority": "0.9", "id": "blog.html", "type": "blog_listing", "lang": "en"})
    pages.append({"url": f"{BASE_URL}/ro/blog.html", "lastmod": TODAY, "changefreq": "weekly", "priority": "0.7", "id": "ro/blog.html", "type": "blog_listing", "lang": "ro"})
    pages.append({"url": f"{BASE_URL}/ru/blog.html", "lastmod": TODAY, "changefreq": "weekly", "priority": "0.7", "id": "ru/blog.html", "type": "blog_listing", "lang": "ru"})

    # 3. Blog articles
    articles_path = os.path.join(DIR, "articles.json")
    if os.path.exists(articles_path):
        with open(articles_path, encoding='utf-8') as f:
            articles = json.load(f)
        for a in articles:
            s_en = a["slug"]
            s_ro = a.get("slug_ro", s_en)
            s_ru = a.get("slug_ru", s_en)
            
            # EN
            pages.append({
                "url": f"{BASE_URL}/en/blog/{s_en}.html",
                "lastmod": a["date"],
                "changefreq": "monthly",
                "priority": "0.6",
                "slugs": {"en": s_en, "ro": s_ro, "ru": s_ru},
                "type": "article",
                "lang": "en"
            })
            # RO
            pages.append({
                "url": f"{BASE_URL}/ro/blog/{s_ro}.html",
                "lastmod": a["date"],
                "changefreq": "monthly",
                "priority": "0.5",
                "slugs": {"en": s_en, "ro": s_ro, "ru": s_ru},
                "type": "article",
                "lang": "ro"
            })
            # RU
            pages.append({
                "url": f"{BASE_URL}/ru/blog/{s_ru}.html",
                "lastmod": a["date"],
                "changefreq": "monthly",
                "priority": "0.5",
                "slugs": {"en": s_en, "ro": s_ro, "ru": s_ru},
                "type": "article",
                "lang": "ru"
            })
    
    return pages

def generate_sitemap(pages):
    """Generate XML sitemap with hreflang tags"""
    print("Generating sitemap.xml...")
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    
    for p in pages:
        xml.append('  <url>')
        xml.append(f'    <loc>{p["url"]}</loc>')
        xml.append(f'    <lastmod>{p["lastmod"]}</lastmod>')
        xml.append(f'    <changefreq>{p["changefreq"]}</changefreq>')
        xml.append(f'    <priority>{p["priority"]}</priority>')
        
        # Add hreflang for articles and main pages
        if p.get("slugs"):
            s = p["slugs"]
            is_article = p.get("type") == "article"
            prefix_en = "en/blog/" if is_article else "en/"
            prefix_ro = "ro/blog/" if is_article else "ro/"
            prefix_ru = "ru/blog/" if is_article else "ru/"
            
            suffix = ".html" if is_article else ""
            url_en = f"{BASE_URL}/{prefix_en}{s['en']}{suffix}"
            url_ro = f"{BASE_URL}/{prefix_ro}{s['ro']}{suffix}"
            url_ru = f"{BASE_URL}/{prefix_ru}{s['ru']}{suffix}"
            
            xml.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{url_en}"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="ro" href="{url_ro}"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="ru" href="{url_ru}"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url_en}"/>')
        
        elif p.get("type") == "blog_listing":
            xml.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE_URL}/en/blog.html"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="ro" href="{BASE_URL}/ro/blog.html"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="ru" href="{BASE_URL}/ru/blog.html"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/en/blog.html"/>')
        elif p.get("id") in ["blog.html", "ro/blog.html", "ru/blog.html"]:
            xml.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE_URL}/en/blog.html"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="ro" href="{BASE_URL}/ro/blog.html"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="ru" href="{BASE_URL}/ru/blog.html"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/en/blog.html"/>')
        
        xml.append('  </url>')
    
    xml.append('</urlset>')
    
    with open(os.path.join(DIR, "sitemap.xml"), "w", encoding='utf-8') as f:
        f.write("\n".join(xml))
    print(f"  + sitemap.xml with {len(pages)} entries")

def generate_robots():
    """Generate robots.txt"""
    print("Generating robots.txt...")
    content = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(DIR, "robots.txt"), "w") as f:
        f.write(content)
    print("  + robots.txt")

def patch_head_tags():
    """Add canonical and hreflang tags to all main pages in en/, ro/, and ru/ subdirectories"""
    print("Patching main pages for SEO...")
    
    for p_en, langs in SLUG_MAP.items():
        path_en = os.path.join(DIR, "en", p_en)
        path_ro = os.path.join(DIR, "ro", langs["ro"])
        path_ru = os.path.join(DIR, "ru", langs["ru"])
        
        for lang, path in [("en", path_en), ("ro", path_ro), ("ru", path_ru)]:
            if not os.path.exists(path): continue
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            url_en = f"{BASE_URL}/en/{p_en}"
            url_ro = f"{BASE_URL}/ro/{langs['ro']}"
            url_ru = f"{BASE_URL}/ru/{langs['ru']}"
            
            curr_canonical = f"{BASE_URL}/{lang}/{langs[lang]}" if lang != "en" else f"{BASE_URL}/en/{p_en}"
            
            seo_block = f'\n  <link rel="canonical" href="{curr_canonical}" />\n'
            seo_block += f'  <link rel="alternate" hreflang="en" href="{url_en}" />\n'
            seo_block += f'  <link rel="alternate" hreflang="ro" href="{url_ro}" />\n'
            seo_block += f'  <link rel="alternate" hreflang="ru" href="{url_ru}" />\n'
            seo_block += f'  <link rel="alternate" hreflang="x-default" href="{url_en}" />'
            
            content = re.sub(r'\s*<link rel="canonical"[^>]*/?>\n?', '', content)
            content = re.sub(r'\s*<link rel="alternate" hreflang=[^>]*/?>\n?', '', content)
            
            content = content.replace('</head>', f'{seo_block}\n</head>')
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [OK] Patched head tags for {lang}/{os.path.basename(path)}")

if __name__ == "__main__":
    pages = get_pages()
    generate_sitemap(pages)
    generate_robots()
    patch_head_tags()
    print("\nSEO Update Complete!")
