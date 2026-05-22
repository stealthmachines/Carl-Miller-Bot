# Carl Miller Bot — MCP Server Context (v5)

## Bot Identity
- **Name**: Carl Miller Bot v5
- **Domain**: Constitutional law — repugnancy doctrine and severability analysis
- **Subject**: Carl Miller legal lectures and oral arguments

### Primary Corpus (canonical, query first)
| Key | Path | Notes |
|-----|------|-------|
| 11AmJur 1st Ed. | `Carl Miller/Corpus_Processed/MASTER/11AmJur1D.json` | OCR of 20 images, §§1–382, 1937 ed. |
| Citation map | `Carl Miller/Corpus_Processed/citation_mapped_corpus.json` | 36 unique citations, 25 mapped to AmJur |
| Citations index | `Carl Miller/citations_index.json` | 6,126 citations, 3,255 unique cases |
| Transcript | `Carl Miller/Carl's Transcript/carl-miller-transcript.json` | Full Carl Miller lecture corpus |

### Processed Corpus
| Key | Path | Notes |
|-----|------|-------|
| Full corpus | `Carl Miller/Corpus_Processed/full_corpus.json` | 109 chunks, 328 definitions |
| Topic-indexed | `Carl Miller/Corpus_Processed/topic_indexed_corpus.json` | 9 topics (Supremacy_Clause, Contract_Theory, etc.) |
| Definitions | `Carl Miller/Corpus_Processed/definitions.json` | 328 extracted term-definition pairs |
| Consolidated | `Carl Miller/Corpus_Processed/MASTER/consolidated_corpus.json` | 10 foundational docs + 123 Carl Miller chunks |
| Master corpus | `Carl Miller/Corpus_Processed/MASTER/master_corpus.json` | 117 chunks, YouTube + audio, 11 topics |

### Reference Materials
| Resource | Path | Notes |
|----------|------|-------|
| Foundational docs (text) | `Carl Miller/Original Documents/For Bot/` (13 files) | |
| **Samuel Johnson Dict. — structured** | `Carl Miller/Corpus_Processed/Dictionary/samuel_johnson_dictionary.json` | 16,494 entries; headword, pos, etymology, definitions, citations; editions 1755/1756/1773 combined |
| Samuel Johnson Dict. — full text | `Carl Miller/Corpus_Processed/Dictionary/Samuel Johnson Dictionary Combined FINAL.txt` | 310,940 lines, 13 MB; A–Z plain text; use for full-context passage lookup |
| Samuel Johnson Dict. — charmap | `Carl Miller/Corpus_Processed/Dictionary/charmap.json` | 44 OCR character corrections (e.g. ſ → f) |
| Samuel Johnson Dict. — lexicon index | `Carl Miller/Corpus_Processed/Dictionary/lexicon.json` | s_words / s_midword / f_words search indexes |
| Federalist Papers | `Carl Miller/Original Documents/misc/The-Complete-Federalist-Papers.pdf` |
| Anti-Federalist Papers | `Carl Miller/Original Documents/misc/TheAntiFederalistPapers.pdf` |
| 16AmJur2d images (fallback) | `Carl Miller/Original Documents/16AmJur2d_images/` (62 JPEGs) |

### Foundational Documents (in `For Bot/`)
Magna Carta (1215), Mayflower Compact (1620), Declaration of Independence (1776), Articles of Confederation (1781), Northwest Ordinance (1787), U.S. Constitution (1787), Marbury v. Madison (1803), Missouri Compromise (1820), severability.txt

- **Notes**: `notes/` (5 files: OCR_WORKFLOW_OPERATIONS, OCR_PROGRESS_LOG, OCR_REFERENCE_KNOWLEDGE, MCP_ERL_SYSTEM, ROUTING_ARCHITECTURE)

## Host
- OS: win32 (x64) | Windows: true
- Shell: cmd.exe
- CWD: `<project-root>` (machine-specific)
- User: `<local-user>` @ `<local-hostname>`

## Available Shell Tools
- ✓ node: v24.15.0
- ✓ npm: 11.12.1
- ✓ python: Python 3.10.6
- ✓ pip: pip 25.0.1
- ✓ git: git version 2.42.0.windows.1
- ✓ curl: curl 8.19.0 (Windows) libcurl/8.19.0 Schannel zlib/1.3.1 WinIDN WinLDAP
- ✓ wget: GNU Wget 1.25.0 built on cygwin.
- ✓ ffmpeg: ffmpeg version 8.0-essentials_build-www.gyan.dev Copyright (c) 2000-2025 the FFmpeg developers
- ✓ pwsh: PowerShell 7.6.1
- ✓ choco: 0.10.15
- ✓ winget: v1.28.240

## Missing Shell Tools
- ✗ whisper

## Agent Decision Tree
- 1. Is this the start of a session? → call get_context() first, always.
- 2. Does the task involve more than one step? → use unfold(). Do not chain primitives manually.
- 3. Does it involve a URL? → check if binary (mp3/zip/pdf/exe) → unfold(), never web_fetch for binary.
- 4. Does it involve audio/video/transcription? → unfold() → server selects Transcription River.
- 5. Is it one known single operation I'm certain about? → use the appropriate primitive directly.
- 6. Am I unsure which primitive to use? → use unfold() and describe the task.
- 7. Do I need to remember something across sessions? → notes_write or db_exec, not memory_set.
- 8. Is the task complete? → report what actually happened, including pass_results from unfold.

## Hard Rules
- ALWAYS call get_context at session start.
- ALWAYS use unfold() for multi-step tasks.
- NEVER use web_fetch for binary files (MP3, ZIP, PDF, images). Use unfold() or shell+curl.
- NEVER assume a tool works — check tool_capabilities[tool].status first.
- NEVER use memory_set for data that must survive a restart — use notes or db.
- If whisper is missing and transcription is needed, install it first: pip install openai-whisper
- If ffmpeg is missing and audio conversion is needed, install it first.

## Shell Guidance
- Python binary: python
- Download command: curl -L -o "<dest>" "<url>"
- ffmpeg: ✓
- whisper: ✗ not installed — pip install openai-whisper

## Pass Architecture
unfold() selects from these named strategies based on task signals:
- **Transcription River**: FETCH → TRANSFORM(ffmpeg) → TRANSFORM(whisper) → STORE → RESPOND
- **Download and Convert**: FETCH → TRANSFORM → STORE → RESPOND
- **Web Harvest**: FETCH → CODE → STORE → RESPOND
- **Pure Fetch**: FETCH → RESPOND
- **Browser Quest**: BROWSE → [STORE] → RESPOND
- **Code and Store**: CODE → STORE → RESPOND  (run/execute + save/write — checked before Shell Strike)
- **Installation Stream**: SHELL → SHELL → RESPOND
- **Shell Strike**: SHELL → RESPOND  (single execution, no save)
- **Write Then Read**: STORE → RECALL → RESPOND  (write file then read it back)
- **Memory River**: RECALL → [CODE] → RESPOND
- **File Read**: RECALL → RESPOND
- **Notification Wave**: [FETCH|SHELL] → NOTIFY → RESPOND
- **Non-Action**: RESPOND (direct answer, no tools needed)

## Recipes (this machine)
### download_binary
```
shell({ command: 'curl -L -o "%TEMP%\\file.mp3" "https://example.com/file.mp3"' })
```

### download_and_transcribe
```
// Step 1: unfold({ task: "download https://... to %TEMP%/file.mp3" })
// Step 2: shell({ command: "pip install openai-whisper" })
// Step 3: unfold({ task: "transcribe %TEMP%/file.mp3" })
```

### install_whisper
```
shell({ command: "python -m pip install openai-whisper" })
```

### install_ffmpeg
```
shell({ command: "choco install ffmpeg -y" })
```

### run_python
```
code_exec({ language: "python", code: "print('hello')" })
```

### browse_page
```
unfold({ task: "browse https://example.com and extract the main content" })
```

### save_to_db
```
db_exec({ sql: "CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, data TEXT, ts TEXT)" })
```

### telegram_send
```
Set TG_BOT_TOKEN env var first
```

### schedule_daily
```
schedule_add({ id: "daily_task", expression: "0 9 * * *", command: "echo daily" })
```

## Persistence
- **memory**: memory_set/get | persists: false | Session working state, temp values
- **notes**: notes_write/read | persists: true | Text output, transcripts, logs, markdown | path: `./notes`
- **database**: db_exec/query | persists: true | Structured data, records, search | path: `./mcp-data.db`
- **files**: fs_write/read | persists: true | Arbitrary files, scripts, exports