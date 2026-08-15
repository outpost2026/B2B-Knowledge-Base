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
4. [Testing](#4-testing) — mock, MagicMock, unit test, dead code, test pyramida, contract testing (CDC), schema testy
5. [Web Scraping & HTML](#5-web-scraping--html) — DOM, CSS selector, hashed CSS module, lazy fetch
6. [Data Processing & Matching](#6-data-processing--matching) — dedup, fuzzy matching
7. [Text & Unicode](#7-text--unicode) — hyphen, non-breaking hyphen, escapy
8. [Core Concepts](#8-core-concepts) — idempotence, synchronní vs asynchronní, guardrail
9. [CI/CD & Verzování](#9-cicd--verzovani) — CI, CD, pipeline, matrix, fail-fast, Dependabot, CodeQL, semver
10. [Design Patterns](#10-design-patterns) — Singleton, Mutex
11. [LLM & Nondeterminismus](#11-llm--nondeterminismus) — determinismus, halucinace, konfabulace
12. [Observability & Resilience](#12-observability--resilience) — observability, metrics, percentily, feature flags, resilience
13. [ML/CV pojmy (částečně)](#13-mlcv-pojmy-castecne) — inference, latency, epoch, dataset
14. [Ruff — principy bez black boxu (příloha)](#14-ruff--principy-bez-black-boxu-priloha)
15. [Frontend & Next.js](#15-frontend--nextjs) — React, App Router, API routes, SSR/ISR/CSR, Tailwind, Vercel
16. [Monorepo & Workspaces](#16-monorepo--workspaces) — monorepo, npm workspaces
17. [Databáze & SQL](#17-databaze--sql) — PostgreSQL, SQL, tabulka, klíče, indexy, JSONB, migrace
18. [DevOps & Deployment](#18-devops--deployment) — DevOps, Docker, porty, monitoring, healthchecks, CI/CD
19. [Cloud & PaaS](#19-cloud--paas) — PaaS, serverless, provider-agnostic

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

### 4.3 Test pyramida

**CO:** Hierarchie testů podle rozsahu + rychlosti + počtu:
```
Unit Tests          ← testují jednu funkci/třídu izolovaně (nejvíce, nejrychlejší)
  ↓
Contract Tests      ← testují rozhraní mezi dvěma moduly
  ↓
Integration Tests   ← testují více modulů dohromady (s reálnými závislostmi)
  ↓
E2E Tests           ← testují celý systém od UI/API po databázi (nejméně, nejpomalejší)
```

**PROČ:** Čím širší test, tím dražší a pomalejší. Pyramida říká: **většina testů má být na spodku (unit)** — rychlé, izolované. Málo E2E — pomalé a křehké.

**JAK (analogie):** Pyramida stavíš stabilní základnou. Když máš 80 % E2E testů, je to "inverted pyramid" = křehké, pomalé, drahé.

**EFEKT (EROI):** Pochopíš, KAM který test patří. To je ontologie testování — klíčová pro rozhodování, co testovat a jak.

### 4.4 Contract testing / CDC (Consumer-Driven Contract)

**CO:** Test, který ověřuje **rozhraní mezi dvěma moduly** — dodržuje producer smlouvu, kterou od něj consumer očekává? **CDC (Consumer-Driven Contract)** = consumer definuje kontrakt, producer se mu přizpůsobí.

**PROČ:** V modulární architektuře si moduly předávají data (JSON). Typický bug: producer změní klíč z `ply` na `move_number` → consumer čte `ply` → dostává `None` → nikdo nekřičí (žádná type error) → LLM dostane `move ?` místo `move 27`. **Tento bug není odhalitelný unit testy** — oba moduly procházejí své testy izolovaně. Problém je v rozhraní mezi nimi.

**JAK:**
```python
# Consumer definuje kontrakt — test píše ten, kdo data čte
def test_contract():
    data = json.load(open("cache.json"))
    for key in PROMPT_KEYS:   # {"ply", "move_san", "centipawn_loss", "phase"}
        assert key in data["blunders"][0]
```

**Pravidlo:** Consumer definuje kontrakt. Test žije u consumeru. Pokud se změní klíče v modelu → contract test selže dřív, než se bug dostane do LLM.

**EFEKT (EROI):** Chytá chyby rozhraní, které unit testy nevidí. U MCP pipeline (JSON na disku, producer+consumer v jednom repu) stačí lightweight varianta — nepotřebuješ Pact server ani schema registry.

### 4.5 Schema testy / placeholder detection / noise-floor detection

**CO:** Tři konkrétní typy contract testů pro data → LLM vrstvu:
- **Schema test** — ověří, že JSON obsahuje klíče, které consumer čte.
- **Placeholder detection** — ověří, že prompt neobsahuje neznámé hodnoty (např. `?`). Detekuje bugy, které schema test neodhalí (klíč existuje, ale je null).
- **Noise-floor detection** — kontroluje sémantickou konzistenci (např. `assert accuracy > 0` — accuracy nemůže být 0 u reálné hry).

**PROČ:** Schema test ověří strukturu, placeholder sémantiku promptu, noise-floor přípustnost hodnot. Tři úrovně = kompletní ochrana.

**JAK (analogie):** Schema test = "dokument má kapitoly". Placeholder = "kapitoly nejsou prázdné". Noise-floor = "kapitoly dávají smysl" (není tam 0 tam, kde 0 být nemá).

**EFEKT (EROI):** Vrstvená validace dat pro LLM vrstvu — nejen že data existují, ale že dávají smysl. Klíčové proti tichému šíření chyb do promptu.

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

## 9. CI/CD & Verzování

> **Kontext vzniku:** Imerzní edukace CI (CI_GitHub_Actions_imerzni_edu_v1.md) — dev implementoval CI až po 4 měsících R&D. Tato sekce vytěžuje zavedenou terminologii.

### 9.1 CI (Continuous Integration)

**CO:** Automatické otestování každé změny. Push na GitHub → spustí se čistý server → naklonuje kód → nainstaluje závislosti → spustí testy → výsledek green/red.

**PROČ:** Tvůj mozek má limit ~7 věcí v krátkodobé paměti. Děláš-li 5 změn v různých repozitářích, nemůžeš si pamatovat, jestli každá nerozbila něco. CI je tvůj **externí mozek** — do 2 minut víš, že je něco rozbité, dokud máš kontext v hlavě.

**JAK (analogie):** CI = automatický hlídač, který po každé změně otestuje celý systém. Ne "jak se píše kód", ale "jestli pořád funguje".

**EFEKT (EROI):** CI dává smysl až ve fázi stabilizace — když máš funkční produkt a přidáváš featury. V R&D fázi je test outdated za 20 minut. Milestone: kdy začneš rozbíjet věci, aniž bys to věděl.

### 9.2 CD (Continuous Deployment)

**CO:** Automatické nasazení po testech. CI = otestovat. CD = nasadit.

**PROČ:** U tebe zatím CD není — zatím jen CI. Rozdíl pochopíš jako: CI odpovídá na "funguje to?", CD na "je to nasazené?".

**EFEKT (EROI):** Konceptuální rozlišení CI vs CD — pipeline je řetězec: push → test → deploy.

### 9.3 Pipeline

**CO:** Celý řetězec automatizovaných kroků: push → test → deploy. Každý krok = jeden job/stage.

**EFEKT (EROI):** Pipeline je abstrakce "co se stane s kódem od commitu po produkci".

### 9.4 Matrix

**CO:** Testování na více konfiguracích paralelně (Python 3.10/3.11/3.12, více OS). `strategy: matrix: python-version: ["3.10", "3.11", "3.12"]`.

**PROČ:** Tvůj dev stroj má 3.12, zákazník může mít 3.10. Klasická chyba: `f-string`, `match-case`, `walrus operator` — každá Python verze přidává novinky. Na tvém stroji funguje, u zákazníka padá.

**JAK:** `fail-fast: false` = pokud 3.10 spadne, 3.11 a 3.12 běží dál. Bez toho by CI zabil všechny testy při první chybě.

**⚠️ Lekce z produkce:** Matrix verze musí být **podmnožina** deklarovaného rozsahu (`python_requires = >=3.11`), ne nadmnožina. Přidání 3.10 k `>=3.11` failne hned u pip install, ne u testů.

**EFEKT (EROI):** +2 řádky YAML (2 minuty) → chytí version-specific bug dřív, než se dostane k zákazníkovi.

### 9.5 Cron / Nightly cron

**CO:** Časovač — `cron: "0 6 * * *"` = každý den v 6:00 UTC. Nightly = noční automatický run i bez pushnutí.

**PROČ (solo dev):** Neděláš commity každý den; Dependabot aktualizuje balíčky sám (může něco rozbít); GitHub může mít výpadek. Nightly je "ranní kontrola" — přijdeš k PC, vidíš green/red.

**EFEKT (EROI):** +3 řádky (2 minuty) → chytí problémy, které by jinak zůstaly skryté týdny.

### 9.6 Fail-fast

**CO:** Princip: pokud jedna varianta selže, okamžitě zastav/zabij ostatní. (V matrixu: `fail-fast: true` = zabít vše při první chybě.)

**PROČ:** Rychlá signalizace chyby. Ale v matrixu se často chce `fail-fast: false` — aby ses dozvěděl, jestli ostatní verze procházejí.

**EFEKT (EROI):** Fail-fast je design filozofie: selhat brzy a hlasitě, ne tiše pokračovat do neznáma.

### 9.7 Dependabot

**CO:** GitHub robot na automatickou aktualizaci závislostí. Týdně zkontroluje nové verze (pytest, ezdxf, numpy...) a vytvoří PR s aktualizací.

**PROČ:** Solo dev nemá kapacitu ručně sledovat aktualizace. Stará verze = bezpečnostní díra + chybí featury. Nová verze = může rozbít kód. Dependabot pošle PR, CI se spustí na PR a ukáže green/red → víš, zda je nová verze kompatibilní.

**EFEKT (EROI):** Automatická údržba = méně chyb, víc času na RE. Dependabot = součást CI (nejen testy, ale i údržba deps).

### 9.8 CodeQL

**CO:** GitHub security scanner — automaticky prohledá kód na bezpečnostní chyby: SQL injection, OS command injection (subprocess bez sanitizace), credential leak (heslo v kódu), nezabezpečené importy.

**PROČ:** **B2B důvěryhodnost** — zákazník se zeptá "a co security scanning?". CodeQL je průmyslový standard (Microsoft, Google). V RE kódu snadno necháš cestu k serveru nebo API klíč — CodeQL to chytí dřív, než to pushneš do public repa.

**⚠️ Lekce z produkce:** CodeQL v4 vyžaduje `actions: read` permission v top-level bloku. Debug pattern: `##[error]Resource not accessible by integration` = chybí `actions: read`.

**EFEKT (EROI):** 10 minut YAML → ochrana před únikem credentialů + B2B prodejní argument.

### 9.9 Další CI terminologie (zkráceně)

| Pojem | Význam |
|-------|--------|
| **PAT** | Personal Access Token — bezpečnostní klíč pro GitHub API |
| **Workflow dispatch** | Ruční spuštění workflow z UI |
| **Repository dispatch** | Spuštění workflow z jiného repa |
| **Runner** | Server, který CI spouští (ubuntu-latest); self-hosted = vlastní server |
| **Green/Red** | Testy prošly / selhaly |
| **SLSA / Attestations** | Kryptografický důkaz původu artifactu |

### 9.10 Semver (semantic versioning, major/minor/patch)

**CO:** Standard verzování: `major.minor.patch` (např. `1.2.3`). **Major** (1→2) = breaking changes. **Minor** = nová featura, zpětně kompatibilní. **Patch** = oprava bugu.

**PROČ:** "numpy 1→2 = breaking" — major bump může rozbít kód. Rozlišení major/minor určuje riziko aktualizace.

**EFEKT (EROI):** Neuděláš chybu a nerozbiješ zákazníkovi kód. `>=1.4.4` v requirements = "používám verzi od 1.4.4 výše".

---

## 10. Design Patterns

> **Kontext vzniku:** RETENEZEC_PRICIN_pipeline_nedeterminismus (ontologie pro junior dev) — analýza lichess pipeline, kde nedeterminismus engine vedl k chybným výsledkům.

### 10.1 Singleton

**CO:** Design pattern — **jedna instance na celou aplikaci**. Ať kdekoli požádáš o objekt, dostaneš stejnou instanci.

**PROČ (v kontextu lichess):** Engine (Stockfish) je drahý zdroj — vytvořit nový proces per call = prázdná Transposition Table = **fyzický nedeterminismus** (stejný FEN dá různý výsledek, spread 533-1149 cp). Singleton = sdílená instance engine napříč aplikací.

**JAK (analogie):** Jeden sdílený klíč od toalety, ne kopie pro každého. Všichni používají tentýž objekt.

**EFEKT (EROI):** Singleton zajišťuje **sdílení stavu** (TT, cache). Ale pozor — sdílený stav bez synchronizace = race condition. Proto Singleton + Mutex jdou ruku v ruce.

### 10.2 Mutex (lock)

**CO:** Synchronizační prvek — umožňuje přístup k prostředku jen jednomu vláknu v daný okamžik. (Synonymum: lock. Detaily viz sekce 1.5 acquire.)

**PROČ (v kontextu lichess):** `_analysis_lock = threading.Lock()` serializuje přístup k engine — žádné dvě vlákna nesmí volat engine současně (UCI by se corruptnul).

**EFEKT (EROI):** Mutex je odpověď na otázku "co když dvě vlákna chtějí stejný zdroj?". Základní stavební kámen thread-safe aplikací.

---

## 11. LLM & Nondeterminismus

> **Kontext vzniku:** RETENEZEC — proč pipeline dávala různé výsledky pro stejný vstup. Klíčové rozlišení pro každého, kdo pracuje s LLM + deterministickými nástroji.

### 11.1 Determinismus vs nedeterminismus

**CO:**
- **Determinismus:** stejný vstup = stejný výstup.
- **Nedeterminismus:** stejný vstup může dát rozdílný výstup.

**PROČ v tvém kontextu:** Stockfish je fyzicky deterministický (daná TT + threads + depth = stejný výsledek). Ale když se per call vytvoří **nový proces** s prázdnou TT, každý call běží "z nuly" → nedeterministický výstup (spread 533-1149 cp). LLM je naopak **inherentně nedeterministický** (sampling).

**JAK (analogie):** Deterministický = pekárna, která vždy upeče přesně stejný chléb z přesně stejné mouky. Nedeterministický = chléb se mění podle nálady pekaře.

**EFEKT (EROI):** Když tvůj pipeline mísí deterministické a nedeterministické komponenty, musíš rozumět, KDE nedeterminismus vzniká — jinak dostaneš nedetekovatelné chyby (viz 11.2).

### 11.2 Halucinace (LLM)

**CO:** Model generuje informace, které nejsou podložené daty. "Visici dama" je čistá halucinace — není podložena daty.

**PROČ:** LLM je pravděpodobnostní model — generuje text, ne fakta. Pokud vstup (prompt/data) neobsahuje odpověď, model si ji **vymyslí** sebevědomě.

**EFEKT (EROI):** Halucinace je vlastnost, ne bug. Pochopení = návrh pipeline, který nedůvěřuje LLM výstupu bez ověření (contract testy, noise-floor, deterministická orákula).

### 11.3 Konfabulace

**CO:** Aktivní vymýšlení informací na základě rozporových dat. Odlišná od halucinace: konfabulace nastává, když jsou data **rozporuplná** a model si "domyslí" koherentní příběh.

**JAK:** Halucinace = chybějící data → vymyšlení. Konfabulace = rozporová data → "slepení" příběhu, který dává smysl.

**EFEKT (EROI):** Rozlišení halucinace vs konfabulace = diagnostická přesnost. Podle typu chyby zvolíš jinou opravu (chybějící data vs rozporová data).

---

## 12. Observability & Resilience

> **Kontext vzniku:** Hluboký ponor do rezerv vývoje MCP serveru — 6 gapů (resilience, security, observability, feature flags, terminologie, internals).

### 12.1 Observability (pozorovatelnost)

**CO:** Schopnost systému **odhalit, co se děje uvnitř** z vnějšku — přes logy, metriky, trace. "Chyby ano, zdraví ne" = klasický gap: víš, že server spadl, ale neproč.

**PROČ:** Bez observability jsi slepý — řešíš symptomy, ne příčiny. S metrics endpointem by 100 % error rate odhalil okamžitě.

**EFEKT (EROI):** Observability = "řídicí panel" systému. Investice do ní se vrací při každém bugu.

### 12.2 Metrics / percentily (p50/p95/p99)

**CO:** Číselné ukazatele výkonu systému. **Percentily** = "kolik % požadavků bylo rychlejších než hodnota". p50 = medián (polovina požadavků). p95 = 95 % požadavků. p99 = 99 %.

**PROČ:** Průměr lže (pár pomalých requestů ho zkazí). p99 ukáže **nejhorší typické zpoždění** — "uživatel v nejhorších 1 % případů čeká X ms".

**JAK (analogie):** p50 = typický zákazník, p99 = nejméně trpělivý zákazník. Optimalizuješ-li jen medián, necháš pomalé 1 % trpět.

**EFEKT (EROI):** `mcp_requests_total`, `mcp_latency_seconds` (prometheus) — měřit per tool. Latency z MCP = klíčová (MCP timeout 60s je nepřítel).

### 12.3 Resilience (odolnost)

**CO:** Schopnost systému **přežít a zotavit se** z poruch. Auto-restart (winsw jako Windows Service, `onFailure=restart`) + health check.

**PROČ:** "Server padá v noci" — nikdo to nevidí. Resilience = systém se sám restartuje a notifikuje.

**EFEKT (EROI):** Spadlý server = největší nepřítel služby. Auto-restart + notifikace = 2 hodiny práce, trvalá ochrana.

### 12.4 Feature flags

**CO:** Přepínače funkcí — aktivace/deaktivace featury **bez release** (přes env var `ENABLED_PROVIDERS`).

**PROČ:** "Pomalý feedback loop" — každá změna vyžaduje release. Feature flag = zapneš/vypneš funkci v produkci za sekundu, bez nasazení.

**EFEKT (EROI):** Test izolovaně → aktivace bez release. A/B testy, canary releases, rychlý rollback.

### 12.5 Structured logging

**CO:** Logování ve **strukturovaném formátu** (JSON), ne volný text. Každá chyba má definované pole (timestamp, level, tool, message).

**PROČ:** Volný text nelze strojově filtrovat. Structured log = greppovatelný, agregovatelný, analyzovatelný.

**EFEKT (EROI):** Tiché selhání + volné logy = neviditelná chyba. Structured logging = každá chyba má stopy.

---

## 13. ML/CV pojmy (částečně)

> **Kontext vzniku:** YOLO11_GARDEN_MONITOR_GLOSSARY — glossary pro CV začátečníka. Zahrnuty jen genericky použitelné pojmy; YOLO/CV specifické detaily jsou doménový balast.

### 13.1 Inference

**CO:** Okamžik, kdy model zpracuje jeden vstup (obrázek/text) a vrátí predikci. "AI model zpracuje jeden obrázek a řekne 'toto je rostlina'."

**PROČ:** Inference je "běh modelu" — na rozdíl od tréninku. Trénink = učení z dat. Inference = použití naučeného.

**EFEKT (EROI):** Pojem se používá napříč ML i LLM. Rozumíš rozdílu trénink vs inference.

### 13.2 Latency

**CO:** Zpoždění — jak dlouho trvá jedna operace. 16 ms = rychlé, 500 ms = pomalé. (Viz též 12.2 — p50/p95/p99 latency.)

**EFEKT (EROI):** Latency je měřitelná metrika kvality — zvlášť kritická u MCP (timeout 60s).

### 13.3 Epoch / Dataset

**CO:** **Epoch** = jedno kompletní pročtení celého datasetu během tréninku. 50 epoch = model viděl každý obrázek 50×. **Dataset** = datová sada (vstupy + odpovědi).

**EFEKT (EROI):** Základní ML terminologie — pojmy, na které narazíš u každého ML projektu.

---

## 14. Ruff — principy bez black boxu (detailní příloha)

> Vzhledem k tomu, že ruff byl v artefaktu vysvětlen podrobně, zachovávám zde jádro pro rychlý referenční přehled.

- **Ruff** = statický analyzátor + formátor pro Python (Rust → rychlý).
- `ruff check` = linter (hledá podezřelé vzory), `ruff format` = formátor (sjednocuje styl).
- **Statický** = pracuje s textem kódu, nespouští ho → chytá chyby, které testy nepokryjí.
- **Ruff debt** = nahromaděná porušení, když guard nefunguje. Vznik 4 kroky: pravidla nastavená → guard rozbitý → commit prošel → porušení přibývala.
- **`--fix` nebezpečné:** ruff je lexikální, nezná záměr. U F401 smaže import se side-effectem → rozbiješ program.

---

## 15. Frontend & Next.js

> **Kontext vzniku:** SKILL_GAPS_ROZBOR_Q3_2026_v2 — imerzní analýza `outprep` (Next.js monorepo standalone web app) pro aspiraci portu MCP serveru na standalone produkt. Autor zná Streamlit (dashboard = stránky); Next.js = stejný koncept s plným backendem a TS.

### 15.1 Next.js

**CO:** **React framework** od Vercelu. React = knihovna pro UI komponenty. Next.js = framework, který přidává souborové routování, API routes (backend ve stejném projektu), server-side rendering a serverless deployment.

**PROČ:** Next.js = nejpopulárnější React framework, default pro nové projekty. Pro standalone produkt (GUI na systeq.cz) je volba č.1.

**JAK (analogie):** Next.js = "Streamlit pro produkční web, ale s plným backendem a TS".

**EFEKT (EROI):** Frontend gap rozšiřuje TS: už to není jen jazyk pro testy — je to jazyk celého standalone frontendu.

### 15.2 React

**CO:** Knihovna pro **UI komponenty** — znovupoužitelné stavební bloky rozhraní. Komponenta = funkce/JSX vracející HTML.

**JAK (analogie):** Komponenty ≈ Streamlit stránky, ale s jiným modelem (deklarativní, stavová).

**EFEKT (EROI):** React = základní kámen frontendu; Next.js na něm staví.

### 15.3 App Router / API routes

**CO:**
- **App Router** = souborové routování: složka v `src/app/` = URL cesta. `src/app/page.tsx` → `/`, `src/app/api/.../route.ts` → HTTP endpoint.
- **API routes** = backend ve stejném projektu (`GET /api/jobs` → JSON). Route = HTTP endpoint.

**JAK (analogie):** File-based routing = složka je URL. API route = endpoint, jako bys psal Flask/FastAPI handler.

**EFEKT (EROI):** Autor nezná web backend. App Router + API routes = web backend v jednom projektu, bez separátního serveru.

### 15.4 Server Components / Client Components

**CO:** Rozdělení kódu podle toho, kde běží:
- **Server Component** — kód běží na serveru (přístup k DB, bez JS v prohlížeči)
- **Client Component** — kód běží v prohlížeči (interaktivita, state)

**EFEKT (EROI):** Klíčové pochopení Next.js — ne vše běží v prohlížeči; část logiky běží serverově (bezpečnější, rychlejší).

### 15.5 SSR / ISR / CSR

**CO:** Způsoby renderování stránek:
- **SSR (Server-Side Rendering)** — HTML generováno na serveru při requestu
- **ISR (Incremental Static Regeneration)** — statické stránky s periodickou regenerací
- **CSR (Client-Side Rendering)** — HTML generováno v prohlížeči z JS

**EFEKT (EROI):** Volba renderování = kompromis výkon vs čerstvost vs interaktivita. Základní frontend ontologie.

### 15.6 Tailwind CSS

**CO:** Utility-first CSS framework. Místo psaní CSS tříd v souborech píšeš utility třídy přímo do HTML (`flex`, `p-4`, `text-lg`).

**JAK (analogie):** "Analogie: bez Bootstrap" — Tailwind = utility (stavební bloky), Bootstrap = hotové komponenty.

**EFEKT (EROI):** Styling bez psaní CSS od nuly. Autor má HTML+CSS renderer (Calibri/A4) — Tailwind je podobný koncept, pro web.

### 15.7 Vercel

**CO:** Hosting platforma pro Next.js (serverless). Nativní deployment bez správy serveru.

**JAK (analogie):** Vercel ≈ Cloud Run (serverless, autor zná), ale specializovaný na Next.js.

**EFEKT (EROI):** Deployment standalone produktu = push do gitu → live. (Viz též 19.1 PaaS.)

### 15.8 NDJSON streaming

**CO:** Newline-Delimited JSON — **postupné posílání dat po řádcích**, každý řádek je samostatný JSON objekt. Alternativa k poslání celého JSON pole najednou.

**JAK (analogie):** Místo "pošlu 1000 řádků najednou, pak počkáš" → "pošlu řádek po řádku, jak je generuji". Uživatel vidí data dřív.

**EFEKT (EROI):** Streaming = postupné doručování dat. Užitečné pro long-running generování (reporty, hromadné výstupy).

---

## 16. Monorepo & Workspaces

> **Kontext vzniku:** outprep — oddělení zodpovědnosti (web ≠ ETL) se sdílenou instalací závislostí. Autor zná multi-repo (každý MCP zvlášť); workspaces = nový koncept.

### 16.1 Monorepo

**CO:** Jedno git repo s **více balíčky**. Místo 3 repozitářů (web, engine, ETL) máš 1 repo se strukturou:
```
outprep/
  src/                    # Next.js web
  packages/engine/        # @outprep/engine — core logika (TS lib)
  packages/fide-pipeline/ # @outprep/fide-pipeline — ETL/CLI
  packages/harness/       # CLI pro accuracy testy
```

**PROČ:** Oddělení zodpovědnosti, sdílená instalace závislostí, samostatná testovatelnost. Změna v core → vidíš dopad na všechny balíčky v jednom PR.

**JAK (analogie pro autora):** oddělit `run_etl.py` (ETL) od web UI v samostatných balíčcích, sdílet `core` logiku (matcher, report renderer).

**EFEKT (EROI):** Monorepo = organizace projektů. Opak autorovy praxe (každý MCP = vlastní repo).

### 16.2 npm workspaces

**CO:** Mechanismus npm pro monorepo — jedno `node_modules` na úrovni rootu, sdílené napříč balíčky. `npm install` na rootu nainstaluje závislosti všech `packages/*`.

**PROČ:** Sdílené závislosti bez duplicit, lokální propojení balíčků (`@outprep/engine` je importovatelný z webu bez publish).

**EFEKT (EROI):** Workspaces = "jedna instalace, mnoho balíčků". Základ monorepo workflow.

---

## 17. Databáze & SQL

> **Kontext vzniku:** SKILL_GAPS v2 — nový gap (PostgreSQL). Klíčový insight: autor ukládá výstupy do `output/*.json,.md` souborů. **Soubory nejsou databáze.** Pro historii, dedup, vztahy a dotazování potřebuje DB.

### 17.1 PostgreSQL / relační databáze

**CO:** **Relační databáze** (open-source) — data v tabulkách, dotazování SQL. Standard pro produkční aplikace. Zvládá i **JSONB** (flexibilní data bez strict schématu) → hybrid relační + NoSQL.

**PROČ:** Soubory (`output/*.json`) nemají historii, vztahy, dedup, dotazování. PostgreSQL nabízí: "co bylo minulý týden?", JOIN tabulek, UNIQUE index (nativní dedup), řádky s metadaty.

**JAK (porovnání soubory vs DB):**

| Soubory | PostgreSQL |
|---------|-----------|
| Žádná historie s dotazováním | Dotazy: "co bylo minulý týden?" |
| Žádné vztahy (inzerát ↔ query) | JOIN tabulek |
| Dedup ručně (correlation_cache) | UNIQUE index (nativní) |
| Soubory se hromadí | Řádky s metadaty, mazání podle relevance |

**EFEKT (EROI):** Produkční perzistence standalone produktu. SQL = univerzální dovednost (platí pro všechny DB).

### 17.2 Tabulka / řádky / sloupce

**CO:** **Tabulka** = struktura dat (sloupce = typy, řádky = data). Jeden řádek = jeden záznam (např. jeden inzerát).

**JAK (analogie):** Tabulka ≈ Excel sheet. Sloupec = typ (TEXT, INTEGER, DATE), řádek = řádek dat.

**EFEKT (EROI):** Základní ontologie relačních dat — pochopení tabulky je 50 % SQL.

### 17.3 PRIMARY KEY / SERIAL / FOREIGN KEY

**CO:**
- **PRIMARY KEY** — jedinečný identifikátor řádku (`id INTEGER PRIMARY KEY`)
- **SERIAL** — auto-increment ID (Postgres automaticky zvyšuje číslo)
- **FOREIGN KEY / REFERENCES** — vztah mezi tabulkami (odkaz na řádek jiné tabulky)

**JAK (analogie):** PRIMARY KEY = rodné číslo řádku. SERIAL = automatické číslování (autoincrement). FOREIGN KEY = "tento inzerát patří do query č. 5" — odkaz na cizí tabulku.

**EFEKT (EROI):** Klíče = identifikace (PK) a vztahy (FK). Bez nich nejsou vztahy mezi daty.

### 17.4 INDEX / UNIQUE INDEX

**CO:**
- **INDEX** — datová struktura pro zrychlení dotazů (vyhledávání bez procházení všech řádků)
- **UNIQUE INDEX** — index + omezení: hodnota se nesmí opakovat → **nativní dedup**

**JAK (analogie):** INDEX = rejstřík v knize (najdeš stránku bez čtení celé knihy). UNIQUE INDEX = "tato hodnota už existuje → chyba" — automatický dedup.

**EFEKT (EROI):** UNIQUE INDEX na URL = nativní dedup inzerátů, nahrazuje ruční correlation_cache. Klíčový insight pro MCP-jobs.

### 17.5 JSONB

**CO:** JSON sloupec v Postgres — uloží celý JSON objekt jako data, **dotazovatelný**. Flexibilní data bez strict schématu.

**JAK (analogie):** V tabulce máš i sloupec, kam můžeš uložit "cokoliv ve formátu JSON" (celý profil, metadata) a pak se v něm dotazovat.

**EFEKT (EROI):** JSONB = hybrid relační + NoSQL — flexibilita JSONu s výhodami databáze. (`profile_json JSONB` — celý objekt.)

### 17.6 Migrace

**CO:** Evoluce schématu databáze — změny struktury tabulek v čase. `CREATE TABLE IF NOT EXISTS` (idempotentní), `ALTER TABLE` (přidání/změna sloupce).

**PROČ:** Databáze se vyvíjí s aplikací. Migrace = **verzované, opakovatelné změny schématu** — ne ruční ALTER v produkci.

**EFEKT (EROI):** Migrace = "git pro schéma". Idempotentní (viz 8.1) = bezpečně opakovatelná.

### 17.7 TOAST

**CO:** Komprese velkých polí v Postgres (The Oversized-Attribute Storage Technique). Velké hodnoty (např. PGN texty) se automaticky kompresují a ukládají mimo hlavní tabulku.

**EFEKT (EROI):** Proč Postgres zvládne velké texty bez zpomalení tabulky. Interní detail, ale vysvětluje výkon.

---

## 18. DevOps & Deployment

> **Kontext vzniku:** SKILL_GAPS v2 — nový gap (DevOps). Klíčový insight: MCP-jobs spouští ručně z IDE. **Produkční ELT běží sám** — denně v noci scrapne, zpracuje, uloží. Ráno otevře web a vidí výsledky.

### 18.1 DevOps

**CO:** **Propojení vývoje (Dev) a provozu (Ops).** Konkrétně: scheduling (automatizace ELT), monitoring (vědět, že pipeline běží), deployment (nasazení), CI/CD (automatický build+test na push), konfigurace mimo kód (.env, porty).

**PROČ:** Ruční spouštění z IDE ≠ produkční pipeline. Produkční ELT běží sám — esence automatizace.

**EFEKT (EROI):** DevOps = vrstva, která dělá produkt "produkčním". Autor ji nemá → nový gap.

### 18.2 Scheduler / Cron

**CO:** Automatický plánovač úloh. **Cron** = formát `minuta hodina den měsíc den_tydne` (`0 6 * * 1` = pondělí 6:00). **Vercel Cron** = serverless cron v `vercel.json`. (Detaily Cron viz 9.5.)

**PROČ:** ELT musí běžet sám, ne ručně z IDE. Cron = plánovač v OS/cloud.

**EFEKT (EROI):** Scheduler = "kdy se co má spustit". Základ automatizace ELT.

### 18.3 Monitoring / healthchecks.io

**CO:** **Monitoring** = sledování stavu systému. **healthchecks.io** = dead-man's-switch monitoring: služba pingne healthchecks.io, pokud běží. Pokud ping nedorazí (spadla) → **alarm (email)**.

**JAK (analogie):** Dead-man's-switch = "zvonek, který bije, dokud držíš tlačítko. Přestaneš mačkat → zazvoní alarm." Cron mlčí = nevíš, jestli běží. healthchecks.io pošle email.

**EFEKT (EROI):** Vědět o selhání **dřív než uživatel**. `fetch(process.env.HEALTHCHECKS_TWIC_URL)` po úspěšném běhu.

### 18.4 Docker / image / container / docker-compose

**CO:**
- **Docker** = zabalená aplikace + závislosti (kód, runtime, knihovny, konfigurace)
- **Image** = šablona (statický balíček)
- **Container** = běžící instance image
- **docker-compose** = více služeb v jednom souboru (`postgres + web + etl` jedním příkazem)

**JAK (analogie):** Image = ISO instalačka, Container = nainstalovaný běžící program. Compose = "spusť celý stack" (postgres:16, porty 5432:5432).

**EFEKT (EROI):** Reprodukovatelnost — stejné prostředí všude (lokal, server, cloud). Autor zná Docker→Cloud Run; compose multi-service = nové.

### 18.5 Porty / loopback

**CO:**
- **Port** = číslo, na kterém služba poslouchá (80/443 HTTP, 5432 Postgres, 3000 Next dev)
- **Loopback (localhost)** = síť jen lokálního počítače (127.0.0.1)

**JAK (analogie):** Port = dveře do služby (čísla domů v síti). Loopback = komunikace uvnitř vlastního počítače.

**EFEKT (EROI):** Základ síťové ontologie. `5432:5432` v docker-compose = mapování portu host → kontejner.

### 18.6 GitHub Actions / CI/CD pipeline

**CO:** CI/CD platforma na GitHubu — `.github/workflows/*.yml`. Na push spustí build+test (lint, pytest). (Základ CI/CD viz 9.1-9.2.)

**PROČ:** Autor nemá CI. Build+test na push = chytí regrese dřív, než se rozbije produkce.

**EFEKT (EROI):** CI = automatický build+test na každý push. GitHub Actions = nativní implementace.

### 18.7 husky / lint-staged

**CO:** Git hooks (před commit):
- **husky** — spouští skripty při git událostech (pre-commit)
- **lint-staged** — spustí lint/formát jen na **staged soubory** (rychlé, ne na celý repo)

**JAK (analogie):** Pre-commit hook = kontrola před odchodem z domu (zámek, světla). lint-staged = kontroluje jen věci v kufru, ne celý dům.

**EFEKT (EROI):** Lokální guardrail (viz 8.3) — chytí chyby před commitem, ne v CI. Levná prevence drahých chyb.

---

## 19. Cloud & PaaS

> **Kontext vzniku:** SKILL_GAPS v2 — AZ-900 rozšířeno o PaaS kontext. Insight: autor už používá PaaS koncepty (Vercel, Neon, Docker) **bez vědomí, že to jsou PaaS**. AZ-900 dá názvosloví a framework.

### 19.1 PaaS (Platform as a Service)

**CO:** Platforma, která hostuje aplikaci **bez správy infrastruktury** (bez VM, OS, updatů). Nahraj kód → běží.

**JAK (analogie):** PaaS = pronájem hotové kuchyně (spotřebiče, voda, plyn jsou zařízené). Ty jen vaříš (nahraješ kód). Ops (správa kuchyně) řeší platforma.

**Příklady (autorovy zkušenosti):** Cloud Run, Vercel, App Service. Analogie: Vercel ≈ App Service (Azure PaaS), Neon ≈ Azure Database for PostgreSQL.

**EFEKT (EROI):** Pochopíš, že to, co už používáš (Vercel, Neon, Cloud Run), má název: PaaS. AZ-900 = názvosloví + framework. Přechod na Azure = přejmenování terminologie.

### 19.2 Serverless

**CO:** Běží na cloudu **bez správy serveru** — platíš jen za skutečné běhy (scale to zero). (Detaily viz 12.4/9.9.)

**JAK (analogie):** Serverless = elektřina — platíš za spotřebu, ne za elektrárnu. Vercel, Neon, Cloud Functions.

**EFEKT (EROI):** Serverless je podmnožina PaaS modelu. Autor ho už používá (Cloud Run) — termín jen pojmenovává praxi.

### 19.3 Provider-agnostic

**CO:** Návrh, který **funguje s jakýmkoli hostem** bez změny kódu. Příklad: `DATABASE_URL` env proměnná — připojení k lokálnímu Dockeru i Neon/Supabase/Railway je stejné.

**JAK (analogie):** Provider-agnostic = nabíječka USB-C — funguje s každým adaptérem, ne jen jedním značkovým.

**EFEKT (EROI):** Konfigurace mimo kód (.env) = přenositelnost mezi providery. Protiklad lock-inu (vázanosti na jednoho providera).

### 19.4 Environment variables (.env)

**CO:** Konfigurace **mimo kód** — hodnoty v `.env` souboru (nikdy v gitu). `DATABASE_URL=postgres://user:pass@localhost:5432/db`.

**PROČ:** Kód je stejný pro všechny prostředí (lokální, produkce); liší se jen konfigurace. Secret (heslo, API klíč) patří do .env, ne do kódu.

**EFEKT (EROI):** Autor už zná (AGENTS.md security) — potvrzeno. Základ konfigurace produkčních aplikací.

---

## Metadata

- **Tags:** `#swe`, `#glossary`, `#terminologie`, `#ontologie`, `#edu`, `#concurrency`, `#testing`, `#web-scraping`, `#python`, `#cicd`, `#design-patterns`, `#llm`, `#observability`, `#ml`, `#frontend`, `#nextjs`, `#monorepo`, `#databaze`, `#sql`, `#devops`, `#docker`, `#paas`, `#cloud`
- **EROI:** 9/10 (živý edukační artefakt; náklad = údržba, benefit = trvalá adopce terminologie → překonání unknown unknowns)
- **Živý dokument:** průběžně doplňovat nové termíny z dev workflow.

## Jak doplňovat nový termín (návod pro autora i LLM)

1. Najdi v kontextu zvýrazněný termín (`**termín**`).
2. Ověř, zda už není v tomto dokumentu (grep) — **P1 pravidlo, žádné duplicity**.
3. Pokud není, doplň novou sekci s šablonou: **CO / PROČ / JAK (analogie) / EFEKT (EROI)**.
4. Zvýrazni termín boldem a uveď kontext, ve kterém ses s ním setkal.
5. Pokud je v artefaktu vysvětlení, zachovej jádro a rozšiř.

### Rozšířená šablona (v2.1 — zjištění z ADOPCNI_METODOLOGIE_2026_v1)

Kromě základní struktury CO/PROČ/JAK/EFEKT doplň u každého nového termínu:

| Položka | Pravidlo |
|---------|----------|
| **Kdy použít / Kdy NE** | Architektonické rozhodování — terminologie bez rozhodovacího prahu je pasivní znalost |
| **Protiklad / záměna** | "Singleton ≠ statická třída", "Mock ≠ fake", "Cache invalidation ≠ eviction" — nejčastější chyby vznikají záměnou |
| **Odkaz na kód** | Konkrétní místo v repozitářích, kde se termín reálně používá (např. `engine_client.py:205`) |
| **Koncept mapa** | 1-řádkový vztah k okolním pojmům (např. `race condition → lock → mutex → deadlock → timeout`) — viz Concept Mapping v adopční metodice |

**SRS provázání:** každý nový termín je zdrojem pro 1-2 Anki flashcards (opakování v intervalech 1→3→7→14 dní). Termíny bez reálného kontextu se do glossary NEzapisují (kvalita > kvantita, anti-akumulace).
