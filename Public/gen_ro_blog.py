with open('en/blog.html', 'r', encoding='utf-8') as f:
    en = f.read()

# ── RO: slug map EN→RO ──
slug_map = {
    'blog/how-to-repair-corrupted-pdf.html': 'blog/cum-sa-repari-un-fisier-pdf-corupt-in-cateva-secunde.html',
    'blog/hidden-metadata-in-your-documents.html': 'blog/datele-ascunse-din-documentele-tale-si-de-ce-conteaza.html',
    'blog/pdf-a-vs-regular-pdf.html': 'blog/pdf-a-vs-pdf-obisnuit-cand-sa-folosesti-fiecare-format.html',
    'blog/5-things-you-didnt-know-about-pdfs.html': 'blog/5-lucruri-pe-care-nu-le-stiai-despre-fisierele-pdf.html',
    'blog/gdpr-document-compliance.html': 'blog/gdpr-si-metadata-documentelor-sunt-fisierele-tale-conforme.html',
    'blog/batch-watermark-pdfs.html': 'blog/cum-sa-adaugi-watermark-pe-sute-de-pdf-uri-simultan.html',
    'blog/document-security-for-lawyers.html': 'blog/de-ce-fiecare-firma-de-avocatura-are-nevoie-de-un-tool-de-inspectie-documente.html',
    'blog/secure-file-shredding-explained.html': 'blog/de-ce-delete-nu-sterge-cu-adevarat-explicatia-shredding-ului-securizat.html',
    'blog/excel-reports-for-document-audits.html': 'blog/generarea-rapoartelor-excel-pentru-audituri-de-documente-ghid-complet.html',
    'blog/why-offline-document-processing.html': 'blog/de-ce-procesarea-offline-a-documentelor-conteaza-mai-mult-ca-niciodata.html',
    'blog/flatten-pdf-to-image.html': 'blog/cum-sa-aplatizezi-un-pdf-la-format-doar-imagini-si-de-ce-ai-vrea.html',
    'blog/document-audit-checklist.html': 'blog/checklist-complet-pentru-auditul-documentelor-in-2026.html',
    'blog/protect-documents-before-sharing.html': 'blog/7-pasi-pentru-protejarea-documentelor-inainte-de-partajare.html',
    'blog/batch-processing-saves-hours.html': 'blog/nu-mai-procesa-documente-unul-cate-unul-procesarea-batch-economiseste-ore.html',
    'blog/ocr-scanned-pdfs.html': 'blog/cum-sa-faci-pdf-urile-scanate-searchable-cu-ocr.html',
    'blog/evidence-bundling-best-practices.html': 'blog/cele-mai-bune-practici-pentru-bundling-ul-de-probe-legale.html',
    'blog/what-is-pdf-hardening.html': 'blog/ce-este-pdf-hardening-si-cand-ai-nevoie-de-el.html',
    'blog/accountants-document-management.html': 'blog/sfaturi-de-gestionare-a-documentelor-pentru-contabili-si-auditori.html',
    'blog/docinspector-vs-online-pdf-tools.html': 'blog/docinspector-vs-tool-uri-pdf-online-care-e-diferenta.html',
    'blog/windows-11-pdf-processing.html': 'blog/configurarea-docinspector-pe-windows-11-ghid-rapid.html',
}

# RO translated titles and descriptions
ro_cards = [
    ('how-to', '2026-05-09', 'cum-sa-repari-un-fisier-pdf-corupt-in-cateva-secunde.html',
     'Cum să Repari un Fișier PDF Corupt în Câteva Secunde',
     'PDF-ul nu se deschide? Află cum să repari fișierele PDF corupte cu instrumentul de reparare în lot DocInspector. Funcționează 100% offline.'),
    ('security', '2026-05-10', 'datele-ascunse-din-documentele-tale-si-de-ce-conteaza.html',
     'Datele Ascunse din Documentele Tale (Și De Ce Contează)',
     'PDF-urile și fișierele Word conțin metadate ascunse care pot expune informații personale, istoricul editărilor și locații GPS.'),
    ('education', '2026-05-11', 'pdf-a-vs-pdf-obisnuit-cand-sa-folosesti-fiecare-format.html',
     'PDF/A vs PDF Obișnuit — Când Să Folosești Fiecare Format',
     'Nu toate PDF-urile sunt egale. Află diferența dintre PDF/A și PDF standard și când să folosești fiecare format.'),
    ('education', '2026-05-12', '5-lucruri-pe-care-nu-le-stiai-despre-fisierele-pdf.html',
     '5 Lucruri Pe Care Nu Le Știai Despre Fișierele PDF',
     'PDF-urile par simple, dar ascund o complexitate surprinzătoare. Iată 5 fapte despre fișierele PDF pe care majoritatea nu le cunosc.'),
    ('security', '2026-05-13', 'gdpr-si-metadata-documentelor-sunt-fisierele-tale-conforme.html',
     'GDPR și Metadatele Documentelor: Sunt Fișierele Tale Conforme?',
     'Metadatele documentelor pot conține date personale care încalcă GDPR. Află cum să auditezi și să cureți documentele.'),
    ('how-to', '2026-05-14', 'cum-sa-adaugi-watermark-pe-sute-de-pdf-uri-simultan.html',
     'Cum Să Adaugi Watermark pe Sute de PDF-uri Simultan',
     'Trebuie să aplici watermark pe un folder întreg de PDF-uri? Iată cum să faci asta în câteva secunde cu DocInspector.'),
    ('industry', '2026-05-15', 'de-ce-fiecare-firma-de-avocatura-are-nevoie-de-un-tool-de-inspectie-documente.html',
     'De Ce Fiecare Firmă de Avocatură Are Nevoie de un Tool de Inspecție Documente',
     'Documentele juridice ascund riscuri. Află de ce inspecția documentelor este esențială pentru firmele de avocatură.'),
    ('security', '2026-05-16', 'de-ce-delete-nu-sterge-cu-adevarat-explicatia-shredding-ului-securizat.html',
     'De Ce „Delete" Nu Șterge Cu Adevărat — Explicația Shredding-ului Securizat',
     'Când ștergi un fișier, acesta rămâne pe disc. Află cum funcționează shredding-ul securizat și de ce contează.'),
    ('how-to', '2026-05-17', 'generarea-rapoartelor-excel-pentru-audituri-de-documente-ghid-complet.html',
     'Generarea Rapoartelor Excel pentru Audituri de Documente — Ghid Complet',
     'Află cum DocInspector generează rapoarte Excel detaliate pentru audituri de foldere, cu analiza metadatelor.'),
    ('security', '2026-05-18', 'de-ce-procesarea-offline-a-documentelor-conteaza-mai-mult-ca-niciodata.html',
     'De Ce Procesarea Offline a Documentelor Contează Mai Mult Ca Niciodată',
     'Instrumentele cloud sunt convenabile, dar îți pun documentele în pericol. Iată de ce procesarea offline este alegerea mai sigură.'),
    ('how-to', '2026-05-19', 'cum-sa-aplatizezi-un-pdf-la-format-doar-imagini-si-de-ce-ai-vrea.html',
     'Cum Să Aplatizezi un PDF la Format Doar Imagini (Și De Ce Ai Vrea)',
     'Aplatizarea PDF-urilor la format imagine elimină conținutul ascuns și asigură WYSIWYG. Află când și cum să folosești această tehnică.'),
    ('education', '2026-05-20', 'checklist-complet-pentru-auditul-documentelor-in-2026.html',
     'Checklist Complet pentru Auditul Documentelor în 2026',
     'Un checklist practic pentru auditarea securității documentelor în organizația ta. Acoperă metadate, control acces și conformitate.'),
    ('how-to', '2026-05-21', '7-pasi-pentru-protejarea-documentelor-inainte-de-partajare.html',
     '7 Pași pentru Protejarea Documentelor Înainte de Partajare',
     'Înainte să trimiți, asigură-te că documentele tale nu scurg informații sensibile. Iată 7 pași esențiali.'),
    ('how-to', '2026-05-22', 'nu-mai-procesa-documente-unul-cate-unul-procesarea-batch-economiseste-ore.html',
     'Nu Mai Procesa Documente Unul Câte Unul — Procesarea Batch Economisește Ore',
     'Dacă procesezi încă documentele individual, pierzi ore în fiecare săptămână. Află cum procesarea batch transformă fluxul de lucru.'),
    ('how-to', '2026-05-23', 'cum-sa-faci-pdf-urile-scanate-searchable-cu-ocr.html',
     'Cum Să Faci PDF-urile Scanate Searchable cu OCR',
     'PDF-urile scanate sunt doar imagini — nu poți căuta sau copia text din ele. Află cum OCR rezolvă această problemă.'),
    ('industry', '2026-05-24', 'cele-mai-bune-practici-pentru-bundling-ul-de-probe-legale.html',
     'Cele Mai Bune Practici pentru Bundling-ul de Probe Legale',
     'Crearea de pachete de probe gata pentru tribunal necesită o pregătire atentă a documentelor. Iată cele mai bune practici.'),
    ('education', '2026-05-25', 'ce-este-pdf-hardening-si-cand-ai-nevoie-de-el.html',
     'Ce Este PDF Hardening și Când Ai Nevoie de El?',
     'PDF hardening face documentele rezistente la modificări și elimină amenințările ascunse. Află ce înseamnă și când să-l folosești.'),
    ('industry', '2026-05-26', 'sfaturi-de-gestionare-a-documentelor-pentru-contabili-si-auditori.html',
     'Sfaturi de Gestionare a Documentelor pentru Contabili și Auditori',
     'Contabilii gestionează mii de documente financiare sensibile. Iată cum să le gestionezi în siguranță și eficient.'),
    ('education', '2026-05-27', 'docinspector-vs-tool-uri-pdf-online-care-e-diferenta.html',
     'DocInspector vs Tool-uri PDF Online — Care E Diferența?',
     'De ce să alegi un instrument desktop față de serviciile PDF online gratuite? Iată o comparație sinceră.'),
    ('how-to', '2026-05-28', 'configurarea-docinspector-pe-windows-11-ghid-rapid.html',
     'Configurarea DocInspector pe Windows 11 — Ghid Rapid',
     'Pune DocInspector în funcțiune pe Windows 11 în mai puțin de 2 minute. Descarcă, instalează și procesează primul tău lot.'),
]

cat_labels = {
    'how-to': 'Cum se face',
    'security': 'Securitate',
    'education': 'Educatie',
    'industry': 'Industrie',
}

cards_html = '\n'.join([
    f'''  <div class="blog-card reveal" data-category="{cat}">
    <div class="blog-card-meta"><span class="blog-category" data-i18n="blog.cat.{cat}">{cat_labels[cat]}</span><time datetime="{date}">{date}</time></div>
    <h3><a href="{slug}">{title}</a></h3>
    <p>{desc}</p>
    <a href="{slug}" class="blog-read-more" data-i18n="blog.readMore">Citeste articolul &rarr;</a>
  </div>'''
    for cat, date, slug, title, desc in ro_cards
])

# Build RO from scratch using EN as template but with RO content
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
ro = ro.replace('<a href="user-guide.html" data-i18n="nav.guide">User Guide</a>', '<a href="ghid-utilizare.html" data-i18n="nav.guide">Ghid utilizare</a>')
ro = ro.replace('<a href="reports.html" data-i18n="nav.reports">Reports &amp; Feedback</a>', '<a href="rapoarte.html" data-i18n="nav.reports">Rapoarte &amp; Feedback</a>')
ro = ro.replace('<a href="contact.html" data-i18n="nav.contact">Contact</a>', '<a href="contact.html" data-i18n="nav.contact">Contact</a>')
ro = ro.replace('<a href="download.html" class="btn btn-primary btn-sm mobile-only" data-i18n="nav.download">Download</a>',
                '<a href="descarcare.html" class="btn btn-primary btn-sm mobile-only" data-i18n="nav.download">Descarca</a>')
ro = ro.replace('<a href="download.html" class="btn btn-primary btn-sm desktop-only" data-i18n="nav.download">Download</a>',
                '<a href="descarcare.html" class="btn btn-primary btn-sm desktop-only" data-i18n="nav.download">Descarcare</a>')
ro = ro.replace('<a href="privacy.html" data-i18n="footer.privacy">Privacy Policy</a>',
                '<a href="politica-de-confidentialitate.html" data-i18n="footer.privacy">Politica de Confidentialitate</a>')
ro = ro.replace('<a href="terms.html" data-i18n="footer.terms">Terms of Service</a>',
                '<a href="termeni.html" data-i18n="footer.terms">Termeni</a>')
ro = ro.replace('<a href="refund.html" data-i18n="footer.refund">Refund Policy</a>',
                '<a href="rambursare.html" data-i18n="footer.refund">Rambursare</a>')

# Replace the cards block with RO translated cards
import re
ro = re.sub(r'<div class="blog-grid" id="blogGrid">.*?</div>\s*\n\s*<div class="blog-no-results"',
            f'<div class="blog-grid" id="blogGrid">\n{cards_html}\n</div>\n\n<div class="blog-no-results"',
            ro, flags=re.DOTALL)

with open('ro/blog.html', 'w', encoding='utf-8') as f:
    f.write(ro)
print('RO blog.html done with translated cards and correct slugs')
