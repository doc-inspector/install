import os
import glob
import re

html_files = glob.glob('c:/Users/Admin/Desktop/doc-inspector-site-main/Public/*.html')

new_js = """        (() => {
            const btns = document.querySelectorAll('.lang-btn');
            const navToggle = document.getElementById('navToggle'); 
            const navLinks = document.getElementById('navLinks');
            
            btns.forEach(btn => {
                btn.onclick = (e) => { 
                    e.stopPropagation(); 
                    const dd = btn.closest('.lang-dropdown');
                    dd.classList.toggle('open'); 
                };
            });
            
            document.querySelectorAll('.lang-item').forEach(i => {
                i.onclick = () => {
                    if (window.__i18n) window.__i18n.setLang(i.dataset.lang); 
                    document.querySelectorAll('.lang-dropdown.open').forEach(dd => dd.classList.remove('open'));
                };
            });
            
            if (navToggle) navToggle.onclick = () => { 
                navLinks.classList.toggle('active'); 
                navToggle.classList.toggle('open'); 
            };
            
            document.onclick = () => document.querySelectorAll('.lang-dropdown.open').forEach(dd => dd.classList.remove('open'));
        })();"""

old_js_regex = re.compile(r'\(\(\)\s*=>\s*\{.*?const\s+dd\s*=\s*document\.getElementById\(\'langDropdown\'\).*?dd\.classList\.remove\(\'open\'\);\s*\}\)\(\);', re.DOTALL)

mobile_lang_html = """
                        <div class="lang-dropdown mobile-only">
                            <button class="lang-btn"><span class="lang-pill">EN</span> <span class="chev">▾</span></button>
                            <div class="lang-menu">
                                <button class="lang-item" data-lang="EN">EN</button>
                                <button class="lang-item" data-lang="RO">RO</button>
                                <button class="lang-item" data-lang="RU">RU</button>
                            </div>
                        </div>"""

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add desktop-only class to the existing lang-dropdown in nav-actions
    content = content.replace('<div class="lang-dropdown" id="langDropdown">', '<div class="lang-dropdown desktop-only">')

    # Add mobile-only lang-dropdown at the end of nav-links
    if "mobile-only" not in content:
        content = content.replace('</nav>', mobile_lang_html + '\n                    </nav>')

    # Replace old JS
    content = old_js_regex.sub(new_js, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {filepath}")
