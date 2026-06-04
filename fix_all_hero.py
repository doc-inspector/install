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

# English original text from RO and RU (because we failed to replace them earlier)
en_pill = "Free Online Document Tools &#x2014; No Download Required"
en_h1 = "Process Documents Directly in Your Browser"
en_p_pattern = re.compile(r'Sanitize metadata, add watermarks.*?No account needed\.', re.DOTALL)

ro_pill = "UNELTE ONLINE GRATUITE PENTRU PDF &#x2014; FĂRĂ INSTALARE"
ro_h1 = "Procesează PDF-uri Direct în Browserul Tău"
ro_p = """Sanitizează metadate, adaugă watermark, criptează, redactează sau repară documente PDF online &#x2014; <strong style="color:#fff">sandbox izolat</strong>
        și șterse imediat după descărcare. Nu este necesar un cont."""

ru_pill = "БЕСПЛАТНЫЕ ОНЛАЙН ИНСТРУМЕНТЫ &#x2014; БЕЗ УСТАНОВКИ"
ru_h1 = "Обрабатывайте PDF Прямо в Браузере"
ru_p = """Очистка метаданных, добавление водяных знаков, шифрование, удаление данных или ремонт PDF документов онлайн. Файлы обрабатываются в <strong style="color:#fff">изолированной песочнице</strong>
        и удаляются сразу после скачивания."""

def process_file(lang, filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject Badges
    # First, let's remove any empty badges-row if it somehow still exists
    content = content.replace('<div class="badges-row gsap-fade">\n  \n      </div>', "")
    content = content.replace('<div class="badges-row gsap-fade">\n      </div>', "")
    
    # We look for where to inject it. We should inject it right after the hero-lead paragraph.
    p_pattern = re.compile(r'(<p class="hero-lead gsap-fade">.*?</p>)', re.DOTALL)
    if p_pattern.search(content):
        # check if it already has the HTML for badges (not just the CSS class)
        if '<div class="badges-row gsap-fade">' not in content:
            content = p_pattern.sub(r'\1\n      ' + badges_html[lang], content)

    # 2. Fix Translations for RO and RU
    if lang == 'ro':
        content = content.replace(en_pill, ro_pill)
        content = content.replace(en_h1, ro_h1)
        content = en_p_pattern.sub(ro_p, content)
    elif lang == 'ru':
        content = content.replace(en_pill, ru_pill)
        content = content.replace(en_h1, ru_h1)
        content = en_p_pattern.sub(ru_p, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for lang, filepath in files.items():
    process_file(lang, filepath)

print("Badges and translations injected successfully!")
