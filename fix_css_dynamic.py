import re

files = [
    r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
]

def fix_css(content):
    # Original (or what it is now):
    # .tool-opts {
    #   max-height:0; overflow:hidden;
    #   transition:max-height .4s ease, opacity .3s;
    #   opacity:0;
    # }
    # .tool-opts.open { max-height:1200px; opacity:1; }
    
    pattern = r'\.tool-opts\s*\{\s*max-height:0;\s*overflow:hidden;\s*transition:max-height [^;]+;\s*opacity:0;\s*\}\s*\.tool-opts\.open\s*\{\s*max-height:1200px;\s*opacity:1;\s*\}'
    
    replacement = r'''.tool-opts {
        display: grid; grid-template-rows: 0fr;
        transition: grid-template-rows .4s ease, opacity .3s;
        opacity: 0;
      }
      .tool-opts.open { grid-template-rows: 1fr; opacity: 1; }
      .tool-opts > div { overflow: hidden; }'''
    
    return re.sub(pattern, replacement, content)

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = fix_css(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Fixed CSS to use dynamic grid-template-rows!")
