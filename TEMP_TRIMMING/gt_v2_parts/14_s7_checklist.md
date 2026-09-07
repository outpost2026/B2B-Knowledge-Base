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
47. **Test izolace** (P73) — integracni testy proti dedikovane test DB (databaze/schema/transakce s rollbackem), nikdy TRUNCATE/DROP/DELETE proti sdilene produkci/dev DB; sdilena DATABASE_URL testu a produkce = kriticka chyba
48. **URL canonicalizace** (P74) — tracking/session parametry (searchId, rps, search_id, utm_*) odstraneny v centralnim bode Ad.__post_init__; kanonicky URL = dedup klic, per-provider cleanup zakazan (drift)
49. **DB-level cross-portal dedup** (P75) — sdileny normalizovany fuzzy klic (NFKD + dash→hyphen) mezi pipeline a DB, fuzzy sloupce + index, batched lookup, priorita vitez dle bohatosti dat (description>salary>company>location), tie-break first-seen
50. **Anti-bot per-portal headers** (P76) — deterministicka anti-bot/consent blokace (UA+Accept kombinace) overena live testem (5/5), fix per-portal header variantou v __init__ providera
51. **End-of-list vs layout change** (P77) — 0 karet na strance page>1 = INFO end-of-list (config `pages` > realny pocet stranek), ERROR jen pro page 1. `parse_listings` prijima `page` kontext (default 1), `scrape_all` ho predava. Reference: GT-094.
52. **GCP 5vrstvá autentizace** (P-GCP-01) — při 403 v GCP ověřit 5 vrstev: IAM role, Access Scopes, Metadata Server, Workspace/Cloud, SA quota. Nejčastější: Access Scopes nebo Workspace/Cloud mismatch. Source: GT-GCP-001.
53. **Cron ≠ SSH** (P-GCP-02) — crontab na GCP VM = absolutní cesty, sudo s NOPASSWD v sudoers.d, GCP region explicitní (ne default). Source: GT-GCP-002.
54. **Serverless immutable** (P-GCP-03) — Cloud Function = neměnný kontejnerový otisk. Ctrl+S = lokální kopie. Oprava = gcloud deploy. Source: GT-GCP-003.
55. **GCS je jediná trvalá paměť** (P-GCP-04) — Cloud Functions /tmp/ = RAM, po doběhu smaže vše. Start = download z GCS, konec = upload. Source: GT-GCP-004.
56. **Hard Reset protokol** (P-GCP-05) — při zacyklení >30 minut: smazat poškozený soubor, vložit ověřený blok, smazat data, začít z nuly. Source: GT-GCP-005.
57. **Unicode-aware regex** (P80) — při parsování textových dat s regionálními formáty: otestovat regex proti reálným datům VCETNE Unicode variací (en-dash U+2013, non-breaking space U+00A0, různé quote znaky). Nikdy nepředpokládat ASCII-only vstup v multilingual scraping pipeline. En-dash a hyphen-minus vypadají identicky — vizuální kontrola nepomůže, nutný DB audit. Source: GT-095.
58. **Cross-portal dedup: title+company, ne URL** (P81) — cross-portal analytika: nikdy nepoužívat URL jako dedup klíč napříč portály (každý portál má unikátní URL schéma). Používat title+company (nebo fuzzy_title+fuzzy_company) jako dedup signál. URL-based dedup funguje jen uvnitř jednoho portálu. Source: GT-096.
59. **Modular dependency injection** (P82) — při refactoru na balíčky: žádné vzájemné importy mezi moduly. Závislosti se předávají jako parametry. Vzor: `tabs/*.py` importuje `metrics`, `filters`, `components`, nikdy `app.py`. Source: GT-097.
60. **Contract tests mandatory při splitu** (P83) — při refactoru na balíčky: contract testy součástí kroku 4 (package split), ne backlog. Povinné: purity (zakázané importy), interface (signatury), layers (směry importů). Source: GT-098.
61. **Frontend smoke test gate** (P90) — UI layout změny kolem `st.dataframe(on_select)` ověřovat ručním během; pytest nerenderuje frontend. Znovu-povolení odstraněného triggeru bez reprodukce = reintrodukce. Source: GT-099.
62. **Print-before-raise defense** (P91) — API s warning-before-exception side efektem neověřovat dotykem+try/except; ověřit stav přímo (existence souboru). Source: GT-100.
63. **Single dependency source of truth** (P92) — pyproject = kontrakt, requirements/deploy = synchronizované deriváty; po version bump `pip install -e .`; `pip check` ve verification gate. Source: GT-101.
64. **Package-data build verification** (P93) — data soubory deklarovány v package-data + ověřeny wheel namelist inspekcí; broad-except bez logování maskuje totální rozpad. Source: GT-102.
65. **Structural dispatch over name matching** (P94) — dispatcher rodiny funkcí váže pozicí/arity, ne názvy parametrů; runtime smoke test celé rodiny. Source: GT-103.
66. **Framework logger direct attach** (P95) — loggery s propagate=False potřebují handler přímo na uzlu; setup v render cyklu idempotentní (guard flag). Source: GT-104.
67. **No live I/O in unit tests** (P96) — async/background cesty stubovat monkeypatchem; flaky = determinismus bug; 2 zelená pásma = minimum gate. Source: GT-105.

