# PITEVNÍ KNIHA: MCP SERVERY (sdílená)

Cross-repo ponaučení z vývoje MCP serverů — cnc-tools (mcp-local-server) a linkedin-mcp-custom.

**Datum:** 2026-07-15 | **Verze:** 5

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
| 022 | Silent failure pattern (`except Exception: continue`) | MCP-Jobs | ✅ Fixed (per-card logging + skip count + 0-ads alert) |
| 023 | Salary filter: split() vs regex false-reject | MCP-Jobs | ✅ Fixed (`_SALARY_NUM_RE` regex) |
| 024 | Exclude čeština — domain-specific semantics | MCP-Jobs | ✅ Fixed (portal-contextual exclude lists) |
| 025 | ETL feedback loop dependency (real data reveals silent degradation) | MCP-Jobs | ✅ Mitigated (ETL runner + session-start health check protocol) |
| 026 | LLM-assisted dev blind spots (can't detect silent degradations) | cross-repo | ⚠️ Mitigated (require ETL feedback loop for all data pipelines) |
| 027 | L2 Resources (mcp-jobs://ads/{query_id}) | MCP-Jobs | ✅ Fixed (3 resources: /list, /{query_id}, /{query_id}/report) |
| 028 | PowerShell f-string quoting + cp1250 encoding (6-layer stack) | cross-repo | ✅ Fixed (6-layer defence-in-depth from $PROFILE to Python runtime) |

---

### Detailní záznamy

**cnc-tools (001–006, 021):** → `mcp-local-server/pitevni_kniha_mcp_v1.md`
**linkedin-mcp (007–020):** → `linkedin-mcp-custom/pitevni_kniha_v1.md`
**MCP-Jobs (022–027):** → `04_KNOWLEDGE_BASE/01_MCP/mcp_jobs_pitevni_kniha_v1.md`

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

## Detail MCP-Jobs (022–027)

### 022 — Silent failure pattern (`except Exception: continue`)

**Root cause:** Všichni 4 provider scrapers v MCP-Jobs používaly `except Exception: continue` při parsování jednotlivých karet inzerátů. Pokud HTML struktura změnila (např. Bazos změnil CSS třídy), parsovací kód tiše failoval — žádná chyba, žádný warning, 0 výsledků.

**Detekce:** Claude audit identifikoval pattern teoreticky, teprve ETL běh odhalil, že Bazos selectory byly roky rozbité.

**Dopad:** Bazos vracel 0 výsledků po dobu ~měsíců (od změny HTML struktury). Uživatel/LLM akceptoval 0 jako "není poptávka".

**Fix:**
1. Per-card `logger.warning()` s detailní zprávou (na jakém poli parsování selhalo)
2. Počítadlo skipnutých karet (`skipped` proměnná)
3. 0-ads `logger.error()` alert — pokud provider vrátí 0, logger.error s CTX
4. `logger.exception()` v `server.py` `_run_pipeline()` error handleru

**Lesson:** `except Exception: continue` je systematické riziko — nezpůsobuje pád, ale tichou ztrátu dat. Každý scrape kód musí logovat skipnuté položky a alertovat na 0 výsledků.

---

### 023 — Salary filter: split() vs regex false-reject

**Root cause:** `_salary_filter()` používal `str.split()` + `int()` na surový string "30 000 - 50 000 Kč". `split()` na mezerách vytvořil `['30', '000', '-', '50', '000', 'Kč']` → `int('000')` = `ValueError` → false reject validní inzeráty s českým formátem čísel (mezera jako tisícový oddělovač).

**Detekce:** Claude audit — test s 3 sample stringy, 2/3 failovaly.

**Fix:** Nahrazen `_SALARY_NUM_RE` regexem: `re.findall(r'\d{1,3}(?:[ \u00a0]\d{3})+|\d+', text)` — zachytí "30 000" i "50000", ignoruje "000" bez prefixu.

**Lesson:** Nikdy nepoužívej `str.split()` na user-facing textových datech. Český formát čísel používá mezeru jako tisícový oddělovač. Regex je jediný robustní přístup.

---

### 024 — Exclude čeština — domain-specific semantics

**Root cause:** Czech exclude terms `poptavam`, `poptavame`, `shanim`, `hledam` byly aplikovány globálně. Na většině portálů znamenají "hledám práci" (spam). Na Bazosu ale znamenají "poptávám zaměstnance" (validní job ad inzerce v sekcích jako zahradník/truhlář/střechy).

**Detekce:** Debug script na zahradník query — 451/462 Bazos ads zamítnuto booleanem, 11/11 zbývajících zamítnuto exclude termy.

**Fix:** Odebrány `poptavam/poptavame/shanim/hledam` z exclude listů pro Bazos-only query (zahradnik, truhlar, strechy). Multi-word `hledam praci`, `hledame kolegu` ponechány (jednoznačné).

**Lesson:** Stejné slovo může mít opačný význam podle kontextu a portálu. Exclude listy musí být portal-specific nebo alespoň portal-aware.

---

### 025 — ETL feedback loop dependency

**Root cause:** Žádný mechanismus pro pravidelné ověření, že scrapers stále fungují. Selectory se rozbijí při změně HTML struktury (typicky každých pár měsíců u českých portálů). Bez ETL běhu s vizuální kontrolou výsledků nelze degradaci detekovat.

**Detekce:** Manuální ETL run s analýzou matched vs skipped poměru.

**Fix:**
1. Vytvořen `scripts/run_etl.py` — ETL runner s timestampovaným výstupem
2. `output/etl_latest.json` — poslední běh pro snadné porovnání
3. Protokol: spustit ETL na začátku každé session jako health check
4. Doporučeno: automatický diff proti předchozímu běhu s alertem na >20% pokles matched ads

**Lesson:** MCP data pipeline bez ETL health checku je slepá. LLM-assisted vývoj vyžaduje reálná data pro detekci degradace. Audit bez ETL je jen teorie.

---

### 026 — LLM-assisted dev blind spots

**Root cause:** LLM generuje nový kód výborně, ale nedokáže detekovat degradaci existujícího kódu. Tři z pěti odhalených bugů byly v kódu, který LLM neviděl (staré selectory, config exclude listy). LLM nemá "paměť" fungujícího stavu — neví, že dříve selectory fungovaly.

**Detekce:** Meta-analýza session — porovnání audit predikcí s ETL realitou.

**Dopad:** LLM-assisted vývoj může vytvářet iluzi stability. Nový kód je otestovaný, ale starý kód tiše degraduje.

**Mitigace:**
1. Pravidelný ETL feedback loop (entry 025)
2. Version comparison v ETL runneru (matched count trend)
3. Testy, které testují reálné HTML (mocky s aktuální strukturou)
4. Session-start health check

---

### 027 — L2 Resources: mcp-jobs://ads/{query_id}

**Status:** ✅ Fixed (MCP-Jobs v0.4.0)

**Symptom:** Search tooly vracely data pouze v kontextu LLM odpovědi. Bez možnosti znovu získat stejná data bez nového scrapingu. L2 vrstva (Resources) chyběla v celém MCP maturity modelu projektu.

**Root cause:** FastMCP podporuje Resources, ale žádný tool je neimplementoval. Data byla pomíjivá — doručena jako tool response, pak ztracena.

**Fix:** 3 resources na URI `mcp-jobs://ads/`:
- `/list` — JSON seznam všech uložených resultsetů
- `/{query_id}` — JSON data (shodná s tool response)
- `/{query_id}/report` — Markdown report

Architektura: in-memory `_query_store`, `_store_results()` helper, modifikace všech 3 search toolů pro ukládání + vrácení `query_id` a `resource_uri`.

**Verifikace:** 103/103 testů, 6 nových resource testů. L2 maturity: ⬜ → ✅

---

### 028 — PowerShell f-string quoting + cp1250 encoding

**Status:** ✅ Fixed (cross-repo, 6-layer stack)

**Symptom:** Dva persistentní problémy při agentním vývoji na Windows:
1. `SyntaxError: f-string: unmatched '['` při `python -c "..."` s f-stringy
2. `UnicodeEncodeError: 'charmap' codec can't encode` při tisku emoji/unicode

**Root cause (quoting):** Windows API `CommandLineToArgvW` rozděluje argumenty Python `-c` na mezerách. Víceřádkový kód s vnořenými uvozovkami se rozseká dřív, než ho Python vstupně zpracuje. Tři vrstvy interpretace (PowerShell → cmd.exe → Python) každá přidává vlastní escaping pravidla.

**Root cause (encoding):** Windows Console defaultuje na cp1250. Python stdout encoding = cp1250 → emoji a Unicode supplementary planes (U+1F000+) nelze zobrazit.

**Fix — 6-vrstvý stack:**

| # | Vrstva | Mechanismus |
|---|--------|-------------|
| 6 | PowerShell autoload | `_github/_init.ps1` → `$PROFILE` (PS5.1 + PS7) |
| 5 | AI guardrails | `.ai_guardrails.json` shell_rules — zákaz `python -c` s komplexním kódem |
| 4 | Dokumentace | `docs/powershell_encoding.md` — root cause + FAQ pro junior dev |
| 3 | Project helpers | `scripts/init.ps1` — Run-Python, Invoke-Pipeline, Compare-ETL wrappery |
| 2 | Batch launcher | `mcp-jobs.bat` — `set PYTHONIOENCODING=utf-8` + `PYTHONUTF8=1` |
| 1 | Python runtime | `cli.py` + `server.py` → `ensure_utf8_stdout()` |

Plus: `opencode.jsonc` — přidáno `-X utf8` do commandů všech 3 MCP serverů.

**Hlavní pravidlo:** Nikdy `python -c "..."` s komplexním kódem na Windows PowerShellu. Vždy .py soubor → `python -X utf8 script.py`.

**Verifikace:** 12 syntetických guardrail testů (12/12 PASS). 103 unit testů OK. Encoding OK: české znaky + emoji + azbuka.

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

### P19 — Structured logging v scrape path

Každý scrape/provider modul musí mít:

1. **Per-card logging** — `logger.warning()` při selhání parsování jedné karty (ne `except Exception: continue`)
2. **Počítadlo skipů** — `skipped` proměnná, logovaná na konci scrape cyklu
3. **0-ads alert** — pokud provider vrátí 0 výsledků, `logger.error()` s CTX (portál url, query)
4. **Per-provider skip count** — agregace v pipeline logu

```python
# GOOD pattern
matched = 0
skipped = 0
for card in cards:
    try:
        ad = parse_card(card)
        matched += 1
    except Exception as e:
        skipped += 1
        logger.warning("Skipped card %d/%d: %s", i, total, e)
if matched == 0:
    logger.error("Provider %s returned 0 ads — possible selector breakage", provider_name)
```

Bez strukturovaného logování je `except Exception: continue` time bomb — nikdo neví, že data tiše mizí.

---

### P20 — ETL health check / session-start protocol

Každý MCP server, který zpracovává data z externích zdrojů (scraping, API), musí mít:

1. **Spustitelný ETL runner** — `scripts/run_etl.py` nebo ekvivalent, který:
   - Projde pipeline od začátku do konce
   - Uloží timestampovaný výstup do `output/` adresáře
   - Udržuje `output/etl_latest.json` (poslední běh)
2. **Session-start health check** — na začátku každé session spustit ETL a zkontrolovat matched count proti baseline
3. **Alert threshold** — pokud matched ads klesnou o >20 % oproti baseline, je pravděpodobné, že se změnila HTML struktura nebo API response (trigger pro audit selektorů)

**Bez ETL feedback loopu LLM neví, že scrapers tiše degradují. Audit bez reálných dat je jen teorie.**

Referenční implementace: `MCP-Jobs/scripts/run_etl.py`

---

### P21 — L2 Resources (URI-adresovatelná data)

Každý MCP server, který produkuje data přes tooly, by měl tato data zpřístupnit jako **MCP Resources** (L2 maturity). Důvody:

1. **Oddělení produkce od konzumu** — tool vyrobí data jednou, resource je zpřístupňuje opakovaně (0ms latence oproti novému scrapingu)
2. **Adresovatelnost** — URI `mcp-server://{namespace}/{id}` lze sdílet, ukládat, indexovat
3. **UI integrace** — MCP Apps a další klienti umí resources zobrazit jako karty/odkazy
4. **RAG připravenost** — markdown report z resource je přímo indexovatelný

Referenční implementace: `MCP-Jobs/src/mcp_jobs/server.py` — `_query_store` + 3 resource handlery.

URI schéma:
```
server://ads/list                  — JSON: seznam všech uložených sad
server://ads/{id}                  — JSON: data dané sady
server://ads/{id}/report           — markdown: human-readable report
```

Architektura: in-memory dict + export helper. Storage perzistence je oddělený concern (lze přidat později).

---

### P22 — Windows PowerShell: nikdy `python -c` s komplexním kódem

Na Windows PowerShellu je `python -c "..."` s komplexním kódem (f-stringy, vnořené uvozovky, cykly, dict comprehension) křehký. Root cause: Windows API `CommandLineToArgvW` rozděluje argument na mezerách → kód se rozseká dřív, než ho Python uvidí.

**Zakázaný pattern:**
```powershell
# FAIL: f-string s vnorenyma uvozovkama
python -c "print(f'{a['title']}')"

# FAIL: komplexni kod s cykly ve vice radcich
python -c @"
for a in data:
    print(f'  * {a["title"]}')
"@
```

**Bezpečný pattern:**
```powershell
# 1. Zapiste kod do .py souboru
@"
for a in data:
    t = a.get('title','')
    print(f'  * {t}')
"@ | Out-File $env:TEMP\script.py -Encoding UTF8

# 2. Spustete s -X utf8
python -X utf8 $env:TEMP\script.py

# 3. (volitelne) smazani
Remove-Item $env:TEMP\script.py
```

**Výjimka:** Jednoduché jednořádkové příkazy bez f-stringů a vnořených uvozovek jsou OK:
```powershell
python -X utf8 -c "print('hello')"
python -X utf8 -c "import json; print(json.dumps({'a': 1}))"
```

Toto pravidlo je zakotveno v `.ai_guardrails.json` shell_rules a dokumentováno v `docs/powershell_encoding.md`.

---

### P23 — Windows encoding: vždy PYTHONIOENCODING + PYTHONUTF8 + -X utf8

Windows Console defaultuje na cp1250 (Central European). Python stdout encoding = cp1250 → emoji a supplementary Unicode selhávají.

**Tři úrovně ochrany:**

1. **Shell-level** (nejspolehlivější):
   ```powershell
   $env:PYTHONIOENCODING = "utf-8"
   $env:PYTHONUTF8 = "1"
   ```
   Nastaví se automaticky z `$PROFILE` → `_init.ps1` (6. vrstva stacku).

2. **Process-level** (vždy při spuštění):
   ```powershell
   python -X utf8 script.py
   ```
   `-X utf8` flag říká Pythonu: "používej UTF-8 všude, ignoruj console encoding."

3. **Code-level** (poslední záchrana):
   ```python
   import sys
   sys.stdout.reconfigure(encoding="utf-8", errors="replace")
   ```
   Implementováno v `cli.py` a `server.py` (P18 rule).

**Checklist při encoding erroru:**
1. `$env:PYTHONIOENCODING` je 'utf-8'? → pokud ne, načti `_init.ps1` nebo nastav ručně
2. Používáš `-X utf8`? → pokud ne, přidej
3. Má Python kód `sys.stdout.reconfigure()`? → pokud ne, přidej (nebo importuj `ensure_utf8_stdout()` z utils)

---

## Dědičnost napříč projekty

Pravidla P1–P23 se přenášejí do každého nového MCP projektu. Při zakládání nového repozitáře:

1. Kopírovat `P11` (console script) + `P12` (`.bat` launcher) — první věc po `uv sync`
2. Kopírovat `P14` (path quoting) — při každém file I/O
3. Kopírovat `P16` (PS1 scripts) — při každé Windows administraci
4. Kopírovat `P17` (workspace context) — ihned po vytvoření server skeletonu
5. Kopírovat `P18` (console encoding) — při prvním `print()` v kódu
6. Kopírovat `P19` (structured logging) — při prvním scrape cyklu
7. Kopírovat `P20` (ETL health check) — ihned po zprovoznění pipeline
8. Kopírovat `P21` (L2 Resources) — při návrhu API (tool = produkce, resource = konzum)
9. Kopírovat `P22` (no `python -c` inline) — při prvním agentním vývoji na Windows PowerShellu
10. Kopírovat `P23` (encoding triad) — ihned po instalaci Pythonu (PYTHONIOENCODING + PYTHONUTF8 + -X utf8)

---

*sdilena_pitevni_kniha_mcp.md — 2026-07-15 — v5 — přidány 027 (L2 Resources: mcp-jobs://ads), 028 (PowerShell f-string + cp1250 6-layer stack), P21 (L2 Resources), P22 (no python -c inline), P23 (encoding triad: PYTHONIOENCODING + PYTHONUTF8 + -X utf8), dědičnost rozšířena na 10 kroků*
