"""
build_citation_map.py
Build citation_mapped_corpus.json from Carl Miller chunks + Am. Jur. transcription.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import json
import re
import datetime
from collections import defaultdict

# ── File paths ──────────────────────────────────────────────────────────────
BASE = "C:/Users/Owner/Downloads/Legal-Vision-main/Legal-Vision-main/Carl Miller/Corpus_Processed"
CORPUS_PATH = f"{BASE}/consolidated_corpus.json"
TRANSCRIPTION_PATH = f"{BASE}/transcription_progress.json"
OUTPUT_PATH = f"{BASE}/citation_mapped_corpus.json"

# ── Load data ────────────────────────────────────────────────────────────────
print("Loading source files...")
with open(CORPUS_PATH, encoding='utf-8', errors='replace') as f:
    corpus = json.load(f)

with open(TRANSCRIPTION_PATH, encoding='utf-8', errors='replace') as f:
    transcription = json.load(f)

# Pull Carl Miller chunks
cm_chunks = []
for doc in corpus['documents']:
    if 'Carl Miller' in doc['name']:
        cm_chunks = doc['chunks']
        break
print(f"  Carl Miller chunks: {len(cm_chunks)}")
print(f"  Am. Jur. image entries: {len(transcription)}")

# ── STEP 1 — Extract citations from Carl Miller chunks ──────────────────────
print("\nStep 1: Extracting citations from Carl Miller chunks...")

# Amendment name → ordinal key
AMENDMENT_NAMES = {
    'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5,
    'sixth': 6, 'seventh': 7, 'eighth': 8, 'ninth': 9, 'tenth': 10,
    'eleventh': 11, 'twelfth': 12, 'thirteenth': 13, 'fourteenth': 14,
    '1st': 1, '2nd': 2, '3rd': 3, '4th': 4, '5th': 5,
    '6th': 6, '7th': 7, '8th': 8, '9th': 9, '10th': 10,
    '11th': 11, '12th': 12, '13th': 13, '14th': 14,
}
ORDINAL_TO_WORD = {
    1: 'First', 2: 'Second', 3: 'Third', 4: 'Fourth', 5: 'Fifth',
    6: 'Sixth', 7: 'Seventh', 8: 'Eighth', 9: 'Ninth', 10: 'Tenth',
    11: 'Eleventh', 12: 'Twelfth', 13: 'Thirteenth', 14: 'Fourteenth',
}

# Amendment search terms for Am. Jur. lookup
AMENDMENT_AMJUR_TERMS = {
    1: ['First Amendment', 'freedom of speech', 'freedom of press', 'right to petition', 'religious freedom', 'freedom of religion'],
    2: ['Second Amendment', 'right to bear arms', 'bear arms', 'militia'],
    3: ['Third Amendment', 'quartering of soldiers', 'quarter any soldier'],
    4: ['Fourth Amendment', 'search and seizure', 'unreasonable search', 'right of the people to be secure'],
    5: ['Fifth Amendment', 'due process', 'double jeopardy', 'self-incrimination', 'grand jury', 'just compensation'],
    6: ['Sixth Amendment', 'speedy trial', 'right to counsel', 'right to a speedy'],
    7: ['Seventh Amendment', 'trial by jury', 'jury in civil'],
    8: ['Eighth Amendment', 'cruel and unusual', 'excessive bail', 'excessive fines'],
    9: ['Ninth Amendment', 'enumeration of rights', 'rights retained by the people'],
    10: ['Tenth Amendment', 'reserved to the states', 'powers reserved', 'powers not delegated'],
    11: ['Eleventh Amendment', 'judicial power', 'suit against state'],
    12: ['Twelfth Amendment', 'election of president', 'electoral'],
    13: ['Thirteenth Amendment', 'slavery', 'involuntary servitude', 'abolish slavery'],
    14: ['Fourteenth Amendment', 'equal protection', 'privileges or immunities', 'due process of law', 'citizenship'],
}

def get_context(text, match_start, match_end, window=80):
    """Return ±window chars around a match."""
    start = max(0, match_start - window)
    end = min(len(text), match_end + window)
    snippet = text[start:end].replace('\n', ' ')
    if start > 0:
        snippet = '…' + snippet
    if end < len(text):
        snippet = snippet + '…'
    return snippet.strip()

# Storage: keyed by normalized string
amendments_map = {}   # norm_key -> {ordinal, raw_variants, mentions}
cases_map = {}        # norm_key -> {raw_variants, mentions}
statutes_map = {}     # norm_key -> {raw_variants, mentions}
const_refs_map = {}   # norm_key -> {raw_variants, mentions}
amjur_refs_map = {}   # norm_key -> {raw_variants, mentions}

# ── Amendment regex ──────────────────────────────────────────────────────────
AMEND_RE = re.compile(
    r'\b(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|'
    r'eleventh|twelfth|thirteenth|fourteenth|'
    r'1st|2nd|3rd|4th|5th|6th|7th|8th|9th|10th|11th|12th|13th|14th)\s+amendment\b',
    re.IGNORECASE
)

# ── Case citation regex: Name v. Name or Name vs. Name ──────────────────────
CASE_RE = re.compile(
    r'\b([A-Z][a-zA-Z\'\-\.]{1,30}(?:\s+[A-Z][a-zA-Z\'\-\.]{1,30}){0,3})\s+'
    r'v(?:s)?\.?\s+'
    r'([A-Z][a-zA-Z\'\-\.]{1,30}(?:\s+[A-Z][a-zA-Z\'\-\.]{1,30}){0,3})'
    r'(?:[,\s]+[\dA-Z][\w\s\.\(\)]*)?',
    re.MULTILINE
)

# Reporter/citation suffix for cleanup
REPORTER_RE = re.compile(
    r',?\s*\d+\s+(?:U\.S\.|S\.Ct\.|L\.Ed\.|F\.\d+d|F\.Supp|Cranch|Wheat|Wall|How|Pet|Dal|Met|'
    r'Blatch|Abb|N\.W\.|S\.W\.|S\.E\.|A\.|P\.|N\.E\.|So\.|Cal\.|N\.Y\.|Ill\.|Tex\.|Fla\.|Ohio|'
    r'Mich\.|Pa\.|Mass\.|Va\.|Ga\.|Ind\.|Iowa|Kan\.|Ky\.|La\.|Me\.|Md\.|Minn\.|Miss\.|Mo\.|'
    r'Mont\.|Neb\.|Nev\.|N\.H\.|N\.J\.|N\.M\.|N\.C\.|N\.D\.|Okla\.|Or\.|R\.I\.|S\.C\.|S\.D\.|'
    r'Tenn\.|Utah|Vt\.|Wash\.|W\.Va\.|Wis\.|Wyo\.|L\.R\.A\.|Ann\.Cas\.|Am\.St\.Rep\.).*',
    re.IGNORECASE
)

# False-positive case name fragments to skip
SKIP_CASE_WORDS = {
    'united states', 'united state', 'the united', 'of the', 'in the', 'and the',
    'under the', 'from the', 'by the', 'for the', 'to the', 'with the',
    'it is', 'this is', 'that is', 'there is', 'he is', 'she is',
    'you have', 'they have', 'we have', 'i have', 'have the',
    'article', 'section', 'amendment', 'constitution', 'congress', 'court',
    'federal', 'state', 'government', 'law', 'rights', 'people',
}

def is_valid_case_name(name):
    """Filter obvious false positives from case extraction."""
    name_lower = name.lower().strip()
    if len(name_lower) < 3:
        return False
    # Must start with uppercase letter
    if not name[0].isupper():
        return False
    # Must not be a common phrase
    if name_lower in SKIP_CASE_WORDS:
        return False
    # Must not be all caps (abbreviation)
    if name.isupper() and len(name) > 4:
        return False
    # Filter single common words
    common = {'the', 'and', 'but', 'for', 'nor', 'yet', 'so', 'or', 'a', 'an',
              'this', 'that', 'these', 'those', 'it', 'its', 'he', 'she', 'they',
              'we', 'you', 'i', 'my', 'our', 'your', 'their', 'his', 'her',
              'be', 'is', 'are', 'was', 'were', 'been', 'being', 'have', 'has',
              'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
              'may', 'might', 'shall', 'must', 'can', 'not', 'no', 'if', 'as',
              'at', 'by', 'in', 'of', 'on', 'to', 'up', 'out', 'all', 'any',
              'also', 'only', 'just', 'now', 'than', 'then', 'there', 'here',
              'when', 'where', 'why', 'how', 'which', 'who', 'what', 'whom',
              'under', 'over', 'into', 'from', 'with', 'about', 'after',
              'before', 'since', 'until', 'while', 'because', 'though', 'although',
              'however', 'therefore', 'thus', 'hence', 'furthermore', 'moreover',
              'nevertheless', 'notwithstanding', 'regardless'}
    if name_lower in common:
        return False
    return True

def normalize_case_key(plaintiff, defendant):
    """Produce a normalized key like 'marbury v. madison'."""
    p = plaintiff.strip().lower()
    d = defendant.strip().lower()
    # Remove trailing punctuation
    p = re.sub(r'[,\.\s]+$', '', p)
    d = re.sub(r'[,\.\s]+$', '', d)
    return f"{p} v. {d}"

# ── Statute regex ─────────────────────────────────────────────────────────────
STATUTE_RE = re.compile(
    r'\b(?:'
    r'UCC\s+\d+[-–]\d+(?:\.\d+)?(?:\s*[a-zA-Z])?|'          # UCC 1-207
    r'\d+\s+U\.S\.C\.(?:\s+§\s*\d+)?|'                        # 42 U.S.C. § 1983
    r'MCL\s+\d+[\.\d]*|'                                       # MCL 750.123
    r'Article\s+(?:I{1,3}|IV|V{1,3}|VI|VII|VIII|IX|X{1,2}|\d+)'  # Article VI
    r'(?:\s*,?\s*(?:Paragraph|Para|Section|Sec|§)\s*\d+(?:\s+\d+)?)?'
    r')',
    re.IGNORECASE
)

# ── Constitutional reference regex ────────────────────────────────────────────
CONST_REF_RE = re.compile(
    r'\bArticle\s+(?:\d+|I{1,3}|IV|V{1,3}|VI|VII|VIII|IX|X{1,2})'
    r'(?:\s*,?\s+(?:Paragraph|Para|Section|Sec|§|Clause)\s+(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten))'
    r'(?:\s*,?\s+(?:Paragraph|Para|Section|Sec|§|Clause)\s+(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten))?',
    re.IGNORECASE
)

# ── Am. Jur. reference regex ──────────────────────────────────────────────────
AMJUR_RE = re.compile(
    r'\b(?:Am\.?\s*Jur\.?(?:\s+\d+)?|American\s+Jurisprudence)\b',
    re.IGNORECASE
)

def normalize_statute(raw):
    """Normalize a statute reference."""
    s = raw.strip()
    s = re.sub(r'\s+', ' ', s)
    return s.lower()

def normalize_const_ref(raw):
    s = raw.strip()
    s = re.sub(r'\s+', ' ', s)
    # Normalize number words
    word_to_num = {'one':'1','two':'2','three':'3','four':'4','five':'5',
                   'six':'6','seven':'7','eight':'8','nine':'9','ten':'10'}
    for w, n in word_to_num.items():
        s = re.sub(r'\b' + w + r'\b', n, s, flags=re.IGNORECASE)
    return s.lower()


# ── Process each chunk ────────────────────────────────────────────────────────
for chunk in cm_chunks:
    chunk_num = chunk['chunk_num']
    text = chunk.get('content', '')
    existing_concepts = chunk.get('concepts', {})

    # ---------- Amendments ----------
    # First use existing concepts.amendments
    for amend_str in existing_concepts.get('amendments', []):
        m = re.match(
            r'(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|'
            r'eleventh|twelfth|thirteenth|fourteenth)',
            amend_str, re.IGNORECASE
        )
        if m:
            word = m.group(1).lower()
            ordinal = AMENDMENT_NAMES.get(word)
            if ordinal:
                norm_key = f"amendment_{ordinal:02d}"
                if norm_key not in amendments_map:
                    amendments_map[norm_key] = {
                        'ordinal': ordinal,
                        'raw_variants': set(),
                        'mentions': [],
                    }
                amendments_map[norm_key]['raw_variants'].add(amend_str.strip())

    # Also regex-scan the text for amendments
    for m in AMEND_RE.finditer(text):
        word = m.group(1).lower()
        ordinal = AMENDMENT_NAMES.get(word)
        if ordinal:
            norm_key = f"amendment_{ordinal:02d}"
            raw = m.group(0).strip()
            ctx = get_context(text, m.start(), m.end())
            if norm_key not in amendments_map:
                amendments_map[norm_key] = {
                    'ordinal': ordinal,
                    'raw_variants': set(),
                    'mentions': [],
                }
            amendments_map[norm_key]['raw_variants'].add(raw)
            # Avoid duplicate chunk mentions
            existing_chunks = [mn['chunk_num'] for mn in amendments_map[norm_key]['mentions']]
            if chunk_num not in existing_chunks:
                amendments_map[norm_key]['mentions'].append({
                    'chunk_num': chunk_num,
                    'context': ctx,
                })

    # Ensure mentions for existing_concepts amendments (if we didn't catch them via regex)
    for amend_str in existing_concepts.get('amendments', []):
        m2 = re.match(
            r'(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|'
            r'eleventh|twelfth|thirteenth|fourteenth)',
            amend_str, re.IGNORECASE
        )
        if m2:
            word = m2.group(1).lower()
            ordinal = AMENDMENT_NAMES.get(word)
            if ordinal:
                norm_key = f"amendment_{ordinal:02d}"
                if norm_key in amendments_map:
                    existing_chunks = [mn['chunk_num'] for mn in amendments_map[norm_key]['mentions']]
                    if chunk_num not in existing_chunks:
                        # find context via simple search
                        idx = text.lower().find(amend_str.lower())
                        ctx = get_context(text, idx, idx + len(amend_str)) if idx >= 0 else amend_str
                        amendments_map[norm_key]['mentions'].append({
                            'chunk_num': chunk_num,
                            'context': ctx,
                        })

    # ---------- Cases ----------
    for m in CASE_RE.finditer(text):
        plaintiff = m.group(1).strip()
        defendant = m.group(2).strip()
        if not is_valid_case_name(plaintiff) or not is_valid_case_name(defendant):
            continue
        # Clean trailing reporter/numbers from defendant
        defendant = re.sub(r'\s*[\d,]+.*$', '', defendant).strip()
        defendant = re.sub(r'[,\.]+$', '', defendant).strip()
        if not defendant or not is_valid_case_name(defendant):
            continue

        norm_key = normalize_case_key(plaintiff, defendant)
        raw = f"{plaintiff} v. {defendant}"
        ctx = get_context(text, m.start(), m.end())

        if norm_key not in cases_map:
            cases_map[norm_key] = {'raw_variants': set(), 'mentions': []}
        cases_map[norm_key]['raw_variants'].add(raw)
        existing_chunks = [mn['chunk_num'] for mn in cases_map[norm_key]['mentions']]
        if chunk_num not in existing_chunks:
            cases_map[norm_key]['mentions'].append({'chunk_num': chunk_num, 'context': ctx})

    # ---------- Statutes ----------
    for m in STATUTE_RE.finditer(text):
        raw = m.group(0).strip()
        norm_key = normalize_statute(raw)
        ctx = get_context(text, m.start(), m.end())
        if norm_key not in statutes_map:
            statutes_map[norm_key] = {'raw_variants': set(), 'mentions': []}
        statutes_map[norm_key]['raw_variants'].add(raw)
        existing_chunks = [mn['chunk_num'] for mn in statutes_map[norm_key]['mentions']]
        if chunk_num not in existing_chunks:
            statutes_map[norm_key]['mentions'].append({'chunk_num': chunk_num, 'context': ctx})

    # Also add from existing concepts.codes
    for code_str in existing_concepts.get('codes', []):
        norm_key = normalize_statute(code_str)
        if norm_key not in statutes_map:
            statutes_map[norm_key] = {'raw_variants': set(), 'mentions': []}
        statutes_map[norm_key]['raw_variants'].add(code_str.strip())
        existing_chunks = [mn['chunk_num'] for mn in statutes_map[norm_key]['mentions']]
        if chunk_num not in existing_chunks:
            idx = text.lower().find(code_str.lower())
            ctx = get_context(text, idx, idx + len(code_str)) if idx >= 0 else code_str
            statutes_map[norm_key]['mentions'].append({'chunk_num': chunk_num, 'context': ctx})

    # ---------- Constitutional references ----------
    for m in CONST_REF_RE.finditer(text):
        raw = m.group(0).strip()
        norm_key = normalize_const_ref(raw)
        ctx = get_context(text, m.start(), m.end())
        if norm_key not in const_refs_map:
            const_refs_map[norm_key] = {'raw_variants': set(), 'mentions': []}
        const_refs_map[norm_key]['raw_variants'].add(raw)
        existing_chunks = [mn['chunk_num'] for mn in const_refs_map[norm_key]['mentions']]
        if chunk_num not in existing_chunks:
            const_refs_map[norm_key]['mentions'].append({'chunk_num': chunk_num, 'context': ctx})

    # ---------- Am. Jur. references ----------
    for m in AMJUR_RE.finditer(text):
        raw = m.group(0).strip()
        norm_key = 'am. jur. constitutional law'
        ctx = get_context(text, m.start(), m.end())
        if norm_key not in amjur_refs_map:
            amjur_refs_map[norm_key] = {'raw_variants': set(), 'mentions': []}
        amjur_refs_map[norm_key]['raw_variants'].add(raw)
        existing_chunks = [mn['chunk_num'] for mn in amjur_refs_map[norm_key]['mentions']]
        if chunk_num not in existing_chunks:
            amjur_refs_map[norm_key]['mentions'].append({'chunk_num': chunk_num, 'context': ctx})

print(f"  Amendments found: {len(amendments_map)}")
print(f"  Cases found: {len(cases_map)}")
print(f"  Statutes found: {len(statutes_map)}")
print(f"  Constitutional refs found: {len(const_refs_map)}")
print(f"  Am. Jur. refs found: {len(amjur_refs_map)}")

# ── STEP 2 — Build Am. Jur. search index ────────────────────────────────────
print("\nStep 2: Building Am. Jur. search index...")

# Parse section numbers from text
SECTION_RE = re.compile(r'§\s*(\d+(?:\.\d+)?)')
# Case in Am. Jur. text: Name v. Name, reporter
AMJUR_CASE_RE = re.compile(
    r'\b([A-Z][a-zA-Z\'\-\.]{1,30}(?:\s+[A-Z][a-zA-Z\'\-\.]{1,30}){0,3})\s+v\.\s+'
    r'([A-Z][a-zA-Z\'\-\.]{1,30}(?:\s+[A-Z][a-zA-Z\'\-\.]{1,30}){0,3})'
    r'(?:\s*,\s*\d+)',
)
DOCTRINAL_PHRASES = [
    'notwithstanding', 'null and void', 'liberally construed',
    'cannot be converted', 'right of the people', 'supremacy', 'repugnan',
]

amjur_index = []  # list of dicts with image, pages, sections, cases, doctrinal, text

for img_key, entry in transcription.items():
    pages_field = entry.get('pages', '')
    text = entry.get('text', '')

    # Extract section numbers
    sections = [f"§ {s}" for s in SECTION_RE.findall(text)]
    # Deduplicate preserving order
    seen = set()
    sections_dedup = []
    for s in sections:
        if s not in seen:
            seen.add(s)
            sections_dedup.append(s)

    # Extract page number range from pages field
    page_match = re.search(r'pp?\.\s*([\d\-–]+)', pages_field)
    page_range = page_match.group(0) if page_match else pages_field[:60]

    # Extract cases
    img_cases = []
    for m in AMJUR_CASE_RE.finditer(text):
        p = m.group(1).strip()
        d = m.group(2).strip()
        if is_valid_case_name(p) and is_valid_case_name(d):
            img_cases.append(normalize_case_key(p, d))

    # Extract doctrinal sentences
    doctrinal_hits = []
    text_lower = text.lower()
    for phrase in DOCTRINAL_PHRASES:
        if phrase in text_lower:
            # Find sentence containing phrase
            idx = text_lower.find(phrase)
            start = max(0, idx - 150)
            end = min(len(text), idx + 150)
            snippet = text[start:end].replace('\n', ' ').strip()
            doctrinal_hits.append({'phrase': phrase, 'snippet': snippet})

    amjur_index.append({
        'image': img_key,
        'pages': pages_field,
        'page_range': page_range,
        'sections': sections_dedup[:20],  # cap
        'cases': img_cases,
        'doctrinal_hits': doctrinal_hits,
        'text': text,
    })

print(f"  Am. Jur. index entries: {len(amjur_index)}")

# ── STEP 3 — Match citations to Am. Jur. sources ────────────────────────────
print("\nStep 3: Matching citations to Am. Jur. sources...")

def search_amjur(terms, window=300):
    """
    Search all Am. Jur. image entries for any of the given terms (case-insensitive).
    Returns list of match dicts: image, pages, sections, text_excerpt.
    """
    results = []
    for entry in amjur_index:
        text = entry['text']
        text_lower = text.lower()
        for term in terms:
            term_lower = term.lower()
            idx = text_lower.find(term_lower)
            if idx >= 0:
                start = max(0, idx - window)
                end = min(len(text), idx + len(term) + window)
                excerpt = text[start:end].replace('\n', ' ').strip()
                if start > 0:
                    excerpt = '…' + excerpt
                if end < len(text):
                    excerpt = excerpt + '…'
                results.append({
                    'image': entry['image'],
                    'pages': entry['pages'],
                    'am_jur_sections': entry['sections'],
                    'text_excerpt': excerpt[:800],  # cap excerpt length
                })
                break  # one match per image entry per citation
    return results

def make_case_search_terms(norm_key):
    """Generate search term variants for a case name."""
    # norm_key like "marbury v. madison"
    parts = norm_key.split(' v. ')
    if len(parts) != 2:
        return [norm_key]
    p, d = parts
    terms = []
    # Title-case variants
    pt = p.title()
    dt = d.title()
    terms.append(f"{pt} v. {dt}")
    terms.append(f"{pt} v {dt}")
    # Last name only for plaintiff
    p_last = p.split()[-1].title()
    d_last = d.split()[-1].title()
    terms.append(f"{p_last} v. {d_last}")
    # Original case key title-cased
    terms.append(norm_key.title())
    return terms

# Known correct citation forms for common cases Carl Miller mentions
KNOWN_CITATIONS = {
    'marbury v. madison': 'Marbury v. Madison, 5 U.S. (1 Cranch) 137 (1803)',
    'mcculloch v. maryland': "McCulloch v. Maryland, 17 U.S. (4 Wheat.) 316 (1819)",
    "m'culloch v. maryland": "McCulloch v. Maryland, 17 U.S. (4 Wheat.) 316 (1819)",
    'cohens v. virginia': 'Cohens v. Virginia, 19 U.S. (6 Wheat.) 264 (1821)',
    'martin v. hunter': "Martin v. Hunter's Lessee, 14 U.S. (1 Wheat.) 304 (1816)",
    'yick wo v. hopkins': 'Yick Wo v. Hopkins, 118 U.S. 356 (1886)',
    'yick v. hopkins': 'Yick Wo v. Hopkins, 118 U.S. 356 (1886)',
    'hurtado v. california': 'Hurtado v. California, 110 U.S. 516 (1884)',
    'holden v. hardy': 'Holden v. Hardy, 169 U.S. 366 (1898)',
    'muller v. oregon': 'Muller v. Oregon, 208 U.S. 412 (1908)',
    'calder v. bull': 'Calder v. Bull, 3 U.S. (3 Dall.) 386 (1798)',
    'chisholm v. georgia': 'Chisholm v. Georgia, 2 U.S. (2 Dall.) 419 (1793)',
    'miranda v. arizona': 'Miranda v. Arizona, 384 U.S. 436 (1966)',
    'mapp v. ohio': 'Mapp v. Ohio, 367 U.S. 643 (1961)',
    'terry v. ohio': 'Terry v. Ohio, 392 U.S. 1 (1968)',
    'weeks v. united states': 'Weeks v. United States, 232 U.S. 383 (1914)',
    'boyd v. united states': 'Boyd v. United States, 116 U.S. 616 (1886)',
    'miranda v. state of arizona': 'Miranda v. Arizona, 384 U.S. 436 (1966)',
    'norton v. shelby county': 'Norton v. Shelby County, 118 U.S. 425 (1886)',
    'vanhorne v. dorrance': 'Vanhorne v. Dorrance, 2 U.S. (2 Dall.) 304 (1795)',
    'ellingham v. dye': 'Ellingham v. Dye, 178 Ind. 336 (1912)',
    'ware v. hylton': 'Ware v. Hylton, 3 U.S. (3 Dall.) 199 (1796)',
    'jones v. securities': 'Jones v. Securities & Exchange Commission, 298 U.S. 1 (1936)',
}

# ── Build citation entries ────────────────────────────────────────────────────
all_citations = []
ref_counter = {'case': 0, 'amendment': 0, 'statute': 0, 'const_ref': 0, 'am_jur': 0}

# Chunk reference index
chunk_ref_index = {str(c['chunk_num']): [] for c in cm_chunks}

def register_ref(ref_id, mentions):
    """Add ref_id to chunk_ref_index for each mentioned chunk."""
    for mention in mentions:
        cn = str(mention['chunk_num'])
        if cn in chunk_ref_index and ref_id not in chunk_ref_index[cn]:
            chunk_ref_index[cn].append(ref_id)

# ── Cases ────────────────────────────────────────────────────────────────────
print("  Processing cases...")
for norm_key, info in sorted(cases_map.items()):
    ref_counter['case'] += 1
    ref_id = f"CM_CASE_{ref_counter['case']:03d}"

    search_terms = make_case_search_terms(norm_key)
    am_jur_sources = search_amjur(search_terms)

    corrected = KNOWN_CITATIONS.get(norm_key, None)
    # Try a few more key variants
    if corrected is None:
        for k, v in KNOWN_CITATIONS.items():
            if norm_key.startswith(k) or k.startswith(norm_key):
                corrected = v
                break

    entry = {
        'ref_id': ref_id,
        'type': 'case',
        'normalized_key': norm_key,
        'raw_spoken_variants': sorted(info['raw_variants']),
        'corrected_citation': corrected,
        'carl_miller_mentions': info['mentions'],
        'am_jur_sources': am_jur_sources,
        'mapped': len(am_jur_sources) > 0,
    }
    all_citations.append(entry)
    register_ref(ref_id, info['mentions'])

# ── Amendments ───────────────────────────────────────────────────────────────
print("  Processing amendments...")
for norm_key, info in sorted(amendments_map.items()):
    ref_counter['amendment'] += 1
    ref_id = f"CM_AMEND_{ref_counter['amendment']:03d}"
    ordinal = info['ordinal']
    word = ORDINAL_TO_WORD.get(ordinal, str(ordinal))

    # Build search terms for this amendment
    search_terms = AMENDMENT_AMJUR_TERMS.get(ordinal, [f"{word} Amendment"])

    am_jur_sources = search_amjur(search_terms)

    entry = {
        'ref_id': ref_id,
        'type': 'amendment',
        'normalized_key': norm_key,
        'ordinal': ordinal,
        'amendment_name': f"{word} Amendment",
        'raw_spoken_variants': sorted(info['raw_variants']),
        'carl_miller_mentions': info['mentions'],
        'am_jur_sources': am_jur_sources,
        'mapped': len(am_jur_sources) > 0,
    }
    all_citations.append(entry)
    register_ref(ref_id, info['mentions'])

# ── Statutes ─────────────────────────────────────────────────────────────────
print("  Processing statutes...")
for norm_key, info in sorted(statutes_map.items()):
    ref_counter['statute'] += 1
    ref_id = f"CM_STAT_{ref_counter['statute']:03d}"

    search_terms = list(info['raw_variants'])
    am_jur_sources = search_amjur(search_terms)

    entry = {
        'ref_id': ref_id,
        'type': 'statute',
        'normalized_key': norm_key,
        'raw_spoken_variants': sorted(info['raw_variants']),
        'carl_miller_mentions': info['mentions'],
        'am_jur_sources': am_jur_sources,
        'mapped': len(am_jur_sources) > 0,
    }
    all_citations.append(entry)
    register_ref(ref_id, info['mentions'])

# ── Constitutional refs ──────────────────────────────────────────────────────
print("  Processing constitutional refs...")
for norm_key, info in sorted(const_refs_map.items()):
    ref_counter['const_ref'] += 1
    ref_id = f"CM_CONST_{ref_counter['const_ref']:03d}"

    # Supremacy clause / Article 6 Para 2 → search for supremacy
    search_terms = list(info['raw_variants'])
    norm_lower = norm_key.lower()
    if 'article' in norm_lower and ('6' in norm_lower or 'vi' in norm_lower):
        search_terms += ['supremacy', 'notwithstanding', 'Supremacy of Acts']
    elif 'article' in norm_lower and ('2' in norm_lower or 'ii' in norm_lower):
        search_terms += ['executive power', 'President']

    am_jur_sources = search_amjur(search_terms)

    entry = {
        'ref_id': ref_id,
        'type': 'const_ref',
        'normalized_key': norm_key,
        'raw_spoken_variants': sorted(info['raw_variants']),
        'carl_miller_mentions': info['mentions'],
        'am_jur_sources': am_jur_sources,
        'mapped': len(am_jur_sources) > 0,
    }
    all_citations.append(entry)
    register_ref(ref_id, info['mentions'])

# ── Am. Jur. refs ────────────────────────────────────────────────────────────
print("  Processing Am. Jur. refs...")
for norm_key, info in sorted(amjur_refs_map.items()):
    ref_counter['am_jur'] += 1
    ref_id = f"CM_AMJUR_{ref_counter['am_jur']:03d}"

    search_terms = ['11 Am. Jur.', 'American Jurisprudence', 'Constitutional Law']
    am_jur_sources = search_amjur(search_terms)
    # For Am. Jur. refs, just take first 3 matches
    am_jur_sources = am_jur_sources[:3]

    entry = {
        'ref_id': ref_id,
        'type': 'am_jur',
        'normalized_key': norm_key,
        'raw_spoken_variants': sorted(info['raw_variants']),
        'carl_miller_mentions': info['mentions'],
        'am_jur_sources': am_jur_sources,
        'mapped': len(am_jur_sources) > 0,
    }
    all_citations.append(entry)
    register_ref(ref_id, info['mentions'])

# ── STEP 4 — Compute summary stats ──────────────────────────────────────────
total = len(all_citations)
mapped = sum(1 for c in all_citations if c['mapped'])
unmapped = total - mapped

type_counts = defaultdict(lambda: {'total': 0, 'mapped': 0})
for c in all_citations:
    t = c['type']
    type_counts[t]['total'] += 1
    if c['mapped']:
        type_counts[t]['mapped'] += 1

# ── STEP 5 — Write output ────────────────────────────────────────────────────
print("\nStep 5: Writing output...")

output = {
    'metadata': {
        'created': datetime.datetime.now().isoformat(),
        'description': 'Carl Miller citation map — every citation/reference in the lecture mapped to its source passage in 11 Am. Jur. Constitutional Law',
        'carl_miller_source': 'consolidated_corpus.json (Carl Miller Teachings chunks)',
        'reference_source': 'transcription_progress.json (11 Am. Jur. Constitutional Law, pp. 604–1185)',
        'total_unique_citations': total,
        'total_mapped': mapped,
        'total_unmapped': unmapped,
        'breakdown_by_type': {
            t: {'total': v['total'], 'mapped': v['mapped']}
            for t, v in sorted(type_counts.items())
        },
    },
    'citations': all_citations,
    'chunk_reference_index': chunk_ref_index,
}

# Convert sets to lists for JSON serialization
def make_serializable(obj):
    if isinstance(obj, set):
        return sorted(obj)
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_serializable(i) for i in obj]
    return obj

output = make_serializable(output)

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nOutput written to: {OUTPUT_PATH}")

# ── Print summary ────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Total unique citations extracted : {total}")
print(f"Mapped to Am. Jur. source(s)     : {mapped}")
print(f"Unmapped                         : {unmapped}")
print(f"Mapping rate                     : {mapped/total*100:.1f}%")
print()
print("Breakdown by type:")
for t, v in sorted(type_counts.items()):
    pct = v['mapped']/v['total']*100 if v['total'] else 0
    print(f"  {t:<14} total={v['total']:3d}  mapped={v['mapped']:3d}  ({pct:.0f}%)")

print()
print("Top 20 cases extracted:")
case_entries = [(c['normalized_key'], len(c['carl_miller_mentions']), c['mapped'])
                for c in all_citations if c['type'] == 'case']
case_entries.sort(key=lambda x: -x[1])
for key, mentions, is_mapped in case_entries[:20]:
    print(f"  {'[MAPPED]' if is_mapped else '[-----]'} {key} ({mentions} mention{'s' if mentions!=1 else ''})")

print()
print("Chunks with most references:")
chunk_refs_sorted = sorted(chunk_ref_index.items(), key=lambda x: -len(x[1]))
for cn, refs in chunk_refs_sorted[:10]:
    print(f"  Chunk {cn:>3}: {len(refs)} refs -> {refs[:5]}")
