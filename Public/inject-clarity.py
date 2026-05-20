"""
inject-clarity.py
=================
Injectează scriptul de urmărire Microsoft Clarity în <head> al tuturor
fișierelor HTML din directoarele en/, ro/, ru/ (inclusiv subdirectoarele blog/).

Rulează o singură dată: python inject-clarity.py
"""

import os
import re

# ── Codul de urmărire Clarity ─────────────────────────────────────────────────
CLARITY_SCRIPT = """    <!-- Microsoft Clarity -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        })(window, document, "clarity", "script", "wu1m2q0juc");
    </script>"""

# Marker pentru a evita injectarea duplicată
CLARITY_MARKER = "clarity.ms/tag/wu1m2q0juc"

# Directorul rădăcină al site-ului (unde se află en/, ro/, ru/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Contoare ──────────────────────────────────────────────────────────────────
updated = 0
skipped_already = 0
skipped_no_head = 0
errors = 0

# ── Parcurgere recursivă ──────────────────────────────────────────────────────
for lang in ["en", "ro", "ru"]:
    lang_dir = os.path.join(BASE_DIR, lang)
    if not os.path.isdir(lang_dir):
        print(f"[WARN] Directorul '{lang}' nu există, se sare.")
        continue

    for root, dirs, files in os.walk(lang_dir):
        for fname in files:
            if not fname.endswith(".html"):
                continue

            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Sare dacă scriptul este deja prezent
                if CLARITY_MARKER in content:
                    skipped_already += 1
                    continue

                # Caută </head> (case-insensitive)
                match = re.search(r"</head>", content, re.IGNORECASE)
                if not match:
                    print(f"[WARN] Fără </head> în: {fpath}")
                    skipped_no_head += 1
                    continue

                # Injectează scriptul imediat înainte de </head>
                insert_pos = match.start()
                new_content = (
                    content[:insert_pos]
                    + "\n"
                    + CLARITY_SCRIPT
                    + "\n"
                    + content[insert_pos:]
                )

                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_content)

                rel = os.path.relpath(fpath, BASE_DIR)
                print(f"[OK]   {rel}")
                updated += 1

            except Exception as e:
                print(f"[ERR]  {fpath} → {e}")
                errors += 1

# ── Raport final ──────────────────────────────────────────────────────────────
print()
print("=" * 55)
print(f"  Fișiere actualizate   : {updated}")
print(f"  Deja aveau Clarity    : {skipped_already}")
print(f"  Fără </head> (sărite) : {skipped_no_head}")
print(f"  Erori                 : {errors}")
print("=" * 55)
print("Done! Încarcă toate fișierele pe GitHub pentru a face live.")
