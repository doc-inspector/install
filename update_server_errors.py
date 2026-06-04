import re

file_path = r"E:\Website online and local app new project\Public2\Public\server.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """        # --- Package outputs into a zip ---
        import zipfile
        zip_path = job_dir / f"docinspector_results_{job_id[:8]}.zip"
        
        success_count = 0
        with zipfile.ZipFile(str(zip_path), "w", zipfile.ZIP_DEFLATED) as zf:
            for r in results:
                if r["status"] == "ok":
                    fp = out_dir / r["output"]
                    if fp.exists():
                        zf.write(str(fp), arcname=r["output"])
                        success_count += 1
                        
        if success_count > 0:"""

new_block = """        # --- Package outputs into a zip ---
        import zipfile
        zip_path = job_dir / f"docinspector_results_{job_id[:8]}.zip"
        
        success_count = 0
        with zipfile.ZipFile(str(zip_path), "w", zipfile.ZIP_DEFLATED) as zf:
            error_log = []
            for r in results:
                if r["status"] == "ok":
                    fp = out_dir / r["output"]
                    if fp.exists():
                        zf.write(str(fp), arcname=r["output"])
                        success_count += 1
                elif r["status"] == "error":
                    fp_err = in_dir / r["file"]
                    if fp_err.exists():
                        zf.write(str(fp_err), arcname=f"errors/{r['file']}")
                    error_log.append(f"File: {r['file']} - Error: {r['message']}")
            
            if error_log:
                err_log_path = job_dir / "error_log.txt"
                err_log_path.write_text("\\n".join(error_log), encoding="utf-8")
                zf.write(str(err_log_path), arcname="errors/error_log.txt")
                        
        if success_count > 0:"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated server.py successfully!")
else:
    print("Could not find the block to replace!")
