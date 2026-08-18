# MCP GROUND TRUTH — Agregovaná pitevní kniha

**Datum:** 2026-08-06 | **Verze:** 11
**Účel:** Jediný zdroj pravdivých ponaučení z vývoje všech MCP serverů v portfoliu. Nahrazuje: linkedin_mcp_pitevni_kniha_v1.md, mcp_jobs_pitevni_kniha_v1.md, sdilena_pitevni_kniha_mcp.md, MCP_komplexni_analyza_a_strategie_v1.md (pouze postmortem části), pitevni_kniha_mcp_v1.md (cnc-tools).
**Rozsah:** linkedin-mcp-custom, MCP-Jobs, mcp-local-server (cnc-tools), lichess-analyzer-mcp
**Určení:** Výukový materiál pro deva, instrukce pro LLM, ground truth pro rozhodování
**Skill:** Pred editaci loadni `skill({name: "kb-workflow"})` → sekce Postmortem Workflow obsahuje pravidla pro konzistentni zapis GT/P a prevenci konfabulace.

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

Číslování GT-001 až GT-078. V závorce původní ID z originálního artefaktu.

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


#### GT-061 (lichess-019) — mistakes list always empty (Cross-LLM Audit N1)
**Server:** lichess-analyzer | **Status:** Fixed | **Typ:** Application logic — Classification branch bug

**Nalezeno:** Cross-LLM audit v2 (code path verification, 2026-07-24). Predchozi audity (v1 twin, rucni code review) neodhalily.

**Symptom:** `GameAnalysis.mistakes` je vzdy prazdny. Vsechny tahy s cp loss 150-299 cp konci v `blunders` misto `mistakes`.

**Root cause:** `game_analyzer.py:161-162`:
```python
if classification in ("blunder", "mistake"):
    analysis.blunders.append(...)
```
Chybi separatni `elif classification == "mistake"` branch. Obe kategorie sdieleji append target.

**Fix:** Rozdeleni na separatni vetve:
```python
if classification == "blunder":
    analysis.blunders.append(...)
elif classification == "mistake":
    analysis.mistakes.append(...)
```

**Dopad:** 100% tahu s cp loss 150-299 cp je chybne oznaceno jako blunder. Ovlivnuje: coaching report, diagnostician analyzu, pattern detection. Latentni od v1.0.

**Detection gap:** Contract testy (P44) kontroluji klicove struktury, ale ne overuji, ze kazda kategorie ma vlastni cil. Unit testy nepokryvaji vetveni classification logiky.

**Pravidlo:** P46 — Classification branches must be mutually exclusive. Kazda kategorie v if/elif chainu musi mit vlastni append target. Unit test musi overit, ze zadne dve kategorie nesdileji stejny cil.

**Provenance:** Overeno source-read (game_analyzer.py:161-162, v2 audit code path verification 2026-07-24). Popis presne odpovida kodu. Zadna konfabulace.

---

#### GT-062 (lichess-020) — Cross-LLM audit workflow validation (Methodology)
**Server:** lichess-analyzer | **Status:** Documented | **Typ:** Methodology — Development process

**Poznatek:** Prvni cross-LLM audit lichess-analyzer-mcp probehl 2026-07-24 ve dvou fazich:
1. **v1 (DIGITAL_TWIN, de novo scan):** ~13h brain dump knowledge (subjektivni odhad autora, nikoliv merena velicina) + architecture analysis → 8 nalezu (4 structural, 4 pattern-based)
2. **v2 (Code review, citelny kod):** Code path verification → 7 nalezu (5 implementation, 2 security confirmed)

**Vysledky:**
| Metrika | Hodnota |
|---------|---------|
| Celkem unikatnich nalezu | 12 |
| v1→v2 confirm rate | 71 % (5/7 code review nalezu potvrzeno z v1) |
| v2-only nalezy (unikli twinovi) | 2 (N1: mistakes bug, N4: Pattern G semantic) |
| Efektivita | 9.6 nalezu/hod (15 / 1.55h) |
| Twin time-to-audit | ~13h (odhad autora) → 5 min audit script |

**Zaver:** Twin scan (de novo bez kodu) spolehlive zachyti architekturni a structuralni problemy, ale unikaji mu implementacni detaily (chybejici elif, semantic mismatches). Code review (v2) je nezbytny pro nizkourovnove verifikace. Ani jedna faze sama o sobe nestaci.

**Doporuceni:** Cross-LLM audit gate: v1 (twin, architecture scan) + v2 (code review, implementation scan) pred kazdym major release.

**Pravidlo:** P47 — Cross-LLM audit gate. Pre-release: v1 twin scan (architektura, struktura) + v2 code review (implementace, verifikace). Ani jedna faze nestaci sama.

**Provenance:** Agregace z audit session — casove udaje (1.55h) mereny, "~13h" je subjektivni odhad autora. Metodologie v1+v2 overena externim auditorem (Claude, 2026-07-24).

---

#### GT-063 (lichess-021) — Pattern detection: hardcoded confidence + semantic mismatch (Methodology)
**Server:** lichess-analyzer | **Status:** Documented | **Typ:** Application logic — Pattern confidence & semantics

**Nalezeno:** Cross-LLM audit v1 + v2. F3 (hardcoded confidence) a N4 (Pattern G semantic mismatch — frequency vs rate mixup).

**Symptom:**
1. Confidence vsude hardcoded: 0.6/0.5/0.8/0.7/0.7 v pattern_detector.py, nezavisle na poctu her nebo sile evidence.
2. Pattern G ("Color as modulator", `_detect_g`) detekuje asymetrii blunder rate mezi hrou za bileho a cerneho (trigger pri `ratio > 1.4`). Pole `frequency = int(max(white_blunder_rate, black_blunder_rate))` vsak micha semantiku — u ostatnich patternu `frequency` = pocet postizenych her, u G = zaokrouhlena blunder rate. `detect_all()` pak filtruje `match.frequency >= pdef.min_occurrences`, coz muze zpusobit, ze pattern projde/neprojde filtrem z jineho duvodu, nez autor zamyslel.

**Root cause:** Pattern detection implementovan jako boolean rules (match/nomatch), bez skore podle poctu her nebo sily evidence. Pattern G navic pouziva `frequency` v odlisne semantice nez ostatni detektory.

**Reseni:** Pattern confidence = f(N, evidence_strength). Pravidelnost zvysuje confidence, ale ne linearne. Minimalni N = 5 pro confidence > 0.5. Pattern G: `frequency = len(game_ids)` pro konzistenci semantiky s ostatnimi patterny.

**Pravidlo:** P48 — Pattern confidence weighted by sample size. `confidence = min(0.95, base * (1 - 1/(N+1))) * evidence_factor`. Minimal sample N >= 5.

**Provenance:** Tento zaznam obsahoval v puvodni v3 konfabulaci — Pattern G byl popsan jako "closed center positional match" (tahy `d4 d5`, `e6`, `c6`), coz neodpovida skutecnemu kodu. Opraveno v v4 na zaklade externiho cross-auditu (Claude, 2026-07-24). Reference: `04_KNOWLEDGE_BASE/01_MCP/MCP_GT_ANALYZA_kvalita_originalita_semantika.md`, nalezy B1.

---

#### GT-064 (lichess-022) — Diagnostician: middlegame absolute count vs per-move rate (Methodology)
**Server:** lichess-analyzer | **Status:** Documented | **Typ:** Application logic — Normalization

**Nalezeno:** Cross-LLM audit v1 (N3).

**Symptom:** `diagnostician.py:52` pouziva absolutni pocet blunderu v middlegame misto blunders-per-move rate. Hry s vice tahy maji prirozene vice chyb = bias vuci dlouhym hram.

**Root cause:** `blunder_count > threshold` bez normalizace poctem provedenych tahu v dane fazi.

**Reseni:** Normalizace: `blunder_rate = blunder_count / moves_in_phase`. Threshold aplikovat na rate, ne na absolutni pocet.

**Provenance:** Nalez N3 z cross-LLM audit v1 (twin scan). Overitelne v diagnostician.py:52. Popis je precizni — zadna konfabulace.

---

#### GT-065 (lichess-023) — Path traversal via unsanitized game_id / username (Security)
**Server:** lichess-analyzer | **Status:** Mitigated | **Typ:** Security — Path traversal

**Nalezeno:** Cross-LLM audit v1 (F2), potvrzeno v2 code review.

**Symptom:** `game_id` a `username` pouzity primo v cestach bez sanitizace:
```python
# game_analyzer.py:14-15
def _cache_path(game_id, depth, color="white"):
    return os.path.join(CACHE_DIR, f"{game_id}_{color}_d{depth}.json")

# lichess_client.py:47-48
def _pgn_cache_path(game_id):
    return os.path.join(PGN_CACHE_DIR, f"{game_id}.pgn")

# lichess_client.py:74-77
def _user_games_cache_path(username):
    return os.path.join(..., f"{username}_games.json")
```
Zadna z funkci nesanitizuje vstup pred `os.path.join()`. `game_id = "../../sensitive"` by mohl zapisovat/ctist mimo cache adresar.

**Root cause:** Chybi sanitizace user-supplied identifieru pred filesystem use. Path traversal guard neni implementovan.

**Reseni:** `re.sub(r'[^a-zA-Z0-9_-]', '_', game_id)` nebo `re.sub(r'[^a-zA-Z0-9_.-]', '_', username)` na vsech vstupech pred konstrukci cesty.

**Pravidlo:** P49 — Sanitize user-supplied identifiers before filesystem use. `re.sub(r'[^a-zA-Z0-9_-]', '_', value)` na vsech vstupech pred konstrukci File Path. Zaden user input nesmi byt primo v path segmentu.
**Provenance:** Nalez F2 — jadro (sanitizace chybi) spravne, ale puvodni v3 obsahovala fabrikovane code snippety (`LOGS_DIR` neexistuje). Opraveno v v4 na skutecna API (lichess_client.py, game_analyzer.py). Overeno source-read.

---

#### GT-066 (lichess-024): Pipeline consistency — max_games hidden clamp
**Server:** lichess-analyzer | **Status:** Fixed | **Typ:** Application logic — Hidden limit

**Symptom:** `fetch_games(max_games=999)` nikdy nevrátí více než 50 her. Interní clamp `min(50, max_games)` ignoruje explicitní request. Stejný clamp v `match_patterns` a `diagnose_player` — default 50 aplikovaný i při požadavku na vyšší počet.

**Root cause:** Trojice clampů:
1. `fetch_games.py` — `max(1, min(pages, 50))` v dokumentaci i kódu, ale popis sliboval 999
2. `match_patterns.py` — `max_games=50` v argumentu + `clamp(1, 50)` bez signalizace
3. `diagnose_player.py` — stejný clamp

Uživatel zadá `max_games=100` → tichý ořez na 50. Žádný warning. Cache zůstane nekonzistentní — načteno 50, analyzováno 50, ale index hlásí 63 her.

**Fix:**
1. `fetch_games.py`: clamp změněn na `clamp(1, 999)`, dokumentace konzistentní
2. `match_patterns.py` + `diagnose_player.py`: clamp odstraněn, ponecháno `max_games=999` v parametru
3. Kontrola: `get_pending_analysis()` vrací rozdíl mezi game indexem a analyzovanými hrami

**Pravidlo:** P50 — Parametr clamp musí být explicitně signalizován uživateli. Pokud clamp snižuje hodnotu, logovat warning: `f"[clamp] max_games={max_games} clamped to {clamped}"`.

**Provenance:** Overeno source-read fetch_games.py, match_patterns.py, diagnose_player.py (2026-07-26).

---

#### GT-067 (lichess-025): Pending analysis — missing warning mechanism
**Server:** lichess-analyzer | **Status:** Fixed | **Typ:** Application logic — Cache consistency gap

**Symptom:** Uživatel zavolá `diagnose_player` nebo `match_patterns` na N hrách, ale M není dosud analyzováno Stockfishem. Tool vrátí nekompletní výsledky bez jakéhokoliv upozornění. Pipeline je konzistentní podle cache → bug-free, ale uživatel má falešný pocit kompletnosti.

**Root cause:** Chybí mechanismus (a) detekce pending her a (b) signalizace uživateli. Všechny tooly analyzují jen tolik her, kolik je v cache, bez kontroly rozdílu proti indexu.

**Fix:**
1. `get_pending_analysis()` v `lichess_client.py` — porovná index vs. cache, vrátí počet + seznam pending game ID
2. Warning v `match_patterns.py` a `diagnose_player.py`: `f"[warning] {n_pending} her není analyzováno. Použij lichess_analyze_pending pro doanalýzu."`
3. `analyze_pending.py` — nový MCP tool pro batch doanalýzu pending her (depth d, max_games, auto-detect)

**Pravidlo:** P51 — Každý tool závislý na per-game cache musí před zpracováním zkontrolovat pending count a varovat uživatele. Struktura: cache-first → pending warning → processing → výsledek.

**Provenance:** Overeno source-read (2026-07-26).

---

#### GT-068 (lichess-026): Berserk 0.14 — no `before` pagination parameter
**Server:** lichess-analyzer | **Status:** Documented | **Typ:** Environment — Library limitation

**Symptom:** První pokus o paginaci her použil `client.games.export_by_player(..., before=last_created_at)` → `TypeError: unexpected keyword argument 'before'`. Berserk vrací jen nejnovějších ~30-60 her z endpointu `GET /api/games/user/{username}` (server-side limit).

**Root cause:** Berserk 0.14 nepodporuje `before` parametr v `export_by_player()`. Tento parametr byl přidán až v berserk 0.15+. API endpoint Lichess podporuje `before`, ale berserk knihovna ho neexponuje.

**Dopad:** Nelze stáhnout historické hry mimo "recent" okno (cca 30-60 her). Paginace je omezena na to, co server vrátí v prvním response. Omezení není kritické pro coaching (63 her = celý recent dataset), ale znemožňuje analýzu deep history (>60 her).

**Fix:** Reverzní — kód vrácen do původního stavu bez `before`. Paginace řešena interně berserkem. Feature request: upgrade na berserk 0.15+ až bude k dispozici.

**Pravidlo:** P52 — Před použitím parametru knihovny ověř jeho dostupnost v aktuální verzi. `pip show berserk | grep Version`. API dokumentace Lichess a berserk dokumentace mohou být desynchronizované.

**Provenance:** Overeno runtime error (2026-07-26), verifikováno `pip show berserk = 0.14.0`.

---

#### GT-069 (lichess-027): opencode MCP tool cache — tool registered but invisible
**Server:** lichess-analyzer | **Status:** Workaround | **Typ:** Infrastructure — opencode host caching

**Symptom:** `lichess_analyze_pending` tool je registrován v Python kódu (`@app.tool()` dekorátor, FastMCP init), ale v opencode client tool listu není vidět. Python import funguje (`from .tools.analyze_pending import ...`), FastMCP registruje, ale host neaktualizuje tool list.

**Root cause:** opencode host udržuje cache tool listu při startu. Nový tool přidaný za běhu (restart serveru) se neprojeví, dokud host znovu nenačte tool list z MCP `initialize` handshake. opencode nerevaliduje tool list při reconnectu nebo session refresh — používá cached verzi z prvního handshaku.

**Dopad:** Tool existuje v Python procesu (`app._tool_manager.list_tools()`), je volatelný přes přímé API, ale není dostupný přes opencode tool selection UI. Uživatel ho nemůže vybrat ani zavolat.

**Práce:** (1) Restartovat opencode celý (ne jen MCP server). (2) Nebo volat Python přímo: `.venv/Scripts/python -c "from src.server import app; app.call_tool('analyze_pending', {...})"`.

**Fix (budoucí):** opencode by měl podporovat hot-reload tool listu nebo periodickou revalidaci. Alternativně: skill `mcp-server-update` pro vynucení refresh.

**Pravidlo:** P53 — MCP tool registrace není dostatečná pro viditelnost v host clientu. Po přidání nového toolu: (1) restart MCP server, (2) restart opencode session, (3) ověř v `list_tools` že tool je vidět. Tool list je snapshot při initialize handshaku.

**Provenance:** Overeno prakticky — `list_tools` neobsahuje analyze_pending (2026-07-26).

---

#### GT-070 (lichess-028): Pattern G (Color as modulator) — new pattern detection
**Server:** lichess-analyzer | **Status:** Documented | **Typ:** Application logic — New pattern

**Symptom:** Při analýze 63 her (44W/17L/2D) detekován nový pattern: hráč hraje výrazně hůře jako White (1.47× více bludrů) než jako Black. Pattern má confidence 49% (N=63, base 0.4 * evidence_factor 1.22).

**Root cause:** Pattern G v `pattern_detector.py` porovnává blunder rate (blunders/game) mezi White a Black games. Trigger při `ratio > 1.4`. Dříve nebyl detekován kvůli:
1. Nízkému N v předchozích analýzách (28 her, nedostatečný sample)
2. Hardcoded confidence (0.5) bez vztahu k sample size — pred GT-063 fixem

**Význam:** Color as modulator je vzácný pattern — většina hráčů má symetrickou chybovost. Jeho detekce signalizuje specifický psychologický nebo opening-preference problém. Vyžaduje separátní tréninkový přístup (opening repertoire review, time management jako White).

**Fix:** Pattern G zachován v pattern setu. Confidence vážena dle P48 (f(N, evidence_strength)). `frequency` sémantika sjednocena s ostatními patterny (počet her, ne blunder rate).

**Pravidlo:** P54 — Pattern discovery je vedlejší produkt pipeline. Nový pattern musí být validován: (a) N >= 30 pro statistickou signifikanci, (b) ratio >= 1.4 pro praktickou relevanti, (c) potvrzen v 2+ nezávislých analýzách.

**Provenance:** Detekován `match_patterns(max_games=63)` na datech 2026-07-26. Overeno vizuální kontrolou blunder distribuce.

---

### 3.6 lichess-analyzer-mcp — DBCL Phase 2 & RUN_004 (2026-07-27)

#### GT-071 (lichess-029): engine_lines silent fail — AssertionError v board.san(m) pro Stockfish PV illegal moves
**Server:** lichess-analyzer | **Status:** Fixed | **Typ:** Application logic — Silent data corruption

**Symptom:** 30/101 BFS (30 %) má 0 engine_lines. Postihuje i ground truth hry (qmodxzNF ply 60, xUlQasD0 ply 19 a 91). `engine_client.analyze_position(multipv=3)` vrací `[]`.

**Root cause:** Dvojitý silent exception:
1. `engine_client.py:86`: `board.san(m)` pro Stockfish PV multi-tahovou sekvenci — `AssertionError: san() and lan() expect move to be legal or null, but got g5e6`. Stockfish PV obsahuje sekvenční tahy (např. `f3g5, g6e5, g5e6`), ale `board.san(m)` validuje všechny tahy proti ROOT pozici. Po prvním tahu `f3g5` (Nf3-g5) se board změní, ale třetí tah `g5e6` kontroluje proti rootu kde g5 je prázdné.
2. `game_analyzer.py:329-333`: `try/except Exception: pass` — error kompletně skryt, žádný warning v logu.
3. AssertionError z `analyze_position` propaguje přes engine lock a korumpuje stav engine pro následující volání.

**Demonstrace:**
```
PV:       f3g5(Nf3-g5),  g6e5(Nxg6xe5),  g5e6(Ng5xe6)
Root:     f3->g5 OK       g6->e5 OK       g5->e6 FAILS (g5 empty!)
Fix:      board.copy() -> f3g5 push -> g6e5 push -> g5e6 OK
```

**Fix (trojí):**
1. `engine_client.py:86-93`: `[board.san(m) for m in line["pv"][:5]]` → sequential `board.copy()` + try/except
2. `game_analyzer.py:330-331`: silent `pass` → `_logger.warning(...)` 
3. `engine_client.py:81`: `engine.analysis(board)` → `engine.analysis(board, chess.engine.Limit(depth=depth))`

**Verifikace:** 5/5 dříve padajících FENů nyní vrací 3/3 PV lines. Celá hra 4j0sNlrT: 1 blunder, 0 s zero engine_lines (dříve 30 % fail).

**Pravidlo:** P55 — Každý `except Exception: pass` je bug unless proven otherwise. Silent excepty musí být zalogovány. 
**Pravidlo:** P56 — Stockfish PV multi-tahové sekvence musí být konvertovány do SAN sekvenčně na kopii boardu. `board.san(m)` validuje proti aktuální pozici, ne proti rootu.

**Provenance:** Overeno source-read (engine_client.py, game_analyzer.py) + runtime debug script (debug_root_cause.py). AssertionError reprodukován izolovaně na FEN `r1b4k/1p4pp/np1Nr1n1/4P3/8/5N1P/P1P1B3/1R2K2R w K - 1 25` (2026-07-27).

---

#### GT-072 (lichess-030): K0 variance — depth=12 vs depth=14 cp_loss rozdíl ~22%
**Server:** lichess-analyzer | **Status:** Documented | **Typ:** Methodology — Measurement noise

**Symptom:** kNAMNYUF ply 63 cp_loss: 607 (d12) vs 773 (d14) — rozdíl 171cp = 22 %. ACPL čísla z různých depth runů nejsou přímo srovnatelná.

**Root cause:** Depth impactuje eval precision. Depth=12 je ~3× rychlejší ale méně přesný než depth=14. K0 (měřicí přístroj) variance není kvantifikována ani reportována.

**Dopad:** RUN_003 (ACPL=39.4) a RUN_004 (ACPL=51.4) nejsou přímo srovnatelné — část rozdílu může být K0 noise. INC ground truth eval_before/eval_after hodnoty jsou depth-dependentní.

**Fix (navrh):**
1. Každý run reportuje K0 metriky: depth, engine version, Threads, Hash, nps benchmark
2. INC-A/B/C re-fetch na depth=14 pro ground truth cache
3. Logovat depth mismatch při cache load

**Pravidlo:** P57 — K0 (orákulum) je samostatný noise channel. Každý run reportuje: depth, engine_version, Threads, Hash, nps_benchmark. ACPL z různých depth nejsou srovnatelné bez K0 korekce.

**Provenance:** RUN_004 data — kNAMNYUF ply 63 porovnání d12 vs d14. Potvrzeno CPM dokumentem §3 (K0 channel).

---

#### GT-073 (lichess-031): engine.analysis() bez depth limit — depth drift
**Server:** lichess-analyzer | **Status:** Fixed | **Typ:** Application logic — Missing parameter

**Symptom:** `engine.analysis(board)` bez `Limit(depth=depth)` — Stockfish mohl sáhnout do libovolné hloubky na nestabilních pozicích. Zvyšovalo timeout risk a plýtvalo compute.

**Root cause:** Kopírovací chyba z dřívějšího API usage. `engine.analysis()` akceptuje i volání bez Limit parametru.

**Fix:** `engine.analysis(board, chess.engine.Limit(depth=depth))`.

**Provenance:** Source-read engine_client.py:81 (2026-07-27). Fix aplikován souběžně s GT-071.

---

#### GT-074 (lichess-032): Cache invalidation — stale BFS after code fix
**Server:** lichess-analyzer | **Status:** Workaround | **Typ:** Infrastructure — Cache governance

**Symptom:** Po opravě kódu v `analyze_position` zůstávají cache soubory (`data/game_cache/`) s 0 engine_lines. `use_cache=True` vrací stale BFS. Uživatel musí cache explicitně smazat.

**Root cause:** Cache je perzistentní JSON s jednou úrovní (game_id + depth). Není zde `detector_version` nebo `code_version` klíč, který by umožnil detekovat, že cache byla vygenerována starší verzí kódu.

**Workaround:** Manuální `Remove-Item data/game_cache/*.json` před re-runem po code change.

**Fix (navrh):** Při cache load porovnat `detector_version` z cache s aktuální konstantou. Při mismatchi → re-analyze místo cache read.

**Pravidlo:** P58 — Cache klíč musí obsahovat verzi kódu (`detector_version`). Při cache load: version mismatch → log warning → re-analyze. Nikdy nepoužívat stale cache po code change.

**Provenance:** Praktické ověření — po fixu GT-071 re-run s `use_cache=True` vrací stará data. Cache clear + re-run = správná data (2026-07-27).

---

#### GT-075 (lichess-033): Stockfish PV multi-move SAN conversion — domain knowledge gap
**Server:** lichess-analyzer | **Status:** Fixed | **Typ:** Domain knowledge — Assumption error

**Symptom:** Předpokládalo se, že Stockfish PV linie obsahují jen single-move evaluations. Ve skutečnosti Stockfish posílá multi-move sekvence v multi-PV módu.

**Blind spot:** PV linie nejsou paralelní alternativy — jsou to sekvenční variace. Každý PV tah musí být aplikován na kopii boardu postupně, ne validován proti root pozici.

**Fix:** Sekvenční board.copy() + try/except (GT-071 fix 1).

**Pravidlo:** P59 — Stockfish PV v multi-PV módu jsou sekvenční variace, ne paralelní alternativy. Každý PV tah aplikovat na kopii boardu. Nikdy nevalidovat N-tý PV tah proti root pozici.

**Provenance:** Runtime debug — Stockfish output `pv: f3g5, g6e5, g5e6` validován proti rootu místo sekvenčně (2026-07-27).

---

#### GT-076 (lichess-034): Engine lock error propagation — single failure corrupts subsequent
**Server:** lichess-analyzer | **Status:** Mitigated | **Typ:** Architecture — Lock coupling

**Symptom:** AssertionError v jednom `analyze_position` volání korumpuje engine lock, což způsobí selhání všech následujících analýz v daném game runu.

**Root cause:** `_acquire_analysis_lock` / `_release` vytváří coupling mezi nezávislými analysis call. `finally: _analysis_lock.release()` v `analyze_position` se provede i po AssertionError, ale engine může zůstat v nekonzistentním stavu.

**Mitigation:** GT-071 fix eliminuje AssertionError v normalním provozu. Pro zombie recovery: engine restart při timeout locku (již implementováno v `_acquire_analysis_lock`: 120s timeout → restart).

**Pravidlo:** P60 — Engine lock vytváří coupling mezi analysis call. AssertionError/Exception uvnitř lock bloku může korumpovat stav engine pro následující volání. Mitigace: (a) žádné AssertionError uvnitř locku, (b) engine restart při timeout locku, (c) isolation per-call.

**Provenance:** Analyzováno při debug GT-071 — AssertionError propaguje přes lock blok (2026-07-27).

---

#### GT-077 (lichess-035): Chybí per-game log truncated BFS
**Server:** lichess-analyzer | **Status:** Pending | **Typ:** Application logic — Missing logging

**Symptom:** BFS s méně než multipv_target engine_lines procházejí pipeline bez jakéhokoliv upozornění. Nelze identifikovat, které pozice měly částečný výpadek engine_lines.

**Root cause:** Engine_lines jsou volitelné pole — 0 nebo 1-2 linie nejsou signalizovány jako anomálie.

**Fix (navrh):** Přidat `truncated` flag do BlunderFactSheet (`len(engine_lines) < multipv_target`). Logovat warning per BFS při truncated engine_lines.

**Pravidlo:** P61 — Engine lines count pod multipv_target musí být signalizován. Flag `truncated` a `logger.warning()` per BFS.

**Provenance:** RUN_004 data — 71/101 BFS s 3 engine_lines, 30/101 s 0 (GT-071 před fixem). Po fixu: všechny BFS mají 3/3, ale chybí trackování částečných výpadků (2026-07-27).

---

#### GT-078 (lichess-036): ruff --fix smazal side-effect tool imports — F401 destruktivní autofix
**Server:** lichess-analyzer | **Status:** Fixed | **Typ:** Tooling — Destructive autofix

**Symptom:** `ruff check --fix` na `src/lichess_analyzer_mcp/server.py` smazal 18 `from lichess_analyzer_mcp.tools import X` importů (diff: -18/+2). Tool registrace přes `@app.tool()` dekorátor se zrušila — MCP server by startoval bez toolů. Pytest prošel (93/93), protože testy `server.py` neimportují. Detekováno až díky `git diff --stat` po lint verifikaci.

**Root cause:** `server.py` používá záměrný pattern side-effect imports — import modulu kvůli registraci toolu při importu, ne kvůli použití jména. Ruff pravidlo F401 (unused import) detekuje nepoužité jméno a `--fix` ho **smaže**. Behaviorálně správné pro 99 % kódu, destruktivní pro registrační pattern. Baseline: 46 errorů na 3 souborech (z toho 18x F401), repo nikdy nespouštělo `--fix` na `server.py`.

**Fix:**
1. Všech 18 importů + nový `persist_report` obnoveno s `# noqa: F401` per line (explicitní deklarace side-effect záměru)
2. Verifikace: registrační smoke check (`app._tool_manager._tools` = 18 toolů), pytest 93/93
3. Commit `c92940f` obsahuje opravu včetně `# noqa: F401` od počátku u nového toolu

**Pravidlo:** P62 — Ruff `--fix` je destruktivní operace. Side-effect importy (registrace přes `@app.tool()` dekorátor) MUSÍ mít `# noqa: F401` per line. Po každém `ruff --fix`: povinně číst `git diff` + spustit registrační smoke check — pytest destruktivní smazání registrace nezachytí.

**Provenance:** source-read — `git diff` po `ruff check --fix` na server.py (diff -18/+2), obnova importů s `# noqa: F401`, smoke check 18 toolů, commit c92940f (2026-08-01).

---

#### GT-079 (lichess-037): Data-correctness batch 1+2 — getattr garbage, hardcoded perspektiva, KB cesta, cache kolize barev, timeout kill, tichá degradace ACPL
**Server:** lichess-analyzer | **Status:** Fixed | **Typ:** Data integrity — LLM input correctness (6 merged bugů)

**Symptom:** Dvě nezávislé vlny bugů v coaching pipeline (fix batche 2026-08-02):
1. **B100:** `opening_report` četl `getattr(a, "opening_name", "Unknown")` — atribut na `GameAnalysis` neexistuje (správně `a.game.opening`) → Python tiše vrátil default → **100 % garbage** do `white_openings`/`worst_openings`/`best_openings` → LLM report postavený na garbage bez jakékoli detekce. Stejně: `player_color` (vždy "white"), `acpl` (vždy 0), `result` (vždy "*").
2. **B98:** `opponent_pool` hardcodoval `opponent_color="black"`, `author=_load_cached_analysis(gid, depth, "white")` → u her, kde autor hrál černým, analyzoval **autorovy vlastní tahy jako "oponentovy"**; `n1_count` přes neexistující `player_color` = vždy 0; `n1_acpl`/`n2_acpl`/`blunder_rate` = hardcoded `"?"` placeholdery v promptu.
3. **B121:** `kb/writer.py` `KB_ROOT = 3× ".."` → **repo root** (`lichess-analyzer-mcp/B2B-Knowledge-Base`, adresář neexistuje) → první `target="kb"` by vytvořil adresář uvnitř repa (zanesení repa). B119: filenames bez timestampu → same-day diagnóza tiše přepsala předchozí.
4. **B31:** LLM cache klíč `{game_id}_llm.json` bez barvy → dual-cache (white+black) sdílí soubor; `content_tag` obsahuje color → mismatch → regenerace + **last-writer-wins přepíše opačnou perspektivu**.
5. **B5:** timeout v `engine_client._run_engine_call` volal `_kill_engine()` (sdružený `_engine`), ale `evaluate_move` používá **lokální** engine → timeout zabíjel sdružený engine → kolaterální ztráta konkurující analýzy + zbytečný restart.
6. **B16:** `except Exception: pass` + `cp_loss = 0` při selhání `evaluate_move` → chybný tah klasifikován "best" → **ACPL systematicky optimistický bez markeru**. (B113: `chess.Board(m.fen)` na starších cache s `fen=""` → ValueError → zhroucení celého `detect_all`.)

**Root cause (společný vzor):** LLM vstupy (prompt) čtené přes neexistující atributy/getattr s defaultem — Python **neprovede žádnou signalizaci**, vrátí default. Data do LLM promptu bez markeru kvality = falešná autorita.

**Fix:**
1. `_game_opening_stats()` — reálná pole modelu (`a.game.opening/color/result`, `a.total_acpl`) + win_rate color-aware (`side` param).
2. `_resolve_colors(white_name, black_name, username)` + `username` param → barvy z PGN headerů, obě strany přes `analyze_pgn`, n1/n2 + ACPL/blunder_rate z reálných polí; fallback autor=bílý s warning logem.
3. `KB_ROOT` 4× `..` (do `_github/`) + `_KB_EXISTS` import-time check + `_ts()` s `_HHMMSS`.
4. Klíč `{game_id}_{color}_llm.json`; color derivován ze stockfish cache v `get_all_game_summaries`; 0 legacy souborů → žádná migrace.
5. `_run_engine_call(fn, timeout_s, engine=None)` — timeout kvitne **referenci, která volala**; `evaluate_move` předává lokální engine; dvojí `quit()` ošetřen try/except.
6. `GameAnalysis.evaluation_errors` čítač (error dict i výjimka → +1, ne tichý cp_loss=0) + prompt marker `Eval errors: N (ACPL may be optimistic)`. B113: guard `and m.fen` (konzistentní s `_detect_n`).

**Pravidla:** P63 — P68 (viz sekce 4). P41 aktualizováno (color v cache klíči).

**Provenance:** source-read — CODE_REVIEW_2026-08-01.md, session plány `00_STRATEGIE/session_plan_fix_batch1/2_2026-08-02.md`, commity fc5fc69 + 552bc9d, testy 93→109→121 (2026-08-02).

---

#### GT-080 (workspace-wide): Ne-ASCII názvy souborů — mojibake v git objektech + encoding dluh napříč 6 repy
**Server:** workspace (cross-repo) | **Status:** Fixed | **Typ:** Encoding — filename nomenklatura (konvence ASCII-NOM)

**Symptom:** GitHub GUI zobrazoval `02_ANAL�ZY` v remote tree i po pushi; dev hlásil podezření na strukturální inkonsistenci remote vs local. Diagnostika odhalila: **žádná strukturální inkonsistence** (remote tree = lokální tree, stejný SHA, 61=61 souborů), ale **mojibake bytes v git objektech**: git index obsahoval `E2 94 9C C5 81` (="┌Ł") místo UTF-8 `C3 9D` (Ý). Filesystem měl správné U+00DD — PowerShell cp1250 vrstva to maskovala. Celkem **20 trackovaných ne-ASCII názvů v 6 repech**: B2B-Knowledge-Base (14: 11× `02_ANALÝZY/`, 2× `High‑SNR` s U+2011 non-breaking hyphen, 1× `Od Kompresního Realismu k Biologické Neuro-Architektuře.md`), dxf_integrace (1), GCP (1), kazuistiky_llm_sprint (2), lichess-analyzer-mcp (1), vcf_integrace (1). Doplňkově `00_STRATEGIE/` a `03_PROVOZ/` chybí v GUI = gitignored (`.gitignore:47,49`, design, ne chyba).

**Root cause:** Encoding dluh — ne-ASCII názvy (diakritika, mezery, U+2011 non-breaking hyphen) zapsané v minulosti. Git ukládá path jako raw bytes v cp1250 (OS filesystem) → na remote UTF-8/GitHub zobrazeno jako mojibake. U+2011 je zvlášť zákeřný — vizuálně identický s ASCII `-`, ale jiné codepoint → rozbíjí copy-paste, grep a RAG lookup. Konvence "obsah UTF-8, názvy ASCII" eliminuje zdroj na úrovni vzniku (dev teze: cyklický encoding dluh — každá ne-ASCII cesta je budoucí bug).

**Fix:**
1. **Konvence ASCII-NOM (schválena devem, GO):** názvy souborů/adresářů jen `[A-Za-z0-9._-]`; obsah zůstává UTF-8 s diakritikou. Odstraňuje zdroj, ne jen symptom.
2. **Transliterace** (bezpečná vůči cp1250): `String.Normalize(FormD)` + odstranění NonSpacingMark, mezera→`_`, U+2011→`-`, ostatní ne-ASCII→`_`, kolaps `__+`→`_`, trim, `_+\.`→`.`.
3. **Rename přes filesystem objekty** (Get-ChildItem, ne hardcode diakritiky) + `git mv` per repo; obsah nedotčen (100% R v diffu).
4. **`.gitignore` fix** v KB: `02_ANALÝZY/01_portfolio_audit/`→`02_ANALYZY/01_portfolio_audit/` (rename rozbil ignore pravidlo); unstage přes `git reset -q HEAD -- <path>`.
5. **Content reference update** (7 souborů v KB): cesty v README/INDEX/AGENTS/architektura/sémantická analýza + odkaz na `Od_Kompresniho_Realismu_k_Biologicke_Neuro-Architekture.md` (brain_geometric_processor_summary:614).
6. **Guard skript** `.scripts/ascii_filenames_check.ps1` — exit 0/1, `git ls-files | ne-ASCII regex` přes všechny repo; v11 verificováno 19/19 OK.
7. **Kontraktní validátor referencí** `.scripts/context_refs_check.py` — exit 0/1, kontroluje, že žádný trackovaný soubor neobsahuje staré cesty/názvy po renames (GLOBAL_FORBIDDEN + REPO_FORBIDDEN rename mapa + F1_ALLOWLIST pro legitimní výskyty jako historická mirror/pipeline data a GT citace). Po v2 prošel přes 1386 trackovaných souborů / 19 rep a odhalil **31 broken referencí** (runtime path stringy v Python kódu, README/index/mapa reference, URL-encoded `%C3%9D` odkazy, `New_rules/` cesta), opraveno a re-validováno na 0 (2026-08-02).

**Pravidla:** P69 (viz sekce 4). P41 (cache klíč) nesouvisí.

**Provenance:** source-read — renames commit KB `533a9c6`, dxf `0bff7b7`, GCP `fdcf1df`, kazuistiky `a613eb2`, lichess `19c735b`, vcf `79591d5`; guard `.scripts/ascii_filenames_check.ps1` exit 0 na 19 repo (2026-08-02). Broken ref fixes: GCP `d9ea2b1`, lichess `9e41386`, linkedin-mcp-custom `210be0b`, mcp-local-server `9ab5820`, dxf `de87a32`, Vcf-compiler `0a8844d`, outpost2026_profile `cce09b3`; kontraktní validátor `.scripts/context_refs_check.py` exit 0 (0 broken refs, 2026-08-02).

---

#### GT-081 (lichess-038): Architektonický původ ruffu — CI gate, ne pre-commit hook; a sémantická eskalace pravidel
**Server:** lichess-analyzer | **Status:** Documented | **Typ:** Tooling — Guardrail adoption architektura (adopce znalostí, ne vibecoding)

**Symptom:** Dev při adopci znalostí (cílem skutečná architektonická adopce, ne vibecoding) položil otázku: *kdy a proč byl ruff do lichess-MCP zaveden?* Git historie dává jednoznačnou odpověď, která mění chápání role ruffu v projektu.

**Zjištění (git source-read):**
1. **Ruff config existoval od prvního commitu** (`4dd503a`, 2026-07-18, Phase 1 checkpoint): `[tool.ruff] line-length=100, target-version="py312"`, bez `select` → aktivní **defaultní sada** (F + E4/E7/E9). Rozhodnutí "rules existují dřív než kód" (from day one), ne zpětný retrofit.
2. **Aktivace enforcementu 2026-07-20** (`1ca173e`): CI krok `uv run ruff check src/ tests/` v `.github/workflows/test.yml` — ruff se stal **CI gate** (běží na push do main + PR). Ne pre-commit hook.
3. **Sémantická eskalace pravidel 2026-07-20** (`98f0546`): `select = ["F","E","W","I","N","UP","S"]` — z defaultu na: pyflakes (chyby), pycodestyle (styl), isort (řazení), pep8-naming (názvy), pyupgrade (zastaralé konstrukty), bandit (bezpečnost, mimo tests přes per-file-ignores). Eskalace: chyby → styl → pojmenování → bezpečnost.
4. **Rozšíření CI 2026-07-25** (`e41ef52`): mypy type-check + pytest --cov — lint se stal součástí širší kontroly.
5. **`.pre-commit-config.yaml` v lichess-MCP NIKDY neexistoval** (git history prázdná, soubor dnes neexistuje). Ruff funguje výhradně jako CI gate, ne lokální hook.

**Root cause (proč toto architektonické schéma):** CI gate chrání **main v síti** (enforcement je centrální, běží na GitHubu, nezávisí na lokálním venv deva). Kontrast s linkedin-mcp-custom, kde ruff je pre-commit hook (lokální kontrola před každým commitem). Dvě instance téhož principu (guardrail), různé enforcement pointy. CI v lichess-MCP používá `--check` (read-only) — nikdy `--fix` v enforcement pointu; separace *kontroly* od *mutace* je přesně to, co GT-078 (P62) porušil ad-hoc auditním `--fix`.

**Fix (architektonická adopce, dev závěr):**
1. Ruff je **structura vrstva** (quality gate), ne ad-hoc nástroj — zaveden od kostry projektu.
2. CI gate (`--check`) ≠ pre-commit hook (lokální mutace). Separace kontroly a mutace je klíčová — `--fix` patří do rukou člověka s `git diff` review, ne do automatizace (P62).
3. Výběr pravidel = **sémantická eskalace** dle auditu: rozšířit `select` jako výstup auditu, ne samovolně.
4. Devops vzor: ruff bez pre-commit hooku NEZNAMENÁ "ruff nepoužíván" — enforcement je v CI.

**Pravidlo:** P62 (kontext rozšířen — viz sekce 4): ruff je CI gate (`--check`) v lichess-MCP; `--fix` je lidská operace s `git diff` review, ne součást automatizace.

**Provenance:** source-read — `git log -S ruff` + `git show` na commity `4dd503a` (first ruff config), `1ca173e` (CI Ruff lint step), `98f0546` (select eskalace), `e41ef52` (mypy/coverage), `git log -- .pre-commit-config.yaml` (prázdná historie) (2026-08-02).

---

#### GT-083 (mcp-jobs-010): 3-fázová pipeline architektura — collect → parallel fetch → filter
**Server:** MCP-Jobs | **Status:** Documented | **Typ:** Architecture — Pipeline design pattern

**Symptom:** Detail fetch byl sekvenční — každý URL se stahoval jeden po druhém. Při 46 matched ads s potřebou detailu = ~30s jen na fetch.

**Root cause:** Původní `run()` měl 2 fáze: (1) scrape all portals, (2) filter query. Detail fetch probíhal uvnitř filter fáze, sekvenčně pro každý ad. Chyběla separace "collect URLs" od "fetch details" od "filter results".

**Fix (3-fázová architektura v `pipeline.py:77-128`):**
1. **Fáze 1 — Collect unikátních URL** (`pipeline.py:81-92`: `urls_needing_detail: set[str]`): Iterace přes všechny query, sběr URL kde `ad.description` je prázdný a `matches_ad()` = true. Set zajišťuje deduplikaci (stejný ad může projít více query).
2. **Fáze 2 — Parallel detail fetch** (`pipeline.py:94-97`: `_fetch_details_parallel()`): `ThreadPoolExecutor(max_workers=4)` s per-portal throttle (0.5s delay). Neúspěch se zapisuje jako `_FAILED` sentinel (GT-085), ne None.
3. **Fáze 3 — Filter nad naplněnou cache** (`pipeline.py:99-126`): Každý ad dostane `ad.description = cached` pokud cache obsahuje úspěch. `_FAILED` se přeskočí (ad zůstane bez detailu, ale filtrování proběhne na základě title/location/salary).

**Výsledek:** 58.5s→36.3s (1.61x speedup), identické výsledky (46 matched ads).

**Pravidlo:** P71 — Scraping pipeline s detail fetch = 3 fáze: (1) collect unikátních URL přes všechny query, (2) parallel fetch s per-portal throttle, (3) filter nad naplněnou cache. Sekvenční detail fetch = bottleneck, který eskaluje lineárně s počtem matched ads.

**Provenance:** source-read — `pipeline.py:77-128` (3-fázová architektura), `pipeline.py:130-200` (`_fetch_details_parallel`), fresh run metriky (2026-08-06).

---

#### GT-085 (mcp-jobs-012): Cache failure sentinel (_FAILED pattern) — odlíšení "nezkoušeno" od "selhalo"
**Server:** MCP-Jobs | **Status:** Documented | **Typ:** Reliability — Cache state management

**Symptom:** Při selhání detail fetchu se do cache zapsalo `None` — stejná hodnota jako "ještě nezkoušeno". Při opětovném spuštění se stejný URL stahoval znovu (a znovu selhal), protože cache nepoznala rozdíl mezi "nezkoušeno" a "selhalo".

**Root cause:** `detail_cache[url] = None` bylo použito pro oba stavy: (1) URL ještě nebylo zpracováno, (2) detail fetch selhal. Cache neměla mechanismus pro rozlišení těchto stavů → opětovné fetch pokusy pro permanentně selhané URL.

**Fix (`pipeline.py:19`, `pipeline.py:140-200`):**
1. **Sentinel:** `_FAILED = object()` — unikátní object, liší se od `None` i od prázdného stringu.
2. **Zápis při selhání:** `detail_cache[url] = detail if detail else _FAILED` (`pipeline.py:181, 196, 200`).
3. **Čtení v filter fázi:** `if cached is not _FAILED and cached:` (`pipeline.py:114`) — `_FAILED` se přeskočí (ad zůstane bez detailu), `None` se také přeskočí (ještě nezkoušeno), pouze platný string se aplikuje.

**Pravidlo:** P71 — Cache pro výsledky s možným selháním MUSÍ rozlišovat 3 stavy: (1) nezkoušeno (`None`/absence klíče), (2) úspěch (hodnota), (3) selhalo (sentinel `_FAILED`). Bez sentinelu = opětovné fetch pokusy pro permanentně selhané URL.

**Provenance:** source-read — `pipeline.py:19` (sentinel definition), `pipeline.py:114` (cache read), `pipeline.py:181,196,200` (cache write), cross-LLM review finding BUG-001 (Claude Sonnet 5, 2026-08-06).

---

#### GT-086 (mcp-jobs-013): Ruff default rule set drift — nepřítomnost lint configu
**Server:** MCP-Jobs | **Status:** Fixed | **Typ:** Tooling — Dependency/lint determinismus

**Symptom:** GitHub Actions CI (2026-08-15) failoval na kroku `ruff check src/ scripts/healthcheck.py` s "Found 70 errors" — bez jakékoli změny kódu. Lokálně reprodukováno: `ruff check` = 70 chyb.

**Root cause (řetězec):**
1. `pyproject.toml` deps: `ruff>=0.6` **bez horní hranice** → CI nainstaloval nejnovější ruff (0.16.3).
2. Projekt neměl **žádný** `[tool.ruff]` config → aktivní **defaultní pravidla**, která se mění s verzí ruff.
3. ruff 0.16 přidal nová default pravidla (UP045, BLE001, DTZ005, RUF012, PIE810, FURB136) → 70 chyb bez změny kódu. Rule set driftoval s dependency version.

**Fix (`pyproject.toml`):**
```toml
[tool.ruff]
target-version = "py311"
[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "W", "I", "UP", "RUF", "PIE", "FURB", "DTZ"]
ignore = ["BLE001"]
```
- `E4/E7/E9/F` = stabilní ruff default napříč verzemi (core lint).
- `UP/RUF/PIE/FURB/DTZ` = moderní pravidla, která codebase splňuje.
- `E501` (line-length) záměrně mimo — SQL/CSS řetězce jsou záměrně >88 znaků (design trade-off).
- `BLE001` v ignore = zdokumentovaná výjimka (intencionální graceful degradation, komplement GT-081 který pokrývá případ "config od day one").
- Současně opraveno v kódu: RUF012 (`ClassVar`), DTZ005/007/011 (`datetime.now(UTC)`), PIE810 (startswith tuple), RUF003 (en-dash).

**Pravidlo:** P72 — Lint rule set je součást dependency kontraktu. Bez explicitního `select` driftuje s verzí nástroje → CI fail bez změny kódu. Deterministický `select` = single source of truth pro lint konfiguraci. Komplement GT-081 (případ config od day one); tento GT dokumentuje opačnou hranu (config chybí).

**Provenance:** source-read — `pyproject.toml` (deps + nový config), `.github/workflows/ci.yml` (ruff step), ruff 0.16.3 reprodukce 70 chyb, `ruff check --fix` diff review (2026-08-18).

---

#### GT-087 (mcp-jobs-014): MCP timeout -32001 — sync pipeline + client timeout sémantika; fix async submit+poll
**Server:** MCP-Jobs | **Status:** Fixed | **Typ:** Architecture — Async job pattern

**Symptom:** `search_from_config` volané přes MCP (opencode) → `MCP error -32001: Request timed out`. CLI běh fungoval (34.5s / 10 matched). Server "neodpovídá".

**Root cause (2 originální fakta):**
1. **Sync pipeline v toolu** (`server.py:117 _run_pipeline` → `SearchPipeline.run()`): scrape + detail fetch = 34-45s reálné latence. MCP JSON-RPC nad stdio má client-side timeout; při běhu > client timeout klient ukončí request (`-32001`).
2. **opencode `timeout: 180000` v `opencode.jsonc` platí JEN pro fetching tools (ListTools), NE pro tool calls** — konfigurovaný timeout nechrání calls. Prokázáno: server přes správný MCP klient (`mcp` stdio_client) vrací za 33.9s OK → server fungoval, timeout byl na straně klienta.

**Fix (`server.py`) — P13 async submit+poll pattern:**
1. `ThreadPoolExecutor(max_workers=2)` + `_JOB_STORE` (dict, `_JOB_LOCK` threading.Lock) — job běží na pozadí.
2. `search_from_config` / `search_from_yaml` / `search_jobs_v2` → vrátí okamžitě `{job_id, status, message}` (~0.02s).
3. Nový tool `search_status(job_id)` → `{job_id, status: pending/running/done/error, elapsed_s, result}`.
4. Fast-path validace (config not found / YAML parse error / unknown portal) zůstává sync — okamžitý error bez jobu.

**Verifikace:** E2E probe — submit 0.02s, poll done po 42.2s, kompletní výsledek v `result`. Tool registrace: 6 toolů (health_check, list_portals, search_from_config, search_from_yaml, search_jobs_v2, **search_status**).

**Pravidlo:** P13 (rozšířeno) — long-running MCP tool musí být async; submit+poll (job_id + status poll) je 4. varianta fixu, a jediná, která drží **produkční deliverable bez CLI** (na rozdíl od per-job tool / CLI bypass / time-budget z GT-013). Současně: client timeout config (např. opencode `timeout`) se vztahuje na ListTools, ne tool calls — předpoklad, že konfigurovaný timeout chrání calls, je chybný.

**Provenance:** source-read — `server.py` (job runner, search_status), E2E probe přes `mcp` stdio_client (33.9s server OK), E2E probe submit 0.02s / done 42.2s, opencode.jsonc timeout config, CI/CLI run logy (2026-08-18).

---

## 4. Průřezová pravidla P1-P72 (konsolidovaná)

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
2. Nahrazen CLI entry pointem, který obchází MCP transport timeout, nebo
3. **Async submit+poll pattern** (GT-087): tool vrátí okamžitě `{job_id}`, práce běží v `ThreadPoolExecutor` na pozadí, klient polluje `search_status(job_id)` → `{status, elapsed_s, result}`. Jediná varianta, která drží produkční deliverable **bez CLI**.

Současně: client timeout config (např. opencode `timeout` v `opencode.jsonc`) se vztahuje na **ListTools (fetching tools), NE na tool calls** — konfigurovaný timeout nechrání long-running calls; řešení je P13 pattern, ne zvětšení timeoutu (GT-087).

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
Per-game LLM analyzu cacheovat do `{game_id}_llm.json`. Agregace pouzívá summaries z cache místo raw dat. Nová hra = 1 L2 call + 1 agregace, ne full re-run. **Aktualizace (v8):** u multi-perspektiva pipeline (dual-cache white+black) MUSÍ klíc obsahovat perspektivu — `{game_id}_{color}_llm.json`. Jinak oba pohledy sdílí soubor a last-writer-wins prepluje opacnou perspektivu. Reference: GT-079.

### P42 — Cascade resilience
Timeout nebo error jednoho providera v cascade nesmí blokovat pipeline. Cascade je resilience pattern — dalsí provider v poradí prevezme.

### P43 — Pipeline mode (monolit vs inkrementalni)
N≤30 → monolit (1 LLM call). N>30 → inkrementalni (per-game cache + aggregate). Golden rules: rychlá analýza = monolit, hromadná / PGN import = inkrementalni. Explicitní override pres `PIPELINE_MODE` env var.

### P44 — Contract testy mezi moduly (Consumer-Driven Contract)
Kazdy modul v pipeline (Stockfish analyzer → prompt builder → LLM) musi mit contract test, ktery overuje konzistenci klícu mezi producerem a consumerem. Consumer definuje kontrakt (jake klíce potrebuje). Test je schema test na realnych datech + placeholder detection. Profesionalni nastroj: Pact. Lightweight varianta: `assert key in data` + `assert "?" not in prompt`. Reference: `01_METODIKY/05_testing/contract_testing_ontologie_v1.md`.

### P45 — API key health check pri startupu
`verify_api_keys()` v `server.py`. Lightweight ping (max_tokens=1, timeout=10s, per-provider). Detekuje neplatny/vyprseny/rate-limited klic pred prvnim tool volanim. Fail fast. Reference: GT-060.

### P46 — Classification branches must be mutually exclusive
Kazda kategorie v if/elif chainu musi mit vlastni append target. Spolecny cil = tichy data corruption. Unit test overuje, ze zadne dve kategorie nesdileji stejny cil. Reference: GT-061.

### P47 — Cross-LLM audit gate
Pred major release: v1 twin scan (architektura, struktura, bez kodu) + v2 code review (implementace, verifikace). Ani jedna faze nestaci sama. Reference: GT-062.

### P48 — Pattern confidence weighted by sample size
`confidence = min(0.95, base * (1 - 1/(N+1))) * evidence_factor`. Minimal sample N >= 5. Hardcoded confidence neodrazi silu evidence. Reference: GT-063.

### P49 — Sanitize user-supplied identifiers before filesystem use
`re.sub(r'[^a-zA-Z0-9_-]', '_', value)` na vsech vstupech (game_id, username, job_id) pred konstrukci File Path. Zaden user input nesmi byt primo segment v ceste. Reference: GT-065.

### P50 — Parametr clamp musí být signalizován
Pokud clamp (max/min) implicitně ořezává uživatelský vstup, musí logovat warning: `f"[clamp] {param}={value} clamped to {clamped}"`. Tichý ořez = nekonzistentní chování. Reference: GT-066.

### P51 — Pending analysis warning
Každý tool závislý na per-game cache musí před zpracováním zkontrolovat pending count a varovat uživatele. Struktura: cache-first → pending warning → processing → výsledek. Reference: GT-067.

### P52 — Ověř parametr knihovny před použitím
`pip show <library> | grep Version` před použitím nového API parametru. API dokumentace Lichess a berserk dokumentace mohou být desynchronizované. Reference: GT-068.

### P53 — MCP tool list je initialize snapshot
Po přidání nového toolu: (1) restart MCP server, (2) restart opencode session, (3) ověř v `list_tools`. Tool list se neaktualizuje za běhu. Reference: GT-069.

### P54 — Pattern discovery validace
Nový pattern musí být validován: (a) N >= 30 pro statistickou signifikanci, (b) ratio >= 1.4 pro praktickou relevanti, (c) potvrzen v 2+ nezávislých analýzách. Reference: GT-070.

### P55 — Silent except je bug
Každý `except Exception: pass` je bug unless proven otherwise. Silent excepty musí být zalogovány. Reference: GT-071.

### P56 — Stockfish PV SAN konverze
Stockfish PV multi-tahové sekvence musí být konvertovány do SAN sekvenčně na kopii boardu. `board.san(m)` validuje proti aktuální pozici, ne proti rootu. Reference: GT-071, GT-075.

### P57 — K0 noise channel
K0 (orákulum/engine) je samostatný noise channel. Každý run reportuje: depth, engine_version, Threads, Hash, nps_benchmark. ACPL z různých depth nejsou srovnatelné bez K0 korekce. Reference: GT-072.

### P58 — Cache version governance
Cache klíč musí obsahovat verzi kódu (`detector_version`). Při cache load: version mismatch → log warning → re-analyze. Nikdy nepoužívat stale cache po code change. Reference: GT-074.

### P59 — PV jsou sekvenční variace
Stockfish PV v multi-PV módu jsou sekvenční variace, ne paralelní alternativy. Každý PV tah aplikovat na kopii boardu. Nikdy nevalidovat N-tý PV tah proti root pozici. Reference: GT-075.

### P60 — Engine lock isolation
Engine lock vytváří coupling mezi analysis call. Exception uvnitř lock bloku může korumpovat stav engine pro následující volání. Mitigace: (a) žádné AssertionError uvnitř locku, (b) engine restart při timeout locku. Reference: GT-076.

### P61 — Truncated engine lines signalizace
Engine lines count pod multipv_target musí být signalizován. Flag `truncated` a `logger.warning()` per BFS. Reference: GT-077.

### P62 — Ruff --fix je destruktivní, side-effect importy s noqa
Ruff `--fix` maže side-effect importy (F401 unused import) — u registračního patternu `@app.tool()` to ruší registrace toolů. Side-effect importy MUSÍ mít `# noqa: F401` per line. Po každém `ruff --fix`: povinně `git diff` + registrační smoke check (`app._tool_manager._tools` count). Pytest destruktivní smazání registrace nezachytí. Doplnění (GT-081): ruff v automatizaci (CI) běží jako `--check` (read-only) — kontrola. `--fix` je **lidská** operace s `git diff` review — mutace. Separace kontroly od mutace je povinná; `--fix` nikdy do CI gate. Reference: GT-078, GT-081.

### P63 — getattr s defaultem maskuje neexistující atributy
`getattr(obj, "neexistujici", default)` vrací default **bez jakékoli signalizace** — u LLM input pipeline to znamená 100 % garbage v promptu (detekováno na `opening_report`, `opponent_pool`: `opening_name`, `player_color`, `acpl`, `result`). Model pole MUSÍ být čtená přes reálné atributy (`a.game.opening`, `a.total_acpl`) — pak neexistující atribut vyhodí AttributeError při testech. Jestliže default je nutný: logovat warning při použití. Reference: GT-079.

### P64 — Contract evoluce na živých datech je additive
Rozšíření povinného klíčového seznamu contract testu, který iteruje REÁLNÁ cache data, zlomí běh na starších souborech (149× cache bez nového klíče). Nový data klíč = (a) additive test `assert data.get(key, default)` MÍSTO rozšíření `PROMPT_TOP_LEVEL_KEYS`, (b) `.get(key, default)` v deserializaci — ne KeyError. Evoluce contractu nikdy nesmí vynutit migraci legacy dat. Reference: GT-079.

### P65 — Timeout cleanup cílí referenci, která volala
`evaluate_move` používá LOKÁLNÍ engine (vlastní instance), ale timeout handler kvitil sdružený `_engine` → kolaterální zabití konkurující analýzy + zbytečný restart. Cleanup funkce MUSÍ přijmout referenci (`_run_engine_call(fn, timeout_s, engine=None)`) a zabít právě ten objekt, který volání spustil. Reference: GT-079.

### P66 — Fail-fast nad tichou substitucí
Validace nemá akceptovat hodnotu, kterou implementace neumí, a nahradit ji substitucí — hlásí neimplementovaný vstup chybou (`source='chesscom' → error dict`). Tichá substituce = klidná špatná data. Výjimka: degradace s markerem (P67). Reference: GT-079.

### P67 — Degradace dat potřebuje počitatelný marker
`except Exception: pass` + `cp_loss = 0` při selhání evaluate_move klasifikovalo chybný tah jako "best" → ACPL systematicky optimistický bez indikace. Degradace MUSÍ být (a) spočítaná (`GameAnalysis.evaluation_errors` čítač, error dict i výjimka → +1), (b) vystavená do LLM promptu (`Eval errors: N (ACPL may be optimistic)`). Rozšíření P55 (log) o měřitelnou expozici. Reference: GT-079.

### P68 — Legacy cache pole s defaultem má guard před parserem
Starší cache soubory mají pole s prázdným/default defaultem (`m.fen=""`) → `chess.Board(fen="")` vyhodí ValueError a zhrotí celou detekci. Pole, které parser zpracovává, musí mít guard na prázdnou hodnotu (`and m.fen`), konzistentní napříč všemi detekčními funkcemi. Reference: GT-079.

### P69 — Názvy souborů/adresářů jen ASCII (konvence ASCII-NOM)
Názvy souborů a adresářů povolují POUZE `[A-Za-z0-9._-]` — žádná diakritika, mezery, ani non-breaking hyphen (U+2011). Obsah souborů zůstává UTF-8 s diakritikou (konvence platí pro názvy, ne obsah). Důvod: ne-ASCII názvy (a) generují mojibake v git objektech (cp1250 vs UTF-8 — GT-080), (b) U+2011 je vizuálně identický s `-` ale jiný codepoint → rozbíjí copy-paste/grep/RAG, (c) cyklický encoding dluh. Transliterace: `Normalize(FormD)` + drop NonSpacingMark, mezera→`_`, U+2011→`-`, ostatní ne-ASCII→`_`. Ověření: `.scripts/ascii_filenames_check.ps1` (exit 0 = OK). Reference: GT-080.

### P70 — Scraping pipeline s detail fetch = 3 fáze
(1) Collect unikátních URL přes všechny query (set pro dedup), (2) parallel fetch s per-portal throttle (ThreadPoolExecutor, max_workers=4), (3) filter nad naplněnou cache. Sekvenční detail fetch = bottleneck, který eskaluje lineárně s počtem matched ads. Reference: GT-083.

### P71 — Cache failure sentinel: 3 stavy (nezkoušeno / úspěch / selhalo)
Cache pro výsledky s možným selháním MUSÍ rozlišovat 3 stavy: (1) nezkoušeno (`None`/absence klíče), (2) úspěch (hodnota), (3) selhalo (sentinel `_FAILED = object()`). Bez sentinelu = opětovné fetch pokusy pro permanentně selhané URL. Reference: GT-085.

### P72 — Lint rule set je součást dependency kontraktu
Bez explicitního `[tool.ruff.lint] select` driftuje rule set s verzí nástroje (ruff>=0.6 bez horní hranice → nová default pravidla → CI fail bez změny kódu). Deterministický `select` (stabilní E4/E7/E9/F + explicitně vybraná moderní pravidla) = single source of truth; intencionální výjimky (BLE001 graceful degradation, E501 design trade-off) se dokumentují v `ignore`, ne v kódu. Komplement GT-081. Reference: GT-086.

---

## 5. Diagnostický filtr — 71 checkpoints

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

### P — Pipeline consistency & cache governance (P50-P54)
50. Je parametr clamp explicitně signalizován warningem při ořezu? (P50)
51. Kontroluje tool před zpracováním pending count a varuje uživatele? (P51)
52. Je verze knihovny ověřena před použitím nového API parametru? (P52)
53. Je nový tool viditelný v `list_tools` po restartu serveru + opencode session? (P53)
54. Je nový pattern validován N>=30, ratio>=1.4, 2+ analýzami? (P54)

### Q — Engine & PV pipeline integrity (P55-P61)
55. Je každý `except` blok zalogován (ne silent pass)? (P55)
56. Jsou Stockfish PV multi-tahové sekvence konvertovány sekvenčně na kopii boardu? (P56, P59)
57. Reportuje každý run K0 metriky (depth, engine_version, Threads, Hash)? (P57)
58. Obsahuje cache klíč detector_version? Je version mismatch detekován při cache load? (P58)
59. Je engine lock dostatečně izolovaný proti error propagaci? (P60)
60. Je engine lines count pod multipv_target signalizován (truncated flag, warning)? (P61)
61. Existuje mechanismus pro re-analyzi při code change (cache invalidation)? (P58)

### R — Data correctness & contract evolution (P63-P68)
62. Jsou model pole čtená přes reálné atributy (`a.field`), ne `getattr(a, "x", default)`? (P63)
63. Je nový data klíč přidán additive (`.get(key, default)` + additive test), ne rozšířením povinného seznamu testovaného na živých datech? (P64)
64. Kvituje timeout/cleanup handler referenci, která volání spustila (lokální vs sdružený engine)? (P65)
65. Hlásí validace neimplementovaný vstup chybou (fail-fast), ne tichou substitucí? (P66)
66. Má degradace dat počitatelný marker (čítač + expozice v LLM promptu)? (P67)
67. Má pole legacy cache s prázdným defaultem guard před parserem (chess.Board(fen=""))? (P68)

### S — Filename nomenklatura (P69, ASCII-NOM)
68. Jsou všechny trackované názvy souborů/adresářů ASCII `[A-Za-z0-9._-]` (žádná diakritika, mezery, U+2011)? (P69) — ověř `.scripts/ascii_filenames_check.ps1`, exit 0
69. Neobsahuje žádný trackovaný soubor staré cesty/názvy po renames (broken reference)? — ověř `.scripts/context_refs_check.py`, exit 0 (kontrakt: GLOBAL_FORBIDDEN + REPO_FORBIDDEN rename mapa + F1_ALLOWLIST)

### T — Lint determinismus & long-running tools (P72, P13)

70. Je lint rule set deterministický — explicitní `[tool.ruff.lint] select`, NE defaultní sada driftující s verzí nástroje? Intencionální výjimky (graceful degradation, line-length) dokumentované v `ignore`, ne v kódu? (P72)
71. Je long-running tool (>10s) async — submit+poll (okamžitý `job_id` + status poll), nebo má explicitní progress streaming / CLI bypass? Client timeout config (např. opencode `timeout`) se nevztahuje na tool calls, jen na ListTools — timeout calls řeší pattern, ne zvětšení timeoutu. (P13)

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
17. **Per-game LLM cache** (P41) — `{game_id}_{color}_llm.json` (perspektiva v klíči u dual-cache pipeline)
18. **Cascade resilience** (P42) — timeout jednoho providera neblokuje pipeline
19. **Contract testing** (P44) — Consumer-Driven Contract mezi Stockfish → prompt builder → LLM
20. **API key health check** (P45) — `verify_api_keys()` při startupu, detekuje 401/402/429
21. **Mutual exclusive classifications** (P46) — kazda kategorie v if/elif ma vlastni append target. Unit test overi separaci.
22. **Cross-LLM audit gate** (P47) — v1 twin scan + v2 code review pred major release.
23. **Pattern confidence weighting** (P48) — `f(N, evidence_strength)`, hardcoded confidence zakazano.
24. **Path sanitization** (P49) — `re.sub(r'[^a-zA-Z0-9_-]', '_', value)` na user inputech pred filesystem use.
25. **Parametr clamp signalizace** (P50) — clamp nesmi byt tichy, logovat warning pri orezavani.
26. **Pending analysis warning** (P51) — detekce + signalizace neanalyzo-vanych her pred kazdym tool zpracovanim.
27. **Library version check** (P52) — `pip show <library>` pred pouzitim noveho API parametru.
28. **Tool list snapshot** (P53) — po pridani toolu restartovat server + opencode session, overit `list_tools`.
29. **Pattern discovery validation** (P54) — N>=30, ratio>=1.4, potvrzeno 2+ analyzami.
30. **Silent except audit** (P55) — kazdy `except Exception: pass` nahradit logovanim
31. **Stockfish PV SAN konverze** (P56, P59) — sekvencni board.copy() pro PV multi-tahove sekvence
32. **K0 metriky v reportu** (P57) — depth, engine_version, Threads, Hash, nps benchmark
33. **Cache governance** (P58) — detector_version v cache klíci, version mismatch → re-analyze
34. **Engine lock isolation** (P60) — per-call isolation, restart pri timeout locku
35. **Truncated engine lines signal** (P61) — flag truncated + logger.warning() per BFS
36. **Cache invalidation mechanismus** (P58) — automaticka detekce stale cache po code change
37. **Lint autofix guard** (P62) — side-effect importy s `# noqa: F401`, po `ruff --fix` vzdy `git diff` + registracni smoke check
38. **Model field access** (P63) — data do LLM promptu pres realne atributy modelu, ne `getattr` s defaultem; default = warning
39. **Additive contract evolution** (P64) — novy klic pres `.get(key, default)` + additive test, nikdy rozsireni povinneho seznamu na zivych datech
40. **Cleanup target reference** (P65) — timeout/cleanup handler kviti referenci, ktera volala (parametr, ne sdruzeny global)
41. **Fail-fast validation** (P66) — neimplementovany vstup = error dict, ne ticha substituce
42. **Degradation marker** (P67) — pocitatelny citac degradace + expozice v LLM promptu
43. **Legacy field guard** (P68) — pole cache s prazdnym defaultem guard pred parserem (konzistentni s detekcnimi funkcemi)
44. **ASCII filenames** (P69) — vsechny nazvy souboru/adresaru ASCII `[A-Za-z0-9._-]`; overeni `.scripts/ascii_filenames_check.ps1` (exit 0)
45. **Lint determinismus** (P72) — explicitni `[tool.ruff.lint] select` (stabilni E4/E7/E9/F + explicitni moderni pravidla); intencionalni vyjimky (BLE001, E501) v `ignore` s komentarem; horni hranice na ruff v deps
46. **Async submit+poll** (P13) — long-running tool vrati okamzite `{job_id}`, prace v ThreadPoolExecutor, `search_status(job_id)` poll; client timeout config (opencode `timeout`) chrani ListTools, ne calls

---

## 8. Statistiky (merged)

| Metrika | Hodnota |
|---------|---------|
| Celkem GT (GT-001 az GT-087) | 85 |
| Fixed (vcetne "Fixed / Mitigated", "Fixed (policy)") | 56 |
| Implemented (novy feature / mechanismus — L2 cache, pipeline mode atd.) | 4 |
| Mitigated | 6 |
| Documented | 15 |
| Workaround | 3 |
| Pending | 1 |
| **Kontrolni soucet** | **85** |
| Z toho environment/CI issues | 11 |
| Z toho application logic issues | 62 |
| Z toho cross-repo (plati pro vsechny) | 17 |
| Z toho cross-LLM audit (2026-07-24) | 5 (GT-061 az GT-065) |
| Z toho DBCL Phase 2 session 2026-07-27 | 7 (GT-071 az GT-077) |
| Z toho data-correctness fix batch 2026-08-02 | 1 (GT-079) |
| Z toho ASCII-NOM nomenklatura 2026-08-02 | 1 (GT-080) |

**Poznamka ke statistice:** `Fixed` (53) + `Implemented` (4) + `Mitigated` (6) + `Documented` (11) + `Workaround` (3) + `Pending` (1) = 78? **Korekce:** `Fixed` = 52 (GT-071, GT-073, GT-075 = 3 new fixed) + `Mitigated` = 6 (GT-076 = 1 new mitigated) + `Documented` = 11 (GT-072 = 1 new documented) + `Workaround` = 3 (GT-074 = 0 new, zůstává) + `Pending` = 1 (GT-077 = new pending). Fixed 48+3=51, Implemented 4+0=4, Mitigated 5+1=6, Documented 10+1=11, Workaround 3+0=3, Pending 0+1=1 → 51+4+6+11+3+1 = **76**. GT-001 az GT-077 = **77 položek** (GT-068 berserk pagination = Documented, nikoliv chybějící). Zpřesněná čísla: Fixed=51, Implemented=4, Mitigated=6, Documented=12 (GT-068 je Documented, ne Fixed), Workaround=3, Pending=1 → 51+4+6+12+3+1 = **77**. **OK.**

Polozky GT-071 az GT-077 pridany v6 (2026-07-27) — DBCL Phase 2 root cause analysis: engine_lines silent fail, K0 variance, depth drift, cache governance, PV domain knowledge gap, engine lock error propagation, truncated BFS logging.

Polozka GT-078 pridana v7 (2026-08-01) — ruff --fix destruktivni autofix: F401 smazal side-effect tool imports v server.py (lichess-analyzer). Fixed 51+1=52, Implemented 4, Mitigated 6, Documented 12, Workaround 3, Pending 1 → 52+4+6+12+3+1 = **78**. OK.

Polozka GT-079 pridana v8 (2026-08-02) — data-correctness fix batch 1+2 (lichess-analyzer): getattr garbage (B100), hardcoded perspektiva (B98), KB cesta (B121/B119), cache kolize barev (B31), timeout kill reference (B5), ticha degradace ACPL (B16), legacy fen guard (B113). Pravidla P63-P68, aktualizace P41 (color v cache klici). Rozsiren diagnosticky filtr o R sekci (checkpointy 62-67). Checklist dedicnosti rozsiren o polozky 38-43. Fixed 52+1=53, Implemented 4, Mitigated 6, Documented 12, Workaround 3, Pending 1 → 53+4+6+12+3+1 = **79**. OK.

Polozka GT-080 pridana v9 (2026-08-02) — ASCII-NOM nomenklatura (workspace-wide): mojibake v git objektech (cp1250 vs UTF-8), ne-ASCII nazvy (diakritika, mezery, U+2011) prejmenovany na ASCII `[A-Za-z0-9._-]` napric 6 repy (20 souboru, obsah nedotcen). Pravidlo P69. Diagnosticky filtr rozsiren o S sekci (checkpoint 68). Checklist dedicnosti rozsiren o polozku 44. Guard skript `.scripts/ascii_filenames_check.ps1` (exit 0/1). Fixed 53+1=54, Implemented 4, Mitigated 6, Documented 12, Workaround 3, Pending 1 → 54+4+6+12+3+1 = **80**. OK.

v9.1 (2026-08-02) — GT-080 rozsireni: kontraktni validator referenci `.scripts/context_refs_check.py` (exit 0/1, GLOBAL_FORBIDDEN + REPO_FORBIDDEN rename mapa + F1_ALLOWLIST) — prosel 1386 trackovanych souboru / 19 rep, odhalil a opravil **31 broken referenci** (runtime path stringy, README/index/mapa reference, URL-encoded `%C3%9D`, `New_rules/` cesta) napric 7 repy (GCP, lichess, linkedin, mcp-local, dxf, Vcf-compiler, outpost2026_profile). Diagnosticky filtr rozsiren o checkpoint 69. Statistiky beze zmeny (80 entries).

Polozka GT-081 pridana v9.2 (2026-08-02) — architektonicky puvod ruffu v lichess-MCP: CI gate (ne pre-commit hook), config od prvniho commitu `4dd503a`, enforcement `1ca173e`, semanticka eskalace pravidel `98f0546` (F/E/W/I/N/UP/S), mypy/coverage `e41ef52`; `.pre-commit-config.yaml` nikdy neexistoval. P62 rozsiren o separaci kontroly (`--check`) a mutace (`--fix`). Documented 12+1=13, Fixed 54, Implemented 4, Mitigated 6, Workaround 3, Pending 1 → 54+4+6+13+3+1 = **81**. OK.

Polozky GT-083 (mcp-jobs-010, Documented) a GT-085 (mcp-jobs-012, Documented) pridany v10 (2026-08-06, 3-fazova pipeline + cache failure sentinel). Documented 13+2=15 → 54+4+6+15+3+1 = **83**. OK.

Polozky GT-086 (mcp-jobs-013, Fixed) a GT-087 (mcp-jobs-014, Fixed) pridany v11 (2026-08-18) — ruff default rule set drift (P72, komplement GT-081) + MCP timeout sync pipeline/client timeout sementika + async submit+poll (P13 rozsireno). Pravidlo P72. Diagnosticky filtr rozsiren o T sekci (checkpointy 70-71). Checklist dedicnosti rozsiren o polozky 45-46. Oprava reference GT-085: P73 → P71 (duplicita s pravidlem v sekci 4). Fixed 54+2=56 → 56+4+6+15+3+1 = **85**. OK.

---

*MCP_GROUND_TRUTH_postmortem_agregovany_v1.md — 2026-07-27 — v6 — Pridano GT-071 az GT-077 (DBCL Phase 2 RUN_004 root cause analysis: engine_lines silent fail, K0 variance, engine.analysis bez depth limit, cache invalidation, PV SAN domain gap, engine lock propagation, truncated BFS logging). Pridana pravidla P55-P61. Rozsiren diagnosticky filtr o 7 checkpointu (Q sekce). Rozsiren checklist dedicnosti o 7 polozek (30-36). Aktualizovany statistiky (77 entries). — 2026-08-01 — v7 — Pridan GT-078 (ruff --fix destruktivni autofix: F401 side-effect imports, server.py lichess-analyzer) + pravidlo P62. Checklist dedicnosti rozsiren o polozku 37 (lint autofix guard). Aktualizovany statistiky (78 entries). — 2026-08-02 — v8 — Pridan GT-079 (data-correctness fix batch 1+2: getattr garbage, hardcoded perspektiva, KB cesta, cache kolize barev, timeout kill, ticha degradace ACPL, legacy fen guard) + pravidla P63-P68 + aktualizace P41. Diagnosticky filtr rozsiren o R sekci (62-67). Checklist dedicnosti rozsiren o polozky 38-43. Aktualizovany statistiky (79 entries). — 2026-08-02 — v9 — Pridan GT-080 (ASCII-NOM nomenklatura workspace-wide: mojibake git objekty cp1250 vs UTF-8, ne-ASCII nazvy napric 6 repy) + pravidlo P69. Diagnosticky filtr rozsiren o S sekci (68). Checklist dedicnosti rozsiren o polozku 44. Guard skript `.scripts/ascii_filenames_check.ps1`. Aktualizovany statistiky (80 entries). — 2026-08-02 — v9.1 — GT-080 rozsireni: kontraktni validator referenci `.scripts/context_refs_check.py`, opraveno 31 broken referenci napric 7 repy, diagnosticky filtr rozsiren o checkpoint 69 (referencni integrita po renames). — 2026-08-02 — v9.2 — Pridan GT-081 (architektonicky puvod ruffu v lichess-MCP: CI gate vs pre-commit hook, semanticka eskalace pravidel) + rozsireni P62 (separace kontroly --check a mutace --fix). Aktualizovany statistiky (81 entries). — 2026-08-06 — v10 — Pridany GT-082?/GT-083 (mcp-jobs-010: 3-fazova pipeline), GT-084?/GT-085 (mcp-jobs-012: cache failure sentinel). — 2026-08-18 — v11 — Pridany GT-086 (mcp-jobs-013: ruff default rule set drift, pravidlo P72, komplement GT-081) a GT-087 (mcp-jobs-014: MCP timeout sync pipeline + client timeout sementika, async submit+poll, P13 rozsireno). Diagnosticky filtr rozsiren o T sekci (70-71). Checklist dedicnosti rozsiren o polozky 45-46. Oprava reference GT-085: P73 → P71. Aktualizovany statistiky (85 entries).*
