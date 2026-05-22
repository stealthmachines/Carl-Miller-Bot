#!/usr/bin/env python3
"""
Carl Miller Enhanced Corpus Processor
Integrates Marbury v. Madison (1803) - THE DEFINITIVE REPUGNANCY DOCTRINE
Emphasis: "Anything in conflict with Supreme Law is NULL AND VOID FROM INCEPTION"
"""

import re
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"C:\Users\Owner\Downloads\Legal-Vision-main\Legal-Vision-main\Carl Miller")
OUTPUT_DIR = BASE_DIR / "Corpus_Processed" / "ENHANCED"

CHUNK_SIZE = 3500

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
    """Identify which document a chunk comes from"""
    chunk_lower = chunk.lower()
    
    if "john by the grace of god king of england" in chunk_lower:
        return "Magna_Carta_1215"
    elif "mayflower compact" in chunk_lower or "covenant and combine" in chunk_lower:
        return "Mayflower_Compact_1620"
    elif "marbury v madison" in chunk_lower or "chief justice marshall" in chunk_lower:
        return "Marbury_v_Madison_1803"
    elif "carl miller" in chunk_lower or "violate your rights" in chunk_lower:
        return "Carl_Miller_Teachings"
    else:
        return "Unknown"

def extract_repugnancy_analysis(chunk, doc_type):
    """Extract and analyze repugnancy/conflict concepts"""
    analysis = {
        "repugnancy_statements": [],
        "nullity_claims": [],
        "supremacy_references": [],
        "historical_precedents": [],
        "legal_principles": []
    }
    
    # Marbury v. Madison - KEY REPUGNANCY DOCTRINE
    marbury_patterns = [
        r"(?:anything\s+that\s+is\s+in\s+conflict\s+is\s+null\s+and\s+void\s+of\s+law|secondary\s+law\s+to\s+come\s+in\s+conflict|supreme\s+law\s+would\s+prevail|illogical\s+for\s+secondary\s+law)",
        r"(?:null\s+and\s+void\s+of\s+law|bear\s+no\s+power\s+to\s+enforce|bear\s+no\s+obligation\s+to\s+obey|purports\s+to\s+settle\s+as\s+if\s+it\s+never\s+existed)",
        r"(?:unconstitutionality\s+would\s+date\s+from\s+the\s+enactment|not\s+from\s+the\s+date\s+so\s+branded)",
        r"(?:no\s+courts\s+are\s+bound\s+to\s+uphold\s+it|no\s+citizens\s+are\s+bound\s+to\s+obey\s+it|operates\s+as\s+a\s+mere\s+nullity|fiction\s+of\s+law)",
    ]
    
    # General constitutional conflict patterns
    conflict_patterns = [
        r"(?:repugnant|repugnancy|in\s+conflict\s+with|contrary\s+to|clash\s+with|invalidates)",
        r"(?:supreme\s+law\s+of\s+the\s+land|article\s+\d+\s+paragraph\s+\d+|marbury\s+v\s+madison\s+\d+\s+u\.?s?)",
        r"(?:conflicting\s+provisions|cannot\s+be\s+reconciled|inconsistent\s+with\s+constitution)",
    ]
    
    # Historical precedents
    historical_patterns = [
        r"(?:magna\s+carta|king\s+john|barons|twenty-five\s+barons|law\s+of\s+the\s+land|judgment\s+of\s+his\s+equals)",
        r"(?:mayflower|compact|covenant|civil\s+body\s+politick|just\s+and\s+equal\s+laws)",
        r"(?:forefathers|constitution\s+of\s+united\s+states|1787|ratified|supreme\s+court)",
    ]
    
    # Legal principles
    principle_patterns = [
        r"(?:vested\s+legal\s+rights|right\s+to\s+remedy|government\s+of\s+laws\s+not\s+of\s+men|blackstone\s+commentaries)",
        r"(?:judicial\s+authority|original\s+jurisdiction|appellate\s+jurisdiction|warranted\s+by\s+constitution)",
        r"(?:ironclad\s+contract|statute\s+of\s+frauds|specific\s+performance|beneficiary\s+of\s+contract)",
    ]
    
    for pattern in marbury_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["nullity_claims"].extend(matches)
            analysis["repugnancy_statements"].extend(matches)
        except re.error:
            pass
    
    for pattern in conflict_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["repugnancy_statements"].extend(matches)
            analysis["supremacy_references"].extend(matches)
        except re.error:
            pass
    
    for pattern in historical_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["historical_precedents"].extend(matches)
        except re.error:
            pass
    
    for pattern in principle_patterns:
        try:
            matches = re.findall(pattern, chunk, re.IGNORECASE)
            analysis["legal_principles"].extend(matches)
        except re.error:
            pass
    
    return analysis

def main():
    print("Carl Miller Enhanced Corpus Processor")
    print("=" * 70)
    print("INTEGRATING MARBURY V MADISON (1803)")
    print("REPUGNANCY DOCTRINE: Conflict = NULL AND VOID FROM INCEPTION\n")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Read all sources in chronological order
    print("[1] Loading Founding Documents & Marbury v. Madison (1803)...")
    
    sources = {
        "Magna Carta (1215)": (BASE_DIR / "Magna Carta.txt", 1215),
        "Mayflower Compact (1620)": (BASE_DIR / "The Mayflower Compact.txt", 1620),
        "Marbury v. Madison (1803)": (BASE_DIR / "Marbury v. Madison, 5 U.S. 137 (1803).txt", 1803),
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
                print(f"    {name}: {len(chunks)} chunks, {len(content):,} bytes")
    
    # Add Carl Miller teachings
    print("\n[2] Adding Carl Miller Constitutional Teachings...")
    transcript_path = BASE_DIR / "Carl-Miller-Whisper-citation-corrected.txt"
    if transcript_path.exists():
        content = read_file(transcript_path)
        all_content.append({
            "name": "Carl Miller Transcript (Modern Application)",
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
        print(f"    Carl Miller: {len(chunks)} chunks, {len(content):,} bytes")
    
    # Combine and chunk
    print("\n[3] Combining All Sources Chronologically...")
    combined_content = ""
    for source in all_content:
        combined_content += source["content"] + "\n"
    
    final_chunks = chunk_text(combined_content, CHUNK_SIZE)
    print(f"    Total chunks: {len(final_chunks)}")
    print(f"    Total size: {len(combined_content):,} bytes")
    
    # Process each chunk
    print("\n[4] Analyzing for REPUGNANCY Doctrine...")
    all_chunks_data = []
    repugnancy_stats = {
        "total_repugnancy_mentions": 0,
        "total_nullity_claims": 0,
        "total_supremacy_refs": 0,
        "total_historical_precedents": 0,
        "total_legal_principles": 0,
        "by_document": {},
        "key_marbury_quotes": []
    }
    
    for i, chunk in enumerate(final_chunks):
        document_type = identify_document_type(chunk)
        analysis = extract_repugnancy_analysis(chunk, document_type)
        
        chunk_data = {
            "chunk_num": i,
            "document": document_type,
            "year": None,
            "content": chunk,
            "repugnancy_analysis": analysis,
            "word_count": len(chunk.split())
        }
        
        all_chunks_data.append(chunk_data)
        
        # Aggregate stats
        repugnancy_stats["total_repugnancy_mentions"] += len(analysis["repugnancy_statements"])
        repugnancy_stats["total_nullity_claims"] += len(analysis["nullity_claims"])
        repugnancy_stats["total_supremacy_refs"] += len(analysis["supremacy_references"])
        repugnancy_stats["total_historical_precedents"] += len(analysis["historical_precedents"])
        repugnancy_stats["total_legal_principles"] += len(analysis["legal_principles"])
        
        # Track by document
        if document_type not in repugnancy_stats["by_document"]:
            repugnancy_stats["by_document"][document_type] = {
                "mentions": 0,
                "nullity_claims": 0,
                "precedents": 0,
                "principles": 0
            }
        repugnancy_stats["by_document"][document_type]["mentions"] += len(analysis["repugnancy_statements"])
        repugnancy_stats["by_document"][document_type]["nullity_claims"] += len(analysis["nullity_claims"])
        repugnancy_stats["by_document"][document_type]["precedents"] += len(analysis["historical_precedents"])
        repugnancy_stats["by_document"][document_type]["principles"] += len(analysis["legal_principles"])
        
        # Collect key Marbury quotes
        if "marbury v madison" in document_type.lower():
            if "null and void" in chunk.lower() or "supreme law" in chunk.lower():
                repugnancy_stats["key_marbury_quotes"].append({
                    "chunk_num": i,
                    "quote": chunk[:200].strip() + "..." if len(chunk) > 200 else chunk.strip()
                })
    
    # Fill in year information
    chunk_index = {}
    for source in source_info:
        chunk_index[source["name"]] = source["year"]
    
    for chunk in all_chunks_data:
        chunk["year"] = chunk_index.get(chunk["document"], None)
    
    # Create topic index
    print("\n[5] Building Topic Index...")
    topics = {
        "Chronological_Historical_Base": [],
        "Repugnancy_Doctrine": [],
        "Nullity_From_Inception": [],
        "Supremacy_Clause": [],
        "Vested_Rights": [],
        "Judicial_Review": [],
        "Common_Law_Principles": []
    }
    
    for chunk in all_chunks_data:
        doc = chunk["document"]
        analysis = chunk["repugnancy_analysis"]
        
        if doc in ["Magna_Carta_1215", "Mayflower_Compact_1620"]:
            topics["Chronological_Historical_Base"].append(chunk)
        elif "marbury" in doc.lower():
            topics["Judicial_Review"].append(chunk)
            if analysis["nullity_claims"]:
                topics["Nullity_From_Inception"].append(chunk)
        elif "carl miller" in doc.lower():
            if analysis["repugnancy_statements"]:
                topics["Repugnancy_Doctrine"].append(chunk)
            if analysis["legal_principles"]:
                topics["Vested_Rights"].append(chunk)
        else:
            topics["Common_Law_Principles"].append(chunk)
    
    print(f"    Topics: {list(topics.keys())}")
    for topic, chunks in topics.items():
        print(f"      - {topic}: {len(chunks)} chunks")
    
    # Create output files
    print("\n[6] Writing Enhanced Corpus...")
    
    # Master enhanced corpus
    enhanced_corpus = {
        "metadata": {
            "processed_at": datetime.now().isoformat(),
            "emphasis": "REPUGNANCY DOCTRINE FROM MARBURY V MADISON (1803)",
            "chronological_order": True,
            "total_chunks": len(all_chunks_data),
            "total_documents": len(source_info),
            "key_principle": "Anything in conflict with Supreme Law is NULL AND VOID FROM INCEPTION"
        },
        "sources": source_info,
        "chunks": all_chunks_data,
        "topics": topics,
        "repugnancy_analysis": repugnancy_stats,
    }
    
    corpus_file = OUTPUT_DIR / "enhanced_historical_corpus.json"
    with open(corpus_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_corpus, f, indent=2, ensure_ascii=False)
    print(f"    Saved: {corpus_file} ({corpus_file.stat().st_size:,} bytes)")
    
    # Detailed repugnancy analysis
    analysis_file = OUTPUT_DIR / "detailed_repugnancy_analysis.json"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(repugnancy_stats, f, indent=2, ensure_ascii=False)
    print(f"    Saved: {analysis_file}")
    
    # Processing summary
    summary = f"""# Carl Miller Enhanced Historical Corpus - REPUGNANCY DOCTRINE

## CORE PRINCIPLE (From Marbury v. Madison, 1803)
> **"Anything that is in conflict with the Supreme Law is NULL AND VOID OF LAW"**
> - Chief Justice John Marshall

> **"For a secondary law to come in conflict with the Supreme Law was illogical, for certainly the Supreme Law would prevail over all other law"**
> - Marbury v. Madison, 5 U.S. 137 (1803)

> **"Unconstitutionality would date from the enactment of such a law, not from the date so branded in an open court of law"**
> - Marbury v. Madison

> **"No courts are bound to uphold it, and no citizens are bound to obey it. It operates as a mere nullity, or a fiction of law, which means it doesn't exist in law."**
> - Marbury v. Madison

## CHRONOLOGICAL FOUNDATION (1215-1803-2024)

### 1. Magna Carta (1215) - Foundation of "Law of the Land"
- King John's charter to barons
- Clause 39: "No free man shall be seized...except by the lawful judgment of his equals or by the law of the land"
- Clause 40: "To no one will we sell, to no one deny or delay right or justice"
- 25-barons security mechanism (proto-checks and balances)

### 2. Mayflower Compact (1620) - Covenant Government
- "Covenant and combine ourselves together into a civil Body Politick"
- "Enact, constitute, and frame, such just and equal Laws...for the General Good"
- Promise of "due Submission and Obedience"

### 3. Marbury v. Madison (1803) - Judicial Review & Supremacy
- Est. that laws conflicting with Constitution are NULL AND VOID FROM INCEPTION
- Chief Justice John Marshall's opinion
- 9 pages of Shepard Citations, never overturned
- Defines repugnancy doctrine definitively

### 4. Carl Miller Teachings (2024) - Modern Application
- Article 6, Paragraph 2 interpretation
- Supremacy Clause enforcement
- Practical courtroom application
- Citizen empowerment strategies

## REPUGNANCY STATISTICS

"""
    
    summary += f"""
**Overall:**
- Total Repugnancy Mentions: {repugnancy_stats['total_repugnancy_mentions']}
- Total Nullity Claims: {repugnancy_stats['total_nullity_claims']}
- Total Supremacy References: {repugnancy_stats['total_supremacy_refs']}
- Total Historical Precedents: {repugnancy_stats['total_historical_precedents']}
- Total Legal Principles: {repugnancy_stats['total_legal_principles']}

**By Document:**
"""
    
    for doc, stats in repugnancy_stats["by_document"].items():
        summary += f"\n- **{doc}**:\n  - Repugnancy mentions: {stats['mentions']}\n  - Nullity claims: {stats['nullity_claims']}\n  - Historical precedents: {stats['precedents']}\n  - Legal principles: {stats['principles']}\n"
    
    summary += f"""
## TOPICS IDENTIFIED

"""
    
    for topic, chunks in topics.items():
        summary += f"- {topic}: {len(chunks)} chunks\n"
    
    summary += f"""
## KEY MARBURY QUOTES ON REPUGNANCY

"""
    
    for quote in repugnancy_stats["key_marbury_quotes"][:5]:
        summary += f"### Chunk {quote['chunk_num']}: {quote['quote']}\n\n"
    
    summary += f"""
## PROCESSING DATE
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## USAGE
This corpus integrates:
1. Historical founding documents (1215-1620)
2. Marbury v. Madison judicial doctrine (1803)
3. Carl Miller's modern application (2024)

Emphasis on REPUGNANCY as the mechanism for identifying null and void laws.
"""
    
    with open(OUTPUT_DIR / "repugnancy_enhanced_summary.md", 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"    Saved: {OUTPUT_DIR / 'repugnancy_enhanced_summary.md'}")
    
    print("\n" + "=" * 70)
    print("SUCCESS: ENHANCED CORPUS WITH MARBURY V MADISON DOCTRINE COMPLETE!")
    print(f"📂 Output: {OUTPUT_DIR}")
    print(f"📊 Total chunks: {len(all_chunks_data)}")
    print(f"📊 Total repugnancy mentions: {repugnancy_stats['total_repugnancy_mentions']}")

if __name__ == "__main__":
    main()