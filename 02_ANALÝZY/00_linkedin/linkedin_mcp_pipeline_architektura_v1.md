# LinkedIn MCP Pipeline — Architektura automatizované analýzy nabídek

**Datum:** 2026-07-05 | **Autor:** outpost2026
**Účel:** Návrh pipeline pro automatizaci sběru, parsování a EROI hodnocení LinkedIn nabídek pomocí MCP serverů

---

## 1. Problém a cíl

### 1.1 Současný stav (ruční workflow)

1. Uživatel si uloží nabídku na LinkedIn (`/jobs-tracker/`)
2. Ručně otevře každou nabídku, copy-paste full textu do OpenCode
3. LLM analyzuje, spočítá fit score, zapíše do `agregovany_report.md`
4. Metadata se ručně přidají do `metadata_stacku.json`

**Problém:** Neškálovatelné, časově náročné, chybovost při ručním přepisu.

### 1.2 Cílový stav

```
LinkedIn (uložené nabídky)
       │
       ▼
   MCP server (extrakce)
       │
       ▼
   Parsování → EROI scoring → Zápis do KB
       │
       ▼
   Notifikace (nové relevantní nabídky)
```

### 1.3 Existující KB artefakty (kostra pipeline)

| Soubor | Účel v pipeline |
|--------|-----------------|
| `agregovany_report.md` | Cílový výstup — EROI hodnocení jednotlivých nabídek |
| `metadata_stacku.json` | Strojově čitelná data o nabídkách (schema pro parsování) |
| `synteticky_report_analyza.md` | Golden rules weighting, thresholdy, kalibrace vah |
| `portfolio_audit_a_match.md` | Skill match matice — autorův stack vs. tržní poptávka |

---

## 2. Deep dive: MCP servery pro LinkedIn

### 2.1 Přehled existujících řešení

| Server | Jazyk | Auth | Tooly | Hvězdy | Status |
|--------|-------|------|-------|--------|--------|
| **stickerdaniel/linkedin-mcp-server** | Python | Cookie (Playwright) | `search_jobs`, `get_job_details`, `get_person_profile`, `get_company_profile`, `search_people`, `send_message` | ~150 | ✅ Aktivní, 20+ contributorů |
| **pauling-ai/linkedin-mcp-server** (fork) | Python | Cookie (Playwright) | To samé + messaging, post engagement | 3 | ✅ Aktivní fork |
| **mvanhorn/linkedin-mcp-server** (fork) | Python | Cookie (Playwright) | To samé + `get_inbox`, `get_conversation`, `connect_with_person` | Nový | ✅ Aktivní |
| **hubertusgbecker/mcp-linkedin-server** (fork) | Python | Cookie (Playwright) | + notifikace, plný post extraction, profile analytics | Nový | ✅ Aktivní |
| **sanu495/linkedin-mcp-server** (fork) | Python | Cookie (Playwright) | + `close_browser` | Nový | ✅ Aktivní |
| **wlyonscat/server-mcp-linkedin** | Python | Cookie (Playwright) | + **resume/CL generování**, **application tracking** | Nový | ✅ FastMCP |
| **akvinayaktiwari/LinkedIn-MCP-Server** | Python | API? | `get_my_profile`, `search_jobs`, `create_post`, `get_connections` | Nový | ⚠️ Základní |
| **linkedin-jobs-mcp-server** (npm) | TS | **Bez auth** | `search_linkedin_jobs` — pouze veřejné vyhledávání | — | ⚠️ Omezený |
| **ahardy42/job-search-mcp** | TS | Bez auth | `job_search`, `job_description_search` | — | ⚠️ Omezený |

### 2.2 Detail: stickerdaniel/linkedin-mcp-server (doporučený základ)

**Nejzralejší a nejaktivnější LinkedIn MCP server.**

**Architektura:**
- Python + FastMCP
- Playwright pro browser automation
- Cookie-based autentikace (první login ručně, pak storage_state)
- STDIO transport

**Klíčové tooly:**

| Tool | Parametry | Výstup |
|------|-----------|--------|
| `search_jobs` | keywords, location, limit=25 | Seznam job URL + total count |
| `get_job_details` | job_id | title, company, location, posted_date, applicants_count, full_description, seniority, employment_type, job_function, industries, benefits, direct URL |
| `get_person_profile` | public_identifier, sections | Strukturovaný profil (experience, education, skills, certifications...) |
| `get_company_profile` | public_identifier, sections | Company info, posts, jobs |
| `search_people` | keywords, location, limit | Seznam profilů |

**Instalace:**
```bash
# Přes uvx (doporučeno)
uvx linkedin-mcp-server

# Nebo lokálně
git clone https://github.com/stickerdaniel/linkedin-mcp-server
cd linkedin-mcp-server
uv run linkedin-mcp-server
```

**Autentikace (první spuštění):**
```
1. Server spustí Playwright browser (headless=False)
2. Uživatel se přihlásí ručně na linkedin.com
3. Session se uloží do linkedin_state.json
4. Při dalších spuštěních se session reloadne (headless=True)
```

### 2.3 Co existující MCP servery **neumí**

| Funkce | Dostupná? | Důvod |
|--------|-----------|-------|
| Čtení uložených nabídek | ❌ | LinkedIn nemá API endpoint; nutné custom Playwright scraping `/jobs-tracker/` |
| Automatický EROI scoring | ❌ | Vyžaduje napojení na authorovu KB (skill matice, golden rules) |
| Zápis do agregovany_report.md | ❌ | Vyžaduje znalost struktury KB a commit logiky |
| Hromadná analýza nových nabídek | ❌ | Není implementováno v žádném existujícím MCP serveru |

### 2.4 API vs. Scraping — technická omezení

| Aspekt | Veřejná API (linkedin-jobs-api) | Playwright scraping | Voyager API (volaný z browseru) |
|--------|----------------------------------|---------------------|-------------------------------|
| **Auth potřeba** | Ne | Ano (cookie) | Ano (cookie + csrf) |
| **Uložené nabídky** | ❌ | ✅ | ⚠️ Možné, queryId rotuje |
| **Full-text detailu** | ❌ (jen perex) | ✅ | ⚠️ Částečně |
| **Blokování** | ✅ Mírné | ⚠️ Medium (stealth potřebný) | ✅ Málo (voláno z browseru) |
| **Údržba** | ✅ Stabilní | ⚠️ Selektory rotují | ❌ queryId rotuje každé týdny |

**Doporučení:** Playwright scraping DOM cestou (nejrobustnější poměr údržba/funkce).

---

## 3. Varianta A: Basic — Maximalní využití existujících MCP serverů

### 3.1 Architektura

```
                    ┌──────────────────────────────┐
                    │      OpenCode / Cline         │
                    │   (orchestrační vrstva)        │
                    └──────┬───────────────┬────────┘
                           │               │
              ┌────────────┴─────┐   ┌─────┴──────────────┐
              │  mcp-local-server │   │linkedin-mcp-server  │
              │  (20 custom toolů)│   │(stickerdaniel fork) │
              │                   │   │                    │
              │ + linkedin_saved_ │   │ search_jobs        │
              │   jobs_list       │   │ get_job_details    │
              │ + linkedin_analyze│   │ get_person_profile │
              │   _saved          │   │ get_company_profile│
              └────────┬──────────┘   └────────────────────┘
                       │
              ┌────────┴──────────┐
              │  B2B-Knowledge-Base│
              │  (agregovany_report│
              │   metadata_stacku │
              │   .json, INDEX.md)│
              └───────────────────┘
```

### 3.2 Komponenty

#### 3.2.1 Existující: `linkedin-mcp-server` (žádný vývoj)

Stačí přidat do konfigurace OpenCode:
```json
{
  "mcpServers": {
    "linkedin": {
      "command": "uvx",
      "args": ["linkedin-mcp-server"]
    }
  }
}
```

Poskytuje: `search_jobs`, `get_job_details`, profily, firmy.

#### 3.2.2 Custom tool #1: `linkedin_saved_jobs_list` (nový, ~100 ř.)

**Zařazení:** `mcp-local-server/src/mcp_local_server/tools/linkedin_jobs.py`

**Funkce:** Extrahuje seznam uložených nabídek z `/jobs-tracker/` Saved tab.

**Technologie:** Playwright (již v .venv), storage_state session.

**Výstup:**
```
📋 Nalezeno 12 uložených nabídek (kontrola: 2026-07-05 14:00)

| # | Job ID       | Firma                | Název pozice                     | Match | Applicantů |
|---|-------------|----------------------|----------------------------------|-------|------------|
| 1 | 4252026496  | MSM GROUP            | Logistics & System Architect     | 0/10  | 7          |
| 2 | 4251987632  | TD SYNNEX            | AI Integrator                    | —     | 18         |
...

🆕 Nové od poslední kontroly: 3
```

**Cache:** Ukládá job_id do `linkedin_saved_cache.json` (v KB `02_ANALÝZY/00_linkedin/`).

#### 3.2.3 Custom tool #2: `linkedin_analyze_saved` (nový, ~200 ř.)

**Zařazení:** `mcp-local-server/src/mcp_local_server/tools/linkedin_jobs.py`

**Funkce:** Projde nové nabídky, stáhne detail (přes `get_job_details` z linkedin-mcp-server), spočítá EROI, zapíše do KB.

**Výstup:**
```
🔍 ANALÝZA NOVÝCH NABÍDEK (2026-07-05)

1. MSM GROUP — Logistics & System Architect (58 % fit)
   ✅ Silný positioning match (85 %)
   ⚠️ Domain gap: logistics vs manufacturing
   🟡 SLEDOVAT

2. TD SYNNEX — AI Integrator (37 % fit)
   ❌ Domain mismatch (enterprise IT)
   ❌ ML frameworks gap
   🔴 NESLEDOVAT

Zapsáno do agregovany_report.md jako #015, #018.
```

### 3.3 Workflow orchestrace (v OpenCode)

```
1. Uživatel spustí:
   → "Zkontroluj nové LinkedIn nabídky"

2. OpenCode volá:
   → mcp-local-server → linkedin_saved_jobs_list()
     → Playwright otevře jobs-tracker
     → Porovná s cache, najde nové

3. Pro každou novou nabídku:
   → linkedin-mcp-server → get_job_details(job_id)
   → mcp-local-server → linkedin_analyze_saved(job_data)
     → Spočítá fit score dle golden rules
     → Zapíše do agregovany_report.md
     → Přidá do metadata_stacku.json
     → Commitne do KB

4. Výstup:
   → "3 nové nabídky. 2 NESLEDOVAT, 1 SLEDOVAT (MSM GROUP 58 %)."
```

### 3.4 Odhad náročnosti

| Komponenta | Status | Odhad |
|------------|--------|-------|
| Instalace linkedin-mcp-server | ⚙️ 5 min | `uvx linkedin-mcp-server` |
| První login (cookie session) | ⚙️ 2 min | Ručně, jednorázově |
| `linkedin_saved_jobs_list` | 🔧 1-2 h | Playwright + DOM scraping |
| `linkedin_analyze_saved` | 🔧 2-3 h | EROI engine + zápis do KB |
| Testy | 🔧 1 h | Skicy pro tooly |
| **Celkem Basic** | | **~4-6 h** |

---

## 4. Varianta B: Complex — Plná integrace do mcp-local-server

### 4.1 Architektura

```
                    ┌──────────────────────────────────────┐
                    │           mcp-local-server            │
                    │                                      │
                    │  linkedin/                           │
                    │  ├── linkedin_jobs.py                │
                    │  │   ├── linkedin_saved_jobs_list    │
                    │  │   ├── linkedin_job_detail         │
                    │  │   ├── linkedin_analyze_saved      │
                    │  │   └── linkedin_search             │
                    │  ├── linkedin_scraper.py             │
                    │  │   ├── LinkedInSavedJobsScraper    │
                    │  │   └── LinkedInJobDetailScraper    │
                    │  └── linkedin_profile.py            │
                    │      ├── linkedin_profile_lookup     │
                    │      └── linkedin_company_lookup     │
                    │                                      │
                    │  scoring/                            │
                    │  ├── eroi_engine.py                  │
                    │  │   ├── compute_fit_score           │
                    │  │   └── calculate_eroi              │
                    │  └── golden_rules.py                 │
                    │      ├── domain_matcher              │
                    │      ├── tech_stack_matcher          │
                    │      └── skill_gap_analyzer          │
                    │                                      │
                    │  kb_writer/                          │
                    │  ├── agregovany_report_writer.py     │
                    │  └── metadata_stacku_writer.py       │
                    │                                      │
                    │  linkedin_state.json                 │
                    │  linkedin_saved_cache.json           │
                    └──────────────────────────────────────┘
```

### 4.2 Komponenty

#### 4.2.1 `linkedin/linkedin_scraper.py` — Playwright wrapper

Třída `LinkedInSavedJobsScraper`:
```python
class LinkedInSavedJobsScraper:
    STATE_FILE = "linkedin_state.json"
    
    async def __aenter__(self): ...  # init Playwright, load session
    async def login(self): ...       # headless=False, manual login
    async def get_saved_jobs(self) -> list[dict]: ...  # DOM scraping jobs-tracker
    async def get_job_detail(self, job_id: str) -> dict: ...  # full detail from /jobs/view/
    async def close(self): ...
```

#### 4.2.2 `linkedin/linkedin_jobs.py` — MCP tooly (4 tooly)

| Tool | Popis | Parametry |
|------|-------|-----------|
| `linkedin_saved_jobs_list` | Seznam uložených nabídek | max_results, refresh |
| `linkedin_job_detail` | Full-text detail + struktura | job_id |
| `linkedin_analyze_saved` | Hromadná EROI analýza nových | max_results, auto_write |
| `linkedin_search` | Vyhledávání na LinkedIn | keywords, location, filters |

#### 4.2.3 `scoring/eroi_engine.py` — EROI scoring engine

Napojení na existující golden rules:

```python
# Načte váhy ze synteticky_report_analyza.md
WEIGHTS = {
    "domain": 0.35,
    "tech_stack": 0.25,
    "role": 0.20,
    "growth": 0.10,
    "formal": 0.05,
    "location": 0.05,
}

# Načte autorův stack z portfolio_audit_a_match.md
AUTHOR_STACK = {
    "languages": ["Python"],
    "cloud": ["GCP"],
    "frameworks": ["Streamlit", "FastAPI"],
    "domains": ["CNC/CAM", "manufacturing", "RE", "IoT/ESP32"],
    "methodologies": ["system_integration", "golden_master_testing"],
}

def compute_fit_score(job: dict) -> float:
    """Vrací weighted fit score 0-100 podle golden rules."""
    domain_score = domain_matcher(job["domain"], AUTHOR_STACK["domains"])
    tech_score = tech_stack_matcher(job["tech_stack"], AUTHOR_STACK)
    role_score = role_matcher(job["title"], job["description"])
    ...
    return weighted_sum
```

#### 4.2.4 `scoring/golden_rules.py` — Matching engine

- `domain_matcher(job_domain, author_domains)` → 0-100
  - Přesná shoda: 85-100
  - Adjacent (manufacturing → logistics): 40-60
  - Mimo (enterprise IT): 10-20
- `tech_stack_matcher(job_tech, author_stack)` → 0-100
  - Koreluje proti `metadata_stacku.json` overlap_with_author
- `skill_gap_analyzer(job_requirements, author_skills)` → list[gap]
  - Vrací dovednosti chybějící v autorově stacku

#### 4.2.5 `kb_writer/` — Automatický zápis do KB

```python
class AgregovanyReportWriter:
    def append_entry(self, entry: dict):
        """Přidá nový záznam #XXX do agregovany_report.md."""
        # 1. Najde poslední číslo záznamu
        # 2. Vygeneruje formátovaný blok (nadpis, fit hodnocení, EROI, strategie)
        # 3. Vloží před "Souhrnná statistika"
        # 4. Aktualizuje souhrnnou tabulku

class MetadataStackuWriter:
    def append_entry(self, entry: dict):
        """Přidá entry do metadata_stacku.json a refresh aggregace."""
```

### 4.3 Konfigurace

V `mcp-local-server/.env`:
```ini
LINKEDIN_EMAIL=xxx
LINKEDIN_PASSWORD=xxx
LINKEDIN_HEADLESS=true
LINKEDIN_ANALYZE_AUTO_WRITE=true
```

V `mcp-local-server/config.py`:
```python
LINKEDIN_CACHE_PATH = KB_ROOT / "02_ANALÝZY" / "00_linkedin" / "linkedin_saved_cache.json"
LINKEDIN_STATE_PATH = PROJECT_ROOT / "linkedin_state.json"
```

### 4.4 Plný workflow (diagram)

```
┌─────────────────────────────────────────────────────────────────────┐
│ 1. TRIGGER                                                          │
│    "Zkontroluj LinkedIn" / cron (daily) / manual                    │
└──────────────────────────┬──────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 2. EXTRACT                                                          │
│    linkedin_saved_jobs_list(refresh=True)                           │
│      → Playwright: jobs-tracker, DOM scrape                        │
│      → Porovnání s linkedin_saved_cache.json                       │
│      → Identifikace NOVÝCH nabídek (ne v cache)                    │
└──────────────────────────┬──────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 3. FETCH DETAILS                                                    │
│    Pro každou NOVOU nabídku:                                        │
│      → linkedin_job_detail(job_id)                                  │
│        → Playwright: /jobs/view/{id}/, full-text extrakce          │
│      → Parsování do strukturovaného dictu:                          │
│        {title, company, location, domain, tech_stack,               │
│         requirements, benefits, description, applicants}            │
└──────────────────────────┬──────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 4. ANALYZE                                                          │
│    Pro každou nabídku:                                              │
│      → eroi_engine.compute_fit_score(job_data)                      │
│        → domain_matcher: 35 % váha                                  │
│        → tech_stack_matcher: 25 % váha                              │
│        → role_matcher: 20 % váha                                    │
│        → growth_potential: 10 % váha                                │
│        → formal_requirements: 5 % váha                              │
│        → location: 5 % váha                                         │
│      → skill_gap_analyzer(job_data, author_stack)                   │
│      → EROI výpočet (P converze × hodnota / čas)                   │
└──────────────────────────┬──────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 5. WRITE TO KB                                                      │
│    Pro SLEDOVAT nabídky:                                            │
│      → kb_writer.append_entry(entry)                                │
│        → Do agregovany_report.md (formátovaný blok)                 │
│        → Do metadata_stacku.json (strojový záznam)                  │
│        → git add + git commit (dle AGENTS.md)                       │
│    Vždy:                                                             │
│      → linkedin_saved_cache.json (update timestamp)                 │
└──────────────────────────┬──────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 6. REPORT                                                           │
│    "✅ Analýza dokončena. 3 nové nabídky:                           │
│       🔴 NESLEDOVAT: TD SYNNEX (37 %), Sourcein (24 %)             │
│       🟡 SLEDOVAT: MSM GROUP (58 %)                                 │
│     Zapsáno do KB jako #015-#018.                                    │
│     Commit: [ANALÝZY] add: 3 new LinkedIn offers #015-#018"         │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.5 Odhad náročnosti

| Komponenta | Odhad | Závislosti |
|------------|-------|------------|
| `linkedin_scraper.py` | 2-3 h | Playwright, storage_state |
| `linkedin_jobs.py` (4 tooly) | 2 h | scraper |
| `eroi_engine.py` | 2-3 h | golden_rules, synteticky_report |
| `golden_rules.py` | 2 h | metadata_stacku, portfolio_audit |
| `kb_writer/` | 2-3 h | markdown templating, git |
| Testy | 2 h | pytest, mock scraper |
| Konfigurace + .env | 30 min | config.py |
| **Celkem Complex** | | **~12-16 h** |

---

## 5. Vazba na existující KB artefakty

### 5.1 Schema mapping: JSON kostra

Struktura `metadata_stacku.json` definuje **výstupní schema** pro každou nabídku:

```json
{
  "id": "XXX",
  "date": "2026-07-05",
  "company": {
    "type": "manufacturing",
    "size_range": "medium",
    "industry": "industrial_automation"
  },
  "title": "Job Title",
  "role": {
    "category": "industrial_automation",
    "subcategory": "test_engineer",
    "seniority": "medior",
    "employment_type": "HPP",
    "location": "Praha",
    "remote_policy": "hybrid",
    "applicants": 12
  },
  "tech_stack": {
    "programming": ["Python"],
    "frameworks": ["..."],
    "overlap_with_author": {
      "direct_match": ["Python"],
      "partial_match": [],
      "no_match": ["..."],
      "_auto_generated": true
    }
  },
  "domain": {
    "primary": "industrial_automation",
    "secondary": "...",
    "specific": "..."
  },
  "formal_requirements": {
    "years_experience_min": 3,
    "education": null,
    "languages": ["English"]
  },
  "eroi": {
    "fit_score_pct": 58,
    "conversion_probability": "0.30_0.40",
    "estimated_value_monthly_czk": 120000,
    "estimated_prep_cost_hours": 3,
    "verdict": "SLEDOVAT",
    "critical_mismatch": false,
    "mismatch_dimensions": [],
    "_generated_by": "linkedin_analyze_saved"
  }
}
```

**Poznámka:** `overlap_with_author` a `eroi` sekce jsou **generovány automaticky** EROI enginem, nikoliv ručně.

### 5.2 Golden rules vazba

Soubor `synteticky_report_analyza.md` definuje:

| Pravidlo | Použití v pipeline |
|----------|-------------------|
| Váhy dimenzí (domain 35 %, tech 25 %, ...) | Základ `eroi_engine.compute_fit_score()` |
| Thresholdy (≥65 % SLEDOVAT high, 50-64 % medium...) | Klasifikace výsledku |
| SNR technologií (PLC 66.7 %, Python 50 %) | Priorizace tech stack matcheru |
| Confusion matrix | Kalibrace domain matcheru |

### 5.3 Skill match vazba

Soubor `portfolio_audit_a_match.md` (skill match matrix) definuje:

| Skill | GitHub evidence | Použití v pipeline |
|-------|-----------------|-------------------|
| Python | ✅ Expert | Direct match |
| Reverse Engineering | ✅ Expert | Unikátní USP boost |
| TypeScript/Playwright | ❌ Gap | Deduction v tech matcheru |
| PLC | ❌ Gap | Deduction v tech matcheru |

Tyto hodnoty jsou načteny do `scoring/golden_rules.AUTHOR_STACK` a použity při `tech_stack_matcher()` a `skill_gap_analyzer()`.

### 5.4 Výstupní formát: agregovany_report.md

Pipeline generuje entry v existujícím formátu:

```markdown
## 🟡 ZÁZNAM #XXX — Název pozice @ Firma
**Datum:** 2026-07-05
**EROI verdict:** SLEDOVAT — popis (≈XX % fit)

### Analýza pozice
- **Role:** ...
- **Seniorita:** ...
- **Typ:** ...
- **Doména:** ...
- **Firma:** ...
- **Stack:** ...
- **LinkedIn skill match:** ..., **X uchazečů**

### Fit hodnocení
| Dimenze | Váha | Match | Váženě | Komentář |
| ... (generováno EROI enginem)

### Kvalitativní vhled
... (generováno LLM z full-textu + fit score)

### EROI analýza
| Faktor | Hodnocení |
| ... (generováno EROI enginem)

### Strategie
... (generováno LLM pro SLEDOVAT nabídky)

---

## 6. Implementační roadmapa

### Fáze 1: Basic (4-6 h) — OKAMŽITÁ HODNOTA

```
1. Instalace linkedin-mcp-server → uvx linkedin-mcp-server
2. linkedin_saved_jobs_list → Playwright, DOM scrape, cache
3. linkedin_analyze_saved → EROI scoring, tabulkový výstup
4. Ruční zápis do KB (automatizovaný výstup, manuální commit)
```

### Fáze 2: Scoring engine (+6 h) — AUTOMATIZACE SKÓROVÁNÍ

```
1. golden_rules.py → domain_matcher, tech_stack_matcher
2. eroi_engine.py → weighted scoring, EROI kalkulace
3. Automatické overlap_with_author generování
```

### Fáze 3: KB writer (+6 h) — PLNÁ AUTOMATIZACE

```
1. agregovany_report_writer.py → append, update summary
2. metadata_stacku_writer.py → append, refresh aggregate
3. Git commit (dle AGENTS.md)
```

### Fáze 4: Notifikace (+2 h) — PROAKTIVNÍ REŽIM

```
1. linkedin_saved_jobs_list → notifikace o nových nabídkách
2. Daily cron / OpenCode schedule
3. Report push (GitHub / email / Telegram)
```

---

## 7. Bezpečnost a údržba

### 7.1 Credentials

| Co | Kde | .gitignore? |
|----|-----|-------------|
| `LINKEDIN_EMAIL` | `.env` | ✅ |
| `LINKEDIN_PASSWORD` | `.env` | ✅ |
| `linkedin_state.json` | kořen projektu | ✅ |
| `linkedin_saved_cache.json` | KB `02_ANALÝZY/00_linkedin/` | ❌ (verzovat) |

### 7.2 LinkedIn anti-bot

| Opatření | Implementace |
|----------|-------------|
| Storage state persistence | Sníží počet loginů na 1× |
| Headless=False při prvním loginu | Přirozený browser fingerprint |
| Dynamic delays | `random.uniform(2, 5)` mezi akcemi |
| Rate limiting | Max 1 request / 3 sec |
| Session refresh | Reload každých 24 h |

### 7.3 Údržba

| Riziko | Frekvence | Mitigace |
|--------|-----------|----------|
| Změna DOM selektorů LinkedIn | Každých 2-3 měsíce | Fallback selektory, XPath |
| Rotace queryId | Každé týdny | (Pouze pokud použita Voyager API cesta) |
| LinkedIn blokuje session | Občasně | Notifikace, manual re-login |
| Změna golden rules vah | Dle autorova uvážení | Parametrizace v configu |

---

## 8. Srovnání variant

| Aspekt | Basic (Var A) | Complex (Var B) |
|--------|---------------|-----------------|
| **Čas do první hodnoty** | ~1 den | ~3-4 dny |
| **Množství nového kódu** | ~300 ř. | ~1500 ř. |
| **Závislost na externím MCP** | Vysoká (linkedin-mcp-server) | Nízká (vlastní scraper) |
| **Automatický scoring** | Základní (váhy, tabulka) | Plný (domain/tech/role matcher) |
| **Automatický zápis do KB** | ❌ (pouze výstup) | ✅ (append + commit) |
| **Notifikace** | ❌ | ✅ |
| **Údržba** | Nízká (stačí update MCP serveru) | Střední (vlastní kód) |
| **Vendor lock-in** | ⚠️ linkedin-mcp-server | ✅ Žádný |

---

## 9. Open questions

1. **Frekvence kontroly:** Denně? Týdně? Pouze na vyžádání?
2. **Notifikace:** Kam? (GitHub issue, email, Telegram, OpenCode prompt?)
3. **Míra automatizace zápisu:** Má pipeline rovnou commitovat do KB, nebo jen zobrazit výsledek k review?
4. **Historické nabídky:** Chcete při prvním spuštění analyzovat všechny uložené nabídky, nebo jen nové?
5. **LinkedIn search vs. saved:** Chcete pouze analyzovat uložené, nebo aktivně vyhledávat nové dle kritérií?

---

## 10. Odkazy

- [stickerdaniel/linkedin-mcp-server](https://github.com/stickerdaniel/linkedin-mcp-server) — hlavní MCP server
- [agregovany_report.md](agregovany_report.md) — výstupní report
- [metadata_stacku.json](metadata_stacku.json) — strojové schema
- [synteticky_report_analyza.md](synteticky_report_analyza.md) — golden rules
- [portfolio_audit_a_match.md](../01_portfolio_audit/portfolio_audit_a_match.md) — skill matrix
- [AGENTS.md](../../AGENTS.md) — commit pravidla
- [INDEX.md](../../INDEX.md) — registr artefaktů
