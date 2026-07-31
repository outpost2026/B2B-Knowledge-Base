# CROSS-AUDIT FIX BALIK — MCP-Jobs v0.4.0 (Phase 08)

**Typ:** fix report | **Účel:** dokumentace aplikace P0/P1/P2 fixů z cross-auditu + fresh test verifikace | **EROI:** 9/10
**Autor:** Ondřej Soušek (outpost2026) | **Datum:** 2026-07-31
**Repo:** https://github.com/outpost2026/MCP-Jobs | **Branch:** main | **Fix HEAD:** a99713c + working tree (před push)

---

## 1. VSTUPNÍ STAV

- **Audit v1 (verifikovaný):** CROSS_AUDIT_MCP-jobs_v1 — C1/C2 CRITICAL, M1-M7 MAJOR, 66% coverage.
- **Audit Grok/xAI (nový, 2026-07-31):** konvergentní s v1; navíc base.py silent except (C2 doplněk), SSRF (m6, nízká priorita), bazos fetch_detail NIT (m7). **Chybná interpretace M4** — "částečně opraveno" NEplatí, guard `if cards and not ads` nechrání rozbitý selektor (cards=[] → ticho). v1 M4 potvrzen jako nevyřešený.
- **Metoda:** každý fix verifikován proti kódu (P>0.9), poté fresh ETL run + determinismus check.

## 2. APLIKOVANÉ FIXY (10)

| ID | Fix | Soubor | Detail |
|----|-----|--------|--------|
| C1 | dedup ztráta dat | `pipeline.py:_dedup` | fuzzy_key rozšířen o `(ad.location or "")`; při dropu `logger.warning` (duplicate URL / fuzzy hit). Pobočky s jinou lokalitou projdou. |
| C2 | silent errors | `http.py`, `storage.py:157`, `base.py:97` | import logger; silent `return None`/`pass` → `logger.warning(...)`. Corrupted correlation cache zalogován. |
| M1 | malformed boolean | `config.py:124` | `logger.warning` → `raise ValueError(f"Query {name!r}: malformed boolean ...")`. Fail-fast splněn. Ověřeno: všechny 3 config soubory validní. |
| M2 | detail_cache retry | `pipeline.py:100` | failed fetch se NEcachuje (`detail_cache[ad.url]` jen při úspěchu) → další query retry. |
| M3 | bazos salary no-op | `pipeline.py:_salary_filter` | fallback `ad.salary or ad.price`. |
| M4 | container guard | `bazos.py`/`jobs.py`/`pracecz.py` | nová větev `if not cards: logger.error("...0 cards...")` před stávajícím blokem. |
| M5 | guardrails test | `tests/synthetic_guardrails.py` → `tests/test_synthetic_guardrails.py` | rename + pytest konvence; odstraněn main() runner, Windows hardcode `.venv\Scripts\mcp-jobs.exe`, závislost na `~/.config/opencode`. |
| M6 | pyproject dev extra | `pyproject.toml` | `[project.optional-dependencies] dev = [pytest, pyyaml, ruff]`. |
| M7 | dead import + location | `server.py` | `Matcher` import odstraněn; search_expert location `AND` → `OR` join. |
| m3 | datetime | `storage.py:rag_index_md` | `__import__('datetime')` → top-level `datetime`. |

## 3. FRESH TEST VERIFIKACE (determinismus / regrese)

- **Run:** `run_etl.py --config config.yaml` → 98.7s, EXIT 0 (baseline 99.9s).
- **Porovnání s baseline** `etl_20260731_154939.json`:

| Metrika | Baseline | Fresh | Verdikt |
|---|---|---|---|
| total_matched | 26 | **26** | identické |
| uniq URL | 15 | **15** | identické |
| per-query (8) | 5/1/6/4/3/3/3/1 | 5/1/6/4/3/3/3/1 | 0 diff |
| NEW-only / BASE-only | — | 12/12 | tržní drift + searchId parametry, NE regrese |

- **Anomálie z logu (58 WARNING, 0 ERROR):**
  - 33× fuzzy dedup drop — očekávané (stejný title+company+location, jiná URL = repost se searchId). Dříve tiché, teď viditelné (C2).
  - 24× exact dup URL — očekávané (ad napříč kategoriemi).
  - 1× 404 bazos `/brigada/160/` — legitimní stop paginace (text None → break).
  - 0 ERROR — selectory zdravé, M4 guard nealarmuje falešně.

## 4. TEST SUITE

- **103 → 123 PASS** (+20: dedup-location, dedup-warning, salary-price fallback, salary-over-price, HTTP exception ×3, container guard ×3, malformed-boolean-fail-fast, detail-cache-retry, guardrails 8).
- Změněn `test_from_yaml_malformed_boolean_logged` → `test_from_yaml_malformed_boolean_fails_fast` (M1 semantika).
- `ruff` nenainstalován lokálně — deklarován v dev extra.

## 5. VYŘEŠENO / PENDING

**Vyřešeno (Phase 08):** C1, C2, M1-M7, m3.

**Pending (Phase 09+):**
- P2: SSRF URL validace (m6 Grok, nízká priorita — lokální nástroj), bazos fetch_detail NotImplementedError dokumentace (m7 Grok), container-guard testy (doplněny zde), m1 search_expert Praha hardcode.
- CI/CD (GitHub Actions + ruff + mypy + coverage report).
- Coverage report (66% baseline; pipeline 55% → jádro nyní pokryto novými testy).
- SQLite/FTS5 persistent storage.
- Streamable-http transport.
- Security threat model.
- README sync (97→123 testů, aktualizace claimů).
- Sladit nemecko-blocklist mezi config a scrapers topics.csv.

## 6. Metadata

- **EROI:** 9/10 | **Tags:** `#mcp-jobs`, `#cross-audit`, `#fix-balik`, `#phase08`, `#determinism`, `#fresh-test`
- **Návaznost:** CROSS_AUDIT_MCP-jobs_v1 (vstup), CROSS_AUDIT_HANDOFF_MCP-jobs (metoda).
