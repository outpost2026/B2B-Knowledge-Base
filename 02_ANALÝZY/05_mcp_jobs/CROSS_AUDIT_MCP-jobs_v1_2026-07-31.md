# CROSS-AUDIT MCP-jobs v1 — Výstupní report nezávislého LLM auditu

**Typ:** audit report | **Účel:** syntéza de novo cross-auditu MCP-Jobs konkurenčním LLM (chain-of-thought) | **EROI:** 9/10
**Autor:** Ondřej Soušek (outpost2026) | **Datum:** 2026-07-31
**Auditovaný:** MCP-Jobs v0.4.0, HEAD `bb3905a`, https://github.com/outpost2026/MCP-Jobs
**Metoda:** LLM auditor prošel repo živě z remote dle CROSS_AUDIT_HANDOFF promptu (de novo, bez teze); nálezy verifikovány autorem proti zdrojovému kódu v pracovní kopii.
**Verifikace nálezů:** ✅ potvrzeno kódem | ⚠️ částečně | ❌ vyvráceno

---

## SEKCE A — NÁLEZY

### CRITICAL

| ID | Závažnost | Umístění | Nález | Dopad | Verifikace |
|----|-----------|----------|-------|-------|------------|
| C1 | CRITICAL | `src/mcp_jobs/pipeline.py:43-47` | `_dedup` fuzzy_key = `(title.lower(), company.lower())`. Dva různé inzeráty (stejný title+company, jiná URL a lokalita — běžné u firem s pobočkami) → druhý **tiše zahozen** bez logu | Reálná ztráta dat napříč lokalitami | ✅ potvrzeno |
| C2 | CRITICAL | `http.py:60-61,70-71,77-78`; `storage.py:157-158`; server detail fetch | **Silent errors bez logování**: `except requests.RequestException: return None` (3× v http.py, logger vůbec neimportován), `except Exception: pass` v `storage.save_correlation`, `except Exception: return None` v `_fetch_detail_text` | Tiché selhání = falešná jistota o datech; poškozený correlation cache se tiše přepíše | ✅ potvrzeno |

### MAJOR

| ID | Závažnost | Umístění | Nález | Dopad | Verifikace |
|----|-----------|----------|-------|-------|------------|
| M1 | MAJOR | `config.py:124-128` + `pipeline.py` | Malformed boolean → jen `logger.warning`, query **zaregistrována**, `evaluate_boolean` vrací False → **tichá 0 shod** pro celou query. README/handoff tvrdí "fail-fast" — není | Uživatel vidí 0 výsledků bez spojení s chybou syntaxe | ✅ potvrzeno |
| M2 | MAJOR | `pipeline.py:84-89` | `detail_cache` cachuje i failure (`None`) — v rámci běhu se failed fetch už nikdy nezkusí | Chybějící popisy = horší matching/exclude kvalita | ✅ potvrzeno |
| M3 | MAJOR | `bazos.py:122`, `pipeline.py:27-34` | Bazos populuje `price`, nikdy `salary`; `_salary_filter` čte `ad.salary` → **filtr pro bazos fakticky no-op** (permisivní fallback `not ad.salary → True`) | Salary filtr tiše nefunguje pro dominantní portál | ✅ potvrzeno |
| M4 | MAJOR | `bazos.py:132` (vzor napříč providers) | Změna container selektoru (`div.inzeraty`) → `cards` prázdné → `if cards and not ads` je False → **úplné ticho, 0 ads bez erroru** | Scraper tiše rozbitý po redesignu portálu | ✅ potvrzeno |
| M5 | MAJOR | `tests/synthetic_guardrails.py` | Není pytest-konvenčně pojmenovaný → **nikdy sbírán CI**; 12 guardrail testů = dead code z pohledu `pytest tests/`; navíc hardcode Windows cesty (`.venv\Scripts\mcp-jobs.exe`) | Falešný pocit pokrytí | ✅ potvrzeno |
| M6 | MAJOR | `pyproject.toml` | Chybí `[project.optional-dependencies]` dev → README quick-start `pip install -e ".[dev]"` **selže** (reprodukováno) | Rozbitý onboarding | ✅ potvrzeno |
| M7 | MAJOR | `README.md` | README stale: uvádí 97/81 testů, skutečnost 103; tool sada zastaralá | Dezinformace pro čtenáře/public delivery | ✅ potvrzeno |

### MINOR

| ID | Umístění | Nález |
|----|----------|-------|
| m1 | `server.py` search_expert | Location s vícero slovy → `(Praha) AND (5)` — sémanticky špatně (chce OR/frázi) |
| m2 | `server.py:423-429` `_default_category` | jobs hardcoded `prace/praha/` — search_jobs_v2 vždy Praha, nezdokumentováno |
| m3 | `server.py:13` | `Matcher` import nepoužitý (dead import) |
| m4 | `bazos.py:49` | Pagination offset hardcoded `(page-1)*20` (magic number) |
| m5 | `storage.py:202` | `__import__('datetime')` inline — datetime už importován na řádku 6 |
| m6 | `pipeline.py:92` | `ad.description = detail` mutuje sdílený pool objekt — cache benefit, ale pořadí queries ovlivňuje performance (korektnost OK) |
| m7 | `storage.py:save_timestamped` | Dva samostatné write (latest + timestamped) — crash window mezi zápisy |

### COVERAGE & TESTS (z audit výstupu)

- **Celkové coverage 66 %**; kritické sliznice: `pipeline.py` 55 % (chybí řádky 69-103 = jádro `run()` kde jsou C1/M2), `storage.py` 34 %, `server.py` 57 % (MCP tool entry pointy netestované), `http.py` 67 % (chybí exception větve = C2), `cli.py` 0 %.
- Chybí: **negativní dedup test** (stejný title+company, jiná URL/lokalita → oba zůstanou), **malformed-boolean test**, HTTP exception-branch testy.
- `live_scrapers.py` testuje deprecated cestu (`build_search_url`+`parse_listings`), ne produkční `scrape_all()`.
- 103 testů PASS (potvrzeno spuštěním).

### VYVRÁCENÉ HYPOTÉZY

| Hypotéza | Výsledek |
|----------|----------|
| Dependency mismatch: pyproject deklaruje `fastmcp>=3.0.0` ale import je `from mcp.server.fastmcp import FastMCP` (jiný balíček) → rozbitá deklarace | ❌ **VYVRÁCENO** — `pip install fastmcp` strhne `mcp` jako tranzitivní dep, import funguje. Auditor správně self-correctoval |

---

## SEKCE B — VERDIKT

Jádro MCP-Jobs je **robustní**: boolean AST matcher (AND/OR/NOT/parens precedence, NFKD diakritika), config dataclasses, rate limiting a 103 procházejících testů jsou nadprůměrné proti konkurenci (žádný nalezený konkurenční repo nemá srovnatelnou test suite). Hlavní slabiny NEJSOU v matching logice, ale v **tiché odolnosti**: silent errors na HTTP/storage vrstvě (C2), tichá ztráta dat v dedup (C1) a tichý fallback-to-0-shod u malformed boolean (M1) — vzorce, které produkují falešnou jistotu. **Public delivery readiness: NE** — chybí CI/CD, coverage reporting, dev extra, rename guardrails testu a oprava README (M5/M6/M7).

## SEKCE C — TOP 5 PRIORIT (EROI: dopad vs náklad)

| # | Fix | Dopad | Náklad |
|---|-----|-------|--------|
| 1 | **C1** dedup: zahrnout lokalitu/URL do fuzzy_key NEBO logovat zahoz | Vysoký (data loss) | S |
| 2 | **C2** logging: import logger do http.py/storage.py, nahradit silent `return None`/`pass` za `logger.warning` | Vysoký (diagnostika) | S |
| 3 | **M1** malformed boolean: fail-fast (raise) při load NEBO skip + explicitní chybový výstup v pipeline | Střední (falešná 0 shod) | S |
| 4 | **M4** container guard: `if not cards: logger.error("selector broken")` napříč providers | Střední (tiché rozbití) | S |
| 5 | **M6+M7** pyproject dev extra + README sync (103 testů) | Střední (onboarding) | S |

## SEKCE D — CHYBĚJÍCÍ TESTY (co by nálezy odhalilo)

1. `test_dedup_different_urls_kept` — stejný title+company, různé URL/lokalita → očekávat 2 ads (chytí C1)
2. `test_malformed_boolean_fails_fast` — nevyvážené závorky → očekávat raise/skip, NE 0 shod (chytí M1)
3. `test_http_exception_logged` — HTTP error → očekávat `logger.warning` záznam (chytí C2)
4. `test_salary_filter_bazos_price_fallback` — bazos ad s `price` → filtr aplikován (chytí M3)
5. `test_container_selector_broken_logs` — prázdný `cards` → očekávat error log (chytí M4)

---

## Odkazy

- Vstupní handoff: `02_ANALÝZY/05_mcp_jobs/CROSS_AUDIT_HANDOFF_MCP-jobs_2026-07-31.md`
- Srovnání s konkurencí: `02_ANALÝZY/05_mcp_jobs/` (srovnani_architektur + rešerše 17 konkurenčních rep)
- Fix plán: P0/P1/P2 pending v MCP-Jobs/.ai_state.json (rozhodovací krok autora)
