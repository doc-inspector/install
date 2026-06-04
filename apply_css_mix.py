import re

files = [
    r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
]

def update_css(content):
    # Update .tool-card
    content = content.replace(
        'background: linear-gradient(135deg, rgba(6, 182, 212, 0.05), rgba(15, 32, 66, 0.8)) !important;',
        'background: linear-gradient(135deg, color-mix(in srgb, var(--brand, #06b6d4) 5%, transparent), rgba(15, 32, 66, 0.8)) !important;'
    )
    content = content.replace(
        'border: 1px solid rgba(6, 182, 212, 0.2) !important;',
        'border: 1px solid color-mix(in srgb, var(--brand, #06b6d4) 20%, transparent) !important;'
    )
    
    # Update .tool-card::before
    content = content.replace(
        'background:linear-gradient(135deg,rgba(6,182,212,0.12),transparent);',
        'background:linear-gradient(135deg,color-mix(in srgb, var(--brand, #06b6d4) 12%, transparent),transparent);'
    )
    
    # Update .tool-card:hover
    content = content.replace(
        'border-color: rgba(6,182,212,.65) !important;',
        'border-color: color-mix(in srgb, var(--brand, #06b6d4) 65%, transparent) !important;'
    )
    content = content.replace(
        'background: linear-gradient(135deg, rgba(6, 182, 212, 0.12), rgba(20, 50, 95, 0.85)) !important;',
        'background: linear-gradient(135deg, color-mix(in srgb, var(--brand, #06b6d4) 12%, transparent), rgba(20, 50, 95, 0.85)) !important;'
    )
    content = content.replace(
        'box-shadow: 0 12px 36px rgba(6, 182, 212, 0.18), inset 0 1px 0 rgba(255,255,255,0.1);',
        'box-shadow: 0 12px 36px color-mix(in srgb, var(--brand, #06b6d4) 18%, transparent), inset 0 1px 0 rgba(255,255,255,0.1);'
    )
    
    # Update .tool-card.selected
    content = content.replace(
        'border-color: rgba(6,182,212,.95) !important;',
        'border-color: var(--brand, #06b6d4) !important;'
    )
    content = content.replace(
        'background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(10, 30, 60, 0.9)) !important;',
        'background: linear-gradient(135deg, color-mix(in srgb, var(--brand, #06b6d4) 20%, transparent), rgba(10, 30, 60, 0.9)) !important;'
    )
    content = content.replace(
        'box-shadow: 0 0 25px rgba(6, 182, 212, 0.25), inset 0 1px 0 rgba(255,255,255,0.15);',
        'box-shadow: 0 0 25px color-mix(in srgb, var(--brand, #06b6d4) 25%, transparent), inset 0 1px 0 rgba(255,255,255,0.15);'
    )
    
    # Update ripple
    content = content.replace(
        'background:rgba(6,182,212,.2); transform:scale(0);',
        'background:color-mix(in srgb, var(--brand, #06b6d4) 20%, transparent); transform:scale(0);'
    )
    
    # Update check-ring
    content = content.replace(
        'background:var(--cyan); display:flex; align-items:center;',
        'background:var(--brand, var(--cyan)); display:flex; align-items:center;'
    )
    
    # Clean up inline styles for inner opts to use the brand background!
    # Instead of replacing specific inline styles, let's just make sure all .tool-opts-inner look good
    # First, let's add a CSS rule to overwrite background inside tool-opts-inner
    new_inner_css = """
      .tool-opts-inner {
        border-top:1px solid rgba(255,255,255,.07);
        padding:1rem; display:grid; gap:.8rem;
        background: linear-gradient(to bottom, color-mix(in srgb, var(--brand, #06b6d4) 6%, transparent), rgba(0,0,0,0.3)) !important;
        border: 1px solid color-mix(in srgb, var(--brand, #06b6d4) 15%, rgba(255,255,255,0.05)) !important;
        border-radius: 12px;
        margin-bottom: 1rem;
      }
"""
    content = re.sub(r'\.tool-opts-inner\s*\{[^}]*\}', new_inner_css.strip(), content)
    
    return content

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = update_css(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Updated CSS with color-mix for brand colors!")
