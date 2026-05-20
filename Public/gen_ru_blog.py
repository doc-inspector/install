with open('en/blog.html', 'r', encoding='utf-8') as f:
    en = f.read()

import re

ru_cards = [
    ('how-to', '2026-05-09', 'kak-vosstanovityu-povrezhdyonney-pdf-fayl-za-neskolyuko-sekund.html',
     'Как Восстановить Повреждённый PDF-Файл за Несколько Секунд',
     'PDF не открывается? Узнайте, как исправить повреждённые PDF-файлы с помощью инструмента пакетного восстановления DocInspector. Работает полностью офлайн.'),
    ('security', '2026-05-10', 'skretee-dannee-v-vashih-dokumentah-i-pochemu-yato-vazhno.html',
     'Скрытые Данные в Ваших Документах (И Почему Это Важно)',
     'Ваши PDF и Word-файлы содержат скрытые метаданные, которые могут раскрыть личную информацию, историю правок и GPS-координаты.'),
    ('education', '2026-05-11', 'pdf-a-vs-obechney-pdf-kogda-ispolyuzovatyu-kazhdey-format.html',
     'PDF/A vs Обычный PDF — Когда Использовать Каждый Формат',
     'Не все PDF одинаковы. Узнайте разницу между PDF/A и стандартным PDF и когда использовать каждый формат.'),
    ('education', '2026-05-12', '5-veschey-kotoree-ve-ne-znali-o-pdf-faylah.html',
     '5 Вещей, Которые Вы Не Знали о PDF-Файлах',
     'PDF кажется простым, но скрывает удивительную сложность. Вот 5 фактов о PDF-файлах, которые большинство не знает.'),
    ('security', '2026-05-13', 'gdpr-i-metadannee-dokumentov-sootvetstvu-t-li-vashi-fayle.html',
     'GDPR и Метаданные Документов: Соответствуют ли Ваши Файлы?',
     'Метаданные документов могут содержать персональные данные, нарушающие GDPR. Узнайте, как проверить и очистить документы.'),
    ('how-to', '2026-05-14', 'kak-dobavityu-vod-nee-znaki-na-sotni-pdf-srazu.html',
     'Как Добавить Водяные Знаки на Сотни PDF Сразу',
     'Нужно добавить водяные знаки на целую папку с PDF? Узнайте, как пакетно обработать документы за секунды с DocInspector.'),
    ('industry', '2026-05-15', 'pochemu-kazhdoy-ridicheskoy-firme-nuzhen-instrument-inspektsii-dokumentov.html',
     'Почему Каждой Юридической Фирме Нужен Инструмент Инспекции Документов',
     'Юридические документы скрывают риски. Узнайте, почему инспекция документов необходима для юридических фирм.'),
    ('security', '2026-05-16', 'pochemu-delete-ne-udal-et-po-nasto-schemu-bezopasnoe-unichtozhenie-faylov.html',
     'Почему «Delete» Не Удаляет По-Настоящему — Безопасное Уничтожение Файлов',
     'Когда вы удаляете файл, он остаётся на диске. Узнайте, как работает безопасное уничтожение и почему это важно.'),
    ('how-to', '2026-05-17', 'generatsi-excel-otchyotov-dl-audita-dokumentov-polnoe-rukovodstvo.html',
     'Генерация Excel-Отчётов для Аудита Документов — Полное Руководство',
     'Узнайте, как DocInspector генерирует подробные Excel-отчёты для аудита папок с анализом метаданных каждого документа.'),
    ('security', '2026-05-18', 'pochemu-oflayn-obrabotka-dokumentov-vazhnee-chem-kogda-libo.html',
     'Почему Офлайн-Обработка Документов Важнее, Чем Когда-Либо',
     'Облачные инструменты удобны, но подвергают ваши документы риску. Вот почему офлайн-обработка — более разумный выбор.'),
    ('how-to', '2026-05-19', 'kak-szhatyu-pdf-do-formata-tolyuko-izobrazheniy-i-zachem.html',
     'Как Сжать PDF до Формата Только Изображений (И Зачем)',
     'Сжатие PDF до формата только изображений удаляет скрытый контент и обеспечивает WYSIWYG. Узнайте, когда и как это использовать.'),
    ('education', '2026-05-20', 'polney-cheklist-audita-dokumentov-na-2026-god.html',
     'Полный Чеклист Аудита Документов на 2026 Год',
     'Практический чеклист для аудита безопасности документов в вашей организации. Охватывает метаданные, контроль доступа и соответствие.'),
    ('how-to', '2026-05-21', '7-shagov-dl-zaschite-dokumentov-pered-otpravkoy.html',
     '7 Шагов для Защиты Документов Перед Отправкой',
     'Прежде чем отправить, убедитесь, что ваши документы не раскрывают конфиденциальную информацию. Вот 7 ключевых шагов.'),
    ('how-to', '2026-05-22', 'hvatit-obrabatevatyu-dokumente-po-odnomu-paketna-obrabotka-yakonomit-chase.html',
     'Хватит Обрабатывать Документы По Одному — Пакетная Обработка Экономит Часы',
     'Если вы всё ещё обрабатываете документы по отдельности, вы тратите часы каждую неделю. Узнайте, как пакетная обработка трансформирует рабочий процесс.'),
    ('how-to', '2026-05-23', 'kak-sdelatyu-otskanirovannee-pdf-dostupnemi-dl-poiska-s-ocr.html',
     'Как Сделать Отсканированные PDF Доступными для Поиска с OCR',
     'Отсканированные PDF — это просто изображения, в них нельзя искать или копировать текст. Узнайте, как OCR решает эту проблему.'),
    ('industry', '2026-05-24', 'luchshie-praktiki-komplektovani-dokazatelyustv-dl-ristov.html',
     'Лучшие Практики Комплектования Доказательств для Юристов',
     'Создание пакетов доказательств, готовых к суду, требует тщательной подготовки документов. Вот лучшие практики на 2026 год.'),
    ('education', '2026-05-25', 'chto-takoe-pdf-hardening-i-kogda-on-nuzhen.html',
     'Что Такое PDF Hardening и Когда Он Нужен?',
     'PDF hardening делает документы устойчивыми к изменениям и удаляет скрытые угрозы. Узнайте, что это значит и когда использовать.'),
    ('industry', '2026-05-26', 'sovete-po-upravleni-dokumentami-dl-buhgalterov-i-auditorov.html',
     'Советы по Управлению Документами для Бухгалтеров и Аудиторов',
     'Бухгалтеры работают с тысячами конфиденциальных финансовых документов. Вот как управлять ими безопасно и эффективно.'),
    ('education', '2026-05-27', 'docinspector-vs-onlayn-pdf-instrumente-v-chyom-raznitsa.html',
     'DocInspector vs Онлайн PDF-Инструменты — В Чём Разница?',
     'Зачем выбирать настольный инструмент вместо бесплатных онлайн-сервисов PDF? Вот честное сравнение.'),
    ('how-to', '2026-05-28', 'nastroyka-docinspector-na-windows-11-bestrey-start.html',
     'Настройка DocInspector на Windows 11 — Быстрый Старт',
     'Запустите DocInspector на Windows 11 менее чем за 2 минуты. Скачайте, установите и обработайте первый пакет.'),
]

cat_labels_ru = {
    'how-to': 'Как сделать',
    'security': 'Безопасность',
    'education': 'Образование',
    'industry': 'Индустрия',
}

cards_html_ru = '\n'.join([
    f'''  <div class="blog-card reveal" data-category="{cat}">
    <div class="blog-card-meta"><span class="blog-category" data-i18n="blog.cat.{cat}">{cat_labels_ru[cat]}</span><time datetime="{date}">{date}</time></div>
    <h3><a href="{slug}">{title}</a></h3>
    <p>{desc}</p>
    <a href="{slug}" class="blog-read-more" data-i18n="blog.readMore">Читать статью &rarr;</a>
  </div>'''
    for cat, date, slug, title, desc in ru_cards
])

ru = en
ru = ru.replace('lang="en"', 'lang="ru"')
ru = ru.replace('content="Tips, guides, and insights on document security, PDF repair, batch processing, and digital compliance from DocInspector."',
                'content="Советы, руководства и аналитика по безопасности документов, восстановлению PDF и пакетной обработке."')
ru = ru.replace('<span class="lang-pill">EN</span>', '<span class="lang-pill">RU</span>')
ru = ru.replace('class="lang-item active" data-lang="en"', 'class="lang-item" data-lang="en"')
ru = ru.replace('class="lang-item" data-lang="ru"', 'class="lang-item active" data-lang="ru"')
ru = ru.replace('placeholder="Search articles..."', 'placeholder="Поиск статей..."')
ru = ru.replace('No articles found matching your search.', 'Статьи не найдены.')
ru = ru.replace('<a href="price.html" data-i18n="nav.price">Price</a>', '<a href="tseny.html" data-i18n="nav.price">Цены</a>')
ru = ru.replace('<a href="user-guide.html" data-i18n="nav.guide">User Guide</a>', '<a href="rukovodstvo.html" data-i18n="nav.guide">Руководство</a>')
ru = ru.replace('<a href="reports.html" data-i18n="nav.reports">Reports &amp; Feedback</a>', '<a href="otchety.html" data-i18n="nav.reports">Отчёты &amp; Отзывы</a>')
ru = ru.replace('<a href="contact.html" data-i18n="nav.contact">Contact</a>', '<a href="kontakty.html" data-i18n="nav.contact">Контакты</a>')
ru = ru.replace('<a href="download.html" class="btn btn-primary btn-sm mobile-only" data-i18n="nav.download">Download</a>',
                '<a href="skachat.html" class="btn btn-primary btn-sm mobile-only" data-i18n="nav.download">Скачать</a>')
ru = ru.replace('<a href="download.html" class="btn btn-primary btn-sm desktop-only" data-i18n="nav.download">Download</a>',
                '<a href="skachat.html" class="btn btn-primary btn-sm desktop-only" data-i18n="nav.download">Скачать</a>')
ru = ru.replace('<a href="privacy.html" data-i18n="footer.privacy">Privacy Policy</a>',
                '<a href="konfidentsialnost.html" data-i18n="footer.privacy">Конфиденциальность</a>')
ru = ru.replace('<a href="terms.html" data-i18n="footer.terms">Terms of Service</a>',
                '<a href="usloviya.html" data-i18n="footer.terms">Условия</a>')
ru = ru.replace('<a href="refund.html" data-i18n="footer.refund">Refund Policy</a>',
                '<a href="vozvrat.html" data-i18n="footer.refund">Возврат</a>')

ru = re.sub(r'<div class="blog-grid" id="blogGrid">.*?</div>\s*\n\s*<div class="blog-no-results"',
            f'<div class="blog-grid" id="blogGrid">\n{cards_html_ru}\n</div>\n\n<div class="blog-no-results"',
            ru, flags=re.DOTALL)

with open('ru/blog.html', 'w', encoding='utf-8') as f:
    f.write(ru)
print('RU blog.html done with translated cards and correct slugs')
