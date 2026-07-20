# MCP GROUND TRUTH — Agregovaná pitevní kniha

**Datum:** 2026-07-20 | **Verze:** 2
**Účel:** Jediný zdroj pravdivých ponaučení z vývoje všech MCP serverů v portfoliu. Nahrazuje: linkedin_mcp_pitevni_kniha_v1.md, mcp_jobs_pitevni_kniha_v1.md, sdilena_pitevni_kniha_mcp.md, MCP_komplexni_analyza_a_strategie_v1.md (pouze postmortem části), pitevni_kniha_mcp_v1.md (cnc-tools).
**Rozsah:** linkedin-mcp-custom, MCP-Jobs, mcp-local-server (cnc-tools), lichess-analyzer-mcp
**Určení:** Výukový materiál pro deva, instrukce pro LLM, ground truth pro rozhodování

---

## 1. Mapa superseded artefaktů

| Původní soubor | Co se přebírá | Co se zahazuje |
|----------------|---------------|----------------|
| `linkedin_mcp_pitevni_kniha_v1.md` | Entry 007-024 (plné znění) | Duplicitní statistiky, Session 3→4 timeline (historický) |
| `mcp_jobs_pitevni_kniha_v1.md` | Entry 022-035 (plné znění) | Cross-LLM audit metoda 032 (meta-poznatek, ne bug) |
| `sdilena_pitevni_kniha_mcp.md` | Průřezová pravidla P1-P23, Entry 001-028 (stručné) | Duplicitní popisy (odkazovaly na originály) |
| `pitevni_kniha_mcp_v1.md` (cnc-tools) | Entry 001-014, Diagnostický filtr, P24-P28 | Cross-referenční mapa (nyní redundantní) |
| `MCP_komplexni_analyza_a_strategie_v1.md` | §9 Secret exposure, EROI framework, §10-11 akční plány | §1 Fenomén MCP, §4 Rešerše, §6 Use case, §7 Predikce |
| `MCP_practical_workflow_guide_v1.md` | §7 Falsifikace, §8 Rozhodovací framework | §2 Filosofie, §3 Scénáře (není postmortem) |

---

## 2. Sémantické nálezy — co bylo opraveno při agregaci

### 2.1 Vyřešené rozpory

| Rozpor | Původní stav | Stav v GT |
|--------|-------------|-----------|
| Entry 016 (MCP timeout) | sdilena: `✅ Fixed` / detail `⚠️ Workaround` | `✅ Fixed` — per-job tool + CLI bypass |
| Entry 020 (Cookie lifecylce) | linkedin: `⚠️ Otevřeno` / sdilena: `✅ Fixed` | `✅ Fixed` — session cache + checkpoint detection |
| Input validation status | analyza §5.1: `⏳ Pending` / §11: `✅ Implementováno` | `✅ Implementováno` (Session 16) |
| Verze číslování | Každý repo měl vlastní číselnou řadu | Jednotné GT#ID, zdrojové ID v závorce |

### 2.2 Eliminované duplikace

- Encoding/PowerShell/quoting problem: 6 rúzných zápisů → 1 merged entry (GT-031)
- MCP transport timeout: 3 výskyty → 1 merged entry (GT-013)
- EROI matice: 2 verze → 1 konsolidovaná
- Secret exposure: 2 dokumenty → 1 sekce

### 2.3 Odstraněný nadbytečný text

- Tržní analýza MCP ekosystému (není postmortem)
- Predikce na 2027 (spekulativní)
- Filosofické pasáže "od příkazů k záměrům"
- Tabulka veřejných MCP serverů
- Adopční křivka a Gaussova distribuce uživatelů

### 2.4 Zachované unikátní části

- **Diagnostický filtr** (47 checkpoints) — z cnc-tools pitevni_kniha
- **WF simulace v3** (24/26 OK) — z cnc-tools pitevni_kniha
- **6-layer encoding stack** — z MCP-Jobs
- **L2 Resources architektura** — z MCP-Jobs

---

## 3. Katalog chyb (merged)

Číslování GT-001 až GT-042. V závorce původní ID z originálního artefaktu.

### 3.1 cnc-tools (mcp-local-server)

#### GT-001 (CNC-001): Sekvenční bottleneck — Cross-repo paralelizace
**Server:** cnc-tools | **Status:** Fixed

**Symptom:** `MCP error -32001: Request timed out` při `tool_git_status_all` a `tool_cross_repo_search`. Audit log: `duration_s: 61.7-62.4` — přesně nad 60s MCP client timeout.

**Root cause:** Oba nástroje iterovaly 14 repozitářů sériově v jedné `for` smyčce. 14 x 4.4s = 61.7s.

**Fix:** `ThreadPoolExecutor(max_workers=4)`. 14 repo / 4 vlakna x 4.4s = ~15.4s.

**Pravidlo:** P1 — Jakmile nástroj iteruje N>1 nezávislých zdrojů, musí být paralelizován.

---

#### GT-002 (CNC-002): Vnořené timeouty bez signalizace
**Server:** cnc-tools | **Status:** Fixed

**Symptom:** `tool_git_diff` vrací error až po 60s, subprocess timeout byl 30s. Dvojité čekání: 30s subprocess + 30s client = 60s ztraceného času.

**Root cause:** Subprocess timeout (30s) byl příliš blízko client timeoutu (60s).

**Fix:** Subprocess timeout ≤ 15s. Fail fast: error za 15s je lepší než timeout za 60s.

**Pravidlo:** P2 — Subprocess timeout v MCP toolu musí být max 25% MCP client timeoutu.

---

#### GT-003 (CNC-003): Read-only git s write lockem
**Server:** cnc-tools | **Status:** Fixed

**Symptom:** `git status`/`git diff` trvaly 3-5s na read-only operaci.

**Root cause:** Git implicitně zapisuje do `.git/index.lock`. `--no-optional-locks` chyběl.

**Fix:** `["git", "--no-optional-locks", ...]` ve všech subprocess voláních.

**Pravidlo:** P3 — Každý read-only git subprocess call musí používat `--no-optional-locks`.

---

#### GT-004 (CNC-004): JSON data corruption — session state
**Server:** cnc-tools | **Status:** Fixed

**Symptom:** `tool_session_state` failuje s `'str' object has no attribute 'get'`.

**Root cause:** `.ai_state.json` obsahoval string místo dict. `v.get("value", "")` padá, pokud `v` není dict.

**Fix:** `isinstance(v, dict)` check + auto-repair mechanismus.

**Pravidlo:** P4 — Každý JSON deserializer: try/except + isinstance guard + auto-repair.

---

#### GT-005 (CNC-005): Absence duration metriky
**Server:** cnc-tools | **Status:** Fixed

**Symptom:** Bez audit logu nelze identifikovat, který tool způsobuje timeout.

**Root cause:** Žádná per-tool duration metrika. Subprocess timeout (30s) a MCP timeout (60s) tvoří šedou zónu.

**Fix:** `@auditable` dekorátor na všech tool funkcích. Povinné: `ts`, `tool`, `duration_s`, `ok`.

**Pravidlo:** P5 — Diagnostika: `@auditable` na každém toolu s povinnými metrikami.

---

#### GT-006 (CNC-006): Absence timeout guardu
**Server:** cnc-tools | **Status:** Fixed

**Symptom:** Jeden pomalý tool (62s) blokuje celý server (STDIO half-duplex).

**Root cause:** FastMCP nemá per-tool timeout. Dlouhý tool = zamknutý server.

**Fix:** `concurrent.futures.TimeoutError` wrapper pro I/O tooly s potenciálem >10s.

**Pravidlo:** P6 — I/O tool s potenciálem >10s musi mít wrapper s `concurrent.futures.TimeoutError`.

---

#### GT-007 (CNC-007): LLM blind path navigation
**Server:** cnc-tools | **Status:** Fixed

**Symptom:** LLM volá nástroje s cestou `C:\_github\...` — server vrací `CHYBA: mimo povolený rozsah`. LLM ztrácí 2-3 iterace hádáním správné cesty.

**Root cause:** `ALLOWED_ROOTS` je interní konstanta serveru. LLM nemá mechanismus, jak ji zjistit.

**Fix:** `tool_workspace_info()` vracející root, guardrails profil, index summary. Workspace root logován do stderr při startu.

**Pravidlo:** P17 — Každý MCP server musí poskytnout workspace context tool.

---

#### GT-008 (CNC-008): Console encoding corruption
**Server:** cnc-tools | **Status:** Fixed

**Symptom:** `UnicodeEncodeError: 'charmap' codec can't encode` při tisku emoji/Unicode na Windows.

**Root cause:** Windows Console = cp1250, Python stdout encoding = cp1250.

**Fix:** `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` + `$env:PYTHONIOENCODING='utf-8'`.

**Pravidlo:** P18 + P23 — Encoding triad: PYTHONIOENCODING + PYTHONUTF8 + -X utf8.

---

#### GT-009 (CNC-009): Pre-release Python deadlock (F1)
**Server:** cnc-tools | **Status:** Fixed

**Symptom:** Všechny git MCP nástroje timeoutují s `-32001` po 60s. Git funguje <1s z bash.

**Root cause:** Python 3.11.0rc2 (pre-release) — nedokončený subprocess pipe management na Windows. Pipe buffer deadlock.

**Fix:** Python 3.11.9 stable (z python.org). `requires-python` vylučuje rc verze.

**Pravidlo:** P24 — Nikdy nepoužívat pre-release Python (< stable) pro MCP servery. Version check při startu.

---

#### GT-010 (CNC-010): StreamHandler stderr deadlock (F3)
**Server:** cnc-tools | **Status:** Fixed

**Symptom:** I po fixu Python verze zustává latentní deadlock.

**Root cause:** `StreamHandler(sys.stderr)` v audit.py. Pipe buffer (4-64 KB) se zaplní → event loop freeze → MCP timeout.

**Fix:** StreamHandler odstraněn, zachován pouze FileHandler.

**Pravidlo:** P25 — Nikdy nepřidávat StreamHandler(sys.stderr) v MCP serveru. Logovat jen do FileHandler.

---

#### GT-011 (CNC-011): subprocess.run handle inheritance (F2)
**Server:** cnc-tools | **Status:** Fixed

**Symptom:** Git subprocess drží MCP STDIO handles → pipe se nikdy neuzavře → client timeout.

**Root cause:** `subprocess.run()` dědí všechny handles z rodiče. MCP STDIO pipy jsou otevřeny → child proces je drží.

**Fix:** `asyncio.create_subprocess_exec()` místo `subprocess.run()`. `stdin=asyncio.subprocess.DEVNULL`.

**Pravidlo:** P26 — Všechna I/O v MCP tools přes `asyncio.create_subprocess_exec`. `subprocess.run` zakázán.

---

#### GT-012 (CNC-012): MCP test pyramida
**Server:** cnc-tools | **Status:** Fixed

**Symptom:** Unit testy (67) vse PASS, E2E test odhalí 14 anomálií (git timeout, VCF binary, encoding). Unit testy nedetekují transport-level problémy.

**Root cause:** 3 vrstvy testování: unit → integration → E2E. Chyběla integration a E2E vrstva.

**Fix:** 3-vrstvá test pyramida: (1) unit testy logiky, (2) integration testy MCP request/response, (3) E2E testy pres reálný STDIO.

**Pravidlo:** P27 — MCP test pyramida: unit > integration > E2E + smoke test po každé změně.

---

#### GT-013 (CNC-013) = LNKD-016 = JOBS-merged: MCP transport timeout pro batch operace
**Server:** cross-repo | **Status:** Fixed

**Symptom:** `analyze_saved_jobs` (N=27, ~85s) a `get_saved_jobs` → `MCP error -32001: Request timed out`. MCP protokol (JSON-RPC nad stdio) má timeout 60-120s.

**Root cause:** MCP není navržen pro long-running batch operace. Sekvenční scraping N jobů: N x ~3s = 150s+ pro N=49.

**Fix (trojí):**
1. Per-job tool (one call per job) namísto batch tool
2. CLI test script bypassující MCP transport: `scripts/test_scrape.py`
3. Time-budget: analyzovat jen tolik jobů, kolik se vejde do max_seconds

**Pravidlo:** P13 + P27 (část):
- MCP tool s N>10 I/O operací musí být async s progress streamingem, nebo nahrazen CLI entry pointem
- Pro batching: `limit` + `max_seconds` parametry, vracet `unprocessed_ids`

---

#### GT-014 (CNC-014): WF simulace v3 — emoji v MCP outputu
**Server:** cnc-tools | **Status:** Fixed

**Symptom:** 6 toolů vracelo emoji ([FILE], [OK], [FAIL], [!], [TIMEOUT]) místo ASCII-safe textu.

**Root cause:** Historický pozustatek z vizuálního formátování. Emoji nebyly detekovány code review ani testy.

**Fix:** Vsechny emoji nahrazeny ASCII markery. Grep kontrola: `rg "[\u2600-\u27BF\U0001F000-\U0001FFFF]" src/`.

**Pravidlo:** P28 — Encoding audit v CI: zdrojové soubory nesmí obsahovat emoji. Automatizovatelný grep.

---

### 3.2 linkedin-mcp-custom

#### GT-015 (LNKD-007): Typová záměna BrowserContext vs Browser
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** `get_or_create_browser()` vracelo `BrowserContext`, ale volající kód ocekaval `Browser`. Patchright (Playwright fork) rozlisuje `Browser` (process) a `BrowserContext` (izolovaný session).

**Fix:** Singleton na úrovni `BrowserContext`. Vsechny tool funkce prijímají `context` a volají `context.new_page()`.

---

#### GT-016 (LNKD-008): Shadow lokální proměnná (Missing global)
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** Python bez `global` deklarace vytvorí lokální shadow proměnnou. `close_browser()` zapisovala `_context = None` bez `global _context`.

**Fix:** Pridáno `global _context, _page, _playwright` do každé funkce, která zapisuje do globálních proměnných.

**Pravidlo:** P7 — Každá funkce zapisující do modulové globální proměnné musí mít `global jméno`.

---

#### GT-017 (LNKD-009): Auth navigační konflikt
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** `is_logged_in()` volalo `page.goto("/feed/")` — tím opustilo aktuální stránku. Target navigace pak zacala znovu, ale tool uz pokracoval s extrakcí z prázdné stránky.

**Fix:** Auth check pred navigací na target URL. Poradí: (1) `ensure_authenticated(page)`, (2) `navigate_to_page(url)`.

**Pravidlo:** P8 — Auth first, navigace second. Nic mezi ně nevkládat.

---

#### GT-018 (LNKD-010): Fragilita CSS selektorů
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** LinkedIn A/B testy mení CSS class names bez varování. Selektor na CSS trídách je ephemeral.

**Fix:** Dvě vrstvy: (1) specifický CSS selector pro rychlost, (2) text-based fallback `innerText` matching.

**Pravidlo:** P9 — Nikdy nespoléhat jen na CSS třídy. Používat sémantické HTML atributy (`href`, `aria-label`, `role`).

---

#### GT-019 (LNKD-011): Paginační slepota
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** Dva bugy: (1) prepisovač cílové stránky místo klikání na "Další", (2) po kliknutí se neceká na DOM refresh.

**Fix:** `_click_next_page()` hledající "Další" bez ohledu na císlo stránky. `wait_for_timeout(3000)` + `wait_for_selector`.

---

#### GT-020 (LNKD-012): Špatný git repo root v parents indexu
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** `Path.parents` je 0-indexovaný. `parents[1]` je správne pro 2 složky hloubky, pouzito `parents[2]`.

**Fix:** Opraven index + pridan `relative_to()` assert pro verifikaci.

**Pravidlo:** P10 — `Path.parents` je 0-indexovaný od nejbližšího rodiče. Ověř `relative_to()` před prvním použitím.

---

#### GT-021 (LNKD-013): Fragilní extrakce job ID
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** Původní implementace hledala jen `[href*="/jobs/view/"]`. LinkedIn ukládá ID i v data atributech, script JSON blotech, `aria-label`.

**Fix:** 4-vrstvá extrakce: (1) `<a href>`, (2) element attributes, (3) script JSON, (4) full outerHTML regex.

---

#### GT-022 (LNKD-014): KBWriter dedup fallback — `industry` = vzdy None
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** `_find_entry_index()` porovnával `title|company` (správně) proti `title|company.industry` (vzdy None). Company name se nikam neukládala.

**Fix:** Ukládat `eroi.company` do `company.industry`.

---

#### GT-023 (LNKD-015): Summary table non-idempotent
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** `_update_summary_table()` vzdy appendoval nový radek, nikdy nekontroloval existenci radku se stejným ID.

**Fix:** Před appendem zkontrolovat existenci radku; pokud existuje → nahradit. Pokud ne → append.

---

#### GT-024 (LNKD-017): Python version mismatch (.venv vs system)
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** `.python-version` = 3.12, `.venv` vytvoren s Python 3.11 (system). Package se nainstaloval, ale závislosti vyzadují >=3.12.

**Fix:** `uv venv --python 3.12 && uv sync`.

---

#### GT-025 (LNKD-018): Console script not in PATH
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** `uv sync` instaluje konzolové scripty do `.venv/Scripts/`, který není v system PATH.

**Fix:** (1) `.bat` wrapper v repo root, (2) `.venv/Scripts` pridan do User PATH.

**Pravidlo:** P11 + P12 — Po `uv sync` ověř konzolový script. `.bat` wrapper v kazdém repo root.

---

#### GT-026 (LNKD-020): Cookie lifecycle — silent expiry
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** LinkedIn session cookies mají neurcitou dobu expirace (dny az týdny). Bez pre-checku nelze expiraci detekovat.

**Fix:** Session cache (cookie age tracking) + checkpoint detection + explicitní `ensure_authenticated()` pred kazdým scrapingem.

**Pravidlo:** P15 — Session monitoring: pre-check + log + graceful handling.

---

#### GT-027 (LNKD-021): CI/CD cookie export — cookies nejsou JSON
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** Patchright persistent context ukládá cookies do Chromium SQLite databáze, ne jako JSON.

**Fix:** `scripts/export_cookies.py` — export pres `context.cookies()` → JSON → GitHub Secret. Workflow injectuje pres `context.add_cookies()`.

---

#### GT-028 (LNKD-022): PAT workflow scope
**Server:** linkedin-mcp | **Status:** Documented

**Root cause:** `git push` rejectnul commit s `.github/workflows/` — PAT postrádá `workflow` scope.

**Fix:** Pridat `workflow` scope do PAT v GitHub Developer settings.

---

#### GT-029 (LNKD-024): Scorer unit test discovery
**Server:** linkedin-mcp | **Status:** Fixed

**Root cause:** 6/27 nových testů selhalo — ocekavané hodnoty neodpovídaly skutecné scorer logice.

**Fix:** Testy opraveny na aktuální chování. Testy nyní slouží jako living documentation.

---

### 3.3 MCP-Jobs

#### GT-030 (JOBS-022): Silent failure pattern
**Server:** MCP-Jobs | **Status:** Fixed

**Root cause:** Všichni 4 scraperi používali `except Exception: continue`. Změna HTML struktury → tichá ztráta dat.

**Fix:** Per-card `logger.warning()`, skip counter, 0-ads `logger.error()` alert.

**Pravidlo:** P19 — Structured logging v scrape path: per-card logging, skip count, 0-ads alert.

---

#### GT-031 (JOBS-023/SHELL-019/PS-034): Salary filter split vs regex / Shell escaping / PS quoting
**Server:** MCP-Jobs / cross-repo | **Status:** Fixed / Mitigated

**Symptomy:** (a) Salary filter rejectuje ceský formát císla, (b) PowerShell v bash stringu 3/3 selhání, (c) `SyntaxError: f-string: unmatched '['` pri `python -c "..."`.

**Root cause (společná):** Textová data nelze parsovat jednoduchými nástroji (split, int) bez respektování locale/encoding. Shell escaping na Windows je 3-vrstvý problém (PowerShell → cmd.exe → Python).

**Fix (sjednocený):**
1. **Salary:** `_SALARY_NUM_RE = re.compile(r'\d{1,3}(?:[ \u00a0]\d{3})+|\d+')` — respektuje ceský formát
2. **Shell:** Kazdou PS operaci psát jako `.ps1` script
3. **Inline kód:** Nikdy `python -c "..."` s komplexním kódem na Windows PowerShellu

**Pravidlo:** P16 + P22 — PowerShell v bash = piš .ps1 soubor. Nikdy `python -c` s komplexním kódem.

---

#### GT-032 (JOBS-024): Exclude ceština — domain-specific semantics
**Server:** MCP-Jobs | **Status:** Fixed

**Root cause:** Czech exclude terms `poptavam`, `shanim` aplikovány globálně. Na Bazosu znamenají "poptávám zamestnance" (validní job).

**Fix:** Portal-specific exclude listy. Multi-word `hledam praci` ponechany (jednoznacné).

---

#### GT-033 (JOBS-025): ETL feedback loop dependency
**Server:** MCP-Jobs | **Status:** Mitigated

**Root cause:** Zádný mechanismus pro pravidelné ověrení funkcnosti scrapers. HTML struktura portálu se mení bez varování.

**Fix:** ETL runner (`scripts/run_etl.py`) + session-start health check + output/etl_latest.json.

**Pravidlo:** P20 — ETL health check při startu kazdé session. Alert pri >20% poklesu matched ads.

---

#### GT-034 (JOBS-026): LLM-assisted dev blind spots
**Server:** cross-repo | **Status:** Mitigated

**Root cause:** LLM detekuje degradaci existujícího kódu teoreticky, ale ne bez reálných dat.

**Fix:** Pravidelný ETL feedback loop + version comparison + testy s reálným HTML.

---

#### GT-035 (JOBS-027): AST re-parse per ad (N1)
**Server:** MCP-Jobs | **Status:** Fixed

**Root cause:** `evaluate_boolean()` volal `parse_boolean()` pro kazdý inzerát zvlášť. 8 query x 1000 ad = 8000 parsování.

**Fix:** `@functools.lru_cache(maxsize=128)` na `parse_boolean()`. 8000 → 8 parsování.

---

#### GT-036 (JOBS-028): Chybějící guardraily (pages + rate limiting)
**Server:** MCP-Jobs | **Status:** Fixed

**Root cause:** Bulk-scrape neměl zádný limit. `search_jobs_v2(pages=500)` by spustilo stovky requestů.

**Fix:** `pages = max(1, min(pages, 50))` clamp guard + `request_delay=1.0` + `_throttle()`.

---

#### GT-037 (JOBS-029): Boolean auto-validace při config loadu
**Server:** MCP-Jobs | **Status:** Fixed

**Root cause:** `validate_boolean()` existovala, ale nikdo ji nevolal při loadu configu.

**Fix:** Volání `validate_boolean(qc.boolean)` v `UserConfig._from_raw()`.

---

#### GT-038 (JOBS-030): MCP error kontrakt
**Server:** MCP-Jobs | **Status:** Fixed

**Root cause:** Kazdý tool rešil error handling jinak. Per-provider errors vraceny embedded v datech.

**Fix:** Jednotný formát: `[{"error": "..."}]` pro vsechny tools.

---

#### GT-039 (JOBS-031): Config error messages + lint
**Server:** MCP-Jobs | **Status:** Fixed

**Root cause:** `CategoryConfig(**c)` házel raw TypeError na neznámý YAML klíc.

**Fix:** try/except TypeError s popisnou zprávou. Importy přesunuty na top-level.

---

#### GT-040 (JOBS-033): L2 Resources — mcp-jobs://ads/{query_id}
**Server:** MCP-Jobs | **Status:** Fixed

**Root cause:** Search tooly vracely data jen v kontextu LLM. Bez L2 Resources nebyly výsledky adresovatelné.

**Fix:** 3 resources: `/list`, `/{query_id}`, `/{query_id}/report`. In-memory `_query_store`.

**Pravidlo:** P21 — L2 Resources (URI-adresovatelná data) pro kazdý MCP server, který produkuje data.

---

#### GT-041 (JOBS-034+035): 6-layer encoding stack
**Server:** cross-repo | **Status:** Implemented

**Systematické rešení encoding/quoting na Windows.** Defense in depth:

| # | Vrstva | Mechanismus |
|---|--------|-------------|
| 6 | PS autoload | `_github/_init.ps1` → `$PROFILE` |
| 5 | AI guardrails | `.ai_guardrails.json` shell_rules |
| 4 | Dokumentace | `docs/powershell_encoding.md` |
| 3 | Project helpers | `scripts/init.ps1` wrappery |
| 2 | Batch launcher | `set PYTHONIOENCODING=utf-8` + `PYTHONUTF8=1` |
| 1 | Python runtime | `ensure_utf8_stdout()` |

---

#### GT-042 (CNC-014 continuation): Session compact — MCP workdir vs source code
**Server:** cross-repo | **Status:** Documented

**Symptom:** Session compact = prepnutí kontextu MCP toolů, ne source code. Nejednoznacnost kde spouštět príkazy.

**Lesson:** Vsechny bash príkazy musí mít explicitní `workdir` parametr.

---

#### GT-043 (lichess-001): Editable install — .pth path jen src/, chybi project root
**Server:** lichess-analyzer | **Status:** Fixed

**Symptom:** `python -m src.server` → `ModuleNotFoundError: No module named 'src'`. Opencode hlasi status "invalid".

**Root cause:** `uv pip install -e .` vytvorilo `__editable__.lichess_analyzer_mcp-0.1.0.pth` s jedinou radkou: `C:\...\lichess-analyzer-mcp\src`. Kod ale importuje `from src.app import app` — potrebuje project root na sys.path, ne `src/`. Bez nej `-m src.server` hleda `src/server.py` pod `src/` → `src/src/server.py`, ktere neexistuje.

**Fix:** Pridana druha radka do `.pth`:
```
C:\Users\PC\Documents\Repozitar_Dev\_github\lichess-analyzer-mcp
C:\Users\PC\Documents\Repozitar_Dev\_github\lichess-analyzer-mcp\src
```

**Pravidlo:** P29 (cast) — Po `pip install -e .` se `src` layoutem over `.pth` content. Project root musi byt prvni.

---

#### GT-044 (lichess-002): async def main() + asyncio.run(app.run()) — event loop konflikt
**Server:** lichess-analyzer | **Status:** Fixed

**Symptom:** Server startne (logy do stderr), pak okamzite pada s `RuntimeError: Already running asyncio in this thread`. Bez otevreneho STDIO kanalu.

**Root cause:** FastMCP `app.run()` interně volá `anyio.run(self.run_stdio_async)` — spousti vlastni event loop. Obaleni do `asyncio.run(main())` vytvari druhy event loop → konflikt.

**Fix:** main() musi byt sync:
```python
def main():
    app.run()

if __name__ == "__main__":
    main()
```

Misto puvodniho:
```python
async def main():
    await app.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())  # RuntimeError: Already running asyncio
```

**Pravidlo:** P29 — FastMCP server: main() vzdy sync `def main(): app.run()`. Nikdy `asyncio.run(app.run())` — app.run() uz spousti vlastni event loop.

---

### 3.5 lichess-analyzer-mcp — LLM Reasoning Pipeline

#### GT-045 (lichess-003): Cerebras API response format — `reasoning` misto `content`
**Server:** lichess-analyzer | **Status:** Fixed

**Symptom:** Cerebras API vrací 200 OK, ale `content = data["choices"][0]["message"]["content"]` je `None`. Pipeline hlásí "fallback" nebo padá do `str(data)` raw JSON dumpu.

**Root cause:** Cerebras API používá proprietární `reasoning` field v message objektu namísto standardního `content`. OpenAI kompatibilní klienti očekávají `message.content`.

**Fix:** Fallback chain v parseru:
```python
msg = data["choices"][0]["message"]
content = msg.get("content") or msg.get("reasoning")
```

**Pravidlo:** P30 — LLM klient musí mít fallback chain pro nestandardní response fieldy u kazdého provideru. Nikdy nespoléhat na `["content"]` bez `get()`.

---

#### GT-046 (lichess-004): LLM_MAX_TOKENS clipping — nekompletní coaching reporty
**Server:** lichess-analyzer | **Status:** Fixed

**Symptom:** DeepSeek V4 Flash vrací report useknutý uprostřed vety (2895 tok). Chybí sekce "Silné stránky" a "Zaměření na další sezení".

**Root cause:** Default `LLM_MAX_TOKENS=2000` je nedostatecný pro 6 patternu + weakness report + 5 sekcí. DeepSeek V4 Flash má prumernou odezvu ~3500 tok pro plný report.

**Fix:** `LLM_MAX_TOKENS` zvýsen na 4000. Report rozsíren na 3472 tok (plných 5 sekcí, 53 lines).

**Pravidlo:** P31 — LLM coaching pipeline: `max_tokens >= 4000`. Default 2000 testovat na reprezentativním vzorku, ne jen na 1-2 patternech.

---

#### GT-047 (lichess-005): Cascade provider silence
**Server:** lichess-analyzer | **Status:** Mitigated

**Symptom:** Uzivatel neví, které providery byly k dispozici a který z nich vyhrál. Cascade skončí na prvním úspechu, ale stav ostatních není videt.

**Root cause:** `generate_coaching_report_with_logs` vrací cascade_log jako tuple, ale volající kód casto pouzívá jen `generate_coaching_report` (bez logu). Console vitezství providera není nikde perzistentní.

**Fix:** Cascade log vracen paralelne s reportem. Report header nyní uvádí providera, model, tokens, cost, latency.

**Pravidlo:** P32 — Cascade fallback: vzdy expose per-provider status (attempted/skipped/error) do výstupu. Nikdy netlacit stav provideru.

---

#### GT-048 (lichess-006): Timing dict type change — silent crash
**Server:** lichess-analyzer | **Status:** Fixed

**Symptom:** `TypeError: unsupported format string passed to dict.__format__`. Pipeline crashne po LLM callu, report se nezapíse.

**Root cause:** Time format zmenen z `{"phase": float}` na `{"phase": {"duration": float, "label": str}}`. `md_reporter.py` pouzíval `timing.get("total", 0)` — ocekava float, dostává dict.

**Fix:** Zmena vsech prístupu k timing datum: `.get("total", {}).get("duration", 0)`.

**Pravidlo:** P33 — Po zmene datového formatu aktualizuj VŠECHNY konzumenty, nejen producenta. Testuj s reprezentativními daty (ne jen unit testy s mocky).

---

#### GT-049 (lichess-007): Cache dump key mismatch
**Server:** lichess-analyzer | **Status:** Fixed

**Symptom:** `compare_providers.py` nacítá 0 patternu z cached dumpu. Provideri generují reporty bez pattern analyzy (pouze weakness report).

**Root cause:** Dump file (`test_optimized_output.json`) pouzívá klíce `patterns_detected` a `games_analyzed` (list). Skript hledá `patterns` a `analyses_data`. Zádný klíč nesedí.

**Fix:** Fallback chain: `.get("patterns_detected", data.get("patterns", data.get("pattern_results", [])))`.

**Pravidlo:** P34 — Cache/export JSON schema musí být explicitne zdokumentována a verze kontrolována. Libovolný konzument musí pouzívat fallback chain.

---

#### GT-050 (lichess-008): Stockfish re-analýza pri kazdém běhu — 24 min pipeline
**Server:** lichess-analyzer | **Status:** Fixed

**Symptom:** 5 her = 24 min pipeline. 99.9% casu spotrebovává Stockfish (deterministický, opakovatelný krok).

**Root cause:** Zádné cache-mechanismus. Kazdý pipeline run analyzuje vsechny hry Stockfishem znovu, i kdyz výsledek je deterministicky stejný.

**Fix:** `cache_first` strategie:
1. Pred Stockfish analyzou zkontrolovat `data/game_cache/{game_id}.json`
2. Pokud existuje a depth >= requested → pouzít cache
3. Jinak analyzovat a ulozit do cache
4. Výsledek: 5 her = 0.1s (místo 24 min)

**Pravidlo:** P35 — Deterministické pipeline kroky (Stockfish analyza) cacheovat (game_id + depth jako klíč). LLM inference ne — kazdý běh = nová odpoved.

---

#### GT-051 (lichess-009): Provider model ID — UI vs API discrepancy
**Server:** lichess-analyzer | **Status:** Mitigated

**Symptom:** Cerebras model `llama3.1-8b` (z dokumentace) vrací 404. NVIDIA model `nvidia/nemotron-3-super-120b-a12b` na `api.nvidia.com` vrací SSL error.

**Root cause:** (a) Cerebras API model ID != display name/docs. Skutecný model: `gpt-oss-120b`, `zai-glm-4.7`, `gemma-4-31b`. (b) NVIDIA endpoint `api.nvidia.com` nepouzívá standardní /v1 schema — SSL hostname mismatch fix pres `integrate.api.nvidia.com/v1`.

**Fix:** Vzdy volat `/v1/models` endpoint pro discovery. Vyreseno 2026-07-20: NVIDIA base URL fix, Cerebras model ID correct.

**Pravidlo:** P36 — Provider model ID vzdy overit pres `/v1/models` API. Docs a UI jsou nespolehlivé. Po zmene providera endpointu testovat s minimálním promptem (1 token).

---

#### GT-052 (lichess-010): SNR evaluation framework
**Server:** lichess-analyzer | **Status:** Documented

**Poznatek:** Při porovnání 3 LLM provideru (NVIDIA, Cerebras, DeepSeek V4 Flash) vznikl metodologický problém: jak objektivne urcit, který výstup je kvalitnejsí, bez subjektivního biasu.

**Resení:** SNR (Signal-to-Noise Ratio) evaluation framework:

| Kriterium | Váha | Co merí |
|---|---|---|
| Grounding k patternum | 30% | Zda report pouzívá stejné patterny jako vstup (ne inventuje) |
| Konfidence % citace | 20% | Zda uvádí confidence hodnoty z pattern detectionu |
| Phase ACPL citace | 15% | Zda cituje fázová ACPL data z weakness reportu |
| Hallucinace (míň = líp) | 20% | Inventované patterny nebo nepodlozená tvrzení |
| Struktura/délka | 10% | Zda pokrývá vsech 5 sekcí |
| Tréninková konkrétnost | 5% | Konkrétní cvicení vs obecná doporucení |

**Aplikace:** DeepSeek V4 Flash SNR 93/100 (nejvyssí), NVIDIA 57, Cerebras 54.

**Pravidlo:** P38 (metodologické) — Porovnání LLM výstupu: vzdy pouzít SNR framework s váhami. Nikdy subjektivní "libí se mi".

---

#### GT-053 (lichess-011): DeepSeek Chat — cost ban policy
**Server:** lichess-analyzer | **Status:** Fixed (policy)

**Symptom:** Financní — DeepSeek Chat ($0.27/$1.10 per 1M tok) je 3.6× drazsí nez DeepSeek V4 Flash ($0.14/$0.28) za stejnou nebo horsí kvalitu.

**Decision:** DeepSeek Chat vyrazen z default cascade. Ponechán v `PROVIDERS` konfiguraci pro explicitní volání. Zakázán v default `cascade_order`.

**Pravidlo:** P37 — Kazdý provider v LLM cascade musí mít explicitní cost/benefit schválení. Drazsí alternativy (>2× cena za stejnou kvalitu) blokovat v default konfiguraci.

---

#### GT-054 (lichess-012): Multi-provider API key management
**Server:** lichess-analyzer | **Status:** Documented

**Poznatek:** Tři API klíce (NVIDIA, Cerebras, DeepSeek) vyzadují kazdý jiné nakládání:
- NVIDIA: spolecný free key, omezený rate limit
- Cerebras: free + $5 credit, model specificky
- DeepSeek: jeden key pro chat i v4 flash, paid (credit-based)

**Best practice:** `.env` soubor s exportem vsech klícu. `auth.json` v `~/.local/share/opencode/` pro centrální správu.

**Pravidlo:** P39 — Multi-API key management: `.env` pro lokální vývoj, `auth.json` pro opencode, `.gitignore` pro oba. Nikdy necommitovat.

---

#### GT-055 (lichess-013): LLM_MAX_TOKENS env var — silent fallback na default
**Server:** lichess-analyzer | **Status:** Fixed

**Symptom:** `os.environ.get("LLM_MAX_TOKENS", "2000")` vrací 2000 i kdyz promenná není nastavena. Zádná warning/error ze by default mohl být nedostatecný.

**Root cause:** Env var je optional. Pokud chybí, pouzije se default — ale uzivatel neví, ze by mel nastavit vyssi hodnotu pro plný report.

**Fix:** Startup log: `print(f"[llm] LLM_MAX_TOKENS={llm_max_tokens} (recommended >=4000 for full reports)", file=sys.stderr)`.

**Pravidlo:** P40 — Env var s velkým dopadem na kvalitu výstupu musí logovat varování pri nedoporučené hodnote. Ne jen tichý default.

---

#### GT-056 (lichess-014): Per-game LLM cache — Level 2 cache pro inkrementální agregaci
**Server:** lichess-analyzer | **Status:** Implemented

**Symptom:** Pri pridání nové hry do pipeline se LLM layer spoustí znovu na VŠECHNY hry. S rostoucím N lineárne roste prompt size i cost.

**Root cause:** LLM prompt obsahuje inline raw data vsech her. Nelze oddelit "uz analyzované" od "nových".

**Resení:** Dvouúrovnová cache:

| Level | Obsah | Cache soubor |
|---|---|---|
| L1 (existuje) | Stockfish analyza | `{game_id}_{color}_d{depth}.json` |
| L2 (nový) | LLM per-game analyza | `{game_id}_llm.json` |

Per-game LLM analyza (deep analysis frontiervým modelem) → cache. Agregace pouzívá L2 summaries místo raw dat. Nová hra = jen 1 L2 call + 1 agregacní call se summaries z cache.

**Implementace:** `src/services/game_llm_cache.py`. Uprava `build_coaching_prompt()` o `game_summaries` parametr.

**Pravidlo:** P41 — Dvouúrovnová cache pro LLM pipeline: Level 2 (per-game LLM) oddeluje analyzu od agregace.

---

#### GT-057 (lichess-015): NVIDIA timeout na agregaci s per-game summaries
**Server:** lichess-analyzer | **Status:** Documented

**Symptom:** Agregacní call s 5 per-game summaries timeoutuje na NVIDIA. Cerebras nebo DeepSeek V4 uspějí.

**Root cause:** Prompt s summaries (~2500 chars) delsí → vyssi pravdepodobnost timeoutu na free NVIDIA tieru.

**Fix:** Cascade resilience: timeout providera preskocí. Pro agregaci se summaries pouzít Cerebras nebo DeepSeek V4.

**Pravidlo:** P42 — Cascade je resilience pattern. Timeout jednoho providera neblokuje pipeline.

---

#### GT-058 (lichess-016): Pipeline mode — monolit vs inkrementalni cache
**Server:** lichess-analyzer | **Status:** Implemented

**Poznatek:** Per-game LLM cache není univerzálne výhodná. Pro malé N (≤30) je monolit efektivnejší (méne tokenu, kratsí cas). Pro velké N (100+) se cache amortizuje a prinásí 44% úsporu.

**Resení:** `run_coaching_pipeline(mode)` s auto-detekcí:

```python
def run_coaching_pipeline(..., mode="auto"):
    if mode == "auto":
        mode = "mono" if n <= 30 else "incremental"
```

Golden rules:
- N≤30 + rychlá analýza → monolit
- N>30 + dávková analýza → inkrementalní (cache)
- PGN import / GM hry → inkrementalní (per-game deep analysis)
- Explicitní `PIPELINE_MODE` env var override

**Implementace:** `run_coaching_pipeline()` v `llm_client.py`. Minimalní scope creep — jedna wrapper funkce, stávající API beze zmeny.

**Pravidlo:** P43 — Pipeline mode: monolit pro N≤30, inkrementalní pro N>30. Golden rules: explicitní override pres PIPELINE_MODE env var nebo parametr.

---

#### GT-059 (lichess-017): _build_game_prompt wrong key names → low SNR
**Server:** lichess-analyzer | **Status:** Fixed | **Typ:** Application logic — Key mapping bug

**Poznatek:** Per-game LLM výstupy mely low SNR. Debug odhalil 3 bugy:

1. **Wrong key names v `_build_game_prompt()`**: `move_number` misto `ply`, `san` misto `move_san`, `cp_loss` misto `centipawn_loss`. LLM dostaval `move ?, loss ?cp` — skutecná data se ztrácela.
2. **`accuracy: 0.0`**: auto_annotate() nepočítalo accuracy. Všechny cache soubory mely accuracy=0.0.
3. **`phase_stats: {}`**: phase_stats nebylo nikdy populováno.

**Resení:**
- Opraveny klíce v `_build_game_prompt()`: `ply`, `move_san`, `centipawn_loss`
- Přidány `_compute_accuracy()` a `_compute_phase_stats()` do `GameAnalysis.auto_annotate()`
- Opraveno 18 stale cache souborů skriptem `scripts/repair_cache.py`
- Vytvořeny contract testy v `tests/test_prompt_contract.py` (13 testu)

**Contract test strategy — detail:**
Problém spadá do domény **Contract Testing** (Consumer-Driven Contract), podmnoziny Integration Testing v testovací ontologii:

```
Unit Tests          ← testují jednu funkci/třídu izolovaně
  ↓
Contract Tests      ← ← ← testují rozhraní mezi moduly
  ↓
Integration Tests   ← testují vice modulu dohromady
  ↓
E2E Tests           ← testují celý systém
```

Oba moduly (GameAnalysis.to_dict() a _build_game_prompt()) procházely unit testy v izolaci. Problém byl v *rozhraní mezi nimi* — nikdo netestoval, zda klíče, které prompt builder čte, odpovídají klíčům, které model produkuje.

Implementováno ve 3 vrstvách:

1. **Schema testy** — load real cache JSON, check all keys prompt reads:
   `test_blunder_subkeys` overuje, ze kazdy blunder ma `ply, move_san, centipawn_loss, phase`
2. **Placeholder detection** — `test_prompt_has_no_unknown_move` kontroluje, ze prompt neobsahuje `?`
3. **Noise-floor detection** — `test_accuracy_not_zero` overuje semantickou konzistenci dat

**Profesionální nástroje vs lightweight varianta:**
V enterprise microservices se pouziva **Pact** (pact.io) — consumer definuje ocekavani v testu, producer se verifikuje proti nemu. Pro MCP server je adekvátní lightweight varianta: schema test na realnych datech + placeholder detection (`assert "?" not in prompt`). Viz `01_METODIKY/05_testing/contract_testing_ontologie_v1.md`.

**Vysledek po fixu:**
- Pred: `"accuracy 0.0%", "Middlegame blunder (move ?, loss ?cp)"`
- Po: `"přesnost 94,6%", "move 27, Ng3 (blunder), cp_loss 497"` — specifická, akcní rada

**Pravidlo:** P44 — Contract testy mezi moduly. Kazdy modul v pipeline musí mít test, ktery overuje konzistenci klícu mezi producerem a consumerem. Consumer definuje kontrakt. Test selze dríve, nez se bug dostane do LLM outputu.

---
#### GT-060 (lichess-018): Iteracni optimalizace - JSON validation, CI/CD, unit testy sluzeb, API key check
**Server:** lichess-analyzer | **Status:** Implemented | **Typ:** Infrastructure + kvalita

**Poznatek:** Meta-analyza po GT-059 odhalila 4 kriticke slabiny:
1. Per-game LLM output neni validovan jako JSON pred cachingem - tichy fail na dalsim cteni
2. Chybi CI/CD - testy se pousteji jen rucne
3. `engine_client.py` nema unit testy - sluzba je netestovana
4. API klice se nekontroluji pri startu - vyprseny klic = silent fail na cascade

**Reseni:**
1. `game_llm_cache.py`: Pridano `_validate_json_output()` - kontroluje JSON parsovatelnost, extrakci z ```json bloku. Pokud LLM vrati garbage, cascade zkusi dalsiho providera.
2. `.github/workflows/test.yml`: GitHub Actions - push/PR na main spusti `ruff check` + `pytest` na Python 3.12.
3. `tests/test_engine_client.py`: 5 unit testu s mocknutym Stockfish - `_find_stockfish()`, `analyze_position()`, `evaluate_move()`, `close_engine()`. Zadna realna binary potreba.
4. `llm_client.py` + `server.py`: `verify_api_keys()` pri startupu posle ping (max_tokens=1, timeout=10s). Vystup: `[server] API key check`. Detekuje 401/402/429.

**Stav testu:** 33/33 pass (15 unit + 13 contract + 5 engine mock)
**CI/CD:** `.github/workflows/test.yml` (Linux, Python 3.12, ruff + pytest)

**Pravidlo:** P45 - API key health check pri startupu. `verify_api_keys()` v `server.py`. Lightweight ping (max_tokens=1, timeout=10s). Detekuje neplatny/vyprseny klic pred prvnim tool volanim.


## 4. Průřezová pravidla P1-P40 (konsolidovaná)

### P1 — Paralelizace
Jakmile tool iteruje N>1 nezávislých zdrojů (repozitáře, soubory, API), použij `ThreadPoolExecutor`. Počet workerů: min(4, N). I/O-bound operace skálují lineárne do ~8 vláken.

### P2 — Časové konstanty
Subprocess timeout v MCP toolu musí být max 25% MCP client timeoutu. Client timeout 60s → subprocess timeout 15s. Fail fast, fail loud.

### P3 — Read-only locky
Kazdý read-only subprocess call (git, grep, diff) používej `["git", "--no-optional-locks"]`. Eliminuje filesystem lock contention.

### P4 — JSON defenziva
Kazdý JSON state deserializer: `try/except` + `isinstance(v, dict)` guard + auto-repair. Počítej s corrupt daty.

### P5 — Diagnostika
`@auditable` na kazdém toolu. Povinné: `ts`, `tool`, `duration_s`, `ok`. Bez metriky není diagnostika.

### P6 — Timeout guard
I/O tool s potenciálem >10s → wrapper s `concurrent.futures.TimeoutError`.

### P7 — Globální proměnné
Kazdá funkce, která zapisuje do modulové globální proměnné, musí mít `global jméno`. Python bez `global` vytvorí lokální shadow — tichá ztráta dat.

### P8 — Pořadí operací
Auth/navigace/destruktivní operace: auth first, navigace second. Nic mezi ně nevkládat.

### P9 — Žádné CSS třídy v selektorech
Používej sémantické HTML atributy (`href`, `aria-label`, `role`). CSS třídy jsou ephemeral — A/B testy je mení bez varování.

### P10 — Verifikace cest
`Path.parents` je 0-indexovaný od nejbližšího rodice. Ověř `relative_to()` pred prvním pouzitím.

### P11 — Console script distribution
Po `uv sync` vzdy explicitně ověř, z ekonzolový script je dostupný:
```bash
.venv/Scripts/<tool> --help   # musí fungovat
where <tool>                   # musí najít exe
```
Pokud `where` selze → pridej `.venv/Scripts` do PATH nebo vytvor `.bat` wrapper.

### P12 — Cross-shell launcher
Kazdý CLI nástroj na Windows musí mít `.bat` wrapper v repo root:
```batch
@echo off
"%~dp0.venv\Scripts\<tool>.exe" %*
```

### P13 — Long-running batch operations
MCP tool, který iteruje N>10 I/O operací, musí být buď:
1. Asynchronní s progress streamingem (MCP `ctx.info()`), nebo
2. Nahrazen CLI entry pointem, který obchází MCP transport timeout

### P14 — Windows path quoting
- Vzdy `pathlib.Path` (nikdy string concatenation)
- Pri predání cesty subprocessu: `str(resolved_path)` + explicitní quoting
- Testuj cesty v cmd.exe, PowerShell i Git Bash
- `_github\` prefix ~70 chars → riziko MAX_PATH (260 chars)

### P15 — Session monitoring
Pred kazdým pipeline runem: (1) `is_logged_in()` + log `page.url`, (2) pokud auth selze, loguj response body (může být checkpoint), (3) `--login` flow bez restartu MCP serveru.

### P16 — PowerShell v bash = piš .ps1 soubor
Nikdy nevkládej PowerShell one-linery do bash stringů. Vzdy: napiš `.ps1` script, spust pres `powershell -File scripts/operace.ps1`.

### P17 — Workspace context export
Kazdý MCP server pro LLM agenty musí:
1. Při startu vypsat workspace root do stderr: `print(f"[server] Workspace root: {root}", file=sys.stderr)`
2. Poskytnout `tool_workspace_info()` vracející root, guardrails profil, index summary
3. Kontextové soubory prednačíst do cache pri startu

### P18 — Console encoding na Windows (Unicode safety)
1. `$env:PYTHONIOENCODING='utf-8'` pred kazdým python príkazem
2. `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` v startupu
3. Emoji zakázána v kódu (.ai_guardrails.json)

### P19 — Structured logging v scrape path
Kazdý scrape modul musí mít: per-card `logger.warning()`, skip counter, 0-ads `logger.error()` alert.

### P20 — ETL health check / session-start protocol
Kazdý MCP server s externími zdroji musí mít: ETL runner + session-start health check + alert threshold (>20% pokles matched ads).

### P21 — L2 Resources (URI-adresovatelná data)
Tool vyrobí data jednou, resource je zpřístupňuje opakovaně. URI schema: `server://{namespace}/{id}`.

### P22 — Windows PowerShell: nikdy `python -c` s komplexním kódem
`python -c "..."` s f-stringy, vnorenými uvozovkami, cykly je křehký. Root cause: Windows API `CommandLineToArgvW` delí argument na mezerách.

### P23 — Windows encoding: PYTHONIOENCODING + PYTHONUTF8 + -X utf8
Tri úrovne ochrany: (1) shell-level env var, (2) process-level `-X utf8`, (3) code-level `sys.stdout.reconfigure()`.

### P24 — Python version audit
- Nikdy pre-release Python (< stable) pro MCP servery
- `requires-python = ">=3.12.0,!=3.11.0rc1,!=3.11.0rc2"` v pyproject.toml
- Version check pri startu serveru

### P25 — stderr hygiene
- Nikdy StreamHandler(sys.stderr) v MCP serveru
- Logovat jen do FileHandler nebo rotating file
- Audit log = file-based, ne stderr-based

### P26 — asyncio subprocess
- Vsechna I/O v MCP tools pres `asyncio.create_subprocess_exec()`
- `stdin=asyncio.subprocess.DEVNULL` pro git operace
- `asyncio.wait_for(proc.communicate(), timeout=15)` pro fail-fast
- Vzdy `cwd=` explicitně
- `subprocess.run` zakázán v MCP tools

### P27 — MCP test pyramida
1. Unit vrstva — testy logiky jednotlivých nástrojů
2. Integration vrstva — testy MCP request/response (pres FastMCP.call_tool)
3. E2E vrstva — testy pres reálný STDIO transport
4. Smoke test po kazdé změně: `git_status(B2B-Knowledge-Base)` <5s

### P28 — Encoding audit v CI
Kazdý build musí kontrolovat, ze zdrojové soubory neobsahují emoji:
```bash
rg "[\u2600-\u27BF\U0001F000-\U0001FFFF]" src/
```

### P29 — FastMCP main() sync, nikdy async wrapper
`app.run()` (FastMCP) interně volá `anyio.run()` = spoustí vlastní event loop. main() musí byt sync:

```python
# SPRAVNE
def main():
    app.run()

if __name__ == "__main__":
    main()

# CHYBNE — RuntimeError: Already running asyncio
async def main():
    await app.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Rozsireni:** Po `pip install -e .` se `src` layoutem over `.pth` obsahuje project root, nejen `src/`.

### P30 — LLM response format fallback
`data["choices"][0]["message"]["content"]` není univerzální. Cerebras pouzívá `reasoning` místo `content`. Pouzívat `msg.get("content") or msg.get("reasoning")`.

### P31 — LLM max_tokens pro coaching
Coaching pipeline s 6+ patterny a 5 sekcemi vyzaduje `max_tokens >= 4000`. Default 2000 testovat na reprezentativním vzorku.

### P32 — Cascade status exposure
Cascade fallback musí expose per-provider status (attempted/skipped/error + tokens + cost) do výstupu. Nikdy netlacit stav provideru.

### P33 — Data format change consistency
Po zmene datového formatu aktualizovat VŠECHNY konzumenty. Testovat s reprezentativními daty, ne jen unit testy.

### P34 — Cache schema versioning
Cache/export JSON schema explicitne dokumentovat a verze kontrolovat. Konzumenti pouzívat fallback chain pres `.get()`.

### P35 — Deterministické kroky cacheovat
Stockfish analyza (deterministická) cacheovat pres `game_id + depth`. LLM inference ne — kazdý běh = nová odpoved.

### P36 — Provider model ID overení
Vzdy volat `/v1/models` API pro discovery. Docs a UI jsou nespolehlivé. Testovat s minimálním promptem.

### P37 — Cost/benefit provider governance
Kazdý provider v LLM cascade musí mít explicitní cost schválení. Drazsí alternativy (>2× cena za stejnou kvalitu) blokovat.

### P38 — SNR evaluation framework
Porovnání LLM výstupu: vzdy pouzít SNR framework (grounding 30%, confidence 20%, phase data 15%, hallucinations 20%, structure 10%, concreteness 5%).

### P39 — Multi-API key management
`.env` pro lokální vývoj, `auth.json` pro opencode, `.gitignore` pro oba. Kazdý provider muze mít jiný key management (free vs paid, shared vs dedicated).

### P40 — Env var warning na suboptimal values
Env var s dopadem na kvalitu musí logovat varování pri hodnotách pod doporuceným minimem. Příklad: `LLM_MAX_TOKENS=2000` → warning "recommended >=4000".

### P41 — Dvouúrovnová LLM cache (Level 2)
Per-game LLM analyzu cacheovat do `{game_id}_llm.json`. Agregace pouzívá summaries z cache místo raw dat. Nová hra = 1 L2 call + 1 agregace, ne full re-run.

### P42 — Cascade resilience
Timeout nebo error jednoho providera v cascade nesmí blokovat pipeline. Cascade je resilience pattern — dalsí provider v poradí prevezme.

### P43 — Pipeline mode (monolit vs inkrementalni)
N≤30 → monolit (1 LLM call). N>30 → inkrementalni (per-game cache + aggregate). Golden rules: rychlá analýza = monolit, hromadná / PGN import = inkrementalni. Explicitní override pres `PIPELINE_MODE` env var.

### P44 — Contract testy mezi moduly (Consumer-Driven Contract)
Kazdy modul v pipeline (Stockfish analyzer → prompt builder → LLM) musí mit contract test, ktery overuje konzistenci klícu mezi producerem a consumerem. Consumer definuje kontrakt (jake klíce potrebuje). Test je schema test na realnych datech + placeholder detection. Profesionalni nastroj: Pact. Lightweight varianta: `assert key in data` + `assert "?" not in prompt`. Reference: `01_METODIKY/05_testing/contract_testing_ontologie_v1.md`.

---

## 5. Diagnostický filtr — 49 checkpoints

### A — Časové konstanty
1. Je subprocess timeout kratsí nez MCP client timeout? (P2)
2. Je subprocess timeout ≤15s pro git operace? (P2)
3. Mají vsechny subprocess volání explicitní `timeout=`? (P2)

### B — Paralelizace
4. Iteruje tool pres N>1 nezávislých zdrojů? → paralelizovat (P1)
5. Je `git_status_all` implementován s `ThreadPoolExecutor`? (P1)
6. Je `cross_repo_search` s `ThreadPoolExecutor`? (P1)
7. Je počet workerů 4-8 pro I/O-bound? (P1)

### C — Git operace
8. Mají vsechny git subprocess volání `--no-optional-locks`? (P3)
9. Je timeout pro git grep/log/diff jednotný? (P2)
10. Vrací timeoutnutý subprocess error okamzitě? (P2)

### D — JSON storage
11. Má JSON state load `try/except`? (P4)
12. Má kazdá deserializovaná hodnota `isinstance(v, dict)`? (P4)
13. Existuje auto-repair pro poskozené záznamy? (P4)

### E — Diagnostika
14. Mají vsechny nástroje `@auditable` dekorátor? (P5)
15. Loguje audit `duration_s` pro kazdý tool call? (P5)
16. Je audit log JSON lines? (P5)

### F — Timeout guard
17. Má tool s dlouhým během (>10s) timeout wrapper? (P6)
18. Vrací timeoutnutý tool error místo blokování serveru? (P6)

### G — Workspace context
19. Vypisuje server při startu workspace root do stderr? (P17)
20. Existuje tool vracející workspace info? (P17)
21. Jsou kontextové soubory prednačteny při startu? (P17)

### H — Console encoding
22. Je `PYTHONIOENCODING=utf-8` nastaveno? (P18, P23)
23. Má server `sys.stdout.reconfigure(encoding='utf-8')`? (P18)
24. Jsou emoji vyloucena ze zdrojového kódu? (P28)

### I — Python version & deploy
25. Je Python stabilní release (ne rc/alpha/beta)? (P24)
26. Je `requires-python` explicitní v pyproject.toml? (P24)
27. Existuje version check při startu serveru? (P24)

### J — stderr hygiene
28. Je StreamHandler(sys.stderr) odstraněn? (P25)
29. Jsou vsechny print/log výstupy směrovány do souboru? (P25)
30. Je audit log file-based, ne stderr-based? (P25)

### K — async subprocess
31. Jsou vsechna subprocess volání async? (P26)
32. Mají git operace `stdin=DEVNULL`? (P26)
33. Je timeout ≤15s + `asyncio.wait_for`? (P26)
34. Jsou `cwd` a env parametry explicitní? (P26)

### L — Test pyramida
35. Existuje MCP integration test (tool → framework, bez STDIO)? (P27)
36. Existuje MCP E2E test (pres reálný STDIO)? (P27)
37. Bězí smoke test (`git_status` <5s) po kazdé zmene? (P27)
38. Jsou transport-level anomálie pokryty testy? (P27)

### M — Diagnostika / monitorování
39. Je `git log -5` promptnejsi nez `-20`?
40. Existuje `ping()` tool pro ověření, ze server zije?
41. Je MCP client timeout konfigurovatelný per-tool?
42. Je v logu timestamp + duration pro kazdý subprocess call?
43. Lze rozlišit "server mrtev" od "tool zpracovává"?

### N — Encoding & Console (rozsířeno)
44. Je PYTHONIOENCODING=utf-8? (P18, P23)
45. Má server `sys.stdout.reconfigure('utf-8')`? (P18)
46. Jsou emoji a Unicode supplementary zakázány v kódu? (P28)
47. Vrací tool ceské znaky bez chyby? (P23)

### O — Server initialization (P29)
48. Je main() sync `def main(): app.run()`? Nikdy `async` + `asyncio.run()` (P29)
49. Ma `.pth` soubor po `pip install -e .` project root + `src/`, ne jen `src/`? (P29)

---

## 6. EROI rozhodovací framework

### 6.1 Kdy MCP NEPOUZÍT

| Situace | Proc MCP nefunguje | Co místo toho |
|---------|-------------------|---------------|
| Sub-100ms operace (ctení 1 souboru) | JSON-RPC overhead > samotná operace | CLI nebo skript |
| Hromadné operace (git status na 13 repo) | Sériové volání 13x tool je pomalejší | Dávkový skript |
| Jednorázové ad-hoc príkazy | Tool musíš definovat, otestovat, dokumentovat | CLI |
| Credentials / secrets | Riziko úniku do LLM kontextu | OS env var + gh CLI |
| 100% determinismus | LLM se muze rozhodnout tool nepouzít | Skript/Makefile |
| Rychle se menící API | Kazdá zmena toolu = restart serveru | Jupyter / skript |

### 6.2 EROI matice

| | Jednoduché rešení | Slozité rešení |
|--|------------------|----------------|
| **Vysoká potřeba MCP** | MCP dává smysl (doménové nástroje, multi-client) | MCP dává smysl |
| **Nízká potřeba MCP** | Nepouzívat (prímý príkaz stací) | Zatím nepouzívat |

### 6.3 Rozhodovací flowchart

```
Potrebuju provést operaci?
├─ Jednorázová? → CLI / rucne
├─ >3×?
│  ├─ Cistě lokální, bez doménového kontextu? → Python skript
│  └─ Potrebuji to zpřístupnit LLM / více klientům?
│     ├─ Read-only a bezpečnostne citlivé? → MCP tool (povolené cesty, audit)
│     ├─ Vyžaduje doménové know-how? → MCP tool (tool description = dokumentace)
│     └─ Write operace? → MCP tool (jen se zárukou bezpecnosti)
└─ >50×? → Zvaž samostatný balícek / pip modul
```

### 6.4 Template pro nový tool

| Otázka | Váha |
|--------|------|
| Frekvence pouzití (>5×/mesíc?) | tool pokud ano |
| Počet klientů (>1?) | tool pokud ano |
| Doménová znalost (střední+?) | tool pokud ano |
| Bezpecnostní riziko (střední+?) | tool (s audit) |
| Write operace? | tool (s validací) |

---

## 7. Dědičnost — checklist pro nový MCP projekt

Při zakládání nového MCP repozitáře:

1. **Console script** (P11+P12) — `[project.scripts]` v pyproject.toml + `.bat` wrapper
2. **Path quoting** (P14) — pathlib.Path pro vsechny cesty
3. **Windows encoding** (P18+P23) — PYTHONIOENCODING + PYTHONUTF8 + -X utf8
4. **Workspace context** (P17) — workspace info tool pri startu
5. **Audit logging** (P5) — @auditable na vsech tool funcích
6. **Test pyramida** (P27) — unit > integration > E2E + smoke test
7. **ETL health check** (P20) — session-start ETL pro scrapers
8. **L2 Resources** (P21) — URI-adresovatelná data
9. **Async subprocess** (P26) — asyncio.create_subprocess_exec, ne subprocess.run
10. **Python version audit** (P24) — requires-python + startup check
11. **FastMCP sync main** (P29) — `def main(): app.run()`. Nikdy `async def` + `asyncio.run()`.
12. **Editable install path** (P29) — po `pip install -e .` se `src` layoutem over `.pth` ma project root + `src/`
13. **LLM response format fallback** (P30) — `msg.get("content") or msg.get("reasoning")` pro kazdého providera
14. **LLM max_tokens** (P31) — `max_tokens >= 4000` pro coaching pipeline
15. **Cascade log exposure** (P32) — per-provider status, tokens, cost v kazdém reportu
16. **API key management** (P39) — `.env` + `auth.json` + `.gitignore` pro vsechny providery
17. **Per-game LLM cache** (P41) — `{game_id}_llm.json` pro inkrementální agregaci
18. **Cascade resilience** (P42) — timeout jednoho providera neblokuje pipeline
19. **Contract testing** (P44) — P44 — Consumer-Driven Contract mezi Stockfish → prompt builder → LLM
20. **API key health check** (P45) — `verify_api_keys()` při startupu, detekuje 401/402/429

---

## 8. Statistiky (merged)

| Metrika | Hodnota |
|---------|---------|
| Celkem bugů (GT-001 az GT-059) | 59 |
| Fixed | 50 (85%) |
| Workaround/Mitigated | 5 (8%) |
| Documented | 4 (7%) |
| Z toho environment/CI issues | 11 |
| Z toho application logic issues | 48 |
| Z toho cross-repo (platí pro vsechny) | 13 |
| Z toho zachyceno contract testy (GT-059) | 1 |

---

*MCP_GROUND_TRUTH_postmortem_agregovany_v1.md — 2026-07-20 — v2 — Rozsírení o LLM reasoning pipeline: GT-045 az GT-060, pravidla P30-P45, SNR framework, provider governance, per-game LLM cache, pipeline mode switch, contract testy. Pridany lichess-analyzer LLM sekce (3.5).*
