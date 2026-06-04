import re

files = [
    r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix max-height
    content = content.replace('max-height:350px;', 'max-height:1200px;')
    
    # 2. Fix the label for confirm password to be more explicit
    # en: Confirm Password (Required if encrypting) -> Confirm Document Open Password
    # ro: Confirmă Parola (Obligatoriu) -> Confirmă Parola pt. Deschidere
    # ru: Подтвердите пароль (Обязательно) -> Подтвердите пароль для открытия
    content = content.replace(
        '<label class="opt-label" for="enc-pw2">Confirm Password (Required if encrypting)</label>',
        '<label class="opt-label" for="enc-pw2">Confirm Document Open Password</label>'
    )
    content = content.replace(
        '<label class="opt-label" for="enc-pw2">Confirmă Parola (Obligatoriu)</label>',
        '<label class="opt-label" for="enc-pw2">Confirmă Parola pt. Deschidere (Obligatoriu)</label>'
    )
    content = content.replace(
        '<label class="opt-label" for="enc-pw2">Подтвердите пароль (Обязательно)</label>',
        '<label class="opt-label" for="enc-pw2">Подтвердите пароль для открытия (Обязательно)</label>'
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed max-height and labels!")
