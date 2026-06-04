import re

server_py = r"E:\Website online and local app new project\Public2\Public\server.py"

with open(server_py, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace op_redact
old_redact = """def op_redact(in_path: Path, out_path: Path, options: dict):
    \"\"\"
    Find & redact keywords by flattening the PDF to image-only
    (true text-layer removal — visual redaction via Ghostscript).
    For a future version, coordinate-based redaction with pdftk/mutool
    can be implemented here.
    \"\"\"
    _require_tool(GS, "Ghostscript")
    # Flatten to image PDF removes all text vectors
    op_flatten(in_path, out_path)"""

# Handle potential CRLF
old_redact_crlf = old_redact.replace('\n', '\r\n')

new_redact = """def op_redact(in_path: Path, out_path: Path, options: dict):
    \"\"\"
    Find & redact keywords using PyMuPDF (fitz).
    It searches for the exact phrases and adds black rectangle redactions,
    removing the underlying text and vectors.
    \"\"\"
    keywords_raw = options.get("redactKeywords", "")
    keywords = [k.strip() for k in keywords_raw.split(',') if k.strip()]
    
    if not keywords:
        # If no keywords are provided, fallback to flatten to image
        op_flatten(in_path, out_path)
        return

    try:
        import fitz
    except ImportError:
        # Fallback if PyMuPDF is not installed
        op_flatten(in_path, out_path)
        return

    doc = fitz.open(str(in_path))
    for page in doc:
        for kw in keywords:
            text_instances = page.search_for(kw)
            for inst in text_instances:
                page.add_redact_annot(inst, fill=(0, 0, 0))
        # physically apply redactions to remove underlying text/images
        page.apply_redactions()

    doc.save(str(out_path), garbage=4, deflate=True)
    doc.close()"""

if old_redact in content:
    content = content.replace(old_redact, new_redact)
elif old_redact_crlf in content:
    content = content.replace(old_redact_crlf, new_redact)
elif "def op_redact" in content:
    # Use regex
    content = re.sub(r'def op_redact\(in_path: Path, out_path: Path, options: dict\):.*?op_flatten\(in_path, out_path\)', new_redact, content, flags=re.DOTALL)

with open(server_py, 'w', encoding='utf-8') as f:
    f.write(content)

# Update requirements.txt
req_file = r"E:\Website online and local app new project\Public2\Public\requirements.txt"
with open(req_file, 'r', encoding='utf-8') as f:
    req_content = f.read()

if "PyMuPDF" not in req_content and "pymupdf" not in req_content:
    with open(req_file, 'a', encoding='utf-8') as f:
        f.write("\nPyMuPDF==1.24.4\n")

print("Backend updated with PyMuPDF redaction!")
