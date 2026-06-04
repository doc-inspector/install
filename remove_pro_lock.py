import re

files = [
    r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to remove the entire `proFeatures.forEach` loop from updateUI
    # The pattern starts with `const proFeatures` and ends right before `}` of `updateUI`
    pattern = r"const proFeatures = \['redact', 'flatten'\];[\s\S]*?card\.style\.pointerEvents = \"auto\";\s*\}\s*\}\);"
    content = re.sub(pattern, '', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Removed PRO lock from Redact and Flatten features in all languages!")
