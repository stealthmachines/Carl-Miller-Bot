#!/usr/bin/env python3
"""
Final Enhanced Corpus Processor
Integrates: Missouri Compromise (1820), Northwest Ordinance (1787), Severability Clause
Emphasis: REPUGNANCY DOCTRINE - "Any Thing in Constitution or Laws to the Contrary Notwithstanding"
"""

import re
import json
from pathlib import Path
from datetime import datetime
import subprocess

BASE_DIR = Path(r"C:\Users\Owner\Downloads\Legal-Vision-main\Legal-Vision-main\Carl Miller")
OUTPUT_DIR = BASE_DIR / "Corpus_Processed" / "FINAL_COMPLETE"
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
    
    if "missouri compromise" in chunk_lower or "1820" in chunk_lower:
        return "Missouri_Compromise_1820"
    elif "northwest ordinance" in chunk_lower or "territorial government" in chunk_lower:
        return "Northwest_Ordinance_1787"
    elif "severability" in chunk_lower:
        return "Severability_Principle"
    elif "declaration of independence" in chunk_lower or "july 4 1776" in chunk_lower:
        return "Declaration_Independence_1776"
    elif "articles of confederation" in chunk_lower:
        return "Articles_Confederation_1781"
    elif "constitution" in chunk_lower and "1787" in chunk_lower or "we the people" in chunk_lower:
        return "Constitution_1787"
    elif "marbury v madison" in chunk_lower:
        return "Marbury_v_Madison_1803"
    elif "magna carta" in chunk_lower:
        return "Magna_Carta_1215"
    elif "mayflower" in chunk_lower:
        return "Mayflower_Compact_1620"
    elif "carl miller" in chunk_lower:
        return "Carl_Miller_2024"
    else:
        return "Unknown"

def extract_repugnancy_analysis(chunk, doc_type):
    analysis = {
        "supremacy_statements": [],
        "conflict_statements": [],
        "nullity_claims": [],
        "historical_precedents": [],
        "severability_clauses": []
    }
    
    # Supremacy Clause patterns (Article 6)
    supremacy_patterns = [
        r"(?:supreme\s+law\s+of\s+the\s+land|anything\s+to\s+the\s+contrary\s+notwithstanding)",
        r"(?:judges\s+in\s+every\s+state\s+shall\s+be\s+bound\s+thereby|laws\s+of\s+united\s+states)",
        r"(?:treaties\s+made\s+under\s+authority\s+of\s+united\s+states)",
    ]
    
    # Conflict/Repugnancy patterns
    conflict_patterns = [
        r"(?:anything\s+in\s+constitution\s+or\s+laws\s+of\s+any\s+state\s+to\s+the\s+contrary\s+notwithstanding)",
        r"(?:conflict\s+with\s+supreme\s+law|in\s+conflict\s+notwithstanding|contrary\s+provisions)",
        r"(?:null\s+and\s+void|bear\s+no\s+power|bear\s+no\s+obligation)",
    ]
    
    # Severability patterns
    severability_patterns = [
        r"(?:severability\s+clause|severable\s+provisions|saving\s+provision|remaining\s+valid)",
        r"(?:if\s+any\s+provision\s+be\s+held\s+invalid|remainder\s+shall\s+continue\s+in\s+force)",
    ]
    
    # Missouri Compromise patterns
    missouri_patterns = [
        r"(?:missouri\s+compromise|1820|slavery\s+borders|territorial\s+acquisition)",
        r"(?:free\s+states|slave\s+states|balance\s+power)",
    ]
    
    # Northwest Ordinance patterns
    ordinance_patterns = [
        r"(?:northwest\s+ordinance|1787|territorial\s+government|enlightened\s+policy)",
        r"(?:no\s+question\s+of\s+slavery|civil\s+liberties|free\s+soil)",
    ]
    
    for pattern in supremacy_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["supremacy_statements"].extend(matches)
        except re.error:
            pass
    
    for pattern in conflict_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["conflict_statements"].extend(matches)
            analysis["nullity_claims"].extend(matches)
        except re.error:
            pass
    
    for pattern in severability_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["severability_clauses"].extend(matches)
        except re.error:
            pass
    
    for pattern in missouri_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["historical_precedents"].extend(matches)
        except re.error:
            pass
    
    for pattern in ordinance_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["historical_precedents"].extend(matches)
        except re.error:
            pass
    
    return analysis

def main():
    print("FINAL COMPLETE CORPUS PROCESSOR")
    print("=" * 70)
    print("ADDITIONAL: Missouri Compromise (1820) + Northwest Ordinance (1787) + Severability\n")
    print("CORE REPUGNANCY PRINCIPLE:")
    print('"This Constitution, and the Laws of the United States which shall be made in")')
    print('"Pursuance thereof; and all Treaties made, or which shall be made, under the")')
    print('"Authority of the United States, shall be the supreme Law of the Land; and the")')
    print('"Judges in every State shall be bound thereby, any Thing in the Constitution")')
    print('"or Laws of any State to the Contrary notwithstanding."')
    print("=" * 70)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Load all PDFs and text files
    print("[1] Extracting PDFs and reading text files...")
    
    all_sources = {
        # New additions
        "Missouri Compromise (1820)": (BASE_DIR / "1820MissouriCompromise.pdf", 1820, "pdf"),
        "Northwest Ordinance (1787)": (BASE_DIR / "NW-Ordinance.pdf", 1787, "pdf"),
        "Severability Principle": (BASE_DIR / "severability.txt", 2024, "text"),
        # Existing documents
        "Declaration of Independence (1776)": (BASE_DIR / "Declaration_Integrated/declaration_of_independence_1776.txt", 1776, "text"),
        "Articles of Confederation (1781)": (BASE_DIR / "Declaration_Integrated/articles_of_confederation_1781.txt", 1781, "text"),
        "U.S. Constitution (1787)": (BASE_DIR / "Declaration_Integrated/u.s._constitution_1787.txt", 1787, "text"),
        "Magna Carta (1215)": (BASE_DIR / "Magna Carta.txt", 1215, "text"),
        "Mayflower Compact (1620)": (BASE_DIR / "The Mayflower Compact.txt", 1620, "text"),
        "Marbury v. Madison (1803)": (BASE_DIR / "Marbury v. Madison, 5 U.S. 137 (1803).txt", 1803, "text"),
    }
    
    extracted_texts = {}
    
    for name, (path, year, file_type) in all_sources.items():
        if file_type == "pdf":
            output_file = OUTPUT_DIR / f"{name.replace(' ', '_').lower()}.txt"
            try:
                result = subprocess.run(
                    ['pdftotext', str(path), str(output_file)],
                    capture_output=True,
                    timeout=30
                )
                content = read_file(output_file) if output_file.exists() else ""
                print(f"    {name}: {len(content):,} bytes (extracted from PDF)")
            except Exception as e:
                print(f"    {name}: Error - {str(e)[:50]}")
                content = ""
        else:
            content = read_file(path)
            if content:
                print(f"    {name}: {len(content):,} bytes (text file)")
            else:
                print(f"    {name}: Empty or not found")
        
        if content:
            extracted_texts[name] = {"year": year, "content": content}
    
    if not extracted_texts:
        print("\nERROR: No content extracted!")
        return
    
    # Step 2: Process all sources
    print("\n[2] Processing all sources...")
    
    all_content = []
    source_info = []
    
    for name, data in extracted_texts.items():
        chunks = chunk_text(data["content"], CHUNK_SIZE)
        all_content.append({"name": name, "year": data["year"], "content": data["content"], "chunk_num": len(source_info)})
        source_info.append({"name": name, "year": data["year"], "num_chunks": len(chunks), "total_size": len(data["content"])})
        print(f"    {name}: {len(chunks)} chunks")
    
    # Step 3: Combine and chunk
    print("\n[3] Combining all sources...")
    combined_content = ""
    for source in all_content:
        combined_content += source["content"] + "\n"
    
    final_chunks = chunk_text(combined_content, CHUNK_SIZE)
    print(f"    Total chunks: {len(final_chunks)}")
    print(f"    Total size: {len(combined_content):,} bytes")
    
    # Step 4: Analyze repugnancy
    print("\n[4] Analyzing for REPUGNANCY DOCTRINE...")
    all_chunks_data = []
    repugnancy_stats = {
        "total_supremacy_statements": 0,
        "total_conflict_statements": 0,
        "total_nullity_claims": 0,
        "total_severability_clauses": 0,
        "total_historical_precedents": 0,
        "by_document": {}
    }
    
    for i, chunk in enumerate(final_chunks):
        doc_type = identify_document_type(chunk)
        analysis = extract_repugnancy_analysis(chunk, doc_type)
        
        chunk_data = {
            "chunk_num": i,
            "document": doc_type,
            "year": None,
            "content": chunk,
            "repugnancy_analysis": analysis,
            "word_count": len(chunk.split())
        }
        
        all_chunks_data.append(chunk_data)
        
        repugnancy_stats["total_supremacy_statements"] += len(analysis["supremacy_statements"])
        repugnancy_stats["total_conflict_statements"] += len(analysis["conflict_statements"])
        repugnancy_stats["total_nullity_claims"] += len(analysis["nullity_claims"])
        repugnancy_stats["total_severability_clauses"] += len(analysis["severability_clauses"])
        repugnancy_stats["total_historical_precedents"] += len(analysis["historical_precedents"])
        
        if doc_type not in repugnancy_stats["by_document"]:
            repugnancy_stats["by_document"][doc_type] = {
                "supremacy": 0, "conflict": 0, "nullity": 0, "severability": 0, "precedents": 0
            }
        repugnancy_stats["by_document"][doc_type]["supremacy"] += len(analysis["supremacy_statements"])
        repugnancy_stats["by_document"][doc_type]["conflict"] += len(analysis["conflict_statements"])
        repugnancy_stats["by_document"][doc_type]["nullity"] += len(analysis["nullity_claims"])
        repugnancy_stats["by_document"][doc_type]["severability"] += len(analysis["severability_clauses"])
        repugnancy_stats["by_document"][doc_type]["precedents"] += len(analysis["historical_precedents"])
    
    # Fill years
    chunk_index = {s["name"]: s["year"] for s in source_info}
    for chunk in all_chunks_data:
        chunk["year"] = chunk_index.get(chunk["document"], None)
    
    # Step 5: Create output files
    print("\n[5] Writing Final Complete Corpus...")
    
    corpus = {
        "metadata": {
            "processed_at": datetime.now().isoformat(),
            "emphasis": "REPUGNANCY DOCTRINE + SUPREMACY CLAUSE + SEVERABILITY",
            "chronological_order": True,
            "total_chunks": len(final_chunks),
            "total_documents": len(source_info),
            "core_principle": "Any Thing in Constitution or Laws to the Contrary Notwithstanding"
        },
        "sources": source_info,
        "chunks": all_chunks_data,
        "repugnancy_analysis": repugnancy_stats,
    }
    
    corpus_file = OUTPUT_DIR / "final_complete_corpus.json"
    with open(corpus_file, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
    print(f"    Saved: {corpus_file} ({corpus_file.stat().st_size:,} bytes)")
    
    # Summary
    summary = f"""# Final Complete Historical Corpus

## PROCESSING EMPHASIS
**REPUGNANCY DOCTRINE**: Any law conflicting with Supreme Law is NULL AND VOID FROM INCEPTION

**SUPREMACY CLAUSE** (Article 6, Paragraph 2):
> "This Constitution, and the Laws of the United States which shall be made in Pursuance thereof; and all Treaties made, or which shall be made, under the Authority of the United States, shall be the supreme Law of the Land; and the Judges in every State shall be bound thereby, any Thing in the Constitution or Laws of any State to the Contrary notwithstanding."

**SEVERABILITY PRINCIPLE**:
> If any provision is held invalid, the remainder shall continue in force

## CHRONOLOGICAL DOCUMENTS (1215-1787-1803-1820-2024)

"""
    for source in source_info:
        summary += f"- {source['name']} ({source['year']}): {source['num_chunks']} chunks, {source['total_size']:,} bytes\n"
    
    summary += f"""
## REPUGNANCY STATISTICS

**Overall:**
- Supremacy Statements: {repugnancy_stats['total_supremacy_statements']}
- Conflict Statements: {repugnancy_stats['total_conflict_statements']}
- Nullity Claims: {repugnancy_stats['total_nullity_claims']}
- Severability Clauses: {repugnancy_stats['total_severability_clauses']}
- Historical Precedents: {repugnancy_stats['total_historical_precedents']}

**By Document:**
"""
    for doc, stats in repugnancy_stats["by_document"].items():
        summary += f"- {doc}:\n  - Supremacy: {stats['supremacy']}, Conflict: {stats['conflict']}, Nullity: {stats['nullity']}, Severability: {stats['severability']}, Precedents: {stats['precedents']}\n"
    
    with open(OUTPUT_DIR / "final_summary.md", 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"    Saved: {OUTPUT_DIR / 'final_summary.md'}")
    
    print("\n" + "=" * 70)
    print("SUCCESS: FINAL COMPLETE CORPUS READY!")
    print(f"Total documents: {len(source_info)}")
    print(f"Total chunks: {len(final_chunks)}")
    print(f"Total size: {len(combined_content):,} bytes")

if __name__ == "__main__":
    main()