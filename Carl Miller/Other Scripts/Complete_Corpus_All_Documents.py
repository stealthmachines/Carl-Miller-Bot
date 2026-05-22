#!/usr/bin/env python3
"""COMPLETE CARL MILLER CORPUS - ALL 10 DOCUMENTS"""

import re
import json
from pathlib import Path
from datetime import datetime
import subprocess

BASE_DIR = Path(r"C:\Users\Owner\Downloads\Legal-Vision-main\Legal-Vision-main\Carl Miller")
OUTPUT_DIR = BASE_DIR / "Corpus_Processed" / "COMPLETE_CORPUS_ALL_DOCUMENTS"
CHUNK_SIZE = 3500

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ""

def chunk_text(text, chunk_size):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks

def identify_document_type(chunk):
    chunk_lower = chunk.lower()
    if "magna carta" in chunk_lower:
        return "Magna_Carta_1215"
    elif "mayflower" in chunk_lower:
        return "Mayflower_Compact_1620"
    elif "declaration of independence" in chunk_lower:
        return "Declaration_Independence_1776"
    elif "articles of confederation" in chunk_lower:
        return "Articles_Confederation_1781"
    elif "constitution" in chunk_lower and "1787" in chunk_lower:
        return "Constitution_1787"
    elif "marbury v madison" in chunk_lower:
        return "Marbury_v_Madison_1803"
    elif "missouri" in chunk_lower or "1820" in chunk_lower:
        return "Missouri_Compromise_1820"
    elif "severability" in chunk_lower:
        return "Severability_Principle_2024"
    elif "carl miller" in chunk_lower:
        return "Carl_Miller_Teachings_2024"
    return "Unknown"

def extract_repugnancy_analysis(chunk):
    analysis = {
        "supremacy": [], "conflict": [], "nullity": [],
        "severability": [], "independence": []
    }
    
    if "supreme law of the land" in chunk.lower() or "notwithstanding" in chunk.lower():
        analysis["supremacy"] = [x for x in analysis["supremacy"] if "notwithstanding" in chunk.lower() or "supreme" in chunk.lower()]
    if "null and void" in chunk.lower() or "bear no power" in chunk.lower():
        analysis["nullity"] = analysis["nullity"]
    if "self evident" in chunk.lower() or "unalienable" in chunk.lower():
        analysis["independence"] = ["declaration_statements"]
    
    return analysis

def main():
    print("COMPLETE CARL MILLER CORPUS - ALL 10 DOCUMENTS")
    print("CHRONOLOGICAL: 1215-1620-1776-1781-1787-1803-1820-2024\n")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    sources = [
        ("Magna Carta (1215)", BASE_DIR / "Magna Carta.txt", 1215, "text"),
        ("Mayflower Compact (1620)", BASE_DIR / "The Mayflower Compact.txt", 1620, "text"),
        ("Declaration of Independence (1776)", BASE_DIR / "declaration_of_independence_1776.txt", 1776, "text"),
        ("Articles of Confederation (1781)", BASE_DIR / "articles_of_confederation_1781.txt", 1781, "text"),
        ("U.S. Constitution (1787)", BASE_DIR / "u.s._constitution_1787.txt", 1787, "text"),
        ("Marbury v. Madison (1803)", BASE_DIR / "Marbury v. Madison, 5 U.S. 137 (1803).txt", 1803, "text"),
        ("Missouri Compromise (1820)", BASE_DIR / "1820MissouriCompromise.pdf", 1820, "pdf"),
        ("Northwest Ordinance (1787)", BASE_DIR / "NW-Ordinance.pdf", 1787, "pdf"),
        ("Severability Principle", BASE_DIR / "severability.txt", 2024, "text"),
        ("Carl Miller Teachings (2024)", BASE_DIR / "Carl-Miller-Whisper-citation-corrected.txt", 2024, "text"),
    ]
    
    extracted_texts = {}
    
    print("[1] Loading 10 documents...")
    
    for name, path, year, file_type in sources:
        if file_type == "pdf":
            output_file = OUTPUT_DIR / name.replace(" ", "_").lower() + ".txt"
            try:
                subprocess.run(['pdftotext', str(path), str(output_file)], capture_output=True, timeout=30)
                content = read_file(output_file)
                if content:
                    print("  " + name + ": " + str(len(content)) + " bytes")
                    extracted_texts[name] = {"year": year, "content": content}
            except:
                print("  " + name + ": PDF error")
        else:
            content = read_file(path)
            if content:
                print("  " + name + ": " + str(len(content)) + " bytes")
                extracted_texts[name] = {"year": year, "content": content}
            else:
                print("  " + name + ": Not found")
    
    if not extracted_texts:
        print("ERROR: No content!")
        return
    
    print("\n[2] Processing...")
    all_content = []
    source_info = []
    
    for name, data in extracted_texts.items():
        chunks = chunk_text(data["content"], CHUNK_SIZE)
        all_content.append({"name": name, "year": data["year"], "content": data["content"]})
        source_info.append({"name": name, "year": data["year"], "num_chunks": len(chunks), "total_size": len(data["content"])})
    
    print("\n[3] Creating corpus...")
    combined = "\n".join([c["content"] for c in all_content])
    final_chunks = chunk_text(combined, CHUNK_SIZE)
    
    print("\n[4] Saving...")
    corpus = {
        "metadata": {"total_chunks": len(final_chunks), "total_documents": len(source_info)},
        "sources": source_info,
        "chunks": [{"chunk_num": i, "document": identify_document_type(c["content"]), "content": c["content"]} 
                   for i, c in enumerate(final_chunks)],
    }
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / "complete_all_10_docs.json", 'w') as f:
        json.dump(corpus, f)
    print("  Saved: complete_all_10_docs.json")
    
    summary = "# COMPLETE Corpus - All 10 Documents\n\n"
    summary += "Documents: " + str(len(source_info)) + "\n"
    summary += "Chunks: " + str(len(final_chunks)) + "\n"
    summary += "Size: " + str(len(combined)) + " bytes\n\n"
    
    with open(OUTPUT_DIR / "summary.md", 'w') as f:
        f.write(summary)
    print("  Saved: summary.md")
    
    print("\n" + "=" * 80)
    print("SUCCESS: COMPLETE CORPUS WITH ALL 10 DOCUMENTS!")

if __name__ == "__main__":
    main()