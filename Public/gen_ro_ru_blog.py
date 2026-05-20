import shutil

with open('en/blog.html', 'r', encoding='utf-8') as f:
    en = f.read()

# ── RO ──
ro = en
ro = ro.replace('lang="en"', 'lang="ro"')
ro = ro.replace('content="Tips, guides, and insights on document security, PDF repair, batch processing, and digital compliance from DocInspector."',
                'content="Sfaturi, ghiduri si analize despre securitatea documentelor, repararea PDF-urilor si procesare in lot."')
ro = ro.replace('<span class="lang-pill">EN</span>', '<span class="lang-pill">RO</span>')
ro = ro.replace('class="lang-item active" data-lang="en"', 'class="lang-item" data-lang="en"')
ro = ro.replace('class="lang-item" data-lang="ro"', 'class="lang-item active" data-lang="ro"')
ro = ro.replace('placeholder="Search articles..."', 'placeholder="Cauta articole..."')
ro = ro.replace('No articles found matching your search.', 'Nu s-au gasit articole care sa corespunda cautarii.')
ro = ro.replace('<a href="price.html" data-i18n="nav.price">Price</a>', '<a href="preturi.html" data-i18n="nav.price">Preturi</a>')
ro = ro.replace('<a href="user-guide.html" data-i18n="nav.guide">User Guide</a>', '<a href="ghid-utilizare.html" data-i18n="nav.guide">Ghid</a>')
ro = ro.replace('<a href="reports.html" data-i18n="nav.reports">Reports &amp; Feedback</a>', '<a href="rapoarte.html" data-i18n="nav.reports">Rapoarte &amp; Feedback</a>')
ro = ro.replace('<a href="contact.html" data-i18n="nav.contact">Contact</a>', '<a href="contact.html" data-i18n="nav.contact">Contact</a>')
ro = ro.replace('<a href="download.html" class="btn btn-primary btn-sm mobile-only" data-i18n="nav.download">Download</a>',
                '<a href="descarcare.html" class="btn btn-primary btn-sm mobile-only" data-i18n="nav.download">Descarca</a>')
ro = ro.replace('<a href="download.html" class="btn btn-primary btn-sm desktop-only" data-i18n="nav.download">Download</a>',
                '<a href="descarcare.html" class="btn btn-primary btn-sm desktop-only" data-i18n="nav.download">Descarca</a>')
ro = ro.replace('<a href="privacy.html" data-i18n="footer.privacy">Privacy Policy</a>',
                '<a href="politica-de-confidentialitate.html" data-i18n="footer.privacy">Politica de Confidentialitate</a>')
ro = ro.replace('<a href="terms.html" data-i18n="footer.terms">Terms of Service</a>',
                '<a href="termeni.html" data-i18n="footer.terms">Termeni</a>')
ro = ro.replace('<a href="refund.html" data-i18n="footer.refund">Refund Policy</a>',
                '<a href="rambursare.html" data-i18n="footer.refund">Rambursare</a>')
with open('ro/blog.html', 'w', encoding='utf-8') as f:
    f.write(ro)
print('RO done')

# ── RU ──
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
with open('ru/blog.html', 'w', encoding='utf-8') as f:
    f.write(ru)
print('RU done')
