import re

files = [
    r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
]

def patch_file(content):
    # Reduce tools-hero padding (top from 9rem to 6.5rem, bottom from 5rem to 2rem)
    content = content.replace("padding:9rem 0 5rem;", "padding:6.5rem 0 2rem;")
    
    # Reduce hero-lead bottom margin (from 2.5rem to 1.5rem)
    content = content.replace("margin:0 auto 2.5rem;", "margin:0 auto 1.5rem;")
    
    # Reduce the space between hero and the tools-layout section
    content = content.replace('<section style="padding-top:2rem;position:relative;z-index:1">', '<section style="padding-top:0;position:relative;z-index:1">')
    
    # Optionally remove the empty badges-row if it exists
    empty_badges = """<div class="badges-row gsap-fade">
  
      </div>"""
    if empty_badges in content:
        content = content.replace(empty_badges, "")

    return content

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = patch_file(html)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

print("Spacing successfully reduced!")
