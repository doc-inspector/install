import re

files = [
    r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
]

def add_owner_confirm(content, lang):
    if 'id="enc-owner2"' in content: return content
    
    label_text = {
        'en': 'Confirm Permissions Password',
        'ro': 'Confirmă Parola pt. Permisiuni',
        'ru': 'Подтвердите пароль для разрешений'
    }
    placeholder = {
        'en': 'Re-enter to confirm',
        'ro': 'Reintroduceți pentru confirmare',
        'ru': 'Введите еще раз для подтверждения'
    }
    
    # We want to insert the confirm password right after enc-owner div.
    pattern = r'(<input class="opt-input" id="enc-owner" type="password"[^>]*>\s*</div>)'
    replacement = r'\1\n                <div class="opt-row" style="margin-top:0.5rem;">\n                  <label class="opt-label" for="enc-owner2">{label}</label>\n                  <input class="opt-input" id="enc-owner2" type="password" placeholder="{ph}">\n                </div>'.format(label=label_text[lang], ph=placeholder[lang])
    
    return re.sub(pattern, replacement, content)

def fix_js(content):
    if "pwOwner2" in content: return content
    # Add validation for owner password
    pattern = r"(const pw2 = document\.getElementById\('enc-pw2'\)\.value;\s*if \(!pw\)\s*\{\s*alert\('Please enter an encryption password\.'\);\s*return;\s*\}\s*if \(pw !== pw2\)\{\s*alert\('Passwords do not match\.'\);\s*return;\s*\})"
    replacement = r"\1\n      const pwOwner = document.getElementById('enc-owner').value;\n      const pwOwner2 = document.getElementById('enc-owner2').value;\n      if (pwOwner && pwOwner !== pwOwner2) { alert('Permissions passwords do not match.'); return; }"
    return re.sub(pattern, replacement, content)

for lang_idx, filepath in enumerate(files):
    lang = ['en', 'ro', 'ru'][lang_idx]
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix max-height
    content = content.replace('max-height:350px;', 'max-height:1200px;')
    
    # 2. Fix the label for confirm password to be more explicit
    content = content.replace(
        '<label class="opt-label" for="enc-pw2">Confirm Password (Required if encrypting)</label>',
        '<label class="opt-label" for="enc-pw2">Confirm Document Open Password</label>'
    )
    content = content.replace(
        '<label class="opt-label" for="enc-pw2">Confirmă Parola (Obligatoriu)</label>',
        '<label class="opt-label" for="enc-pw2">Confirmă Parola pt. Deschidere</label>'
    )
    content = content.replace(
        '<label class="opt-label" for="enc-pw2">Подтвердите пароль (Обязательно)</label>',
        '<label class="opt-label" for="enc-pw2">Подтвердите пароль для открытия</label>'
    )
    
    # 3. Add enc-owner2
    content = add_owner_confirm(content, lang)
    
    # 4. Fix JS
    content = fix_js(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed max-height, labels, and added owner confirm!")
