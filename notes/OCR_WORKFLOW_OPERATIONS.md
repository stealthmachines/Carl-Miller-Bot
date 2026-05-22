# OCR WORKFLOW OPERATIONS
**Status**: Active | **Last Updated**: 2026-05-22

---

## CORPUS STATUS (Current Authoritative Sources)

| Document | Canonical Source | Fallback | Status |
|----------|-----------------|---------|--------|
| 11 Am. Jur. 1st Ed. Constitutional Law | `Carl Miller/Corpus_Processed/MASTER/11AmJur1D.json` (3.4 MB) | ~~IMG_2xxx images~~ (deprecated) | ✅ Complete |
| 16 Am. Jur. 2d Constitutional Law (1964) | `Carl Miller/Corpus_Processed/citation_mapped_corpus.json` | `Carl Miller/Original Documents/16AmJur2d_images/img_01..img_62.jpeg` | ✅ Integrated |

> **NOTE**: The `IMG_2xxx` iCloud photo set is **deprecated**. All 11AmJur content has been processed into `11AmJur1D.json`. Do not re-process these images.

---

## SESSION RESUME PROCEDURE

If context is lost or LM Studio restarts:

```
1. get_context()                              # Reload system state
2. notes_read "OCR_WORKFLOW_OPERATIONS"       # This file
3. notes_read "OCR_REFERENCE_KNOWLEDGE"       # Domain expertise + protocols
4. notes_read "OCR_PROGRESS_LOG"              # What's been done
5. notes_read "MCP_ERL_SYSTEM"               # Server/tool capabilities
```

For active image work (16AmJur2d fallback processing only):
```
notes_read "OCR_WORKFLOW_OPERATIONS"  → Step: IMAGE PROCESSING WORKFLOW below
```

---

## IMAGE PROCESSING WORKFLOW
*(For new image OCR — primary corpus is JSON, this only applies if images must be processed directly)*

### Step 1: Enhance Image
```bash
magick "PATH\img_NN_<hash>.jpeg" -resize 800%x800% -filter Lanczos "PATH\img_NN_MAGNIFIED.jpg"
# If "Image too small to scale": use -resize 300%x300% or 400%x400%
```

### Step 2: OCR
```bash
"C:\Program Files\Tesseract-OCR\tesseract.exe" "PATH\img_NN_MAGNIFIED.jpg" "PATH\img_NN_RAW" -l eng -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,;:!?()-@[]$%&*+=<>?/|"
```

### Step 3: Context-Aware Transcription
- Apply legal syntax knowledge (see `OCR_REFERENCE_KNOWLEDGE`)
- Fix OCR errors using section numbering patterns
- Preserve left/right page markers: `=== LEFT PAGE ===` / `=== RIGHT PAGE ===`
- Maintain cross-reference format (supra, infra, see, see also)
- Verify section number sequences

### Step 4: Save
```
Output file: PATH\img_NN_PERFECTED.txt
```

Then append to the appropriate canonical JSON:
- **11AmJur content** → append entry to `Carl Miller/Corpus_Processed/MASTER/11AmJur1D.json`
- **16AmJur2d content** → run `Carl Miller/Other Scripts/integrate_16amjur2d.py`

Entry format for 11AmJur1D.json:
```json
{
  "IMG_NN_<hash>.jpeg": {
    "date": "YYYY-MM-DD",
    "pages": "[description]",
    "text": "[transcribed content]",
    "status": "completed",
    "confidence": "XX%",
    "method_used": "ImageMagick Lanczos 8x + Tesseract OCR + Legal Context",
    "notes": "[key discoveries, cross-references found]"
  }
}
```

---

## CROSS-REFERENCE VERIFICATION (Active During OCR)
1. Scan all `§ XX` references in each transcribed image
2. Verify `supra` references point to earlier sections
3. Verify `infra` references point to later sections
4. Flag missing/out-of-sequence sections as "pending"
5. Back-fill when the referenced section is later transcribed

---

## CONFLICT RESOLUTION
| Situation | Action |
|-----------|--------|
| OCR garbled | Use context from related transcriptions + section number sequence |
| Section number conflict | Check forward/backward progression in `11AmJur1D.json` |
| Cross-reference not found | Verify OCR; if still missing, flag in notes field |

---

## SESSION CORRECTION (Documented 2026-05-17)
- `transcription_progress2.json` was **not** being updated during an earlier session
- Separate `_PERFECTED.txt` files were created instead
- **Corrected methodology**: Always append to `transcription_progress2.json` AND save `_PERFECTED.txt`

---

## ERL CONTEXT MANAGEMENT
- Start: `erl_context_init(force=true)`
- Archive old context after large sessions: `erl_prune(branch="session_context", max_age_days=7)`
- Store session state: `memory_set("ocr_session_state", {...})`
