#!/usr/bin/env python3
"""
update-headers.py
Standardizes all static pages' headers to match the Home Page header layout,
styling, micro-interactions, and responsiveness.
"""
import os
import re

DIR = os.path.dirname(os.path.abspath(__file__))

SLUG_MAP = {
    "index.html": {"en": "index.html", "ro": "index.html", "ru": "index.html"},
    "tools-online.html": {"en": "tools-online.html", "ro": "unelte-online.html", "ru": "onlayn-instrumenty.html"},
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

def extract_reference_header(lang):
    """Extracts the <header class="site-header"> block from lang/index.html"""
    path = os.path.join(DIR, lang, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    match = re.search(r'<header class="site-header">.*?</header>', content, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find reference header in {path}")
    return match.group(0)

def main():
    # 1. Extract reference headers
    ref_headers = {
        "en": extract_reference_header("en"),
        "ro": extract_reference_header("ro"),
        "ru": extract_reference_header("ru")
    }
    print("Extracted reference headers successfully.")

    # 2. Iterate through all static pages
    for p_en, langs in SLUG_MAP.items():
        for lang in ["en", "ro", "ru"]:
            slug_curr = langs[lang]
            page_path = os.path.join(DIR, lang, slug_curr)
            if not os.path.exists(page_path):
                print(f"Skipping {lang}/{slug_curr} (does not exist)")
                continue

            print(f"Standardizing header for: {lang}/{slug_curr}")

            # Load page content
            with open(page_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Start with the reference header for this language
            ref_header = ref_headers[lang]

            # A. Customize the active menu highlights
            # Extract nav-links block
            nav_links_match = re.search(r'<div class="nav-links">(.*?)</div>', ref_header, re.DOTALL)
            if nav_links_match:
                nav_links_html = nav_links_match.group(1)
                # Remove class="active" from all elements inside nav-links
                clean_nav_links_html = re.sub(r'\s*class="active"', '', nav_links_html)
                
                # Determine which page to highlight
                active_item = None
                if p_en == "index.html":
                    active_item = "./"
                elif p_en == "price.html":
                    active_item = SLUG_MAP["price.html"][lang].replace(".html", "")
                elif p_en == "blog.html":
                    active_item = "blog"
                elif p_en == "contact.html":
                    active_item = SLUG_MAP["contact.html"][lang].replace(".html", "")
                elif p_en.startswith("user-guide"):
                    active_item = SLUG_MAP["user-guide.html"][lang].replace(".html", "")

                # Inject class="active" to the highlighted link
                if active_item:
                    # Pattern matches href="active_item"
                    pattern = f'href="{active_item}"'
                    clean_nav_links_html = clean_nav_links_html.replace(pattern, f'href="{active_item}" class="active"')
                
                # Replace the nav-links block in our customized header
                ref_header = ref_header.replace(nav_links_html, clean_nav_links_html)

            # B. Customize the lang-dropdown menu relative links
            slug_en_raw = SLUG_MAP[p_en]["en"]
            slug_ro_raw = SLUG_MAP[p_en]["ro"]
            slug_ru_raw = SLUG_MAP[p_en]["ru"]

            # Remove .html for the links, handle index.html as ./ or directory roots
            slug_en = "./" if slug_en_raw == "index.html" else slug_en_raw.replace(".html", "")
            slug_ro = "./" if slug_ro_raw == "index.html" else slug_ro_raw.replace(".html", "")
            slug_ru = "./" if slug_ru_raw == "index.html" else slug_ru_raw.replace(".html", "")

            if lang == "en":
                en_href = slug_en
                ro_href = f"../ro/" if slug_ro_raw == "index.html" else f"../ro/{slug_ro}"
                ru_href = f"../ru/" if slug_ru_raw == "index.html" else f"../ru/{slug_ru}"
            elif lang == "ro":
                en_href = f"../en/" if slug_en_raw == "index.html" else f"../en/{slug_en}"
                ro_href = slug_ro
                ru_href = f"../ru/" if slug_ru_raw == "index.html" else f"../ru/{slug_ru}"
            else:  # ru
                en_href = f"../en/" if slug_en_raw == "index.html" else f"../en/{slug_en}"
                ro_href = f"../ro/" if slug_ro_raw == "index.html" else f"../ro/{slug_ro}"
                ru_href = slug_ru

            custom_dropdown = f"""<div class="lang-dropdown">
          <button class="lang-btn" aria-label="Language">
            <span class="lang-pill">{lang.upper()}</span>
            <span class="chev">▾</span>
          </button>
          <div class="lang-menu">
            <a href="{en_href}" class="lang-item{" active" if lang == "en" else ""}" data-lang="en">EN</a>
            <a href="{ro_href}" class="lang-item{" active" if lang == "ro" else ""}" data-lang="ro">RO</a>
            <a href="{ru_href}" class="lang-item{" active" if lang == "ru" else ""}" data-lang="ru">RU</a>
          </div>
        </div>"""

            # Regex-replace the extracted ref_header's dropdown block
            ref_header = re.sub(r'<div class="lang-dropdown">.*?</div>\s*</div>', custom_dropdown, ref_header, flags=re.DOTALL)

            # C. Perform search & replace on the file
            # Target both `<header class="site-header">` and variations like `<header class="site-header" id="siteHeader">`
            updated_content, count = re.subn(
                r'<header class="site-header"[^>]*>.*?</header>',
                ref_header,
                content,
                flags=re.DOTALL
            )

            if count > 0:
                with open(page_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print(f"  -> Successfully updated {lang}/{slug_curr}")
            else:
                print(f"  [WARNING] Could not find header block in {lang}/{slug_curr}")

    print("\nStatic headers standardization finished!")

if __name__ == "__main__":
    main()

