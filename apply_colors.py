import re
import os

colors = {
    'watermark': '#0ea5e9', # Sky Blue
    'sanitize': '#f97316',  # Orange
    'encrypt': '#a855f7',   # Purple
    'redact': '#ef4444',    # Red
    'flatten': '#10b981',   # Emerald
    'compress': '#eab308',  # Yellow
    'bundle': '#f59e0b'     # Amber
}

files = [
    r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
]

def update_html(content, lang):
    # 1. Update Tool Cards with --brand
    for tool, color in colors.items():
        card_pattern = r'(<div class="tool-card" id="card-{0}")( onclick="toggleTool)'.format(tool)
        content = re.sub(card_pattern, r'\1 style="--brand: {0};"\2'.format(color), content)
        
        opts_pattern = r'(<div class="tool-opts" id="opts-{0}")(>)'.format(tool)
        content = re.sub(opts_pattern, r'\1 style="--brand: {0};"\2'.format(color), content)
        
    # 2. Update the accent colors inside the panels to use var(--brand)
    # The title style is: style="font-size:0.85rem; font-weight:800; color:var(--cyan); ...
    content = content.replace('color:var(--cyan);', 'color:var(--brand, var(--cyan));')
    content = content.replace('accent-color:var(--cyan)', 'accent-color:var(--brand, var(--cyan))')
    
    # 3. Fix the encryption logic!
    if lang == 'en':
        js_replace = r"""
    if (selectedOps.has('encrypt')) {
      const pw  = document.getElementById('enc-pw') ? document.getElementById('enc-pw').value : '';
      const pw2 = document.getElementById('enc-pw2') ? document.getElementById('enc-pw2').value : '';
      const pwOwner = document.getElementById('enc-owner') ? document.getElementById('enc-owner').value : '';
      const pwOwner2 = document.getElementById('enc-owner2') ? document.getElementById('enc-owner2').value : '';
      if (!pw && !pwOwner) { alert('Please enter at least one password (Document Open or Permissions).'); return; }
      if (pw && pw !== pw2){ alert('Document Open Passwords do not match.'); return; }
      if (pwOwner && pwOwner !== pwOwner2) { alert('Permissions passwords do not match.'); return; }
    }"""
    elif lang == 'ro':
        js_replace = r"""
    if (selectedOps.has('encrypt')) {
      const pw  = document.getElementById('enc-pw') ? document.getElementById('enc-pw').value : '';
      const pw2 = document.getElementById('enc-pw2') ? document.getElementById('enc-pw2').value : '';
      const pwOwner = document.getElementById('enc-owner') ? document.getElementById('enc-owner').value : '';
      const pwOwner2 = document.getElementById('enc-owner2') ? document.getElementById('enc-owner2').value : '';
      if (!pw && !pwOwner) { alert('Vă rugăm introduceți o parolă (de Deschidere sau Permisiuni).'); return; }
      if (pw && pw !== pw2){ alert('Parolele de deschidere nu se potrivesc.'); return; }
      if (pwOwner && pwOwner !== pwOwner2) { alert('Parolele de permisiuni nu se potrivesc.'); return; }
    }"""
    elif lang == 'ru':
        js_replace = r"""
    if (selectedOps.has('encrypt')) {
      const pw  = document.getElementById('enc-pw') ? document.getElementById('enc-pw').value : '';
      const pw2 = document.getElementById('enc-pw2') ? document.getElementById('enc-pw2').value : '';
      const pwOwner = document.getElementById('enc-owner') ? document.getElementById('enc-owner').value : '';
      const pwOwner2 = document.getElementById('enc-owner2') ? document.getElementById('enc-owner2').value : '';
      if (!pw && !pwOwner) { alert('Пожалуйста, введите пароль (для открытия или для разрешений).'); return; }
      if (pw && pw !== pw2){ alert('Пароли для открытия не совпадают.'); return; }
      if (pwOwner && pwOwner !== pwOwner2) { alert('Пароли для разрешений не совпадают.'); return; }
    }"""
        
    # Find the old encrypt validation block
    pattern_js = r"if \(selectedOps\.has\('encrypt'\)\)\s*\{[\s\S]*?(?:return;\s*\}){1,3}\s*\}"
    content = re.sub(pattern_js, js_replace.strip(), content)
    
    return content

for i, filepath in enumerate(files):
    lang = ['en', 'ro', 'ru'][i]
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = update_html(content, lang)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("HTML files updated with colors and encryption logic!")
