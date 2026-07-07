# PITEVNÍ KNIHA: MCP SERVERY (sdílená)

Cross-repo ponaučení z vývoje MCP serverů — cnc-tools (mcp-local-server) a linkedin-mcp-custom.

## Přehled záznamů

| # | Název | Server | Status |
|---|-------|--------|--------|
| 001 | Sekvenční bottleneck (Cross-repo paralelizace) | cnc-tools | ✅ Fixed |
| 002 | Vnořené timeouty bez signalizace | cnc-tools | ✅ Fixed |
| 003 | Read-only git bez `--no-optional-locks` | cnc-tools | ✅ Fixed |
| 004 | JSON data corruption v session state | cnc-tools | ✅ Fixed |
| 005 | Absence duration metriky v tool implementaci | cnc-tools | ✅ Fixed |
| 006 | Absence timeout guardu na úrovni tool wrapperu | cnc-tools | ✅ Fixed |
| 007 | Typová záměna BrowserContext vs Browser | linkedin-mcp | ✅ Fixed |
| 008 | Shadow lokální proměnná (Missing global) | linkedin-mcp | ✅ Fixed |
| 009 | Auth navigační konflikt (is_logged_in redirect) | linkedin-mcp | ✅ Fixed |
| 010 | Fragilita CSS selektorů (DOM mutace) | linkedin-mcp | ✅ Fixed |
| 011 | Paginační slepota (Missing second page) | linkedin-mcp | ✅ Fixed |
| 012 | Špatný git repo root v parents indexu | linkedin-mcp | ✅ Fixed |

---

### Detailní záznamy

**cnc-tools (001–006):** → `mcp-local-server/pitevni_kniha_mcp_v1.md`
**linkedin-mcp (007–012):** → `linkedin-mcp-custom/pitevni_kniha_v1.md`

---

## Průřezová pravidla (platí pro všechny MCP servery)

### P1 — Časové konstanty
Subprocess timeout v MCP toolu musí být **max 25 %** MCP client timeoutu. Client timeout 60 s → subprocess timeout 15 s. Fail fast, fail loud.

### P2 — Paralelizace
Jakmile tool iteruje N>1 nezávislých zdrojů, použij `ThreadPoolExecutor`. Počet workerů: min(4, N). I/O-bound operace škálují lineárně do ~8 vláken.

### P3 — Read-only locky
Každý read-only subprocess call (git, grep, diff) používej `["git", "--no-optional-locks"]`. Eliminuje filesystem lock contention.

### P4 — JSON defenziva
Každý JSON state deserializer: `try/except` + `isinstance(v, dict)` guard + auto-repair. Počítej s corrupt daty.

### P5 — Diagnostika
`@auditable` na každém toolu. Povinné: `ts`, `tool`, `duration_s`, `ok`. Bez metriky není diagnostika.

### P6 — Timeout guard
I/O tool s potenciálem >10 s → wrapper s `concurrent.futures.TimeoutError`.

### P7 — Globální proměnné
Každá funkce, která **zapisuje** do modulové globální proměnné, musí mít `global jméno`. Python bez `global` vytvoří lokální shadow proměnnou — tichá ztráta dat.

### P8 — Pořadí operací
Auth/navigace/destruktivní operace: auth first, navigace second. Nic mezi ně nevkládat.

### P9 — Žádné CSS třídy v selektorech
Používej sémantické HTML atributy (`href`, `aria-label`, `role`). CSS třídy jsou ephemeral — A/B testy je mění bez varování.

### P10 — Verifikace cest
`Path.parents` je 0-indexovaný od nejbližšího rodiče. Ověř `relative_to()` před prvním produkčním použitím.

---

*sdilena_pitevni_kniha_mcp.md — 2026-07-07 — v1*
