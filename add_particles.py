import re

files = [
    r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add hex-particles
    content = content.replace('<section class="tools-hero">', '<section class="tools-hero" style="position:relative;overflow:hidden;">\n    <div class="cyber-grid"></div>\n    <div class="hex-particles"></div>')
    
    # Ensure container sits above particles
    content = content.replace('<div class="container">\n      <div class="hero-eyebrow-pill', '<div class="container" style="position:relative;z-index:1;">\n      <div class="hero-eyebrow-pill')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Added particles to tools-hero section!")
