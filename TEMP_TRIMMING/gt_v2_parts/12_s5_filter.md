## 5. Diagnostický filtr — 82 checkpointů

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
31. Je root logger konfigurován na FileHandler od startu (žádný logging.lastResort / implicitní StreamHandler stderr)? (P25, GT-089)

### K — async subprocess
32. Jsou vsechna subprocess volání async? (P26)
33. Mají git operace `stdin=DEVNULL`? (P26)
34. Je timeout ≤15s + `asyncio.wait_for`? (P26)
35. Jsou `cwd` a env parametry explicitní? (P26)

### L — Test pyramida
36. Existuje MCP integration test (tool → framework, bez STDIO)? (P27)
37. Existuje MCP E2E test (pres reálný STDIO)? (P27)
38. Bězí smoke test (`git_status` <5s) po kazdé zmene? (P27)
39. Jsou transport-level anomálie pokryty testy? (P27)

### M — Diagnostika / monitorování
40. Je `git log -5` promptnejsi nez `-20`?
41. Existuje `ping()` tool pro ověření, ze server zije?
42. Je MCP client timeout konfigurovatelný per-tool?
43. Je v logu timestamp + duration pro kazdý subprocess call?
44. Lze rozlišit "server mrtev" od "tool zpracovává"? (GT-089: timeouting poll = server frozen, ne běh jobu)

### N — Encoding & Console (rozsířeno)
45. Je PYTHONIOENCODING=utf-8? (P18, P23)
46. Má server `sys.stdout.reconfigure('utf-8')`? (P18)
47. Jsou emoji a Unicode supplementary zakázány v kódu? (P28)
48. Vrací tool ceské znaky bez chyby? (P23)

### O — Server initialization (P29)
49. Je main() sync `def main(): app.run()`? Nikdy `async` + `asyncio.run()` (P29)
50. Ma `.pth` soubor po `pip install -e .` project root + `src/`, ne jen `src/`? (P29)

### P — Pipeline consistency & cache governance (P50-P54)
51. Je parametr clamp explicitně signalizován warningem při ořezu? (P50)
52. Kontroluje tool před zpracováním pending count a varuje uživatele? (P51)
53. Je verze knihovny ověřena před použitím nového API parametru? (P52)
54. Je nový tool viditelný v `list_tools` po restartu serveru + opencode session? (P53)
55. Je nový pattern validován N>=30, ratio>=1.4, 2+ analýzami? (P54)

### Q — Engine & PV pipeline integrity (P55-P61)
56. Je každý `except` blok zalogován (ne silent pass)? (P55)
57. Jsou Stockfish PV multi-tahové sekvence konvertovány sekvenčně na kopii boardu? (P56, P59)
58. Reportuje každý run K0 metriky (depth, engine_version, Threads, Hash)? (P57)
59. Obsahuje cache klíč detector_version? Je version mismatch detekován při cache load? (P58)
60. Je engine lock dostatečně izolovaný proti error propagaci? (P60)
61. Je engine lines count pod multipv_target signalizován (truncated flag, warning)? (P61)
62. Existuje mechanismus pro re-analyzi při code change (cache invalidation)? (P58)

### R — Data correctness & contract evolution (P63-P68)
63. Jsou model pole čtená přes reálné atributy (`a.field`), ne `getattr(a, "x", default)`? (P63)
64. Je nový data klíč přidán additive (`.get(key, default)` + additive test), ne rozšířením povinného seznamu testovaného na živých datech? (P64)
65. Kvituje timeout/cleanup handler referenci, která volání spustila (lokální vs sdružený engine)? (P65)
66. Hlásí validace neimplementovaný vstup chybou (fail-fast), ne tichou substitucí? (P66)
67. Má degradace dat počitatelný marker (čítač + expozice v LLM promptu)? (P67)
68. Má pole legacy cache s prázdným defaultem guard před parserem (chess.Board(fen=""))? (P68)

### S — Filename nomenklatura (P69, ASCII-NOM)
69. Jsou všechny trackované názvy souborů/adresářů ASCII `[A-Za-z0-9._-]` (žádná diakritika, mezery, U+2011)? (P69) — ověř `.scripts/ascii_filenames_check.ps1`, exit 0
70. Neobsahuje žádný trackovaný soubor staré cesty/názvy po renames (broken reference)? — ověř `.scripts/context_refs_check.py`, exit 0 (kontrakt: GLOBAL_FORBIDDEN + REPO_FORBIDDEN rename mapa + F1_ALLOWLIST)

### T — Lint determinismus & long-running tools (P72, P13)

71. Je lint rule set deterministický — explicitní `[tool.ruff.lint] select`, NE defaultní sada driftující s verzí nástroje? Intencionální výjimky (graceful degradation, line-length) dokumentované v `ignore`, ne v kódu? (P72)
72. Je long-running tool (>10s) async — submit+poll (okamžitý `job_id` + status poll), nebo má explicitní progress streaming / CLI bypass? Client timeout config (např. opencode `timeout`) se nevztahuje na tool calls, jen na ListTools — timeout calls řeší pattern, ne zvětšení timeoutu. (P13)
73. Používají integrační testy izolovanou test DB (dedikovaná databáze/schéma/transakce s rollbackem), ne sdílenou produkční/dev DB? Neobsahuje žádný test fixture destruktivní `TRUNCATE`/`DROP`/`DELETE` proti datům, která test nevytvořil? (P73)

### U — Dedup & anti-bot integrita scrapingu (P74-P77)

74. Jsou tracking/session parametry (`searchId`, `rps`, `search_id`, `utm_*`) odstraněny z URL v centrálním bodě (`Ad.__post_init__`), ne per-provider? Kanonický URL je stabilní napříč běhy (UNIQUE dedup funguje)? (P74)
75. Je cross-portal dedup DB-level (fuzzy sloupce + index) se sdíleným normalizovaným klíčem (NFKD diakritika, en/em-dash→hyphen) mezi pipeline a DB? Má deterministickou prioritu vítěze (bohatost dat, tie-break first-seen)? Používá batched lookup (1 round-trip), ne per-ad SELECT? (P75)
76. Je deterministická anti-bot/consent-page blokace ověřena live testem (5/5 reprodukce) a fixnuta per-portal header variantou (UA+Accept kombinace), ne univerzálním UA? (P76)
77. Loguje stránka s 0 kartami ERROR jen pro page 1 (layout change), a pro page > 1 INFO (end-of-list)? Přijímá `parse_listings` page kontext a `scrape_all` ho předává? (P77)

### V — GCP Infrastructure & Serverless (P-GCP-01..05)

78. Při 403 v GCP: ověřeno všech 5 autentizačních vrstev (IAM role, Access Scopes, Metadata Server, Workspace/Cloud, SA quota)? Nejčastější příčina: Access Scopes nebo Workspace/Cloud mismatch. (P-GCP-01)
79. Crontab na GCP VM: absolutní cesty ke všemu (Python, binárky, adresáře)? sudo s NOPASSWD v sudoers.d? GCP region = správný (ne default)? (P-GCP-02)
80. Serverless immutable: každá změna = `gcloud deploy`, ne hotfix za běhu? `Ctrl+S` = změna lokální kopie, ne deploy. (P-GCP-03)
81. GCP Cloud Functions: `/tmp/` = RAM, po doběhu smaže vše. Start = download z GCS, konec = upload. Žádná trvalá paměť v kontejneru. (P-GCP-04)
82. Při zacyklení v chybách >30 minut: proveden Hard Reset (smazat poškozený soubor → ověřený blok → smazat data → začít z nuly)? Reset = optimalizace, ne prohra. (P-GCP-05)

