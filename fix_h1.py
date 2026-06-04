import re

files = [
    r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
]

def patch_file(content):
    # 1. Reduce font size and increase max-width in CSS
    old_css = "font-size:clamp(2.4rem,5vw,4.2rem);"
    new_css = "font-size:clamp(2.2rem,4.5vw,3.6rem);"
    content = content.replace(old_css, new_css)
    
    content = content.replace("max-width:820px;", "max-width:960px;")
    
    # 2. Remove <br> from the h1 tags to allow dynamic centering and wrapping
    content = content.replace("Process Documents Directly in<br>Your Browser", "Process Documents Directly in Your Browser")
    content = content.replace("Procesează PDF-uri Direct<br>în Browserul Tău", "Procesează PDF-uri Direct în Browserul Tău")
    content = content.replace("Обрабатывайте PDF<br>Прямо в Браузере", "Обрабатывайте PDF Прямо в Браузере")
    
    return content

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = patch_file(html)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

print("H1 successfully updated!")
