# MCP ERL SYSTEM
**Server**: local-mcp v3.0.0 | **ERL**: v3 | **Updated**: 2026-05-22

---

## CORE ARCHITECTURE

- **Endpoint**: `http://localhost:3333/sse` (primary) | `http://localhost:3334/sse` (dos)
- **Pattern**: Wu-Wei Unfold Architecture — FETCH→TRANSFORM→STORE→RESPOND (or other sequences)
- **FlowState**: Carries `cwd`, `env`, `data`, `last_path`, `last_url`, `browser_session` across passes
- **Tools**: 57 primitives across 14 capability groups

### Non-Negotiable Directives
1. **ALWAYS** call `get_context()` at session start
2. **ALWAYS** use `unfold()` for multi-step tasks
3. **NEVER** use `web_fetch()` for binary files (MP3/ZIP/PDF/images)
4. **NEVER** use `memory_set()` for persistent data — use `notes_write()` or `db_exec()`
5. **THINK** step by step; report what actually happened

---

## PERSISTENCE LAYERS

| Layer | Tool | Scope | Notes |
|-------|------|-------|-------|
| Memory | `memory_set/get` | Session-only | Lost on restart |
| Notes | `notes_write/read` | Persistent | Markdown in `./notes/` |
| Database | `db_exec/query` | Persistent | SQLite via `mcp-data.db` |
| ERL Ledger | `erl_append` + branches | Persistent | Hash-chained, `erl-ledger.json` |

---

## ERL v3 (Elegant Recursive Ledger)

- **Hash-chained**: SHA-256(parentID + timestamp + branch + content)
- **Branching**: Diverge from any entry; HEAD tracks tip per branch
- **Merging**: Linear replay (no diff conflicts)
- **Verification**: Cryptographic integrity check of entire chain

### Branch Structure
```
├── main (genesis)
├── session_context  HEAD → 1e663f2a...
│   ├── [1] 2026-05-17 Server initialized — MCP v3.0.0          (5173561a...)
│   ├── [2] 2026-05-17 Session guidance / system prompt         (205f1152...)
│   └── [3] 2026-05-22 Notes consolidation: 28→5 files  ← HEAD  (1e663f2a...)
├── twin_flame_probes
│   └── [1] 2026-05-17 Baseline probe                          (e6055e3d...)
├── twin_flame_evals
│   └── [1] 2026-05-17 Confidence-9 eval                       (9213d72e...)
└── task_* (diverge from session_context)
    └── Merge back when complete
```

### ERL Tools (6)
| Tool | Purpose |
|------|---------|
| `erl_history` | View branch history |
| `erl_search` | Search entries by content/role/tags |
| `erl_verify` | Verify cryptographic integrity |
| `erl_merge` | Merge one branch into another |
| `erl_create_branch` | Create new branches |
| `erl_append` | Add entries to branches |

### Auto-Initialization (server.js)
`erlStandardInit()` runs on server startup:
```
[ERL] Initializing standard session structure...
[ERL] ✓ Session context initialized with 2 foundational entries
[ERL] ✓ Ledger integrity verified
```

---

## ALL 57 TOOLS

**Shell**: `shell`, `shell_stream`
**Filesystem**: `fs_read`, `fs_write`, `fs_list`, `fs_delete`, `fs_stat`, `fs_search`
**Browser**: `browser_open`, `browser_navigate`, `browser_click`, `browser_fill`, `browser_screenshot`, `browser_extract`, `browser_close`
**Code**: `code_exec` (Python, Node, Bash)
**Database**: `db_query`, `db_exec`, `db_tables`, `db_export`
**Notes**: `notes_write`, `notes_read`, `notes_list`, `notes_delete`, `notes_search`
**Web**: `web_fetch`
**System**: `sysinfo`, `processes`, `process_kill`, `clipboard_read`, `clipboard_write`, `notify`
**Network**: `http_serve`, `http_serve_stop`
**Schedule**: `schedule_add`, `schedule_list`, `schedule_remove`
**Email**: `smtp_send`
**Telegram**: `tg_send`, `tg_listen`, `tg_inbox`, `tg_stop`
**Memory**: `memory_set`, `memory_get`, `memory_list`, `memory_delete`
**Env**: `env_get`, `env_list`, `process_info`

---

## VISION & OCR CAPABILITIES (Added 2026-05-17)

### Tools in server.js
| Tool | Purpose |
|------|---------|
| `ocr_transcribe` | Single image → text via Tesseract. Params: `image_path`, `output_format`, `language` |
| `vision_batch` | Multi-image directory processing |
| `legal_vision` | Advanced legal document understanding (structure, citations, cross-refs, metadata) |

### `legal_vision` — Returns
```json
{
  "document_type": "INDEX",
  "structure": {"has_index": true, "layout": "two_column"},
  "cross_references": {"infra": [...], "supra": [...], "section_refs": [...]},
  "metadata": {"publisher": "...", "page_number": "...", "volume": "..."},
  "interpretation": {"legal_concepts": [...], "topics_identified": [...]}
}
```

### Installation
```powershell
# Run as Administrator
choco install tesseract-ocr -y
```

### Correction Note (2026-05-17)
Prior to this date, some ERL entries falsely claimed vision/OCR existed. The tools were built fresh this session. Principle established: **"Always verify before claiming"** — check actual code before asserting capability.

---

## TOKEN EFFICIENCY

### Context Cleanup Procedure
When LM Studio context is high (>60%):
1. Click **"Clear all messages"** in LM Studio
2. Send: `load the MCP_ERL_SYSTEM note and summarize current capabilities`
3. Context drops from ~67% → ~5-10% utilization

**One-command automation** (if available):
```
erl_first_cleanup()
```

### Results Achieved (2026-05-04)
- Before: 63.2% context utilization
- After: ~5% context utilization
- **~58% token recovery**
- Mechanism: ERL v3 persistence + `session_context` branch stores all knowledge compactly

### Usage Pattern
```
1. get_context()                  # Load system state
2. unfold({ task: "..." })        # Do work
3. notes_write / db_exec          # Persist results (not memory_set)
4. [On cleanup] Clear messages → reload this note
```
