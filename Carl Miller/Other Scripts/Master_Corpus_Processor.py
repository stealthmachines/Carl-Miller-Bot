#!/usr/bin/env python3
"""
Carl Miller Master Corpus Processor
Uses YouTube captions (most detailed) + PDFs for structure
Creates distilled, deduplicated corpus
"""

import re
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"C:\Users\Owner\Downloads\Legal-Vision-main\Legal-Vision-main\Carl Miller")
OUTPUT_DIR = BASE_DIR / "Corpus_Processed" / "MASTER"

CHUNK_SIZE = 5000
MIN_CONFIDENCE = 0.7  # For deduplication

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def read_pdf_simple(file_path):
    """Simple PDF text extraction using PyPDF2 if available"""
    try:
        import pypdf
        with open(file_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
    except ImportError:
        print("PyPDF2 not available, skipping PDF extraction")
        return ""
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""

def chunk_text(text, chunk_size):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks

def extract_key_concepts(chunk):
    """Extract constitutional concepts and legal terms"""
    concepts = {
        "amendments": [],
        "cases": [],
        "terms": [],
        "codes": []
    }
    
    # Amendment patterns
    amendment_patterns = [
        r"\d+(?:st|nd|rd|th)\s+Amendment",
        r"First\s+Amendment", r"Second\s+Amendment", r"Third\s+Amendment",
        r"Fourth\s+Amendment", r"Fifth\s+Amendment", r"Sixth\s+Amendment",
        r"Seventh\s+Amendment", r"Eighth\s+Amendment", r"Ninth\s+Amendment",
        r"Tenth\s+Amendment"
    ]
    
    # Case patterns
    case_patterns = [
        r"(\w+(?:\s+\w+)*\s+v?\.\s+\w+(?:\s+\w+)*)(?:\s+,\s*\d+\s+[Uu]S?\.?|v\s+\d+\s+[Uu]S?)?",
        r"Marbury\s+v?\.\s+Madison", r"Erie\s+Railroad\s+v?\.\s+Tompkins"
    ]
    
    # Legal term patterns
    legal_patterns = [
        r"(?:Article\s+\d+|Paragraph\s+\d+|Supremacy\s+Clause|Statute\s+of\s+Frauds|Laches|Specific\s+Performance|Due\s+Process|Double\s+Jeopardy|Self-incrimination|Grand\s+Jury|Common\s+Law|Admiralty|Bill\s+of\s+Attainder|Writ\s+of\s+Assistance|Treason|Sedition|Probable\s+Cause|Compulsory\s+Process|Shepard\s+Citations|AmJur\s+Prudence)",
        r"Title\s+\d+\s+[Uu]S(?:\.?C(?:odes?)?)\s+Section\s+\d+",
    ]
    
    # Title 18 USC Section 2381
    title_patterns = [
        r"Title\s+18\s+[Uu]?\.?S(?:\.?C(?:odes?)?)\s+Section\s+2381",
        r"Title\s+V\s+[Uu]?\.?S(?:\.?C(?:odes?)?)\s+(?:Section|Code)\s+(?:556D|557|706)"
    ]
    
    for pattern in amendment_patterns:
        matches = re.findall(pattern, chunk, re.IGNORECASE)
        concepts["amendments"].extend(matches)
    
    for pattern in case_patterns:
        matches = re.findall(pattern, chunk, re.IGNORECASE)
        concepts["cases"].extend(matches)
    
    for pattern in legal_patterns:
        matches = re.findall(pattern, chunk, re.IGNORECASE)
        concepts["terms"].extend(matches)
    
    for pattern in title_patterns:
        matches = re.findall(pattern, chunk, re.IGNORECASE)
        concepts["codes"].extend(matches)
    
    # Remove duplicates
    for key in concepts:
        concepts[key] = list(set(concepts[key]))
    
    return concepts

def identify_topic(chunk):
    """Identify main topic based on content"""
    chunk_lower = chunk.lower()
    
    topics = {
        "Introduction": ["name", "welcome", "thank", "inviting", "home", "carl miller"],
        "Background": ["vietnam", "blue book", "soldier", "military", "combat", "marine", "air force"],
        "Contract_Theory": ["contract", "ironclad", "beneficiary", "statute of frauds", "enforceable", "offer", "agreement"],
        "Supremacy_Clause": ["article 6", "supremacy", "supreme law", "marbury v madison", "notwithstanding"],
        "Second_Amendment": ["second amendment", "keep and bear arms", "infringed", "militia", "collective right"],
        "Fourth_Amendment": ["fourth amendment", "search and seizure", "warrant", "probable cause", "666 bill"],
        "Fifth_Amendment": ["fifth amendment", "grand jury", "double jeopardy", "due process", "self-incrimination", "title v"],
        "Sixth_Amendment": ["sixth amendment", "trial", "counsel", "jury", "confront", "subpoena"],
        "Seventh_Amendment": ["seventh amendment", "jury trial", "common law", "fact finder"],
        "Ninth_Amendment": ["ninth amendment", "unenumerated rights", "retained rights"],
        "Tenth_Amendment": ["tenth amendment", "reserved powers", "police powers", "states"],
        "Legal_Tools": ["black's law dictionary", "am juris", "case law", "cite", "shepard citations"],
        "Tactics": ["court", "jurisdiction", "specific performance", "laches", "acquiesce"],
        "Military_Oath": ["oath of office", "treason", "title 18", "2381", "sedition"],
        "Due_Process": ["due process", "title v", "556d", "jurisdiction ceases"],
        "Common_Law": ["common law", "admiralty", "errie railroad", "tomkins", "forefathers"],
    }
    
    for topic, keywords in topics.items():
        if any(keyword in chunk_lower for keyword in keywords):
            return topic
    
    return "General"

def main():
    print("Carl Miller Master Corpus Processor")
    print("=" * 60)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Read YouTube captions (primary source - most detailed)
    print("\n[1] Reading YouTube Captions (Primary Source)...")
    youtube_path = BASE_DIR / "Youtube-CC" / "captions.txt"
    if youtube_path.exists():
        youtube_content = read_file(youtube_path)
        print(f"    Size: {len(youtube_content):,} bytes, {youtube_content.count(chr(10))+youtube_content.count(chr(13))} lines")
    else:
        youtube_content = ""
        print(f"    ERROR: File not found")
    
    # Read audio transcript (corrected version)
    print("\n[2] Reading Corrected Audio Transcript...")
    transcript_path = BASE_DIR / "Carl-Miller-Whisper-citation-corrected.txt"
    if transcript_path.exists():
        transcript_content = read_file(transcript_path)
        print(f"    Size: {len(transcript_content):,} bytes")
    else:
        transcript_content = ""
        print(f"    ERROR: File not found")
    
    # Read PDF (if possible)
    print("\n[3] Reading PDF Files (Structure Reference)...")
    pdf_content = ""
    pdf_paths = [
        BASE_DIR / "Carl-Miller-Law-Study.pdf",
        BASE_DIR / "constitutional-law-by-carl-miller.pdf"
    ]
    
    try:
        import pypdf
        for pdf_path in pdf_paths:
            if pdf_path.exists():
                print(f"    Processing: {pdf_path.name}")
                pdf_content += read_pdf_simple(pdf_path) + "\n"
        print(f"    Total PDF size: {len(pdf_content):,} bytes")
    except ImportError:
        print("    PyPDF2 not available, skipping PDF extraction")
    
    # Combine sources (YouTube + Transcript for redundancy)
    print("\n[4] Combining and Cleaning Sources...")
    combined_content = youtube_content + "\n" + transcript_content
    print(f"    Combined size: {len(combined_content):,} bytes")
    
    # Chunk the content
    print("\n[5] Chunking Content...")
    chunks = chunk_text(combined_content, CHUNK_SIZE)
    print(f"    Total chunks: {len(chunks)}")
    
    # Process each chunk
    print("\n[6] Processing Chunks...")
    all_chunks = []
    entity_counts = {
        "amendments": set(),
        "cases": set(),
        "terms": set(),
        "codes": set()
    }
    
    for i, chunk in enumerate(chunks):
        concepts = extract_key_concepts(chunk)
        topic = identify_topic(chunk)
        
        chunk_data = {
            "chunk_num": i,
            "topic": topic,
            "content": chunk,
            "concepts": concepts,
            "word_count": len(chunk.split())
        }
        
        all_chunks.append(chunk_data)
        
        # Aggregate entities
        for key in entity_counts.keys():
            entity_counts[key].update(concepts[key])
    
    # Create topic index
    print("\n[7] Building Topic Index...")
    topic_index = {}
    for chunk in all_chunks:
        topic = chunk["topic"]
        if topic not in topic_index:
            topic_index[topic] = []
        topic_index[topic].append(chunk)
    
    print(f"    Topics found: {len(topic_index)}")
    for topic, chunks in topic_index.items():
        print(f"      - {topic}: {len(chunks)} chunk(s)")
    
    # Create output files
    print("\n[8] Writing Output Files...")
    
    # Full master corpus
    master_corpus = {
        "metadata": {
            "processed_at": datetime.now().isoformat(),
            "source": "YouTube captions + Audio transcript",
            "total_chunks": len(all_chunks),
            "total_topics": len(topic_index),
        },
        "chunks": all_chunks,
        "topic_index": topic_index,
    }
    
    master_file = OUTPUT_DIR / "master_corpus.json"
    with open(master_file, 'w', encoding='utf-8') as f:
        json.dump(master_corpus, f, indent=2, ensure_ascii=False)
    print(f"    Saved: {master_file} ({master_file.stat().st_size:,} bytes)")
    
    # Deduplicated entities
    print("\n[9] Aggregating Unique Entities...")
    unique_entities = {
        "amendments": list(entity_counts["amendments"]),
        "cases": list(entity_counts["cases"]),
        "terms": list(entity_counts["terms"]),
        "codes": list(entity_counts["codes"]),
    }
    
    entities_file = OUTPUT_DIR / "unique_entities.json"
    with open(entities_file, 'w', encoding='utf-8') as f:
        json.dump(unique_entities, f, indent=2, ensure_ascii=False)
    print(f"    Saved: {entities_file}")
    for entity_type, entities in unique_entities.items():
        print(f"      - {entity_type}: {len(entities)} unique items")
    
    # Processing summary
    summary = f"""# Carl Miller Master Corpus - Processing Summary

## Sources Processed
- YouTube Captions: {len(youtube_content):,} bytes
- Audio Transcript: {len(transcript_content):,} bytes  
- PDF Documents: {len(pdf_content):,} bytes (if available)

## Processing Statistics
- Total Chunks: {len(all_chunks)}
- Topics Identified: {len(topic_index)}
- Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Unique Entities Extracted
- Amendments: {len(unique_entities['amendments'])}
- Case Law Citations: {len(unique_entities['cases'])}
- Legal Terms: {len(unique_entities['terms'])}
- Code References: {len(unique_entities['codes'])}

## Topics Found
"""
    
    for topic, chunks in topic_index.items():
        summary += f"- {topic}: {len(chunks)} chunk(s)\n"
    
    with open(OUTPUT_DIR / "processing_summary.md", 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"    Saved: {OUTPUT_DIR / 'processing_summary.md'}")
    
    print("\n" + "=" * 60)
    print("✅ MASTER CORPUS PROCESSING COMPLETE!")
    print(f"📂 Output: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()