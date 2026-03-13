import glob

html_files = glob.glob('c:/Users/Admin/Desktop/doc-inspector-site-main/Public/*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace footer bug link
    content = content.replace('href="contact.html" class="btn btn-outline btn-sm" data-i18n="footer.bug"', 'href="https://doc-inspector.com/reports" class="btn btn-outline btn-sm" data-i18n="footer.bug"')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated links in", filepath)
