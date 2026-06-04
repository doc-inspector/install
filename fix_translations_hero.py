import os

ro_html = r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html"
ru_html = r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"

en_pill = "Free Online Document Tools &#x2014; No Download Required"
en_h1 = "Process Documents Directly in Your Browser"
en_p = """Sanitize metadata, add watermarks, encrypt, redact or repair your documents online &#x2014; <strong style="color:#fff">isolated sandbox</strong>
        and deleted immediately after download. No account needed."""

ro_pill = "UNELTE ONLINE GRATUITE PENTRU PDF &#x2014; FĂRĂ INSTALARE"
ro_h1 = "Procesează PDF-uri Direct în Browserul Tău"
ro_p = """Sanitizează metadate, adaugă watermark, criptează, redactează sau repară documente PDF online &#x2014; <strong style="color:#fff">sandbox izolat</strong>
        și șterse imediat după descărcare. Nu este necesar un cont."""

ru_pill = "БЕСПЛАТНЫЕ ОНЛАЙН ИНСТРУМЕНТЫ &#x2014; БЕЗ УСТАНОВКИ"
ru_h1 = "Обрабатывайте PDF Прямо в Браузере"
ru_p = """Очистка метаданных, добавление водяных знаков, шифрование, удаление данных или ремонт PDF документов онлайн. Файлы обрабатываются в <strong style="color:#fff">изолированной песочнице</strong>
        и удаляются сразу после скачивания."""

def fix_lang(filepath, pill, h1, p):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = content.replace(en_pill, pill)
    content = content.replace(en_h1, h1)
    content = content.replace(en_p, p)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_lang(ro_html, ro_pill, ro_h1, ro_p)
fix_lang(ru_html, ru_pill, ru_h1, ru_p)

print("Translations applied successfully!")
