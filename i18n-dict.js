// i18n-dict.js
window.I18N = {
  EN: {
    // NAV
    "nav.home": "Home",
    "nav.price": "Price",
    "nav.guide": "User Guide",
    "nav.reports": "Reports & Feedback",
    "nav.contact": "Contact",



// CONTACT
"contact.pageTitle": "Contact – DocInspector",
"contact.title": "Contact & Support",
"contact.subtitle": "If you have questions about licensing, installation, performance issues or integration, use the form below or contact us directly by email.",
"contact.hpLabel": "Leave this empty",
"contact.labelName": "Your name",
"contact.labelEmail": "Email",
"contact.labelSubject": "Subject",
"contact.labelMessage": "Message",
"contact.phName": "John Doe",
"contact.phEmail": "you@company.com",
"contact.phMessage": "Describe your question or issue...",
"contact.btnSend": "Send message",
"contact.opt.general": "General question",
"contact.opt.install": "Installation issue",
"contact.opt.license": "License & activation",
"contact.opt.integration": "Integration & automation",
"contact.opt.support": "Technical support",
"contact.opt.other": "Other",
"contact.side.directTitle": "Direct support",
"contact.side.directText": "If your request is urgent or related to licensing / activation, contact us directly:",
"contact.side.hoursTitle": "Hours",
"contact.side.hoursDays": "Monday – Friday",
"contact.side.hoursTime": "09:00 – 18:00 (GMT+2)",
"contact.side.responseTitle": "Response time",
"contact.side.responseLine1": "Typical response time: ",
"contact.side.responseStrong": "2–12 hours",
"contact.side.responseLine2": "Max 24h during peak periods.",
"contact.side.beforeTitle": "Before contacting us",
"contact.side.before1": "Ensure you use the latest version of the application.",
"contact.side.before2": "Try reproducing the problem with a smaller test folder.",
"contact.side.before3": "Include any relevant log files or screenshots.",




    // BRAND
    "brand.subtitle": "Document Manager, Repair & Audit Suite",

    // HERO
    "hero.eyebrow": "Windows desktop utility",
    "hero.title1": "Protect, repair and audit your",
    "hero.title2": "evidence documents",
    "hero.title3": "with confidence.",
    "hero.lead":
      "DocInspector Pro rebuilds vulnerable PDFs, hardens evidence bundles, audits workstations and generates professional reports for legal, corporate and IT environments – while preserving your folder structure.",
    "hero.badge1": "Normalize and OCR PDFs at a controlled DPI to make them safer to share.",
    "hero.badge2": "Produce bundle summaries and Excel reports ready for court or audits.",
    "hero.badge3": "Scan folders or whole PCs to map and sanitize sensitive documents.",
    "btn.download": "Download trial",
    "btn.pricing": "View pricing",
    "hero.footnote": "No always-on agent. Runs on demand, produces exportable logs and reports.",
    "hero.screenshotLabel": "Click to preview the full GUI screens.",

    // MODULES
    "modules.title": "Core modules, grouped like in the app",
    "modules.subtitle":
      "Each module below matches the main groups in the GUI. Inside, every card represents one action the suite can run over your folders and evidence bundles.",

    // STATUS
    "status.planned": "Planned",

    // MODULE: PDF
    "module.pdf.title": "PDF Repair and Hardening",
    "module.pdf.tagline":
      "Clean, normalize and lock down risky documents before sending or archiving them.",
    "feature.rebuild.title": "Rebuild + OCR PDF",
    "feature.rebuild.desc":
      "Rasterizes each page at the chosen DPI, runs OCR, and rebuilds a clean, searchable PDF that is easier to archive and share.",
    "feature.flatten.title": "Flatten to Image-Only PDF",
    "feature.flatten.desc":
      "Converts each page into a bitmap image, stripping editable layers, comments and hidden objects, leaving only what you can literally see.",
    "feature.officepdf.title": "Office PDF Converter",
    "feature.officepdf.desc":
      "Batch-convert Word and Excel documents to PDFs using a controlled pipeline, preserving your folder structure.",
    "feature.watermark.title": "Add Watermark",
    "feature.watermark.desc":
      "Apply consistent text watermarks (for example “CONFIDENTIAL” or case IDs) across a full batch of PDFs in one go.",
    "feature.findremove.title": "Find and Remove",
    "feature.findremove.desc":
      "Scan PDFs for sensitive phrases or patterns and automatically clean or redact the detected content before disclosure.",

    // MODULE: REPORTING
    "module.reporting.title": "Reporting and Evidence",
    "module.reporting.tagline":
      "Build bundle overviews and detailed file inventories for case files or audits.",
    "feature.pdfsummary.title": "PDF Bundle Summary",
    "feature.pdfsummary.desc":
      "Scans PDFs in a folder tree and generates a simple “borderou” with file names, sizes and page counts.",
    "feature.advreport.title": "Advanced Bundle Report",
    "feature.advreport.desc":
      "Produces a richer Excel report including Word, Excel and other formats, with smarter page counting and more columns.",
    "feature.folderreport.title": "Folder Evidence Report",
    "feature.folderreport.desc":
      "Inventories every supported file in a folder structure so you can attach the report to legal or audit paperwork.",

    // MODULE: AUDIT
    "module.audit.title": "Audit and Security",
    "module.audit.tagline": "Discover, sanitize and track documents on a PC or evidence disk.",
    "feature.sanitize.title": "Sanitize Docs",
    "feature.sanitize.desc":
      "Clean metadata, comments and hidden content from supported document types in bulk, before sending them out.",
    "feature.auditpc.title": "Audit This PC",
    "feature.auditpc.desc":
      "Scan fixed drives and standard locations to identify and list documents that may contain sensitive information.",
    "feature.secdelete.title": "Secure Delete + Audit Trail",
    "feature.secdelete.desc":
      "Securely delete selected files while keeping a clear audit log of what was removed and when.",
    "feature.encryption.title": "Encryption",
    "feature.encryption.desc":
      "Package hardened bundles into encrypted containers or password-protected archives, ready to send externally.",

    // WORKFLOW
    "workflow.title": "From messy folders to hardened, traceable bundles.",
    "workflow.text":
      "DocInspector Pro is built for teams that live in PDFs, Word and Excel all day. Instead of cleaning each file manually, you process entire trees in one run and get hardened bundles plus reports.",
    "workflow.p1":
      "Drag a matter folder into the tool, pick modules and let the suite rebuild, flatten and sanitize.",
    "workflow.p2":
      "Generate Excel overviews that show every file, page count and hash – attach them directly to case files.",
    "workflow.p3":
      "Detect stray documents on workstations and pull them into controlled, logged evidence locations.",
    "workflow.p4":
      "Non-PDF files (audio, images, videos) stay with the bundle so context is never lost.",

    // BOTTOM CARDS
    "bottom.card1.title": "How DocInspector Pro keeps your folder structure",
    "bottom.card1.text":
      "Input and Output are separate – you always choose a clean output root. For each processed file, the original folder structure is re-created under the Output path. Non-PDF files (audio, images, archives, emails) can be copied as-is so you keep the bundle together.",
    "bottom.card2.title": "Typical result after one run",
    "bottom.card2.text":
      "A hardened bundle of PDFs and companion files sharing an identical folder structure, one or more Excel reports listing every item and page count, and log files that show what was processed, skipped or failed. Perfect for zipping, archiving or copying to an evidence drive.",

    // FOOTER
    "footer.copyright": "© 2025 Vladimir Tonu – All rights reserved",
    "footer.support": "Support",
    "footer.bug": "Report a bug"
  },

  RO: {
    // NAV
    "nav.home": "Acasă",
    "nav.price": "Preț",
    "nav.guide": "Ghid utilizare",
    "nav.reports": "Rapoarte & Feedback",
    "nav.contact": "Contact",




/* =========================
   CONTACT (RO)
   ========================= */
"contact.pageTitle": "Contact – DocInspector",
"contact.title": "Contact & Suport",
"contact.subtitle": "Dacă ai întrebări despre licențiere, instalare, probleme de performanță sau integrare, folosește formularul de mai jos sau contactează-ne direct prin email.",
"contact.hpLabel": "Lasă acest câmp gol",
"contact.labelName": "Numele tău",
"contact.labelEmail": "Email",
"contact.labelSubject": "Subiect",
"contact.labelMessage": "Mesaj",
"contact.phName": "Ion Popescu",
"contact.phEmail": "tu@companie.com",
"contact.phMessage": "Descrie întrebarea sau problema...",
"contact.btnSend": "Trimite mesajul",
"contact.opt.general": "Întrebare generală",
"contact.opt.install": "Problemă la instalare",
"contact.opt.license": "Licență & activare",
"contact.opt.integration": "Integrare & automatizare",
"contact.opt.support": "Suport tehnic",
"contact.opt.other": "Altceva",
"contact.side.directTitle": "Suport direct",
"contact.side.directText": "Dacă solicitarea este urgentă sau ține de licențiere / activare, contactează-ne direct:",
"contact.side.hoursTitle": "Program",
"contact.side.hoursDays": "Luni – Vineri",
"contact.side.hoursTime": "09:00 – 18:00 (GMT+2)",
"contact.side.responseTitle": "Timp de răspuns",
"contact.side.responseLine1": "Timp tipic de răspuns: ",
"contact.side.responseStrong": "2–12 ore",
"contact.side.responseLine2": "Maxim 24h în perioade aglomerate.",
"contact.side.beforeTitle": "Înainte să ne contactezi",
"contact.side.before1": "Asigură-te că folosești cea mai recentă versiune a aplicației.",
"contact.side.before2": "Încearcă să reproduci problema cu un folder de test mai mic.",
"contact.side.before3": "Include orice log-uri relevante sau capturi de ecran.",


    // BRAND
    "brand.subtitle": "Manager documente, reparare & audit",

    // HERO
    "hero.eyebrow": "Utilitar desktop pentru Windows",
    "hero.title1": "Protejează, repară și auditează",
    "hero.title2": "documentele de probă",
    "hero.title3": "cu încredere.",
    "hero.lead":
      "DocInspector Pro reconstruiește PDF-uri vulnerabile, întărește pachete de evidență, auditează stații de lucru și generează rapoarte profesionale pentru medii juridice, corporate și IT – păstrând structura folderelor.",
    "hero.badge1": "Normalizează și rulează OCR pe PDF-uri la un DPI controlat pentru a le face mai sigure la partajare.",
    "hero.badge2": "Generează rezumate de pachete și rapoarte Excel pregătite pentru instanță sau audit.",
    "hero.badge3": "Scanează foldere sau PC-uri întregi pentru a cartografia și igieniza documente sensibile.",
    "btn.download": "Descarcă trial",
    "btn.pricing": "Vezi prețurile",
    "hero.footnote": "Fără agent permanent. Rulează la cerere și produce loguri/rapoarte exportabile.",
    "hero.screenshotLabel": "Click pentru a vedea toate ecranele GUI.",

    // MODULES
    "modules.title": "Modulele de bază, grupate ca în aplicație",
    "modules.subtitle":
      "Fiecare modul de mai jos corespunde grupurilor principale din GUI. În interior, fiecare card reprezintă o acțiune pe care suita o poate rula pe folderele și pachetele tale de evidență.",

    // STATUS
    "status.planned": "Planificat",

    // MODULE: PDF
    "module.pdf.title": "Reparare și întărire PDF",
    "module.pdf.tagline": "Curăță, normalizează și blochează documentele riscante înainte de trimitere sau arhivare.",
    "feature.rebuild.title": "Rebuild + OCR PDF",
    "feature.rebuild.desc":
      "Rasterizează fiecare pagină la DPI-ul ales, rulează OCR și reconstruiește un PDF curat, căutabil, mai ușor de arhivat și partajat.",
    "feature.flatten.title": "Flatten în PDF doar-imagine",
    "feature.flatten.desc":
      "Transformă fiecare pagină într-o imagine bitmap, eliminând straturi editabile, comentarii și obiecte ascunse, lăsând doar ce se vede.",
    "feature.officepdf.title": "Convertor Office → PDF",
    "feature.officepdf.desc":
      "Convertește în batch documente Word și Excel în PDF-uri printr-un flux controlat, păstrând structura folderelor.",
    "feature.watermark.title": "Adaugă watermark",
    "feature.watermark.desc":
      "Aplică watermark text (de ex. „CONFIDENȚIAL” sau ID caz) pe un lot întreg de PDF-uri dintr-o singură rulare.",
    "feature.findremove.title": "Caută și elimină",
    "feature.findremove.desc":
      "Scanează PDF-uri după fraze/pattern-uri sensibile și curăță/redactează automat conținutul detectat înainte de divulgare.",

    // MODULE: REPORTING
    "module.reporting.title": "Raportare și evidență",
    "module.reporting.tagline": "Construiește overviews și inventare detaliate pentru dosare sau audituri.",
    "feature.pdfsummary.title": "Rezumat pachet PDF",
    "feature.pdfsummary.desc":
      "Scanează PDF-urile dintr-un arbore de foldere și generează un „borderou” simplu cu nume fișiere, dimensiuni și număr de pagini.",
    "feature.advreport.title": "Raport avansat pachet",
    "feature.advreport.desc":
      "Generează un raport Excel mai bogat incluzând Word, Excel și alte formate, cu numărare mai inteligentă a paginilor și mai multe coloane.",
    "feature.folderreport.title": "Raport evidență folder",
    "feature.folderreport.desc":
      "Inventariază toate fișierele suportate dintr-o structură de foldere pentru a atașa raportul la documente juridice sau de audit.",

    // MODULE: AUDIT
    "module.audit.title": "Audit și securitate",
    "module.audit.tagline": "Descoperă, igienizează și urmărește documentele de pe un PC sau disk de evidență.",
    "feature.sanitize.title": "Igienizează documente",
    "feature.sanitize.desc":
      "Curăță metadate, comentarii și conținut ascuns din tipurile suportate, în batch, înainte de trimitere.",
    "feature.auditpc.title": "Audit acest PC",
    "feature.auditpc.desc":
      "Scanează discuri fixe și locații standard pentru a identifica și lista documente ce pot conține informații sensibile.",
    "feature.secdelete.title": "Ștergere sigură + jurnal",
    "feature.secdelete.desc":
      "Șterge sigur fișiere selectate păstrând un jurnal clar cu ce s-a eliminat și când.",
    "feature.encryption.title": "Criptare",
    "feature.encryption.desc":
      "Împachetează bundle-urile întărite în containere criptate sau arhive cu parolă, gata de trimis extern.",

    // WORKFLOW
    "workflow.title": "De la foldere haotice la bundle-uri întărite și trasabile.",
    "workflow.text":
      "DocInspector Pro este construit pentru echipe care lucrează zilnic cu PDF, Word și Excel. În loc să cureți manual fiecare fișier, procesezi arbori întregi dintr-o singură rulare și obții bundle-uri întărite plus rapoarte.",
    "workflow.p1": "Trage un folder de caz în tool, alege modulele și lasă suita să reconstruiască, să „flatten”-eze și să igienizeze.",
    "workflow.p2": "Generează rapoarte Excel cu fiecare fișier, număr de pagini și hash – atașabile direct la dosare.",
    "workflow.p3": "Detectează documente rătăcite pe stații și mută-le în locații de evidență controlate, cu log.",
    "workflow.p4": "Fișierele non-PDF (audio, imagini, video) rămân în bundle ca să nu pierzi contextul.",

    // BOTTOM CARDS
    "bottom.card1.title": "Cum păstrează DocInspector Pro structura folderelor",
    "bottom.card1.text":
      "Input și Output sunt separate – alegi mereu un output curat. Pentru fiecare fișier procesat, structura originală se recreează sub Output. Fișierele non-PDF (audio, imagini, arhive, emailuri) pot fi copiate ca atare ca să păstrezi bundle-ul complet.",
    "bottom.card2.title": "Rezultatul tipic după o rulare",
    "bottom.card2.text":
      "Un bundle întărit de PDF-uri și fișiere asociate cu structură identică, unul sau mai multe rapoarte Excel cu fiecare element și număr de pagini, plus loguri cu ce a fost procesat, sărit sau eșuat. Perfect pentru arhivare, zip sau copiere pe un disk de evidență.",

    // FOOTER
    "footer.copyright": "© 2025 Vladimir Tonu – Toate drepturile rezervate",
    "footer.support": "Suport",
    "footer.bug": "Raportează un bug"
  },

  RU: {
    // NAV
    "nav.home": "Главная",
    "nav.price": "Цена",
    "nav.guide": "Руководство",
    "nav.reports": "Отчёты и отзывы",
    "nav.contact": "Контакты",



/* =========================
   CONTACT (RU)
   ========================= */
"contact.pageTitle": "Контакты – DocInspector",
"contact.title": "Контакты и поддержка",
"contact.subtitle": "Если у вас есть вопросы по лицензированию, установке, производительности или интеграции, используйте форму ниже или свяжитесь с нами напрямую по email.",
"contact.hpLabel": "Оставьте это поле пустым",
"contact.labelName": "Ваше имя",
"contact.labelEmail": "Email",
"contact.labelSubject": "Тема",
"contact.labelMessage": "Сообщение",
"contact.phName": "Иван Иванов",
"contact.phEmail": "you@company.com",
"contact.phMessage": "Опишите ваш вопрос или проблему...",
"contact.btnSend": "Отправить сообщение",
"contact.opt.general": "Общий вопрос",
"contact.opt.install": "Проблема установки",
"contact.opt.license": "Лицензия и активация",
"contact.opt.integration": "Интеграция и автоматизация",
"contact.opt.support": "Техническая поддержка",
"contact.opt.other": "Другое",
"contact.side.directTitle": "Прямая поддержка",
"contact.side.directText": "Если запрос срочный или связан с лицензией / активацией, свяжитесь с нами напрямую:",
"contact.side.hoursTitle": "Часы работы",
"contact.side.hoursDays": "Понедельник – Пятница",
"contact.side.hoursTime": "09:00 – 18:00 (GMT+2)",
"contact.side.responseTitle": "Время ответа",
"contact.side.responseLine1": "Обычно отвечаем за: ",
"contact.side.responseStrong": "2–12 часов",
"contact.side.responseLine2": "До 24 часов в периоды высокой нагрузки.",
"contact.side.beforeTitle": "Перед обращением",
"contact.side.before1": "Убедитесь, что используете последнюю версию приложения.",
"contact.side.before2": "Попробуйте воспроизвести проблему на меньшей тестовой папке.",
"contact.side.before3": "Приложите релевантные логи или скриншоты.",



    // BRAND
    "brand.subtitle": "Менеджер документов, восстановление и аудит",

    // HERO
    "hero.eyebrow": "Десктоп-утилита для Windows",
    "hero.title1": "Защищайте, восстанавливайте и проверяйте",
    "hero.title2": "документы-доказательства",
    "hero.title3": "уверенно.",
    "hero.lead":
      "DocInspector Pro восстанавливает уязвимые PDF, укрепляет наборы доказательств, проверяет рабочие станции и создаёт профессиональные отчёты для юридических, корпоративных и IT-сред — сохраняя структуру папок.",
    "hero.badge1": "Нормализует и выполняет OCR для PDF с контролируемым DPI, чтобы безопаснее делиться файлами.",
    "hero.badge2": "Создаёт сводки наборов и отчёты Excel, готовые для суда или аудита.",
    "hero.badge3": "Сканирует папки или целые ПК для поиска и очистки чувствительных документов.",
    "btn.download": "Скачать trial",
    "btn.pricing": "Посмотреть цены",
    "hero.footnote": "Без постоянного агента. Запуск по требованию, экспортируемые логи и отчёты.",
    "hero.screenshotLabel": "Нажмите, чтобы посмотреть все экраны GUI.",

    // MODULES
    "modules.title": "Основные модули, сгруппированные как в приложении",
    "modules.subtitle":
      "Каждый модуль ниже соответствует основным группам в GUI. Внутри каждая карточка — это отдельное действие, которое пакет может выполнить над папками и наборами доказательств.",

    // STATUS
    "status.planned": "Планируется",

    // MODULE: PDF
    "module.pdf.title": "Восстановление и усиление PDF",
    "module.pdf.tagline": "Очистка, нормализация и блокировка рискованных документов перед отправкой или архивированием.",
    "feature.rebuild.title": "Rebuild + OCR PDF",
    "feature.rebuild.desc":
      "Растеризует каждую страницу с выбранным DPI, выполняет OCR и пересобирает чистый, поисковый PDF, удобный для архивации и обмена.",
    "feature.flatten.title": "Flatten в PDF только-изображение",
    "feature.flatten.desc":
      "Преобразует каждую страницу в bitmap, удаляя редактируемые слои, комментарии и скрытые объекты, оставляя только видимое.",
    "feature.officepdf.title": "Конвертер Office → PDF",
    "feature.officepdf.desc":
      "Пакетно конвертирует Word/Excel в PDF через контролируемый конвейер, сохраняя структуру папок.",
    "feature.watermark.title": "Добавить watermark",
    "feature.watermark.desc":
      "Применяет текстовые водяные знаки (например «CONFIDENTIAL» или ID дела) к партии PDF за один запуск.",
    "feature.findremove.title": "Найти и удалить",
    "feature.findremove.desc":
      "Сканирует PDF на чувствительные фразы/шаблоны и автоматически очищает/редактирует найденное перед раскрытием.",

    // MODULE: REPORTING
    "module.reporting.title": "Отчёты и доказательства",
    "module.reporting.tagline": "Сводки наборов и детальные инвентаризации файлов для дел или аудита.",
    "feature.pdfsummary.title": "Сводка PDF-набора",
    "feature.pdfsummary.desc":
      "Сканирует PDF в дереве папок и создаёт простой «borderou» с именами, размерами и количеством страниц.",
    "feature.advreport.title": "Расширенный отчёт по набору",
    "feature.advreport.desc":
      "Создаёт более богатый Excel-отчёт включая Word/Excel и другие форматы, с умным подсчётом страниц и доп. колонками.",
    "feature.folderreport.title": "Отчёт по папке доказательств",
    "feature.folderreport.desc":
      "Инвентаризирует все поддерживаемые файлы в структуре папок для прикрепления к юридическим/аудит документам.",

    // MODULE: AUDIT
    "module.audit.title": "Аудит и безопасность",
    "module.audit.tagline": "Поиск, очистка и отслеживание документов на ПК или диске доказательств.",
    "feature.sanitize.title": "Очистка документов",
    "feature.sanitize.desc":
      "Удаляет метаданные, комментарии и скрытое содержимое из поддерживаемых типов документов пакетно, перед отправкой.",
    "feature.auditpc.title": "Аудит этого ПК",
    "feature.auditpc.desc":
      "Сканирует диски и стандартные локации, чтобы выявить и перечислить документы с потенциально чувствительными данными.",
    "feature.secdelete.title": "Безопасное удаление + журнал",
    "feature.secdelete.desc":
      "Безопасно удаляет выбранные файлы, сохраняя понятный аудит-лог что удалено и когда.",
    "feature.encryption.title": "Шифрование",
    "feature.encryption.desc":
      "Упаковывает усиленные наборы в зашифрованные контейнеры или архивы с паролем, готовые к внешней отправке.",

    // WORKFLOW
    "workflow.title": "От хаоса в папках — к усиленным и отслеживаемым наборам.",
    "workflow.text":
      "DocInspector Pro создан для команд, которые ежедневно работают с PDF, Word и Excel. Вместо ручной очистки каждого файла вы обрабатываете целые деревья за один запуск и получаете усиленные наборы и отчёты.",
    "workflow.p1": "Перетащите папку дела, выберите модули и запустите пересборку, flatten и очистку.",
    "workflow.p2": "Создайте Excel-обзор с каждым файлом, количеством страниц и хэшем — и приложите к делу.",
    "workflow.p3": "Обнаруживайте «лишние» документы на рабочих станциях и переносите их в контролируемые локации с логом.",
    "workflow.p4": "Файлы не-PDF (аудио, изображения, видео) остаются в наборе — контекст не теряется.",

    // BOTTOM CARDS
    "bottom.card1.title": "Как DocInspector Pro сохраняет структуру папок",
    "bottom.card1.text":
      "Input и Output разделены — вы всегда выбираете чистый Output. Для каждого обработанного файла исходная структура папок пересоздаётся в Output. Файлы не-PDF (аудио, изображения, архивы, письма) можно копировать как есть, чтобы набор оставался целым.",
    "bottom.card2.title": "Типичный результат после одного запуска",
    "bottom.card2.text":
      "Усиленный набор PDF и сопутствующих файлов с идентичной структурой, один или несколько Excel-отчётов со всеми элементами и количеством страниц, и логи с тем, что обработано/пропущено/ошиблось. Идеально для zip/архивации/копирования на диск доказательств.",

    // FOOTER
    "footer.copyright": "© 2025 Vladimir Tonu — Все права защищены",
    "footer.support": "Поддержка",
    "footer.bug": "Сообщить об ошибке"
  }
};
