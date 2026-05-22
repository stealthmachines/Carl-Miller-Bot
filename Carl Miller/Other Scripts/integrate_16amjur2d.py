"""
integrate_16amjur2d.py
Integrates 16 Am. Jur. 2d Constitutional Law (1964) image-sourced sections into
citation_mapped_corpus.json.

Section mapping (16 Am. Jur. 2d images version → Carl Miller's version of 16 Am. Jur. 2d):
  Images §97  → Carl §62
  Images §98  → Carl §57 (also §51)
  Images §114 → Carl §78
  Images §155 range → Carl §105-110 range
  Images §255 → Carl §176
  Images §256 → Carl §177
  Images §257 → Carl §178
  Images §258 → Carl §179
  Images §259 → Carl §180
  Images §260 → Carl §181
  (§165, §176-181 unchanged between versions)

Images directory: 16AmJur2d_images/img_NN_<hash>.jpeg
Edition: Volume 16 American Jurisprudence 2nd Edition, Constitutional Law, 1964,
         Jurisprudence Publishers, Inc. ("Completely Revised and Rewritten in the
         Light of Modern Authorities and Developments")
"""

import json, sys, copy
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:/Users/Owner/Downloads/Legal-Vision-main/Legal-Vision-main/Carl Miller'
CORPUS_PATH = BASE + '/Corpus_Processed/citation_mapped_corpus.json'
OUT_PATH    = BASE + '/Corpus_Processed/citation_mapped_corpus.json'  # overwrite in-place

# ── Section mapping table ─────────────────────────────────────────────────────
# Maps images-version section numbers to Carl's-version section numbers
SECTION_MAP_IMG_TO_CARL = {
    97: 62,    # Tests for self-executing provisions
    98: 57,    # Addressed to legislature (also 51)
    114: 78,   # Limiting function of federal appellate courts
    255: 176,  # [Executive power / distribution of powers]
    256: 177,
    257: 178,
    258: 179,
    259: 180,
    260: 181,
}
# §155 range (images) → §105-110 range (Carl)
# §165, §176-181 unchanged

# ── 16 Am. Jur. 2d source entries (from image readings) ──────────────────────
# Format mirrors am_jur_sources but adds "edition" key.
IMG_DIR = '16AmJur2d_images'

SOURCES_16 = {
    'sec_97_98': {
        'image': IMG_DIR + '/img_19_987165db37e8529fdf2724eba1f58a8e50660f0e.jpeg',
        'edition': '16 Am. Jur. 2d Constitutional Law (1964)',
        'carl_sections': ['§62', '§57'],
        'am_jur_sections': ['§97', '§98'],
        'text_excerpt': (
            '§ 97. Generally. [Tests for self-executing provisions.] One of the recognized '
            'rules is that a constitutional provision is not self-executing if, although it '
            'is briefly stated, the subject of it requires further legislation to bring it '
            'into effect and cannot be enjoyed without such legislation. A constitutional '
            'provision is not self-executing where it does not supply sufficient rules by '
            'which the right conferred may be enjoyed and protected, without the aid of '
            'legislative enactment. '
            '§ 98. Addressed to legislature. A constitutional provision which depends upon '
            'legislative action for its effectuation is ipso facto not self-executing. In '
            'determining whether a provision is directly operative or not self-executing, '
            'one issue is whether the language is addressed to the courts or to the '
            'legislature. A provision that the legislature shall make suitable provisions '
            'for carrying a constitutional amendment into effect is obviously addressed to '
            'the legislature and is indicative of the intention that such amendment shall '
            'not become effective until made so by an act of the legislature.'
        ),
    },
    'sec_114': {
        'image': IMG_DIR + '/img_27_6eff9f91c289bb53533237b8a5830c2b9aaa0a6d.jpeg',
        'edition': '16 Am. Jur. 2d Constitutional Law (1964)',
        'carl_sections': ['§78'],
        'am_jur_sections': ['§114'],
        'text_excerpt': (
            '§ 114. Limiting function of Federal Appellate Courts and decision of '
            'constitutional issues. Every question of constitutional law presented for '
            'determination in a case before the Supreme Court will be decided in the most '
            'limited manner possible, on the narrowest grounds. The Federal Courts will '
            'decide the constitutionality of a statute only if and insofar as it is '
            'necessary to do so to decide the case before the court. Federal courts do '
            'not proceed to the constitutional question until it appears there are no '
            'other grounds upon which the case may be decided.'
        ),
    },
    'sec_115_118': {
        'image': IMG_DIR + '/img_28_de56d452dfd82ddc828be6311da360495228767d.jpeg',
        'edition': '16 Am. Jur. 2d Constitutional Law (1964)',
        'carl_sections': ['§78', '§79', '§80', '§81'],
        'am_jur_sections': ['§115', '§116', '§117', '§118'],
        'text_excerpt': (
            '§ 115. Generally. [Rules for raising constitutional questions.] A decision '
            'sustaining the constitutionality of a statute cannot be rendered in a case '
            'unless the record discloses facts and circumstances upon which the question '
            'of constitutionality is presented for determination. Where the constitutionality '
            'of a statute has not been properly raised, the court will not consider it. '
            '§ 116. Pleading. Courts should not voluntarily pass upon constitutional questions '
            'which need not be decided, although unconstitutionality need not be specially '
            'pleaded. § 117. Administrative and stipulation. Constitutionality is not a '
            'matter the administrative bodies can determine. § 118. [Stipulations by parties.] '
            'Parties cannot stipulate as to the interpretation of a constitution, and a '
            'stipulation will not bind the court as to constitutional questions.'
        ),
    },
    'sec_165': {
        'image': IMG_DIR + '/img_35_3bdd94b0f6cac7b334f2455fa37813ceb70fcb05.jpeg',
        'edition': '16 Am. Jur. 2d Constitutional Law (1964)',
        'carl_sections': ['§165'],
        'am_jur_sections': ['§165'],
        'text_excerpt': (
            '§ 165. [Validity of statutes — generally.] The court cannot declare a statute '
            'void in consequence of alleged improper motives which led to its enactment; '
            'courts look to the enactment, not the motives of the legislature. The general '
            'presumption of validity means that courts will uphold a statute unless its '
            'unconstitutionality is plainly demonstrated. When a statute is brought up '
            'against constitutional challenges, there is always a presumption of validity '
            'in favor of the act of the legislature; courts must be satisfied beyond '
            'reasonable doubt before declaring a statute unconstitutional.'
        ),
    },
    'sec_172_173': {
        'image': IMG_DIR + '/img_38_2c647be9d10bdb9b84ccf574ad3fb4ef0c6216d2.jpeg',
        'edition': '16 Am. Jur. 2d Constitutional Law (1964)',
        'carl_sections': ['§172', '§173'],
        'am_jur_sections': ['§172', '§173'],
        'text_excerpt': (
            '§ 172. Burden of proof. In consequence of the general presumption of the '
            'validity of acts of the legislature as being in accord with the constitution, '
            'there is a presumption that the person relying upon unconstitutionality has '
            'the burden of proof. The party who alleges unconstitutionality has the burden '
            'of establishing invalidity beyond a reasonable doubt. The rule is that a '
            'statute is presumed to be constitutional until proven otherwise, and the '
            'court will not substitute its judgment for that of the legislature unless '
            'the unconstitutionality is clear, plain, and manifest. '
            '§ 173. Judicial self-restraint in exercising power. Judges should observe '
            'the most careful consideration to questions involving the validity and '
            'application of the legislation, and should approach such questions with '
            'great circumspection and circumspection, exercising their power with '
            'great delicacy and restraint.'
        ),
    },
    'sec_176_177': {
        'image': IMG_DIR + '/img_44_5812a6574367d9b4f8366c0233b4639cc3f3bc09.jpeg',
        'edition': '16 Am. Jur. 2d Constitutional Law (1964)',
        'carl_sections': ['§176', '§177'],
        'am_jur_sections': ['§176', '§177'],
        'text_excerpt': (
            '§ 176. [Partial unconstitutionality — proof.] A statute shown to be '
            'unconstitutional is void. The party challenging constitutionality must prove '
            'the facts clearly. Where the invalidity of a portion is shown, the invalidity '
            'of the portion does not necessarily render the remainder void. '
            '§ 177. Generally. [Partial unconstitutionality.] Although it is conceded that '
            'an unconstitutional provision in a statute is not cured or healed by its '
            'coexistence with a valid provision, the general rule is that an '
            'unconstitutional provision in a statute is not fatal to the whole statute, '
            'and the valid parts may stand if they are severable from the invalid parts. '
            'An unconstitutional provision may be rejected and the remainder upheld if '
            'the constitutional and unconstitutional portions are not so intertwined as '
            'to make it apparent that the legislature would not have enacted the statute '
            'without the objectionable provision.'
        ),
    },
    'sec_178': {
        'image': IMG_DIR + '/img_45_258d45f4c3d859c28653c463ec3c3f8ab3c3958a.jpeg',
        'edition': '16 Am. Jur. 2d Constitutional Law (1964)',
        'carl_sections': ['§178'],
        'am_jur_sections': ['§178'],
        'text_excerpt': (
            '§ 178. Protection of rights. The actual existence of a statute prior to a '
            'determination that it is unconstitutional is an operative fact and may have '
            'consequences which cannot justly be ignored; when a statute has been in '
            'effect for some time, questions of rights claimed to have become vested, of '
            'status, of prior determinations deemed to have finality, and acted upon, are '
            'not to be disregarded in the light of the nature both of the statute and of '
            'its prior operation. The general rule is that an unconstitutional act of the '
            'legislature protects no one. It is said that all persons are presumed to know '
            'the law, meaning that the law excuses no one; if any person acts under an '
            'unconstitutional enactment, he does so at his peril and must take the '
            'consequences. Rights acquired under an unconstitutional statute while it is '
            'duly adjudged to be constitutional are valid legal rights protected by the '
            'constitutional right not to have those rights taken without due process of law.'
        ),
    },
    'sec_179_181': {
        'image': IMG_DIR + '/img_46_57d56686613b83da47d3f7aa43723d67d13e5ef1.jpeg',
        'edition': '16 Am. Jur. 2d Constitutional Law (1964)',
        'carl_sections': ['§179', '§180', '§181'],
        'am_jur_sections': ['§179', '§180', '§181'],
        'text_excerpt': (
            '§ 179. Validation generally by amendment to legislation. A statute that '
            'is invalid because it is in conflict with the state constitution may be '
            'rendered valid by amendment of the constitution, as far as reasonable. '
            'On the other hand, the rule is that a statute cannot be made valid '
            'retroactively against one who has already acquired rights under its '
            'invalid provisions. '
            '§ 180. [Validation by subsequent legislation.] An unconstitutional statute '
            'cannot be made valid by subsequent legislation authorizing it or providing '
            'that it shall take effect upon the adoption of such a constitutional amendment. '
            '§ 181. Partial Unconstitutionality; In General. [Severability rule.] '
            'Although it is conceded that an unconstitutional provision in a statute '
            'is not cured or healed by its coexistence with a valid provision, the '
            'constitutional portion of the statute may be preserved where the '
            'unconstitutional portion is severable. A court will presume that if the '
            'legislature had foreseen the invalidity, it would have desired the '
            'remainder of the act to be given effect.'
        ),
    },
    'sec_255_256': {
        'image': IMG_DIR + '/img_60_36a8c16f56eab8430caeaf966430cbb6a102b198.jpeg',
        'edition': '16 Am. Jur. 2d Constitutional Law (1964)',
        'carl_sections': ['§176', '§177'],
        'am_jur_sections': ['§255', '§256'],
        'text_excerpt': (
            '§ 255. [Executive power — international affairs.] The national government '
            'is sovereign in foreign affairs, and the President has broad constitutional '
            'authority over international relations. In the absence of a conflicting act '
            'of Congress, the President may act in international affairs on behalf of '
            'the nation. '
            '§ 256. Vesting discretionary power in judiciary. An apparent exception to '
            'the general rule forbidding the delegation of legislative power to the courts '
            'exists in cases where much discretion is conferred upon the courts. The '
            'legislature cannot delegate its general legislative power to the judiciary, '
            'but it may confer discretionary authority in the administration of laws, '
            'and courts are often vested with discretion as to the manner of proceeding, '
            'the extent of the remedy, and similar matters. Whether a power granted by '
            'statute to the courts is legislative in character is determined by whether '
            'its exercise requires a finding of facts or is purely a policy decision.'
        ),
    },
    'sec_257_260': {
        'image': IMG_DIR + '/img_61_39f8e72b374cdd0a44e98d0b60e81d95d82dfc86.jpeg',
        'edition': '16 Am. Jur. 2d Constitutional Law (1964)',
        'carl_sections': ['§178', '§179', '§180', '§181'],
        'am_jur_sections': ['§257', '§258', '§259', '§260'],
        'text_excerpt': (
            '§ 257. [Incomplete delegation.] A statute which delegates to an officer '
            'the power to determine whether certain contingencies have occurred is not '
            'an improper delegation of legislative power if the statute itself provides '
            'sufficient standards. The delegation is valid if it is accompanied by '
            'adequate standards or guidelines. '
            '§ 258. Effect of laws on contingencies. It is well settled that the '
            'legislature may make a law to take effect upon the happening of a future '
            'contingency or event. The legislature may enact a general law while '
            'providing that it takes effect upon the occurrence of a specified contingency, '
            'and such contingency may be the subject of control by human agencies. '
            '§ 259. [Contingency for effectiveness.] A statute providing for its own '
            'effectiveness upon a future contingency does not delegate legislative power '
            'to the authority that determines whether the contingency has occurred. '
            '§ 260. Effect of laws as to contingencies on subdivision territories. '
            '[Statutes requiring approval of municipal voters or local authority as '
            'a condition of effectiveness.]'
        ),
    },
}

# ── Cases mapping from 16 Am. Jur. 2d image edition to relevant sections ──────
# Maps case ref_ids to the 16 Am. Jur. 2d sources most relevant to them
CASE_TO_16AMJUR_SOURCES = {
    # MAPPED cases — add 16 Am. Jur. 2d parallel sources
    'CM_CASE_000': ['sec_97_98', 'sec_114', 'sec_165'],   # Marbury v. Madison
    'CM_CASE_005': ['sec_178'],                             # Norton v. Shelby County
    'CM_CASE_006': ['sec_178'],                             # Miller v. United States
    'CM_CASE_001': ['sec_114', 'sec_97_98'],               # McCulloch v. Maryland

    # UNMAPPED cases — add source where the PRINCIPLE appears (not the case itself)
    # These cases postdate the 1964 edition or are not in the sections we have images of
    # (See mapping_note for details)
}

# ── Updated mapping notes for unmapped cases ─────────────────────────────────
UPDATED_MAPPING_NOTES = {
    'CM_CASE_008': (
        'Johnson v. Manhattan Railway Co. (1933) predates the 1964 edition of 16 Am. Jur. 2d '
        'but was not found in 11 Am. Jur. Constitutional Law (c.1937). The case concerns '
        'questions of equity jurisdiction and injunctive relief — topics that appear in '
        '16 Am. Jur. 2d but in equity-law volumes, not in the Constitutional Law volume.'
    ),
    'CM_CASE_012': (
        'Erie Railroad Co. v. Tompkins (1938) postdates 11 Am. Jur. (c.1937) and barely '
        'predates the 1964 edition of 16 Am. Jur. 2d. This landmark case abolished federal '
        'general common law; it would appear in sections on federal judicial power and '
        'distribution of powers. The 16 Am. Jur. 2d images cover §47-259 (constitutional '
        'construction, validity, and distribution of powers) but Erie Railroad — primarily '
        'a diversity/common law case — would appear in separate Am. Jur. volumes on '
        'Federal Courts and Federal Practice, not in the Constitutional Law volume.'
    ),
    'CM_CASE_013': (
        'Murdoch v. Pennsylvania (1943) predates the 1964 edition of 16 Am. Jur. 2d. '
        'This First Amendment case (striking down city licensing requirements for '
        'religious literature distribution) would appear in the Freedom of Religion '
        'and Freedom of Expression sections of 16 Am. Jur. 2d Constitutional Law. '
        'Those sections are beyond §300 in 16 Am. Jur. 2d and are not in the images '
        'available (which cover §47-259). The principle that an unconstitutional licensing '
        'ordinance provides no legal protection is directly stated in 16 Am. Jur. 2d §178 '
        '(img_45): "The general rule is that an unconstitutional act of the legislature '
        'protects no one... if any person acts under an unconstitutional enactment, he '
        'does so at his peril."'
    ),
    'CM_CASE_014': (
        'Shuttlesworth v. City of Birmingham (1963) barely predates the 1964 edition of '
        '16 Am. Jur. 2d. This First Amendment case (striking down permit requirements '
        'for demonstrations) would appear in Freedom of Assembly sections of 16 Am. Jur. 2d '
        'Constitutional Law, beyond §300, not in the available images (§47-259). '
        'Shuttlesworth appears in footnotes of §§115, 165, and 172 in the 16 Am. Jur. 2d '
        'images in the context of: raising constitutional questions (§115), invalidity '
        'of ordinances (§165), and burden of proof for unconstitutionality (§172).'
    ),
    'CM_CASE_015': (
        'Peterson v. City of Greenville (1963) barely predates the 1964 edition of '
        '16 Am. Jur. 2d. This civil rights case (state enforcement of private discrimination '
        'constitutes state action) would appear in Equal Protection and State Action sections '
        'of 16 Am. Jur. 2d, beyond §300, not in the available images (§47-259).'
    ),
    'CM_CASE_016': (
        'Shapiro v. Thompson (1969) postdates the 1964 edition of 16 Am. Jur. 2d '
        'Constitutional Law and therefore does not appear in it. This case would be '
        'covered in later supplemental pocket parts or in subsequent Am. Jur. 2d updates.'
    ),
    'CM_CASE_017': (
        'Miranda v. Arizona (1966) postdates the 1964 edition of 16 Am. Jur. 2d '
        'Constitutional Law. Miranda would appear in the Criminal Law and Due Process '
        'sections of 16 Am. Jur. 2d in later supplements or other volumes (Criminal Law, '
        'Evidence). Not present in the 1964 Constitutional Law volume.'
    ),
    'CM_CASE_018': (
        'United States v. Bishop (1973) postdates the 1964 edition of 16 Am. Jur. 2d '
        'Constitutional Law. This tax crime willfulness case does not appear in this edition.'
    ),
    'CM_CASE_019': (
        'Owen v. City of Independence (1980) postdates the 1964 edition of 16 Am. Jur. 2d '
        'Constitutional Law. This § 1983 municipal liability case would appear in later '
        'supplements or in 42 Am. Jur. 2d (Civil Rights). Not present in this edition.'
    ),
    'CM_CASE_020': (
        'Maine v. Thiboutot (1980) postdates the 1964 edition of 16 Am. Jur. 2d '
        'Constitutional Law. This § 1983 case would appear in later supplements. '
        'Not present in this edition.'
    ),
    'CM_REF_033': (
        '42 U.S.C. § 1983 as a statutory right of action for constitutional deprivations '
        'is discussed in 16 Am. Jur. 2d §178 (Protection of rights) in the context of '
        'rights acquired under unconstitutional statutes, and more specifically in '
        '42 Am. Jur. 2d (Civil Rights). The core principle — that a person deprived of '
        'constitutional rights under color of law has a remedy — is stated in 16 Am. Jur. '
        '2d §178: "Rights... acquired under an unconstitutional statute... are valid legal '
        'rights that are protected by the constitutional right not to have those rights '
        'taken without due process of law."'
    ),
}


def run():
    with open(CORPUS_PATH, encoding='utf-8', errors='replace') as f:
        corpus = json.load(f)

    # ── Update metadata ───────────────────────────────────────────────────────
    corpus['metadata']['updated'] = datetime.now().isoformat()
    corpus['metadata']['supplemental_source_16amjur2d'] = (
        'Volume 16 American Jurisprudence 2nd Edition, Constitutional Law, 1964, '
        'Jurisprudence Publishers, Inc. — "Completely Revised and Rewritten in the '
        'Light of Modern Authorities and Developments by the Editorial Staff of the '
        'Publishers." Images: 16AmJur2d_images/ directory (62 images, §47-§259). '
        'Note: 11 Am. Jur. (c.1937) remains the primary source per Carl Miller\'s '
        'own reference materials; 16 Am. Jur. 2d serves as parallel/supplemental.'
    )
    corpus['metadata']['section_map_16amjur2d'] = {
        'description': (
            'Section number cross-reference: 16 Am. Jur. 2d IMAGES version → '
            'Carl Miller\'s version of 16 Am. Jur. 2d (earlier/less-revised printing). '
            'Sections not listed here are the same number in both printings.'
        ),
        'images_to_carl': SECTION_MAP_IMG_TO_CARL,
        'carl_to_images': {v: k for k, v in SECTION_MAP_IMG_TO_CARL.items()},
        'notes': {
            '155_range': 'Images §155 range → Carl §105-110 range',
            '165': 'Same section number in both versions',
            '176-181': 'Same section number in both versions',
        }
    }
    corpus['metadata']['total_unmapped'] = sum(
        1 for c in corpus['citations'] if not c.get('mapped', True)
    )

    # ── Process each citation ─────────────────────────────────────────────────
    updated_count = 0
    note_updated  = 0

    for cit in corpus['citations']:
        ref_id = cit.get('ref_id', '')

        # Add 16 Am. Jur. 2d sources to existing mapped cases
        if ref_id in CASE_TO_16AMJUR_SOURCES:
            existing_images = {s.get('image', '') for s in cit.get('am_jur_sources', [])}
            for src_key in CASE_TO_16AMJUR_SOURCES[ref_id]:
                src = copy.deepcopy(SOURCES_16[src_key])
                if src['image'] not in existing_images:
                    cit.setdefault('am_jur_sources', []).append(src)
                    existing_images.add(src['image'])
                    updated_count += 1

        # Update mapping notes for unmapped cases
        if ref_id in UPDATED_MAPPING_NOTES:
            cit['mapping_note'] = UPDATED_MAPPING_NOTES[ref_id]
            note_updated += 1

    # ── Add 16 Am. Jur. 2d section index to top level ─────────────────────────
    corpus['amjur2d_section_index'] = {
        'edition': '16 Am. Jur. 2d Constitutional Law (1964)',
        'images_dir': '16AmJur2d_images/',
        'sections': {
            src_key: {
                'image':            src['image'],
                'am_jur_sections':  src['am_jur_sections'],
                'carl_sections':    src['carl_sections'],
                'text_excerpt':     src['text_excerpt'][:300] + '...',
            }
            for src_key, src in SOURCES_16.items()
        }
    }

    # ── Write output ──────────────────────────────────────────────────────────
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

    print(f'Updated: {OUT_PATH}')
    print(f'  16 Am. Jur. 2d sources added to existing citations: {updated_count}')
    print(f'  Mapping notes updated for unmapped cases:           {note_updated}')
    print(f'  Total citations: {len(corpus["citations"])}')
    print(f'  Mapped: {sum(1 for c in corpus["citations"] if c.get("mapped", True))}')
    print(f'  Unmapped: {sum(1 for c in corpus["citations"] if not c.get("mapped", True))}')
    print()
    print('Section mapping index (images version → Carl version):')
    for img_sec, carl_sec in SECTION_MAP_IMG_TO_CARL.items():
        print(f'  §{img_sec:3d} (images) → §{carl_sec} (Carl\'s version)')
    print('  §165, §176-§181: same in both versions')

if __name__ == '__main__':
    run()
