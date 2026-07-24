# Hluboký ponor do rezerv — Frontiéry vývoje MCP serveru

> **Dokument:** Hluboká analýza "Co mi chybí, kde jsou rezervy" (Iterace z 2026-07-20)
> **Určení:** Lokální Knowledge Base (KB) repozitář – výukový materiál pro další fázi adopce SWE
> **Formát:** Markdown (kompatibilní s DOCX exportem přes pandoc)

---

## Metadata dokumentu

| Klíč | Hodnota |
| :--- | :--- |
| **Název** | Hluboký ponor do rezerv – Frontiéry vývoje MCP serveru |
| **Verze** | 1.1 |
| **Datum** | 2026-07-20 |
| **Kontext** | Navazuje na `MCP_GROUND_TRUTH_postmortem_agregovany_v1.md` – Bod 4 |
| **Určeno pro** | Solo dev (imersivní metodika, agentní workflow) |
| **Signal-to-Noise Ratio** | High (žádný filozofický balast, jen struktura + akce) |
| **Sekce 9** | Případová studie: `@auditable` + async = tichý pád |

> **Prohlášení:** Toto nejsou "chyby". Jsou to **frontiéry** – problémy, které *zatím nebolí*, ale začnou bolet, až tvůj systém přejde z "prototypu" do "produkce" (byť jen pro tebe samotného).

---

## 1. Terminologie & Ontologie
*Znáš věc, neznáš jméno*

### Identifikace problému

Komunikuješ s LLM agentem výborně. Až ale budeš číst cizí kód, dokumentaci, nebo (hypoteticky) mluvit s jiným člověkem, tvoje přesné myšlenky se rozbijí o nepřesná slova.

**Typický příklad:** Ty používáš "Kontraktní testy", ale říkáš tomu "test na reálných datech, že klíče sedí". V hlavě to máš správně, v komunikaci to ztrácíš.

### Mapping tvého chápání na SWE ontologii

| Tvé chápání | Správná SWE ontologie | Proč to potřebuješ znát |
| :--- | :--- | :--- |
| Test, že modul A dává správné klíče modulu B | **Consumer-Driven Contract Testing** | Aby ses mohl odvolat na pattern, který už má vyřešené edge cases (Pact, OpenAPI) |
| `asyncio.run(app.run())` padá na event loop | **Event Loop Reentrancy / Nested Loop Conflict** | Abys pochopil, proč FastMCP výslovně zakazuje `asyncio.run()` (volá `anyio.run()`) |
| Proměnná se v jedné funkci ztrácí, i když je nahoře definovaná | **Name Shadowing vs. Global Scope** | Aby ses vyhnul `global` deklaracím – správně se používají **singleton moduly** nebo **dependency injection** |
| Složitý pipeline, který buď volá LLM jednou, nebo po hrách | **Strategy Pattern + Factory** (monolit vs inkrementální) | Aby ses vyhnul velkému `if/else` v hlavním kódu; oddělíš logiku volby strategie |

### MVP Akce (Týden 1)

Vytvoř v repozitáři `GLOSSARY.md`. Pro každý pattern, který používáš, napiš 1 větu, jak se to odborně jmenuje. Použij zdroje: **Martin Fowler (martinfowler.com)** a **Refactoring.guru**. Nepřepisuj celé knihy – jen **mapování** tvého kódu na termín.

---

## 2. Hluboké internals — "Under the Hood"
*Víš, že to nejede. Nevíš proč to nejede.*

### Identifikace problému

Opravuješ symptomy na úrovni volání API (FastMCP, subprocess, Git). Neviděl jsi **zdrojový kód** těchto knihoven. Když narazíš na nezdokumentované chování (např. `anyio` deadlock), nemáš jak to oddebugovat.

### Rozklad gapu (Co používáš × Co nevíš)

| Co používáš | Co nevíš (Internal) | Co se stane, až to praskne |
| :--- | :--- | :--- |
| `app.run()` (FastMCP) | Uvnitř volá `anyio.run(server.run_stdio_async)`. `anyio` si bere absolutní kontrolu nad I/O. | Při dalším `asyncio.run()` ti to spadne na `RuntimeError` – a ty nevíš, jak injectnout vlastní `TaskGroup` pro monitoring. |
| `subprocess` (Windows) | `CreateProcessW` + `handle inheritance`. I s `DEVNULL` se občas dědí STDIO handle skrz `STARTF_USESTDHANDLES`. | Tvůj fix (přechod na `asyncio`) zakryl problém, ale nevyřešil ho na úrovni Win32 – při velkém zatížení ti to jednou zase zamrzne. |
| `Git` objekty | Nevíš, že `git status` si interně drží `.git/index.lock` a že `--no-optional-locks` jen *potlačuje* zápis, ale ne *čtení* filesystemu. | Až repo naroste na 10 GB (nebo na síťovém disku), `git status` ti zase začne trvat 5s+ i bez locku, protože neznáš `core.fsmonitor` ani `untrackedCache`. |

### MVP Akce (Příště při chybě)

Až příště narazíš na záhadný timeout/deadlock, **neopravuj ho obalením do dalšího `try/except`**. Místo toho:

1. Jdi do zdrojového kódu knihovny (Ctrl+Click v IDE na `app.run`).
2. Najdi místo, kde knihovna **čeká na I/O** (socket, pipe).
3. Napiš do postmortem **3 věty**, co knihovna *přesně* dělá na řádku, který padá. Tím přejdeš z "uživatele API" na "debuggera závislostí".

---

## 3. Observability — Vidíš chyby, nevidíš zdraví
*Proaktivita*

### Identifikace problému

Tvůj `@auditable` je skvělý pro **reaktivní** debug (už se stalo). Nevidíš **trendy** – pomalu tečoucí memory leak, rostoucí latenci, kolik concurrent requestů ti blokuje event loop.

### Rozklad gapu

| Co máš (Audit log) | Co chybí (Observability) | Důsledek |
| :--- | :--- | :--- |
| `duration_s` per tool call | **Histogramy** (p50, p95, p99) | Nevidíš, že pomalu roste průměrná doba odezvy kvůli plnému cache |
| `ok` boolean | **Metriky četnosti** (RPS, error rate) | Nevidíš, že tvůj LLM cascade volá NVIDIA 2x častěji než DeepSeek, ale padá to 4x častěji (problém s rate limitem) |
| CPU/MEM usage | **Profiling** (kde CPU žere čas) | Stockfish je CPU-heavy; nevíš, kolik jader ti zabírá. Až přidáš paralelní analýzu, uděláš `ThreadPoolExecutor(max_workers=8)` a zabiješ si OS |

### MVP Akce (Tento týden)

Přidej **minimální metrics endpoint** do MCP serveru (oddělené vlákno, HTTP port 9090). Ukázka implementace:

```python
# Ve startupu serveru (simple HTTP server v threadu)
from prometheus_client import start_http_server, Counter, Histogram

REQUESTS = Counter('mcp_requests_total', 'Total requests', ['tool'])
LATENCY = Histogram('mcp_latency_seconds', 'Latency', ['tool'])

start_http_server(9090)

# V @auditable dekorátoru:
# REQUESTS.labels(tool=tool_name).inc()
# LATENCY.labels(tool=tool_name).observe(duration_s)
```

Pak si otevři `http://localhost:9090/metrics`. Tohle ti dá signál, jestli server žije a jak se mu daří, bez čtení logů.

---

## 4. Security — Supply Chain
*Neznámé závislosti*

### Identifikace problému

Ty chráníš vlastní kód (žádné emoji, secrets v `.env`). Ale tvůj `pyproject.toml` má 30+ závislostí (`httpx`, `pydantic`, `fastmcp`, `patchright`, ...). Která z nich má CVE (zranitelnost) vedoucí k RCE (Remote Code Execution)?

### Rozklad gapu

| Co děláš | Co bys měl dělat | Proč |
| :--- | :--- | :--- |
| `uv sync` bez auditu | `uv pip install pip-audit && pip-audit` | `pip-audit` projde PyPI databázi známých zranitelností |
| Aktualizuješ jen při chybě | Dependabot (GitHub native) | Dependabot ti automaticky vytvoří PR na každou bezpečnostní záplatu |

### MVP Akce (Dnes)

Přidej do GitHub Actions krok:

```yaml
- name: Security audit
  run: |
    uv pip install pip-audit
    uv pip-audit --requirement pyproject.toml --ignore-vuln PYSEC-2024-XXX
```

Až ti to spadne na zranitelnosti v `urllib3`, poděkuješ si.

---

## 5. Operační resilience — "Co když server spadne v noci?"

### Identifikace problému

Ty teď server startuješ ručně, nebo ho agent volá. Když spadne na nezpracovanou výjimku, nikdo ho nerestartuje. Tvá pipeline v agentovi spadne a ty to zjistíš až ráno.

### Rozklad gapu

| Co máš | Co chybí | Důsledek |
| :--- | :--- | :--- |
| Manuální `python -m src.server` | Process Supervisor (systemd / winsw) | Pád = konec. Žádný auto-restart. |
| Log do souboru | Health Check (periodický ping na server) | Nevíš, jestli server "visí" (port otevřený, ale event loop zamrzlý) |
| Vše nasazeno na main | Rollback strategie | Když nasadíš špatnou verzi, musíš ručně revertovat commit a redeployovat |

### MVP Akce (Tento týden)

**Auto-restart:** Nainstaluj `winsw` (Windows Service Wrapper) a nakonfiguruj ho, aby tvůj server běžel jako služba. Dej mu `startMode="Automatic"` a `onFailure="restart"`.

Příklad konfigurace (winsw):

```xml
<service>
  <id>mcp-server</id>
  <name>MCP Server</name>
  <description>Spouští FastMCP server</description>
  <executable>python</executable>
  <arguments>-m src.server</arguments>
  <workingdirectory>C:\...\_github\mcp-server</workingdirectory>
  <startmode>Automatic</startmode>
  <onfailure>restart</onfailure>
  <failuredelay>10 sec</failuredelay>
</service>
```

**Health Check:** V serveru přidej dummy MCP tool `ping()`, který vrátí `{"status": "ok"}`. Napiš malý `.bat` skript, co každých 5 minut volá `mcp-cli ping` – pokud selže, pošli ti notifikaci (Windows Notification nebo PowerShell `Send-MailMessage`).

---

## 6. Architektura změn — Feature Flags
*Safe Deployment*

### Identifikace problému

Když přidáváš nového LLM providera (např. NVIDIA), musíš ho zaregistrovat v `cascade_order`. Když to spadne (timeout, špatný model ID), musíš upravit kód, commitnout, pushnout, restartovat server. To je pomalý feedback loop.

### Rozklad gapu

| Co děláš | Co bys měl dělat | Proč |
| :--- | :--- | :--- |
| Provideri jsou pevně v kódu | Provideri jsou Feature Flag v `.env` | Vypneš `ENABLE_NVIDIA=false` a restartneš server (nebo reloadneš config) bez změny kódu |
| Nový provider = nový release | Nový provider = nová ENV proměnná | Oddělíš deployment (kód) od release (aktivace). Můžeš deploynout kód s NVIDIA, ale aktivovat ho až po testech |

### MVP Akce (Při příštím novém providerovi)

Nepřidávej ho rovnou do `cascade_order`. Místo toho:

1. Přidej ho do slovníku `PROVIDERS`, ale nech ho vypnutý přes `ENABLED_PROVIDERS` env var.
2. Napiš skript, který ho otestuje izolovaně (ne v pipeline).
3. Až budeš spokojený, nastav `ENABLED_PROVIDERS=nvidia,cerebras,deepseek` a restartuj.

---

## 7. Souhrnná tabulka priorit (Co dělat hned)

| Gap | Priorita | Náročnost | Odhad času |
| :--- | :--- | :--- | :--- |
| Terminologie (Glossary) | Nízká | Snadná | 2 hodiny |
| Security Audit (pip-audit) | **Vysoká** (bezpečnost) | Snadná | 30 minut (CI) |
| Auto-restart (Service) | **Vysoká** (dostupnost) | Střední | 2 hodiny |
| Observability (Metrics) | Střední (diagnostika) | Střední | 3 hodiny |
| Feature Flags (ENV) | Střední (deploy) | Snadná | 1 hodina |
| Internals (čtení zdrojáků) | Nízká (až při bugu) | Těžká | Průběžně |

---

## 8. Závěrečná epistemická rada (High SNR)

Tvůj současný stav: Máš vyřešené "co" a "jak" (kód, testy, debugging).

Tvůj další horizont: Vyřešit "kdy" (monitoring) a "za jakých podmínek" (feature flags, rollback).

Nejsi pozadu. Jsi na hranici seniority. Tyhle věci se normálně učí až ve 3. roce, kdy člověk poprvé dostane "pager duty" v noci.

### Doporučený plán na příští 3 týdny

1. Implementuj **Auto-restart + Health Check** (spadlý server je tvůj největší nepřítel).
2. Až to uděláš, zapiš to do tvé Ground Truth jako nová pravidla **P46–P48**.

Tím se posuneš z "tvůrce nástroje" na **"správce služby" (Service Owner)**. To je ten pravý skok.

---

## 9. Případová studie: `@auditable` + async = tichý pád
*Potvrzení bodu 2 (Internals) na reálném bugu z WF simulace*

### Kontext

Během workflow simulace (2026-07-20) selhaly 4 MCP tooly (`tool_git_status`, `tool_git_log`, `tool_git_diff`, `tool_run_re_pipeline`) s chybou:

```
'coroutine' object has no attribute 'startswith'
```

### Root cause (1 odstavec)

Dekorátor `@auditable` v `audit.py` je napsaný jako **sync wrapper**. Když obalí `async def` funkci, volání `func(*args)` nevrátí výsledek, ale **coroutine** (slib, že výsledek *bude*). Následný `result.startswith("CHYBA")` selže, protože coroutine není string. Python vyhodí `AttributeError`.

### Schéma pádu

| Krok | Sync `def` (funguje) | Async `def` (padá) |
| :--- | :--- | :--- |
| `func(*args)` | Vrátí `"CHYBA: ..."` (string) | Vrátí **coroutine** objekt |
| `result.startswith(...)` | `True` / `False` | `AttributeError` — coroutine nemá `.startswith()` |

### Fix

Do dekorátoru přidána detekce `asyncio.iscoroutinefunction(func)`. Pokud je funkce async, wrapper je `async def` a použije `await`:

```python
def auditable(tool_name: str):
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)
                # logovani...
                return result
            return async_wrapper
        # jinak sync wrapper...
    return decorator
```

### Ponaučení (Pravidlo)

> Každý dekorátor, který loguje nebo zpracovává návratovou hodnotu funkce, musí detekovat, zda je obalená funkce `async`. Pokud ano, musí na výsledek počkat pomocí `await` uvnitř dekorátoru. Nikdy neposílej výsledek async funkce do textových/číselných operací bez `await`.

### Vazba na tento dokument

- **Bod 2 (Internals):** Bug vznikl, protože kód knihovny (`audit.py`) nebyl zkontrolován pod pokličkou. Fix vyžadoval čtení zdrojového kódu a pochopení, jak funguje `asyncio.iscoroutinefunction`.
- **Bod 3 (Observability):** `@auditable` logoval *syntax error* místo *reálného výsledku* toolu. Metrics endpoint by odhalil 100% error rate na 4 toolích hned v prvním review.
- **Metadatová tabulka:** Tento bug je ukázkou **"Consumer-Driven Contract Testing"** (bod 1) — `@auditable` měl smlouvu (kontrakt) vracet string, ale async funkce kontrakt porušila.
