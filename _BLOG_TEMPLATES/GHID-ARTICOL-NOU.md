# 📝 Ghid — Cum Adaugi un Articol Nou pe Doc-Inspector.com

> Urmează pașii în ordine. Nu sări niciun pas.

---

## PASUL 1 — Definește articolul (înainte de orice)

Notează-ți aceste 7 valori — le vei folosi peste tot:

| Câmp | Exemplu |
|------|---------|
| **SLUG_RO** | `cum-sa-protejezi-pdf-ul-cu-parola` |
| **SLUG_EN** | `how-to-password-protect-pdf` |
| **SLUG_RU** | `kak-zashchitit-pdf-parolem` |
| **TITLU_RO** | `Cum Să Protejezi un PDF cu Parolă` |
| **TITLU_EN** | `How to Password Protect a PDF` |
| **TITLU_RU** | `Как Защитить PDF Паролем` |
| **DATA** | `2026-07-15` |
| **CATEGORIE** | `how-to` (valori posibile: `security`, `how-to`, `education`, `industry`) |
| **DESCRIERE_RO** | Max 160 caractere, pentru meta description + card |
| **DESCRIERE_EN** | Max 160 caractere |
| **DESCRIERE_RU** | Max 160 caractere |

---

## PASUL 2 — Creează cele 3 fișiere HTML

Copiază template-ul pentru fiecare limbă și înlocuiește toate `{{PLACEHOLDER}}`-urile:

```
_BLOG_TEMPLATES/template-ro.html  →  Public/ro/blog/{{SLUG_RO}}.html
_BLOG_TEMPLATES/template-en.html  →  Public/en/blog/{{SLUG_EN}}.html
_BLOG_TEMPLATES/template-ru.html  →  Public/ru/blog/{{SLUG_RU}}.html
```

**Ce înlocuiești în fiecare fișier:**

| Placeholder | Cu ce îl înlocuiești |
|-------------|----------------------|
| `{{SLUG_RO}}` | slug-ul RO |
| `{{SLUG_EN}}` | slug-ul EN |
| `{{SLUG_RU}}` | slug-ul RU |
| `{{TITLU}}` | titlul în limba fișierului |
| `{{DESCRIERE}}` | descrierea în limba fișierului |
| `{{DATA}}` | data în format `YYYY-MM-DD` |
| `{{CATEGORIE}}` | una din: `security`, `how-to`, `education`, `industry` |
| `{{CONTINUT}}` | conținutul articolului (HTML) |

---

## PASUL 3 — Adaugă cardul în paginile de listing

Fișiere de modificat:
- `Public/ro/blog.html`
- `Public/en/blog.html`
- `Public/ru/blog.html`

**Găsește primul `<a class="blog-card"` din fișier și inserează ÎNAINTE de el:**

### Card RO (în `ro/blog.html`):
```html
<a href="blog/{{SLUG_RO}}" class="blog-card reveal" data-category="{{CATEGORIE}}" data-title="{{TITLU_lowercase}}" data-desc="{{DESCRIERE_lowercase}}">
  <div class="blog-card-meta">
    <span data-i18n="blog.cat.{{CATEGORIE}}">{{ETICHETA_CATEGORIE_RO}}</span> | {{DATA}}
  </div>
  <h3>{{TITLU_RO}}</h3>
  <p>{{DESCRIERE_RO}}</p>
  <div class="blog-card-read" data-i18n="blog.readMore">Citește articolul →</div>
</a>
```

### Card EN (în `en/blog.html`):
```html
<a href="blog/{{SLUG_EN}}" class="blog-card reveal" data-category="{{CATEGORIE}}" data-title="{{TITLU_EN_lowercase}}" data-desc="{{DESCRIERE_EN_lowercase}}">
  <div class="blog-card-meta">
    <span data-i18n="blog.cat.{{CATEGORIE}}">{{CATEGORY_LABEL_EN}}</span> | {{DATA}}
  </div>
  <h3>{{TITLU_EN}}</h3>
  <p>{{DESCRIERE_EN}}</p>
  <div class="blog-card-read" data-i18n="blog.readMore">Read article →</div>
</a>
```

### Card RU (în `ru/blog.html`):
```html
<a href="blog/{{SLUG_RU}}" class="blog-card reveal" data-category="{{CATEGORIE}}" data-title="{{TITLU_RU_lowercase}}" data-desc="{{DESCRIERE_RU_lowercase}}">
  <div class="blog-card-meta">
    <span data-i18n="blog.cat.{{CATEGORIE}}">{{ETICHETA_CATEGORIE_RU}}</span> | {{DATA}}
  </div>
  <h3>{{TITLU_RU}}</h3>
  <p>{{DESCRIERE_RU}}</p>
  <div class="blog-card-read" data-i18n="blog.readMore">Читать статью →</div>
</a>
```

**Etichete categorii:**
| Cod | RO | EN | RU |
|-----|----|----|-----|
| `security` | Securitate | Security | Безопасность |
| `how-to` | Cum se face | How-To | Инструкции |
| `education` | Educație | Education | Образование |
| `industry` | Industrie | Industry | Отрасль |

---

## PASUL 4 — Adaugă în Sitemap

Fișier: `Public/sitemap.xml`

Găsește ultimul bloc `<url>` de tip blog și adaugă **după el** 3 blocuri noi (unul per limbă):

```xml
  <url>
    <loc>https://doc-inspector.com/en/blog/{{SLUG_EN}}</loc>
    <lastmod>{{DATA}}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <xhtml:link rel="alternate" hreflang="en" href="https://doc-inspector.com/en/blog/{{SLUG_EN}}"/>
    <xhtml:link rel="alternate" hreflang="ro" href="https://doc-inspector.com/ro/blog/{{SLUG_RO}}"/>
    <xhtml:link rel="alternate" hreflang="ru" href="https://doc-inspector.com/ru/blog/{{SLUG_RU}}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://doc-inspector.com/en/blog/{{SLUG_EN}}"/>
  </url>
  <url>
    <loc>https://doc-inspector.com/ro/blog/{{SLUG_RO}}</loc>
    <lastmod>{{DATA}}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <xhtml:link rel="alternate" hreflang="en" href="https://doc-inspector.com/en/blog/{{SLUG_EN}}"/>
    <xhtml:link rel="alternate" hreflang="ro" href="https://doc-inspector.com/ro/blog/{{SLUG_RO}}"/>
    <xhtml:link rel="alternate" hreflang="ru" href="https://doc-inspector.com/ru/blog/{{SLUG_RU}}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://doc-inspector.com/en/blog/{{SLUG_EN}}"/>
  </url>
  <url>
    <loc>https://doc-inspector.com/ru/blog/{{SLUG_RU}}</loc>
    <lastmod>{{DATA}}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <xhtml:link rel="alternate" hreflang="en" href="https://doc-inspector.com/en/blog/{{SLUG_EN}}"/>
    <xhtml:link rel="alternate" hreflang="ro" href="https://doc-inspector.com/ro/blog/{{SLUG_RO}}"/>
    <xhtml:link rel="alternate" hreflang="ru" href="https://doc-inspector.com/ru/blog/{{SLUG_RU}}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://doc-inspector.com/en/blog/{{SLUG_EN}}"/>
  </url>
```

---

## PASUL 5 — Push pe GitHub

```bash
git add Public/ro/blog/{{SLUG_RO}}.html
git add Public/en/blog/{{SLUG_EN}}.html
git add Public/ru/blog/{{SLUG_RU}}.html
git add Public/ro/blog.html Public/en/blog.html Public/ru/blog.html
git add Public/sitemap.xml
git commit -m "blog: adauga articol {{SLUG_EN}}"
git push
```

---

## Checklist final ✅

- [ ] 3 fișiere HTML create (RO + EN + RU)
- [ ] Toate `{{PLACEHOLDER}}`-urile înlocuite în toate 3 fișiere
- [ ] Card adăugat în `ro/blog.html`, `en/blog.html`, `ru/blog.html`
- [ ] Sitemap actualizat cu cele 3 blocuri
- [ ] Push pe GitHub
- [ ] Verificat că articolul se deschide pe site

---

## Reguli de respectat mereu

1. **Slug-ul** = doar litere mici, cifre, cratime. Fără spații, fără diacritice.
2. **Copyright footer** = mereu `© 2025 DocInspector` (nu niciodată un nume personal)
3. **Author în schema.org** = `"@type": "Organization", "name": "DocInspector"`
4. **hreflang** = toate 3 limbi prezente în fiecare fișier
5. **data-i18n** pe footer + nav = nu modifica, se traduce automat din i18n-dict.v2.js
6. **Nu adăuga** `Vladimir Tonu` / `Tonu Vladimir` nicăieri
