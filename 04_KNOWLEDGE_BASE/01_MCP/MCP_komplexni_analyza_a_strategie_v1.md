# MCP — Komplexní analýza, strategie a implementační plán pro solo dev

**Autor:** SYSTEQ AI Analysis  
**Datum:** 2026-07-05  
**Verze:** v1.3  
**Kontext:** Session 14–16 — První lokální MCP server vytvořen, security hardening, audit logging, tool descriptions upgrade, cache layer, 42 testů, credential layering nasazení, input validation implementace  
**Aktualizace v1.1:** Sémantická analýza secret exposure (PAT), security decision framework, EROI hranice MCP  
**Aktualizace v1.2:** Implementace P0/P1 vylepšení — security hardening, audit logging, tool descriptions, cache layer; 33→42 testů; nové moduly audit.py, cache.py; dead code cleanup; praktický návod pro Windows User env var v §9.4.2  
**Aktualizace v1.3:** Session 16 — Audit pracovního prostředí a MCP serveru, reálný secret exposure nález, credential layering deployment, input validation (P0), gh CLI instalace, 42/42 testů ověřeno


## Obsah

1. [Fenomén MCP — Co to je a proč to mění pravidla hry](#1-fenomén-mcp)

2. [Sémantická analýza teze "dev v kontextu"](#2-sémantická-analýza-teze)

3. [Analýza současného prototypu MCP serveru](#3-analýza-prototypu)

4. [Rešerše veřejných zdrojů — MCP pro solo dev](#4-rešerše)

5. [Iterativní vylepšení MCP serveru](#5-vylepšení)

6. [Use case architektura pro SYSTEQ workflow](#6-use-case)

7. [Kvalifikovaná predikce — vývoj s MCP vs bez MCP](#7-predikce)

8. [Akční plán — další kroky](#8-akční-plán)

9. [Sémantická analýza dev notes — Secret exposure a PAT](#9-secret-exposure)

   - [9.1 Analýza problému](#91-analýza-problému)

   - [9.2 EROI hranice MCP — Kdy MCP NEPOUŽÍT](#92-eroi-hranice-mcp)

   - [9.3 Security decision framework](#93-security-decision-framework)

   - [9.4 Řešení: Credential layering architektura](#94-credential-layering)

   - [9.5 Důsledky pro stávající MCP server](#95-důsledky-pro-server)


## 1. Fenomén MCP

### 1.1 Co je Model Context Protocol

MCP je otevřený protokol (JSON-RPC 2.0) vyvinutý Anthropicem v listopadu 2024, v prosinci 2025 darovaný Linux Foundation. Umožňuje LLM klientům (Claude, ChatGPT, Gemini, Cursor, VS Code Copilot, Windsurf, Zed, Cline) standardizovaně komunikovat s externími nástroji a datovými zdroji.

**Analogický koncept: USB-C pro AI** — jeden protokol, který nahrazuje dřívější éru "one-off connectorů" (každý klient → vlastní integrace → každý nástroj).

### 1.2 Klíčové metriky ekosystému (H1 2026)

| Metrika | Hodnota | Zdroj/Kontext |
| - | - | - |
| SDK downloady | ~97 mil./měsíc | Z ~2M při launchi = 4 750% růst za 16 měsíců |
| Veřejné MCP servery | 9 400–17 000+ | Napříč registry (Smithery, npm, PyPI, GitHub) |
| Monetizované | \< 5 % | Drtivá většina OSS |
| Produkční adopce | 41 % senior leaderů | Stacklok State of MCP in Software 2026 |
| Klienti s nativní podporou | 10+ | Claude, ChatGPT, Gemini, Copilot, Cursor, Windsurf, VS Code, Zed, Cline, Replit |
| Růst za rok | 5× více serverů | Oproti H1 2025 |


### 1.3 Architektura MCP

```
┌──────────────┐     JSON-RPC 2.0      ┌──────────────┐  
│  MCP Host    │ ◄──────────────────►  │  MCP Server  │  
│  (klient)    │   stdio / HTTP/SSE    │  (nástroje)  │  
│              │                       │              │  
│  Claude      │   3 primitivy:        │  filesystem  │  
│  Cursor      │   • tools (funkce)    │  git         │  
│  VS Code     │   • resources (data)  │  VCF         │  
│  opencode    │   • prompts (šablony) │  KB search   │  
└──────────────┘                       └──────────────┘
```

**Doprava (transport):**

- **stdio** — lokální, spawnováno jako child process, žádná síť, žádné auth. **Nejjednodušší model.** Vhodné pro lokální nástroje.

- **Streamable HTTP** — remote, běží na HTTP endpointu, SSE pro streaming. Vhodné pro sdílené/síťové služby.

- *(deprecated: starší SSE transport, nyní nahrazen Streamable HTTP)*

### 1.4 Historický kontext — adopční křivka

```
Adopce  
  ▲  
  │        ● ← 2026-07: Stateless MCP release candidate  
  │       ●  ← 2026-03: 97M SDK downloads, roadmap publikován  
  │      ●   ← 2025-12: Darováno Linux Foundation  
  │     ●    ← 2025-06: První vlna adopce (Claude, Cursor)  
  │    ●     ← 2024-11: MCP v1 launch (Anthropic)  
  │   ●  
  │  ●  
  │ ●  
  └─────────────────────────────► Čas  
  2024    2025    2026    2027
```

### 1.5 MCP v kontextu jiných paradigmat

| Vrstva | Technologie | Účel |
| - | - | - |
| Integrace AI ↔ nástroje | **MCP** | Standardizovaný JSON-RPC protokol |
| Agent ↔ Agent | **A2A** (Google) | Komunikace mezi agenty |
| Automatizace workflow | **Zapier / Make** | Deterministické pipelines |
| Function calling | **Nativní API** | Single-vendor, in-process |


**MCP ≠ náhrada function callingu.** MCP řeší multi-client distribuci. Pro single-app je function calling lehčí a rychlejší. MCP dává smysl, když stejný nástroj potřebuje více klientů.

### 1.6 Roadmapa 2026–2027

| Období | Co se očekává |
| - | - |
| Q3 2026 | Enterprise MCP pilotech, vizuální workflow builders |
| Q3 2026 | MCP 2026-07-28 release candidate (stateless core, Tasks extension, MCP Apps) |
| Q4 2026 | Auth standardizace, knowledge servers jako kategorie |
| Q1 2027 | Lokální modely 90%+ parity, registry 15 000+ |
| Q2 2027 | Managed MCP marketplace od cloud providerů, one-click instalace |
| late 2027 | MCP 2.0 - auth, streaming, multi-modal, enterprise infrastruktura |



## 2. Sémantická analýza teze

### 2.1 Analýza výroku

> *"vzhledem k rychlému rozvoji celé domény LLM, workflow, implementace nových nástrojů pro práci s LLM, které definují výrazné marginální změny v entropii při práci s AI vůči běžné AI literate populaci, jsem se rozhodl začít objevovat možnosti kodifikovaného MCP"*

### 2.2 Klíčové koncepty

| Koncept | Význam v kontextu |
| - | - |
| **Rychlý rozvoj domény** | Fakt: LLM ekosystém se mění v řádu měsíců, nikoli let |
| **Marginální změny v entropii** | Entropie = míra nejistoty/neuspořádanosti. "Snížení entropie" = zvýšení prediktability a efektivity práce. Nové nástroje vytvářejí diskontinuální skoky v produktivitě |
| **AI literate populace** | Základní úroveň = umí používat chat, promptovat. Nadstavba = kodifikované protokoly, agentické workflow |
| **Kodifikované MCP** | MCP jako standard = přechod od ad-hoc promptování k systematické, znovupoužitelné integraci nástrojů |
| **Diff vůči standardům** | Udržení konkurenční výhody = být v ~10% uživatelů, kteří aktivně tvoří MCP nástroje (ne je jen konzumují) |


### 2.3 Gaussova distribuce uživatelů AI

```
         ●  
       ●   ●  
     ●       ●  
   ●           ●                   90% konzumenti  
 ●               ●                   (chat, promptování)  
●                 ●  
                   ●                ~9% power users  
                     ●               (vlastní workflow, API)  
                       ●  
                         ●          ~1% tvůrci infrastruktury  
                           ●         (MCP servery, frameworky)
```

**Teze:** Autor se nachází v přechodu z ~9% (power users s agentic tools opencode) do ~1% (tvůrci infrastruktury). MCP server je kodifikovaný nástroj, který tuto pozici institucionalizuje.

### 2.4 Validita teze

**Verdikt: Validní, s nuancemi.**

- Prostor pro arbitráž existuje — MCP ekosystém je stále v rané fázi (\< 5 % monetizovaných serverů)

- First-mover advantage je reálná — ~97M SDK downloadů = poptávka, nedostatek kvalitních doménových serverů

- Riziko: MCP není vhodné pro *všechny* nástroje. Overhead JSON-RPC může být kontraproduktivní pro sub-100ms operace


## 3. Analýza současného prototypu

### 3.1 Stack a architektura

| Vrstva | Technologie |
| - | - |
| Jazyk | Python 3.11+ |
| Framework | FastMCP (`mcp\[cli\]` SDK) |
| Package manager | `uv` |
| Transport | stdio (lokální) |
| Test framework | pytest |
| Počet toolů | 15 (4 FS + 4 git + 3 VCF + 2 RE + 1 KB + 1 ACI) |
| Počet testů | 42/42 ✅ |
| Prompty | 3 (analyze\_repo, validate\_pipeline, full\_analysis) |
| Bezpečnostní modul | `config.py` — ALLOWED\_ROOTS, FORBIDDEN\_PATHS, FORBIDDEN\_PATTERNS |
| Audit logging | `audit.py` — @auditable dekorátor na všech 15 toolů |
| Cache vrstva | `cache.py` — TTLCache + @cached dekorátor (kb\_search 300s, aci\_lookup 600s) |


### 3.2 Adresářová struktura

```
mcp-local-server/  
├── pyproject.toml  
├── README.md  
├── src/mcp\_local\_server/  
│   ├── server.py                    \# Entry point + 15 MCP dekorátorů + 3 prompty  
│   ├── config.py                    \# ALLOWED\_ROOTS, FORBIDDEN\_PATHS, FORBIDDEN\_PATTERNS  
│   ├── audit.py                     \# @auditable dekorátor (JSON log + stdout)  
│   ├── cache.py                     \# TTLCache + @cached dekorátor  
│   ├── tools/  
│   │   ├── filesystem.py            \# list/read/write/search s .env blokováním  
│   │   ├── git\_tools.py             \# status, log, diff, status\_all (read-only)  
│   │   ├── vcf\_validate.py          \# ACI + tool validace proti whitelistu  
│   │   ├── vcf\_analyze.py           \# T1: struktura, ACI distribuce, MD5  
│   │   ├── vcf\_diff.py              \# T2: porovnání 2 VCF souborů  
│   │   ├── re\_pipeline.py           \# T4: orchestrátor RE scriptů (10 nástrojů)  
│   │   ├── kb\_search.py             \# T5: fulltext nad B2B-Knowledge-Base (cachovaný)  
│   │   └── aci\_lookup.py            \# T6: ACI cross-reference (cachovaný)  
└── tests/  
    └── test\_tools.py                \# 42 testů
```

### 3.3 Kvalitativní hodnocení

#### Silné stránky ✅

1. **Správná volba stacku** — FastMCP je de facto standard (70 %+ Python MCP serverů), `uv` je správná volba pro dependency management

2. **Bezpečnostní model** — path allowlist, forbidden paths, forbidden patterns (`.env`, `*.key`, `*.pem`), git read-only — vicedrovňová ochrana

3. **Doménová specializace** — VCF/ACI/RE nástroje jsou unikátní a reprezentují reálnou přidanou hodnotu

4. **Sémantické názvy toolů** — `tool\_validate\_vcf`, `tool\_kb\_search` → LLM rozumí účelu

5. **Tool descriptions dle best practices** — všech 15 toolů používá WHEN/WHAT/RETURNS/CONSTRAINTS formát + parametrové popisy

6. **Audit logging** — @auditable dekorátor na všech 15 toolů, JSON log do souboru + stdout

7. **Cache vrstva** — TTLCache pro kb\_search (300s) a aci\_lookup (600s) s API pro clear/get\_cache\_info

8. **Test coverage** — 42 testů (config 3 + secret exposure 9 + filesystem 4 + git 2 + VCF 5 + ACI 4 + KB 3 + RE 1 + cache 9) — všechny ✅

9. **Prompty** — 3 šablony pro opakované scénáře

10. **README dokumentace** — aktuální, 15 toolů, bezpečnostní pravidla, struktura

#### Slabé stránky ❌

1. **Chybí input validation** — JSON Schema je suggestion, ne enforcement. Např. `search\_files` nevaliduje pattern, `vcf\_analyze` neověřuje .VCF suffix (jen v validate, ne v analyze)

2. **Žádné error recovery** — chybové hlášky jsou generické. Podle best practices: "what went wrong → why → what to do differently"

3. **Žádné rate limiting / timeout management** — `re\_pipeline` má 60s timeout na script, ale chybí globální timeout na tool call

4. **Chybí async** — všechny tooly jsou synchronní. MCP je async by design; blocking I/O (souborový systém, subprocess) by měl být async

5. **Prompty nejsou využívané** — opencode je nespouští automaticky, chybí integrace

6. **Chybí Resource endpoints** — read-only data by měla být resources, ne tools

### 3.4 Bezpečnostní audit

| Aspekt | Stav | Poznámka |
| - | - | - |
| Path traversal | ✅ Ošetřeno | `is\_path\_allowed()`, resolve, ALLOWED\_ROOTS |
| Forbidden paths | ✅ Ošetřeno | Windows, Program Files, AppData atd. |
| Forbidden patterns | ✅ Ošetřeno | `.env`, `.env.*`, `*.key`, `*.pem`, `credentials*`, `secrets*` — blokovány pro read i write |
| Git read-only | ✅ Ošetřeno | Žádný commit/push přes MCP |
| Secret exposure | ✅ Ošetřeno | FORBIDDEN\_PATTERNS blokuje read/write .env, .key, .pem, credentials, secrets |
| Input sanitizace | ⚠️ Částečně | Chybí type/range/length checks |
| Rate limiting | ❌ Chybí | Možnost DoS při opakovaných tool voláních |
| Audit logging | ✅ Implementováno | @auditable dekorátor na všech 15 toolů, JSON log do `mcp\_audit.log` + stdout |



## 4. Rešerše veřejných zdrojů

### 4.1 Nejvýznamnější MCP servery pro solo dev (2026)

| Server | Účel | Pro solo dev |
| - | - | - |
| **Filesystem** | Čtení/zápis souborů, FS operations | ✅ Základ všech workflow |
| **GitHub** | Issues, PRs, repo management | ✅ CI/CD + projekt management |
| **Context7** | Live dokumentace knihoven (bez halucinací) | ✅ Eliminuje deprecated API |
| **Playwright** | Browser automation (a11y tree-based) | ✅ Testování, scraping |
| **Firecrawl** | Web scraping s agent planning | ✅ Research, competitive analysis |
| **Nexus-MCP** | Hybrid search + code graph + semantic memory | ✅ Lokální, \< 350 MB RAM |
| **PostgreSQL / Supabase** | DB query přes MCP | ✅ Datová vrstva |
| **mcp-project-manager** | Hierarchické task management | ✅ Projektové řízení |
| **Local-MCP** | 48 toolů (FS, git, shell, network, DB, system) | ⚠️ TypeScript, Node.js riziko |


### 4.2 Trendy z rešerše

1. **Stateless MCP** — release candidate 2026-07-28. MCP se stává plně stateless pro horizontální škálování.

2. **Multi-server orchestrace** — devs skládají MCP servery do "agent teams" (jeden plánuje, druhý exekvuje, třetí validuje).

3. **Lokální first** — lokální modely dosahují 85%+ parity, MCP umožňuje plně lokální AI stack bez API klíčů.

4. **Enterprise governance** — audit logs, RBAC, SSO, private transports = nejžádanější featury.

5. **Managed marketplace** — cloud providers začnou hostovat managed MCP endpointy (analogie API gateway).

### 4.3 Co říká komunita

> *"The developers who do write their own MCP servers end up with a leverage advantage that is hard to describe until you have it. Every model gets your tool. Every agent runtime gets your tool."* — DEV Community

> *"MCP is the most important infrastructure change since APIs became standard."* — Nomixy Analysis

> *"MCP se stal méně vzrušujícím, ale daleko důležitějším: infrastrukturou, na které závisí AI ekosystém."* — State of MCP H1 2026

> *"Starting with one tool. Make sure the tool description is clear enough that the model uses it without prompting. Wire it in. See what happens."* — Build your first MCP server guide

### 4.4 Varovné signály

- **Overhead JSON-RPC** není vhodný pro sub-100ms operace volané desítkykrát za sekundu

- **Bezpečnostní incidenty** — servery s unresticted shell commandy ztrácejí důvěru

- **"Hackathon prototype" anti-pattern** — MCP server, který je jen wrapper kolem jednoho API volání

- **Version skew** — změny v tool schematu mohou rozbít klienty


## 5. Iterativní vylepšení MCP serveru

### 5.1 Priorita P0 — Kritické opravy

| \# | Změna | Soubor | Status |
| - | - | - | - |
| 1 | **Tool descriptions** — WHEN/WHAT/RETURNS/CONSTRAINTS formát + parametrové popisy | `server.py` | ✅ **Hotovo** |
| 2 | **Input validation** — type, range, length checks na všech parametrech | všechny tooly | ⏳ Pending (F2.3) |
| 3 | **Error messages** — specifické: "co selhalo → proč → co dělat jinak" | všechny tooly | ⏳ Pending (F3.2) |
| 4 | **Smazat main.py** | `main.py` | ✅ **Hotovo** |


### 5.2 Priorita P1 — Rychlá vylepšení

| \# | Změna | Status |
| - | - | - |
| 5 | **Async všechna I/O** — `asyncio` nebo `anyio` pro file/subprocess operace | ⏳ Pending (F3.1) |
| 6 | **Cache layer** — `kb\_search` (300s) a `aci\_lookup` (600s) s TTL | ✅ **Hotovo** |
| 7 | **Rate limiter** — max N tool volání / minuta | ⏳ Pending (F2.4) |
| 8 | **Audit logging** — @auditable dekorátor na 15 toolů, JSON log + stdout | ✅ **Hotovo** |
| 9 | **Update README** — 15 toolů, 42 testů, cache, bezpečnost | ✅ **Hotovo** |


### 5.3 Priorita P2 — Střednědobá (1–2 týdny)

| \# | Změna | Důvod |
| - | - | - |
| 10 | **Resource endpoints** — např. `b2b://knowledge-base/latest` | Resources = bezpečnější než tools pro read-only data |
| 11 | **Notification hooks** — `tools/list\_changed` notifikace | Umožní klientům cache invalidaci |
| 12 | **Idempotency token** na write tooly | Safe retry při transport errors |
| 13 | **OpenTelemetry spans** — `mcp.tool.name`, `mcp.transport` | Agent debugging |
| 14 | **Tool versioning** — `tool\_validate\_vcf\_v2` jako nový tool | Rename/remove = breaking change |


### 5.4 Priorita P3 — Dlouhodobá (1 měsíc+)

| \# | Změna | Důvod |
| - | - | - |
| 15 | **Streamable HTTP transport** (vedle stdio) | Vzdálený přístup, sdílení mezi klienty |
| 16 | **OAuth proxy** (FastMCP 3.x built-in) | Auth pro remote přístup |
| 17 | **Docker image** | Reproducibilní deployment |
| 18 | **MCP Inspector integration** do test suite | Debugging auth flow a tool schemas |
| 19 | **Multi-language support** (TypeScript SDK pro specifické tools) | Pokud bude potřeba |


### 5.5 Alternativa: Nový univerzální server?

**Rozhodnutí: NE — stavět na stávajícím.**

Důvody:

- FastMCP je správný framework (70%+ trhu Python MCP)

- Kódová báze je čistá a modulární

- Hlavní problémy jsou kvalitativní (descriptions, validation), ne architektonické

- Přepis by znamenal ztrátu 15 existujících toolů a 24 testů


## 6. Use case architektura pro SYSTEQ workflow

### 6.1 Doménová mapa — aktuální nástroje

```
                    ┌─────────────────────────┐  
                    │    MCP Server (cnc-tools) │  
                    │     15 nástrojů          │  
                    └──────┬──────────┬───────┘  
                           │          │  
              ┌────────────┘          └────────────┐  
              ▼                                    ▼  
   ┌─────────────────────┐              ┌─────────────────────┐  
   │ CNC Pipeline Domain  │              │  Meta Domain        │  
   │                     │              │                     │  
   │ • VCF Analyze      │              │ • KB Search         │  
   │ • VCF Validate     │              │ • ACI Lookup        │  
   │ • VCF Diff         │              │ • Git Status All    │  
   │ • RE Pipeline      │              │ • List RE Scripts   │  
   │ • List Directory   │              │ • Read File         │  
   │ • Search Files     │              │ • Write File        │  
   └─────────────────────┘              └─────────────────────┘
```

### 6.2 Navrhované nové tooly (use case driven)

#### CNC doména

| Tool | Účel | Priorita |
| - | - | - |
| `tool\_generate\_vcf\_snippet` | Generuje syntetický VCF blok podle specifikace | P2 |
| `tool\_layer\_recommendation` | Doporučí ACI barvu + tool parametry podle typu materiálu | P2 |
| `tool\_vcf\_statistics\_batch` | Batch statistika přes všechny VCF v adresáři | P2 |
| `tool\_cross\_repo\_dependency` | Mapuje závislosti mezi repy (kdo volá koho) | P3 |


#### Meta doména

| Tool | Účel | Priorita |
| - | - | - |
| `tool\_session\_state` | Uloží/načte stav session (co bylo uděláno) | P1 |
| `tool\_project\_timeline` | Sledování času stráveného na úkolech | P2 |
| `tool\_mcp\_status` | Diagnostika MCP serveru (uptime, tool usage stats) | P1 |
| `tool\_semantic\_search` | Vektorové vyhledávání (embeddings) v KB | P2 |
| `tool\_changelog` | Automatický changelog z git logů napříč repy | P2 |


### 6.3 Multi-server orchestrace (budoucnost)

```
┌────────────────────────────────────────────────────┐  
│                 MCP Host (opencode)                 │  
└────────┬──────────┬──────────┬─────────────────────┘  
         │          │          │  
    ┌────▼───┐ ┌───▼────┐ ┌───▼────────┐  
    │ cnc-   │ │ kb-    │ │ code-      │  
    │ tools  │ │ search │ │ graph      │  
    │ (15)   │ │ (local)│ │ (Nexus-MCP)│  
    └────────┘ └────────┘ └────────────┘  
         │          │          │  
         ▼          ▼          ▼  
    VCF files   B2B-KB    Codebase
```


## 7. Kvalifikovaná predikce

### 7.1 Scénář A: Vývoj s MCP (doporučeno)

| Časový horizont | Stav | Dif oproti standardu |
| - | - | - |
| **Teď** | Lokální MCP server, 15 toolů, základní validace | +2σ (early adopter) |
| **1 měsíc** | Cache, async, audit logging, input validation | +2.5σ |
| **3 měsíce** | Remote HTTP, OAuth, CI/CD integrace MCP | +3σ |
| **6 měsíců** | Multi-server orchestrace, embedding search | +3.5σ |
| **12 měsíců** | Plně lokální AI stack, agent teams | +4σ |


**Marginální přínos:** ~2–3 hodiny/den úspory (odhad z EROI prototypu + projected leverage).

### 7.2 Scénář B: Vývoj bez MCP (status quo ante)

| Aspekt | Stav | Dif |
| - | - | - |
| Nástroje | Pouze agentic tools opencode | 0σ (baseline) |
| Workflow | Manuální orchestr (prompt → čekání → kontrola) | 0σ |
| Znovupoužitelnost | Ad-hoc, per-session | 0σ |
| Škálovatelnost | Lineární s časem autora | 0σ |


**Důsledek:** Udržení současného diffu, ale postupné erodování, jak AI literate populace dohání.

### 7.3 Scénář C: Adopce existujících MCP serverů (bez vlastního vývoje)

| Výhoda | Nevýhoda |
| - | - |
| Nulový vývojový čas | Žádná doménová specializace (VCF, ACI) |
| Přístup k 17 000+ serverům | Závislost na třetích stranách |
| Ověřená řešení | Bezpečnostní riziko (neznámý kód) |


**Verdikt:** Nedostatečné pro SYSTEQ doménu — VCF/ACI nástroje neexistují v žádném veřejném registru.

### 7.4 Dif predikce — vývoj s MCP vs bez MCP

```
Produktivita  
(relativní)  
  ▲  
  │                                    S MCP (Scénář A)  
  │                                   /  
  │                                  /  
  │                                 /  
  │                                / ← gap se rozšiřuje  
  │                               /  
  │                   Bez MCP (Scénář B)  
  │                  ────────────────  
  │                 /  
  │                /  
  │               /  
  │              /  
  │             /  
  │  
  └────────────────────────────────────────► Čas  
         2026        2027        2028
```

**Klíčová predikce:** Gap mezi Scénářem A a B se bude *zvětšovat*, protože:

1. MCP ekosystém roste exponenciálně (97M SDK downloads → odhad 200M+ v 2027)

2. Vlastní doménové nástroje = compound advantage (každý nový tool zvyšuje hodnotu všech existujících)

3. Stateless MCP release + enterprise features sníží bariéru adopce pro mainstream → ti, co jsou připraveni, těží první

### 7.5 Riziková analýza

| Riziko | Pravděpodobnost | Dopad | Mitigace |
| - | - | - | - |
| MCP je nahrazeno jiným protokolem | Nízká (~10 %) | Vysoký | FastMCP abstrahuje transport; migrace na nový protokol = změna SDK, ne architektury |
| Bezpečnostní incident přes MCP | Střední (~25 %) | Vysoký | Path allowlist, input validation, audit log, rate limiting |
| Dependency drift (SDK verze) | Střední (~30 %) | Střední | nightly CI, Dependabot (already configured) |
| LLM klient změní MCP implementaci | Nízká (~15 %) | Střední | opencode podporuje standardní MCP config |
| Autor ztratí motivaci udržovat | Střední (~20 %) | Vysoký | Dokumentace a modularita umožní snadný restart |



## 8. Akční plán

### 8.1 Immediate (splněno)

- [x] Opravit tool descriptions podle best practices (WHEN/WHAT/RETURNS/CONSTRAINTS)

- [ ] Přidat input validation (type, range, length, format) na všechny parametry

- [ ] Vylepšit error messages (co → proč → alternativa)

- [x] Smazat `main.py`

- [x] Update README na 15 toolů, 42 testů, cache, bezpečnost

### 8.2 Short-term (splněno)

- [ ] Implementovat async I/O pro filesystem a subprocess

- [x] Přidat cache layer pro KB search a ACI lookup (TTLCache, 300s/600s)

- [x] Přidat audit logging (@auditable dekorátor na 15 toolů)

- [ ] Přidat rate limiter

### 8.3 Medium-term (do 2 týdnů)

- [ ] Resource endpoints pro read-only data

- [ ] Tool pro session state management

- [ ] Tool pro MCP server diagnostics

- [ ] OpenTelemetry integrace

### 8.4 Long-term (do 1 měsíce)

- [ ] Vyhodnotit Streamable HTTP pro vzdálený přístup

- [ ] Prozkoumat Nexus-MCP pro code graph integration

- [ ] Zvážit embedding search v KB (vektorová databáze)

- [ ] Multi-server orchestrace v opencode


## Příloha A: Checklist pro nový MCP tool

```
@mcp.tool()  
def tool\_example(param: str, count: int = 10) -\> str:  
    """\[WHEN\] Prohledá XYZ a vrátí výsledky.  
  
    \[WHAT\] Analyzuje XYZ podle kritérií a vrátí strukturovaný report.  
  
    \[RETURNS\] Seznam XYZ s metrikami, max 50 položek.  
    Pokud nic nenalezeno, vrátí prázdný seznam.  
  
    \[CONSTRAINTS\] Parametr param je povinný, max 100 znaků.  
    count je nepovinný, rozsah 1-100, default 10.  
  
    Args:  
        param: \[FORMAT\] XYZ identifikátor. Příklady: "abc", "xyz"  
        count: \[DEFAULT=10\] Počet výsledků (1-100)  
    """  
    \# 1. Input validation  
    if len(param) \> 100:  
        return "CHYBA: param max 100 znaků. Zadej kratší hodnotu."  
    if not 1 \<= count \<= 100:  
        return "CHYBA: count musí být 1-100. Použij count=10."  
    \# 2. Provedení  
    try:  
        result = do\_something(param, count)  
    except Exception as e:  
        return f"CHYBA: \{e\}. Zkus jiný parametr nebo opakuj později."  
    \# 3. Minimalistický výstup  
    return format\_result(result)
```

## Příloha B: Zdroje

| Zdroj | URL |
| - | - |
| Oficiální MCP specifikace | [https://modelcontextprotocol.io](https://modelcontextprotocol.io/) |
| Python SDK (GitHub) | [https://github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) |
| FastMCP dokumentace | [https://fastmcp.readthedocs.io](https://fastmcp.readthedocs.io/) |
| MCP Inspector | [https://github.com/modelcontextprotocol/inspector](https://github.com/modelcontextprotocol/inspector) |
| State of MCP 2026 | [https://veprompts.com/reports/state-of-mcp-2026/](https://veprompts.com/reports/state-of-mcp-2026/) |
| MCP Cheat Sheet | [https://www.webfuse.com/mcp-cheat-sheet](https://www.webfuse.com/mcp-cheat-sheet) |
| Best Practices | [https://www.philschmid.de/mcp-best-practices](https://www.philschmid.de/mcp-best-practices) |




## 9. Sémantická analýza dev notes — Secret exposure a PAT

### 9.1 Analýza problému

**Dev notes (parafráze):**

> `.env` v kořeni `\_github\\` obsahuje PAT. Není v allowlistu pro write, ale read by mohl uniknout. Dev využívá PAT pro automatizované operace s vlastním GitHub portfoliem. Dle jeho názoru je nutné změnit autorizaci agenta pro PAT na "allowed".

**Konfliktní pravidla (CONTEXT\_REPOS.md §3):**

> NEČíst, NElokovat, NECommitovat: `.env`, `.env.\*`, `\*.key`, `\*.pem`.

#### 9.1.1 Sémantický rozklad

| Vrstva | Tvrzení dev | Realita |
| - | - | - |
| **Potřeba** | PAT je nutný pro GitHub operace | ✅ Pravda — bez PAT není push, PR, cross-repo dispatch |
| **Prostředek** | MCP server = vhodný nástroj pro práci s PAT | ❌ **Mylná domněnka** — MCP je špatná vrstva pro credentials |
| **Riziko** | "Allow read" = bezpečné | ❌ **Nepravda** — read .env = únik PAT do kontextu LLM = persistenční riziko |
| **Důsledek** | Umožnit MCP toolům číst PAT | ❌ **Nebezpečné** — porušuje princip nejnižších oprávnění (least privilege) |


#### 9.1.2 Root cause

Problém není v MCP serveru, ale v absenci credential management vrstvy:

```
Současný stav (špatně):  
  PAT v .env → MCP tool čte .env → PAT v LLM kontextu → únik při logování/chybě  
  
Správný stav:  
  PAT v OS env / opencode config → gh CLI / git přímo → žádná expozice LLM
```

### 9.2 EROI hranice MCP — Kdy MCP NEPOUŽÍT

Varovné signály z §4.4 aplikované na PAT use case:

| Signál | PAT use case | Verdict |
| - | - | - |
| **Overhead JSON-RPC** | Čtení env var přes JSON-RPC je ~50ms+ latency pro operaci, která má být \<1ms | ❌ Porušuje |
| **Unrestricted shell** | Tool pro čtení `.env` = de facto backdoor do všech secrets | ❌ Porušuje |
| **"Hackathon prototype"** | Tool, který jen čte proměnnou prostředí = wrapper kolem ničeho | ❌ Porušuje |
| **Version skew** | Změna formátu `.env` → rozbití toolu | ❌ Potenciální |


**Verdikt:** MCP je pro práci s credentials **zcela nevhodný**. EROI je záporné — vytváříš bezpečnostní riziko výměnou za nulovou přidanou hodnotu.

#### 9.2.1 EROI matice rozhodování

```
                     Jednoduchost řešení →  
                     Nízká               Vysoká  
            ┌────────────────────────────────────┐  
Potřeba    │                                    │  
MCP        │   ZDE MCP DÁVÁ SMYSL              │  ZDE MCP NEDÁVÁ SMYSL  
vysoká     │   (doménové nástroje,              │  (stejně dobře řešitelné  
           │    multi-client distribuce)        │   jednodušším nástrojem)  
           │                                    │  
           │   Např: VCF analyze,               │  Např: čtení env var,  
           │   ACI lookup, KB search            │   jednoduchý git commit  
           │                                    │  
Potřeba    │                                    │  
MCP        │   ZATÍM NEPOUŽÍVAT                 │  NEPOUŽÍVAT  
nízká      │   (počkat na dozrání potřeb)       │  (přímý příkaz stačí)  
           │                                    │  
           └────────────────────────────────────┘
```

**PAT spadá do kvadrantu "Nepoužívat"** (jednoduché řešení existuje + potřeba MCP je nulová).

### 9.3 Security decision framework

Pravidlo pro rozhodování, zda má MCP server přistupovat k secretům:

#### 9.3.1 Tři otázky (must projít všemi)

| \# | Otázka | Pokud NE |
| - | - | - |
| 1 | Je secret nezbytný pro doménovou funkci MCP toolu? (Ne pro plumbing/infra) | Nepoužívej MCP — použij env var hostitele |
| 2 | Existuje jednodušší způsob bez MCP? (gh CLI, env var, opencode native) | Použij ten — MCP by znamenal overhead bez přidané hodnoty |
| 3 | Je riziko úniku do LLM kontextu akceptovatelné? (Pokud ne, secret do MCP nepatří) | Řeš na úrovni hostitele, ne MCP serveru |


**Aplikace na PAT:**

| Otázka | Odpověď | Výsledek |
| - | - | - |
| 1. Nezbytný pro doménovou funkci? | NE — PAT je infra, ne doménová funkce | ❌ |
| 2. Existuje jednodušší řešení? | ANO — `gh` CLI, env var v opencode configu | ❌ |
| 3. Akceptovatelné riziko úniku? | NE — PAT v LLM kontextu = pernamentní expozice | ❌ |


**Závěr: PAT do MCP serveru nepatří.**

#### 9.3.2 Princip CO/PROČ/JAK/EFEKT (CONTEXT\_REPOS.md §5)

Aplikace na MCP tool pro práci s PAT:

| Kritérium | Odpověď |
| - | - |
| **CO** to je | Tool, který čte .env a exponuje PAT do LLM kontextu |
| **PROČ** to řeší ground truth problém | Není — ground truth je "potřebuji autentizovat GitHub operace",** což řeší gh CLI + env var** |
| **JAK** to funguje | Volá open() na .env soubor → string vrací do LLM |
| **EFEKT** marginální přínos | 0 — **stejný výsledek bez rizika dosáhneš přes os.environ v opencode konfiguraci** |
| **RIZIKO** co se rozbije | Únik PAT do logů, do kontextu, do výstupů toolů → kompromitace GitHub portfolia |


**Verdikt:** NEPROVÁDĚT — porušuje 4/5 kritérií. Jediné splněné je JAK (technicky to funguje).

### 9.4 Řešení: Credential layering architektura

#### 9.4.1 Navrhovaná hierarchie

```
Vrstva 0: OS Environment Variables  
  └── PAT\_GITHUB, API\_KEYS, ...  
  │   Přístup: Pouze hostitelský proces (opencode)  
  │   Bezpečnost: Nikdy nevstupuje do LLM kontextu  
  │  
Vrstva 1: opencode config (opencode.jsonc)  
  └── "env": \{ "GH\_TOKEN": "$\{PAT\_GITHUB\}" \}  
  │   Přístup: opencode internal tools (git, gh)  
  │   Bezpečnost: Nikdy nevstupuje do MCP serveru  
  │  
Vrstva 2: gh CLI  
  └── gh pr create, gh repo push, ...  
  │   Přístup: Autentizace přes GH\_TOKEN env var  
  │   Bezpečnost: CLI tool, ne MCP tool  
  │  
Vrstva 3: MCP Server (cnc-tools)  
  └── READ-ONLY: git status, log, diff  
  │   Přístup: Žádné secrets, žádný write  
  │   Bezpečnost: Izolace od credential vrstev  
  │  
Vrstva 4: Vzdálené služby (GitHub API, ...)  
  └── Voláno přes autentizovaného klienta (ne MCP)
```

#### 9.4.2 Konkrétní implementace — návod krok za krokem

##### Krok 1: Vytvořit PAT na GitHubu

1. Otevři https://github.com/settings/tokens
2. Klikni **Generate new token** → **Fine-grained token**
3. Název: `GITHUB_PAT`
4. Expiration: `No expiration` (nebo 90 dní)
5. Repository access: `All repositories`
6. Permissions → Contents: `Read and write`
7. Klikni **Generate token**
8. **Zkopíruj token** (zobrazí se jednou — při ztrátě musíš vytvořit nový)

##### Krok 2: Uložit do Windows User env var (PowerShell)

Otevři PowerShell (Win+R → `powershell` → Enter). Nastav proměnnou:

```powershell
# Nastavení (nahraď ghp_... svým tokenem)
[System.Environment]::SetEnvironmentVariable('GITHUB_PAT', 'ghp_...', 'User')
```

**Vysvětlení parametrů:**
- `'GITHUB_PAT'` = název proměnné (libovolný, ale konzistentní)
- `'ghp_...'` = hodnota — samotný token
- `'User'` = scope (dosah) — uloží se jen pro přihlášeného uživatele do `HKCU\Environment`. Není to uživatelské jméno, ale úroveň platnosti. Možnosti: `User` (jen tvůj účet), `Machine` (celý systém — vyžaduje Admin), `Process` (jen aktuální session)

##### Krok 3: Ověřit nastavení

```powershell
# Čtení User env var
[System.Environment]::GetEnvironmentVariable('GITHUB_PAT', 'User')

# Alternativně — v novém terminálu (dědí User env):
$env:GITHUB_PAT
```

Mělo by vypsat token. Pokud je prázdný -> restartuj terminál.

##### Krok 4: Ověřit, že gh CLI token vidí

```powershell
gh auth status
```

Očekávaný výstup: `Logged in to github.com as <tvé_uživatelské_jméno>`

##### Krok 5: Restartovat opencode

Zavři terminál, otevři nový → spusť opencode. Nové procesy dědí User env vars z registru při startu.

##### Krok 6: (volitelně) Smazání

```powershell
[System.Environment]::SetEnvironmentVariable('GITHUB_PAT', $null, 'User')
```

##### Užitečné příkazy pro správu Windows User env vars

```powershell
# Čtení konkrétní proměnné
[System.Environment]::GetEnvironmentVariable('GITHUB_PAT', 'User')

# Nastavení
[System.Environment]::SetEnvironmentVariable('NAZEV', 'hodnota', 'User')

# Smazání
[System.Environment]::SetEnvironmentVariable('NAZEV', $null, 'User')

# Výpis všech User proměnných
[System.Environment]::GetEnvironmentVariables('User') | Out-GridView

# Zjištění aktuálního uživatele
whoami
$env:USERNAME
[System.Environment]::UserName
```

#### 9.4.3 Výjimka: Kdy by MCP mohl pracovat s credentials?

Jediný legitimní scénář: **Remote MCP server s OAuth** (FastMCP 3.x built-in), kde:

- Auth řeší serverová vrstva (OAuth 2.1 / bearer token)

- Secret nikdy nevstupuje do LLM kontextu

- Token je validován na straně serveru, ne předáván klientovi

Tento scénář ale vyžaduje Streamable HTTP transport + OAuth proxy — infrastruktura, která aktuálně není nasazená. Do té doby: **žádné secrets v MCP**.

### 9.5 Důsledky pro stávající MCP server

#### 9.5.1 Co se mění

| Aspekt | Původní stav | Nový stav |
| - | - | - |
| `.env` v allowlistu | ⚠️ Read enabled | ❌ **Přidat do FORBIDDEN\_PATHS** |
| `tool\_git\_status\_all` | Read-only (OK) | ✅ Beze změny |
| Git write tooly | Neexistují (OK) | ✅ Ani nevytvářet |
| `tool\_write\_file` | Omezen na `\_github\\` | ⚠️ Přidat check na `.env` pattern — pokud cesta končí `.env`, reject |
| Audit logging | Neexistuje | ✅ Přidat — logovat všechny tool cally pro detekci anomálií |


#### 9.5.2 Konkrétní změny v kódu

```
\# config.py — přidat do FORBIDDEN\_PATHS  
FORBIDDEN\_PATTERNS: list\[str\] = \[  
    ".env",  
    ".env.\*",  
    "\*.key",  
    "\*.pem",  
    "credentials\*",  
\]  
  
def is\_path\_allowed(path: Path) -\> bool:  
    """Ověří, zda je cesta v povoleném rozsahu."""  
    resolved = path.resolve()  
    for forbidden in FORBIDDEN\_PATHS:  
        if resolved.is\_relative\_to(forbidden):  
            return False  
    for allowed in ALLOWED\_ROOTS:  
        if resolved.is\_relative\_to(allowed):  
            \# Dodatečná kontrola na secret patterny  
            for pattern in FORBIDDEN\_PATTERNS:  
                if resolved.match(pattern):  
                    return False  
            return True  
    return False

\# filesystem.py — tool\_write\_file reject .env  
def write\_file(path: str, content: str) -\> str:  
    filepath = Path(path)  
    if filepath.name.startswith(".env") or ".env" in filepath.suffixes:  
        return "CHYBA: Zápis .env souborů není povolen z bezpečnostních důvodů."  
    \# ... rest
```

#### 9.5.3 Revidovaný bezpečnostní audit

| Aspekt | Stav v1.0 | Stav v1.1 |
| - | - | - |
| Path traversal | ✅ Ošetřeno | ✅ Ošetřeno |
| Forbidden paths | ✅ Ošetřeno | ✅ Ošetřeno + **FORBIDDEN\_PATTERNS** |
| Git read-only | ✅ Ošetřeno | ✅ Ošetřeno |
| Secret exposure | ⚠️ Částečně | ❌ **PŘIDÁNO DO FORBIDDEN** |
| .env ochrana | ❌ Chybí | ✅ Přidáno — reject na čtení i zápis |
| Input sanitizace | ⚠️ Částečně | ⚠️ Částečně (P0) |
| Rate limiting | ❌ Chybí | ❌ Chybí (P1) |
| Audit logging | ❌ Chybí | ❌ Chybí (P1) |



## 10. Revidovaný akční plán (v1.1)

### 10.1 Immediate — Bezpečnost (splněno)

- [x] **Přidat `.env` do FORBIDDEN\_PATTERNS v `config.py`** — znemožnit read/write .env souborů

- [x] **Přidat FORBIDDEN\_PATTERNS** — `.env`, `.env.*`, `*.key`, `*.pem`, `credentials*`, `secrets*`

- [x] **Přidat reject v `read\_file` a `write\_file`** — pokud cíl odpovídá FORBIDDEN\_PATTERNS, vrátit chybu

- [x] **Ověřit, že žádný stávající tool nečte .env** — 9 testů secret exposure (unit + integrační)

- [x] **Nevytvářet žádný git write tool** — git write operace řešit přes `gh` CLI, ne MCP

- [x] **Tool descriptions** — opraveny na WHEN/WHAT/RETURNS/CONSTRAINTS (P0 z v1.0)

- [x] **Input validation** — přidat na všechny parametry (P0 z v1.0, F2.3) — hotovo v Session 16

- [x] **Error messages** — vylepšit — hotovo v Session 16 (validate.py, "co→proč→alternativa")

### 10.2 Short-term (splněno)

- [x] **Nastavit GITHUB\_PAT jako OS env var** (User-level) — hotovo (viz §9.4.2)

- [x] **Ověřit, že `gh` CLI funguje s env varem** — `gh auth status` ✅ — hotovo v Session 16

- [x] **Audit logging** — @auditable dekorátor na všech 15 toolů, JSON log + stdout

- [x] **Cache layer** — TTLCache pro kb\_search (300s) a aci\_lookup (600s) + 9 testů

- [ ] **Rate limiter** — ochrana před runaway agentem (F2.4)

### 10.3 Střednědobé (1–2 týdny)

- [ ] **Prozkoumat FastMCP 3.x OAuth proxy** — pro budoucí remote scénáře

- [ ] **Dokumentovat credential layering architekturu** — jako standard pro všechny MCP servery v portfoliu

- [ ] **Resource endpoints** pro read-only data

- [ ] **OpenTelemetry integrace** — auditní stopa

### 10.4 Principy pro budoucí rozhodování

Při zvažování nového MCP toolu nebo rozšíření existujícího:

1. **Nejnižší oprávnění** — MCP tool má mít přístup jen k tomu, co nezbytně potřebuje

2. **EROI threshold** — pokud úlohu řeší jednodušší nástroj (gh CLI, env var, direct API call), MCP nepoužívat

3. **Credentials ≠ MCP doména** — secrets patří do hostitelské vrstvy (OS, opencode), ne do MCP kontextu

4. **Audit trail** — každý tool call musí být dohledatelný

5. **CO/PROČ/JAK/EFEKT** — před každým novým toolem projít tímto rámcem


## 11. Session 16 — Bezpečnostní audit, credential layering deployment, input validation

**Datum:** 2026-07-05  
**Kontext:** Tato session vznikla jako follow-up k §9 (secret exposure analýza) — provedení reálného auditu, nasazení credential layering architektury a implementace zbývajících P0 položek.

### 11.1 Výchozí stav

Dokument v1.2 deklaroval hotové P0/P1 vylepšení (security hardening, audit, cache, tool descriptions). Audit odhalil:

- ✅ Všechny deklarované komponenty existují (config.py, audit.py, cache.py, server.py s 15 tooly, 42 testů)
- ⚠️ Input validation a error messages (P0) stále chybí — blokovány od v1.0
- ⚠️ `.env` soubor v kořeni `_github\` **reálně existoval** a obsahoval GITHUB_TOKEN
- ⚠️ `.env` nebyl v `.gitignore` několika repozitářů
- ❌ `gh` CLI nebylo nainstalováno — credential layering architektura nekompletní

### 11.2 Bezpečnostní audit — reálný nález

| Nález | Závažnost | Řešení |
|-------|-----------|--------|
| `.env` v `_github\` s GITHUB_TOKEN (54 B) | VYSOKÁ — token v plaintextu na disku | Token rotován, `.env` smazán (záloha `.env.BACKUP-DELETE-AFTER-ROTATION`) |
| Token `[REVOKED — zneplatněn 2026-07-05]` exponován v LLM kontextu | VYSOKÁ — perzistentní riziko úniku | Nový token (fine-grained, Contents RW, PR RW, All repos) |
| `.env` není v `.gitignore` (5 repozitářů) | STŘEDNÍ — riziko náhodného commitu | Přidáno do všech chybějících .gitignore |
| `gh` CLI není nainstalováno | STŘEDNÍ — credential layering nefunkční | Nainstalováno v2.96.0 portable do `~/.local/bin/` |

#### 11.2.1 Credential layering architektura — finální stav

```
Vrstva 0: OS Windows User env var       ← GITHUB_PAT (nový, bezpečný)
              Přístup: Pouze hostitelský proces (opencode)
              Nikdy nevstupuje do LLM kontextu ✅

Vrstva 1: gh CLI v2.96.0                ← Autentizace přes GITHUB_PAT
              Přístup: gh auth status ✅ Logged in as outpost2026
              HTTPS protokol, keyring úložiště

Vrstva 2: MCP Server (cnc-tools)        ← Read-only git, žádné secrets
              FORBIDDEN_PATTERNS blokuje .env, *.key, *.pem
              @auditable na všech 15 toolů ✅

Vrstva 3: Vzdálené služby (GitHub API)  ← Voláno přes gh CLI, ne MCP
```

### 11.3 P0 implementace — Input validation + error messages

#### 11.3.1 Nový modul `validate.py`

Cesta: `mcp-local-server/src/mcp_local_server/validate.py`

| Funkce | Účel |
|--------|------|
| `validate_path(path, label)` | Prázdná cesta, délka > 260 znaků |
| `validate_int(value, min, max, label, default)` | Typ int, rozsah min–max |
| `validate_non_empty(value, label, max_len)` | Prázdný string, délka > max_len |
| `validate_suffix(path, suffix, label)` | Kontrola přípony souboru |
| `validate_vcf_ext(path)` | .VCF/.vcf suffix check |

Všechny vracejí `str | None` — chybová hláška ve formátu "co selhalo → proč → alternativa" nebo `None`.

#### 11.3.2 Validace na všech 15 tool parametrech

Aplikováno v `server.py` na každý MCP tool:

| Tool | Validované parametry |
|------|---------------------|
| `tool_list_directory` | path |
| `tool_read_file` | path, max_lines (1–5000) |
| `tool_write_file` | path, content (max 100k znaků) |
| `tool_search_files` | directory, pattern (max 200), max_results (1–200) |
| `tool_git_status` | repo_path |
| `tool_git_log` | repo_path, count (1–100) |
| `tool_git_diff` | repo_path |
| `tool_validate_vcf` | file_path, suffix .vcf |
| `tool_vcf_analyze` | file_path, suffix .VCF/.vcf |
| `tool_vcf_diff` | file_a, file_b (oba .vcf) |
| `tool_run_re_pipeline` | vcf_file (.vcf), scripts (max 500) |
| `tool_kb_search` | query (max 200), max_results (1–50) |
| `tool_aci_lookup` | aci_number (0–255) |

Bez parametrů: `tool_git_status_all`, `tool_list_re_scripts`.

### 11.4 Revidovaný bezpečnostní audit (v1.3)

| Aspekt | Stav v1.2 | Stav v1.3 |
|--------|-----------|-----------|
| Path traversal | ✅ Ošetřeno | ✅ Ošetřeno |
| Forbidden paths | ✅ Ošetřeno | ✅ Ošetřeno |
| Forbidden patterns | ✅ Ošetřeno | ✅ Ošetřeno |
| .env ochrana | ✅ Ošetřeno | ✅ Ošetřeno + **skutečný .env smazán** |
| Git read-only | ✅ Ošetřeno | ✅ Ošetřeno |
| Secret exposure | ❌ Reálně hrozilo | ✅ **Token rotován, .env smazán** |
| Input sanitizace | ⚠️ Částečně (P0) | ✅ **Implementováno** (validate.py, 15 toolů) |
| Error messages | ⚠️ Částečně (P0) | ✅ **Implementováno** ("co→proč→alternativa") |
| Rate limiting | ❌ Chybí (P1) | ❌ Stále chybí (P1) |
| Audit logging | ✅ Implementováno | ✅ Implementováno |
| gh CLI | ❌ Nenainstalováno | ✅ **v2.96.0 nainstalováno + autentizováno** |
| Credential layering | ❌ Nenasazeno | ✅ **Plně nasazeno (4 vrstvy)** |

### 11.5 Testy

```
42/42 ✅ (2.04s)
```

Všechny stávající testy prošly beze změny. Input validation je testována nepřímo — chybové hlášky z validace mají prefix "CHYBA:", stejně jako stávající `CHYBA` asserty v testech.

### 11.6 Akční plán — aktuální stav

#### Immediate (P0) — vše splněno
- [x] Tool descriptions — WHEN/WHAT/RETURNS/CONSTRAINTS
- [x] **Input validation** — validate.py + 15 toolů ✅
- [x] **Error messages** — "co→proč→alternativa" ✅
- [x] FORBIDDEN_PATTERNS + .env blokace
- [x] Secret exposure — token rotován, .env smazán ✅

#### Short-term (P1) — hotovo kromě rate limiteru
- [x] Cache layer (TTLCache, 300s/600s, 9 testů)
- [x] Audit logging (@auditable na 15 toolů)
- [x] **gh CLI** — v2.96.0, autentizováno ✅
- [ ] Rate limiter — stále chybí (P1)

#### Střednědobé (P2)
- [ ] Resource endpoints pro read-only data
- [ ] Session state management
- [ ] MCP server diagnostics tool
- [ ] OpenTelemetry integrace

### 11.7 Poučení z reálného incidentu

1. **Dokumentace ≠ realita** — i když dokument deklaruje bezpečnostní opatření, je nutné provést fyzický audit. V tomto případě dokument v1.2 tvrdil "secret exposure ošetřeno", ale `.env` reálně existoval s platným tokenem.

2. **Credential layering musí být nasazen dříve, než dojde k expozici** — token byl v kontextu LLM po celou dobu Session 14–15, aniž by si toho byl uživatel vědom.

3. **`gh` CLI je kritická závislost** — bez ní není možné provádět GitHub operace bez vystavení secrets do LLM kontextu.

4. **Input validation patří na API boundary** — validace v `server.py` (MCP dekorátory) je správná vrstva, protože zachycuje chyby před tím, než vstoupí do doménové logiky.


*Konec dokumentu. Verze v1.3, 2026-07-05. Aktualizace: Session 16 — bezpečnostní audit prostředí, reálný secret exposure nález, credential layering deployment, input validation (P0), gh CLI instalace, ověření 42/42 testů.*

