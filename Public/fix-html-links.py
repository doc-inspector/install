#!/usr/bin/env python3
"""
fix-html-links.py
Removes .html extensions from ALL internal links across all static pages.

Cloudflare Pages automatically 308-redirects .html URLs to extensionless ones.
Having .html in internal links causes Google to see "Page with redirect" for every page.

This script fixes ALL internal href="*.html" links to their extensionless equivalents:
  - "price.html"           → "price"
  - "index.html"           → "./"
  - "../ro/index.html"     → "../ro/"
  - "user-guide.html#compare" → "user-guide#compare"
  - "blog/some-post.html"  → "blog/some-post"
  
It does NOT touch:
  - External links (https://, http://)
  - JavaScript/CSS file references
  - Anchor-only links (#section)
  - Data attributes that aren't href
"""
import os
import re
import glob

DIR = os.path.dirname(os.path.abspath(__file__))

def fix_html_links(content):
    """Replace .html extensions in href attributes with extensionless versions."""
    
    def replace_href(match):
        prefix = match.group(1)   # 'href="' or "href='"
        url = match.group(2)      # the URL value
        quote = match.group(3)    # closing quote
        
        # Skip external links
        if url.startswith(('http://', 'https://', '//', 'mailto:', 'tel:', 'javascript:')):
            return match.group(0)
        
        # Skip non-HTML file references (CSS, JS, images, etc.)
        if any(url.endswith(ext) for ext in ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico', '.pdf', '.zip', '.exe']):
            return match.group(0)
        
        # Split URL from anchor/query
        anchor = ''
        if '#' in url:
            url, anchor = url.split('#', 1)
            anchor = '#' + anchor
        query = ''
        if '?' in url:
            url, query = url.split('?', 1)
            query = '?' + query
        
        # Only process .html URLs
        if not url.endswith('.html'):
            return match.group(0)
        
        # Handle index.html specially → "./" or "../lang/"
        if url == 'index.html':
            new_url = './' + anchor + query
        elif url.endswith('/index.html'):
            # e.g., "../ro/index.html" → "../ro/"
            new_url = url[:-len('index.html')] + anchor + query
        else:
            # e.g., "price.html" → "price", "blog/post.html" → "blog/post"
            new_url = url[:-len('.html')] + anchor + query
        
        return f'{prefix}{new_url}{quote}'
    
    # Match href="..." and href='...' patterns
    # Group 1: href=" or href='
    # Group 2: the URL
    # Group 3: closing quote
    pattern = r'''(href=["'])((?:(?!["']).)+)(["'])'''
    result = re.sub(pattern, replace_href, content)
    
    return result


def fix_action_links(content):
    """Also fix form action attributes if they have .html."""
    def replace_action(match):
        prefix = match.group(1)
        url = match.group(2)
        quote = match.group(3)
        
        if url.startswith(('http://', 'https://', '//')):
            return match.group(0)
        
        if url == 'index.html':
            return f'{prefix}./{quote}'
        elif url.endswith('/index.html'):
            return f'{prefix}{url[:-len("index.html")]}{quote}'
        elif url.endswith('.html'):
            return f'{prefix}{url[:-len(".html")]}{quote}'
        
        return match.group(0)
    
    pattern = r'''(action=["'])((?:(?!["']).)+)(["'])'''
    return re.sub(pattern, replace_action, content)


def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    
    modified = fix_html_links(original)
    modified = fix_action_links(modified)
    
    if modified != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified)
        
        # Count changes
        changes = sum(1 for a, b in zip(original.split('href='), modified.split('href=')) if a != b)
        return changes
    return 0


def main():
    total_files = 0
    total_changes = 0
    
    # Process all HTML files in en/, ro/, ru/ directories
    for lang in ['en', 'ro', 'ru']:
        lang_dir = os.path.join(DIR, lang)
        if not os.path.isdir(lang_dir):
            continue
        
        # Process all .html files (including blog subdirectories)
        for root, dirs, files in os.walk(lang_dir):
            for fname in files:
                if not fname.endswith('.html'):
                    continue
                filepath = os.path.join(root, fname)
                changes = process_file(filepath)
                if changes > 0:
                    rel = os.path.relpath(filepath, DIR)
                    print(f"  ✔ {rel}: {changes} links fixed")
                    total_changes += changes
                    total_files += 1
    
    # Also fix the root redirect page
    root_index = os.path.join(DIR, 'index.html')
    if os.path.exists(root_index):
        changes = process_file(root_index)
        if changes > 0:
            print(f"  ✔ index.html (root): {changes} links fixed")
            total_changes += changes
            total_files += 1
    
    # Fix 404 page
    page_404 = os.path.join(DIR, '404.html')
    if os.path.exists(page_404):
        changes = process_file(page_404)
        if changes > 0:
            print(f"  ✔ 404.html: {changes} links fixed")
            total_changes += changes
            total_files += 1

    print(f"\n{'='*50}")
    print(f"Done! Fixed {total_changes} links across {total_files} files.")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()
