import glob

html_files = glob.glob('c:/Users/Admin/Desktop/doc-inspector-site-main/Public/*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple cache bust parameter
    content = content.replace('href="style.css"', 'href="style.css?v=2"')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done", filepath)
