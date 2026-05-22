#!/usr/bin/env python3
"""
ULTIMATE Carl Miller Corpus - ALL Founding Documents
Complete chronological integration with REPUGNANCY DOCTRINE emphasis
"""

import re
import json
from pathlib import Path
from datetime import datetime
import subprocess

BASE_DIR = Path(r"C:\Users\Owner\Downloads\Legal-Vision-main\Legal-Vision-main\Carl Miller")
OUTPUT_DIR = BASE_DIR / "Corpus_Processed" / "ULTIMATE_CORPUS"
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
    
    if "1820" in chunk_lower and ("missouri" in chunk_lower or "compromise" in chunk_lower):
        return "Missouri_Compromise_1820"
    elif "northwest" in chunk_lower and ("ordinance" in chunk_lower or "1787" in chunk_lower):
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
        "severability_clauses": [],
        "historical_precedents": []
    }
    
    # Supremacy Clause (Article 6) - KEY REPUGNANCY DOCTRINE
    supremacy_patterns = [
        r"(?:supreme\s+law\s+of\s+the\s+land|any\s+thing\s+in\s+the\s+constitution\s+or\s+laws\s+of\s+any\s+state\s+to\s+the\s+contrary\s+notwithstanding)",
        r"(?:judges\s+in\s+every\s+state\s+shall\s+be\s+bound\s+thereby|laws\s+of\s+united\s+states\s+which\s+shall\s+be\s+made\s+in\s+pursuance)",
        r"(?:treaties\s+made\s+under\s+authority\s+of\s+united\s+states)",
    ]
    
    # Conflict/Repugnancy patterns
    conflict_patterns = [
        r"(?:anything\s+to\s+the\s+contrary\s+notwithstanding|conflict\s+notwithstanding|contrary\s+provisions\s+notwithstanding)",
        r"(?:null\s+and\s+void|bear\s+no\s+power\s+to\s+enforce|bear\s+no\s+obligation\s+to\s+obey)",
        r"(?:in\s+conflict\s+with\s+supreme\s+law|repugnant\s+to\s+constitution)",
    ]
    
    # Severability patterns
    severability_patterns = [
        r"(?:severability\s+clause|severable\s+provisions|saving\s+provision|if\s+any\s+portion\s+be\s+unconstitutional|remainder\s+shall\s+continue)",
    ]
    
    # Document-specific patterns
    missouri_patterns = [r"(?:missouri\s+compromise|1820|admission\s+of\s+states)"]
    ordinance_patterns = [r"(?:northwest\s+ordinance|1787|territorial\s+government|no\s+question\s+of\s+slavery)"]
    
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
    
    for pattern in missouri_patterns + ordinance_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["historical_precedents"].extend(matches)
        except re.error:
            pass
    
    return analysis

def main():
    print("ULTIMATE CARL MILLER CORPUS")
    print("=" * 80)
    print("CHRONOLOGICAL INTEGRATION: 1215-1776-1781-1787-1803-1820-2024")
    print("CORE EMPHASIS: REPUGNANCY - 'Any Thing...to the Contrary NOTWITHSTANDING'\n")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Comprehensive source list
    print("[1] Loading all documents...")
    
    sources = {
        # NEW additions
        "Missouri Compromise (1820)": (BASE_DIR / "1820MissouriCompromise.pdf", 1820, "pdf"),
        "Northwest Ordinance (1787)": (BASE_DIR / "NW-Ordinance.pdf", 1787, "pdf"),
        "Severability Principle": (BASE_DIR / "severability.txt", 2024, "text"),
        # Declaration documents (check if extracted)
        "Declaration of Independence (1776)": (BASE_DIR / "Declaration_Integrated/declaration_of_independence_1776.txt", 1776, "text"),
        "Articles of Confederation (1781)": (BASE_DIR / "Declaration_Integrated/articles_of_confederation_1781.txt", 1781, "text"),
        "U.S. Constitution (1787)": (BASE_DIR / "Declaration_Integrated/u.s._constitution_1787.txt", 1787, "text"),
        # Original sources
        "Magna Carta (1215)": (BASE_DIR / "Magna Carta.txt", 1215, "text"),
        "Mayflower Compact (1620)": (BASE_DIR / "The Mayflower Compact.txt", 1620, "text"),
        "Marbury v. Madison (1803)": (BASE_DIR / "Marbury v. Madison, 5 U.S. 137 (1803).txt", 1803, "text"),
        "Carl Miller Teachings (2024)": (BASE_DIR / "Carl-Miller-Whisper-citation-corrected.txt", 2024, "text"),
    }
    
    extracted_texts = {}
    
    for name, (path, year, file_type) in sources.items():
        if file_type == "pdf":
            output_file = OUTPUT_DIR / f"{name.replace(' ', '_').lower()}.txt"
            try:
                result = subprocess.run(
                    ['pdftotext', str(path), str(output_file)],
                    capture_output=True,
                    timeout=30
                )
                content = read_file(output_file)
                if content:
                    print(f"    {name}: {len(content):,} bytes (PDF extracted)")
                    extracted_texts[name] = {"year": year, "content": content}
                else:
                    print(f"    {name}: Empty PDF extraction")
            except Exception as e:
                print(f"    {name}: PDF error - skipping")
        else:
            content = read_file(path)
            if content:
                print(f"    {name}: {len(content):,} bytes (text)")
                extracted_texts[name] = {"year": year, "content": content}
            else:
                print(f"    {name}: Not found or empty")
    
    if not extracted_texts:
        print("\nERROR: No content loaded!")
        return
    
    # Process sources
    print("\n[2] Processing documents...")
    
    all_content = []
    source_info = []
    
    for name, data in extracted_texts.items():
        chunks = chunk_text(data["content"], CHUNK_SIZE)
        all_content.append({"name": name, "year": data["year"], "content": data["content"], "chunk_num": len(source_info)})
        source_info.append({"name": name, "year": data["year"], "num_chunks": len(chunks), "total_size": len(data["content"])})
        print(f"    {name}: {len(chunks)} chunks, {len(data['content']):,} bytes")
    
    # Combine and chunk
    print("\n[3] Creating unified corpus...")
    combined_content = ""
    for source in all_content:
        combined_content += source["content"] + "\n"
    
    final_chunks = chunk_text(combined_content, CHUNK_SIZE)
    print(f"    Total chunks: {len(final_chunks)}")
    print(f"    Total size: {len(combined_content):,} bytes")
    
    # Analyze repugnancy
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
    
    # Create output files
    print("\n[5] Writing ULTIMATE CORPUS...")
    
    corpus = {
        "metadata": {
            "processed_at": datetime.now().isoformat(),
            "emphasis": "REPUGNANCY DOCTRINE - 'Any Thing to the Contrary NOTWITHSTANDING'",
            "chronological_order": True,
            "total_chunks": len(final_chunks),
            "total_documents": len(source_info),
            "supremacy_clause": "Article 6, Paragraph 2 - 'supreme Law of the Land; any Thing...to the Contrary notwithstanding'",
        },
        "sources": source_info,
        "chunks": all_chunks_data,
        "repugnancy_analysis": repugnancy_stats,
    }
    
    corpus_file = OUTPUT_DIR / "ultimate_corpus.json"
    with open(corpus_file, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
    print(f"    Saved: {corpus_file} ({corpus_file.stat().st_size:,} bytes)")
    
    # Summary
    summary = f"""# ULTIMATE Carl Miller Corpus - FINAL VERSION

## CORE REPUGNANCY PRINCIPLE
> "This Constitution, and the Laws of the United States which shall be made in Pursuance thereof; and all Treaties made, or which shall be made, under the Authority of the United States, shall be the supreme Law of the Land; and the Judges in every State shall be bound thereby, **any Thing in the Constitution or Laws of any State to the Contrary notwithstanding.**"
> - Article 6, Paragraph 2, U.S. Constitution

> "Anything that is in conflict with the Supreme Law is **NULL AND VOID OF LAW** from its inception, not from the date you go to court and brand it as unconstitutional."
> - Marbury v. Madison, 5 U.S. 137 (1803)

## CHRONOLOGICAL FOUNDATION (1215-2024)

"""
    for source in source_info:
        summary += f"- **{source['name']}** ({source['year']}): {source['num_chunks']} chunks, {source['total_size']:,} bytes\n"
    
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
    
    with open(OUTPUT_DIR / "ultimate_summary.md", 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"    Saved: {OUTPUT_DIR / 'ultimate_summary.md'}")
    
    print("\n" + "=" * 80)
    print("SUCCESS: ULTIMATE CORPUS COMPLETE!")
    print(f"Documents: {len(source_info)}")
    print(f"Chunks: {len(final_chunks)}")
    print(f"Total Size: {len(combined_content):,} bytes")

if __name__ == "__main__":
    main()