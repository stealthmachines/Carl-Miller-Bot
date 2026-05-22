# OCR REFERENCE KNOWLEDGE
**Project**: 11 Am. Jur. 1st Ed. + 16 Am. Jur. 2d + Samuel Johnson Dictionary | **Updated**: 2026-05-22

---

## SAMUEL JOHNSON DICTIONARY — Sub-Corpus

### Purpose
Provides period-accurate (18th-century) definitions to establish the Framers' original intent. Words are interpreted as they were understood at the time the Constitution and founding documents were written, not by modern statutory redefinition.

### Files in `Carl Miller/Corpus_Processed/Dictionary/`

| File | Contents | Use for |
|------|----------|---------|
| `samuel_johnson_dictionary.json` | **16,494 structured entries**; keys: `metadata`, `lexicon` (search indexes), `entries` (UPPERCASE headword → object) | Exact definition lookup by headword |
| `Samuel Johnson Dictionary Combined FINAL.txt` | 310,940 lines, ~13 MB; full A–Z plain text | Passage/context search, full entry text, surrounding context |
| `charmap.json` | 44 OCR character corrections (e.g. `ſ` → `f`, long-s substitutions) | OCR correction reference |
| `lexicon.json` | Search indexes: `s_words`, `s_midword`, `f_words` arrays | Fast partial-word lookup |

### Entry Schema (`entries[HEADWORD]`)
```json
{
  "headword": "REPUGNANT",
  "key": "REPUGNANT",
  "letter": "R",
  "pos": "/.  a.",
  "etymology": "[repugnans, Lat.]",
  "definitions": [
    { "n": 1, "text": "Contrary; opposite; inconsistent.", "citations": [] }
  ],
  "quality": "high",
  "raw": "..."
}
```

### Coverage
- Base: Vol 1 (1756) A–K + Vol 2 (1755) L–Z
- Supplemented by: Vol 1 (1773) HOCR + Vol 2 (1773) HOCR (gap-fill only)
- Edition label: "Combined OCR-corrected (v2_p8)"
- Entry count: **16,494**

### Usage Pattern
```js
// PREFERRED — structured lookup
const dict = JSON.parse(fs.readFileSync("Carl Miller/Corpus_Processed/Dictionary/samuel_johnson_dictionary.json", "utf8"))
const entry = dict.entries["REPUGNANT"]
// entry.definitions[0].text → "Contrary; opposite; inconsistent."

// FALLBACK — full-text passage search
// grep "REPUGNANT" "Samuel Johnson Dictionary Combined FINAL.txt"
```

### Legal Significance
- Headwords like REPUGNANT, CONSTITUTION, PERSON, RIGHTS, PROPERTY, LIBERTY provide 18th-century meanings
- Courts and constitutional scholars agree that founding-era definitions control over modern statutory meanings
- Carl Miller cites Johnson's Dictionary as the authoritative source for original-intent interpretation

---

---

## DOCUMENT STRUCTURE — 11 Am. Jur. 1st Ed.

- **Volume II**: Commerce TO Constitutional Law, §§ 1-382
- **Publication**: 1937, Bancroft-Whitney / Lawyers Co-operative Publishing Co.
- **Editors**: Willis A. Estrich (Editor in Chief), George S. Gulick (Managing Editor)
- **Format**: Index by topic with section references (§ XX)

### Key Section Ranges
| Topic | Section Range | Pages |
|-------|--------------|-------|
| Commerce Clause | §§ 63-66, 68-73, 131-133 | — |
| Constitutionality of Statutes | §§ 82-147 | — |
| Distribution of Powers | §§ 155-226 | — |
| Police Power | §§ 245-304 | — |
| Fundamental Rights | §§ 308-327 | — |
| Constitutional Law overview | §§ 1-382 | pp. 589-609 |

---

## CROSS-REFERENCE SYSTEM

### Types Found in 11 Am. Jur.
1. **Internal** — Within same volume: `"§ 114. See § 115 infra."` / `"See § 114 supra."`
2. **Inter-Volume** — `"See Volume 1, § 23"` / `"See 11 Am. Jur. 2d, Commerce, § 63"`
3. **Related Topics** — `"See also Police Power, supra"` / `"See Constitutional Limitations, infra"`
4. **See / See Also / But See / But See Also** — primary / supporting / contrary / additional contrary

### Verification Strategy (Active During OCR)
1. Scan all `§ XX` references in each transcribed image
2. Verify `supra` references point to earlier sections; `infra` to later
3. Confirm section number sequences are logical and increasing
4. Flag missing/out-of-sequence sections as "pending"
5. Back-fill when the referenced section is later transcribed

### Self-Correction Mechanism
- If reference to § 120 not yet transcribed → mark "pending"
- When § 120 is reached, verify the reference exists
- If still missing → flag as OCR error; update both transcriptions

### Expected Cross-Reference Patterns
- Section numbers increase throughout the volume
- Commerce §§ 63-78 → Police Power §§ 245-304 → Fundamental Rights §§ 308-346 → Constitutional Limitations §§ 347-382

---

## LEGAL SYNTAX & TRANSCRIPTION STANDARDS

### Common Legal Terms
| Term | Meaning |
|------|---------|
| supra | mentioned above |
| infra | mentioned below |
| et seq. | and the following sections |
| see | primary reference |
| see also | supporting material |
| but see | contrary/limiting authority |
| vested rights | rights already established |
| police power | state regulation authority |

### Citation Patterns
- Case: `Marbury v. Madison, 1 Cranch (U.S.) 137, 2 L.Ed. 60`
- Multiple cases: semicolon-separated; comma for page numbers
- Parallel citations: reporter abbreviations (U.S., L.Ed., S.Ct.)

### Transcription Quality Standards
1. Preserve exact section numbers (`§ XX`)
2. Maintain left/right page distinction (`=== LEFT PAGE ===` / `=== RIGHT PAGE ===`)
3. Keep cross-references intact (supra/infra/see)
4. Preserve indentation hierarchy
5. Correct OCR errors using legal context
6. Verify section number sequences

| Text type | Min. confidence |
|-----------|----------------|
| Clear text | 95% |
| Index pages | 90% |
| Dense legal text | 85% |

---

## OCR TECHNICAL APPROACH

### Recommended Pipeline (ImageMagick + Tesseract)
```bash
# Step 1: Upscale
magick "IMG_XXXX.JPEG" -resize 800%x800% -filter Lanczos "IMG_XXXX_MAGNIFIED.jpg"
# If error "Image too small": use 300% or 400%

# Step 2: OCR with character whitelist
"C:\Program Files\Tesseract-OCR\tesseract.exe" "IMG_XXXX_MAGNIFIED.jpg" "IMG_XXXX_RAW" \
  -l eng -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,;:!?()-@[]$%&*+=<>?/|"
```

### Multi-PSM Strategy
Try multiple PSM modes per image; compare confidence:
- **PSM 3** — Fully automatic page segmentation
- **PSM 6** — Uniform block of text
- **PSM 11** — Sparse text, find as much as possible

### Advanced Preprocessing (Python — when needed)
```python
import cv2

def preprocess_legal_image(image_path):
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    # 1. Detect & correct rotation (Hough line transform)
    # 2. Advanced denoising
    img = cv2.fastNlMeansDenoising(img, h=7, templateWindowSize=7, searchWindowSize=7)
    # 3. Adaptive thresholding (better than OTSU for uneven lighting)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 2)
    # 4. Contrast enhancement
    img = cv2.convertScaleAbs(img, alpha=1.8, beta=-10)
    return img
```

### Alternative Commercial OCR
If Tesseract quality is insufficient: Google Vision API, AWS Textract, or Adobe Acrobat OCR.

---

## EXAMPLE: IMG_2092 (Commerce Clause Index — 95% confidence)

**Technology used**: ImageMagick Lanczos 8x + Tesseract multi-PSM + context-aware corrections

**Key corrections applied**:
- Commerce Commission → Interstate Commerce Commission
- Transportation § references (§ 63, § 69, § 70) fixed
- Warehouses storage/sale references corrected
- Tobacco regulation §§ 100+ corrected
- Indian Tribes Commerce § 66 references fixed

**Sample transcribed output** (partial):
```
INDEX
COMMERCIAL AGENCY - continued
VAUDEVILLE BOOKING AS, § 64
VENUE
  ACTION TO ENFORCE ORDER § 18
  ACTS TO REVIEW ORDER OF § 1
VESTED RIGHT TO CARRY ON, § 71
VEHICLES
  (Vehicle) regulation of, § 73
WAREHOUSES
  REGULATIONS OF, GENERALLY
  TERMINATION OF SERVICES, § 76
VIOLATIONS OF NATURE OF CONTRACT, § 8, 251, 228
WATERS
  CONSERVATION OF STATES' STATE'S
```
