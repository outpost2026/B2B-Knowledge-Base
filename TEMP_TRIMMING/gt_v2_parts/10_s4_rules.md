## 4. Průřezová pravidla P1–P96 + P-GCP-01..05 (kanon; P84–P89 rezervovány epistemické řadě)

### P1 — Paralelizace
Jakmile tool iteruje N>1 nezávislých zdrojů (repozitáře, soubory, API), použij `ThreadPoolExecutor`. Počet workerů: min(4, N). I/O-bound operace skálují lineárne do ~8 vláken.

### P2 — Časové konstanty
Subprocess timeout v MCP toolu musí být max 25% MCP client timeoutu. Client timeout 60s → subprocess timeout 15s. Fail fast, fail loud.

### P3 — Read-only locky
Kazdý read-only subprocess call (git, grep, diff) používej `["git", "--no-optional-locks"]`. Eliminuje filesystem lock contention.

### P4 — JSON defenziva
Kazdý JSON state deserializer: `try/except` + `isinstance(v, dict)` guard + auto-repair. Počítej s corrupt daty.

### P5 — Diagnostika
`@auditable` na kazdém toolu. Povinné: `ts`, `tool`, `duration_s`, `ok`. Bez metriky není diagnostika.

### P6 — Timeout guard
I/O tool s potenciálem >10s → wrapper s `concurrent.futures.TimeoutError`.

### P7 — Globální proměnné
Kazdá funkce, která zapisuje do modulové globální proměnné, musí mít `global jméno`. Python bez `global` vytvorí lokální shadow — tichá ztráta dat.

### P8 — Pořadí operací
Auth/navigace/destruktivní operace: auth first, navigace second. Nic mezi ně nevkládat.

### P9 — Žádné CSS třídy v selektorech
Používej sémantické HTML atributy (`href`, `aria-label`, `role`). CSS třídy jsou ephemeral — A/B testy je mení bez varování.

### P10 — Verifikace cest
`Path.parents` je 0-indexovaný od nejbližšího rodice. Ověř `relative_to()` pred prvním pouzitím.

### P11 — Console script distribution
Po `uv sync` vzdy explicitně ověř, z ekonzolový script je dostupný:
```bash
.venv/Scripts/<tool> --help   # musí fungovat
where <tool>                   # musí najít exe
```
Pokud `where` selze → pridej `.venv/Scripts` do PATH nebo vytvor `.bat` wrapper.

### P12 — Cross-shell launcher
Kazdý CLI nástroj na Windows musí mít `.bat` wrapper v repo root:
```batch
@echo off
"%~dp0.venv\Scripts\<tool>.exe" %*
```

### P13 — Long-running batch operations
MCP tool, který iteruje N>10 I/O operací, musí být buď:
1. Asynchronní s progress streamingem (MCP `ctx.info()`), nebo
2. Nahrazen CLI entry pointem, který obchází MCP transport timeout, nebo
3. **Async submit+poll pattern** (GT-087): tool vrátí okamžitě `{job_id}`, práce běží v `ThreadPoolExecutor` na pozadí, klient polluje `search_status(job_id)` → `{status, elapsed_s, result}`. Jediná varianta, která drží produkční deliverable **bez CLI**.

Současně: client timeout config (např. opencode `timeout` v `opencode.jsonc`) se vztahuje na **ListTools (fetching tools), NE na tool calls** — konfigurovaný timeout nechrání long-running calls; řešení je P13 pattern, ne zvětšení timeoutu (GT-087).

**Varování (GT-089):** submit+poll NEchrání před stderr deadlockem — pokud timeouting `search_status`/`health_check` (ne jen submit), je server frozen (stderr pipe full, lastResort/StreamHandler), ne job běžící; root logger MUSÍ být na FileHandler (P25).

### P14 — Windows path quoting
- Vzdy `pathlib.Path` (nikdy string concatenation)
- Pri predání cesty subprocessu: `str(resolved_path)` + explicitní quoting
- Testuj cesty v cmd.exe, PowerShell i Git Bash
- `_github\` prefix ~70 chars → riziko MAX_PATH (260 chars)

### P15 — Session monitoring
Pred kazdým pipeline runem: (1) `is_logged_in()` + log `page.url`, (2) pokud auth selze, loguj response body (může být checkpoint), (3) `--login` flow bez restartu MCP serveru.

### P16 — PowerShell v bash = piš .ps1 soubor
Nikdy nevkládej PowerShell one-linery do bash stringů. Vzdy: napiš `.ps1` script, spust pres `powershell -File scripts/operace.ps1`.

### P17 — Workspace context export
Kazdý MCP server pro LLM agenty musí:
1. Při startu vypsat workspace root do stderr: `print(f"[server] Workspace root: {root}", file=sys.stderr)`
2. Poskytnout `tool_workspace_info()` vracející root, guardrails profil, index summary
3. Kontextové soubory prednačíst do cache pri startu

### P18 — Console encoding na Windows (Unicode safety)
1. `$env:PYTHONIOENCODING='utf-8'` pred kazdým python príkazem
2. `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` v startupu
3. Emoji zakázána v kódu (.ai_guardrails.json)

### P19 — Structured logging v scrape path
Kazdý scrape modul musí mít: per-card `logger.warning()`, skip counter, 0-ads `logger.error()` alert.

### P20 — ETL health check / session-start protocol
Kazdý MCP server s externími zdroji musí mít: ETL runner + session-start health check + alert threshold (>20% pokles matched ads).

### P21 — L2 Resources (URI-adresovatelná data)
Tool vyrobí data jednou, resource je zpřístupňuje opakovaně. URI schema: `server://{namespace}/{id}`.

### P22 — Windows PowerShell: nikdy `python -c` s komplexním kódem
`python -c "..."` s f-stringy, vnorenými uvozovkami, cykly je křehký. Root cause: Windows API `CommandLineToArgvW` delí argument na mezerách.

### P23 — Windows encoding: PYTHONIOENCODING + PYTHONUTF8 + -X utf8
Tri úrovne ochrany: (1) shell-level env var, (2) process-level `-X utf8`, (3) code-level `sys.stdout.reconfigure()`.

### P24 — Python version audit
- Nikdy pre-release Python (< stable) pro MCP servery
- `requires-python = ">=3.12.0,!=3.11.0rc1,!=3.11.0rc2"` v pyproject.toml
- Version check pri startu serveru

### P25 — stderr hygiene
- Nikdy StreamHandler(sys.stderr) v MCP serveru
- Logovat jen do FileHandler nebo rotating file
- Audit log = file-based, ne stderr-based
- Rozšířeno (GT-089): zákaz platí i pro IMPLICITNÍ cesty na stderr — `logging.lastResort` (root logger bez konfigurace = implicitní StreamHandler stderr) a `print(file=sys.stderr)`. Root logger MUSÍ být konfigurován na FileHandler od prvního startu: `logging.basicConfig(filename=..., level=..., force=True)`. Startup stderr printy max. 1 krátký řádek (P17).

### P26 — asyncio subprocess
- Vsechna I/O v MCP tools pres `asyncio.create_subprocess_exec()`
- `stdin=asyncio.subprocess.DEVNULL` pro git operace
- `asyncio.wait_for(proc.communicate(), timeout=15)` pro fail-fast
- Vzdy `cwd=` explicitně
- `subprocess.run` zakázán v MCP tools

### P27 — MCP test pyramida
1. Unit vrstva — testy logiky jednotlivých nástrojů
2. Integration vrstva — testy MCP request/response (pres FastMCP.call_tool)
3. E2E vrstva — testy pres reálný STDIO transport
4. Smoke test po kazdé změně: `git_status(B2B-Knowledge-Base)` <5s

### P28 — Encoding audit v CI
Kazdý build musí kontrolovat, ze zdrojové soubory neobsahují emoji:
```bash
rg "[\u2600-\u27BF\U0001F000-\U0001FFFF]" src/
```

### P29 — FastMCP main() sync, nikdy async wrapper
`app.run()` (FastMCP) interně volá `anyio.run()` = spoustí vlastní event loop. main() musí byt sync:

```python
# SPRAVNE
def main():
    app.run()

if __name__ == "__main__":
    main()

# CHYBNE — RuntimeError: Already running asyncio
async def main():
    await app.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Rozsireni:** Po `pip install -e .` se `src` layoutem over `.pth` obsahuje project root, nejen `src/`.

### P30 — LLM response format fallback
`data["choices"][0]["message"]["content"]` není univerzální. Cerebras pouzívá `reasoning` místo `content`. Pouzívat `msg.get("content") or msg.get("reasoning")`.

### P31 — LLM max_tokens pro coaching
Coaching pipeline s 6+ patterny a 5 sekcemi vyzaduje `max_tokens >= 4000`. Default 2000 testovat na reprezentativním vzorku.

### P32 — Cascade status exposure
Cascade fallback musí expose per-provider status (attempted/skipped/error + tokens + cost) do výstupu. Nikdy netlacit stav provideru.

### P33 — Data format change consistency
Po zmene datového formatu aktualizovat VŠECHNY konzumenty. Testovat s reprezentativními daty, ne jen unit testy.

### P34 — Cache schema versioning
Cache/export JSON schema explicitne dokumentovat a verze kontrolovat. Konzumenti pouzívat fallback chain pres `.get()`.

### P35 — Deterministické kroky cacheovat
Stockfish analyza (deterministická) cacheovat pres `game_id + depth`. LLM inference ne — kazdý běh = nová odpoved.

### P36 — Provider model ID overení
Vzdy volat `/v1/models` API pro discovery. Docs a UI jsou nespolehlivé. Testovat s minimálním promptem.

### P37 — Cost/benefit provider governance
Kazdý provider v LLM cascade musí mít explicitní cost schválení. Drazsí alternativy (>2× cena za stejnou kvalitu) blokovat.

### P38 — SNR evaluation framework
Porovnání LLM výstupu: vzdy pouzít SNR framework (grounding 30%, confidence 20%, phase data 15%, hallucinations 20%, structure 10%, concreteness 5%).

### P39 — Multi-API key management
`.env` pro lokální vývoj, `auth.json` pro opencode, `.gitignore` pro oba. Kazdý provider muze mít jiný key management (free vs paid, shared vs dedicated).

### P40 — Env var warning na suboptimal values
Env var s dopadem na kvalitu musí logovat varování pri hodnotách pod doporuceným minimem. Příklad: `LLM_MAX_TOKENS=2000` → warning "recommended >=4000".

### P41 — Dvouúrovnová LLM cache (Level 2)
Per-game LLM analyzu cacheovat do `{game_id}_llm.json`. Agregace pouzívá summaries z cache místo raw dat. Nová hra = 1 L2 call + 1 agregace, ne full re-run. **Aktualizace (v8):** u multi-perspektiva pipeline (dual-cache white+black) MUSÍ klíc obsahovat perspektivu — `{game_id}_{color}_llm.json`. Jinak oba pohledy sdílí soubor a last-writer-wins prepluje opacnou perspektivu. Reference: GT-079.

### P42 — Cascade resilience
Timeout nebo error jednoho providera v cascade nesmí blokovat pipeline. Cascade je resilience pattern — dalsí provider v poradí prevezme.

### P43 — Pipeline mode (monolit vs inkrementalni)
N≤30 → monolit (1 LLM call). N>30 → inkrementalni (per-game cache + aggregate). Golden rules: rychlá analýza = monolit, hromadná / PGN import = inkrementalni. Explicitní override pres `PIPELINE_MODE` env var.

### P44 — Contract testy mezi moduly (Consumer-Driven Contract)
Kazdy modul v pipeline (Stockfish analyzer → prompt builder → LLM) musi mit contract test, ktery overuje konzistenci klícu mezi producerem a consumerem. Consumer definuje kontrakt (jake klíce potrebuje). Test je schema test na realnych datech + placeholder detection. Profesionalni nastroj: Pact. Lightweight varianta: `assert key in data` + `assert "?" not in prompt`. Reference: `01_METODIKY/05_testing/contract_testing_ontologie_v1.md`.

### P45 — API key health check pri startupu
`verify_api_keys()` v `server.py`. Lightweight ping (max_tokens=1, timeout=10s, per-provider). Detekuje neplatny/vyprseny/rate-limited klic pred prvnim tool volanim. Fail fast. Reference: GT-060.

### P46 — Classification branches must be mutually exclusive
Kazda kategorie v if/elif chainu musi mit vlastni append target. Spolecny cil = tichy data corruption. Unit test overuje, ze zadne dve kategorie nesdileji stejny cil. Reference: GT-061.

### P47 — Cross-LLM audit gate
Pred major release: v1 twin scan (architektura, struktura, bez kodu) + v2 code review (implementace, verifikace). Ani jedna faze nestaci sama. Reference: GT-062.

### P48 — Pattern confidence weighted by sample size
`confidence = min(0.95, base * (1 - 1/(N+1))) * evidence_factor`. Minimal sample N >= 5. Hardcoded confidence neodrazi silu evidence. Reference: GT-063.

### P49 — Sanitize user-supplied identifiers before filesystem use
`re.sub(r'[^a-zA-Z0-9_-]', '_', value)` na vsech vstupech (game_id, username, job_id) pred konstrukci File Path. Zaden user input nesmi byt primo segment v ceste. Reference: GT-065.

### P50 — Parametr clamp musí být signalizován
Pokud clamp (max/min) implicitně ořezává uživatelský vstup, musí logovat warning: `f"[clamp] {param}={value} clamped to {clamped}"`. Tichý ořez = nekonzistentní chování. Reference: GT-066.

### P51 — Pending analysis warning
Každý tool závislý na per-game cache musí před zpracováním zkontrolovat pending count a varovat uživatele. Struktura: cache-first → pending warning → processing → výsledek. Reference: GT-067.

### P52 — Ověř parametr knihovny před použitím
`pip show <library> | grep Version` před použitím nového API parametru. API dokumentace Lichess a berserk dokumentace mohou být desynchronizované. Reference: GT-068.

### P53 — MCP tool list je initialize snapshot
Po přidání nového toolu: (1) restart MCP server, (2) restart opencode session, (3) ověř v `list_tools`. Tool list se neaktualizuje za běhu. Reference: GT-069.

### P54 — Pattern discovery validace
Nový pattern musí být validován: (a) N >= 30 pro statistickou signifikanci, (b) ratio >= 1.4 pro praktickou relevanti, (c) potvrzen v 2+ nezávislých analýzách. Reference: GT-070.

### P55 — Silent except je bug
Každý `except Exception: pass` je bug unless proven otherwise. Silent excepty musí být zalogovány. Reference: GT-071.

### P56 — Stockfish PV SAN konverze
Stockfish PV multi-tahové sekvence musí být konvertovány do SAN sekvenčně na kopii boardu. `board.san(m)` validuje proti aktuální pozici, ne proti rootu. Reference: GT-071, GT-075.

### P57 — K0 noise channel
K0 (orákulum/engine) je samostatný noise channel. Každý run reportuje: depth, engine_version, Threads, Hash, nps_benchmark. ACPL z různých depth nejsou srovnatelné bez K0 korekce. Reference: GT-072.

### P58 — Cache version governance
Cache klíč musí obsahovat verzi kódu (`detector_version`). Při cache load: version mismatch → log warning → re-analyze. Nikdy nepoužívat stale cache po code change. Reference: GT-074.

### P59 — PV jsou sekvenční variace
Stockfish PV v multi-PV módu jsou sekvenční variace, ne paralelní alternativy. Každý PV tah aplikovat na kopii boardu. Nikdy nevalidovat N-tý PV tah proti root pozici. Reference: GT-075.

### P60 — Engine lock isolation
Engine lock vytváří coupling mezi analysis call. Exception uvnitř lock bloku může korumpovat stav engine pro následující volání. Mitigace: (a) žádné AssertionError uvnitř locku, (b) engine restart při timeout locku. Reference: GT-076.

### P61 — Truncated engine lines signalizace
Engine lines count pod multipv_target musí být signalizován. Flag `truncated` a `logger.warning()` per BFS. Reference: GT-077.

### P62 — Ruff --fix je destruktivní, side-effect importy s noqa
Ruff `--fix` maže side-effect importy (F401 unused import) — u registračního patternu `@app.tool()` to ruší registrace toolů. Side-effect importy MUSÍ mít `# noqa: F401` per line. Po každém `ruff --fix`: povinně `git diff` + registrační smoke check (`app._tool_manager._tools` count). Pytest destruktivní smazání registrace nezachytí. Doplnění (GT-081): ruff v automatizaci (CI) běží jako `--check` (read-only) — kontrola. `--fix` je **lidská** operace s `git diff` review — mutace. Separace kontroly od mutace je povinná; `--fix` nikdy do CI gate. Reference: GT-078, GT-081.

### P63 — getattr s defaultem maskuje neexistující atributy
`getattr(obj, "neexistujici", default)` vrací default **bez jakékoli signalizace** — u LLM input pipeline to znamená 100 % garbage v promptu (detekováno na `opening_report`, `opponent_pool`: `opening_name`, `player_color`, `acpl`, `result`). Model pole MUSÍ být čtená přes reálné atributy (`a.game.opening`, `a.total_acpl`) — pak neexistující atribut vyhodí AttributeError při testech. Jestliže default je nutný: logovat warning při použití. Reference: GT-079.

### P64 — Contract evoluce na živých datech je additive
Rozšíření povinného klíčového seznamu contract testu, který iteruje REÁLNÁ cache data, zlomí běh na starších souborech (149× cache bez nového klíče). Nový data klíč = (a) additive test `assert data.get(key, default)` MÍSTO rozšíření `PROMPT_TOP_LEVEL_KEYS`, (b) `.get(key, default)` v deserializaci — ne KeyError. Evoluce contractu nikdy nesmí vynutit migraci legacy dat. Reference: GT-079.

### P65 — Timeout cleanup cílí referenci, která volala
`evaluate_move` používá LOKÁLNÍ engine (vlastní instance), ale timeout handler kvitil sdružený `_engine` → kolaterální zabití konkurující analýzy + zbytečný restart. Cleanup funkce MUSÍ přijmout referenci (`_run_engine_call(fn, timeout_s, engine=None)`) a zabít právě ten objekt, který volání spustil. Reference: GT-079.

### P66 — Fail-fast nad tichou substitucí
Validace nemá akceptovat hodnotu, kterou implementace neumí, a nahradit ji substitucí — hlásí neimplementovaný vstup chybou (`source='chesscom' → error dict`). Tichá substituce = klidná špatná data. Výjimka: degradace s markerem (P67). Reference: GT-079.

### P67 — Degradace dat potřebuje počitatelný marker
`except Exception: pass` + `cp_loss = 0` při selhání evaluate_move klasifikovalo chybný tah jako "best" → ACPL systematicky optimistický bez indikace. Degradace MUSÍ být (a) spočítaná (`GameAnalysis.evaluation_errors` čítač, error dict i výjimka → +1), (b) vystavená do LLM promptu (`Eval errors: N (ACPL may be optimistic)`). Rozšíření P55 (log) o měřitelnou expozici. Reference: GT-079.

### P68 — Legacy cache pole s defaultem má guard před parserem
Starší cache soubory mají pole s prázdným/default defaultem (`m.fen=""`) → `chess.Board(fen="")` vyhodí ValueError a zhrotí celou detekci. Pole, které parser zpracovává, musí mít guard na prázdnou hodnotu (`and m.fen`), konzistentní napříč všemi detekčními funkcemi. Reference: GT-079.

### P69 — Názvy souborů/adresářů jen ASCII (konvence ASCII-NOM)
Názvy souborů a adresářů povolují POUZE `[A-Za-z0-9._-]` — žádná diakritika, mezery, ani non-breaking hyphen (U+2011). Obsah souborů zůstává UTF-8 s diakritikou (konvence platí pro názvy, ne obsah). Důvod: ne-ASCII názvy (a) generují mojibake v git objektech (cp1250 vs UTF-8 — GT-080), (b) U+2011 je vizuálně identický s `-` ale jiný codepoint → rozbíjí copy-paste/grep/RAG, (c) cyklický encoding dluh. Transliterace: `Normalize(FormD)` + drop NonSpacingMark, mezera→`_`, U+2011→`-`, ostatní ne-ASCII→`_`. Ověření: `.scripts/ascii_filenames_check.ps1` (exit 0 = OK). Reference: GT-080.

### P70 — Scraping pipeline s detail fetch = 3 fáze
(1) Collect unikátních URL přes všechny query (set pro dedup), (2) parallel fetch s per-portal throttle (ThreadPoolExecutor, max_workers=4), (3) filter nad naplněnou cache. Sekvenční detail fetch = bottleneck, který eskaluje lineárně s počtem matched ads. Reference: GT-083.

### P71 — Cache failure sentinel: 3 stavy (nezkoušeno / úspěch / selhalo)
Cache pro výsledky s možným selháním MUSÍ rozlišovat 3 stavy: (1) nezkoušeno (`None`/absence klíče), (2) úspěch (hodnota), (3) selhalo (sentinel `_FAILED = object()`). Bez sentinelu = opětovné fetch pokusy pro permanentně selhané URL. Reference: GT-085.

### P72 — Lint rule set je součást dependency kontraktu
Bez explicitního `[tool.ruff.lint] select` driftuje rule set s verzí nástroje (ruff>=0.6 bez horní hranice → nová default pravidla → CI fail bez změny kódu). Deterministický `select` (stabilní E4/E7/E9/F + explicitně vybraná moderní pravidla) = single source of truth; intencionální výjimky (BLE001 graceful degradation, E501 design trade-off) se dokumentují v `ignore`, ne v kódu. Komplement GT-081. Reference: GT-086.

### P73 — Test izolace: žádné destruktivní operace proti sdílené DB
Testy NESMÍ destruktivně zasahovat do dat, která sama nevytvořily. `TRUNCATE`/`DROP`/`DELETE` v test fixture je povolen POUZE proti izolované test DB (dedikovaná databáze/schéma/transakce s rollbackem). Společná `DATABASE_URL` pro testy a produkci/dev = kritická chyba (vysoká pravděpodobnost destrukce). Reference: GT-088.

### P74 — Tracking/session parametry NESMÍ být součástí dedup klíče
Scrape URL často obsahují session/tracking parametry, které se mění každý běh: jobs.cz `searchId=<UUID>`, prace.cz `rps=<int>`, profesia `search_id`, `utm_*`. UNIQUE(url) pak nechytí duplicity stejného inzerátu (52 duplicit / 20 skupin v live DB). Stripping patří do **centrálního bodu** (`Ad.__post_init__` / `normalize_url`), ne do per-provider kódu — per-provider řešení drifuje (profesia měla `_clean_detail_url`, jobs/pracecz žádný). Zachovat ostatní query parametry (`page`, sort), odstranit jen tracking. Reference: GT-090.

### P75 — Cross-portal dedup: sdílený fuzzy klíč + DB enforcement + deterministická priorita
Stejný inzerát je cross-publikovaný napříč portály (LMC network: jobs.cz+prace.cz, ManpowerGroup: jenprace+profesia). In-memory dedup nestačí napříč běhy. Vyžaduje: (a) **sdílený normalizovaný fuzzy klíč** (lowercase → NFKD strip diakritiky → en/em-dash→hyphen → kolaps whitespace) mezi pipeline `_dedup` i DB `upsert_ads` — jinak divergence; (b) **DB-level enforcement** (fuzzy sloupce + index, batched lookup `unnest(%s::text[])` = 1 round-trip, ne per-ad SELECT); (c) **deterministickou prioritu vítěze** — bohatost dat (description > salary > company > location), tie-break first-seen (existující radka si podrží URL+portal, bez churn), nikoli hardcoded portál ranking. Reference: GT-091.

### P76 — Anti-bot/consent-page detekce je kombinace hlaviček, ne samotný UA
Bot-detekce (Seznam.cz) reaguje na kombinaci `User-Agent` + `Accept` hlavičky — default HttpClient s UA Chrome/120 + Accept deterministicky vrací consent page (5/5 reprodukce). Fix = per-portal header varianta (UA Chrome/126 BEZ Accept) aplikovaná v `__init__` providera, respektující mockeri. Default HttpClient NEJEDNÁ jako univerzální řešení pro všechny portály. Deterministickou blokaci vždy ověř live testem (5/5), ne předpokladem. Reference: GT-092.

### P77 — 0 karet na stránce N>1 = end-of-list (INFO), ne layout change (ERROR)
`parse_listings` logoval ERROR "container selector returned 0 cards — likely broken" pro libovolnou stránku. False-positive: config `pages` (10) > reálný počet stránek (profesia Praha = 8) → trailing stránky existují s 200 OK a normálním title, ale 0 karet = za koncem seznamu. Rozlišení podle page kontextu: **page 1 + 0 karet = ERROR** (reálný layout change/blok), **page > 1 + 0 karet = INFO** "end of listing reached, stopping". `parse_listings` přijímá `page` parametr (default 1, abstraktní signatura v base.py), `scrape_all` předává aktuální stránku. Není to chyba v datech — je to normální ukončení paginace. Reference: GT-094.

