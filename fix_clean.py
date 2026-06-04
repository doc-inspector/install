import os
import re

filepath = r"E:\Website online and local app new project\Public2\Public\en\tools-online.html"
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the extra brace
pattern = r'(card\.style\.pointerEvents = "auto";\s*\}\s*\});\s*\}(\s*// Dynamically update bundle card limits[\s\S]*?updateBtn\(\);\s*\})'
html = re.sub(pattern, r'\1\2', html)

# Fix the newline in alert(msg.join('\n'))
html = html.replace('alert(msg.join("\n"));', r'alert(msg.join("\\n"));')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
