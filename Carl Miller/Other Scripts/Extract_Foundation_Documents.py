#!/usr/bin/env python3
"""Extract all foundation PDFs and create COMPLETE corpus"""

from pathlib import Path
import subprocess

BASE_DIR = Path(r"C:\Users\Owner\Downloads\Legal-Vision-main\Legal-Vision-main\Carl Miller")

pdf_files = {
    "Declaration of Independence (1776)": BASE_DIR / "decind.pdf",
    "Articles of Confederation (1781)": BASE_DIR / "articles.pdf",
    "U.S. Constitution (1787)": BASE_DIR / "const.pdf",
}

print("=== EXTRACTING FOUNDATION DOCUMENTS ===\n")

extracted = {}

for name, pdf_path in pdf_files.items():
    if pdf_path.exists():
        output_file = BASE_DIR / f"{name.replace(' ', '_').lower().replace('(', '').replace(')', '').replace('/', '_')}.txt"
        print("Extracting: " + name + "...")
        
        try:
            result = subprocess.run(
                ['pdftotext', '-layout', str(pdf_path), str(output_file)],
                capture_output=True,
                timeout=30
            )
            
            if output_file.exists():
                size = output_file.stat().st_size
                print("  SUCCESS: " + name)
                print("    Saved: " + output_file.name)
                print("    Size: " + str(size) + " bytes")
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                extracted[name] = {"year": 1776 if "Declaration" in name or "1776" in name else 1781, "content": content, "size": size}
            else:
                print("  FAILED: File not created")
        except Exception as e:
            print("  ERROR: " + str(e)[:80])
    else:
        print(name + ": PDF not found")
    print()

print("=== SUMMARY ===")
print("Total extracted: " + str(len(extracted)))
for name, data in extracted.items():
    print("  " + name + ": " + str(data["size"]) + " bytes")
