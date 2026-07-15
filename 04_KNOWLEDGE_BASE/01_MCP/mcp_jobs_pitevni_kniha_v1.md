# PITEVNÍ KNIHA: MCP-Jobs

Detailní technické záznamy vývoje MCP serveru pro job scraping na českých portálech.

**Datum:** 2026-07-14 | **Verze:** 1
**Repo:** `_github/MCP-Jobs`
**Stack:** Python 3.11+, Playwright, structured logging, boolean parser, ETL pipeline

---

## 022 — Silent failure pattern (`except Exception: continue`)

**Status:** ✅ Fixed

**Symptom:** Bazos scraper vracel 0 výsledků po změně HTML struktury. Pipeline běžela bez chyby, ale data byla prázdná.

**Root cause:** Všichni 4 provider scrapers používaly `except Exception: continue` při parsování jednotlivých karet. Žádná chyba, žádný warning, 0 výsledků.

**Detection:** Claude audit identifikoval pattern teoreticky, ale teprve ETL běh odhalil, že Bazos selectory byly roky rozbité (změna HTML struktury: `.datum` → `span.velikost10`, `.cena` → `.inzeratycena`, `.sub/.lokace` → `.inzeratylok`).

**Fix:**
1. Per-card `logger.warning()` s detailní zprávou (které pole selhalo)
2. Počítadlo skipnutých karet v každém provideru
3. 0-ads `logger.error()` alert na úrovni provideru
4. `logger.exception()` v `server.py` `_run_pipeline()` error handleru

**Kód (pattern):**
```python
# BAD — silent fail
for card in cards:
    try:
        ad = parse_card(card)
        ads.append(ad)
    except Exception:
        continue

# GOOD — structured logging
matched = 0
skipped = 0
for i, card in enumerate(cards, 1):
    try:
        ad = parse_card(card)
        ads.append(ad)
        matched += 1
    except Exception as e:
        skipped += 1
        logger.warning("Skipped card %d/%d: %s", i, total, e)
logger.info("Provider %s: %d matched, %d skipped", name, matched, skipped)
if matched == 0:
    logger.error("Provider %s returned 0 ads — selector breakage likely", name)
```

---

## 023 — Salary filter: split() vs regex false-reject

**Status:** ✅ Fixed

**Symptom:** Inzeráty s platem "30 000 - 50 000 Kč" byly rejectovány salary filtrem. Validní joby s českým formátem čísel mizely.

**Root cause:** `_salary_filter()` používal `str.split()` + `int()`. Český formát používá mezeru jako tisícový oddělovač: `"30 000 - 50 000 Kč".split()` → `['30', '000', '-', '50', '000', 'Kč']`. `int('000')` → `ValueError`.

**Hypotéza auditu:** Split způsobuje false accept ("000" → 0 → pass filter). **Realita:** False reject (ValueError → skip).

**Fix:** `_SALARY_NUM_RE = re.compile(r'\d{1,3}(?:[ \u00a0]\d{3})+|\d+')` — zachytí "30 000" i "50000", ignoruje "000" bez prefixu.

**Verifikace:** 3 nové testy v `test_pipeline.py` — tisícový oddělovač, unparseable ("Dohodou"), cross-URL dedup.

---

## 024 — Exclude čeština — domain-specific semantics

**Status:** ✅ Fixed

**Symptom:** Query "zahradnik" vracela 0 bazos výsledků i přes 11 relevantních inzerátů.

**Root cause:** Czech exclude terms `poptavam`, `poptavame`, `shanim`, `hledam` byly aplikovány globálně. Na Bazosu v sekcích jako zahradník/truhlář/střechy tyto termy znamenají "poptávám zaměstnance" (validní job), ne "hledám práci" (spam).

**Detection:** Debug script — 451/462 Bazos ads zamítnuto booleanem (správně), 11/11 zbývajících zamítnuto exclude termy (false positive).

**Fix:** Odebrány single-word exclude termy z bazos-only queries (zahradnik, truhlar, strechy). Multi-word `hledam praci`, `hledame kolegu` ponechány (jednoznačné).

**Lesson:** Stejné slovo = opačný význam podle kontextu portálu. Exclude listy musí být portal-specific.

---

## 025 — ETL feedback loop dependency

**Status:** ✅ Mitigated

**Symptom:** Bez ETL běhu nebylo možné zjistit, že Bazos selectory jsou rozbité. Audit bez reálných dat odhalil pouze 3/5 bugů.

**Root cause:** Žádný mechanismus pro pravidelné ověření funkčnosti scrapers. HTML struktura českých portálů se mění každých pár měsíců bez varování.

**Fix:**
1. `scripts/run_etl.py` — ETL runner s timestampovaným výstupem (`output/etl_YYYYMMDD_HHMMSS.json`)
2. `output/etl_latest.json` — symlink pro snadné porovnání
3. Session-start health check protokol

---

## 026 — LLM-assisted dev blind spots

**Status:** ⚠️ Mitigated

**Symptom:** Claude audit predikoval salary bug jako false accept a boolean parser jako nejvyšší prioritu. Realita: salary bug byl false reject, boolean parser měl nejnižší prioritu.

**Root cause:** LLM analyzuje kód, ne realitu. Tři z pěti bugů byly v kódu, který LLM neviděl (staré selectory, config exclude). LLM nemá "paměť fungujícího stavu."

**Mitigace:**
1. ETL feedback loop (entry 025) — jediný způsob, jak LLM může detekovat degradaci
2. Session-start ETL health check
3. Testy s reálným HTML (mocky aktuální struktury)

---

---

## 027 — N1: AST re-parse per ad (výkonnostní antipattern)

**Status:** ✅ Fixed (Iteration 4)

**Symptom:** `evaluate_boolean()` volal `parse_boolean()` pro každý jednotlivý inzerát zvlášť. Při 8 query × 1000 ad = 8000 kompletních parsování stejného AST. Blokující bod pro L4 streaming.

**Root cause:** `parse_boolean()` vytvářel nový AST pokaždé, bez cache. Funkcionálně korektní, ale lineárně neškálovatelný.

**Detection:** Sonnet 5.0 audit (cross-LLM meta-analýza). Předchozí v0.3 audit ani autor si nevšimli.

**Fix:** `@functools.lru_cache(maxsize=128)` na `parse_boolean()`. 8000 → 8 parsování.

**EROI:** 1h effort, 99,9% snížení CPU na boolean matchi. Klíčové pro budoucí streaming.

**Lesson:** LRU cache je triviální změna, kterou LLM audit odhalil až při druhém průchodu. Potvrzuje hodnotu cross-LLM metody.

---

## 028 — N4+N5: Chybějící guardraily (pages + rate limiting)

**Status:** ✅ Fixed (Iteration 4)

**Symptom:** `search_jobs_v2(pages=500)` by spustilo stovky sekvenčních requestů bez limitu. Bulk-scrape neměl žádné zpoždění mezi requesty.

**Root cause:** Původní návrh upřednostnil rychlost před ToS compliance. "Playwright zero delay" z Phase 02 byl přenesen do requests-based architektury beze změny.

**Detection:** Sonnet 5.0 audit — identifikoval jako reálné produkční riziko (nejen teoretické).

**Fix:**
1. `pages = max(1, min(pages, 50))` v `search_jobs_v2()` — clamp guard
2. `request_delay=1.0` + `_throttle()` v `HttpClient` — 1s delay mezi requesty

**Důsledek:** Pipeline time 22.7s → 46.2s (+23.5s = rate limiting overhead). Nutný kompromis pro publikaci.

**Lesson:** Rychlost ≠ kvalita. Rate limiting je etický scraping 101, ne volitelný doplněk.

---

## 029 — N6: Boolean auto-validace při config loadu

**Status:** ✅ Fixed (Iteration 4)

**Symptom:** `validate_boolean()` existovala jako otestovaná funkce, ale nikdo ji nevolal při načítání configu. Malformed boolean výraz v YAML se projevil až jako tichý 0 výsledek po 20s+ scrapingu.

**Root cause:** Mrtvý kód — funkce napsaná, otestovaná, ale nezapojená do pipeline.

**Fix:** Volání `validate_boolean(qc.boolean)` v `UserConfig._from_raw()` po vytvoření každého `QueryConfig`.

**Lesson:** Funkce, která není nikým volána, neexistuje. Fail-fast princip: chybu odhalit co nejdřív.

---

## 030 — N7: MCP error kontrakt

**Status:** ✅ Fixed (Iteration 4)

**Symptom:** Per-provider errors v `search_jobs_v2()` byly vraceny jako embedded `errors` pole v datové odpovědi, ne jako tool-level chyba. Každý tool řešil errors jinak.

**Root cause:** Postupný vývoj — každý tool přidán v jiné fázi, error handling nebyl nikdy sjednocen.

**Fix:**
1. Per-provider errors → `[{"error": "Portal errors: ..."}]` při žádných výsledcích
2. Při částečných výsledcích errors zůstávají jako metadata
3. Všechny tools vrací `[{"error": ...}]` konzistentně

---

## 031 — N8+N11: Config error messages + lint

**Status:** ✅ Fixed (Iteration 4)

**Symptom:** `CategoryConfig(**c)` házel raw `TypeError` na neznámý YAML klíč. `from .matcher import matches_ad` byl uvnitř for smyčky.

**Fix:** try/except TypeError s popisnou zprávou v config.py. matches_ad přesunut na top-level import v server.py.

---

## 032 — Cross-LLM audit metoda

**Status:** ✅ Ověřeno

**Zjištění:** Tři modely (v0.3 Claude, Sonnet 5.0, peer review) našly každý jiné nálezy. N1 (AST cache) byl nejcennější — nikdo si ho předtím nevšiml. Security layer byl blind spot všech modelů.

**Závěr:** Metoda "nechat více LLM auditovat stejný kód a porovnat výstupy" je extrémně efektivní pro identifikaci slepých míst. Užitečnost pro imerzní učení: 9/10.

---

## 033 — L2 Resources: mcp-jobs://ads/{query_id}

**Status:** ✅ Fixed (Phase 05)

**Symptom:** Hledání (search_jobs_v2, search_from_config, search_from_yaml) vracelo výsledky pouze v kontextu LLM odpovědi. Data nebyla adresovatelná — jakmile LLM kontext skončil, výsledky nebylo možné znovu získat bez nového scrapingu.

**Root cause:** MCP maturity chyběla L2 vrstva (Resources). Tool data byla pomíjivá — LLM si je mohl přečíst jen jednou v okamžiku volání.

**Detekce:** Explicitní roadmap v README maturity tabulce (L2 Resources označeno jako ⬜ Plánováno).

**Fix:** 3 nové resources:
1. `mcp-jobs://ads/list` — JSON seznam všech uložených resultsetů v session
2. `mcp-jobs://ads/{query_id}` — JSON data (stejná, co tool vrátil)
3. `mcp-jobs://ads/{query_id}/report` — Markdown report (human-readable)

Architektura:
- In-memory `_query_store` v `server.py` (dict: query_id → {data, timestamp})
- `_store_results()` helper — UUID hex[:8] jako klíč
- Každý search tool ukládá výsledky a vrací `query_id` + `resource_uri`
- Výsledky jsou perzistentní po dobu životnosti serveru

**Bump:** v0.3.0 → v0.4.0 (L2 milestone)

**Verifikace:** 103/103 testů, 6 nových resource testů. L2 maturity: ⬜ → ✅

---

## 034 — PowerShell f-string quoting (encoding/quoting fragility)

**Status:** ✅ Fixed (Phase 05)

**Symptom:** Při spouštění Python kódu přes PowerShell `python -c "..."` s f-stringy a vnořenými uvozovkami docházelo k `SyntaxError: f-string: unmatched '['`. Encoding-sensitive znaky (emoji, azbuka) způsobovaly `UnicodeEncodeError: 'charmap' codec can't encode character`.

**Root cause — 3 vrstvy interpretace:**
```
LLM kód → PowerShell → cmd.exe (CommandLineToArgvW) → Python
```
Každá vrstva interpretuje quotes/escaping jinak:

| Vrstva | Interpretace | Konflikt s Pythonem |
|--------|-------------|---------------------|
| PowerShell | `$var`, `@()`, `""` a `''` quoting | `'title'` uvnitř `f"..."` |
| cmd.exe | `^` escape, `%VAR%`, argument splitting | Windows API rozdělí argument na mezerách |
| Python | Dostane už rozbitý kód | `SyntaxError` |

Konkrétně: Windows API `CommandLineToArgvW` rozděluje argumenty podle mezer. Víceřádkový kód s vnořenými uvozovkami v `-c` se rozseká dřív, než ho Python uvidí → SyntaxError.

**Encoding root cause:** Windows Console defaultuje na cp1250 (Central European). Python stdout encoding zdědí cp1250 → emoji a Unicode supplementary planes (U+1F000+) nelze zobrazit → `UnicodeEncodeError`.

**Fix — 6-vrstvý mitigacní stack:**

| Vrstva | Mechanism | Soubor |
|--------|-----------|--------|
| 6 | PowerShell $PROFILE autoload | `_github/_init.ps1` → `$PROFILE` |
| 5 | AI guardrails | `.ai_guardrails.json` shell_rules |
| 4 | Dokumentace | `docs/powershell_encoding.md` |
| 3 | Project-level helpers | `scripts/init.ps1` (Run-Python, Invoke-Pipeline, Compare-ETL) |
| 2 | Batch launcher encoding | `mcp-jobs.bat` (PYTHONIOENCODING + PYTHONUTF8) |
| 1 | Python runtime | `cli.py` + `server.py` → `ensure_utf8_stdout()` |

Plus: `opencode.jsonc` přidáno `-X utf8` do commandů všech 3 MCP serverů.

**Hlavní pravidlo:** Nikdy nepoužívej `python -c "..."` s komplexním kódem v PowerShellu. Vždy piš do .py souboru a spouštěj přes `python -X utf8 script.py`.

**Verifikace:** 12 syntetických guardrail testů — 12/12 PASS. 103/103 unit testů OK.

---

## 035 — 6-layer encoding mitigation — architectural hardening

**Status:** ✅ Implementováno (Phase 05)

**Popis:** Systematické řešení encoding/quoting problémů napříč všemi vrstvami stacku — od PowerShell profilu až po Python runtime. Každá vrstva zachytí selhání té předchozí (defence in depth).

| Vrstva | Co řeší | Selhání vrstvy pod ní zachytí |
|--------|---------|-------------------------------|
| 6. $PROFILE autoload | Encoding vars chybí v session | User/agent zapomněl načíst init.ps1 |
| 5. AI guardrails | AI generuje fragile pattern | Agent neví o Windows omezeních |
| 4. Dokumentace | Dev nechce guardrails číst | AI ignoruje guardrails |
| 3. Project helpers | python -c s komplexním kódem | Dev/agent píše inline kód |
| 2. Batch launcher | Encoding není v server startupu | Python runtime fix nestačí |
| 1. Python runtime | stdout encoding = cp1250 | Všechny vyšší vrstvy selhaly |

**EROI:** 8/10 — ~90 řádků kódu + dokumentace eliminuje ~10–20 min/session encoding/quoting chyb.

**Budoucnost:** Tento stack je přenositelný na jakýkoliv Windows Python projekt. Stačí zkopírovat `_init.ps1`, přidat `$PROFILE` řádek a importovat `ensure_utf8_stdout()`.

---

*mcp_jobs_pitevni_kniha_v1.md — 2026-07-15 — v2 — entries 033–035 (Phase 05: L2 Resources + encoding 6-layer stack)*
