<img width="1659" height="852" alt="image" src="https://github.com/user-attachments/assets/0ed753ca-1cee-4de5-b111-8021181ea8d1" />
https://rumble.com/v2mz5wy-know-your-constitution-with-carl-miller-annotated.html
https://zchg.org/t/carl-miller-complete-including-16-am-jur-2d-constitutional-law-supplemental/530

ERROR is expected, express, and implied.  This is in BETA.  Do your own research.  NOT legal advice, & not intended to replace legal advice.

*Index Source — 11 Am. Jur. 1st Ed., Constitutional Law §§ 1–382 (1937)*

# Carl Miller Bot v5 — Legal Vision by zCHG.org

#### A fully agentic AI assistant specializing in constitutional law research — specifically the **repugnancy doctrine** and **severability analysis** as argued by Carl Miller.
Built on a Wu-Wei dual-MCP stack. Reads American Jurisprudence from fine-print photographic images. Pairs with LM Studio. Includes a "legal council" of up to two local LLMs + one cloud bot.

---

## Stack at a Glance

| Process | Port | File | Purpose |
|---------|------|------|---------|
| MCP Server A | 3333 | `server.js` | Primary tools + LLM bridge (57 tool primitives) |
| MCP Server B | 3334 | `server-dos.js` | Mirror — stochastic divergence |
| Coord-Proxy | 1233 | `coord-proxy.js` | Wu-Wei phi-routing (SOLO / RELAY / CHALLENGE) |
| Wu-Wei Daemon | — | `wuwei-routing/` | HDGL health writer |
| LM Studio | 1234 | *(external)* | **Never touch from code** |

```
Claude / Copilot
      │
      ├── MCP tools (SSE) ──► server.js :3333 ──► ERL ledger
      │                                        └► llm_query ──► LM Studio :1234
      └──────────────────────► server-dos.js :3334 (mirror)
                                    │
coord-proxy :1233 ─────────────────►│ phi-routes between :3333 / :3334 / :1234
```

# Single-Slot Mode Status

At this time, **single-slot mode supports only Slot 2 on port 3334**.

- Slot 1 / port 3333: not designated as the working single-slot target.
- Slot 2 / port 3334: only working single-slot target.

---

## Prerequisites

**None.** The installer handles everything.

---

## One-Click Install + Run

### Windows
Double-click **`INSTALL.bat`** — that's it.

### macOS / Linux
```bash
bash install.sh
```

What happens automatically:
1. **Node.js LTS** installed if missing (Windows: winget or MSI; macOS: Homebrew; Linux: NodeSource/apt/dnf/pacman)
2. **npm packages** installed
3. **LM Studio** downloaded and installed silently
4. **Qwen3.5-9B GGUF** (~4 GB) downloaded and imported into LM Studio
5. **LM Studio server** started on :1234, model loaded into memory
6. **MCP stack** started (server.js :3333 + server-dos.js :3334 + coord-proxy :1233)

### Install options
```bash
node install.mjs --no-launch     # install everything but don't start the stack yet
node install.mjs --skip-model    # skip the 4 GB download (model already present)
node install.mjs --status        # show what's installed and what's missing
```

---

## Already installed? (just start the stack)

```bash
# Windows
start.bat

# macOS / Linux
bash start.sh

# or directly
node launch.mjs
```

`launch.mjs` auto-detects whether the LM Studio server is running and starts it if not. If no models are loaded it triggers a background `lms load`.

### launch.mjs options
```bash
node launch.mjs --no-proxy              # skip coord-proxy (if LM Studio isn't running)
node launch.mjs --status                # probe all ports + list loaded LLMs
node launch.mjs --load-model MODEL_ID   # ask LM Studio to load a specific model
node launch.mjs --help
npm run status
```

**Requires Node.js ≥ 18 and npm. Nothing else.**

```powershell
# Windows — double-click start.bat, or:
node launch.mjs

# macOS / Linux:
bash start.sh
# or: chmod +x start.sh && ./start.sh

# npm:
npm start
```

On first run, `launch.mjs` will automatically run `npm install` if `node_modules` is missing.

Options:
```
node launch.mjs --no-proxy              # skip coord-proxy (if LM Studio isn't running)
node launch.mjs --status                # probe all ports + list loaded LLMs
node launch.mjs --load-model MODEL_ID   # ask LM Studio to load a model (v0.3.x+ API)
node launch.mjs --help
npm run status
```

Ctrl+C (or SIGTERM) shuts down all child processes cleanly.

---

## Carl Miller — Legal Corpus

The primary research domain is **Carl Miller's repugnancy and severability doctrine**:

- **Repugnancy doctrine** — a statute repugnant to the Constitution is void from inception (*Marbury v. Madison*, 1803: "a law repugnant to the constitution is void"), never having had legal force.
- **Severability** — Carl Miller argues most modern statutory schemes fail severability once the repugnant provision is removed, because that provision was central to legislative intent.
- **Primary authority** — 11 Am. Jur. 1st Ed. (1937, §§ 1–382) and 16 Am. Jur. 2d (1964).
- **Framers' intent** — interpreted via Samuel Johnson's Dictionary (1755/1756/1773 editions) and the Federalist / Anti-Federalist Papers.

### Primary Corpus *(query these first)*

| Source | Path | Notes |
|--------|------|-------|
| **11 Am. Jur. 1st Ed.** | `Carl Miller/Corpus_Processed/MASTER/11AmJur1D.json` | OCR of 351 images, §§ 1–382, 1937 ed. — canonical |
| Citation map | `Carl Miller/Corpus_Processed/citation_mapped_corpus.json` | 36 unique citations; 25 mapped to AmJur |
| Citations index | `Carl Miller/citations_index.json` | 6,126 citations, 3,255 unique cases |
| Transcript (JSON) | `Carl Miller/Carl's Transcript/carl-miller-transcript.json` | Full Carl Miller lecture corpus |
| Transcript (text) | `Carl Miller/Carl's Transcript/Carl-Miller-Merged-MASTER.txt` | Merged plain text |

### Processed Corpus *(enriched views)*

| Source | Path | Notes |
|--------|------|-------|
| Full corpus | `Carl Miller/Corpus_Processed/full_corpus.json` | 109 chunks, 328 definitions, entity extraction |
| Topic-indexed | `Carl Miller/Corpus_Processed/topic_indexed_corpus.json` | 9 topics: Supremacy_Clause, Contract_Theory, 5th/6th/7th/10th/2nd/4th Amendments |
| Definitions | `Carl Miller/Corpus_Processed/definitions.json` | 328 term-definition pairs with transcript context |
| Consolidated | `Carl Miller/Corpus_Processed/MASTER/consolidated_corpus.json` | 10 foundational docs + 123 Carl Miller chunks, deduplicated |
| Master corpus | `Carl Miller/Corpus_Processed/MASTER/master_corpus.json` | 117 chunks, YouTube + audio, 11 topics |
| Master merged | `Carl Miller/Corpus_Processed/MASTER/master_corpus_merged.json` | Merged + deduplicated master view |
| Unique entities | `Carl Miller/Corpus_Processed/MASTER/unique_entities.json` | Amendments, cases, terms, codes |

### MASTER Output Files *(generated)*

| File | Path | Description |
|------|------|-------------|
| `11AmJur1D.json` | `MASTER/` | Canonical OCR — keyed by image filename |
| `11AmJur1D.docx` | `MASTER/` | Structured Word document from JSON — headings, section headers, body text |
| `11AmJur1D.html` | `MASTER/` | HTML from DOCX; 7,754 `§-ref` hyperlinks gleaned from authoritative source HTML; 382 `id="sec-N"` anchor targets |

All three MASTER output files carry embedded copyright tags (JSON `_copyright` key; HTML `<meta>` + comment; DOCX `dc:rights`).

### Reference Materials

| Resource | Path | Notes |
|----------|------|-------|
| Foundational docs (text) | `Carl Miller/Original Documents/For Bot/` | 13 txt files (see below) |
| Samuel Johnson Dictionary | `Carl Miller/Corpus_Processed/Dictionary/` | Combined 1755/1756/1773 editions |
| Federalist Papers | `Carl Miller/Original Documents/misc/The-Complete-Federalist-Papers.pdf` | Full text |
| Anti-Federalist Papers | `Carl Miller/Original Documents/misc/TheAntiFederalistPapers.pdf` | Full text |
| Lieber Code (1863) | `Carl Miller/Original Documents/misc/General Orders No 100 The Lieber Code.pdf` | |
| 16 Am. Jur. 2d images | `Carl Miller/Original Documents/16AmJur2d_images/` | 62 JPEGs — fallback only |
| Human-readable PDFs/HTML | `Carl Miller/Original Documents/For Human/` | Constitution, Declaration, AmJur HTML, etc. |
| Authoritative AmJur HTML | `Carl Miller/Original Documents/For Human/AmJur1d_ConstitutionalLaw_Vol11.html` | Word-exported HTML; source of hyperlink map |

### Foundational Documents (`For Bot/`)

Magna Carta (1215) · Mayflower Compact (1620) · Declaration of Independence (1776) · Articles of Confederation (1781) · Northwest Ordinance (1787) · U.S. Constitution (1787) · Marbury v. Madison, 5 U.S. 137 (1803) · Missouri Compromise (1820) · `severability.txt`

### How to query the corpus

```js
// Read canonical AmJur OCR (keyed by image filename — e.g. "IMG_1780.JPEG")
fs_read({ path: "Carl Miller/Corpus_Processed/MASTER/11AmJur1D.json" })

// Search repugnancy / severability across processed corpus
fs_search({ path: "Carl Miller/Corpus_Processed", pattern: "repugnant|severab" })

// Read full transcript
fs_read({ path: "Carl Miller/Carl's Transcript/carl-miller-transcript.json" })

// Read legal_vision tool (OCR + corpus search)
legal_vision({ query: "repugnancy void ab initio Marbury" })
```

---

## ERL v3 — Hash-Chained Context Ledger

ERL (Emergent Reasoning Ledger) is a git-like hash-chained ledger stored in `erl-ledger.json`.

### Key properties

- **Phi-scored retrieval** — recency score uses `γ^k` decay (γ = 0.75, φ = 1.618 base constant)
- **Concurrent write safety** — spinlock via `erl-ledger.json.lock`
- **Merkle checkpoints** — root computed every 50 appends (`CHECKPOINT_INTERVAL`)
- **Branches** — `main`, `session_context`, `twin_flame_evals`, `twin_flame_probes`, `triad_session`
- **ERL merge** — deterministic merge with conflict detection

### Internal functions (Node.js)

| Function | Purpose |
|----------|---------|
| `erlAppend(ledger, { branch, role, content, tags })` | Append entry; returns entry with SHA-256 id |
| `erlBranch(ledger, { name, from_branch })` | Create branch |
| `erlHistory(ledger, { branch, limit })` | Retrieve recent entries |
| `erlVerify(ledger)` | Hash-chain integrity check |
| `erlSearch(ledger, { query, branch })` | Phi-scored semantic search |
| `erlMerge(ledger, { source, target })` | Merge two branches |
| `getLedger()` | Thread-safe read with spinlock |
| `erlSave(ledger)` | Thread-safe write with spinlock |

### MCP tools (callable over SSE)

`erl_append`, `erl_history`, `erl_search`, `erl_verify`, `erl_merge`, `erl_create_branch`, `context_save`, `context_retrieve`, `erl_fold`, `erl_cleanup`, `legal_vision`

---

## MCP Tool Reference (key tools)

### `llm_query`

Direct LLM inference through LM Studio. Logs response to ERL by default.

```json
{
  "prompt": "Your question",
  "model": "qwen3.5-9b@q3_k_xl:2",
  "max_tokens": 200,
  "temperature": 0.7,
  "log": true,
  "branch": "session_context"
}
```

Returns `{ response, prompt_hash, logged_to_erl, model, tokens }`.

**Timeout**: 90 000 ms. The first inference after a reboot is slow — do not lower below 90s.

**Safety rule**: Never call `llm_query` from `Promise.all` across multiple *different* model names simultaneously. LM Studio will evict the first model when the second request loads.

### `twin_flame_eval`

Log a self-evaluation for a model response. Schema is identical on both ports.

```json
{
  "confidence": 8,
  "response_summary": "brief description",
  "prompt": "original prompt",
  "model": "qwen3.5-9b@q3_k_xl:2",
  "branch": "twin_flame_evals",
  "tags": ["custom"]
}
```

Returns `{ logged, branch, entry_id, confidence }`.

### `twin_flame_probe`

Known-answer baseline + drift detection. Stores question/answer pairs and tracks hash drift over time.

### `twin_flame_divergence`

Compare the last N eval entries across both servers to measure response divergence.

### `phi_route`

Get the phi-routing decision for a prompt: `SOLO` (< 0.382), `RELAY` (0.382–0.618), or `CHALLENGE` (> 0.618).

---

## Demo Scripts

### `_twin_demo.mjs` — 2-voice stochastic divergence

Two instances of the same model answer the same question. Because sampling is non-deterministic, responses diverge even with identical weights. Measures **stochastic divergence** — how much randomness/temperature contributes to answer variance.

```powershell
node _twin_demo.mjs
```

### `_triad_demo.mjs` — 3-voice conversation

Three voices answer the same question. Responses are logged to ERL and a thematic alignment check is run.

- **Voice A** — `qwen3.5-9b@q3_k_xl:2` on port 3333
- **Voice B** — `qwen3.5-9b@q3_k_xl` on port 3334
- **Voice C** — GitHub Copilot (inline — no local endpoint needed)

```powershell
# Default run:
node _triad_demo.mjs

# Custom models (any LM Studio hot models):
node _triad_demo.mjs --modelA mistral-7b --modelB llama-3-8b

# Custom question:
node _triad_demo.mjs --question "What is the most important property of a distributed system?"

# Skip Copilot voice (2-model mode):
node _triad_demo.mjs --no-copilot

# Tune generation:
node _triad_demo.mjs --temp 0.9 --max-tokens 300
```

If a model is offline, its voice is skipped gracefully — the triad degrades to a duo without crashing.

### `_probe.mjs` — single-shot probe

Fire individual MCP tool calls for testing and inspection.

---

## Coord-Proxy — Wu-Wei Phi-Routing

`coord-proxy.js` (port 1233) sits between your client and LM Studio, routing requests based on a phi-hash of the prompt content:

| Score | Mode | Behaviour |
|-------|------|-----------|
| < 0.382 | SOLO | Forward directly to LM Studio :1234 |
| 0.382–0.618 | RELAY | Send to server A, relay result to server B for enrichment |
| > 0.618 | CHALLENGE | Send to both servers, have them evaluate each other |

```
phiScore = (sha256(prompt)[0:8] / 0xFFFFFFFF × φ) % 1
```

Distribution converges to φ-emergent proportions: **61.8% SOLO / 23.6% RELAY / 14.6% CHALLENGE**.

Check status:
```powershell
Invoke-RestMethod http://localhost:1233/status
```

---

## Architecture: 3 Mechanisms, Not Slop

Three multi-LLM mechanisms exist in this stack. They are not duplicates — they operate at different layers:

| Mechanism | Layer | Purpose |
|-----------|-------|---------|
| `_twin_demo.mjs` | Demo script | Measure stochastic variance between two samples of the same model |
| `_triad_demo.mjs` | Demo script | Explicit 3-voice conversation: 2 local LLMs + Copilot as participant |
| `coord-proxy.js` | Production routing | SOLO/RELAY/CHALLENGE phi-routing — routes traffic, not a conversation script |

The proxy is the actual production architecture. The demo scripts are measurement tools that use the same underlying transport.

---

## Phi Foundation & Analog-Prime Connection

This stack shares a mathematical foundation with the [Analog-Prime `conscious` platform](https://github.com/stealthmachines/Analog-Prime):

**PHI = 1.6180339887498948482** is the governing constant in both systems.

| This stack | Analog-Prime conscious |
|------------|----------------------|
| ERL recency decay: `γ^k`, γ = 0.75 | HDGL `Dₙ(r)` resonance: `√(φ·Fₙ·2ⁿ·Pₙ·Ω)·r^((n+1)/8)` |
| `phiHash(content) % 1` routing thresholds | Slot4096 phi-lattice bucket assignment |
| SOLO/RELAY/CHALLENGE tri-split | Markov trit gate: −1 / 0 / +1 (REJECT / UNCERTAIN / ACCEPT) |
| Three-voice triad convergence check | Kuramoto 8D oscillator phase-lock (`S(U) ≈ 1.531`) |
| ERL hash-chaining | PCR-style hash chains in PhiKernel |
| Wu-Wei routing (5 compression strategies) | Wu-Wei codec: WW_NONACTION / WW_GENTLE_STREAM / WW_BALANCED_PATH / WW_FLOWING_RIVER / WW_REPEATED_WAVES |

The **Markov trit gate** (−1/0/+1) is genuine tri-state logic — the same reason this stack avoids binary evaluations and uses 1–10 confidence scores. The three-voice triad demo is a digital analog of the Kuramoto synchronisation lock: each voice converges on an answer independently; the divergence metric measures how far apart the phases are.

---

## Safety Rules

1. **Never `Promise.all` across different model names** toward LM Studio — eviction kills one model.
2. **Never auto-discover models** with parallel probes — use confirmed names from the LM Studio UI.
3. **`llm_query` timeout is 90 000 ms** — first inference post-reboot can be slow.
4. **Port 1234 is LM Studio** — never send non-inference traffic; never restart it from code.

---

## File Map

```
── Root ──────────────────────────────────────────────────────────────────────
server.js              MCP Server A — port 3333 (57 tool primitives)
server-dos.js          MCP Server B — port 3334 (mirror)
coord-proxy.js         Wu-Wei phi-routing proxy — port 1233
launch.mjs             Cross-platform one-click launcher (auto-installs deps)
launch_final.mjs       Hardened launcher variant
chat.mjs               Interactive chat entry point
chat_final.mjs         Hardened chat variant
start.bat              Windows double-click → node launch.mjs
start.sh               macOS/Linux → node launch.mjs
start-all.ps1          Legacy PowerShell launcher (Windows only, still works)
start-server.js        Simple process wrapper
install.mjs            Zero-to-running installer (Node + LM Studio + model)
INSTALL.bat            Windows one-click installer
install.sh             macOS/Linux installer
install-bootstrap.ps1  PowerShell bootstrap helper
tools_erl.js           ERL v3 tool exports
tools_cleanup.js       ERL fold / cleanup utilities
erl-ledger.json        Live hash-chained ERL ledger
mcp.json               LM Studio SSE config (points to :3333 / :3334)
package.json           Node dependencies
SYSTEM_PROMPT.md       Full system prompt — paste into LM Studio
SYSTEM_CONTEXT.md      Human-readable context snapshot
SYSTEM_CONTEXT.json    Machine-readable context snapshot
VERSIONS_final.md      Chronological version history (v0.4 → current)
LICENSE                Copyright notice — zCHG.org / Josef Kulovany
_twin_demo.mjs         2-voice stochastic divergence demo
_triad_demo.mjs        3-voice conversation demo (CLI-configurable)
_probe.mjs             Single-shot MCP tool probe

── wuwei-routing/ ────────────────────────────────────────────────────────────
router-phi.ps1         Phi-hash router script
start-routes.ps1       Route daemon (health checks every 30 s)
start.bat              Windows start helper
logs/                  Routing logs
state/                 Active server state + health files

── notes/ ────────────────────────────────────────────────────────────────────
MCP_ERL_SYSTEM.md      ERL v3 spec, branch structure, tool reference
OCR_PROGRESS_LOG.md    OCR pass log — 11 Am. Jur. image set (IMG_1771–IMG_2122)
OCR_REFERENCE_KNOWLEDGE.md  OCR methodology and quality notes
OCR_WORKFLOW_OPERATIONS.md  Operational OCR workflow
ROUTING_ARCHITECTURE.md     Dual-server + coord-proxy topology

── scripts/ ──────────────────────────────────────────────────────────────────
convert_11AmJur1D.cjs  JSON → DOCX → HTML pipeline (links from authoritative HTML)
tag_copyright_MASTER.cjs  Embed copyright tags into JSON/HTML/DOCX in MASTER/
repair_html_qmarks*.cjs   HTML question-mark artifact repair pipeline (v1–v4d)
enhance_html.cjs       HTML enhancement utilities
update_html_from_json.cjs  Sync HTML from JSON edits
_analyze_remaining.cjs  Corpus gap analysis
_debug_search.cjs      Corpus search debugger
_spot_check.cjs        Random section spot-check
_verify_enhance.cjs    Verification pass
(+ other diagnostic scripts)

── Carl Miller/ ──────────────────────────────────────────────────────────────
citations_index.json        6,126 citations, 3,255 unique cases
Complete_Corpus_All_Documents.py  Corpus build script

Carl Miller/Carl's Transcript/
  Carl-Miller-Merged-MASTER.txt      Merged plain-text transcript
  carl-miller-transcript.json        Structured transcript corpus
  Carl-Miller-Whisper-citation-corrected.txt
  Carl-Miller-Whisper-Orig.txt       Original Whisper output

Carl Miller/Corpus_Processed/
  full_corpus.json                   109 chunks, 328 definitions
  topic_indexed_corpus.json          9-topic indexed view
  definitions.json                   328 term-definition pairs
  citation_mapped_corpus.json        36 citations mapped to AmJur
  Dictionary/                        Samuel Johnson 1755/1756/1773 combined
  MASTER/
    11AmJur1D.json    ← canonical OCR (351 images, §§ 1–382, 1937 ed.)
    11AmJur1D.docx    ← generated DOCX (structured headings + body)
    11AmJur1D.html    ← generated HTML (7,754 §-ref hyperlinks injected)
    consolidated_corpus.json         10 foundational docs + 123 Carl Miller chunks
    master_corpus.json               117 chunks, 11 topics
    master_corpus_merged.json        Merged + deduplicated master
    unique_entities.json             Amendments, cases, terms, codes

Carl Miller/Original Documents/
  For Bot/            13 txt foundational docs (Constitution, Declaration, Marbury, etc.)
  For Human/          AmJur HTML, PDFs (Constitution, Declaration, articles, NW Ordinance…)
  misc/               Federalist Papers, Anti-Federalist Papers, Lieber Code
  16AmJur2d_images/   62 JPEG fallback images (16 Am. Jur. 2d)
```

---

## Ports Summary

| Port | Process | Notes |
|------|---------|-------|
| 3333 | `server.js` | Primary MCP server |
| 3334 | `server-dos.js` | Mirror MCP server |
| 1233 | `coord-proxy.js` | Wu-Wei routing proxy |
| 1234 | LM Studio | External — **never modify** |

---

## Current Hot Models

```
qwen3.5-9b@q3_k_xl:2   ← instance 2, persistent
qwen3.5-9b@q3_k_xl     ← instance 1, reload if evicted after reboot
```

Check LM Studio's **Loaded Models** tab before running any demo.

---

## Host Requirements

| Tool | Version | Notes |
|------|---------|-------|
| Node.js | ≥ 18 | Required |
| npm | ≥ 9 | Required |
| Python | 3.10+ | Corpus scripts |
| LM Studio | any | External — manages model serving |
| ffmpeg | any | Audio processing (optional) |
| git | any | Recommended |

---

## Copyright & License

```
COPYRIGHT NOTICE - All original works retain the copyright of their original owners.
All else, as applicable, are copyright Josef Kulovany and zCHG.org pursuant but not
limited to https://zchg.org/t/legal-notice-copyright-applicable-ip-and-licensing-read-me/440

ALL APPLICABLE RIGHTS RESERVED.

https://zchg.org/ — https://josefkulovany.com/law
```

This repo does not have the authority to usurp its parent licensing:
https://zchg.org/t/legal-notice-copyright-applicable-ip-and-licensing-read-me/440

Special thanks to LM Studio.

Want a license? Write to **charg.chg.wecharg@gmail.com**

