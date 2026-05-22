#!/usr/bin/env python3
"""
Carl Miller Bot Full Corpus Processor
Processes complete transcripts to create structured knowledge base
"""

import re
import json
from pathlib import Path
from datetime import datetime

# Configuration
SOURCE_DIR = r"C:\Users\Owner\Downloads\Legal-Vision-main\Legal-Vision-main\Carl Miller"
OUTPUT_DIR = r"C:\Users\Owner\Downloads\Legal-Vision-main\Legal-Vision-main\Carl Miller\Corpus_Processed"
CHUNK_SIZE = 5000  # Characters per chunk for processing

# Known entities and patterns to extract
CONSTITUTIONAL_CONCEPTS = {
    "amendments": [
        r"(?:Second\s+Amendment|Fourth\s+Amendment|Fifth\s+Amendment|Sixth\s+Amendment|Seventh\s+Amendment|Ninth\s+Amendment|Tenth\s+Amendment|First\s+Amendment)",
    ],
    "case_law": [
        r"(\w+(?:\s+\w+)*\s+v?\.(?:\s+\w+(?:\s+\w+)*)[\s,]+(?:\d+(?:\.\d+)?\s+[Uu]?\.?S(?:\.?s?)?)?)",
    ],
    "legal_terms": [
        r"(?:Article\s+\d+|Paragraph\s+\d+|Supremacy\s+Clause|Statute\s+of\s+Frauds|Marbury\s+v?\.\s+Madison|Shepard\s+Citations|Laches|Specific\s+Performance|Due\s+Process|Double\s+Jeopardy|Self-incrimination|Grand\s+Jury|Common\s+Law|Admiralty|Bill\s+of\s+Attainder|Writ\s+of\s+Assistance|Treason|Sedition|Miranda|Probable\s+Cause|Compulsory\s+Process)",
    ],
    "titles_code": [
        r"Title\s+\d+\s+[Uu]?\.?S(?:\.?C(?:odes?)?)\s+Section\s+(\d+)",
    ],
    "quotes_principles": [
        r"(?:I am prepared to give my life if necessary in defense of that Constitution|We have a republic if we can keep it|If you don't know your rights, you don't have any rights|The Constitution is an ironclad contract)",
    ],
}

def read_file(file_path):
    """Read file content with UTF-8 encoding"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def chunk_text(text, chunk_size):
    """Split text into manageable chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks

def extract_entities(chunk, entity_type):
    """Extract entities of specific type from chunk"""
    patterns = CONSTITUTIONAL_CONCEPTS.get(entity_type, [])
    entities = []
    
    for pattern in patterns:
        matches = re.findall(pattern, chunk, re.IGNORECASE)
        entities.extend(matches)
    
    return entities

def process_chunk(chunk, chunk_num):
    """Process a single chunk and extract relevant information"""
    result = {
        "chunk_num": chunk_num,
        "content": chunk[:200] + "..." if len(chunk) > 200 else chunk,
        "entities": {
            "amendments": list(set(extract_entities(chunk, "amendments"))),
            "case_law": list(set(extract_entities(chunk, "case_law"))),
            "legal_terms": list(set(extract_entities(chunk, "legal_terms"))),
            "titles_code": list(set(extract_entities(chunk, "titles_code"))),
            "quotes": list(set(extract_entities(chunk, "quotes_principles"))),
        }
    }
    return result

def identify_topic(chunk):
    """Identify the main topic of a chunk"""
    chunk_lower = chunk.lower()
    
    topics = {
        "Introduction": ["name", "welcome", "thank", "inviting", "home"],
        "Background": ["vietnam", "blue book", "soldier", "military", "servicemember"],
        "Contract_Theory": ["contract", "ironclad", "beneficiary", "statute of frauds", "enforceable"],
        "Supremacy_Clause": ["article 6", "supremacy", "supreme law", "marbury v madison"],
        "Second_Amendment": ["second amendment", "keep and bear arms", "infringed", "militia"],
        "Fourth_Amendment": ["fourth amendment", "search and seizure", "warrant", "probable cause"],
        "Fifth_Amendment": ["fifth amendment", "grand jury", "double jeopardy", "due process", "self-incrimination"],
        "Sixth_Amendment": ["sixth amendment", "trial", "counsel", "jury"],
        "Seventh_Amendment": ["seventh amendment", "jury trial", "common law"],
        "Ninth_Amendment": ["ninth amendment", "unenumerated rights", "retained"],
        "Tenth_Amendment": ["tenth amendment", "reserved powers", "states"],
        "Legal_Tools": ["black's law dictionary", "am juris", "case law", "cite"],
        "Tactics": ["court", "jurisdiction", "specific performance", "laches"],
        "Military_Oath": ["oath of office", "treason", "seditious", "serve"],
    }
    
    for topic, keywords in topics.items():
        if any(keyword in chunk_lower for keyword in keywords):
            return topic
    
    return "General"

def create_topic_index(all_chunks):
    """Create index of chunks by topic"""
    index = {}
    
    for chunk in all_chunks:
        topic = identify_topic(chunk["content"])
        if topic not in index:
            index[topic] = []
        index[topic].append(chunk)
    
    return index

def extract_definitions(chunk):
    """Extract definitions from text"""
    definitions = []
    
    # Look for patterns like "X is defined as Y" or "X means Y"
    pattern = r"(\w+(?:\s+\w+)+)\s+(?:is\s+|means\s+|is defined as\s+)(.+?)(?:\.|,|$)"
    matches = re.findall(pattern, chunk, re.IGNORECASE)
    
    for term, definition in matches:
        definitions.append({
            "term": term,
            "definition": definition.strip(),
            "context": chunk[:100]
        })
    
    return definitions

def main():
    """Main processing function"""
    print("Carl Miller Corpus Processor")
    print("=" * 50)
    
    # Initialize output directory
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Process each source file
    source_files = [
        "Carl-Miller-Whisper-citation-corrected.txt",
        "Carl-Miller-Whisper-Orig.txt",
    ]
    
    all_chunks = []
    all_definitions = []
    entity_count = {
        "amendments": 0,
        "case_law": 0,
        "legal_terms": 0,
        "titles_code": 0,
    }
    
    for source_file in source_files:
        source_path = Path(SOURCE_DIR) / source_file
        if not source_path.exists():
            print(f"WARNING: File not found: {source_file}")
            continue
        
        print(f"\n[PROCESSING] {source_file}")
        content = read_file(source_path)
        print(f"   Size: {len(content):,} characters")
        
        chunks = chunk_text(content, CHUNK_SIZE)
        print(f"   Split into {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks):
            result = process_chunk(chunk, i)
            all_chunks.append(result)
            
            # Track entity counts
            for entity_type in entity_count.keys():
                count = len(result["entities"][entity_type])
                entity_count[entity_type] += count
            
            # Extract definitions
            defs = extract_definitions(chunk)
            all_definitions.extend(defs)
    
    print(f"\n[COMPLETE] Processing Finished")
    print(f"   Total chunks: {len(all_chunks)}")
    print(f"   Total definitions: {len(all_definitions)}")
    print(f"\n[SUMMARY] Entity Extraction:")
    for entity_type, count in entity_count.items():
        print(f"   {entity_type}: {count}")
    
    # Create comprehensive output files
    
    # 1. Full structured corpus
    corpus_data = {
        "metadata": {
            "processed_at": datetime.now().isoformat(),
            "source_files": source_files,
            "total_chunks": len(all_chunks),
            "total_definitions": len(all_definitions),
        },
        "chunks": all_chunks,
        "definitions": all_definitions,
    }
    
    corpus_file = output_path / "full_corpus.json"
    with open(corpus_file, 'w', encoding='utf-8') as f:
        json.dump(corpus_data, f, indent=2, ensure_ascii=False)
    print(f"\n[SAVED] Full corpus to: {corpus_file}")
    
    # 2. Topic-indexed corpus
    topic_index = create_topic_index(all_chunks)
    topic_corpus = {
        "metadata": {
            "processed_at": datetime.now().isoformat(),
            "topics_found": list(topic_index.keys()),
        },
        "topics": topic_index,
    }
    
    topic_file = output_path / "topic_indexed_corpus.json"
    with open(topic_file, 'w', encoding='utf-8') as f:
        json.dump(topic_corpus, f, indent=2, ensure_ascii=False)
    print(f"[SAVED] Topic-indexed corpus to: {topic_file}")
    
    # 3. Extracted definitions
    definitions_file = output_path / "definitions.json"
    with open(definitions_file, 'w', encoding='utf-8') as f:
        json.dump(all_definitions, f, indent=2, ensure_ascii=False)
    print(f"[SAVED] Definitions to: {definitions_file}")
    
    # 4. Summary statistics
    summary_file = output_path / "processing_summary.md"
    summary_content = f"""# Carl Miller Corpus Processing Summary

## Processing Statistics
- **Processed Files**: {len(source_files)}
- **Total Chunks**: {len(all_chunks)}
- **Total Definitions**: {len(all_definitions)}

## Entity Extraction Summary
- **Amendments Referenced**: {entity_count['amendments']}
- **Case Law Citations**: {entity_count['case_law']}
- **Legal Terms**: {entity_count['legal_terms']}
- **Code References**: {entity_count['titles_code']}

## Output Files
- full_corpus.json: Full structured JSON corpus
- topic_indexed_corpus.json: Topic-indexed corpus for quick access
- definitions.json: Extracted definitions
- processing_summary.md: This summary

## Processing Date
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    print(f"[SAVED] Summary to: {summary_file}")
    
    print("\n[SUCCESS] Corpus processing complete!")
    print(f"[OUTPUT] Directory: {output_path}")

if __name__ == "__main__":
    main()