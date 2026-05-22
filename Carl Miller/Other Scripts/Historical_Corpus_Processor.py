#!/usr/bin/env python3
"""
Carl Miller Full Historical Corpus Processor
Merges founding documents with Carl Miller teachings
Emphasizes: REPUGNANCY (conflict = null and void from inception)
"""

import re
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"C:\Users\Owner\Downloads\Legal-Vision-main\Legal-Vision-main\Carl Miller")
OUTPUT_DIR = BASE_DIR / "Corpus_Processed" / "HISTORICAL"

CHUNK_SIZE = 3000  # Smaller chunks for detailed analysis

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
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
    """Identify which historical document a chunk comes from"""
    chunk_lower = chunk.lower()
    
    if "john by the grace of god king of england" in chunk_lower:
        return "Magna_Carta"
    elif "mayflower compact" in chunk_lower or "covenant and combine ourselves" in chunk_lower:
        return "Mayflower_Compact"
    elif "carl miller" in chunk_lower or "violate your rights" in chunk_lower:
        return "Carl_Miller"
    else:
        return "Unknown"

def extract_repugnancy_concepts(chunk):
    """Extract repugnancy/conflict concepts"""
    concepts = {
        "repugnancy_mentions": [],
        "conflict_statements": [],
        "supremacy_claims": [],
        "historical_precedents": []
    }
    
    # Repugnancy patterns (key Carl Miller principle)
    repugnancy_patterns = [
        r"(?:repugnant|repugnancy|in\s+conflict|conflict\s+with|contrary\s+to|null\s+and\s+void|unconstitutional)",
        r"(?:supreme\s+law|supremacy\s+clause|article\s+\d+",
        r"(?:conflict\s+creates|nullity|does\s+not\s+exist|never\s+existed)",
    ]
    
    for pattern in repugnancy_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            concepts["repugnancy_mentions"].extend(matches)
        except re.error:
            pass  # Skip invalid patterns
    
    # Historical precedents
    historical_patterns = [
        r"(?:King\s+John|Magna\s+Carta|1215|1620|Mayflower|Pilgrims|colonists|covenant|compact)",
        r"(?:barons|twenty-five\s+barons|judgment\s+of\s+his\s+equals|law\s+of\s+the\s+land)",
    ]
    
    for pattern in historical_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            concepts["historical_precedents"].extend(matches)
        except re.error:
            pass
    
    return concepts

def main():
    print("Carl Miller Historical Corpus Processor")
    print("=" * 60)
    print("Emphasis: REPUGNANCY - Conflict = Null and Void from Inception\n")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Read all source files in chronological order
    print("[1] Reading Founding Documents (Chronological Order)...")
    
    sources = {
        "Magna Carta": (BASE_DIR / "Magna Carta.txt", 1215),
        "Mayflower Compact": (BASE_DIR / "The Mayflower Compact.txt", 1620),
    }
    
    all_content = []
    source_info = []
    
    for name, (path, year) in sources.items():
        if path.exists():
            content = read_file(path)
            if content:
                all_content.append({
                    "name": name,
                    "year": year,
                    "content": content,
                    "chunk_num": len(source_info)
                })
                chunks = chunk_text(content, CHUNK_SIZE)
                source_info.append({
                    "name": name,
                    "year": year,
                    "num_chunks": len(chunks),
                    "total_size": len(content)
                })
                print(f"    {name} ({year}): {len(chunks)} chunks, {len(content):,} bytes")
    
    # Add Carl Miller transcript (modern application of principles)
    print("\n[2] Adding Carl Miller Teachings (Modern Application)...")
    transcript_path = BASE_DIR / "Carl-Miller-Whisper-citation-corrected.txt"
    if transcript_path.exists():
        content = read_file(transcript_path)
        all_content.append({
            "name": "Carl Miller Transcript",
            "year": 2024,
            "content": content,
            "chunk_num": len(source_info)
        })
        chunks = chunk_text(content, CHUNK_SIZE)
        source_info.append({
            "name": "Carl Miller Transcript",
            "year": 2024,
            "num_chunks": len(chunks),
            "total_size": len(content)
        })
        print(f"    Carl Miller Transcript: {len(chunks)} chunks, {len(content):,} bytes")
    
    # Combine and chunk
    print("\n[3] Combining All Sources...")
    combined_content = ""
    for source in all_content:
        combined_content += source["content"] + "\n"
    
    final_chunks = chunk_text(combined_content, CHUNK_SIZE)
    print(f"    Total chunks: {len(final_chunks)}")
    print(f"    Total size: {len(combined_content):,} bytes")
    
    # Process each chunk
    print("\n[4] Analyzing for REPUGNANCY Principles...")
    all_chunks_data = []
    repugnancy_stats = {
        "total_repugnancy_mentions": 0,
        "total_conflict_statements": 0,
        "total_historical_precedents": 0,
        "by_document": {}
    }
    
    for i, chunk in enumerate(final_chunks):
        document_type = identify_document_type(chunk)
        concepts = extract_repugnancy_concepts(chunk)
        
        chunk_data = {
            "chunk_num": i,
            "document": document_type,
            "year": None,
            "content": chunk,
            "repugnancy_analysis": concepts,
            "word_count": len(chunk.split())
        }
        
        all_chunks_data.append(chunk_data)
        
        # Aggregate stats
        repugnancy_stats["total_repugnancy_mentions"] += len(concepts["repugnancy_mentions"])
        repugnancy_stats["total_conflict_statements"] += len(concepts["conflict_statements"])
        repugnancy_stats["total_historical_precedents"] += len(concepts["historical_precedents"])
        
        # Track by document
        if document_type not in repugnancy_stats["by_document"]:
            repugnancy_stats["by_document"][document_type] = {
                "mentions": 0,
                "precedents": 0
            }
        repugnancy_stats["by_document"][document_type]["mentions"] += len(concepts["repugnancy_mentions"])
        repugnancy_stats["by_document"][document_type]["precedents"] += len(concepts["historical_precedents"])
    
    # Fill in year information
    chunk_index = {}
    for source in source_info:
        chunk_index[source["name"]] = {"start": 0, "end": source["num_chunks"] - 1}
    
    for i, chunk in enumerate(all_chunks_data):
        document = chunk["document"]
        if document in chunk_index:
            chunk["year"] = [
                s["year"] for s in source_info 
                if s["name"] == document
            ][0]
    
    # Create topic index
    print("\n[5] Building Topic Index...")
    topics = {
        "Historical_Founding_Documents": [],
        "Repugnancy_Principles": [],
        "Contract_Theory": [],
        "Supremacy_Clause": [],
        "Laches_Timely_Action": [],
        "Common_Law_Principles": []
    }
    
    for chunk in all_chunks_data:
        if chunk["document"] in ["Magna_Carta", "Mayflower_Compact"]:
            topics["Historical_Founding_Documents"].append(chunk)
        elif "repugnant" in chunk["content"].lower() or "conflict" in chunk["content"].lower():
            topics["Repugnancy_Principles"].append(chunk)
        elif "contract" in chunk["content"].lower() or "ironclad" in chunk["content"].lower():
            topics["Contract_Theory"].append(chunk)
        elif "article 6" in chunk["content"].lower() or "supreme law" in chunk["content"].lower():
            topics["Supremacy_Clause"].append(chunk)
        elif "laches" in chunk["content"].lower() or "timely" in chunk["content"].lower():
            topics["Laches_Timely_Action"].append(chunk)
        else:
            topics["Common_Law_Principles"].append(chunk)
    
    print(f"    Topics: {list(topics.keys())}")
    for topic, chunks in topics.items():
        print(f"      - {topic}: {len(chunks)} chunks")
    
    # Create output files
    print("\n[6] Writing Historical Corpus...")
    
    historical_corpus = {
        "metadata": {
            "processed_at": datetime.now().isoformat(),
            "emphasis": "REPUGNANCY - Conflict = Null and Void from Inception",
            "chronological_order": True,
            "total_chunks": len(all_chunks_data),
            "total_documents": len(source_info),
        },
        "sources": source_info,
        "chunks": all_chunks_data,
        "topics": topics,
        "repugnancy_analysis": repugnancy_stats,
    }
    
    corpus_file = OUTPUT_DIR / "historical_corpus.json"
    with open(corpus_file, 'w', encoding='utf-8') as f:
        json.dump(historical_corpus, f, indent=2, ensure_ascii=False)
    print(f"    Saved: {corpus_file} ({corpus_file.stat().st_size:,} bytes)")
    
    repugnancy_file = OUTPUT_DIR / "repugnancy_analysis.json"
    with open(repugnancy_file, 'w', encoding='utf-8') as f:
        json.dump(repugnancy_stats, f, indent=2, ensure_ascii=False)
    print(f"    Saved: {repugnancy_file}")
    
    summary = f"""# Carl Miller Historical Corpus - Repugnancy Analysis

## Processing Emphasis
**REPUGNANCY**: Any law/contract in conflict with supreme authority is **NULL AND VOID FROM INCEPTION**

## Founding Documents (Chronological Order)
"""
    
    for source in source_info:
        summary += f"- **{source['name']}** ({source['year']}): {source['num_chunks']} chunks, {source['total_size']:,} bytes\n"
    
    summary += f"""
## Repugnancy Statistics
- **Total Repugnancy Mentions**: {repugnancy_stats['total_repugnancy_mentions']}
- **Total Conflict Statements**: {repugnancy_stats['total_conflict_statements']}
- **Total Historical Precedents**: {repugnancy_stats['total_historical_precedents']}

## By Document Type
"""
    
    for doc, stats in repugnancy_stats["by_document"].items():
        summary += f"- {doc}: {stats['mentions']} repugnancy mentions, {stats['precedents']} precedents\n"
    
    with open(OUTPUT_DIR / "repugnancy_summary.md", 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"    Saved: {OUTPUT_DIR / 'repugnancy_summary.md'}")
    
    print("\n" + "=" * 60)
    print("SUCCESS: HISTORICAL CORPUS WITH REPUGNANCY FOCUS COMPLETE!")
    print(f"Output: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()