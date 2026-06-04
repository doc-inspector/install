import re
import os

files_to_update = {
    'en': r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    'ro': r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    'ru': r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
}

# 1. Add enc-pw2
def add_confirm_pw(content, lang):
    if 'id="enc-pw2"' in content: return content
    
    label_text = {
        'en': 'Confirm Password (Required if encrypting)',
        'ro': 'Confirmă Parola (Obligatoriu)',
        'ru': 'Подтвердите пароль (Обязательно)'
    }
    placeholder = {
        'en': 'Re-enter to confirm',
        'ro': 'Reintroduceți pentru confirmare',
        'ru': 'Введите еще раз для подтверждения'
    }
    
    # Find the enc-pw div
    # It looks like:
    # <div class="opt-row">
    #   <label class="opt-label" for="enc-pw">...</label>
    #   <input class="opt-input" id="enc-pw" ...>
    # </div>
    
    # We want to insert the confirm password right after it.
    pattern = r'(<input class="opt-input" id="enc-pw" type="password"[^>]*>\s*</div>)'
    
    replacement = r'\1\n              <div class="opt-row" style="margin-top:0.5rem;">\n                <label class="opt-label" for="enc-pw2">{label}</label>\n                <input class="opt-input" id="enc-pw2" type="password" placeholder="{ph}">\n              </div>'.format(label=label_text[lang], ph=placeholder[lang])
    
    return re.sub(pattern, replacement, content)

# 2. Add wm-angle to RO and RU
def add_wm_angle(content, lang):
    if 'id="wm-angle"' in content: return content
    
    label_text = {
        'ro': 'Unghi (Rotație)',
        'ru': 'Угол (Вращение)'
    }
    options = {
        'ro': '''<option value="-45" selected>Diagonal (-45&deg;)</option>
                    <option value="0">Drept (0&deg;)</option>
                    <option value="45">Diagonal (45&deg;)</option>''',
        'ru': '''<option value="-45" selected>Диагональ (-45&deg;)</option>
                    <option value="0">Прямо (0&deg;)</option>
                    <option value="45">Диагональ (45&deg;)</option>'''
    }
    
    pattern = r'(<span class="range-val" id="wm-op-v">.*?</span>\s*</div>\s*</div>)'
    replacement = r'\1\n                <div class="opt-row">\n                  <label class="opt-label" for="wm-angle">{label}</label>\n                  <select class="opt-select" id="wm-angle">\n                    {opts}\n                  </select>\n                </div>'.format(label=label_text[lang], opts=options[lang])
    
    return re.sub(pattern, replacement, content)


for lang, filepath in files_to_update.items():
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = add_confirm_pw(content, lang)
    if lang != 'en':
        content = add_wm_angle(content, lang)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("HTML files updated!")
