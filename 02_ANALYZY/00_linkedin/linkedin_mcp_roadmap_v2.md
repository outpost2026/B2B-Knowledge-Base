# Architektura a roadmapa — linkedin-mcp-custom

**Autor:** Ondřej Soušek | **Datum:** 2026-07-05
**Účel:** Kompletní technická specifikace pro build vlastního MCP serveru od základů, inspirovaného stickerdaniel/linkedin-mcp-server, s integrovaným EROI scoring engine a KB write-back.

---

## 1. Architektura — Přehled

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MCP Client (Claude Code)                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ JSON-RPC (stdio/HTTP)
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     linkedin-mcp-custom (server.py)                  │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                     FastMCP server                           │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │    │
│  │  │ get_saved_   │  │ get_job_     │  │ analyze_saved_   │  │    │
│  │  │ jobs         │  │ details      │  │ jobs             │  │    │
│  │  └──────┬───────┘  └──────┬───────┘  └───────┬──────────┘  │    │
│  │         │                 │                   │              │    │
│  │         ▼                 ▼                   ▼              │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │               LinkedInExtractor                      │    │    │
│  │  │  ┌─────────────┐  ┌──────────────┐  ┌───────────┐  │    │    │
│  │  │  │ navigate    │  │ scroll +     │  │ noise     │  │    │    │
│  │  │  │ to_page()   │  │ innerText()  │  │ strip()   │  │    │    │
│  │  │  └─────────────┘  └──────────────┘  └───────────┘  │    │    │
│  │  └───────────────────────┬─────────────────────────────┘    │    │
│  │                          │                                   │    │
│  │                          ▼                                   │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │           scraper.py (Patchright browser)            │    │    │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │    │    │
│  │  │  │ auth (cookies)│  │ rate-limit   │  │ modal     │  │    │    │
│  │  │  │              │  │ detection    │  │ dismiss   │  │    │    │
│  │  │  └──────────────┘  └──────────────┘  └───────────┘  │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                   Analysis Engine (EROI)                      │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │    │
│  │  │ domain   │  │ tech     │  │ role     │  │ skill gap  │  │    │
│  │  │ scorer   │  │ scorer   │  │ scorer   │  │ matcher    │  │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │    │
│  │  ┌──────────────────────────────────────────────────────┐  │    │
│  │  │              kb_writer.py                             │  │    │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │  │    │
│  │  │  │ agregovany_  │  │ metadata_    │  │ git       │  │  │    │
│  │  │  │ report.md    │  │ stacku.json  │  │ commit    │  │  │    │
│  │  │  └──────────────┘  └──────────────┘  └───────────┘  │  │    │
│  │  └──────────────────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌─────────────────────┐
              │  LinkedIn (remote)   │
              │  /jobs-tracker/      │
              │  /jobs/view/{id}/    │
              └─────────────────────┘
```

---

## 2. Vrstvy (Layered Architecture)

### Layer 0 — MCP Transport
- FastMCP server (fastmcp>=3.0.0)
- 2 tool registrace: `get_saved_jobs`, `analyze_saved_jobs`
- Volitelné: `get_job_details` pro rozšíření na detailní analýzu
- Vstup/výstup: JSON-RPC přes stdio (default) nebo streamable HTTP

### Layer 1 — Browser Management
- **BrowserManager singleton** (převzato ze stickerdaniel)
- Patchright browser (anti-detection fork Playwrightu)
- Cookie-based auth přes persistentní profil
- `get_or_create_browser()` — lazy init, singleton pattern
- `close_browser()` — cleanup + cookie export

### Layer 2 — Scraping Engine
- `LinkedInExtractor(page)` — tenký wrapper kolem Patchright Page
- Metody:
  - `navigate_to_page(url)` — goto + auth check + rate-limit detection
  - `extract_page(url)` → nahraje stránku → scroll → innerText → strip noise
  - `scrape_job(job_id)` → extrahuje detail jedné nabídky
  - `scrape_saved_jobs()` → extrahuje seznam uložených nabídek + job IDs
- Noise stripping: footer, sidebar, rate-limit sentinel
- Rate-limit detection + retry (1× backoff 5s)

### Layer 3 — EROI Analysis Engine
- **domain_scorer()** — 35 % váha (průmyslová automatizace vs. enterprise IT)
  - Klíčová slova: industrial, manufacturing, automation, PLC, CNC, výroba, factory
  - Doménová klasifikace (industrial vs. non-industrial)
  - Vylučovací kritéria: customer service, sales, support pod engineering titulkem
- **tech_scorer()** — 25 % váha (Python = core, TypeScript/Playwright = sekundární)
  - Skill match matrix z `portfolio_audit_a_match.md`
  - Mapování: autorův stack → požadavky nabídky
  - Gap analýza: direct_match / partial_match / no_match
- **role_scorer()** — 20 % váha (engineering vs. sales/support)
  - Detekce "falešný engineer" patternu
  - Seniorita match
- **growth_scorer()** — 10 % váha (employer reputation)
  - Strategický employer bonus (Siemens, Rockwell, ABB, Bosch, Festo)
- **formal_scorer()** — 5 % váha (formální kvalifikace)
- **location_scorer()** — 5 % váha (Praha/CZ/remote)

### Layer 4 — KB Writer
- `append_report(job_data, analysis)` → přidá appendix do `agregovany_report.md`
- `update_metadata(job_data, analysis)` → update `metadata_stacku.json`
- `git_commit(message)` → commit + push do B2B-Knowledge-Base
- Formát zprávy: viz stávající `agregovany_report.md` (EROI verdict, fit hodnocení, závěr)

---

## 3. Data Flow

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ 1. get_     │───▶│ 2. scrape_saved_ │───▶│ 3. Pro každé   │
│ saved_jobs()│    │ jobs()           │    │    job_id:     │
│ (MCP tool)  │    │ → /jobs-tracker/ │    │    scrape_job() │
└─────────────┘    └──────────────────┘    └────────┬────────┘
                                                    │
                                                    ▼
                                            ┌─────────────────┐
                                            │ 4. EROI analyze │
                                            │ → scores + gaps │
                                            └────────┬────────┘
                                                     │
                                                     ▼
                                            ┌─────────────────┐
                                            │ 5. KB write     │
                                            │ → report.md     │
                                            │ → metadata.json │
                                            │ → git commit    │
                                            └─────────────────┘
```

**Detail datového toku:**

```
Step 1: get_saved_jobs()
  → Browser navigates to https://www.linkedin.com/jobs-tracker/
  → Extracts innerText from <main>
  → Extracts job IDs from a[href*="/jobs/view/"] 
  → Returns {sections: {saved_jobs: raw_text}, job_ids: [...]}

Step 2: Pro každé job_id v job_ids:
  → Browser navigates to https://www.linkedin.com/jobs/view/{id}/
  → Extracts innerText (title, company, description, requirements, benefits)
  → Returns {sections: {job_posting: raw_text}}

Step 3: analyze_saved_jobs() (tool, nebo standalone funkce)
  → domain_scorer(raw_text) → 0-100
  → tech_scorer(raw_text) → 0-100  
  → role_scorer(raw_text) → 0-100
  → growth_scorer(company) → 0-100
  → formal_scorer(raw_text) → 0-100
  → location_scorer(location) → 0-100
  → weighted_total = Σ(score × weight)
  → skill_gaps = [tech not in portfolio]
  → category = SLEDOVAT if ≥65, MEDIUM if 50-64, HRANIČNÍ if 40-49, NESLEDOVAT if <40

Step 4: write_to_kb(job_data, analysis)
  → Append section to agregovany_report.md
  → Insert entry into metadata_stacku.json
  → Recalculate aggregate_insights
  → git add + git commit
```

---

## 4. EROI Scoring Engine — Detail

### 4.1 Váhy a dimenze (golden rules)

| Dimenze | Váha | Funkce | Vstup | Výstup |
|---------|------|--------|-------|--------|
| Doménová shoda | 35 % | `domain_score(text)` | Raw text job posting | 0-100 |
| Technologická shoda | 25 % | `tech_score(text, portfolio)` | Text + skill matrix | 0-100 |
| Role a kompetence | 20 % | `role_score(text)` | Text | 0-100 |
| Růstový potenciál | 10 % | `growth_score(company_name)` | Jméno firmy | 0-100 |
| Formální požadavky | 5 % | `formal_score(text)` | Text | 0-100 |
| Lokalita a režim | 5 % | `location_score(text)` | Text | 0-100 |

### 4.2 Thresholds

| Skóre | Kategorie | Akce |
|-------|-----------|------|
| ≥ 65 % | 🟢 SLEDOVAT high | Aplikovat, alokovat čas |
| 50-64 % | 🟢 SLEDOVAT medium | Sledovat, zvážit po skill gap closure |
| 40-49 % | 🟡 HRANIČNÍ | Pouze pokud nízké náklady na aplikaci |
| < 40 % | 🔴 NESLEDOVAT | Nealokovat čas |

### 4.3 Skill match matrix (pro tech_scorer)

```python
# Přímý přepis z portfolio_audit_a_match.md
SKILL_MATRIX = {
    "Python":          {"weight": 1.0, "match": "expert"},        # 6× poptávka
    "Reverse Engineering": {"weight": 0.9, "match": "expert"},   # USP
    "CNC/CAM":         {"weight": 0.8, "match": "expert"},       # Doménová výhoda
    "GCP Cloud":       {"weight": 0.7, "match": "production"},   # 2× poptávka
    "Test Automation": {"weight": 0.7, "match": "production"},   # Golden master
    "IoT/ESP32":       {"weight": 0.6, "match": "production"},   # 1× poptávka
    "Docker":          {"weight": 0.6, "match": "production"},
    "CI/CD":           {"weight": 0.5, "match": "partial"},      # Chybí GitHub Actions
    "TypeScript":      {"weight": 0.5, "match": "gap"},          # Nutné doučit
    "Kubernetes":      {"weight": 0.4, "match": "gap"},          # Nutné doučit
    "PLC":             {"weight": 0.4, "match": "gap"},          # Nutné doučit
    "Azure":           {"weight": 0.3, "match": "gap"},          # AZ-900 plán
}
```

### 4.4 Domain classifier

```python
INDUSTRIAL_KEYWORDS = [
    "industrial automation", "manufacturing", "factory", "production",
    "PLC", "SCADA", "CNC", "CAM", "robotics", "assembly line",
    "industry 4.0", "iot", "sensor", "actuator", "control system",
    "process control", "quality control", "test engineering",
    "validation", "verification", "system integration",
    "electrical engineering", "mechanical engineering",
]

NON_INDUSTRIAL_KEYWORDS = [
    "customer service", "sales", "support", "account management",
    "help desk", "field service", "technical support",
    "SAP", "CRM", "ERP implementation", "business analyst",
    "frontend", "backend developer", "full stack",
]
```

---

## 5. Porovnání se stickerdaniel/linkedin-mcp-server

| Aspekt | stickerdaniel (v4.17.0) | linkedin-mcp-custom (navrh) |
|--------|------------------------|-----------------------------|
| **Kód** | ~5000+ řádků, 50+ souborů | ~800-1000 řádků, 10-12 souborů |
| **Saved jobs** | ❌ Neexistuje | ✅ Hlavní feature |
| **EROI scoring** | ❌ Chybí | ✅ Integrovaný engine |
| **Skill gap analysis** | ❌ Chybí | ✅ Proti portfolio_audit |
| **KB write-back** | ❌ Chybí | ✅ Report + metadata + git |
| **Job search** | ✅ Ano (10 filtrů) | ❌ Ne (zaměřeno na saved jobs) |
| **Person profiles** | ✅ Ano (10 sections) | ❌ Ne |
| **Company profiles** | ✅ Ano | ❌ Ne |
| **Feed scraping** | ✅ Ano (SDUI + DOM) | ❌ Ne |
| **Messaging** | ✅ Ano (inbox, send, search) | ❌ Ne |
| **Docker support** | ✅ Ano | ❌ Zatím ne |
| **CI/CD** | ✅ GitHub Actions | ❌ Zatím ne |
| **Auth** | ✅ Cookie + import from browser | ✅ Cookie (převzato) |
| **Browser** | ✅ Patchright | ✅ Patchright (převzato) |
| **Rate-limit handling** | ✅ Retry + sentinel | ✅ Převzato |
| **Noise stripping** | ✅ Chrome + conversation | ✅ Základní chrome stripping |

---

## 6. Fáze vývoje

### Fáze 0 — Projektový setup (den 1, ~2 h)

**Cíl:** Funkční vývojové prostředí s prvním "hello world" MCP serverem.

```
mkdir linkedin-mcp-custom && cd linkedin-mcp-custom
uv init
uv add fastmcp>=3.0.0 patchright>=1.40.0 python-dotenv
uv add --dev pytest pytest-asyncio ruff
```

**Struktura:**
```
linkedin-mcp-custom/
├── pyproject.toml
├── README.md
├── AGENTS.md
├── src/
│   └── linkedin_mcp_custom/
│       ├── __init__.py          # __version__
│       ├── server.py            # create_mcp_server()
│       └── cli.py               # Argument parser, main()
```

**Milník:** `uv run python -m linkedin_mcp_custom` vypíše "linkedin-mcp-custom v0.1.0"

### Fáze 1 — Browser management + auth (den 1-2, ~4 h)

**Cíl:** Cookie-based LinkedIn autentizace přes Patchright.

```
src/linkedin_mcp_custom/
├── core/
│   ├── __init__.py
│   ├── browser.py       # BrowserManager (singleton, Patchright wrapper)
│   ├── auth.py          # Cookie import/export, profile persistence
│   └── exceptions.py    # AuthenticationError, RateLimitError, atd.
```

**Klíčové soubory:**
- `core/browser.py` — `BrowserManager` třída, `get_or_create_browser()`, `close_browser()`
- `core/auth.py` — `login()`, `validate_session()`, cookie persistence
- `core/exceptions.py` — `AuthenticationError`, `RateLimitError`, `LinkedInScraperException`

**Milník:** `uv run python -m linkedin_mcp_custom --login` otevře Chromium, přihlásí se, uloží cookies.
`uv run python -m linkedin_mcp_custom --status` vrátí "Session valid."

### Fáze 2 — Scraping engine (den 2-3, ~4 h)

**Cíl:** Základní scraping: navigace → innerText → noise strip.

```
src/linkedin_mcp_custom/
├── scraping/
│   ├── __init__.py
│   ├── extractor.py     # LinkedInExtractor
│   └── utils.py         # noise_strip(), rate_limit_detect(), modal_dismiss()
```

**Extractor API:**
```python
class LinkedInExtractor:
    def __init__(self, page: Page): ...
    async def navigate_to_page(self, url: str) -> None: ...
    async def extract_page(self, url: str) -> ExtractedSection: ...
    async def scrape_job(self, job_id: str) -> dict: ...
    async def scrape_saved_jobs(self) -> dict: ...
```

**Milník:** `extractor.scrape_job("1234567890")` vrátí `{url, sections: {job_posting: "..."}}`

### Fáze 3 — MCP tools registrace (den 3, ~2 h)

**Cíl:** Funkční MCP server s 2-3 nástroji.

```
src/linkedin_mcp_custom/
├── tools/
│   ├── __init__.py
│   ├── job.py           # get_saved_jobs, get_job_details
│   └── analysis.py      # analyze_saved_jobs
```

**Tool registry v `server.py`:**
```python
def create_mcp_server() -> FastMCP:
    mcp = FastMCP("linkedin-mcp-custom", version=__version__)
    
    @mcp.tool()
    async def get_saved_jobs(ctx: Context) -> dict: ...
    
    @mcp.tool()
    async def analyze_saved_jobs(ctx: Context) -> dict: ...
    
    return mcp
```

**Milník:**
```json
// Client call: {"method": "tools/call", "params": {"name": "get_saved_jobs", "arguments": {}}}
// Response: {"url": "...", "sections": {"saved_jobs": "..."}, "job_ids": ["4252026496", ...]}
```

### Fáze 4 — EROI engine (den 3-5, ~6 h)

**Cíl:** Plně funkční scoring engine implementující golden rules.

```
src/linkedin_mcp_custom/
├── analysis/
│   ├── __init__.py
│   ├── domain.py        # domain_score() — 35 %
│   ├── tech.py          # tech_score() — 25 %
│   ├── role.py          # role_score() — 20 %
│   ├── growth.py        # growth_score() — 10 %
│   ├── formal.py        # formal_score() — 5 %
│   ├── location.py      # location_score() — 5 %
│   ├── scorer.py        # Orchestrator: weighted_total + thresholds
│   └── matcher.py       # Skill gap analysis (direct/partial/no match)
```

**Scorer API:**
```python
def analyze_job(job_data: dict, portfolio: dict) -> AnalysisResult:
    """
    Returns:
        AnalysisResult(
            total_score=72.0,
            category="SLEDOVAT",
            dimensions={
                "domain": 80,
                "tech": 65,
                "role": 70,
                "growth": 60,
                "formal": 50,
                "location": 80,
            },
            skill_gaps=[
                Gap(skill="TypeScript", severity="medium"),
                Gap(skill="Azure", severity="low"),
            ],
            recommendation="Aplikovat po doplnění TypeScript základů.",
        )
    """
```

**Test data:** 24 existujících nabídek z KB jako regression test suite.
`pytest tests/test_eroi.py` musí potvrdit, že:
- Siemens #007 → ≥65 % (SLEDOVAT)
- Desoutter #003 → ≥65 % (SLEDOVAT)
- Apify #001 → <40 % (NESLEDOVAT)
- Accenture #002 → <40 % (NESLEDOVAT)

**Milník:** `scorer.analyze(job_text)` dává konzistentní výsledky s historickými daty.

### Fáze 5 — KB writer (den 5-6, ~3 h)

**Cíl:** Zápis výsledků do B2B-Knowledge-Base.

```
src/linkedin_mcp_custom/
├── analysis/
│   └── kb_writer.py     # append_report(), update_metadata(), git_commit()
```

**KB Writer API:**
```python
def append_report(job: dict, analysis: AnalysisResult, path: Path) -> None:
    """Appends formatted section to agregovany_report.md"""

def update_metadata(job: dict, analysis: AnalysisResult, path: Path) -> None:
    """Inserts entry into metadata_stacku.json, refreshes aggregate_insights"""

def git_commit(repo_path: Path, message: str) -> None:
    """git add + git commit (no push unless --push flag)"""
```

**Formát zprávy:** Viz `agregovany_report.md` — dodržet strukturu:
```
## 🔴/🟡/🟢 ZÁZNAM #N — Title @ Company
**Datum:** YYYY-MM-DD
**EROI verdict:** SLEDOVAT / NESLEDOVAT (XX % fit)
### Analýza pozice
- **Role:** ...
### Fit hodnocení
- **Doména (35 %):** ...
### EROI analýza
| Faktor | Hodnocení |
### Závěr
```

**Milník:** `kb_writer.write(job_data, analysis)` vytvoří appendix v `agregovany_report.md`.

### Fáze 6 — End-to-end pipeline (den 6, ~2 h)

**Cíl:** Jediný příkaz: `uv run analyze-saved` provede celý workflow.

```python
# cli.py
@app.command()
async def analyze_saved():
    """Full pipeline: scrape → score → write → commit."""
    extractor = await get_ready_extractor()
    saved = await extractor.scrape_saved_jobs()
    
    results = []
    for job_id in saved["job_ids"]:
        job = await extractor.scrape_job(job_id)
        analysis = scorer.analyze(job["sections"]["job_posting"])
        kb_writer.write(job, analysis)
        results.append(analysis)
    
    kb_writer.commit(f"[LINKEDIN] analyze: {len(results)} saved jobs")
    print(f"✅ Analyzováno {len(results)} nabídek")
```

**Milník:** `uv run analyze-saved` → 5-10 minut → hotový report v B2B-Knowledge-Base.

### Fáze 7 — DevOps + finalizace (den 6-7, ~2 h)

**Cíl:** Produkčně připravený kód.

- `pyproject.toml` — scripts (`uv run analyze-saved`), entry point
- `AGENTS.md` — dev commands, scraping rules (jako stickerdaniel)
- Pre-commit hooks (ruff format + check)
- README.md s: instalace, konfigurace, použití, architektura
- Volitelně: Dockerfile, GitHub Actions CI

---

## 7. Srovnání — velikost kódu

| Vrstva | stickerdaniel (řádky) | linkedin-mcp-custom (odhad) | Rozdíl |
|--------|----------------------|----------------------------|--------|
| server.py | 88 | 60 | -28 |
| auth | 86 | 80 | -6 |
| browser | 632 | 150 | -482 (★) |
| tools/* | 519 (job+person) | 100 (job only) | -419 |
| extractor | 3700 | 250 | -3450 (★) |
| fields.py | 88 | — | — |
| core/* | 39 (init) + ? | 100 | — |
| analysis/* | — | 400 | +400 (★) |
| **Celkem** | **~5000+** | **~1140** | **-3860** |

(★) Hlavní důvody:
- **Browser: 632 → 150** — stickerdaniel má Docker bridge, derived runtime persistence, feed auth check, cookie export/import pro 3 runtime módy. My potřebujeme jen základní singleton.
- **Extractor: 3700 → 250** — stickerdaniel má: feed (SDUI parsing, RSC flight data, scroll loop), messaging (inbox, conversation, send, search, recipient picker), connect person (6 connection states, More menu, incoming accept), company people, sidebar profiles. My potřebujeme jen: navigate, extract page, scrape job, scrape saved jobs.
- **Analysis: 0 → 400** — jediné co přidáváme navíc.

---

## 8. Rizika a mitigace

| Riziko | Pravděpodobnost | Dopad | Mitigace |
|--------|----------------|-------|----------|
| LinkedIn změní /jobs-tracker/ layout | Nízká | Střední | innerText extraction je resilientní. Stačí přeladit noise stripping. |
| Anti-bot detekce (rate-limit) | Střední | Vysoký | Patchright anti-detection + cookie persistence + přestávky mezi requesty. |
| Auth session expirace | Střední | Vysoký | Pravidelná cookie refresh, detect + re-login prompt. |
| EROI skóre nesedí s realitou | Střední | Nízký | Test suite s 24 historickými nabídkami. Kalibrace vah na datech. |
| Git write konflikt | Nízký | Nízký | Append-only pattern. Metadata update přes merge, ne přepis. |
| FastMCP API changes | Nízká | Nízký | Pin version fastmcp>=3.0.0, <4.0.0. |

---

## 9. Závislosti

```toml
# pyproject.toml
[project]
name = "linkedin-mcp-custom"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastmcp>=3.0.0",
    "patchright>=1.40.0",
    "python-dotenv>=1.1.1",
]

[project.scripts]
linkedin-mcp-custom = "linkedin_mcp_custom.cli:main"

[tool.ruff]
line-length = 88
target-version = "py312"
```

---

## 10. Dev workflow (AGENTS.md)

```
# Dev commands
uv sync                          # Install deps
uv run python -m linkedin_mcp_custom --login   # First-time auth
uv run python -m linkedin_mcp_custom --status  # Check session
uv run python -m linkedin_mcp_custom           # Start MCP server
uv run analyze-saved                           # Full pipeline
uv run pytest                    # Run tests (EROI regression)
uv run ruff check .              # Lint
uv run ruff format .             # Format
uv run patchright install chromium  # Install browser

# Scraping rules (per stickerdaniel)
- Prefer innerText and URL navigation over DOM selectors.
- Minimize DOM dependence — use generic selectors (a[href*="/jobs/view/"])
- One section = one navigation
- Detection must be locale-independent
```

---

*Tento dokument je živý. Po každé fázi se aktualizují odhady a rizika.*
