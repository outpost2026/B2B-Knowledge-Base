# CROSS-AUDIT HANDOFF — MCP-Jobs (v0.4.0, refactor)

**Typ:** handoff / audit-injekt | **Účel:** křížová validace konkurenčními LLM (cross audit) | **EROI:** 8/10
**Autor:** Ondřej Soušek (outpost2026) | **Datum:** 2026-07-31
**Repo:** https://github.com/outpost2026/MCP-Jobs | **Branch:** main (= refactor, ff-merged) | **HEAD:** bb3905a

---

## 0. ÚČEL DOKUMENTU

Tento dokument je **LLM-ready / RAG-ready handoff** pro hloubkový audit repozitáře MCP-Jobs
konkurenčním LLM (frontier model). Poskytuje rychlou orientaci o SW, architektuře, záměru,
výstupech, testech a metrikách. **Audit probíhá vždy de novo, bez předchozí teze** — kontext
slouží pouze k orientaci, ne jako přijaté závěry. LLM má **live přístup na remote URL**
(https://github.com/outpost2026/MCP-Jobs) a zájmové části repa si čte sám.

Cíl auditu: identifikace **gaps, silent errors, logických chyb, dependency rizik, sémantických
vazeb a slabin** z pohledu seniorního deva. Scope je korigován (scope creep control): high SNR,
high EROI.

---

## 1. MACHINE-READABLE CONTEXT (rychlé parsování)

```
repo:                MCP-Jobs
remote:              https://github.com/outpost2026/MCP-Jobs
default_branch:      main (refactor ff-merged 2026-07-31)
head_commit:         bb3905a
version:             0.4.0 (pyproject.toml)
license:             MIT
language:            Python >=3.11
framework:           fastmcp>=3.0.0 (MCP SDK, stdio transport)
deps:                requests>=2.32.0, beautifulsoup4>=4.12.0 (+ dev: pytest, yaml)
package_layout:      src/mcp_jobs/ (config, models, http, matcher, pipeline, storage, utils, server, cli, providers/)
providers:           bazos.py, jobs.py, pracecz.py, nyx.py (deprecated)
tools_mcp:           health_check, search_from_config, search_from_yaml, search_jobs_v2, list_portals
resources_mcp:       mcp-jobs://ads/list, mcp-jobs://ads/{query_id}, mcp-jobs://ads/report/{query_id}
prompts_mcp:         search_expert
configs:             config.yaml (AI-native), config_legacy_manual.yaml (fallback), config_pracecz_jobs.yaml
outputs:             JSON + MD reporty, etl_{PROFILE}_{ts}, latest_{PROFILE}, correlation cache
tests:               103 collected (9 test souborů: config, matcher, pipeline, providers, server, utils, synthetic_guardrails, live_scrapers)
commits:             34 (2026-07-13 .. 2026-07-31)
target_domain:       CZ pracovní portály (bazos.cz, jobs.cz, prace.cz)
scoring:             EROI golden rules (domain 35%, tech 25%, role 20%, growth 10%, formal 5%, location 5%) — via B2B-Knowledge-Base
```

## 2. ZÁMĚR / POSITIONING

- **Problém:** autor (Ondřej Soušek, industrial automation / CNC/CAM / formalizace tacitních znalostí)
  hledá relevantní pracovní nabídky na CZ trhu (strojírenství, elektrika, správa budov, IT).
- **Řešení:** MCP server, který stahuje inzeráty z veřejných CZ portálů (bez auth), filtruje je
  boolean matcherem (AND/OR/NOT/parens), NFKD diakritikou, exclude listy se skloňováním, location
  a salary filtry, a výsledky ukládá jako JSON/MD + EROI scoring.
- **Diferenciace vs konkurence:** český trh + diakritika + české skloňování v exclude listech,
  plný boolean AST, 103 unit testů, ToS compliance (rate limiting 1.0s, pages guard, auto-validace).
- **Známé gapy (z interního srovnání 2026-07-31, NEPOVAŽOVAT za tezi):** chybí persistent storage
  (SQLite/FTS5), chybí streamable-http transport (pouze stdio), chybí CI/CD (GitHub Actions, ruff,
  mypy), chybí application tracking, chybí hosted deployment.

## 3. ARCHITEKTURA

```
src/mcp_jobs/
├── cli.py          # entry point: python -m mcp_jobs.cli (stdio transport, -X utf8, PYTHONIOENCODING)
├── server.py       # FastMCP instance, tool/resource/prompt registrace, query_store, correlation cache
├── config.py       # UserConfig -> PortalConfig -> CategoryConfig -> QueryConfig (dataclasses, YAML)
├── models.py       # Ad dataclass (title, url, portal, desc, company, date, price, location)
├── http.py         # HttpClient: retry, timeout, rate limiting (1.0s delay), BeautifulSoup
├── matcher.py      # strip_diacritics (NFKD), boolean AST (recursive-descent), LRU cache, exclude
├── pipeline.py     # SearchPipeline: scrape_all -> per-query filters -> dedup -> results
├── storage.py      # CSV I/O, save_timestamped, save_correlation, markdown_report, rag_index_md
├── utils.py        # strip_emoji
└── providers/      # base.py (ABC + metrics), bazos.py, jobs.py, pracecz.py, nyx.py
```

Pipeline flow:
1. `_scrape_all()` -> pool [Ad] (všechny portály, kategorie, stránky; 1.0s delay mezi requesty)
2. Pro každý query: portal filter -> boolean match (AST, LRU cached) -> exclude filter -> location -> salary
3. dedup (URL-normalize) -> uložení JSON/MD + correlation cache

## 4. METRIKY (golden rules REPO cross validation)

| Metrika | Hodnota | Poznámka |
|---|---|---|
| Unit testy | 103 | test_matcher, test_pipeline, test_providers, test_config, test_server, test_utils, synthetic_guardrails |
| Test pokrytí | neuvedeno | Měření coverage NEprovedeno — gap k ověření |
| CI/CD | NEEXISTUJE | Žádné GitHub Actions, žádný ruff/mypy/pip-audit — gap |
| Lint / typing | chybí | ruff, mypy, pyright nejsou v pyproject — gap |
| Dependency audit | chybí | pip-audit/safety není zapojen — gap |
| Coverage report | chybí | — gap |
| Release/PyPI | NE (v0.4.0 lokálně) | — gap |
| Changelog | NE | — gap |
| Docstring/type hints | ANO | moduly mají type hints + docstringy |
| Structured logging | ANO | per-card skip count, 0-ads alert, žádné silent failures |
| Rate limiting | 1.0s / request | ToS compliance |
| Pages guard | max 50 stránek | resource abuse prevence |
| Auto-validace configu | ANO | fail-fast na malformed YAML/boolean |
| Encoding mitigace | 6-layer stack | cp1250 konzole, PYTHONIOENCODING, -X utf8, sys.stdout.reconfigure |

## 5. UKÁZKY KÓDU (reprezentativní fragmenty)

### 5.1 Boolean AST + NFKD diakritika (matcher.py)
```python
def strip_diacritics(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.category(c).startswith("M"))

@functools.lru_cache(maxsize=128)
def parse_boolean(expression: str) -> _Node:
    tokens = _tokenize(expression)
    parser = _Parser(tokens)
    return parser.parse()

def validate_boolean(expression: str) -> bool:
    if not expression or not expression.strip():
        return True
    try:
        parse_boolean(expression)
        return True
    except (ValueError, IndexError) as e:
        logger.warning("Malformed boolean expression %r: %s", expression, e)
        return False
```

### 5.2 Config dataclasses (config.py)
```python
@dataclass
class QueryConfig:
    boolean: str = ""
    min_salary: int = 0
    locations: list[str] = field(default_factory=list)
    portals: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)

@dataclass
class UserConfig:
    user: str = "default"
    profile: str = "default"
    portals: dict[str, PortalConfig] = field(default_factory=dict)
    queries: dict[str, QueryConfig] = field(default_factory=dict)
    @classmethod
    def from_yaml(cls, path: str | Path) -> UserConfig: ...
    @classmethod
    def from_yaml_string(cls, yaml_content: str) -> UserConfig: ...
```

### 5.3 Exclude matching se skloňováním (matcher.py)
```python
def has_exclude_terms(title, exclude_terms, description="") -> bool:
    # word-boundary na title, substring na description (české skloňování)
    # single-word termy POUZE na title — na popisu false positives
    # ("hledam" matches "Koho hledáme")
    ...
```

## 6. AUDIT PROMPT (injekt pro LLM — vložit celé do promptu)

```
Provádíš hloubkový cross-audit repozitáře MCP-Jobs (https://github.com/outpost2026/MCP-Jobs).
Audit provádíš DE NOVO — nepřebírej žádný závěr z přiloženého kontextu jako pravdivý.
Kontext (sekce 0-5 výše) ti slouží POUZE pro rychlou orientaci. Ověřuj vždy proti live kódu na remote.

ROZSAH (scope creep control — zaměř se striktně na tyto TASKY, nic víc):
1. KÓD: seniorní code review hlavních modulů — matcher.py, pipeline.py, config.py, http.py, providers/*.
   Hledej: logické chyby, silent errors (try/except bez logu), edge cases, race conditions,
   resource leaky (neuzavřené sessiony, file handles), špatné URL/lokační parsování.
2. LOGIKA: boolean matcher (operator precedence, NOT v kombinaci s AND/OR, LRU cache nekonzistence),
   exclude matching (word-boundary vs substring na CZ skloňování), dedup normalizace, salary regex.
3. DEPENDENCIES: fastmcp>=3.0.0, requests, beautifulsoup4 — verze, zranitelnosti, zbytečné deps,
   chybějící pinning, dev-deps.
4. SÉMANTICKÉ VAZBY: konzistence mezi config.yaml, config_legacy_manual.yaml, providers a storage
   (názvy portálů, query profily, correlation cache schéma).
5. TESTS: pokrytí kritických cest (matcher edge cases, pipeline, providers), chybějící E2E testy,
   kvalita testů (ne triviální, netestují implementation detail), testy živých scraperů (live_scrapers.py).
6. SECURITY/ROBUSTNOST: HTML parsing (broken HTML, None handling), SSRF/URL validace, retry/backoff,
   encoding (cp1250/UTF-8 konzole), timeouty.
7. PUBLIC DELIVERY: chybějící CI/CD, lint, typing, coverage report, dependency audit, changelog,
   release. Co je kritické pro otevření jako public repo.

VÝSTUP (strukturovaný, maximální SNR):
- Sekce A: NÁLEZY (ID | závažnost CRITICAL/MAJOR/MINOR/NIT | soubor:řádek | popis | dopad | návrh fixu)
- Sekce B: VERDIKT (3-5 vět — stav jádra, nejkritičtější gap, readiness pro public delivery)
- Sekce C: TOP 5 PRIORIT (rankované dle EROI: dopad vs náklad fixu)
- Sekce D: CHYBĚJÍCÍ TESTS (konkrétní testy, které by chytly tvé nálezy)

NEPSAT: nic co nemůžeš doložit v kódu. Žádné generické best-practices rady bez vazby na repo.
Nepoužívej emoji. U každého nálezu uveď úroveň jistoty (P>0.8 / hypotéza).
```

## 7. SCOPE GUARDRAILS (pro autora i auditora)

- Focus = high SNR, high EROI: jen nálezy s reálným dopadem (silent errors, data ztráta, crash,
  correctness bug). NIT bez dopadu = max 1 řádek.
- Audit NEPŘEJÍMÁ teze z interního srovnání (sekce 2 "známé gapy") — jsou to hypotézy autora,
  nikoli fakt.
- Live scraper testy (E2E) se spouští pouze pokud auditor má běžící Python env; jinak statická analýza.
- Výsledky auditu se zapisují jako nový artefakt (cross_audit_v1_<model>_<datum>.md), nikoli
  modifikace kódu. Nález -> návrh fixu -> samostatný rozhodovací krok autora.

## 8. ZDROJE / REFERENCE

- Repo: https://github.com/outpost2026/MCP-Jobs
- Interní srovnání s konkurencí: 02_ANALÝZY/05_mcp_jobs/ (srovnani_architektur_mcp_vs_scrapers_2026-07-31.md)
- EROI metodika: B2B-Knowledge-Base (00_STRATEGIE)
- Pitevní kniha MCP: 04_KNOWLEDGE_BASE/01_MCP/MCP_GROUND_TRUTH_postmortem_agregovany_v1.md
- Konkurence (benchmark): eliasbiondo/linkedin-mcp-server (163*), SanthaKumar-K-2004/linkedin-mcp-zero (29 tools),
  francisco-perez-sorrosal/linkedin-mcp (SQLite FTS5), ever-jobs/ever-jobs (160+ zdrojů),
  borgius+chinpeerapat+supg jobspy-mcp (JobSpy wrapper)
