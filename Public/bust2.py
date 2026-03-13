import glob

html_files = glob.glob('c:/Users/Admin/Desktop/doc-inspector-site-main/Public/*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple cache bust parameter
    content = content.replace('href="style.css?v=4"', 'href="style.css?v=5"')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done", filepath)
