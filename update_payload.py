import re
import os

files_to_update = {
    'en': r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    'ro': r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    'ru': r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
}

def fix_payload(content):
    if 'watermarkAngle:' in content:
        return content
    
    # In gatherOptions():
    # watermarkOpacity: (parseInt(document.getElementById('wm-opacity')?.value || 15) / 100).toFixed(2),
    # -> add watermarkAngle
    pattern = r'(watermarkOpacity:\s*\(parseInt\(document\.getElementById\(\'wm-opacity\'\)\?\.value \|\| 15\) / 100\)\.toFixed\(2\),)'
    replacement = r"\1\n      watermarkAngle:   document.getElementById('wm-angle')?.value   || '-45',"
    
    return re.sub(pattern, replacement, content)

for lang, filepath in files_to_update.items():
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = fix_payload(content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("JS payload updated with watermarkAngle!")
