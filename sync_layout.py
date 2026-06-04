import os
import re

en_html = r"E:\Website online and local app new project\Public2\Public\en\tools-online.html"
ro_html = r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html"
ru_html = r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"

with open(en_html, 'r', encoding='utf-8') as f:
    en_content = f.read()

with open(ro_html, 'r', encoding='utf-8') as f:
    ro_content = f.read()

with open(ru_html, 'r', encoding='utf-8') as f:
    ru_content = f.read()

hero_pattern = re.compile(r'(<section class="tools-hero"[^>]*>.*?</section>)', re.DOTALL)
en_hero = hero_pattern.search(en_content).group(1)

script_pattern = re.compile(r'(<script>\s*let selectedOps.*?</script>)', re.DOTALL)
en_scripts = script_pattern.search(en_content)
if en_scripts:
    en_script_content = en_scripts.group(0)
else:
    en_script_content = ""

def apply_translations(html, lang):
    if lang == 'ro':
        translations = {
            "FREE ONLINE DOCUMENT TOOLS — NO DOWNLOAD REQUIRED": "UNELTE ONLINE GRATUITE PENTRU PDF — FĂRĂ INSTALARE",
            "Process Documents<br>Directly in<br>Your Browser": "Procesează PDF-uri Direct<br>în Browserul Tău",
            "Sanitize metadata, add watermarks, encrypt, redact or repair your documents online — <strong>isolated sandbox</strong> and deleted immediately after download. No account needed.": "Sanitizează metadate, adaugă watermark, criptează, redactează sau repară documente PDF online — complet gratuit. Fișierele sunt procesate într-un <strong>sandbox izolat</strong> și șterse imediat după descărcare. Nu este necesar un cont.",
            "STEP 1": "PASUL 1",
            "Upload Your Files": "Încarcă Fișierele Tale",
            "Drag & drop or click to select — up to <strong>100 files</strong> at once (max <strong>15 MB</strong> each), 100 free per day.": "Trage & plasează sau fă clic pentru a selecta — până la <strong>100 de fișiere</strong> simultan (max <strong>15 MB</strong> fiecare), 100 gratuit pe zi.",
            "Drag & Drop PDF files here": "Trage & Plasează fișierele PDF aici",
            "or click to browse — max 100 files per day — 15 MB each": "sau fă clic pentru a căuta — max 100 fișiere pe zi — 15 MB fiecare",
            "Select Folder": "Selectează Folder",
            "Select Files": "Selectează Fișiere",
            "STEP 2": "PASUL 2",
            "Select Operations": "Selectează Operațiunile",
            "Choose one or more tools — they run in sequence on your files.": "Alege unul sau mai multe instrumente — ele vor rula pe rând.",
            "License & Limits": "Licență & Limite",
            "Current Tier:": "Nivel curent:",
            "Daily Usage": "Utilizare zilnică",
            "Enter DocInspector License Key...": "Introdu cheia DocInspector...",
            "Activate Key": "Activează Cheia",
            "Remove License": "Elimină Licența",
            "Selected Operations": "Operațiuni Selectate",
            "No operations selected yet.<br>Pick tools from the left.": "Nicio operațiune selectată încă.<br>Alege instrumente din stânga.",
            "Processing pipeline": "Traseu de procesare",
            "Input PDF Files": "Fișiere PDF de Intrare",
            "Uploaded & ready": "Încărcate și gata",
            "Pipeline active stage": "Stadiu activ pipeline",
            "Ready for Download": "Gata pentru Descărcare",
            "Processed output package": "Pachet procesat finalizat",
            "Process Files Now": "Procesează Fișierele Acum",
            "Processing your files": "Se procesează fișierele",
            "This may take a few seconds": "Acest lucru poate dura câteva secunde",
            "Download Results (.zip)": "Descarcă Rezultatele (.zip)",
            "Processing Complete!": "Procesare Completă!",
            "processed successfully": "procesate cu succes",
            "Zero retention": "Zero stocare",
            "files deleted immediately after you download": "fișiere șterse imediat după descărcare",
            "CLI-powered": "Bazat pe CLI",
            "same engines as the desktop app": "aceleași motoare ca și aplicația desktop",
            "Online: PDF focus": "Online: focus pe PDF",
            "Desktop app supports DOCX, XLSX & more": "Aplicația desktop suportă DOCX, XLSX și mai mult",
            "Need unlimited batch processing?": "Ai nevoie de procesare nelimitată?",
            "Download the desktop app for Windows — process thousands of files locally with no limits.": "Descarcă aplicația desktop pentru Windows — procesează mii de fișiere local fără limite.",
            "Download Desktop App": "Descarcă Aplicația Desktop",
            
            "Sanitize Metadata": "Sanitizare Metadate",
            "Remove author name, creation date, software fingerprints, GPS data and all hidden metadata from your PDF. Essential before sharing documents externally.": "Elimină numele autorului, data creării, amprentele software, datele GPS și toate metadatele ascunse din PDF. Esențial înainte de a partaja documente extern.",
            
            "Add Watermark": "Adaugă Watermark",
            "Stamp a diagonal text watermark (e.g. CONFIDENTIAL, DRAFT) onto every page of your PDF with custom text, font, size and opacity.": "Aplică un watermark text diagonal (ex: CONFIDENȚIAL, DRAFT) pe fiecare pagină a PDF-ului cu opacitate și dimensiune font personalizabile.",
            
            "Encrypt PDF": "Cripteaz&abreve; PDF",
            "Password-protect your PDF with 256-bit AES encryption. Only recipients with the correct password can open the document.": "Protejează PDF-ul cu parolă prin criptare AES 256-bit. Doar destinatarii cu parola corectă pot deschide documentul.",
            
            "Find & Redact": "Găsește & Redactează",
            "Permanently remove sensitive text from a PDF by converting it to a secure image-only version with no selectable text layer.": "Elimină permanent textul sensibil dintr-un PDF prin convertirea lui într-o versiune securizată doar imagine, fără un strat de text selectabil.",
            
            "Flatten to Image PDF": "Aplatizare în PDF-Imagine",
            "Convert every page into a raster image inside a PDF. Removes all embedded text, fonts, scripts and active form fields.": "Convertește fiecare pagină într-o imagine raster în interiorul PDF-ului. Elimină tot textul încorporat, fonturile, scripturile și câmpurile active de formular.",
            
            "Rebuild & Repair PDF": "Reconstruiește & Repar&abreve; PDF",
            "Fix corrupted, broken or malformed PDF structures. Linearizes and re-encodes the document for maximum compatibility.": "Repară structuri PDF corupte, defecte sau malformate. Linearizează și re-codifică documentul pentru compatibilitate maximă.",
            
            "PDF Bundle Summary": "Borderou PDF",
            "Drag a folder with up to 100 PDF files (max 15 MB each). Generates a professional <strong style=\"color:#f59e0b\">Excel + PDF report</strong> with file name, page count, SHA-256 hash, encryption status, and totals.": "Trage un folder cu până la 100 de fișiere PDF (max 15 MB fiecare). Generează un <strong style=\"color:#f59e0b\">raport profesional Excel + PDF</strong> cu numele fișierului, numărul de pagini, hash-ul SHA-256, starea criptării și totalurile.",
            "Folder upload": "Încărcare folder",
            
            "Type a keyword and click Add (or comma-separated list)...": "Tastează un cuvânt cheie și apasă Adaugă...",
            "Add": "Adaugă",
            "No keywords added yet. Search matches exact phrases.": "Niciun cuvânt cheie adăugat. Căutarea este exactă.",
            "The entire page text layer is removed to guarantee no sensitive content remains (image-only output).": "Întregul strat de text al paginii este eliminat pentru a garanta că nu rămâne conținut sensibil (doar imagine).",
            
            "Watermark Text": "Text Watermark",
            "Text Size (px)": "Dimensiune Text (px)",
            "Opacity (0.1 - 1)": "Opacitate (0.1 - 1)",
            
            "Permissions Password (Owner)": "Parolă Permisiuni (Proprietar)",
            "Confirm Password": "Confirmă Parola"
        }
    else: # ru
        translations = {
            "FREE ONLINE DOCUMENT TOOLS — NO DOWNLOAD REQUIRED": "БЕСПЛАТНЫЕ ОНЛАЙН ИНСТРУМЕНТЫ — БЕЗ УСТАНОВКИ",
            "Process Documents<br>Directly in<br>Your Browser": "Обрабатывайте PDF<br>Прямо в Браузере",
            "Sanitize metadata, add watermarks, encrypt, redact or repair your documents online — <strong>isolated sandbox</strong> and deleted immediately after download. No account needed.": "Очистка метаданных, добавление водяных знаков, шифрование, удаление данных или ремонт PDF документов онлайн. Файлы обрабатываются в <strong>изолированной песочнице</strong> и удаляются сразу после скачивания.",
            "STEP 1": "ШАГ 1",
            "Upload Your Files": "Загрузите Ваши Файлы",
            "Drag & drop or click to select — up to <strong>100 files</strong> at once (max <strong>15 MB</strong> each), 100 free per day.": "Перетащите или нажмите, чтобы выбрать — до <strong>100 файлов</strong> одновременно (макс. <strong>15 МБ</strong> каждый), 100 бесплатно в день.",
            "Drag & Drop PDF files here": "Перетащите PDF файлы сюда",
            "or click to browse — max 100 files per day — 15 MB each": "или нажмите для обзора — макс 100 файлов в день — 15 МБ каждый",
            "Select Folder": "Выбрать папку",
            "Select Files": "Выбрать файлы",
            "STEP 2": "ШАГ 2",
            "Select Operations": "Выберите операции",
            "Choose one or more tools — they run in sequence on your files.": "Выберите один или несколько инструментов — они будут применяться по очереди.",
            "License & Limits": "Лицензия и Лимиты",
            "Current Tier:": "Текущий уровень:",
            "Daily Usage": "Дневное использование",
            "Enter DocInspector License Key...": "Введите ключ DocInspector...",
            "Activate Key": "Активировать ключ",
            "Remove License": "Удалить лицензию",
            "Selected Operations": "Выбранные операции",
            "No operations selected yet.<br>Pick tools from the left.": "Пока не выбраны операции.<br>Выберите инструменты слева.",
            "Processing pipeline": "Конвейер обработки",
            "Input PDF Files": "Входные PDF файлы",
            "Uploaded & ready": "Загружено и готово",
            "Pipeline active stage": "Активный этап конвейера",
            "Ready for Download": "Готово к скачиванию",
            "Processed output package": "Обработанный пакет файлов",
            "Process Files Now": "Обработать Файлы Сейчас",
            "Processing your files": "Обработка ваших файлов",
            "This may take a few seconds": "Это может занять несколько секунд",
            "Download Results (.zip)": "Скачать Результаты (.zip)",
            "Processing Complete!": "Обработка завершена!",
            "processed successfully": "успешно обработано",
            "Zero retention": "Нулевое удержание",
            "files deleted immediately after you download": "файлы удаляются сразу после скачивания",
            "CLI-powered": "На базе CLI",
            "same engines as the desktop app": "те же движки, что и в десктопном приложении",
            "Online: PDF focus": "Онлайн: фокус на PDF",
            "Desktop app supports DOCX, XLSX & more": "Десктопное приложение поддерживает DOCX, XLSX и др.",
            "Need unlimited batch processing?": "Нужна безлимитная пакетная обработка?",
            "Download the desktop app for Windows — process thousands of files locally with no limits.": "Скачайте десктопное приложение для Windows — обрабатывайте тысячи файлов локально без ограничений.",
            "Download Desktop App": "Скачать Десктопное Приложение",
            
            "Sanitize Metadata": "Очистка Метаданных",
            "Remove author name, creation date, software fingerprints, GPS data and all hidden metadata from your PDF. Essential before sharing documents externally.": "Удаляет имя автора, дату создания, отпечатки ПО, данные GPS и все скрытые метаданные из вашего PDF. Необходимо перед внешней отправкой.",
            
            "Add Watermark": "Добавить Водяной Знак",
            "Stamp a diagonal text watermark (e.g. CONFIDENTIAL, DRAFT) onto every page of your PDF with custom text, font, size and opacity.": "Наносит диагональный текстовый водяной знак (например, КОНФИДЕНЦИАЛЬНО, ПРОЕКТ) на каждую страницу PDF.",
            
            "Encrypt PDF": "Зашифровать PDF",
            "Password-protect your PDF with 256-bit AES encryption. Only recipients with the correct password can open the document.": "Защищает PDF паролем с помощью 256-битного шифрования AES. Только получатели с правильным паролем смогут открыть документ.",
            
            "Find & Redact": "Найти и Удалить Данные",
            "Permanently remove sensitive text from a PDF by converting it to a secure image-only version with no selectable text layer.": "Навсегда удаляет конфиденциальный текст из PDF, преобразуя его в безопасную версию только-изображение.",
            
            "Flatten to Image PDF": "Преобразовать в Изображение",
            "Convert every page into a raster image inside a PDF. Removes all embedded text, fonts, scripts and active form fields.": "Преобразует каждую страницу в растровое изображение внутри PDF. Удаляет встроенный текст, шрифты, скрипты.",
            
            "Rebuild & Repair PDF": "Восстановить и Исправить PDF",
            "Fix corrupted, broken or malformed PDF structures. Linearizes and re-encodes the document for maximum compatibility.": "Исправляет поврежденные или неправильные структуры PDF. Оптимизирует и перекодирует документ.",
            
            "PDF Bundle Summary": "Отчет по Пакету PDF",
            "Drag a folder with up to 100 PDF files (max 15 MB each). Generates a professional <strong style=\"color:#f59e0b\">Excel + PDF report</strong> with file name, page count, SHA-256 hash, encryption status, and totals.": "Перетащите папку до 100 файлов PDF (макс 15 МБ каждый). Генерирует <strong style=\"color:#f59e0b\">профессиональный отчет Excel + PDF</strong> с хешами SHA-256.",
            "Folder upload": "Загрузка папки",
            
            "Type a keyword and click Add (or comma-separated list)...": "Введите ключевое слово и нажмите Добавить...",
            "Add": "Добавить",
            "No keywords added yet. Search matches exact phrases.": "Ключевые слова пока не добавлены.",
            "The entire page text layer is removed to guarantee no sensitive content remains (image-only output).": "Весь текстовый слой страницы удаляется, чтобы гарантировать отсутствие конфиденциального контента (вывод только в виде изображения).",
            
            "Watermark Text": "Текст водяного знака",
            "Text Size (px)": "Размер текста (px)",
            "Opacity (0.1 - 1)": "Непрозрачность (0.1 - 1)",
            
            "Permissions Password (Owner)": "Пароль прав доступа",
            "Confirm Password": "Подтвердите пароль"
        }
        
    for en_text, tl_text in translations.items():
        html = html.replace(en_text, tl_text)
        
    html = html.replace("emoji: '&#x1F910;' },", "emoji: '&#x1F910;' },\n")
    return html

def patch_file(orig_content, lang):
    orig_hero_pattern = re.compile(r'(<section class="tools-hero"[^>]*>.*?</section>)', re.DOTALL)
    new_hero = apply_translations(en_hero, lang)
    if orig_hero_pattern.search(orig_content):
        content = orig_hero_pattern.sub(new_hero.replace('\\', '\\\\'), orig_content)
    else:
        # fallback if not found, just replace something known
        print(f"Could not find tools-hero in {lang}")
        content = orig_content
    
    if en_script_content:
        new_script = apply_translations(en_script_content, lang)
        orig_script_pattern = re.compile(r'(<script>\s*let selectedOps.*?</script>)', re.DOTALL)
        if orig_script_pattern.search(content):
            content = orig_script_pattern.sub(new_script.replace('\\', '\\\\'), content)
            
    content = content.replace("Cripteaz&abreve;", "Criptează")
    content = content.replace("Repar&abreve;", "Repară")
    
    return content

ro_new = patch_file(ro_content, 'ro')
ru_new = patch_file(ru_content, 'ru')

with open(ro_html, 'w', encoding='utf-8') as f:
    f.write(ro_new)

with open(ru_html, 'w', encoding='utf-8') as f:
    f.write(ru_new)

print("Synchronized layout and logic to RO and RU!")
