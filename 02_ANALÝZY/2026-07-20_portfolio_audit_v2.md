# Portfolio Audit v2 - 2026-07-20

**Datum:** 2026-07-20 | **Autor:** outpost2026
**Úcel:** Komplexní audit vsech MCP serveru v portfoliu po iteracni optimalizaci.
**Metoda:** Systematický pruzkum kazdého .py souboru + configu + testu + CI/CD + dokumentace.

---

## Prehled

| Server | Hodnoceni | Zmena od v1 | Kritickych | Strednich | Nizkych |
|--------|-----------|-------------|------------|-----------|---------|
| lichess-analyzer | 4.5/10 | +0.5 | 8 | 15 | 17 |
| cnc-tools | 4/10 | -0.5 | 8 | 15 | 13 |

---

## 1. lichess-analyzer — detail

### 1.1 Kritické (CRITICAL/HIGH)

| # | Soubor | Radky | Problem | Severity |
|---|--------|-------|---------|----------|
| L1 | `.env` | 1-4 | **API klice v repozitari** — LICHESS_TOKEN, DEEPSEEK_API_KEY atd. plaintext v .env, ktery neni spravne odstranen z historie | CRITICAL |
| L2 | `.github/workflows/test.yml` | 14 | **CI broken** — contract testy vyzaduji Stockfish cache, ktera v CI neni. CI vzdy failne. | HIGH |
| L3 | `game_llm_cache.py` | 39-58 | **I/O bez try/except** — open() / json.load() bez ochrany. Poskozeny JSON = unhandled exception. | HIGH |
| L4 | `workspace_info.py` | 20 | **Privatni FastMCP API** — `_tool_manager` je privatni atribut. Rozbije se pri upgradu. | HIGH |
| L5 | `pattern_detector.py` | 160-163 | **Logicka chyba v Bait trap** — centipawn vs pawn units. Thresholdy 0.5/0.3 misto 50/30. Pattern vzdy false. | HIGH |
| L6 | `test_prompt_contract.py` | cely | **Contract testy = integration** — vyzaduji Stockfish cache. Na cistem checkoutu vsechny failnou. | HIGH |
| L7 | `engine_client.py` | 30-36 | **get_engine() neni thread-safe** — dva soubezne volani pred inicializaci mohou spawnout dve instance. | HIGH |
| L8 | `engine_client.py` | 159-163 | **close_engine() nikdy volan** — Stockfish proces zustava viset. Orphan proces + memory leak. | HIGH |

### 1.2 Strední (MEDIUM)

| # | Soubor | Problem |
|---|--------|---------|
| M1 | `logger.py` | Module-level vedlejsi efekty (os.makedirs pri importu) |
| M2 | `game_llm_cache.py` | Neatomicky zapis cache (write-to-temp + rename chybi) |
| M3 | `game_llm_cache.py` | os.listdir bez try/except |
| M4 | `diagnostician.py` | phase_acpl[m.phase] muze hodit KeyError |
| M5 | `pattern_detector.py` | Deleni nulou (anon_blunder_rate / named_blunder_rate) |
| M6 | `match_patterns.py` | Dva sort() prepisuji prvni |
| M7 | `server.py` | Emoji v stderr outputu (porusuje encoding pravidla) |
| M8 | `engine_client.py` | Hardcodovane Windows cesty (C:\Program Files\...) |
| M9 | `llm_client.py` | DeepSeek Chat v PROVIDERS i kdyz je banned |
| M10 | `pyproject.toml` | Chybi pytest-asyncio v dev dependencies |
| M11 | `game_analyzer.py` | Hardcodovany CACHE_DIR |
| M12 | `pyproject.toml` | Ruff konfigurace prazdna (zadna select pravidla) |
| M13 | `kb/writer.py` | Encoding problem v nazvu adresare |
| M14 | `scripts/run_pipeline.py` | Sekvencni analyza (bez ThreadPoolExecutor) |
| M15 | `game_llm_cache.py` | Cache path hardcoduje depth 12 |

### 1.3 Nízké (LOW)

| # | Soubor | Problem |
|---|--------|---------|
| L01 | `engine_client.py` | Fallback "stockfish" je k nicemu |
| L02 | `pyproject.toml` | Nadbytecna zavislost openai |
| L03 | `pyproject.toml` | Nadbytecna zavislost fsrs |
| L04 | `pyproject.toml` | Chybi coverage v dev dependencies |
| L05 | `llm_client.py` | Hruby odhad completion tokenu |
| L06 | `match_patterns.py` + `diagnose_player.py` | Duplicitni kod analyze_one |
| L07 | `server.py` | verify_api_keys() zpomaluje startup |
| L08 | `llm_client.py` | Hardcodovany timeout 60s |
| L09 | `compressibility_validator.py` | PATTERN_BASE_COST = 10 arbitrarni |
| L10 | `tests/__init__.py` | Prazdny __init__.py |
| L11 | `README.md` | Uvadi 28 testu, realne 33 |
| L12 | `README.md` | Nekonzistentni pocet patternu (9 vs 17) |
| L13 | `README.md` + `README_en.md` | Chybi .env.example |
| L14 | `game_llm_cache.py` | _validate_json_output regex krehky |
| L15 | `.github/workflows/test.yml` | Ruff bez select = jen F pravidla |
| L16 | `engine_client.py` | Opakujici se ThreadPoolExecutor boilerplate |
| L17 | `lichess_client.py` | fetch_cloud_eval polyka Exception |

### 1.4 Stav testu

| Kategorie | Pocet | Pokryti |
|-----------|-------|---------|
| Unit (modely) | 15 | 100% |
| Contract (cache) | 13 | 1 modul |
| Engine mock | 5 | 1 modul |
| **Celkem** | **33** | **~20% modulu** |

**Moduly s 0 testy:** llm_client, lichess_client, game_analyzer, diagnostician, pattern_detector, srs_engine, logger, game_llm_cache, vsechny tools (9), resources (2), kb (3), app, server, scripts.

---

## 2. cnc-tools — detail

### 2.1 Kritické (HIGH)

| # | Soubor | Radky | Problem | Severity |
|---|--------|-------|---------|----------|
| C1 | `aci_lookup.py` | 103 | **Unicode replacement character** v source kodu (U+FFFD) | HIGH |
| C2 | `cross_repo_search.py` | 31-48 | **Anti-pattern: asyncio.run() v ThreadPoolExecutor** — nova event loop v kazdem vlakne | HIGH |
| C3 | `git_tools.py` | 44-51 | **Stejny anti-pattern: asyncio.new_event_loop()** — neefektivni, resource leak | HIGH |
| C4 | `vcf_validate.py` | 45 | **ACI substring match bug** — `str(1) in "ACI 10"` = True. False positive pro ACI 10, 11, 20+ | HIGH |
| C5 | `vcf_validate.py` | 35-36 | **Prazdna `known_acis` = vsechny ACI hlaseny jako neznamé** | HIGH |
| C6 | `kb_search.py` | 29, 56 | **Zadny limit na velikost souboru** — OOM pri multi-MB souborech | HIGH |
| C7 | `audit.py` | — | **Audit log nikdy nerotuje** — zaplneni disku | HIGH |
| C8 | `filesystem.py` | 89 | **rglob() nekontroluje zakazane patterny** na kazdem souboru | HIGH |

### 2.2 Strední (MEDIUM)

| # | Soubor | Problem |
|---|--------|---------|
| M1 | `config.py` | Hardcodovane absolutni cesty |
| M2 | `validate.py` | validate_path nekontroluje is_path_allowed |
| M3 | `validate.py` | Modul nema zadne testy |
| M4 | `audit.py` | Modul nema zadne testy |
| M5 | `server.py` | Zadne integration testy |
| M6 | `cross_repo_search.py` + `git_tools.py` | Duplicitni `_collect_repos()` |
| M7 | `pyproject.toml` | Chybi Ruff konfigurace |
| M8 | `pyproject.toml` | Chybi CI/CD (zadny .github/workflows/) |
| M9 | `README.md` | Nepresny pocet toolu (20 vs 21) |
| M10 | `README.md` | Nepresny pocet testu (67 vs 45) |
| M11 | `kb_by_module.py` | Krehke parsovani EROI metadat |
| M12 | `test_tools.py` | time.sleep(0.01) v testu = flaky |
| M13 | `server.py` | Nepresny type hint |
| M14 | `vcf_analyze.py` | MD5 z re-encoded stringu (ne raw bytes) |
| M15 | `re_pipeline.py` | time.time() misto time.monotonic() |

### 2.3 Nízké (LOW)

| # | Soubor | Problem |
|---|--------|---------|
| L01 | `session_state.py` | Mrtvy kod (TEMP_FILE.exists() po rename) |
| L02 | `audit.py` | Heuristika result_ok krehka (startswith "CHYBA") |
| L03 | `server.py` | Volani _load_workspace_context na module level |
| L04 | `aci_lookup.py` | Hardcodovane cesty k config.json |
| L05 | `tools/__init__.py` | Dead code (nikdo neimportuje) |
| L06 | `config.py` | _matches_forbidden_pattern nepodporuje complex globy |
| L07 | `vcf_validate.py` | Tool detekce nejednoznacna |
| L08 | `test_tools.py` | Test silently skipped pri chybejicim VCF souboru |
| L09 | `test_tools.py` | Stejny problem |
| L10 | `vcf_diff.py` | Redundantni identical check |
| L11 | `kb_search.py` | Duplicitni kod pro .md a .json |
| L12 | `server.py` | ensure_ascii=False problem s kodovanim |
| L13 | — | Chybi .gitignore pro .tmp soubory |

### 2.4 Stav testu

| Pocet testu | 45 |
|-------------|-----|
| Moduly s testy | 13/16 |
| Moduly s 0 testy | validate, audit, server |
| CI/CD | ZADNE — chybi .github/workflows/ |

---

## 3. Cross-repo srovnání

### Spolecné silné stránky
- Oba projekty: cista architektura, DDD-like vrstvy, FastMCP
- Obousmerne README s architekturou
- Bezpecnostni model (BLOCKLIST/ALLOWLIST v cnc-tools)

### Spolecné slabiny
- **API klice v repozitari** (lichess-analyzer .env, cnc-tools nema API ale muze mit)
- **Chybi CI/CD** (cnc-tools 0%, lichess-analyzer broken CI)
- **Nedostatecne testovani** (obe ~20% coverage)
- **README neni aktualni** (oba uvadi spatny pocet toolu/testu)
- **Hardcodovane cesty** (Windows-specific, neportabilni)
- **Encoding issues** (oba maji problem s cp1250/UTF-8 na Windows)
- **Ruff bez rules** (cnc-tools zcela bez, lichess-analyzer jen default)

### Rozdíly

| Aspekt | lichess-analyzer | cnc-tools |
|--------|------------------|-----------|
| CI/CD | Broken (existuje ale failne) | Neexistuje |
| Logicka chyba v detection | Pattern I thresholdy | ACI substring match |
| Thread safety | get_engine() race | asyncio.run() v thread poolu |
| Počet testu | 33 | 45 |
| Modulu s 0 testy | ~23 | 3 |
| Hlavni riziko | API klice v gitu | ACI false positives |

### Celkové cross-repo priority

1. **IMMEDIATE**: Rotovat API klice v lichess-analyzer, odstranit .env z historie
2. **HIGH**: Opravit ACI substring bug v cnc-tools (vcf_validate.py:45)
3. **HIGH**: Opravit CI v lichess-analyzer (contract tests na CI)
4. **HIGH**: Pridat CI/CD do cnc-tools (.github/workflows/test.yml)
5. **MEDIUM**: Opravit asyncio anti-pattern v cnc-tools
6. **MEDIUM**: Napsat testy pro validate.py, audit.py, server.py v cnc-tools
7. **MEDIUM**: Napsat testy pro llm_client, pattern_detector v lichess-analyzer
8. **MEDIUM**: Opravit thread-safety get_engine() v lichess-analyzer
9. **LOW**: Pridat Ruff rules do obou projektu
10. **LOW**: Pridat graceful shutdown (close_engine) v lichess-analyzer

---

## 4. Porovnání s auditem v1

| Metrika | v1 (2026-07-18) | v2 (2026-07-20) | Zmena |
|---------|-----------------|-----------------|-------|
| lichess-analyzer | 4.0/10 | 4.5/10 | +0.5 |
| cnc-tools | 4.5/10 | 4.0/10 | -0.5 |
| Testu celkem | 28+67=95 | 33+45=78 | -17 (cnc-tools README prehanel) |
| CI/CD | lichess: broken, cnc: none | lichess: broken, cnc: none | beze zmeny |
| API klice v gitu | neauditovano | LICHESS-ANALYZER: ANO | NOVY FINDING |

---

*Vygenerovano 2026-07-20 autorem outpost2026. Metodologie: full manual code review kazdého .py souboru + testu + configu.*
