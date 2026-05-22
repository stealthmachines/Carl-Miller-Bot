# ROUTING ARCHITECTURE
**Stack**: Wu-Wei MCP + LM Studio + HDGL-inspired routing | **Updated**: 2026-05-22

---

## CURRENT TOPOLOGY

```
Client → [router-phi.ps1] → { local-mcp:3333, local-mcp-dos:3334 } → LLM:1234
                 ↑
         start-routes.ps1 (daemon — health checks every 30s)
                 ↑
         state\active_server  (current routing choice)
```

### Servers
| Server | Port | File | Notes |
|--------|------|------|-------|
| local-mcp | 3333 | `server.js` | Primary |
| local-mcp-dos | 3334 | `server-dos.js` | Secondary / failover |
| LLM | 1234 | LM Studio | Shared endpoint |

Both servers implement **identical Wu-Wei Unfold Architecture**. Difference is isolation of state, not capabilities.

---

## DUAL LM STUDIO CONTEXT (Analysis)

- **Same process**: PID 16908, same port 1234
- **Two contexts**: `qwen3.5-9b@q3_k_xl` (200,000 tokens) + `qwen3.5-9b@q3_k_xl:2` (199,999 tokens)
- The `:2` suffix = separate context slot / chat session / isolated memory buffer
- The 1-token difference is a configuration artifact, not meaningful

### Recommendations
- Use **distinct endpoints** for clear routing (e.g., port 1235 for second context)
- Or pass explicit `context_id` headers in requests
- Both contexts compete for the same GPU memory — avoid simultaneous heavy requests

---

## DUAL MCP SERVER — RECOMMENDED USE

Current state: both servers are redundant (identical capabilities). Recommended evolution:

| Strategy | Implementation |
|----------|---------------|
| **State isolation** | Different DB files + notes dirs per server (immediate) |
| **Task routing** | `local-mcp-dos` for DOS/batch/multi-thread; `local-mcp` for default |
| **Failover** | Auto-switch when primary is unhealthy |
| **Load balancing** | Round-robin or phi-hash distribution |

### State Separation Config (mcp.json)
```json
"local-mcp": {
  "url": "http://localhost:3333/sse",
  "env": {"MCP_DB": "state0/mcp-data.db", "MCP_NOTES": "state0/notes"}
},
"local-mcp-dos": {
  "url": "http://localhost:3334/sse",
  "env": {"MCP_DB": "state1/mcp-data.db", "MCP_NOTES": "state1/notes"}
}
```

---

## HDGL ROUTING — CONCEPTS

**HDGL (High-Dimensional Geometry Load Balancer)** — analog-over-digital load balancing:
- **φ-spiral hashing**: Paths hashed through golden ratio φ = (1+√5)/2
- **Living config**: Routing config regenerated every 30 seconds by daemon
- **Self-healing**: Nodes take over when peers fail; natural failover
- **Analog divergence**: Each node computes independently → unique fingerprints

### Wu-Wei Adaptation
| HDGL Feature | Our Implementation |
|---|---|
| φ-spiral hashing | `Get-PhiHash()` in `router-phi.ps1` |
| 30s daemon cycle | `start-routes.ps1` health check interval |
| Multiple weights | Path-based intelligent routing |
| Self-healing | Auto-failover on unhealthy server |
| Analog state | Time-based phi decisions |
| Fingerprint divergence | Unique cycle hashes per run |

---

## DEPLOYED FILES (wuwei-routing/)

Location: `wuwei-routing/` (project root)

| File | Purpose |
|------|---------|
| `start-routes.ps1` | HDGL daemon — background health checks + state update |
| `router-phi.ps1` | Request-time routing via phi-hash |
| `start.bat` | Easy startup (double-click) |
| `README.md` | Usage documentation |

### Quick Start
```powershell
# Option 1
.\wuwei-routing\start.bat

# Option 2
cd wuwei-routing; .\start-routes.ps1

# Test routing
.\router-phi.ps1 GET /mcp/tools/list
# Output: ROUTING_COMPLETE:server=local-mcp,port=3333,hash=1

# Check state
Get-Content .\wuwei-routing\state\active_server
```

---

## WINDOWS SPECIFICS

Key differences from Linux implementation:

| Linux | Windows |
|-------|---------|
| `/opt/wuwei-routing/` | `.\wuwei-routing\` |
| `date -Iseconds` | `Get-Date -Format 'o'` |
| `md5sum` / `sha256sum` | `[System.Security.Cryptography.SHA256]::Create()` |
| `ps` / `kill` | `Get-Process` / `Stop-Process` |
| `curl` health check | `Invoke-WebRequest -TimeoutSec 2` |
| Forward slashes | Backslashes (or use `$env:PATH` style) |
| `.sh` scripts | `.ps1` (PowerShell) or `.bat` |

### State Directory
```
wuwei-routing\
  state\
    active_server    # Current routing choice: "local-mcp" or "local-mcp-dos"
    health.json      # Server health status (each server: {healthy, last_check, port})
    last_cycle       # Last update timestamp
    version          # Server version info
  logs\
    daemon-YYYYMMDD.log
```
