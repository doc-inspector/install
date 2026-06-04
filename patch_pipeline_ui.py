import re

files = [
    r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
]

def patch_file(content):
    # 1. Update pipeline UI sorting logic
    old_map = "...[...selectedOps].map(op => ({"
    new_map = """...[...selectedOps].sort((a,b) => {
        const order = { 'rebuild':1, 'redact':2, 'flatten':3, 'watermark':4, 'sanitize':5, 'encrypt':6 };
        return (order[a]||99) - (order[b]||99);
      }).map(op => ({"""
    if old_map in content:
        content = content.replace(old_map, new_map)

    # 2. Add green styling to processBtn (inline styles to overwrite the cyan gradient)
    # The original is: <button class="process-btn" id="processBtn" disabled onclick="startProcessing()">
    old_btn = '<button class="process-btn" id="processBtn" disabled onclick="startProcessing()">'
    new_btn = '<button class="process-btn" id="processBtn" disabled onclick="startProcessing()" style="background:linear-gradient(135deg, #10b981, #34d399); box-shadow: 0 4px 20px rgba(16,185,129,.3); color:#ffffff;">'
    if old_btn in content:
        content = content.replace(old_btn, new_btn)

    # There's also hover effects, but inline styles will take precedence for background and color.
    # To fix hover box-shadow, we can inject a quick style rule.
    css_fix = """#processBtn:hover:not(:disabled) { box-shadow: 0 8px 30px rgba(16,185,129,.5), 0 0 40px rgba(16,185,129,.2) !important; transform: translateY(-2px); }"""
    if 'processBtn:hover' not in content:
        content = content.replace('</style>', css_fix + '\n  </style>')

    return content

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = patch_file(html)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

print("Pipeline UI ordered and Process button colored green!")
