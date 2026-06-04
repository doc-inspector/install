import re

file_path = r"E:\Website online and local app new project\Public2\Public\server.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the operations parsing block
old_block = """    try:
        operations = json.loads(request.form.get("operations", "[]"))
    except Exception:
        return jsonify({"error": "Invalid operations JSON."}), 400

    if not operations:
        return jsonify({"error": "No operations selected."}), 400"""

new_block = """    try:
        operations = json.loads(request.form.get("operations", "[]"))
    except Exception:
        return jsonify({"error": "Invalid operations JSON."}), 400

    if not operations:
        return jsonify({"error": "No operations selected."}), 400
        
    # Remove duplicate flatten if redact is present (since redact does flattening anyway)
    if "redact" in operations and "flatten" in operations:
        operations.remove("flatten")
        
    # Enforce logical execution order
    ORDER = {
        "rebuild": 1,
        "redact": 2,
        "flatten": 3,
        "watermark": 4,
        "sanitize": 5,
        "encrypt": 6
    }
    operations = sorted(operations, key=lambda x: ORDER.get(x, 99))"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched server.py successfully!")
else:
    print("ERROR: old_block not found in server.py")
