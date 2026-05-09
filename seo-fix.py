import re, os, datetime

BASE = "https://doc-inspector.com"
DIR = "/home/user/doc-inspector-redesign/Public"
TODAY = datetime.date.today().isoformat()

# SEO data per page
PAGES = {
    "index.html": {
        "title": "DocInspector — Batch Document Repair, Audit & Hardening for Windows",
        "desc": "Professional Windows desktop utility for batch PDF repair, document auditing, metadata sanitization, evidence bundling and secure reporting. 100% offline local processing — no cloud, no AI risk.",
        "keywords": "PDF repair, document audit, batch processing, metadata removal, evidence bundling, Windows desktop, offline PDF tool, document security, PDF hardening",
        "og_title": "DocInspector — Batch Document Repair, Audit & Hardening",
        "og_desc": "Professional Windows utility for batch PDF repair, document auditing & secure reporting. 100% local processing.",
        "priority": "1.0",
        "changefreq": "weekly",
        "jsonld_type": "SoftwareApplication",
    },
    "price.html": {
        "title": "Pricing & Plans — DocInspector Professional Licensing",
        "desc": "Transparent pricing for DocInspector. Choose Basic for PDF rebuilding and evidence kits, or Pro for the full suite with folder-level reports, batch processing, and secure shredding.",
        "keywords": "DocInspector pricing, PDF repair software price, document audit tool cost, batch processing license, professional PDF tool",
        "og_title": "DocInspector Pricing — Professional Licensing Plans",
        "og_desc": "Choose your plan: Basic PDF toolkit or Pro full suite. All plans include 100% local processing.",
        "priority": "0.8",
        "changefreq": "monthly",
    },
    "download.html": {
        "title": "Download DocInspector — Free Trial for Windows",
        "desc": "Download DocInspector for Windows. Professional batch document repair, PDF auditing, and evidence bundling tool. Free 3-day trial, no credit card required. Works 100% offline.",
        "keywords": "download DocInspector, PDF repair tool download, document audit software, Windows PDF tool, free trial, offline document processor",
        "og_title": "Download DocInspector — Free Trial",
        "og_desc": "Download the professional document repair & audit tool for Windows. Free 3-day trial, no credit card required.",
        "priority": "0.9",
        "changefreq": "weekly",
    },
    "user-guide.html": {
        "title": "User Guide — DocInspector Knowledge Hub",
        "desc": "Complete DocInspector user guide. Master batch workflows for PDF repair, document auditing, metadata sanitization, secure shredding, and Excel report generation.",
        "keywords": "DocInspector guide, PDF repair tutorial, document audit how-to, batch processing guide, metadata removal tutorial",
        "og_title": "DocInspector User Guide — Knowledge Hub",
        "og_desc": "Complete guide to mastering DocInspector's batch workflows for PDF repair, auditing, and reporting.",
        "priority": "0.8",
        "changefreq": "monthly",
    },
    "user-guide-audit.html": {
        "title": "Audit & Security Guide — DocInspector",
        "desc": "Learn how to use DocInspector's Audit & Security module to discover hidden sensitive documents, sanitize metadata, and perform secure shredding across your entire PC.",
        "keywords": "document audit, metadata sanitization, secure file shredding, sensitive document discovery, DocInspector audit module",
        "og_title": "Audit & Security Guide — DocInspector",
        "og_desc": "Discover hidden sensitive documents, sanitize metadata, and securely shred files with DocInspector.",
        "priority": "0.7",
        "changefreq": "monthly",
    },
    "user-guide-pdf-repair.html": {
        "title": "PDF Repair & Hardening Guide — DocInspector",
        "desc": "Master DocInspector's PDF Repair module. Reconstruct broken PDFs, apply OCR, flatten documents to image-only formats, add batch watermarks, and harden evidence bundles.",
        "keywords": "PDF repair, fix broken PDF, OCR PDF, flatten PDF, batch watermark, PDF hardening, document reconstruction, DocInspector repair",
        "og_title": "PDF Repair & Hardening Guide — DocInspector",
        "og_desc": "Fix broken PDFs, apply OCR, flatten and watermark documents in batch with DocInspector.",
        "priority": "0.7",
        "changefreq": "monthly",
    },
    "user-guide-reporting.html": {
        "title": "Reporting & Evidence Guide — DocInspector",
        "desc": "Generate comprehensive Excel reports for PDF bundles and folder evidence trees. Learn DocInspector's reporting module for auditors, lawyers, and compliance teams.",
        "keywords": "PDF report generator, evidence tree audit, Excel document report, folder audit report, DocInspector reporting, legal evidence bundle",
        "og_title": "Reporting & Evidence Guide — DocInspector",
        "og_desc": "Generate Excel reports for PDF bundles and evidence folder audits with DocInspector.",
        "priority": "0.7",
        "changefreq": "monthly",
    },
    "contact.html": {
        "title": "Contact & Support — DocInspector",
        "desc": "Contact the DocInspector support team for questions about professional licensing, batch processing features, bug reports, or custom enterprise solutions.",
        "keywords": "DocInspector contact, support, bug report, enterprise license, customer service",
        "og_title": "Contact DocInspector Support",
        "og_desc": "Get help with DocInspector licensing, features, or technical support.",
        "priority": "0.5",
        "changefreq": "yearly",
    },
    "history.html": {
        "title": "Version History & Changelog — DocInspector",
        "desc": "DocInspector version history and changelog. See all updates, improvements, bug fixes and new features across every release.",
        "keywords": "DocInspector changelog, version history, updates, release notes, new features",
        "og_title": "DocInspector Changelog & Version History",
        "og_desc": "All updates, improvements and new features across every DocInspector release.",
        "priority": "0.5",
        "changefreq": "weekly",
    },
    "reports.html": {
        "title": "Bug Reports & Feature Requests — DocInspector",
        "desc": "Report bugs or request new features for DocInspector. Submit feedback securely with attachments to help improve document repair and audit workflows.",
        "keywords": "DocInspector bug report, feature request, feedback, issue tracker",
        "og_title": "Report a Bug or Request a Feature — DocInspector",
        "og_desc": "Help improve DocInspector by reporting bugs or requesting new features.",
        "priority": "0.4",
        "changefreq": "yearly",
    },
    "privacy.html": {
        "title": "Privacy Policy — DocInspector",
        "desc": "DocInspector Privacy Policy. 100% local air-gapped processing guarantees maximum document security with zero cloud uploads or AI data risks.",
        "keywords": "DocInspector privacy, data security, offline processing, GDPR, no cloud, air-gapped",
        "og_title": "Privacy Policy — DocInspector",
        "og_desc": "100% local processing. No cloud. No AI risk. Read our privacy policy.",
        "priority": "0.3",
        "changefreq": "yearly",
    },
    "terms.html": {
        "title": "Terms of Service — DocInspector",
        "desc": "DocInspector Terms of Service. Read the usage terms, licensing agreement, and acceptable use policies for the document repair and audit software.",
        "keywords": "DocInspector terms, terms of service, license agreement, usage policy",
        "og_title": "Terms of Service — DocInspector",
        "og_desc": "DocInspector terms of service and licensing agreement.",
        "priority": "0.3",
        "changefreq": "yearly",
    },
    "refund.html": {
        "title": "Refund Policy — DocInspector",
        "desc": "DocInspector Refund Policy. Free 3-day trial included with every plan. Understand refund eligibility and cancellation terms.",
        "keywords": "DocInspector refund, cancellation, free trial, money back, refund policy",
        "og_title": "Refund Policy — DocInspector",
        "og_desc": "Free 3-day trial. Read our refund and cancellation policy.",
        "priority": "0.3",
        "changefreq": "yearly",
    },
}

# OG image — use existing logo or screenshot
OG_IMAGE = f"{BASE}/assets/logo.png"

def build_seo_block(page, data):
    """Build the SEO meta tags to inject after <meta viewport>"""
    canonical = f"{BASE}/{page}" if page != "index.html" else BASE + "/"
    
    block = f'''
  <!-- SEO -->
  <link rel="canonical" href="{canonical}" />
  <meta name="keywords" content="{data['keywords']}" />
  
  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{data['og_title']}" />
  <meta property="og:description" content="{data['og_desc']}" />
  <meta property="og:image" content="{OG_IMAGE}" />
  <meta property="og:site_name" content="DocInspector" />
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{data['og_title']}" />
  <meta name="twitter:description" content="{data['og_desc']}" />
  <meta name="twitter:image" content="{OG_IMAGE}" />'''
    
    return block

def build_jsonld_software():
    """JSON-LD structured data for the main page"""
    return '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "DocInspector",
    "description": "Professional Windows desktop utility for batch PDF repair, document auditing, metadata sanitization, evidence bundling and secure reporting.",
    "url": "https://doc-inspector.com",
    "downloadUrl": "https://doc-inspector.com/download.html",
    "operatingSystem": "Windows 10, Windows 11",
    "applicationCategory": "UtilitiesApplication",
    "applicationSubCategory": "Document Processing",
    "softwareVersion": "2.0",
    "author": {
      "@type": "Organization",
      "name": "DocInspector",
      "url": "https://doc-inspector.com"
    },
    "offers": [
      {
        "@type": "Offer",
        "name": "Basic",
        "price": "9.99",
        "priceCurrency": "EUR",
        "priceValidUntil": "2027-12-31"
      },
      {
        "@type": "Offer",
        "name": "Pro",
        "price": "18.99",
        "priceCurrency": "EUR",
        "priceValidUntil": "2027-12-31"
      }
    ],
    "featureList": [
      "Batch PDF repair and reconstruction",
      "Document metadata sanitization",
      "Secure file shredding",
      "Evidence bundle creation",
      "Excel report generation",
      "100% offline local processing"
    ]
  }
  </script>'''

def build_jsonld_webpage(page, data):
    """JSON-LD WebPage for subpages"""
    canonical = f"{BASE}/{page}" if page != "index.html" else BASE + "/"
    return f'''
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "{data['og_title']}",
    "description": "{data['og_desc']}",
    "url": "{canonical}",
    "isPartOf": {{
      "@type": "WebSite",
      "name": "DocInspector",
      "url": "https://doc-inspector.com"
    }}
  }}
  </script>'''

def process_page(page, data):
    filepath = os.path.join(DIR, page)
    with open(filepath, 'r') as f:
        html = f.read()
    
    # Skip thanks.html (noindex page)
    if page == "thanks.html":
        return
    
    # Remove existing keywords meta if present (we'll add fresh)
    html = re.sub(r'\s*<meta name="keywords"[^>]*/?>\n?', '', html)
    
    # Remove old OG/Twitter tags if any exist
    html = re.sub(r'\s*<meta property="og:[^>]*/?>\n?', '', html)
    html = re.sub(r'\s*<meta name="twitter:[^>]*/?>\n?', '', html)
    html = re.sub(r'\s*<link rel="canonical"[^>]*/?>\n?', '', html)
    html = re.sub(r'\s*<!-- SEO -->\n?', '', html)
    html = re.sub(r'\s*<!-- Open Graph -->\n?', '', html)
    html = re.sub(r'\s*<!-- Twitter Card -->\n?', '', html)
    html = re.sub(r'\s*<script type="application/ld\+json">.*?</script>\n?', '', html, flags=re.DOTALL)
    
    # Update title
    html = re.sub(
        r'<title[^>]*>.*?</title>',
        f'<title>{data["title"]}</title>',
        html,
        count=1
    )
    
    # Update meta description
    # Handle both single-line and multi-line meta descriptions
    html = re.sub(
        r'<meta name="description"\s*\n?\s*content="[^"]*"\s*/?>',
        f'<meta name="description" content="{data["desc"]}" />',
        html,
        count=1
    )
    
    # Build SEO block
    seo_block = build_seo_block(page, data)
    
    # Add JSON-LD
    if page == "index.html":
        seo_block += build_jsonld_software()
    else:
        seo_block += build_jsonld_webpage(page, data)
    
    # Inject after the last meta viewport line
    # Find the meta description line and inject after it
    desc_pattern = r'(<meta name="description" content="[^"]*" />)'
    match = re.search(desc_pattern, html)
    if match:
        insert_pos = match.end()
        html = html[:insert_pos] + seo_block + html[insert_pos:]
    
    with open(filepath, 'w') as f:
        f.write(html)
    
    print(f"  ✓ {page}")

# Process all pages
print("Applying SEO fixes...")
for page, data in PAGES.items():
    process_page(page, data)

# Update sitemap.xml with all pages and fresh dates
print("\nUpdating sitemap.xml...")
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for page, data in PAGES.items():
    if page == "thanks.html":
        continue
    url = f"{BASE}/{page}" if page != "index.html" else f"{BASE}/"
    sitemap += f'''  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{data.get("changefreq", "monthly")}</changefreq>
    <priority>{data.get("priority", "0.5")}</priority>
  </url>
'''
sitemap += '</urlset>\n'

with open(os.path.join(DIR, "sitemap.xml"), 'w') as f:
    f.write(sitemap)
print("  ✓ sitemap.xml")

# Update robots.txt
print("\nUpdating robots.txt...")
robots = f"""User-agent: *
Allow: /
Disallow: /thanks.html

Sitemap: {BASE}/sitemap.xml
"""
with open(os.path.join(DIR, "robots.txt"), 'w') as f:
    f.write(robots)
print("  ✓ robots.txt")

print("\n✅ SEO audit fixes complete!")
