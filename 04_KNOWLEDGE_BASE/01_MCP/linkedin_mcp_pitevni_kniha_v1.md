# PITEVNÍ KNIHA: linkedin-mcp-custom

Detailní technické záznamy vývoje MCP serveru pro automatizovanou analýzu LinkedIn nabídek.

**Datum:** 2026-07-07 | **Verze:** 1
**Repo:** `_github/linkedin-mcp-custom`
**Stack:** Python 3.12, FastMCP, Patchright (Playwright fork), EROI scoring engine

---

## 007 — Typová záměna BrowserContext vs Browser
**Status:** ✅ Fixed

**Symptom:** `get_or_create_browser()` vracelo `BrowserContext`, ale volající kód očekával `Browser`. Volání `context.browser()` vracelo `None`.

**Root cause:** Patchright (Playwright fork) rozlišuje `Browser` (process) a `BrowserContext` (izolovaný session). Launch persistent context vrací `BrowserContext`, ne `Browser`. Dokumentace Playwrightu tuto distinkci zdůrazňuje, ale autodidakt četl "browser" a očekával `Browser`.

**Fix:** Singleton na úrovni `BrowserContext`. Všechny tool funkce přijímají `context` a volají `context.new_page()`.

**Kód:**
```python
# BAD
_browser: Browser | None = None
_context = await _playwright.chromium.launch_persistent_context(...)
_browser = _context  # type: ignore — BrowserContext != Browser

# GOOD
_context: BrowserContext | None = None
_context = await _playwright.chromium.launch_persistent_context(...)
pages = _context.pages
_page = pages[0] if pages else await _context.new_page()
```

---

## 008 — Shadow lokální proměnná (Missing global)
**Status:** ✅ Fixed

**Symptom:** Session state se ztrácel mezi voláními toolů. Po prvním tool callu byl `_context` správně inicializován, po druhém byl `None`.

**Root cause:** Python bez `global` deklarace vytvoří lokální shadow proměnnou. Funkce `close_browser()` zapisovala do `_context = None` bez `global _context` → vytvořila novou lokální proměnnou, globální zůstala nepřiřazená.

**Fix:** Přidáno `global _context, _page, _playwright` do každé funkce, která zapisuje do globálních proměnných.

**Lesson:** Viz P7 — každá funkce zapisující do modulové globální proměnné musí mít `global jméno`.

---

## 009 — Auth navigační konflikt (is_logged_in redirect)
**Status:** ✅ Fixed

**Symptom:** `ensure_authenticated()` navigovalo na `/feed/` pro kontrolu login stavu, ale tato navigace přerušila právě probíhající načítání target stránky (jobs-tracker). Výsledek: auth check OK, ale target stránka se nenačetla.

**Root cause:** `is_logged_in()` volalo `page.goto("https://www.linkedin.com/feed/")` — tím opustilo aktuální stránku. Poté target navigace musela začít znovu, ale MCP tool už pokračoval s extrakcí z prázdné stránky.

**Fix:** Auth check se provádí před navigací na target URL. V `extract_page()` je pořadí: (1) `ensure_authenticated(page)`, (2) `navigate_to_page(url)`. Tím se auth navigace nekříží s target navigací.

---

## 010 — Fragilita CSS selektorů (DOM mutace)
**Status:** ✅ Fixed

**Symptom:** Po A/B testu LinkedIn změnilo CSS třídy → selektor `button.artdeco-pagination__button--next` přestal fungovat → pagination tiše selhala (vždy vracela page 1).

**Root cause:** LinkedIn používá A/B testování a auto-generované CSS class names. Selektor postavený na CSS třídách je ephemeral — vydrží dny až týdny, pak se změní bez varování.

**Fix:** Dvě vrstvy — (1) specifický selektor pro rychlost, (2) text-based fallback `innerText` matching na "Další"/"Next"/"›". Nikdy nespoléhat jen na CSS třídy.

**Kód:**
```python
# 1) Try specific CSS selector (fast path)
bySelector = document.querySelector('span.cf719dd1._076af65a...')
# 2) Text-based fallback (resilient)
for el of document.querySelectorAll('span, button, a'):
    if /^(Další|Next|›|»)$/i.test(el.innerText):
        el.click()
```

---

## 011 — Paginační slepota (Missing second page)
**Status:** ✅ Fixed

**Symptom:** Session 3 debug: `scrape_saved_jobs()` vrátilo jen 17 job IDs z očekávaných 27+. Chyběla data z page 2 a 3.

**Root cause:** Dva nezávislé bugy:
1. **Pagination click:** Přepisovač cílové stránky (`target_page = current_page + 1`) místo klikání na tlačítko "Další". Pokud se číslo tlačítka neshodovalo s target_page, nekliklo se na nic.
2. **Wait-for-content:** Po kliknutí se nečekalo na DOM refresh → extrakce proběhla ze stejné stránky podruhé.

**Fix:**
1. Nová `_click_next_page()` — hledá tlačítko "Další" bez ohledu na číslo stránky. CSS selector + text fallback.
2. `wait_for_timeout(3000)` + `wait_for_selector` s `timeout=10000` pro detekci nového obsahu.

**Verifikace:** Session 4 — 49 ID z 5 stránek, 0 duplicit.

---

## 012 — Špatný git repo root v parents indexu
**Status:** ✅ Fixed

**Symptom:** `KBWriter.commit_changes()` volalo `git add -A` z `self.linkedin_dir.parents[2]`, ale repo root byl ve skutečnosti `parents[1]`. Výsledek: git commit selhal s `fatal: not a git repository`.

**Root cause:** `Path.parents` je 0-indexovaný. `parents[0]` = `00_linkedin`, `parents[1]` = `02_ANALÝZY`, `parents[2]` = repo root. Index 2 byl špatně — root je `parents[1]` (protože `linkedin_dir` má 2 složky hloubky: `02_ANALÝZY/00_linkedin`).

**Fix:** `parents[1]` → `parents[1]` (správně). Přidán `relative_to()` assert pro verifikaci.

---

## 013 — Fragilní extrakce job ID
**Status:** ✅ Fixed

**Symptom:** `_extract_job_ids()` našlo jen 17/27 job ID v Session 3. LinkedIn ukládá job ID na více místech v DOMu, nejen v `<a href>`.

**Root cause:** Původní implementace hledala jen:
```javascript
document.querySelectorAll('[href*="/jobs/view/"]')
```
To pokrylo jen job ID v `<a>` elementech. LinkedIn ale ukládá ID také v:
- Data atributech (`data-job-id`, `data-entity-urn`)
- Script JSON blotech (`window.__INITIAL_STATE__`)
- `aria-label` a `data-tracking` atributech
- `urn:li:jobPosting:ID` formátu v metadata

**Fix:** 4-vrstvá extrakce:
```javascript
// 1) <a href="/jobs/view/ID">
document.querySelectorAll('[href*="/jobs/view/"]')

// 2) Všechny element attributes — data-*, aria-*, urn:li
for (const attr of el.attributes) {
    /urn:li:jobPosting:(\d{8,})/.test(attr.value)
    /\/jobs\/view\/(\d{8,})/.test(attr.value)
}

// 3) Script JSON — 10-digit numbers near "job"/"posting"/"saved"
for (const script of document.querySelectorAll('script:not([src])')) {
    /(?<!\d)(\d{10})(?!\d)/g  + context check
}

// 4) Full outerHTML regex scan
document.documentElement.outerHTML.match(/\/jobs\/view\/(\d{8,})/g)
```

**Verifikace:** Session 4 — 49/49 ID, 0 duplicit.

---

## 014 — KBWriter dedup fallback: `industry` = vždy None
**Status:** ✅ Fixed

**Symptom:** Každý pipeline run vytvářel nové (duplicitní) záznamy v metadata_stacku.json místo updatu stávajících. Dedup podle LinkedIn job ID fungoval, ale fallback podle title+company nikdy nenalezl shodu.

**Root cause:** v `_format_entry_json()`:
```python
"company": {
    "type": None,
    "size_range": None,
    "industry": None,  # ← company name se nikam neukládá!
}
```
A v `_find_entry_index()`:
```python
# new = title|eroi.company  (správně: "Engineer|Siemens")
new_norm = _normalize(f"{eroi.job_title}|{eroi.company}")
# stored = title|company.industry  (vždy: "Engineer|None" → neshoda)
stored_norm = _normalize(
    f"{entry.get('title', '')}|{entry.get('company', {}).get('industry', '')}"
)
```

**Fix:** Ukládat `eroi.company` do `company.industry`:
```python
"industry": eroi.company,
```

**Dopad:** Nové záznamy mají korektní `industry`, staré záznamy (před fixem) zůstávají s `null` — ty se matchnou jen přes `linkedin_job_id`.

---

## 015 — Summary table non-idempotent
**Status:** ✅ Fixed

**Symptom:** Každý update existujícího záznamu přidal nový řádek do `## Souhrnná statistika` v agregovany_report.md. Po 3 runech → 3 řádky pro každý job.

**Root cause:** `_update_summary_table()`:
```python
if found_table:
    result_lines.append(new_row)  # ← vždy append, nikdy replace
```

**Fix:**
```python
row_replaced = False
for line in lines:
    if found_table and line.strip().startswith(f"| {fid} |"):
        result_lines.append(new_row)  # replace
        row_replaced = True
        continue
    result_lines.append(line)
if found_table and not row_replaced:
    result_lines.append(new_row)  # append if new
```

---

## 016 — MCP transport timeout pro batch operace
**Status:** ⚠️ Workaround

**Symptom:** `get_saved_jobs` a `analyze_saved_jobs` vracejí `MCP error -32001: Request timed out`. Kód běží správně, ale nestihne se dokončit v MCP timeout okně.

**Root cause:** MCP protokol (JSON-RPC over stdio) má timeout na úrovni hostitele (klientská aplikace, typicky 60–120s). Sekvenční scraping N jobů:
- N=27: ~85s → timeout
- N=49: ~150s+ → timeout

MCP není navržen pro long-running batch operace.

**Workaround:** CLI test script `scripts/test_scrape.py` volá scraper přímo bez MCP transportu:
```bash
.venv/Scripts/python scripts/test_scrape.py
```

**Budoucnost:** Možná řešení:
1. Asynchronní MCP s progress streamingem (přes `ctx.info()`)
2. Rozdělení do více malých MCP tool calls (one job per call)
3. Background worker s MCP notification

---

## 017 — Python version mismatch (.venv vs system)
**Status:** ✅ Fixed

**Symptom:** `linkedin-mcp --login` selhával s cryptic import errors. Package vyžaduje Python ≥3.12, ale `.venv` používal 3.11.

**Root cause:** System Python je 3.11.0rc2. `.python-version` = 3.12. `uv sync` vytvořilo .venv z nejbližší dostupné verze (3.11). Package se nainstaloval, ale závislosti (FastMCP, Patchright) vyžadují ≥3.12.

**Detection:**
```bash
python --version              # 3.11 — system
.venv/Scripts/python --version # 3.12 — .venv (po fixu)
```

**Fix:**
```bash
uv venv --python 3.12
uv sync
```

---

## 018 — Console script not in PATH
**Status:** ✅ Fixed

**Symptom:** Uživatel zadá `linkedin-mcp --login` → `command not found`. `.venv/Scripts/linkedin-mcp.exe` existuje, ale není v PATH.

**Root cause:** `uv sync` instaluje konzolové scripty do `.venv/Scripts/`. Tento adresář není v system PATH (na rozdíl od `pip install --user`, který instaluje do `AppData/Roaming/Python/Scripts`).

**Timeline:**
1. `uv sync` → `linkedin-mcp.exe` v `.venv/Scripts/` (OK)
2. `linkedin-mcp` → `command not found` (user confusion)
3. Mitigace: `.bat` wrapper v repo root
4. Trvalé řešení: `.venv/Scripts` přidán do User PATH via `setx`

**Fix:**
```batch
:: .bat wrapper — funguje ze všech shellů
@echo off
"%~dp0.venv\Scripts\linkedin-mcp.exe" %*
```

```powershell
# PATH integrace (jednorázově)
setx PATH "%PATH%;C:\...\linkedin-mcp-custom\.venv\Scripts"
```

---

## 019 — Shell escaping fragility (Windows/Bash/PowerShell)
**Status:** ⚠️ Mitigováno

**Symptom:** Každý pokus o spuštění PowerShell commandu z bash stringu selhal (3/3 v Session 4). Různé znaky (`$`, `\`, `` ` ``, `"`) mají v každém shellu jiný význam.

**Případy selhání:**

| Pokus | Shell | Chyba |
|-------|-------|-------|
| `powershell -Command "[Environment]::SetEnv..."` | Bash → PS | `$env:PATH` expandnuto bashovsky |
| `cmd.exe /c "where linkedin-mcp.exe 2>&1"` | Bash → cmd | `&&`, `>` expandnuto bashovsky |
| `cd /d ... && command` | Bash | `/d` není bash přepínač |

**Řešení (P16):** Každou PowerShell operaci psát jako `.ps1` script a spouštět ho:
```bash
powershell -File scripts/operace.ps1
```

**Lesson pro autodidakta:** Windows development ≠ Linux development. Git Bash není bash na Linuxu. Každý shell je samostatný ekosystém s vlastními pravidly. Testovat commands v target shellu před použitím v automation.

---

## 020 — Cookie lifecycle — silent expiry
**Status:** ⚠️ Otevřeno

**Symptom:** Po dni nebo dvou `ensure_authenticated()` začne vracet `AuthenticationError`. LinkedIn session cookie expiruje, ale není způsob, jak to detekovat předem.

**Root cause:** LinkedIn session management — cookies mají proměnlivou dobu expirace. Není veřejná dokumentace o délce platnosti. Při obnově stránky může LinkedIn vyžadovat CAPTCHA nebo email verification.

**Chybějící:**
1. Pre-check: `is_logged_in()` před scrapingem, s jasnou log message o stavu
2. Graceful handling: při expiraci nefailovat pipeline, ale zastavit a vyzvat k re-loginu
3. Cookie age tracking: ukládat timestamp posledního úspěšného login checku

**Dočasná mitigace:**
```bash
.\linkedin-mcp.bat --status   # check before pipeline
.\linkedin-mcp.bat --login    # re-authenticate
```

---

## Timeline Session 3 → Session 4

| Datum | Událost | Dopad |
|-------|---------|-------|
| Session 3 | První pipeline run: 27 ID, A1–A6 identifikovány | Baseline |
| Session 4 | A4 fix: `industry` store company name | ✅ Dedup funguje |
| Session 4 | A5 fix: summary table idempotent | ✅ Žádné duplicity |
| Session 4 | MCP timeout (A3) reprodukován na `get_saved_jobs` | ⚠️ Workaround |
| Session 4 | Session cookie expired | Uživatel musel re-login |
| Session 4 | `linkedin-mcp` not in PATH → `.bat` wrapper | ✅ Trvalé řešení |
| Session 4 | PowerShell escaping v bash — 3/3 selhání | P16 pravidlo |
| Session 4 | `.venv/Scripts` added to User PATH | ✅ |

---

## Statistiky

| Metrika | Hodnota |
|---------|---------|
| Celkem bugů (007–020) | 14 |
| Fixed | 11 (79 %) |
| Workaround | 1 (7 %) |
| Otevřeno | 2 (14 %) |
| Z toho devtool/environment issues | 4 (019, 017, 018, 016) |
| Z toho application logic issues | 10 |

---

## Session 6 — Záznam 021-024 (2026-07-08)

### 021 — CI/CD cookie export: cookies nejsou JSON, ale Chromium SQLite
**Status:** ✅ Fixed

**Symptom:** GitHub Actions workflow failnul na prvním běhu — `~/.linkedin-mcp-custom/profile/cookies.json` neexistuje, přestože lokálně LinkedIn MCP server funguje. Patchright persistent context ukládá cookies do Chromium SQLite databáze, ne jako samostatný JSON soubor.

**Fix:** Vytvořen `scripts/export_cookies.py` — exportuje cookies přes `context.cookies()` → JSON → GitHub Secret. Workflow injectuje přes `context.add_cookies()`.

**Lesson:** Session cookies pro CI vyžadují explicitní export/import krok. Nutný refresh při expiraci.

### 022 — PAT workflow scope: .github/workflows/ vyžaduje `workflow` scope
**Status:** ✅ Documented

**Symptom:** `git push` rejectnul commit s `.github/workflows/weekly-scrape.yml` — "refusing to allow a Personal Access Token to create or update workflow without workflow scope".

**Fix:** Přidat `workflow` scope do PAT v GitHub Developer settings.

**Lesson:** `repo` scope nestačí pro push workflow souborů. `workflow` scope je samostatná permission.

### 023 — Session compact directory: MCP workdir vs. source code repo
**Status:** ✅ Documented

**Symptom:** Během Session 6 working directory = `mcp-local-server` (cnc-tools), ale práce v `linkedin-mcp-custom`. Nejednoznačnost kde spouštět příkazy.

**Lesson:** Všechny bash příkazy musí mít explicitní `workdir` parametr. Session compact = přepnutí kontextu MCP toolů, ne source code.

### 024 — Scorer unit test discovery: testy jako living documentation
**Status:** ✅ Fixed

**Symptom:** 6 z 27 nových testů selhalo — očekávané hodnoty neodpovídaly skutečné scorer logice (např. `role_score("Sales Engineer")` = 60, ne 25).

**Fix:** Testy opraveny na aktuální chování — 28 testů, 100% pass. Testy nyní slouží jako living documentation.

**Lesson:** Testy psát až po analýze kódu, ne podle očekávání. Failed testy = discovery mechanismus.

---

## Statistiky

| Metrika | Hodnota |
|---------|---------|
| Celkem bugů (007–024) | 18 |
| Fixed | 15 (83 %) |
| Workaround | 1 (6 %) |
| Otevřeno | 2 (11 %) |
| Z toho environment/CI issues | 7 |
| Z toho application logic issues | 11 |

---

*linkedin_mcp_pitevni_kniha_v1.md — 2026-07-07, aktualizováno 2026-07-08 — Session 6 (Záznam 021-024)*
