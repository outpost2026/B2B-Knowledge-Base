# Nástrojový audit dev notebooku — agentní workflow

**Datum:** 2026-10-22 | **Autor:** outpost2026
**Účel:** Empirický snapshot instalovaných nástrojů a delta vůči adopční strategii P06 — co je použitelné pro agentní práci, co chybí.
**Typ:** audit | **Doména:** dev tooling, agentní workflow | **EROI:** 8/10
**Návaznost:** P06 `STRATEGIE_ADOPCE_IT_SWE_AI_ML_nastroju_2026-10-17`, `workspace-guardrails`, `kb-workflow`
**Provenance:** source-read (registry HKLM/HKCU, Program Files, PATH, `pip list`, `npm ls -g`, `opencode.jsonc`, manifesty rep) — 2026-10-22

---

## 1. Metoda

Sken 5 zdrojů: (a) uninstall registry 3 hiveů, (b) Program Files + LocalAppData\Programs, (c) `Get-Command` na 50 CLI jmen, (d) Python/npm package inventory, (e) MCP konfigurace opencode. Žádné tvrzení není z paměti.

---

## 2. Delta vůči P06 (T1 páteř CLI)

P06 (2026-10-17) tvrdil „rg/fd/fzf/jq jen portable, ne na PATH" a „Composer, sqlite3 chybí".

| Nástroj | P06 stav | Stav 2026-10-22 |
|---|---|---|
| rg, fd, jq, fzf, delta | portable | **PIN na PATH** (`.tools\bin`) |
| sqlite3 | chybí | **PIN** |
| Composer | chybí | **PIN** (`composer.bat` + `composer.phar`) |
| bat, lazygit, just/make | chybí | **stále chybí** |

**Závěr:** nejvyšší-ROI krok strategie (pin `.tools` na PATH) je hotový. Ze T1 zbývají 3 položky, všechny EROI ≤ 8.

---

## 3. Inventář — použitelné pro agentní práci

| Vrstva | Nástroje |
|---|---|
| Runtime | Python 3.11.9, node 24 (vendored), npm 11.19, PHP 8.3, pwsh 7 |
| Git/CI | git 2.53, git-lfs, gh 2.x, Docker 29.5 + kubectl (WSL2 `docker-desktop` **stopped**) |
| CLI | rg, fd, jq, fzf, delta, sqlite3, 7z, uv/uvx, ruff 0.16, pytest 9 |
| Cloud | gcloud SDK |
| Python | ezdxf 1.4.4, shapely, pyproj, laspy/lazrs, pandas, pyarrow, matplotlib, streamlit, fastmcp 3.4.4, mcp 1.28, playwright 1.58 (+chromium 1208/1228), pywin32, pyautogui, selenium, psycopg, gensim, nltk, pdfplumber |
| MCP | 5 lokálních serverů: cnc-tools, linkedin-analyzer, mcp-jobs, lichess-analyzer, mcp-retrieval |

---

## 4. Nová osa — GUI aplikace jako headless engine

P06 tuto vrstvu neřeší. Agent neovládá GUI klikáním, ale headless API/CLI.

| Aplikace | Verze | Headless cesta | Vazba na repo |
|---|---|---|---|
| Blender | 5.1.0 | `blender --background --python` (`bpy`) — **funguje, ale není v PATH** | cad2llm, mesh/DXF, thumbnaily |
| SketchUp Pro | 26.1 + 2024 | Ruby 3.2 (`x64-ucrt-ruby320.dll`), `-RubyStartup`; bez true headless | cad2llm (`.rb`) |
| LibreOffice | 26.2.1 | `soffice --headless --convert-to` | kazuistiky, KB export |
| Playwright | 1.58 | browser automation (chromium staženy) | linkedin-mcp, MCP-Jobs, scrapers |
| pywin32 | 312 | COM automation | LibreOffice, Excel, IrfanView |

**Vyřazeno:** LightBurn 2.0.05, VCutWorks 2.00.34 — pouze GUI, žádné CLI/API. VCF se parsuje textově ve `vcf_parser_b2b`, agentní hodnota GUI je nulová.

---

## 5. Mezery

**P1 — blokuje agentní práci:**

| # | Gap | Fix | EROI |
|---|---|---|---|
| 1 | Blender není na PATH → `bpy` nedostupný | přidat `Program Files\Blender Foundation\Blender 5.1\` | 6 |
| 2 | Chybí standalone Ruby → `cad2llm` `.rb` nelze ani syntax-checknout | `winget install RubyInstallerTeam.Ruby.3.2` | 7 |
| 3 | LSP zapnut v configu, ale chybí servery | `pyright`, `typescript-language-server` | 8 |
| 4 | Chybí `az` → Azure/bicep deploy v MCP-Jobs neověřitelný | `winget install Microsoft.AzureCLI` | 5 |
| 5 | Chybí `psql` → Postgres (MCP-Jobs, Meteo) jen přes psycopg | `winget install PostgreSQL.psql` | 5 |

**P2 — rozšíření:** `ollama` (lokální embeddingy pro rag_indexer), `mypy` + `pytest-xdist`, `cloudflared` (vzdálený přístup k MCP), `yq`, `ffmpeg`, `magick`.

### 5.1 Stav po implementaci (2026-10-22, stejný den)

| # | Výsledek |
|---|---|
| 1 | **DONE** — Blender 5.1.0 v user PATH; `bpy` headless OK (Python 3.13.9) |
| 2 | **DONE** — Ruby 3.2.11 (`C:\Ruby32-x64`), gem 3.4.19; `ruby -c` 9/9 `.rb` v cad2llm bez chyby |
| 3 | OPEN — LSP servery |
| 4 | **DONE** — Azure CLI 2.91.0 |
| 5 | **SKIP** — `PostgreSQL.psql` neexistuje; plný server 396 MB zamítnut, psycopg dostačuje |

Reálná spotřeba sítě: **82 MB** (Ruby 15,2 + az 66,8), z toho Blender 0 MB.

---

## 6. Falsifikovatelné metriky

1. **PATH koverage:** kolik z T1+P1 nástrojů je voláno bez absolutní cesty (`Get-Command`) — dnes 7/13.
2. **Headless podíl:** kolik denních tasků jde bez GUI okna — dnes 0/4 domén (CAD, office, laser, cloud).
3. **Čas k prvnímu příkazu** u nové session: dnes ≥1 manuální lookup cesty (Blender, SketchUp).

## 7. Doporučený next step

Pořadí: LSP servery (8) → standalone Ruby (7) → Blender PATH (6) → `az`/`psql` (5). Všechny body jsou reverzibilní, 0 admin (kromě winget).

---

*Snapshot s datem — při změně stavu vzniká nová generace, předchozí do `_ARCHIVE/` (P4).*
