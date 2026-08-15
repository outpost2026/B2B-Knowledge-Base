# SWE Glossary — živá učebnice terminologie pro juniorního deva
**Datum:** 2026-08-15 | **Autor:** outpost2026
**Účel:** Živý edukační dokument — vysvětluje terminologii SWE, kterou dev zaznamenal při LLM-asistovaném solo vývoji (anti-blackbox paradigma). Průběžně doplňovaný.
**Typ:** edu / ontologie | **Doména:** SWE terminologie, koncepty, ontologie | **EROI:** 9/10

> **Jak tento dokument funguje (návod pro čtenáře = autora):**
> - Každý termín má strukturu **CO / PROČ / JAK / EFEKT (EROI)** — pochop logiku, ne jen definici.
> - Termín je vysvětlen v kontextu, ve kterém ses s ním reálně setkal (kontexty z dev workflow).
> - Tento dokument je **živý** — nové termíny se doplňují průběžně, jak na ně narazíš.
> - Cíl: přeměnit *unknown unknowns* na *known unknowns* → pak na *known knowns*.
>
> **Metoda adopce:** terminologie není seznam slov k nabiflování, ale **ontologie** — mapa vztahů mezi pojmy. Pochopíš-li vztah (např. proč race condition vzniká právě u sdíleného stavu ve vláknech), termín si zapamatuješ navždy.

---

## OBSAH

1. [Concurrency & Threading](#1-concurrency--threading) — serializace, race condition, zombie thread, ThreadPoolExecutor, lock/acquire, deadlock
2. [Caching & Data](#2-caching--data) — cache invalidation, TTL, atomický zápis, lazy loading
3. [Python Ekosystém & Tooling](#3-python-ekosystem--tooling) — uv, pyproject.toml, ruff, grep, statický vs runtime
4. [Testing](#4-testing) — mock, MagicMock, unit test, dead code
5. [Web Scraping & HTML](#5-web-scraping--html) — DOM, CSS selector, hashed CSS module, lazy fetch
6. [Data Processing & Matching](#6-data-processing--matching) — dedup, fuzzy matching
7. [Text & Unicode](#7-text--unicode) — hyphen, non-breaking hyphen, escapy
8. [Core Concepts](#8-core-concepts) — idempotence, synchronní vs asynchronní, guardrail

---

## 1. Concurrency & Threading

> **Kontext vzniku:** MCP lichess-analyzer pipeline — 4 paralelní hry frontovaly za lock → MCP timeout → zombie thread → deadlock. 3 bugy se sečetly. Tohle je reálný případ, kdy špatné pochopení vláken rozbilo produkční nástroj.

### 1.1 serializuje (serialize) — serializace přístupu

**CO:** Znamená "udělat ze souběžného něco sekvenčního" — vynutit, aby operace probíhaly **jedna po druhé**, ne paralelně. `_analysis_lock = threading.Lock()` **serializuje** všechny `engine.analyse()` cally napříč vlákny — v daný okamžik může engine analyzovat jen jedno vlákno.

**PROČ:** Engine (Stockfish přes UCI) **není thread-safe**. Dvě vlákna volající engine současně = poškozený komunikační protokol (UCI corrupt). Lock zajistí, že druhé vlákno počká, dokud první neskončí.

**JAK (analogie):** Jedna toaleta, fronta lidí. Lock = zámek na dveře. Když je uvnitř někdo, ostatní čekají venku. Nemůžou být dva v toaletě najednou.

**EFEKT (EROI):** Zabrání race condition, ale **sníží výkon** (paralelní práce se sekvencializuje). Klíčové: rozumět *kde* serializovat a *kolik* parallelismu obětuješ.

### 1.2 Race condition (závodní podmínka)

**CO:** Stav, kdy **výsledek závisí na načasování** souběžných vláken. Dvě vlákna čtou/zapisují sdílený stav bez vzájemné koordinace → kdo doběhne dřív, určí výsledek → nedeterministické, neopakovatelné chování.

**PROČ (v tvém kontextu, bug B1):** `evaluate_move()` voláno z více threadů → SimpleEngine není thread-safe → UCI se corruptne → `cp_loss=0`. Race condition = data jsou "v závodě" o to, kdo je přečte/zapíše první.

**JAK rozpoznat:** Chování, které funguje, když spustíš sám, a rozbíjí se pod zátěží / s více vlákny. Hodnoty občas nulové/nesmyslné bez zjevné příčiny.

**EFEKT (EROI):** Jedna z nejtěžších tříd bugů — nedeterministická, obtížně reprodukovatelná. Prevence: **synchronizace (lock)**, **immutable data**, nebo **thread-local state**.

### 1.3 Abandoned thread / zombie thread

**CO:** Vlákno, které bylo "opuštěné" — nadále běží a drží zdroj (engine, lock), ale nikdo ho neřídí ani nepředpokládá jeho dokončení. Vznikl z timeoutnutého callu.

**PROČ (bug B2):** `_run_with_timeout` spustí vlákno s timeoutem. Když timeout vyprší, hlavní kód pokračuje dál, ale vlákno **žije dál a drží engine**. Další call na engine → corrupt. Zombie = "mrtvý z pohledu řízení, živý z pohledu zdrojů".

**JAK:** Timeout ukončí *čekání* na výsledek, ale **neukončí vlákno**. Vlákno v Pythonu nelze čistě "zabít" zvenku (u CPython GIL — nelze force-kill bez rizika deadlocku). Proto je správný fix **nespouštět vlákno s timeoutem vůbec** (odstranit `_run_with_timeout` z low-level funkcí).

**EFEKT (EROI):** Zombie thread = vytečený zdroj (memory leak + držený lock). Učení: **timeout neřeší uvízlou práci, jen ukončí čekání na ni.** Návrh architektury musí zajistit, že timeoutnutá práce nemůže držet sdílené zdroje.

### 1.4 ThreadPoolExecutor

**CO:** Nástroj z `concurrent.futures` pro správu fondu (poolu) vláken. Místo ručního zakládání vláken mu předáš funkce a počet workerů, on je spustí na fondu a vrátí Future objekty.

**PROČ v tvém kontextu (bug B3):** `diagnose_player.py` + `match_patterns.py` měly 4 paralelní hry frontující za `_analysis_lock`. Každý thread volá `evaluate_move()` → lock serializuje → zbylé thready čekají → MCP timeout 60s → zombie.

**JAK:** `ThreadPoolExecutor(max_workers=4)` — 4 vlákna běží "paralelně". Ale pokud všechny narazí na jeden lock, paralelismus je iluzorní — jen fronta.

**Klíčové ponaučení (anti-pattern):** Paralelní vlákna, která **všechna narazí na stejný sdílený zdroj s lockem**, nepřinesou zrychlení, jen frontu a riziko timeoutu. **Sekvenční analýza v rámci toolu (cache-first)** je tu čistší řešení.

**EFEKT (EROI):** ThreadPoolExecutor je mocný nástroj, ale jeho použití vyžaduje pochopení sdíleného stavu. Použít ho tam, kde je práce **skutečně nezávislá** (bez sdílených zdrojů), je správně. Použít ho na práci frontovanou za jedním lockem = chyba.

### 1.5 acquire (získat zámek)

**CO:** Operace `lock.acquire()` — pokus "uzamknout" zámek. Pokud je volný, vlákno ho získá a pokračuje. Pokud je držený jiným vláknem, vlákno **blokuje (čeká)**, dokud se neuvolní.

**PROČ v fixu F2:** "timeout na acquire + engine restart při timeoutu" — přidat timeout i na samotné čekání o zámek, aby vlákno nečekalo věčně na zombie, který lock nikdy neuvolní.

**JAK (analogie):** Čekáš u zamčených dveří toalety. Bez timeoutu bys čekal věčně, kdyby se uvnitř někdo zasekl. S timeoutem po X sekundách "odstoupíš" a řešíš to jinak (restart engine).

**EFEKT (EROI):** Bezpečné vzory s lockem vždy řeší i případ "co když držitel locku zemře/uvízne" — jinak deadlock.

### 1.6 Deadlock

**CO:** Situace, kdy vlákna na sebe vzájemně čekají a žádné nemůže pokračovat → celý systém zamrzne. `with _analysis_lock:` nikdy neprojde, protože lock drží zombie thread.

**PROČ:** V tvém řetězci selhání: timeoutnutý thread drží lock → všechny další MCP cally čekají na lock věčně → MCP timeout → nové zombie → smrt smyčka.

**EFEKT (EROI):** Deadlock = úplné zamrznutí. Prevence: timeouty na acquire, držení locku co nejkratší dobu, nikdy nedržet dva locky v opačném pořadí.

---

## 2. Caching & Data

### 2.1 Cache invalidation

**CO:** Proces určení, kdy je cached data **zastaralá** a má být zahozena/obnovena. "Cache invalidation — TTL nebo max size limit."

**PROČ:** Cache je kopie dat. Pokud se zdrojová data změní, kopie je zastaralá (stale) → uživatel vidí stará data. Musíš definovat, kdy kopii zahodit.

**JAK (hlavní strategie):**
- **TTL (Time To Live)** — data platí X sekund, pak se zahodí.
- **Max size limit** — když cache přesáhne velikost, vyhodí se nejstarší položky (LRU - Least Recently Used).
- **Cache invalidation** = "jedna ze dvou nejtěžších věcí v informatice" (druhá je pojmenovávání).

**EFEKT (EROI):** Správná invalidation = kompromis mezi **čerstvostí** (TTL krátký) a **výkonem** (TTL dlouhý). Musíš pochopit trade-off.

### 2.2 TTL (Time To Live)

**CO:** Maximální doba života cache záznamu. `fetch_user_games() cache — data/game_cache/{username}_games.json, TTL 5 min` = po 5 minutách je záznam zastaralý a načte se znovu.

**PROČ:** Bez TTL by cache mohla vracet stará data navždy. S TTL víš, že data nejsou starší než 5 minut.

**EFEKT (EROI):** Konfigurovatelná hodnota = kompromis mezi výkonem a čerstvostí. Krátký TTL = vždy čerstvé, ale pomalé. Dlouhý TTL = rychlé, ale riskuješ zastaralá data.

### 2.3 L1 atomický zápis (atomic write)

**CO:** Zápis souboru tak, že je **buď celý, nebo vůbec** — nikdy v půlce poškozený. Vzor: **tmp+replace** — zapíšeš do dočasného souboru (`file.tmp`), pak ho atomicky přejmenuješ (`os.replace`) na cílový název.

**PROČ:** Přímý zápis do cílového souboru může být přerušen (crash, výpadek) → soubor zůstane **poškozený / neúplný** → cache se tiše přepíše nevalidními daty.

**JAK:**
```python
# ŠPATNĚ (non-atomic):
with open("data.json", "w") as f:
    f.write(content)   # crash uprostřed = poškozený soubor

# SPRÁVNĚ (atomic):
with open("data.json.tmp", "w") as f:
    f.write(content)
os.replace("data.json.tmp", "data.json")  # atomický přejmenování
```

**EFEKT (EROI):** `os.replace` je na stejných souborech atomický — buď proběhne celý, nebo vůbec. Čtenář nikdy nevidí poloviční soubor. "L1 atomický zápis — tmp+replace pattern (jako L2 už dělá)."

### 2.4 Lazy loading / lazy fetch / lazy

**CO:** Odložení nákladné operace na **poslední možný okamžik**, kdy je skutečně potřeba. "lazy detail fetch after boolean match, before exclude" = stáhneš detail inzerátu **až po** boolean shodě, ne pro každý inzerát předem.

**PROČ:** Fetch detailů je nákladný (HTTP request). Proč stahovat detaily 100 inzerátů, když jen 5 projde boolean filtrem? **Lazy** = stahuj jen ty, které potřebuješ.

**JAK (analogie):** Nekupuješ si všechny knihy v obchodě předem, abys věděl, kterou přečteš. Počkáš, až vybereš (boolean match), pak teprve "koupíš" (fetch detail).

**OPAK (eager):** Stáhneš vše předem. Někdy výhodné (předvídatelnost), ale plýtvání zdroji.

**EFEKT (EROI):** Lazy = úspora zdrojů, kdy je nákladná operace zbytečná pro většinu dat. Klíčové pochopení pro efektivní pipelines.

---

## 3. Python Ekosystém & Tooling

### 3.1 uv

**CO:** Moderní Python package manager a environment manager, napsaný v **Rustu** (proto extrémně rychlý). Nástupce/náhrada za pip + venv + pip-tools. Instaluje balíčky, vytváří virtuální prostředí, spravuje závislosti.

**PROČ v tvém kontextu:** "The .venv was created with **uv** which doesn't use pip by default." — uv vytváří venv, kde **pip není defaultně dostupný**; uv spravuje balíčky vlastním mechanismem (a je to rychlejší a determinističtější).

**JAK:**
- `uv venv` — vytvoří virtuální prostředí (rychleji než `python -m venv`)
- `uv pip install ...` — instaluje balíčky
- `uv sync` — synchronizuje závislosti z `pyproject.toml`/`uv.lock`
- Ekvivalent `pip` + `venv`, ale rychlejší, s lockfilem pro determinismus

**EFEKT (EROI):** Moderní standard. Učíš-li se nyní, je lepší adopce `uv` než starší `pip`/`venv` odděleně. Rychlost a determinismus = vyšší produktivita.

### 3.2 pyproject.toml (pyroprojekt / "pyproject")

**CO:** Moderní konfigurační soubor Python projektu, ve formátu TOML. Nahrazuje starší `setup.py`, `setup.cfg`, `requirements.txt` (částečně). Definuje metadata, závislosti, build systém, nástroje (ruff, pytest).

**PROČ v tvém kontextu (FIX 8, M6):** "chybí [project.optional-dependencies] → README pip install -e '.[dev]' selže." — `[project.optional-dependencies]` je sekce pro **volitelné extra balíčky** (např. dev nástroje: pytest, ruff).

**JAK (struktura):**
```toml
[project]
name = "mcp-jobs"
version = "0.1.0"
dependencies = ["requests", "pyyaml"]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pyyaml>=6.0", "ruff>=0.6"]

[tool.ruff]
line-length = 100
```

`pip install -e ".[dev]"` — `.` = tento projekt, `[dev]` = nainstaluj i dev extra balíčky.

**EFEKT (EROI):** `pyproject.toml` = centrální místo konfigurace projektu. Nezbytný pro moderní Python.

### 3.3 ruff

**CO:** Statický analyzátor + formátor pro Python, napsaný v Rustu. Dvě funkce:
- `ruff check` = **linter** — hledá podezřelé vzory (nepoužité proměnné, importy, moc dlouhé řádky)
- `ruff format` = **formátor** — sjednocuje styl (délka řádků, uvozovky, mezery)

**PROČ "statický":** Ruff pracuje s **textem kódu**, nespouští ho. Chytá třídu chyb, které testy nepokryjí (nikdo netestuje "nepoužitou proměnnou").

**Klíčové pravidlo ID:**
| ID | Rodina | Význam |
|----|--------|--------|
| F841 | pyflakes (logické) | proměnná přiřazená, nikdy nepřečtená — mrtvý kód |
| E501 | pycodestyle (styl) | řádek delší než 100 znaků |
| F401 | pyflakes | nepoužitý import |

**EFEKT (EROI):** Linter = levná kontrola před během. Oprava pozdě = drahá (ruff debt). Viz sekce "ruff debt" níže.

### 3.4 grep

**CO:** Unixový nástroj pro **hledání textu v souborech** podle patternu. Základní nástroj každého vývojáře.

**PROČ v tvém kontextu (pravidlo P1):** "**grep INDEX** před vytvořením souboru" — před zápisem nového artefaktu do KB je nutné **prohledat existující soubory** (grep/kb_search), aby se nevygenerovala duplicita.

**JAK:**
- `grep "pattern" soubor.txt` — najdi řádky s patternem
- `grep -r "pattern" adresar/` — rekurzivně
- `grep -i` — case-insensitive

**EFEKT (EROI):** `grep` + `git` jsou dva nástroje, které používáš celý život. Hledání v textu = základní diagnostika.

### 3.5 Ruff debt (technický dluh z lintingu)

**CO:** Nahromaděná porušení pravidel v committnutém kódu, která nikdo neopravil. Vznikla, když guard (pre-commit hook) byl rozbitý → každý commit prošel → porušení přibývala nepozorovaně → 46 chyb.

**PROČ "debt" (dluh):** Analogie finančního dluhu — "úrok" = čím déle neopravuješ, tím hůř se to opravuje. Guard je levný teď, drahý pozdě.

**Proč `--fix` nebezpečné:** Ruff je **lexikální nástroj, nezná záměr**. U F401 (nepoužitý import) smaže import, který má **side-effect** (import vykoná kód — registrace toolů). Ruff "ví jen", že se jméno nepoužívá → smaže řádek → rozbiješ program, který se tváří v pořádku.

**EFEKT (EROI):** Automatické opravy nástrojů nejsou vždy bezpečné. Když nástroj smaže řádek, musíš rozumět, **proč** tam řádek byl. Anti-blackbox princip.

---

## 4. Testing

### 4.1 Mock / MagicMock

**CO:** **Mock** = objekt, který **simuluje** (falešně imituje) chování reálného objektu/zdroje, aby test mohl běžet izolovaně bez reálných závislostí. **MagicMock** = konkrétní typ mocku z knihovny `unittest.mock` — "magicky" generuje atributy a metody na požádání.

**PROČ v tvém kontextu:**
- "test_http_exception_logged (**mock** RequestException → záznam v caplog)" — simuluješ výjimku, aniž bys volal reálné HTTP.
- "7 nových unit testů, **mock** MagicMock (žádný reálný Stockfish/network)" — testuješ logiku analyzátoru bez spuštění reálného Stockfish enginu ani network callů.

**JAK (analogie):** Mock = figurant v divadle. Hraje roli Stockfish enginu, ale místo reálného výpočtu vrací předem dané hodnoty. Tak otestuješ, že tvůj kód správně zpracuje výstup, aniž bys čekal 40s na reálný engine.

**EFEKT (EROI):** Mock = izolace testu. Test, který závisí na reálném networku/enginu, je **pomalý a křehký** (flaky). Mock ho udělá rychlý a deterministický. Ale pozor — mock netestuje reálnou integraci (proto existuje i contract/integration testing).

### 4.2 Dead code

**CO:** Kód, který se **nikdy neprovede** / není dosažitelný / nikdo ho nepoužívá. V tvém kontextu (FIX 7, M5): "soubor není `test_*.py` → pytest ho nesbírá (12 testů = **dead code**)."

**PROČ:** Falešný pocit pokrytí — myslíš si, že máš 115 testů, ale 12 se nikdy nespustí. Dead code = plýtvání údržbou + falešná jistota.

**JAK rozpoznat:** Testy, které pytest nepojmenuje podle konvence `test_*.py` / `test_*.py`. Funkce volané nikde. Importy nepoužité (chytá ruff F401).

**EFEKT (EROI):** Dead code je "šum" — zvyšuje kognitivní zátěž a dává falešný pocit bezpečí. Pravidelná údržba odstraňuje.

---

## 5. Web Scraping & HTML

> **Kontext:** Refaktor MCP-jobs pipeline — scraping jobs.cz / prace.cz. Pochopení DOM a CSS selectorů je klíčové pro stabilní scraper.

### 5.1 DOM (Document Object Model)

**CO:** Stromová reprezentace HTML stránky, jak ji vidí prohlížeč a scraping nástroje. Každý element (div, span, a...) je uzel ve stromu s atributy, třídami a obsahem.

**PROČ v tvém kontextu:** "Ověřím aktuální **DOM** na živých stránkách, aby návod byl přesný." — DOM je to, co scraper parsuje. Znát DOM = vědět, kde najít salary, popis, atd.

**JAK:** HTML je text, DOM je **struktura**. Prohlížeč převede `<div class="job"><span>name</span></div>` na strom: root → div → span.

**EFEKT (EROI):** Scraper = čtečka DOM. Čím lépe rozumíš DOM, tím stabilnější selectory napíšeš.

### 5.2 CSS selector

**CO:** Vzor pro **výběr elementů** z DOM podle tříd, atributů, struktury. Např. `[class*='salary']` = vyber element, jehož class atribut obsahuje "salary".

**PROČ v tvém kontextu:** "prace.cz nemá data-test attribut — má hashed CSS module class (křehká). Najdu stabilnější selector (předek/obálka)." — Selector je "adresa" elementu v DOM. Stabilní selector přežije redesign, křehký se rozbije.

**JAK (typy selectorů):**
- `.trida` — element s class="trida"
- `#id` — element s id
- `div > span` — přímý potomek
- `[attr='hodnota']` — podle atributu
- `[class*='salary']` — class obsahující "salary"

**EFEKT (EROI):** Kvalita scraperu = kvalita selectorů. Stabilní = sémantické atributy (data-test), křehké = generované hashed třídy.

### 5.3 Hashed CSS module class (např. RichContent-module-scss-module__x4jkqW__RichContent)

**CO:** Automaticky generovaný název CSS třídy z **CSS Modules / CSS-in-JS bundlerů** (jako Vite, webpack). Formát: `{název}_module-scss-module__{hash}__{skutečnýNázev}` — hash (x4jkqW) je unikátní pro daný build.

**PROČ je to křehké:** Hash se **mění při každém rebuildu / změně kódu / verzi** frontendu. Selector postavený na hashed class se rozbije při každém novém deployi portálu. "To je křehké."

**JAK:** CSS Modules dávají každé třídě lokální scope + hash, aby se třídy nekolidovaly mezi komponentami. Pro scraper je to nepřítel — hashed class není stabilní identifikátor.

**EFEKT (EROI):** V scraping kontextu hledej **stabilní sémantické atributy** (data-test, data-jobad) místo hashed tříd. Pokud nejsou, najdi stabilního **předka/obálku** (sémantický element).

### 5.4 Plain HTTP GET vs headless

**CO:** **Plain HTTP GET** = načtení stránky přímo HTTP requestem (bez spuštění prohlížeče). **Headless** = bezhlavý prohlížeč (renderuje JS, pak scraper).

**PROČ:** "prace.cz detail také dostupný **plain HTTP**, popis v RichContent..." — pokud je obsah dostupný plain HTTP, nemusíš drahý a pomalý headless browser. Server vrací HTML rovnou.

**EFEKT (EROI):** Plain HTTP je rychlejší, levnější, jednodušší. Headless až když stránka renderuje obsah přes JavaScript.

---

## 6. Data Processing & Matching

### 6.1 Dedup / dedup kolize (deduplication collision)

**CO:** **Dedup** = odstranění duplicit (duplicitních záznamů). **Dedup kolize** = situace, kdy dedup **omylem smaže dva RŮZNÉ platné záznamy**, protože je považuje za duplicitní.

**PROČ v tvém kontextu (FIX 1, C1):** `_dedup` stavěl `fuzzy_key=(title, company)` **bez lokality**. Stejný title+company na jiné URL/lokalitě → druhý **tiše zahozen**. = reálná ztráta dat u firem s pobočkami.

**JAK:** Dedup používá "klíč" k identifikaci duplicity. Pokud klíč nezahrnuje lokalitu, dvě pobočky téže firmy (Praha, Brno) vypadají jako duplicita → jedna se smaže. Fix: rozšířit klíč o lokalitu.

**EFEKT (EROI):** Dedup klíč musí obsahovat **všechny rozlišující atributy**. Příliš agresivní dedup = ztráta dat. Příliš mírný = duplicity.

### 6.2 Fuzzy matching / fuzzy-drop

**CO:** **Fuzzy matching** = shoda na základě **podobnosti**, ne přesné rovnosti (překlepy, varianty, "Praha" vs "Praha 5"). **Fuzzy-drop** = zahazování záznamu na základě fuzzy shody.

**PROČ v tvém kontextu (FIX 1):** "Při **fuzzy-drop** jiné URL → logger.warning." — když fuzzy dedup zahodí záznam na jiné URL, měl by se to zalogovat (ne tiše), aby šlo odhalit chybný dedup.

**JAK:** Fuzzy = místo `"Praha" == "Praha 5"` (False) používá podobnost (True). Nástroje: Levenshtein distance, normalizace textu.

**EFEKT (EROI):** Fuzzy je mocný (odolává překlepům), ale **nebezpečný** (může sloučit různé věci). Vždy logovat fuzzy-drop.

---

## 7. Text & Unicode

### 7.1 Hyphen / non-breaking hyphen (U+2011)

**CO:** Dva typy pomlček:
- **ASCII hyphen** `-` (U+002D) — obyčejná pomlčka.
- **Non-breaking hyphen** (U+2011, ‑) — pomlčka, která **neumožňuje zalomení řádku** (word wrapping) na tom místě. Vypadá skoro stejně, ale má jiný Unicode kód.

**PROČ v tvém kontextu:** "Neuro‑Architektuře používá non-breaking **hyphen** (U+2011) v textu, ale původní název souboru měl ASCII - (Neuro-Architektuře)." — Vizuálně podobné, ale **technicky jiné znaky** → soubor `Neuro-Architektuře.md` (ASCII) nenajde odkaz s U+2011 bez úprav.

**JAK rozpoznat:** Znaky, které *vypadají* stejně, ale mají jiný Unicode kód. Nebezpečí: porovnávání řetězců selže, vyhledávání nenajde, filename se neshoduje.

**EFEKT (EROI):** Vždy si ověř Unicode kód, ne vizuální podobu. Názvy souborů: **ASCII-NOM** konvence (jen `[A-Za-z0-9._-]`, žádné diakritiky, žádné U+2011).

### 7.2 Escapy (escaping)

**CO:** Použití zpětného lomítka `\` (nebo jiné syntaxe) k **odlišení speciálního znaku** od jeho doslovné hodnoty. Např. `\"` znamená "citát uvnitř řetězce", ne "konec řetězce".

**PROČ:** "řádky 592, 614 — měly jiné **hyphen/escapy**" — escapy ovlivňují, jak se text interpretuje (markdown odkazy, regex, řetězce).

**EFEKT (EROI):** Pochopení escapování = pochopení, proč se něco "chová divně" v markdownu, regexu, JSON, shellu.

---

## 8. Core Concepts

### 8.1 Idempotence (idempotence)

**CO:** Vlastnost operace, že **opakované provedení dává stejný výsledek jako provedení jednou**. "Opakované loadování skillu by mělo být bezpečné — žádné side effects mimo projekt."

**PROČ:** Pokud je operace idempotentní, můžeš ji bezpečně spustit vícekrát bez vedlejších škod (side effects). Pokud ne, druhé spuštění něco rozbije (např. duplicita).

**JAK (příklady):**
- `GET /users` — idempotentní (jen čte)
- `DELETE /users/5` — idempotentní (po 1. smazání už nemá co mazat, ale výsledek stejný)
- Zápis do souboru bez atomického patternu — **NENÍ** idempotentní (může poškodit)

**EFEKT (EROI):** Idempotence = bezpečnost opakování. Klíčová pro retry logiku, skripty, deploymenty, loadování skillů.

### 8.2 Synchronní vs asynchronní

**CO:**
- **Synchronní:** provádíš operaci a **čekáš**, dokud neskončí. Jeden krok za druhým.
- **Asynchronní:** spustíš operaci a **jdeš dál**; výsledek zpracuješ, až přijde.

**PROČ v tvém kontextu (FIX 1, F1):** "**Synchronní engine access** (bez `_run_with_timeout`, bez thread poolu v evaluate_move)" — vracíš se k synchronnímu přístupu k engine, protože async/parallel tam způsoboval zombie a deadlock.

**EFEKT (EROI):** Synchronní = jednodušší, deterministický, ale blokuje. Asynchronní = výkonnější, ale komplexnější (deadlocky, race conditions). Volba závisí na kontextu.

### 8.3 Guardrail

**CO:** Mechanismus, který **blokuje/varuje před nežádoucí akcí**. "To je princip guardrail: kontrola je levná, oprava pozdě je drahá."

**PROČ:** Guard (např. pre-commit hook) má spouštět kontrolu před commitem a zablokovat ho při selhání. Rozbitý guard → kontroly neprobíhaly → 46 chyb se nahromadilo.

**JAK (analogie):** Zábradlí na mostě. Když je, nepadáš. Když chybí/rozbité, pád je drahý.

**EFEKT (EROI):** Guardrails = levná prevence drahých chyb. Ale guardrail funguje jen pokud je **sám funkční** (testovat i guard).

---

## 9. Ruff — principy bez black boxu (detailní příloha)

> Vzhledem k tomu, že ruff byl v artefaktu vysvětlen podrobně, zachovávám zde jádro pro rychlý referenční přehled.

- **Ruff** = statický analyzátor + formátor pro Python (Rust → rychlý).
- `ruff check` = linter (hledá podezřelé vzory), `ruff format` = formátor (sjednocuje styl).
- **Statický** = pracuje s textem kódu, nespouští ho → chytá chyby, které testy nepokryjí.
- **Ruff debt** = nahromaděná porušení, když guard nefunguje. Vznik 4 kroky: pravidla nastavená → guard rozbitý → commit prošel → porušení přibývala.
- **`--fix` nebezpečné:** ruff je lexikální, nezná záměr. U F401 smaže import se side-effectem → rozbiješ program.

---

## Metadata

- **Tags:** `#swe`, `#glossary`, `#terminologie`, `#ontologie`, `#edu`, `#concurrency`, `#testing`, `#web-scraping`, `#python`
- **EROI:** 9/10 (živý edukační artefakt; náklad = údržba, benefit = trvalá adopce terminologie → překonání unknown unknowns)
- **Živý dokument:** průběžně doplňovat nové termíny z dev workflow.

## Jak doplňovat nový termín (návod pro autora i LLM)

1. Najdi v kontextu zvýrazněný termín (`**termín**`).
2. Ověř, zda už není v tomto dokumentu (grep) — **P1 pravidlo, žádné duplicity**.
3. Pokud není, doplň novou sekci s šablonou: **CO / PROČ / JAK (analogie) / EFEKT (EROI)**.
4. Zvýrazni termín boldem a uveď kontext, ve kterém ses s ním setkal.
5. Pokud je v artefaktu vysvětlení, zachovej jádro a rozšiř.
