import json, sys, re, os
from datetime import datetime
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:/Users/Owner/Downloads/Legal-Vision-main/Legal-Vision-main/Carl Miller/Corpus_Processed'

with open(BASE + '/consolidated_corpus.json', encoding='utf-8') as f:
    corpus = json.load(f)
with open(BASE + '/transcription_progress.json', encoding='utf-8', errors='replace') as f:
    tp = json.load(f)

carl = next(d for d in corpus['documents'] if 'Carl Miller' in d['name'])
full_carl = [(c['chunk_num'], c['content']) for c in carl['chunks']]

# ── Am. Jur. search ─────────────────────────────────────────────────────────
def amjur_search(patterns, window=350):
    hits = []
    for pat_str in patterns:
        try:
            pat = re.compile(pat_str, re.I)
        except Exception:
            continue
        for img_key, entry in tp.items():
            text = entry.get('text', '')
            for m in pat.finditer(text):
                excerpt = text[max(0, m.start()-80):m.start()+window].replace('\n', ' ')
                secs = re.findall(r'§\s*(\d+)', text[max(0, m.start()-500):m.start()+500])
                if not any(h['image'] == img_key for h in hits):
                    hits.append({
                        'image': img_key,
                        'pages': entry.get('pages', ''),
                        'am_jur_sections': list(dict.fromkeys(f'§{s}' for s in secs)),
                        'text_excerpt': excerpt
                    })
    return sorted(hits, key=lambda h: h['image'])

# ── Carl Miller mention finder ───────────────────────────────────────────────
def find_mentions(patterns):
    mentions = []
    for cn, content in full_carl:
        for pat_str in patterns:
            try:
                pat = re.compile(pat_str, re.I)
            except Exception:
                continue
            for m in pat.finditer(content):
                ctx = content[max(0, m.start()-70):m.start()+len(m.group())+70]
                if not any(mn['chunk_num'] == cn for mn in mentions):
                    mentions.append({'chunk_num': cn, 'context': ctx})
                break
    return mentions

# ── Amendment sections in Am. Jur. ──────────────────────────────────────────
AMENDMENT_SEARCHES = {
    'First Amendment':    ['freedom of speech', 'freedom of religion', 'freedom of the press', 'first amendment', 'right to peaceably assemble'],
    'Second Amendment':   ['right to bear arms', 'keep and bear arms', 'second amendment', 'right of the people to keep'],
    'Fourth Amendment':   ['search and seizure', 'fourth amendment', 'unreasonable search', 'right of the people to be secure'],
    'Fifth Amendment':    ['fifth amendment', 'due process of law', 'self-incrimination', 'just compensation', 'grand jury indictment'],
    'Sixth Amendment':    ['sixth amendment', 'speedy trial', 'right to counsel', 'right of the accused', 'confrontation of witnesses'],
    'Seventh Amendment':  ['seventh amendment', 'right of trial by jury', 'common law', 'twenty dollars'],
    'Ninth Amendment':    ['ninth amendment', 'rights retained by the people', 'enumeration of rights'],
    'Tenth Amendment':    ['tenth amendment', 'powers not delegated', 'reserved to the states', 'police power of the state'],
    'Fourteenth Amendment': ['fourteenth amendment', 'equal protection', 'due process', 'privileges or immunities', 'citizenship'],
}

AMENDMENT_CARL_PATTERNS = {
    'First Amendment':    ['first amendment'],
    'Second Amendment':   ['second amendment', 'right to bear arms', 'keep and bear arms'],
    'Fourth Amendment':   ['fourth amendment', 'search and seizure'],
    'Fifth Amendment':    ['fifth amendment', 'self-incrimination', 'due process'],
    'Sixth Amendment':    ['sixth amendment', 'speedy trial', 'right to counsel'],
    'Seventh Amendment':  ['seventh amendment', 'trial by jury', 'common law jury'],
    'Ninth Amendment':    ['ninth amendment'],
    'Tenth Amendment':    ['tenth amendment', 'reserved to the states', 'police power'],
    'Fourteenth Amendment': ['fourteenth amendment', 'equal protection'],
}

# ── Constitutional references ────────────────────────────────────────────────
CONST_REFS = [
    {
        'key': 'article 6 paragraph 2 - supremacy clause',
        'corrected': 'U.S. Constitution, Article VI, Clause 2 (Supremacy Clause)',
        'note': 'The Constitution and laws made in pursuance thereof shall be the supreme law of the land.',
        'carl_patterns': ['article 6', 'supremacy clause', 'paragraph 2', 'supreme law of the land'],
        'amjur_patterns': ['supremacy clause', 'supreme law of the land', 'article vi.*clause 2', 'notwithstanding'],
    },
    {
        'key': 'ucc 1-207 - reservation of rights',
        'corrected': 'Uniform Commercial Code § 1-207 (Performance or Acceptance Under Reservation of Rights)',
        'note': 'Signing with UD and 1-207 without prejudice preserves all constitutional rights.',
        'carl_patterns': ['1-207', 'without prejudice', 'reservation of rights', 'ucc 1'],
        'amjur_patterns': ['reservation of rights', 'without prejudice', 'uniform commercial code'],
    },
    {
        'key': 'statute of frauds',
        'corrected': 'Statute of Frauds (Michigan: MCL 566.132)',
        'note': 'Contracts must be in writing to be enforceable. Carl Miller argues the Constitution is an enforceable written contract.',
        'carl_patterns': ['statute of frauds'],
        'amjur_patterns': ['statute of frauds'],
    },
    {
        'key': '42 u.s.c. section 1983',
        'corrected': '42 U.S.C. § 1983 (Civil action for deprivation of rights)',
        'note': 'Allows suits against persons acting under color of state law who deprive citizens of federal rights.',
        'carl_patterns': ['42.*1983', '1983.*civil rights'],
        'amjur_patterns': ['civil rights act', 'color of law', 'deprivation of rights'],
    },
    {
        'key': 'latches',
        'corrected': 'Doctrine of Laches',
        'note': 'A party who fails to timely assert a right loses all right to proceed.',
        'carl_patterns': ['latches', 'laches'],
        'amjur_patterns': ['laches', 'latches'],
    },
    {
        'key': '11 am. jur. constitutional law',
        'corrected': '11 American Jurisprudence, Constitutional Law',
        'note': 'The primary reference book Carl Miller was teaching from; photographed as transcription_progress.json.',
        'carl_patterns': ['am. jur', 'american jurisprudence'],
        'amjur_patterns': ['american jurisprudence', '11 am. jur'],
    },
]

# ── Case master table ─────────────────────────────────────────────────────────
CASES = [
    # key, corrected_citation, note, carl_patterns, amjur_patterns
    ('marbury v. madison',
     'Marbury v. Madison, 5 U.S. (1 Cranch) 137, 2 L. ed. 60 (1803)',
     'Foundational case: anything repugnant to/in conflict with the Constitution is null and void from inception. No court is bound to uphold it; no citizen is bound to obey it.',
     ['marbury v. madison', 'marbury vs. madison', 'marbury versus madison'],
     ['marbury v. madison', 'marbury.*1 cranch', '1 cranch.*137']),

    ('mcculloch v. maryland',
     'McCulloch v. Maryland, 17 U.S. (4 Wheat.) 316, 4 L. ed. 579 (1819)',
     'Federal supremacy; states cannot tax federal instruments. Cited re: Erie Railroad argument.',
     ['mcculloch v. maryland', 'mcculloch versus maryland'],
     ['mcculloch v. maryland', '4 wheat.*316']),

    ('cohens v. virginia',
     'Cohens v. Virginia, 19 U.S. (6 Wheat.) 264, 5 L. ed. 257 (1821)',
     'Supreme Court has appellate jurisdiction over state court decisions on federal questions. Whisper: "cohen versus virginia six week two".',
     ['cohens? v. virginia', 'cohen versus virginia', 'cohen.*six week'],
     ['cohens v. virginia', '6 wheat.*264']),

    ('swift v. tyson',
     'Swift v. Tyson, 41 U.S. (16 Pet.) 1 (1842)',
     'Federal courts apply general common law independent of state decisions. Later overruled by Erie. Whisper: "Swift v. Tennyson".',
     ['swift v. t[ye]n', 'swift versus tyson', 'swift versus tennyson'],
     ['swift v. tyson', '16 pet.*1']),

    ('boyd v. united states',
     'Boyd v. United States, 116 U.S. 616, 29 L. ed. 746, 6 S. Ct. 524 (1886)',
     'Courts protect against any encroachments on constitutional rights. Liberal construction in favor of citizen.',
     ['boyd v. united states', 'boyd versus united states', r'\bboyd\b'],
     ['boyd v. united states', '116 u. s. 616']),

    ('norton v. shelby county',
     'Norton v. Shelby County, 118 U.S. 425, 30 L. ed. 178, 6 S. Ct. 1121 (1886)',
     'An unconstitutional act is not law; confers no rights, imposes no duties, affords no protection, creates no office.',
     ['norton v. shelby county', 'norton versus shelby county', 'norton.*shelby'],
     ['norton v. shelby county', '118 u. s. 425', 'norton.*shelby']),

    ('miller v. united states',
     'Miller v. United States, 78 U.S. (11 Wall.) 268, 20 L. ed. 135 (1870)',
     'Claim and exercise of a constitutional right cannot be converted into a crime.',
     ['miller v. united states', 'miller vs. united states'],
     ['miller v. united states.*11 wall', r'miller.*78 u\.?\s*s\.?\s*268']),

    ('united states v. cruickshank',
     'United States v. Cruikshank, 92 U.S. 542, 23 L. ed. 588 (1876)',
     'Rights are natural rights pre-existing the Constitution; government cannot abridge what it did not grant.',
     ['cruickshank', 'cruikshank'],
     ['cruickshank', 'cruikshank']),

    ('johnson v. manhattan railroad',
     'Johnson v. Manhattan Railway Co., 289 U.S. 479 (1933)',
     'Referenced by Carl Miller re: unlawful assertion of jurisdiction.',
     ['johnson v. manhattan', 'johnson versus manhattan'],
     ['johnson v. manhattan', 'manhattan railroad']),

    ('evans v. gore',
     'Evans v. Gore, 253 U.S. 245 (1920)',
     'Federal judges salaries and compensation clause argument.',
     ['evans v. gore', 'evans versus gore', 'evidence versus score', 'evans versus score'],
     ['evans v. gore', 'evans.*253 u']),

    ('pollock v. farmers loan',
     "Pollock v. Farmers' Loan & Trust Co., 157 U.S. 429, 15 S. Ct. 673 (1895)",
     'Income tax on property is a direct tax; must be apportioned. Used in Carl Miller income/tax arguments.',
     ["pollock v. farmers", 'pollock versus farmers', 'farmers loan'],
     ['pollock v. farmers', 'farmers loan', '157 u. s. 429']),

    ('mcnutt v. general motors',
     'McNutt v. General Motors Acceptance Corp., 298 U.S. 178, 56 S. Ct. 780 (1936)',
     'Burden on plaintiff to substantively prove jurisdiction; may never be assumed. Whisper: "56 Supreme Court 502".',
     ['mcnutt', 'nutt v. general motors'],
     ['mcnutt', r'298 u\.?\s*s\.?\s*178']),

    ('erie railroad v. tompkins',
     'Erie Railroad Co. v. Tompkins, 304 U.S. 64, 58 S. Ct. 817 (1938)',
     'Federal courts must apply state law in diversity cases; overruled Swift v. Tyson.',
     ['erie railroad', 'erie r.r.'],
     ['erie railroad', 'erie r. r.']),

    ('murdoch v. pennsylvania',
     'Murdoch v. Pennsylvania, 319 U.S. 105, 63 S. Ct. 870 (1943)',
     'No state may convert a secured liberty into a privilege and charge a license or fee for its exercise. Postdates Am. Jur.',
     ['murdoch v. penn', 'murdoch versus penn'],
     ['murdoch v. penn', 'murdoch.*pennsylvania']),

    ('shuttlesworth v. birmingham',
     'Shuttlesworth v. City of Birmingham, 373 U.S. 262 (1963)',
     'If state converts a right into a privilege, citizen may ignore the license and exercise the right with impunity. Postdates Am. Jur.',
     ['shuttlesworth', 'shuttlesford'],
     ['shuttlesworth']),

    ('peterson v. city of greenville',
     'Peterson v. City of Greenville, 373 U.S. 244, 83 S. Ct. 1119 (1963)',
     'State enforcement of racially discriminatory private practices is unconstitutional. Postdates Am. Jur.',
     ['peterson v. city of greenville', 'peterson.*greenville'],
     ['peterson v. city of greenville', 'peterson.*greenville']),

    ('shapiro v. thompson',
     'Shapiro v. Thompson, 394 U.S. 618, 89 S. Ct. 1322 (1969)',
     'Right to interstate travel is fundamental; state cannot arbitrarily burden it. Postdates Am. Jur. Whisper: "Shreveau versus Thompson".',
     ['shapiro v. thompson', 'shapiro versus thompson', 'shreveau versus thompson'],
     ['shapiro v. thompson', 'shapiro.*thompson']),

    ('miranda v. arizona',
     'Miranda v. Arizona, 384 U.S. 436, 86 S. Ct. 1602 (1966)',
     'Fifth Amendment rights during custodial interrogation; right to counsel; right to remain silent. Postdates Am. Jur.',
     ['miranda v. arizona', 'miranda versus arizona'],
     ['miranda v. arizona', 'miranda.*arizona']),

    ('united states v. bishop',
     'United States v. Bishop, 412 U.S. 346, 93 S. Ct. 2008 (1973)',
     'Willfulness requires evil motive or bad purpose; used for tax/criminal intent arguments. Postdates Am. Jur.',
     ['united states v. bishop', 'u.s. v. bishop', 'versus bishop', r'\bbishop\b.*412'],
     ['bishop.*412', 'united states.*bishop']),

    ('owen v. city of independence',
     'Owen v. City of Independence, 445 U.S. 622, 100 S. Ct. 1398 (1980)',
     '42 U.S.C. § 1983 municipal liability; cities have no good-faith immunity defense. Postdates Am. Jur.',
     ['owen v. city', 'owen versus city', 'owned versus city'],
     ['owen v. city', 'owen.*independence']),

    ('maine v. thiboutot',
     'Maine v. Thiboutot, 448 U.S. 1, 100 S. Ct. 2502 (1980)',
     '§ 1983 liability for violation of any federal statute. Postdates Am. Jur. Whisper: "Maine versus Thibodeau".',
     ['maine v. thibou', 'thibodeau', 'main versus thibodeau'],
     ['maine v. thiboutot', 'thiboutot', 'thibodeau']),
]

# ── Build citations ───────────────────────────────────────────────────────────
citations = []
chunk_ref_index = {str(c['chunk_num']): [] for c in carl['chunks']}
ref_counter = 0

# Cases
for (key, corrected, note, carl_pats, amjur_pats) in CASES:
    mentions = find_mentions(carl_pats)
    if not mentions:
        continue
    amjur_sources = amjur_search(amjur_pats)
    ref_id = f'CM_CASE_{ref_counter:03d}'
    ref_counter += 1
    citations.append({
        'ref_id': ref_id,
        'type': 'case',
        'normalized_key': key,
        'corrected_citation': corrected,
        'note': note,
        'carl_miller_mentions': mentions,
        'mention_count': len(mentions),
        'am_jur_sources': amjur_sources,
        'mapped': len(amjur_sources) > 0,
        'mapping_note': '' if amjur_sources else 'Not found in this 11 Am. Jur. volume (Constitutional Law, c.1937 ed.)'
    })
    for mn in mentions:
        cri = chunk_ref_index[str(mn['chunk_num'])]
        if ref_id not in cri:
            cri.append(ref_id)

# Amendments
for amend_name, amjur_pats in AMENDMENT_SEARCHES.items():
    carl_pats = AMENDMENT_CARL_PATTERNS.get(amend_name, [amend_name.lower()])
    mentions = find_mentions(carl_pats)
    if not mentions:
        continue
    amjur_sources = amjur_search(amjur_pats)
    ref_id = f'CM_AMEND_{ref_counter:03d}'
    ref_counter += 1
    citations.append({
        'ref_id': ref_id,
        'type': 'amendment',
        'normalized_key': amend_name.lower(),
        'corrected_citation': f'U.S. Constitution, {amend_name}',
        'note': '',
        'carl_miller_mentions': mentions,
        'mention_count': len(mentions),
        'am_jur_sources': amjur_sources,
        'mapped': len(amjur_sources) > 0,
        'mapping_note': ''
    })
    for mn in mentions:
        cri = chunk_ref_index[str(mn['chunk_num'])]
        if ref_id not in cri:
            cri.append(ref_id)

# Constitutional refs / statutes
for cr in CONST_REFS:
    mentions = find_mentions(cr['carl_patterns'])
    if not mentions:
        continue
    amjur_sources = amjur_search(cr['amjur_patterns'])
    ref_id = f'CM_REF_{ref_counter:03d}'
    ref_counter += 1
    citations.append({
        'ref_id': ref_id,
        'type': 'constitutional_reference',
        'normalized_key': cr['key'],
        'corrected_citation': cr['corrected'],
        'note': cr['note'],
        'carl_miller_mentions': mentions,
        'mention_count': len(mentions),
        'am_jur_sources': amjur_sources,
        'mapped': len(amjur_sources) > 0,
        'mapping_note': ''
    })
    for mn in mentions:
        cri = chunk_ref_index[str(mn['chunk_num'])]
        if ref_id not in cri:
            cri.append(ref_id)

# ── Stats ─────────────────────────────────────────────────────────────────────
total = len(citations)
mapped = sum(1 for c in citations if c['mapped'])
by_type = {}
for c in citations:
    t = c['type']
    if t not in by_type:
        by_type[t] = {'total': 0, 'mapped': 0}
    by_type[t]['total'] += 1
    if c['mapped']:
        by_type[t]['mapped'] += 1

print(f'Total citations: {total}')
print(f'Mapped: {mapped}  Unmapped: {total-mapped}')
for t, s in sorted(by_type.items()):
    print(f'  {t}: {s["mapped"]}/{s["total"]} mapped')
print()
for c in citations:
    print(f'  [{"mapped" if c["mapped"] else "     "}] {c["normalized_key"][:50]:50s}  x{c["mention_count"]:2d}  amjur={len(c["am_jur_sources"])}')

# ── Write output ──────────────────────────────────────────────────────────────
out = {
    'metadata': {
        'created': datetime.now().isoformat(),
        'description': (
            'Carl Miller citation & reference map — every case, amendment, statute, and constitutional '
            'reference spoken by Carl Miller, wrapped with its source passage from 11 Am. Jur. Constitutional Law '
            '(the reference book photographed in transcription_progress.json).'
        ),
        'carl_miller_source': 'consolidated_corpus.json (Carl Miller Teachings, 123 chunks)',
        'reference_source': 'transcription_progress.json (11 Am. Jur. Constitutional Law, pp. 604-1185, c.1937 ed.)',
        'total_unique_citations': total,
        'total_mapped': mapped,
        'total_unmapped': total - mapped,
        'note_on_unmapped': (
            'Cases not found in 11 Am. Jur. are generally post-1937 Supreme Court decisions '
            'that postdate this edition of American Jurisprudence.'
        ),
    },
    'citations': citations,
    'chunk_reference_index': chunk_ref_index,
}

out_path = BASE + '/citation_mapped_corpus.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

size_kb = os.path.getsize(out_path) / 1024
print(f'\nWritten: {out_path}  ({size_kb:.0f} KB)')
