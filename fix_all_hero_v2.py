import re

files = {
    'en': r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    'ro': r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    'ru': r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
}

server_py = r"E:\Website online and local app new project\Public2\Public\server.py"

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

# 1. Fix HTML files
for lang, filepath in files.items():
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # robustly remove empty badges-row block
    content = re.sub(r'<div class="badges-row gsap-fade">\s*</div>', '', content)
    # also remove any existing populated badges-row just in case to avoid duplicates
    content = re.sub(r'<div class="badges-row gsap-fade">.*?</div>', '', content, flags=re.DOTALL)
    
    # inject the correct one right after hero-lead paragraph
    p_pattern = re.compile(r'(<p class="hero-lead gsap-fade">.*?</p>)', re.DOTALL)
    if p_pattern.search(content):
        content = p_pattern.sub(r'\1\n      ' + badges_html[lang], content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 2. Fix server.py
with open(server_py, 'r', encoding='utf-8') as f:
    server_content = f.read()

server_content = server_content.replace('pro_features = {"flatten", "redact"}', 'pro_features = set()')

with open(server_py, 'w', encoding='utf-8') as f:
    f.write(server_content)

print("Badges injected and server operations unlocked!")
