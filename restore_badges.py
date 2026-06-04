import re

files = {
    'en': r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    'ro': r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    'ru': r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
}

badges_html = {
    'en': """<div class="badges-row gsap-fade">
        <span class="sec-badge">🛡️ Zero cloud storage</span>
        <span class="sec-badge">⚡ Deleted after download</span>
        <span class="sec-badge">🔒 Encrypted transit (HTTPS)</span>
        <span class="sec-badge">🤖 No AI — 100% deterministic</span>
        <span class="sec-badge">🇪🇺 GDPR Compliant</span>
        <span class="sec-badge">📄 Up to 100 files/day, free</span>
      </div>""",
      
    'ro': """<div class="badges-row gsap-fade">
        <span class="sec-badge">🛡️ Zero stocare în cloud</span>
        <span class="sec-badge">⚡ Șters după descărcare</span>
        <span class="sec-badge">🔒 Tranzit criptat (HTTPS)</span>
        <span class="sec-badge">🤖 Fără AI — 100% determinist</span>
        <span class="sec-badge">🇪🇺 Conform GDPR</span>
        <span class="sec-badge">📄 Până la 100 fișiere/zi, gratuit</span>
      </div>""",
      
    'ru': """<div class="badges-row gsap-fade">
        <span class="sec-badge">🛡️ Без облачного хранилища</span>
        <span class="sec-badge">⚡ Удаляется после скачивания</span>
        <span class="sec-badge">🔒 Зашифрованный трафик (HTTPS)</span>
        <span class="sec-badge">🤖 Без ИИ — 100% детерминированно</span>
        <span class="sec-badge">🇪🇺 Соответствует GDPR</span>
        <span class="sec-badge">📄 До 100 файлов/день бесплатно</span>
      </div>"""
}

for lang, filepath in files.items():
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the huge margin that was causing the empty space
    content = content.replace("margin-bottom:4rem;", "margin-bottom:1.5rem;")
    
    # Replace the empty badges-row with the populated one
    # Note: earlier I might have completely removed badges-row if it was empty using reduce_spacing.py.
    # Let's check if it exists.
    
    empty_badges = """<div class="badges-row gsap-fade">
  
      </div>"""
      
    # If the exact empty block is still there
    if empty_badges in content:
        content = content.replace(empty_badges, badges_html[lang])
    # If I already removed it, we need to inject it right after the hero-lead paragraph
    elif "hero-lead gsap-fade" in content:
        # regex to find </p> after hero-lead
        pattern = re.compile(r'(<p class="hero-lead gsap-fade">.*?</p>)', re.DOTALL)
        if pattern.search(content):
            # check if we already inserted badges to avoid duplicates
            if "sec-badge" not in content:
                content = pattern.sub(r'\1\n      ' + badges_html[lang], content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Badges restored and spacing optimized!")
