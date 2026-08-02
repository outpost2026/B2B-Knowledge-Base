# PHASE 09 HOTFIX — MCP-Jobs v0.4.0

**Typ:** fix report | **Účel:** dokumentace aplikace F1-F4 + F7/F8/F9/F18 z de novo auditu (public-ready)
**Repo:** https://github.com/outpost2026/MCP-Jobs | **Commit:** 45f70ad (main, pushnuto)
**Návaznost:** DE_NOVO_AUDIT_public_ready_2026-08-01.md (Phase 09 roadmap, Hotfix balík)

---

## 1. Aplikované fixy

| ID | Soubor | Fix | Verifikace |
|----|--------|-----|------------|
| F1 | server.py:17 | `from .storage import CorrelationRecord, Storage` — import chyběl, `_save_correlation()` padal NameError | Reálný zápis do correlation_cache.json OK (žádná výjimka) |
| F2 | pyproject.toml + requirements.txt | `pyyaml>=6.0` do runtime dependencies (config.py:8 import yaml; `pip install .` selhával ImportError) | Manifest: pyyaml v runtime i v requirements |
| F3 | matcher.py `_Word.evaluate` | `(?<!\w)...(?!\w)` místo `\b...\b` — term končící non-word znakem (c++, c#, .net) nikdy nematchoval | 7 nových assertů v test_matcher.py (vč. negativních: cc++ != c++) |
| F4 | server.py search_expert | Multi-word exclude `NOT (hledam AND praci)` — původní `NOT a b` byl parse error (parser je strict-only, implicitní AND nepodporuje) | validate_boolean=True, sémantika NOT(phrase) ověřena evaluate_boolean |
| F7 | README_EN.md L2 Maturity | "Planned" → implementováno (3 resources) | — |
| F8 | README.md + README_EN.md | 97 → 125 testů; srovnávací tabulky v0.3.x → v0.4.0 (Iteration 3→8); +2 řádky (silent errors, persistence) | — |
| F9 | README.md + README_EN.md | Query příklady dle primárního config.yaml (python_ai_engineer, ai_llm_engineer, mcp_agentic, data_engineering, devops_ci_cd, prumyslova_automatizace, cnc_cam_automation, reverse_engineering) | — |
| F18 | docs/l2_resources.md | Perzistence na disk je implementována (query_store.json + correlation_cache.json, od fáze 06) — obě nepravdy opraveny | — |

## 2. Testy

- **125/125 PASS** (123 → 125, +2 nové testy: F3 boundary non-word, F4 multi-word exclude)
- Sada vč. regresní kontroly F4 na původním testu (asserty změněny z `NOT senior` na `NOT (senior)`)

## 3. Doplňky

- README Known Limitations: přidána poznámka o lazy detail fetch (F5 — cap plánován v produktovém balíku, výkonnostní claim "~46 s" se týká pipeline bez detail fetch)
- pyproject dev extras: + `pytest-cov>=5.0` (příprava na coverage baseline)

## 4. Zbývající roadmap (Phase 09)

1. **Engineering-proces (2-3 dny):** uv + uv.lock, ruff + mypy strict, GH Actions ci+release, pre-commit, coverage baseline 66%, Dependabot
2. **Produktový (1 týden):** SQLite+FTS5+WAL, Dockerfile non-root, SSRF allowlist + SECURITY.md (threat model), cap detail fetch (F5), `__main__.py` + `--smoke`
3. **Post-public:** Streamable HTTP + OAuth, PyPI trusted publishing, observability, hosted demo

## 5. Metadata

- **Tags:** `#mcp-jobs`, `#phase09`, `#hotfix`, `#public-ready`
- **Návaznost:** DE_NOVO_AUDIT_public_ready, FIX_BALIK_cross_audit (Phase 08), CROSS_AUDIT_MCP-jobs_v1
