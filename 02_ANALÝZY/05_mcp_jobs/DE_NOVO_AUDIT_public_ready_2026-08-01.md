# DE NOVO AUDIT + PUBLIC-READY RESEARCH — MCP-Jobs (v0.4.0)

**Typ:** analýza / audit | **Účel:** de novo deep-dive audit dle metodiky CROSS_AUDIT_HANDOFF, README sémantická kontrola, research public-ready standardů 2026, inspirace z outprep | **EROI:** 9/10
**Autor:** Ondřej Soušek (outpost2026) | **Datum:** 2026-08-01
**Repo:** https://github.com/outpost2026/MCP-Jobs | **Branch:** main (HEAD 55b0e44, čistý strom)
**Kompletní verze včetně Dockerfile/GitHub Actions/SQLite SQL:** `MCP-Jobs_DE_NOVO_AUDIT_PUBLIC_READY_2026-08-01.docx` (lokálně, *.docx gitignored)

---

## 0. METODIKA

De novo — žádný závěr z v1 auditu/fix balíku přejímán bez ověření. Vše verifikováno proti kódu (pytest 123/123 PASS, 8.4 s). Tříkolejně: (A) kodový audit, (B) research public-ready, (C) outprep analýza. Jistota: P>0.8 = exekucí/čtením, jinak hypotéza.

## 1. OVERENÝ STAV

- Verze 0.4.0 (__init__ = pyproject), Python >=3.11, fastmcp>=3.0.0, deps bez pyyaml (runtime bug, F2)
- Tools (5): health_check, search_from_config, search_from_yaml, search_jobs_v2, list_portals — sedí s README
- Resources: ads_list static + ads_by_id/ads_report_by_id templates — **EN README tvrdí "Planned" = nepravda (F7)**
- Testy: **123 collected / 123 PASS** — README tvrdí 97 = nepravda (F8)

## 2. SEKCE A: NÁLEZY

### CRITICAL (2)
| ID | soubor:řádek | popis | fix |
|----|--------------|-------|-----|
| F1 | server.py:17 vs :62 | `CorrelationRecord` použit v `_save_correlation()` ale **nikdy importován**; konstrukce records stojí mimo try/except | `from .storage import CorrelationRecord, Storage` |
| F2 | pyproject.toml:11-15 | `pyyaml` chybí v runtime deps (config.py:8 import yaml) → `pip install .` selže ImportError | přidat pyyaml>=6.0 do dependencies + requirements.txt |

### MAJOR (5)
| ID | soubor:řádek | popis |
|----|--------------|-------|
| F3 | matcher.py:58-59 | `\b` boundary selže pro query končící non-word znakem — `evaluate_boolean("C++ Developer","c++")` = **False** (C++, C# = běžné IT dotazy, tiše 0 výsledků). Ověřeno exekucí. |
| F4 | server.py:375-381 | `search_expert` generuje `NOT hledam praci` (multi-word exclude) → parser ValueError → rozbité query pro agenta |
| F5 | pipeline.py:90-111 | lazy detail fetch = 1 HTTP request (1 s throttle) na každý matched ad bez description → reálná latence 5-30+ min vs README "~46 s" |
| F6 | config.py/http.py | **žádná URL/SSRF validace** — YAML akceptuje libovolné URL (169.254.169.254, localhost) → SSRF proxy zneužití |
| F7 | README_EN.md:199 | EN README "Resources: Planned" — plně implementováno |

### MINOR (11) / NIT (2)
- F8 README stale: "97" testů (realita 123), srovnávací tabulky v0.3.x (realita 0.4.0)
- F9 README popisuje query z config.yaml.example (python_jobs, cnc_jobs...), ne z primárního config.yaml (python_ai_engineer, cnc_cam_automation...)
- F10 `_salary_filter` any(n>=min) — rozsah "20 000 - 30 000" vs min 25 000 = True, i když spodní hranice pod limitem
- F11 config query/portal body `None` → AttributeError místo srozumitelné ValueError
- F12 `_save_query_store` bez try/except, `_query_store` globální dict bez locku (race)
- F13 guardrails testy netestují skutečnou `ensure_utf8_stdout()` (vakuózní)
- F14 apparent_encoding přebíjí meta charset (mojibake); throttle per-client, ne globální
- F15 correlation_cache bez trimmování → neomezený růst, O(n²) append
- F16 chybí `__main__.py` — `python -m mcp_jobs` nefunguje
- F17 run_etl_metrics.py hardcoded "Unit tests: 79" (stale, realita 123)
- F18 docs/l2_resources.md "perzistence není implementována" — je (query_store.json)
- F19 tests/live_scrapers.py mimo pytest collect (dead)
- F20 loose version ranges bez upper bound; cli.py:30 sahá na private `mcp._tool_manager._tools`
- Doplněk: strip_emoji nechává dvojité mezery; search_jobs_v2 neukládá korelaci; dedup fuzzy key bez NFKD

## 3. README SÉMANTICKÁ AKTUÁLNOST (EN + CZ)

**Verdikt: OBA README JSOU STALE.** Nejzávaznější jsou nepravdy (97 testů vs 123, "Planned" resources), pak zastaralá čísla/verze a popis jiné konfigurace než config.yaml. Zavádějící výkonnostní claim "~46 s" neodpovídá realitě s lazy detail fetchem (F5). Jediný správný self-report: README:221 přiznává nedokumentovaný threat model. Doporučeno: regenerovat čísla, sjednotit EN/CZ strukturu, sekce "Verifikováno" s datem, aktualizovat výkonnostní claimy po fixu F5.

## 4. SEKCE B: VERDIKT

Jádro matcheru (AST, diakritika, exclude, dedup) solidní a dobře testované. Ale 2 CRITICAL bugy drží MCP tool layer na hraně: neimportovaný `CorrelationRecord` (reálné hledání spadne NameError) a chybějící pyyaml v runtime (veřejná instalace rozbitá). Nejhlubší logický gap: word-boundary regex tiše selhává pro C++/C#. Public delivery readiness: **NE** — chybí CI/CD, lint, typing, coverage, dependency audit, SSRF ochrana.

## 5. SEKCE C: TOP 5 PRIORIT (EROI)

1. F1 import CorrelationRecord (1 řádek, zprovozní oba search tooly)
2. F2 pyyaml do runtime deps (1 řádek, umožní instalaci)
3. F3 boundary fix pro C++/C# (malý regex + 2 testy, odblokuje běžné dotazy)
4. F5 cap lazy detail fetch + README výkonnost (z desítek minut na minuty)
5. F6 URL/SSRF allowlist (podmínka bezpečné public delivery)

## 6. SEKCE D: CHYBĚJÍCÍ TESTS (chytily by nálezy)

1. E2E tool test s fake providerem (non-empty results → query_id, žádná exception) → F1
2. Manifest test import mcp_jobs.server bez dev extras → F2
3. Boundary: ("C++ Developer","c++"), ("C# Dev","c#") → True → F3
4. search_expert multi-word exclude → validate_boolean OK → F4
5. Call-count test fetch_detail capped → F5
6. scrape_all("http://169.254.169.254/...") odmítnuto → F6
7. Config None-body → ValueError (ne AttributeError) → F11
8. Salary low-bound → False → F10
9. ensure_utf8_stdout skutečně zavolaná (mock stdout) → F13
10. Dedup s diakritikou (NFKD klíč) → dedup gap

## 7. PUBLIC-READY RESEARCH 2026

**Transport/auth:** Streamable HTTP = 2026 standard (nahrazuje SSE); stdio = jen lokální. FastMCP 3.x: providers+transforms, middleware, per-component authorization, host_origin_protection, mcp-session-id. OAuth 2.1 + PKCE mandatory pro remote; pro stdio postačí env API key + reverse-proxy basic auth.

**Benchmark (nejvyzrálejší = francisco-perez-sorrosal/linkedin-mcp):** SQLite+FTS5+WAL (5 tabulek), cache-first <100 ms, background scraper, adaptive rate limiting, Pydantic exclude_none. ever-jobs: 160+ zdrojů, proxy rotation, Promise.allSettled. eliasbiondo: hexagonální architektura + DI. job-monitor: 3-vrstvá dedup, GH Actions free tier.

**Doporučený stack (detaily v DOCX):**
- SQLite FTS5 WAL: tabulka jobs (id, source, external_id, title, company, location, salary_min/max, url UNIQUE, description, raw_json) + UNIQUE(source, external_id) + jobs_fts (porter unicode61) + triggery. Raw sqlite3, žádný ORM.
- Dockerfile: multi-stage (builder s uv --frozen --no-dev --no-editable → runtime bez uv, USER app, HEALTHCHECK, EXPOSE 8000) + .dockerignore (venv, pycache, git) + OCI labels + SBOM/Trivy.
- GitHub Actions: ci.yml (matrix 3.12/3.13, uv sync --locked, ruff check+format, mypy strict, pytest --cov-fail-under=70, uv audit, uv build) + release.yml (semantic-release + trusted publishing OIDC) + Dependabot.
- ruff: target py312, line-length 100, extend-select [I,UP,B,SIM,RUF]; mypy strict; pytest --strict-markers --cov.
- Best practices: max ~10 tools (každý žere ~4K tokenů), async tools, Pydantic return types + exclude_none, `{"error":...}` dict místo výjimek, uv.lock committed, pre-commit.

**Priority EROI:** 1) SQLite+FTS5 (diferenciace) ★★★★★ 2) uv+CI ★★★★★ 3) Dockerfile non-root ★★★★ 4) async+Pydantic+error pattern ★★★★ 5) Streamable HTTP + OAuth ★★★ 6) semantic-release+PyPI ★★★ 7) observability ★★★

## 8. OUTPREP INSPIRACE (SWE šachová doména)

**Stack:** npm workspaces monorepo (engine / fide-pipeline / harness + Next.js 16 app), PostgreSQL 16 provider-agnostic, Vercel+ISR, Stockfish WASM client-side, ChessEngine interface (browser vs Node adapter).

**Přenositelné senior patterns (TOP 10):**
1. CI/CD jako primární quality gate — outprep jej NEMÁ (jediný gate = lokální husky) → MCP-Jobs udělat opak
2. Testovací pyramida: pure-logic core oddělené od I/O, deterministické fixtures; mock náhodu, ne síť
3. Doménové typy = single source of truth (engine types re-export do app) → pydantic modely sdílené adaptery
4. Provider-agnostic adapter pattern (ChessEngine interface) → BasePortal ABC se 4 implementacemi
5. Graceful degradation (HAS_POSTGRES → return null; cache write failure non-fatal) → feature-flag offline
6. Typovaný error handling → McpError kódy, retry backoff na 429
7. Pre-commit gate (ruff, mypy, fast pytest — NE e2e)
8. Env/secrets hygiena + SECURITY.md s trust modelem
9. Konfigurace s dokumentovanými defaulty + idempotentní migrace
10. README = prodejní + technický, 30s quickstart + smoke test

**Co NEkopírovat (chyby outprep):** žádné CI, e2e v pre-commit hooku, eslint ignoruje packages/**, string-matching error handling, in-memory cache s "TODO Vercel KV", stale docs (forge neexistuje), hardcoded cesty.

## 9. ROADMAP

- **Hotfix (1 den):** F1, F2, F3, F4, F7/F8/F9/F18 (README+docs sync)
- **Engineering-proces (2-3 dny):** uv+uv.lock, ruff+mypy strict, GH Actions ci+release, pre-commit, coverage baseline 66%, Dependabot
- **Produktový (1 týden):** SQLite+FTS5+WAL, Dockerfile, async+Pydantic+error pattern, SSRF allowlist+SECURITY.md, cap detail fetch, __main__.py+--smoke
- **Post-public:** Streamable HTTP+OAuth, PyPI trusted publishing, observability, RAG/embeddings (sqlite-vec/ChromaDB)

## 10. Metadata

- **EROI:** 9/10 | **Tags:** `#mcp-jobs`, `#de-novo-audit`, `#public-ready`, `#outprep`, `#sqlite-fts5`, `#phase09`
- **Návaznost:** CROSS_AUDIT_MCP-jobs_v1, CROSS_AUDIT_HANDOFF (metodika), FIX_BALIK_cross_audit (Phase 08)
