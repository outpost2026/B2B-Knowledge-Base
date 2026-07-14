# PITEVNÍ KNIHA: MCP SERVERY (sdílená)

Cross-repo ponaučení z vývoje MCP serverů — cnc-tools (mcp-local-server) a linkedin-mcp-custom.

**Datum:** 2026-07-14 | **Verze:** 3

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
| 013 | Fragilní extrakce job ID (jen `<a href>`) | linkedin-mcp | ✅ Fixed |
| 014 | KBWriter dedup fallback: `industry` = vždy None | linkedin-mcp | ✅ Fixed |
| 015 | Summary table non-idempotent (duplicity při update) | linkedin-mcp | ✅ Fixed |
| 016 | MCP transport timeout pro batch operace | linkedin-mcp | ✅ Fixed (time-budget + per-job tool) |
| 017 | Python version mismatch (.venv vs system) | linkedin-mcp | ✅ Fixed |
| 018 | Console script not in PATH | linkedin-mcp | ✅ Fixed |
| 019 | Shell escaping fragility (Win/Bash/PS) | cross-repo | ⚠️ Mitigováno |
| 020 | Cookie lifecycle — silent expiry | linkedin-mcp | ✅ Fixed (session cache + checkpoint detection) |
| 021 | LLM blind path navigation (Workspace discovery gap) | cnc-tools | ✅ Fixed (`_load_workspace_context` + `tool_workspace_info`) |

---

### Detailní záznamy

**cnc-tools (001–006, 021):** → `mcp-local-server/pitevni_kniha_mcp_v1.md`
**linkedin-mcp (007–020):** → `linkedin-mcp-custom/pitevni_kniha_v1.md`

---

## Detail linkedin-mcp (013–020)

### 013 — Fragilní extrakce job ID
**Root cause:** `_extract_job_ids()` hledal pouze v `<a href="/jobs/view/ID">` atributech. Job ID uložená v data atributech, `<script>` JSON blobech nebo mimo `<a>` elementy byla ignorována → ztráta ~37 % job ID (17/27 v Session 3).

**Fix:** 4-vrstvá extrakce — (1) `<a href>`, (2) všechny element attributes (data-*, aria-*, urn:li), (3) script JSON bloby s context filtering, (4) full outerHTML regex scan.

**Verifikace:** Session 4 test — 49/49 ID nalezeno, 0 duplicit, 0 missed.

---

### 014 — KBWriter dedup fallback broken
**Root cause:** `_find_entry_index()` porovnával `entry.title|eroi.company` (správně) proti `entry.title|company.industry` (vždy None → neshoda). Funkce `_format_entry_json()` nastavovala `industry: None` — company name se nikam neukládala.

**Fix:** Ukládat `eroi.company` do `company.industry`. Fallback dedup nyní korektně porovnává `title|company_name` proti `stored_title|stored_company`.

**Lesson:** Nikdy nenechávat pole JSON schématu na `None`, pokud existuje hodnota k uložení. Schema drift se detekuje až za běhu.

---

### 015 — Summary table non-idempotent
**Root cause:** `_update_summary_table()` vždy *appendoval* nový řádek tabulky, nikdy nekontroloval existenci řádku se stejným ID. Re-analýza (update) vytvořila duplicitní řádky v `## Souhrnná statistika`.

**Fix:** Před appendem zkontrolovat, zda řádek s `fid` již existuje. Pokud ano → nahradit (in-place update). Pokud ne → append.

**Lesson:** Každá write operace, která může běžet vícekrát na stejných datech, musí být idempotentní. "Golden rule of DevOps."

---

### 016 — MCP transport timeout pro batch operace
**Root cause:** `analyze_saved_jobs` volá `scrape_saved_jobs()` + N× `scrape_job()` + EROI scoring + KB write sequenciálně. Při N=27 a ~3s/job je celkový čas ~85s. MCP hostitel timeoutuje na 60–120s (závisí na klientovi).

**Workaround:** CLI test script `scripts/test_scrape.py` obchází MCP transport a volá scraper přímo. Umožňuje debugging bez timeout interference.

**Limitation:** MCP protokol není navržen pro long-running batch operace (minuty). Každý MCP tool by měl buď (a) streamovat progress, nebo (b) být nahrazen CLI entry pointem.

---

### 017 — Python version mismatch (.venv vs system)
**Root cause:** `.python-version` = 3.12, `pyproject.toml` requires >=3.12, ale `.venv` vytvořen s Python 3.11 (system Python). Console script `linkedin-mcp` se nainstaloval do system Python 3.11 Scripts adresáře → package neimportovatelný.

**Fix:** Recreate `.venv` with Python 3.12: `uv venv --python 3.12`. Verifikace: `.venv/Scripts/python --version` musí vrátit 3.12.x.

**Detection:** `ruff check` hlásí `F821 undefined name` nebo cryptic import errors. System Python `python --version` ≠ `.python-version`.

---

### 018 — Console script not in PATH
**Root cause:** `uv sync` nainstaluje package do `.venv/` a vytvoří `linkedin-mcp.exe` v `.venv/Scripts/`. Tento adresář ale není v system PATH → `linkedin-mcp` command not found.

**Fix (dvojitý):**
1. `.bat` wrapper v repo root: `linkedin-mcp.bat → .venv/Scripts/linkedin-mcp.exe %*`
2. `.venv/Scripts/` trvale přidán do User PATH (via `setx`)

**Lesson:** `uv sync` ≠ `pip install`. Console script je v .venv, ne v globální PATH. Autodidakt očekává `linkedin-mcp` jako globální command. Vždy po `uv sync` ověř: `where linkedin-mcp`.

---

### 019 — Shell escaping fragility (Windows/Bash/PowerShell)
**Root cause:** Vývoj probíhá v Git Bash (bash on Windows), ale deployment a testování na cmd.exe a PowerShell. Každý shell má jiná escaping pravidla:
- **Git Bash:** backtick `` ` `` pro command substitution, `$var`, `\n` pro newline
- **PowerShell:** `$env:VAR`, `...` subexpression, backtick jako escape char
- **cmd.exe:** `%VAR%`, `^` jako escape, `&&` chain

Každý pokus o vnoření PowerShell do bash stringu selhal (3/3 v Session 4).

**Příklady selhání:**
```bash
# Bash → PowerShell (FAIL: $env:PATH expandne bashovsky)
powershell -Command "[Environment]::SetEnvironmentVariable('Path', \"$env:PATH;...\", 'User')"

# Bash → cmd (FAIL: && ampersand expandne bashovsky)
cmd.exe //c "where linkedin-mcp.exe 2>&1"
```

**Mitigace:**
1. Každou PowerShell operaci psát jako `.ps1` script a spouštět ho
2. Pro jednoduché Windows operace použít `cmd.exe //c` (escaping je konzistentnější)
3. `.bat` wrapper místo přímého volání `.exe`

---

### 020 — Cookie lifecycle — silent expiry
**Root cause:** LinkedIn session cookies mají neurčitou dobu expirace (dny až týdny). `is_logged_in()` navštíví `/feed/` a zkontroluje URL na `/feed/` vs `/login`. Pokud LinkedIn redirectne na checkpoint/challenge stránku, nebo pokud se změní URL pattern, vrací `False`.

**Dopad:** MCP server vracející `auth_required` error uprostřed pipeline. Uživatel musí ručně zavolat `--login`.

**Otevřeno:** Chybí (a) automatická detekce expirace před scrapingem, (b) obnovení session bez zásahu uživatele, (c) notifikace o expiraci v logu s časovým razítkem.

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

### P11 — Console script distribution
Po `uv sync` vždy explicitně ověř, že konzolový script je dostupný:
```bash
.venv/Scripts/linkedin-mcp.exe --help   # musí fungovat
where linkedin-mcp                       # musí najít exe v .venv/Scripts
```
Pokud `where` selže → přidej `.venv/Scripts` do PATH nebo vytvoř `.bat` wrapper. `uv sync` sám o sobě negarantuje globální dostupnost scriptu.

### P12 — Cross-shell launcher
Každý CLI nástroj na Windows musí mít `.bat` wrapper v repo root:
```batch
@echo off
"%~dp0.venv\Scripts\linkedin-mcp.exe" %*
```
Toto funguje identicky z cmd, PowerShell i přes explicitní path z Git Bash. `.bat` je jediný formát, který Windows spustí ze všech shellů bez modifikace.

### P13 — Long-running batch operations
MCP tool, který iteruje N>10 I/O operací, musí být buď:
1. Asynchronní s progress streamingem (MCP `ctx.info()`), nebo
2. Nahrazen CLI entry pointem, který obchází MCP transport timeout

Timeout = sekvenční_doba × N. Při N=50 a 3s/job je 150s → každý MCP host timeoutuje.

### P14 — Windows path quoting
- Vždy používej `pathlib.Path` pro konstrukci cest (nikdy string concatenation)
- Při předání cesty subprocessu: `str(resolved_path)` + explicitní quoting v shell příkazu
- Testuj cesty v cmd.exe, PowerShell i Git Bash — každý zpracovává spaces/backslashes jinak
- `C:\Users\PC\Documents\Repozitar_Dev\_github\` = ~70 chars path prefix → riziko MAX_PATH (260 chars)

### P15 — Session monitoring
Před každým pipeline runem:
1. Zavolej `is_logged_in()` a loguj výsledek včetně `page.url`
2. Pokud auth selže, zaloguj nejen "not authenticated", ale i response body (může být checkpoint/challenge page)
3. `--login` flow musí fungovat bez restartu MCP serveru

### P16 — PowerShell v bash = piš .ps1 soubor
Nikdy nevkládej PowerShell one-linery do bash stringů. Vždy:
1. Napiš `.ps1` script
2. Spusť ho: `powershell -File scripts/operace.ps1`

Toto eliminuje dvojité escaping (bash → PowerShell → Windows API) a dělá operaci reviewovatelnou/opakovatelnou.

### P17 — Workspace context export
Každý MCP server, který očekává LLM agenty jako primární uživatele (nikoliv jen CLI), musí poskytnout mechanismus pro zjištění workspace kontextu bez explorace:

1. Při startu vypsat workspace root do stderr: `print(f"[server] Workspace root: {root}", file=sys.stderr)`
2. Poskytnout dedikovaný tool (např. `tool_workspace_info()`) vracející:
   - Root cesta (ALLOWED_ROOTS[0])
   - Guardrails profil z `.ai_guardrails.json`
   - Index summary z `index.md` (datum, session, aktivní repa)
3. Kontextové soubory přednačíst při startu do cache (ne až při prvním volání toolu)

**Bez toho LLM háže cesty, ztrácí 2–3 iterace explorací a snižuje SNR session.**

Referenční implementace: `mcp-local-server/server.py` — `_load_workspace_context()` + `tool_workspace_info()`.

### P18 — Console encoding na Windows (Unicode safety)
Windows console defaultuje na cp1250 (Central European), která neobsahuje emoji (U+1F000+) ani mnoho Unicode znaků. Python 3.x zdědí tuto kódovku pro stdout/stderr.

1. **Před každým python příkazem v PowerShellu:**
   ```powershell
   $env:PYTHONIOENCODING='utf-8'
   ```
2. **V MCP server startupu:**
   ```python
   import sys
   sys.stdout.reconfigure(encoding='utf-8', errors='replace')
   ```
3. **V Python skriptech, které tisknou webový obsah:**
   ```python
   sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # před prvním print()
   ```
4. **Ve zdrojovém kódu — emoji zakázána** (`.ai_guardrails.json` encoding_rules).

Toto je runtime vrstva — liší se od "zákazu emoji v kódu" (vývojová vrstva). Obě jsou nutné.

---

## Dědičnost napříč projekty

Pravidla P1–P18 se přenášejí do každého nového MCP projektu. Při zakládání nového repozitáře:

1. Kopírovat `P11` (console script) + `P12` (`.bat` launcher) — první věc po `uv sync`
2. Kopírovat `P14` (path quoting) — při každém file I/O
3. Kopírovat `P16` (PS1 scripts) — při každé Windows administraci
4. Kopírovat `P17` (workspace context) — ihned po vytvoření server skeletonu
5. Kopírovat `P18` (console encoding) — při prvním `print()` v kódu

---

*sdilena_pitevni_kniha_mcp.md — 2026-07-14 — v3 — přidány 021 (workspace discovery), P17 (workspace context export), P18 (console encoding Windows)*
