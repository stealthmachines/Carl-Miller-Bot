# OCR PROGRESS LOG
**Last Updated**: 2026-05-22 | **Project**: 11 Am. Jur. 1st Ed. + 16 Am. Jur. 2d

---

## 11 AM. JUR. 1ST EDITION — CANONICAL STATE
> **Primary source**: `Carl Miller/Corpus_Processed/MASTER/11AmJur1D.json` (3.4 MB)
> **Original images**: Deprecated (IMG_2xxx iCloud set). Do not process further.
> **Scope**: Volume II — Commerce through Constitutional Law, §§ 1-382, 1937 edition

### Images Transcribed (Historical Record — Pre-JSON Migration)
All of the following are now consolidated into `11AmJur1D.json`:

**Back-to-Front Index Pass (7 images)**
| Image | Content |
|-------|---------|
| IMG_2122 | Back cover / end matter (supplement indexing) |
| IMG_2121 | INDEX: Conspiracy §§ 1-58 (topics A-I) |
| IMG_2120 | INDEX: Conspiracy (continued, topics I-N) |
| IMG_2119 | INDEX: Conspiracy (continued, topics A-K) |
| IMG_2118 | INDEX: Commingling/Confusion §§ 1-13 |
| IMG_2117 | INDEX: Conflict of Laws — Wills §§ 169+ |
| IMG_2116 | INDEX: Conflict of Laws — Wills §§ 169-270 (domicile, trusts, foreign wills, etc.) |

**Forward Content Pass — Constitutional Law pp. 589-609 (13 images)**
| Image | Pages | Sections |
|-------|-------|---------|
| IMG_1783 | pp. 608-609 | §§ 8-10 |
| IMG_1782 | pp. 606-607 | §§ 6-7 |
| IMG_1781 | pp. 604-605 | §§ 4-5 |
| IMG_1780 | pp. 602-603 | §§ 1-3 |
| IMG_1779 | pp. 600-601 | §§ 308-382 (outline final pages) |
| IMG_1778 | pp. 598-599 | §§ 245-304 |
| IMG_1777 | pp. 596-597 | §§ 155-226 |
| IMG_1776 | pp. 594-595 | §§ 78-147 |
| IMG_1775 | pp. 592-593 | §§ 6-77 |
| IMG_1774 | pp. 590-591 | §§ 114-304 |
| IMG_1773 | p. 589 | §§ 1-77 (outline pages) |
| IMG_1772 | — | Copyright / editorial board |
| IMG_1771 | — | Title page |

**Also Completed (Earlier)**
- IMG_2092: Commerce Clause index (95% confidence)

---

## 16 AM. JUR. 2D CONSTITUTIONAL LAW (1964) — INTEGRATION STATE
> **Primary source**: `Carl Miller/Corpus_Processed/citation_mapped_corpus.json`
> **Image fallback**: `Carl Miller/Original Documents/16AmJur2d_images/img_01..img_62.jpeg` (62 images)
> **Integrated via**: `Carl Miller/Other Scripts/integrate_16amjur2d.py`
> **Edition**: Volume 16, Jurisprudence Publishers Inc. ("Completely Revised and Rewritten")

### Section Mapping (16AmJur2d images → Carl Miller's version)
| Images Version § | Carl's Version § | Topic |
|-----------------|-----------------|-------|
| §97 | §62 | Tests for self-executing provisions |
| §98 | §57 (also §51) | Addressed to legislature |
| §114 | §78 | Limiting function of federal appellate courts |
| §155 range | §105-110 range | — |
| §255-260 | §176-181 | Executive power / distribution of powers |
| §165, §176-181 | unchanged | — |

### Integration Status
✅ 62 images scanned and section-mapped
✅ Integrated into `citation_mapped_corpus.json`
✅ Images retained as fallback only — do not re-process unless JSON is corrupt

---

## CROSS-REFERENCE NETWORK (Established)
- **Conspiracy** volume → Evidence, Combination, Rape sections
- **Conflict of Laws** → Contracts (Vols 7-8), multiple volumes
- **Property topics** → Tenancy in common, chattel mortgages
- **Constitutional Law** §§ 1-382 systematically organized

---

## REMAINING WORK (11AmJur — if ever needed)
IMG_2115 through IMG_1784 (~327 images) were not individually OCR'd before the JSON migration. The `11AmJur1D.json` should cover the full document. If gaps are found in the JSON, individual images can be re-processed using the workflow in `OCR_WORKFLOW_OPERATIONS`.
