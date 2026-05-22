#!/usr/bin/env python3
"""
Extract Declaration of Independence, Articles, and Constitution from PDFs
Then integrate into enhanced corpus with full REPUGNANCY analysis
"""

import re
import json
from pathlib import Path
from datetime import datetime
import subprocess

BASE_DIR = Path(r"C:\Users\Owner\Downloads\Legal-Vision-main\Legal-Vision-main\Carl Miller")
OUTPUT_DIR = BASE_DIR / "Corpus_Processed" / "DECLARATION_INTEGRATED"
CHUNK_SIZE = 3500

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
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
    
    if "declaration of independence" in chunk_lower or "july 4 1776" in chunk_lower:
        return "Declaration_of_Independence_1776"
    elif "articles of confederation" in chunk_lower or "confederation" in chunk_lower:
        return "Articles_of_Confederation_1781"
    elif "constitution" in chunk_lower and "1787" in chunk_lower:
        return "Constitution_1787"
    elif "marbury v madison" in chunk_lower or "chief justice marshall" in chunk_lower:
        return "Marbury_v_Madison_1803"
    elif "magna carta" in chunk_lower:
        return "Magna_Carta_1215"
    elif "mayflower" in chunk_lower:
        return "Mayflower_Compact_1620"
    elif "carl miller" in chunk_lower:
        return "Carl_Miller_Teachings"
    else:
        return "Unknown"

def extract_repugnancy_analysis(chunk, doc_type):
    analysis = {
        "independence_statements": [],
        "conflict_statements": [],
        "supremacy_claims": [],
        "historical_precedents": [],
        "legal_principles": []
    }
    
    # Declaration of Independence patterns
    independence_patterns = [
        r"(?:self-evident|unalienable\s+Rights|life|liberty|pursuit\s+of\s+happiness|consent\s+of\s+the\s+governed)",
        r"(?:declaration\s+of\s+independence|july\s+4|thirteen\s+united\s+states)",
    ]
    
    # Articles of Confederation patterns
    articles_patterns = [
        r"(?:articles\s+of\s+confederation|perpetual\s+Union|general\s+committee|federallig)",
        r"(?:delegates|states\s+retaining\s+their\s+sovereignty|each\state\ has\ a\ vote)",
    ]
    
    # Constitution patterns
    constitution_patterns = [
        r"(?:constitution\s+of\s+united\s+states|1787|supreme\s+law|supremacy\s+clause)",
        r"(?:we\s+the\s+people|establish\s+justice|insure\s+domestic\s+tranquility|common\s+defence)",
    ]
    
    # Marbury patterns
    marbury_patterns = [
        r"(?:anything\s+that\s+is\s+in\s+conflict\s+is\s+null\s+and\s+void\s+of\s+law|supreme\s+law\s+would\s+prevail)",
        r"(?:null\s+and\s+void\s+of\s+law|bear\s+no\s+power\s+to\s+enforce|bear\s+no\s+obligation\s+to\s+obey)",
    ]
    
    for pattern in independence_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["independence_statements"].extend(matches)
        except re.error:
            pass
    
    for pattern in articles_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["historical_precedents"].extend(matches)
        except re.error:
            pass
    
    for pattern in constitution_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["supremacy_claims"].extend(matches)
        except re.error:
            pass
    
    for pattern in marbury_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["conflict_statements"].extend(matches)
        except re.error:
            pass
    
    return analysis

def main():
    print("DECLARATION INTEGRATED CORPUS PROCESSOR")
    print("=" * 70)
    print("INTEGRATING: Declaration (1776) + Articles (1781) + Constitution (1787)\n")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Extract PDFs
    print("[1] Extracting PDFs to text...")
    
    pdf_sources = {
        "Declaration of Independence (1776)": (BASE_DIR / "decind.pdf", 1776),
        "Articles of Confederation (1781)": (BASE_DIR / "articles.pdf", 1781),
        "U.S. Constitution (1787)": (BASE_DIR / "const.pdf", 1787),
    }
    
    extracted_texts = {}
    
    for name, (pdf_path, year) in pdf_sources.items():
        output_file = OUTPUT_DIR / f"{name.replace(' ', '_').lower().replace('(', '').replace(')', '')}.txt"
        
        try:
            result = subprocess.run(
                ['pdftotext', '-layout', str(pdf_path), str(output_file)],
                capture_output=True,
                timeout=30
            )
            
            if output_file.exists():
                content = read_file(output_file)
                if content:
                    extracted_texts[name] = {"year": year, "content": content}
                    print(f"    {name}: {len(content):,} bytes, {content.count(chr(10))+content.count(chr(13))} lines")
                else:
                    print(f"    {name}: Empty extraction")
            else:
                print(f"    {name}: File not created")
        except Exception as e:
            print(f"    {name}: Error - {str(e)[:100]}")
    
    if not extracted_texts:
        print("\nERROR: No PDFs extracted successfully!")
        return
    
    # Step 2: Load all sources
    print("\n[2] Loading all sources...")
    
    all_content = []
    source_info = []
    
    # Add extracted documents
    for name, data in extracted_texts.items():
        all_content.append({"name": name, "year": data["year"], "content": data["content"], "chunk_num": len(source_info)})
        chunks = chunk_text(data["content"], CHUNK_SIZE)
        source_info.append({"name": name, "year": data["year"], "num_chunks": len(chunks), "total_size": len(data["content"])})
        print(f"    {name}: {len(chunks)} chunks, {len(data['content']):,} bytes")
    
    # Add existing documents
    existing_sources = {
        "Magna Carta (1215)": (BASE_DIR / "Magna Carta.txt", 1215),
        "Mayflower Compact (1620)": (BASE_DIR / "The Mayflower Compact.txt", 1620),
        "Marbury v. Madison (1803)": (BASE_DIR / "Marbury v. Madison, 5 U.S. 137 (1803).txt", 1803),
    }
    
    for name, (path, year) in existing_sources.items():
        if path.exists():
            content = read_file(path)
            if content:
                all_content.append({"name": name, "year": year, "content": content, "chunk_num": len(source_info)})
                chunks = chunk_text(content, CHUNK_SIZE)
                source_info.append({"name": name, "year": year, "num_chunks": len(chunks), "total_size": len(content)})
                print(f"    {name}: {len(chunks)} chunks, {len(content):,} bytes")
    
    # Add Carl Miller
    transcript_path = BASE_DIR / "Carl-Miller-Whisper-citation-corrected.txt"
    if transcript_path.exists():
        content = read_file(transcript_path)
        all_content.append({"name": "Carl Miller Teachings", "year": 2024, "content": content, "chunk_num": len(source_info)})
        chunks = chunk_text(content, CHUNK_SIZE)
        source_info.append({"name": "Carl Miller Teachings", "year": 2024, "num_chunks": len(chunks), "total_size": len(content)})
        print(f"    Carl Miller: {len(chunks)} chunks, {len(content):,} bytes")
    
    # Step 3: Combine and chunk
    print("\n[3] Combining all sources...")
    combined_content = ""
    for source in all_content:
        combined_content += source["content"] + "\n"
    
    final_chunks = chunk_text(combined_content, CHUNK_SIZE)
    print(f"    Total chunks: {len(final_chunks)}")
    print(f"    Total size: {len(combined_content):,} bytes")
    
    # Step 4: Process chunks
    print("\n[4] Analyzing for REPUGNANCY...")
    all_chunks_data = []
    repugnancy_stats = {
        "total_independence_statements": 0,
        "total_conflict_statements": 0,
        "total_supremacy_claims": 0,
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
        
        repugnancy_stats["total_independence_statements"] += len(analysis["independence_statements"])
        repugnancy_stats["total_conflict_statements"] += len(analysis["conflict_statements"])
        repugnancy_stats["total_supremacy_claims"] += len(analysis["supremacy_claims"])
        repugnancy_stats["total_historical_precedents"] += len(analysis["historical_precedents"])
        
        if doc_type not in repugnancy_stats["by_document"]:
            repugnancy_stats["by_document"][doc_type] = {
                "independence": 0, "conflict": 0, "supremacy": 0, "precedents": 0
            }
        repugnancy_stats["by_document"][doc_type]["independence"] += len(analysis["independence_statements"])
        repugnancy_stats["by_document"][doc_type]["conflict"] += len(analysis["conflict_statements"])
        repugnancy_stats["by_document"][doc_type]["supremacy"] += len(analysis["supremacy_claims"])
        repugnancy_stats["by_document"][doc_type]["precedents"] += len(analysis["historical_precedents"])
    
    # Fill years
    chunk_index = {s["name"]: s["year"] for s in source_info}
    for chunk in all_chunks_data:
        chunk["year"] = chunk_index.get(chunk["document"], None)
    
    # Step 5: Create output files
    print("\n[5] Writing corpus...")
    
    corpus = {
        "metadata": {
            "processed_at": datetime.now().isoformat(),
            "emphasis": "REPUGNANCY DOCTRINE + DECLARATION OF INDEPENDENCE",
            "chronological_order": True,
            "total_chunks": len(all_chunks_data),
            "total_documents": len(source_info),
        },
        "sources": source_info,
        "chunks": all_chunks_data,
        "repugnancy_analysis": repugnancy_stats,
    }
    
    corpus_file = OUTPUT_DIR / "declaration_integrated_corpus.json"
    with open(corpus_file, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
    print(f"    Saved: {corpus_file} ({corpus_file.stat().st_size:,} bytes)")
    
    # Summary
    summary = f"""# Declaration Integrated Corpus

## PROCESSING EMPHASIS
**REPUGNANCY**: Conflict with Supreme Law = NULL AND VOID FROM INCEPTION

## CHRONOLOGICAL DOCUMENTS (1215-1776-1781-1787-1803-2024)

"""
    for source in source_info:
        summary += f"- {source['name']} ({source['year']}): {source['num_chunks']} chunks, {source['total_size']:,} bytes\n"
    
    summary += f"""
## REPUGNANCY STATISTICS

**Overall:**
- Independence Statements: {repugnancy_stats['total_independence_statements']}
- Conflict Statements: {repugnancy_stats['total_conflict_statements']}
- Supremacy Claims: {repugnancy_stats['total_supremacy_claims']}
- Historical Precedents: {repugnancy_stats['total_historical_precedents']}

**By Document:**
"""
    for doc, stats in repugnancy_stats["by_document"].items():
        summary += f"- {doc}: {stats['independence']} independence, {stats['conflict']} conflict, {stats['supremacy']} supremacy, {stats['precedents']} precedents\n"
    
    with open(OUTPUT_DIR / "declaration_summary.md", 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"    Saved: {OUTPUT_DIR / 'declaration_summary.md'}")
    
    print("\n" + "=" * 70)
    print("SUCCESS: DECLARATION INTEGRATED CORPUS COMPLETE!")
    print(f"Total documents: {len(source_info)}")
    print(f"Total chunks: {len(all_chunks_data)}")

if __name__ == "__main__":
    main()