"""
inject-ga4.py
=============
Injecteaza Google Analytics 4 (gtag.js) cu ID-ul G-80038W7D1J
in <head> al tuturor fisierelor HTML din en/, ro/, ru/ (inclusiv blog/).

Rulare: python inject-ga4.py
"""

import os
import re

# ── Codul Google Analytics 4 ─────────────────────────────────────────────────
GA4_SCRIPT = """    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-80038W7D1J"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-80038W7D1J');
    </script>"""

# Marker pentru a evita injectarea duplicata
GA4_MARKER = "G-80038W7D1J"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

updated = 0
skipped_already = 0
skipped_no_head = 0
errors = 0

for lang in ["en", "ro", "ru"]:
    lang_dir = os.path.join(BASE_DIR, lang)
    if not os.path.isdir(lang_dir):
        print(f"[WARN] Directorul '{lang}' nu exista, se sare.")
        continue

    for root, dirs, files in os.walk(lang_dir):
        for fname in files:
            if not fname.endswith(".html"):
                continue

            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Sare daca GA4 e deja prezent
                if GA4_MARKER in content:
                    skipped_already += 1
                    continue

                # Cauta </head>
                match = re.search(r"</head>", content, re.IGNORECASE)
                if not match:
                    print(f"[WARN] Fara </head> in: {fpath}")
                    skipped_no_head += 1
                    continue

                # Injecteaza imediat inainte de </head>
                insert_pos = match.start()
                new_content = (
                    content[:insert_pos]
                    + "\n"
                    + GA4_SCRIPT
                    + "\n"
                    + content[insert_pos:]
                )

                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_content)

                rel = os.path.relpath(fpath, BASE_DIR)
                print(f"[OK]   {rel}")
                updated += 1

            except Exception as e:
                print(f"[ERR]  {fpath} -> {e}")
                errors += 1

print()
print("=" * 50)
print(f"  Fisiere actualizate  : {updated}")
print(f"  Deja aveau GA4       : {skipped_already}")
print(f"  Fara </head> (sarite): {skipped_no_head}")
print(f"  Erori                : {errors}")
print("=" * 50)
print("Done! Incarca pe GitHub pentru a face live.")
