# EROI Chronologický plán & Metodické kostry optimalizací

**Autor profilu:** Ondřej Soušek — Systems Integrator (industrial automation, formalizace, reverse engineering, MCP tooling)
**Datum:** 2026-08-06
**Verze:** 2.0 (aktualizace v1.0 z 2026-06-25)
**Zdroje:** Korekce_vektoru_rozvoje_OS.json, agregovany_report.md, metadata_stacku.json, portfolio_audit_v2.md, Live GitHub API audit
**Provenance:** Live GitHub API (2026-08-06), ověřeno proti skutečnému stavu repozitářů

---

## Přehledová mapa

```
                     EROI (dopad / náklady)
                    ┆
   VELMI VYSOKÝ     ┆  ❶ LinkedIn opt. ─── ❷ Aplikace follow leads
                    ┆
   VYSOKÝ           ┆  ❸ TypeScript ─── ❹ AZ-900 ─── ❺ GitHub Actions
                    ┆
   STŘEDNÍ-VYSOKÝ   ┆  ❻ RE publikace ─── ❼ B2B kontrakt
                    ┆
   STŘEDNÍ          ┆  ❽ PLC basics
                    ┆
                    └──────────────────────────────────────────►
                    IMMEDIATE         SHORT          MEDIUM
                         0-3 týdny    3-6 týdnů    6-16 týdnů
```

---

## FÁZE 1: IMMEDIATE — 0-3 týdny (CRITICAL priority)

---

### ❶ LinkedIn Profile Optimization

| Metrika | Hodnota |
|---------|---------|
| **EROI** | 🟢 VELMI VYSOKÝ (9/10) |
| **Časová investice** | 8-12 hodin |
| **Expected impact** | Nárůst precision o 40-70 % |
| **Success metric** | Precision > 32 % do 14 dnů |
| **Aktuální precision** | 20.8 % (5/24) |

#### Metodická kostra — Linkedin optimalizace

```
KROK 1: HEADLINE (30 min)
═══════════════════════════════════════════════════
  Vzorec:  [CORE ROLE] | [SPECIALIZACE] • [TECH1] • [TECH2] • [USP]

  Současný:  "Industrial Automation & Knowledge Systems | CNC/CAM | Python"
  Nový:      "Industrial Automation Engineer | System Integration • CNC/CAM •
              Python • Reverse Engineering"

  Pravidla:
    - Max 220 znaků
    - 3-5 klíčových slov oddělených • nebo |
    - CORE ROLE = job title který chcete (Industrial Automation Engineer)
    - USP = Reverse Engineering (největší diferenciace)


KROK 2: ABOUT SEKCE (2-3 h)
═══════════════════════════════════════════════════
  Struktura (250-400 slov):
    ┌─ Odstavec 1: Positioning (2-3 věty)
    │   "Specializuji se na převod..." → zachovat stávající
    │
    ├─ Odstavec 2: Technická vrstva (strojově čitelná)
    │   Technická realizace: Python, GCP Cloud Run, Docker,
    │   reverzní inženýrství binárních formátů, golden master
    │   regression testing, CNC/CAM (VCutWorks, LightBurn),
    │   IoT (ESP32), ETL pipeline, RAG systémy.
    │
    ├─ Odstavec 3: Key achievement (1-2 věty)
    │   "V roce 2026 jsem reverzně analyzoval nedokumentovaný
    │   binární formát .VCF a vytvořil deterministický parser
    │   s přesností >99,98 % nasazený na GCP."
    │
    └─ Odstavec 4: Call to action
        "Hledám B2B spolupráci v průmyslové automatizaci,
        CAM/CNC nebo system integration."


KROK 3: SKILLS SEKCE (2 h)
═══════════════════════════════════════════════════
  Současný stav: 5 skills → CÍL: 18-25 skills

  Povinně přidat (řazeno dle priority):
    1. Reverse Engineering           ← USP
    2. Test Automation               ← core competence
    3. Golden Master Testing         ← unikátní
    4. Docker                        ← doloženo GitHubem
    5. IoT (Internet of Things)      ← ESP32 projekty
    6. Data Pipeline / ETL           ← meteo miner, scraping
    7. CAM Software                  ← VCutWorks, LightBurn
    8. System Integration            ← core role
    9. GCP Cloud Run                 ← doloženo
    10. Streamlit                    ← doloženo
    11. GitHub Actions               ← plánováno
    12. CNC Programming              ← již máte
    13. Integration Engineering      ← již máte
    14. Embedded Systems             ← ESP32
    15. Regression Testing           ← metodika
    16. PLC Testing                  ← adjacent skill
    17. REST APIs                    ← ERP integrace
    18. Cloud Computing              ← již máte

  Technika: LinkedIn akceptuje max 50 skills.
    - Vybrat 18-25 s nejvyšším SNR
    - Skills potvrdit GitHubem (kredibilita)
    - 3 skills "endorse" od kolegů/kontaktů


KROK 4: FEATURED SEKCE (30 min)
═══════════════════════════════════════════════════
  Přiřadit do Featured:
    1. GitHub profil (github.com/outpost2026)
    2. VCF parser demo (odkaz na Cloud Run)
    3. LinkedIn článek o RE metodologii (až bude)

KROK 5: OPEN TO WORK (15 min)
═══════════════════════════════════════════════════
  Zapnout s filtry:
    - Pracovní pozice: "Industrial Automation Engineer",
      "System Integration Engineer", "Test Engineer"
    - Lokality: Praha, Brno, Remote
    - Typ: B2B, HPP
    - Vypnout: IT consulting, SaaS, enterprise software


KROK 6: VERIFIKACE (30 min)
═══════════════════════════════════════════════════
  Checklist:
    □ Headline obsahuje "Industrial Automation" + "System Integration"
    □ About má technickou vrstvu (strojově čitelnou)
    □ Skills: min 18, max 25
    □ GitHub propojený do Featured
    □ Omezené job search preference
    □ Profil je v English (CZ trh + international)

  Nástroj: linkedin.com/premium/stats — sledovat
    - Profile views (baseline)
    - Search appearances
    - Precision po 14 dnech
```

---

### ❷ Aplikace na Top Follow Leads

| Metrika | Hodnota |
|---------|---------|
| **EROI** | 🟢 VELMI VYSOKÝ (9/10) |
| **Časová investice** | 6-8 hodin (3 aplikace × 2-3 h) |
| **Expected impact** | 1-2 pohovory z 3 aplikací |
| **Target** | Desoutter #003 (72 %), Siemens #007 (78 %), Thermo Fisher #014 (65 %) |

#### Metodická kostra — Aplikační proces

```
OBECNÝ RÁMEC APLIKACE (2-3 h na jednu)
═══════════════════════════════════════════════════

KROK 1: RESEARCH (30 min)
  - Přečíst full job description (3×)
  - Identifikovat 3 klíčové požadavky
  - Najít 1-2 LinkedIn kontakty ve firmě (HR, team lead)
  - Zjistit technologický stack firmy

KROK 2: CV CUSTOM (1 h)
  Template: Full-CV_EN nebo 01_one-pager
  Úprava:
    - Přeskládat bullet points dle priority JD
    - Přidat relevantní keywords z JD
    - Zdůraznit: RE case study (99.98 %) + test metodologie
    - Potlačit: off-grid, ESP32 (není relevantní)

KROK 3: COVER NOTE (30 min)
  Struktura:
    1. Úvod: "Aplikuji na [role], protože..."
    2. Tělo: 2-3 věty propojující autorovu zkušenost s JD
    3. USP: RE case study / test methodology / manufacturing domain
    4. Závěr: otevřenost pohovoru

KROK 4: LINKEDIN ZPRÁVA hiring managerovi (15 min)
  - Krátká, personalizovaná
  - Odkaz na GitHub nebo VCF parser demo
  - Žádost o 15 min call

KROK 5: FOLLOW-UP PLÁN
  Den 0:  Odeslat aplikaci
  Den 3:  LinkedIn zpráva
  Den 7:  Follow-up email (pokud není odpověď)
  Den 14: Phone call / druhá zpráva → pokud stále nic → move on


SPECIFICKÉ PROFILE PRO JEDNOTLIVÉ FIRMY
═══════════════════════════════════════════════════

DESOUTTER #003 — Light Automation Specialist (72 % fit)
  Argumentační linie:
    - 14 let v CNC/výrobě = rozumím strojům a provozu
    - VCF parser = system integration case study
    - CNC background → PLC je koncepčně blízké
    - "You don't need to tick every box" → otevřeni netradičním profilům
  Gap mitigation:
    - Nastudovat EtherCAT/PROFINET základy (2-4 h před pohovorem)

SIEMENS #007 — Test Engineer Distributed IO (78 % fit)
  Argumentační linie:
    - Golden master regression framework (10/10 PASS)
    - RE case study: 99.98 % přesnost = test engineering
    - Python + CI/CD + AI workflows
    - Manufacturing domain knowledge (ET 200 kontext)
  Gap mitigation:
    - Nastudovat TIA Portal základy (2-4 h)
    - Degree argument: "14 years comparable technical experience"

THERMO FISHER #014 — System Integration Engineer (65 % fit)
  Argumentační linie:
    - "Own system integration" = VCF parser od RE po deployment
    - Structured troubleshooting = pair-diff, golden master
    - IoT/ESP32 + GCP cloud + data pipeline
  Gap mitigation:
    - K8s základy před pohovorem (1-2 dny)
```

---

### ❸ TypeScript + Playwright Quickstart

| Metrika | Hodnota |
|---------|---------|
| **EROI** | 🟢 VYSOKÝ (8/10) |
| **Časová investice** | 15-25 hodin |
| **Expected impact** | Odemčení Rockwell-like rolí (2× výskyt) |
| **Success metric** | Funkční PoC do 3 týdnů |
| **Aktuální stav** | JavaScript není v CV/ GitHub, TS/Playwright gap potvrzen |

#### Metodická kostra — TypeScript + Playwright

```
KROK 1: ZÁKLADY TYPESCRIPT (5-8 h)
═══════════════════════════════════════════════════
  Učební osnova:
    - Typový systém (interfaces, types, generics)
    - Async/await, Promises
    - Node.js runtime základy
    - npm/yarn package management
    - tsconfig.json konfigurace

  Zdroje:
    - Udemy: "Understanding TypeScript" (Maximilian Schwarzmüller)
    - https://www.typescriptlang.org/docs/handbook/
    - Cvičení: přepsat jeden Python script do TS

  Klíčový insight pro autora:
    TS ≠ nový jazyk. TS = JS + types.
    Autor umí Python OOP → TS interfaces, generics, type narrowing
    jsou koncepčně identické. Focus na syntaxi, ne na principy.


KROK 2: PLAYWRIGHT ZÁKLADY (5-8 h)
═══════════════════════════════════════════════════
  Učební osnova:
    - Instalace a konfigurace (playwright.config.ts)
    - Page Object Model (struktura testů)
    - Locators: getByRole, getByText, getByTestId
    - Assertions: toBeVisible, toHaveText, toHaveValue
    - Fixtures a test hooks (beforeEach, afterEach)
    - Tracing a debugging (Playwright Inspector)
    - CI integrace (GitHub Actions)

  Zdroje:
    - Playwright docs: https://playwright.dev/docs/intro
    - Udemy: "Playwright: Test Automation" (Rahul Shetty)

  Autorova výhoda:
    - Už zná test automation koncepty (golden master, regression)
    - Už zná Python pytest fixtures → Playwright fixtures jsou analogické
    - Už zná deterministické testování → Playwright assertions jsou triviální


KROK 3: PRAKTICKÝ PROJEKT — PoC (5-10 h)
═══════════════════════════════════════════════════
  Varianta A: Scraper
    - Cíl: TypeScript scraper pro CNC/CAM fórum nebo průmyslový web
    - Techniky: Playwright page.goto, locators, data extraction
    - Output: JSON s extrahovanými daty

  Varianta B: Test suite pro existující API
    - Cíl: Otestovat REST API (např. vlastní VCF parser API)
    - Techniky: Playwright APIRequestContext, assertions
    - Output: 5-10 passing test cases

  Varianta C: Golden master test v TS
    - Cíl: Převést jeden golden master test z Pythonu do TS
    - Output: Reprodukovatelný baseline test v novém stacku

  Doporučení: Varianta B (API testování) — nejvyšší crossover
    s autorovým stackem a nejlépe demonstruje schopnost.


KROK 4: VERIFIKACE (1 h)
═══════════════════════════════════════════════════
  □ TypeScript PoC v public GitHub repu
  □ Playwright testy procházejí (green pipeline)
  □ README s dokumentací
  □ Zmínka v LinkedIn About a Skills
```

---

## FÁZE 2: SHORT_TERM — 3-6 týdnů (HIGH priority)

---

### ❹ AZ-900 Azure Fundamentals

| Metrika | Hodnota |
|---------|---------|
| **EROI** | 🟢 VYSOKÝ (7.5/10) |
| **Časová investice** | 10-15 hodin |
| **Expected impact** | Zvýšení fit u Azure rolí (4× výskyt) |
| **Success metric** | Certifikát + zmínka v profilu |
| **Cena zkoušky** | ~2 500 Kč (online proctor) |

#### Metodická kostra — AZ-900

```
KROK 1: UČEBNÍ OSNOVA (10-12 h)
═══════════════════════════════════════════════════
  Modul 1: Cloud Concepts (20-25 % zkoušky) — 2-3 h
    - Cloud computing, CAPEX vs OPEX
    - IaaS, PaaS, SaaS modely
    - High Availability, Scalability, Elasticity, Agility
    - Disaster Recovery, RPO/RTO
    → Autor už zná z GCP — jen přejmenovat terminologii

  Modul 2: Azure Architecture & Services (35-40 %) — 4-5 h
    - Azure Regions, Availability Zones, Resource Groups
    - Compute: VMs, Azure App Service, AKS, Container Instances
    - Storage: Blob, Disk, File, Queue, Table
    - Networking: VNet, Load Balancer, VPN Gateway
    - Databases: Cosmos DB, SQL Database, Azure DB for...
    → Srovnávat s GCP: Cloud Run → ACI, Firestore → Cosmos DB, atd.

  Modul 3: Azure Management & Governance (30-35 %) — 3-4 h
    - Azure AD, RBAC, Policy, Blueprints
    - Subscriptions, Management Groups, Cost Management
    - Azure Monitor, Service Health, Advisor
    - Compliance: GDPR, ISO, NIST
    → Autor má GCP IAM zkušenost → analogie

  Modul 4: Cvičné testy (2-3 h)
    - Microsoft Learn: AZ-900 practice test
    - TutorialsDojo: AZ-900 practice exams
    - Whizlabs: AZ-900 simulations


KROK 2: ZKOUŠKA (1 h)
═══════════════════════════════════════════════════
  - Online proctored (z domova)
  - 45 minut, 30-40 otázek
  - Score: 700/1000 = pass
  - Platnost: 1 rok (renewal zdarma)

KROK 3: PROFILOVÁ AKCE (30 min)
═══════════════════════════════════════════════════
  - Přidat certifikaci do LinkedIn Licenses & Certifications
  - Zmínit v About sekci: "Azure fundamentals certified"
  - Přidat Azure do Skills
```

---

### ❺ GitHub Actions + Docker Multi-stage — ✅ HOTOVO

| Metrika | Hodnota |
|---------|---------|
| **EROI** | 🟢 VYSOKÝ (7/10) |
| **Časová investice** | 0 hodin (hotovo) |
| **Expected impact** | Profesionalizace repozitářů |
| **Success metric** | Green pipeline na main — DOKONČENO |
| **Aktuální stav** | ✅ CI/CD deklarován v README: "Actions, CodeQL, Dependabot" (2026-08) |

#### Metodická kostra — CI/CD & Docker

```
KROK 1: DOCKER MULTI-STAGE BUILD (4-6 h)
═══════════════════════════════════════════════════
  Vzorec Dockerfile:
    # Stage 1: Build
    FROM python:3.11-slim AS builder
    COPY requirements.txt .
    RUN pip install --user -r requirements.txt

    # Stage 2: Runtime
    FROM python:3.11-slim
    COPY --from=builder /root/.local /root/.local
    COPY . .
    CMD ["python", "main.py"]

  Aplikovat na:
    - VCF parser (Streamlit)
    - cad2llm
    - RAG-indexer

KROK 2: GITHUB ACTIONS CI/CD (6-8 h)
═══════════════════════════════════════════════════
  Workflow struktura (.github/workflows/ci.yml):
    name: CI/CD
    on: [push, pull_request]
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
          - run: pip install -r requirements.txt
          - run: pytest tests/
          - run: python -m goldmaster run

      deploy:
        needs: test
        if: github.ref == 'refs/heads/main'
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: google-github-actions/auth@v2
          - uses: google-github-actions/deploy-cloudrun@v2

  Success metric:
    - Zelená pipeline na každém pushi
    - Testy běží automaticky
    - Deploy na Cloud Run po merge do main

KROK 3: PŘIDAT README BADGES (1 h)
═══════════════════════════════════════════════════
  [![CI/CD](https://github.com/outpost2026/REPO/actions/workflows/ci.yml/badge.svg)]
  [![Python 3.11](https://img.shields.io/badge/python-3.11-blue)]
  [![License](https://img.shields.io/badge/license-MIT-green)]
```

### ❻ MCP Ekosystém — Diferenciace (NOVÁ)

| Metrika | Hodnota |
|---------|---------|
| **EROI** | 🔥 VELMI VYSOKÝ (9/10) |
| **Časová investice** | 0 hodin (hotovo — 3 servery) |
| **Expected impact** | Unikátní diferenciace na B2B trhu |
| **Success metric** | 3 veřejné MCP servery na GitHubu — DOKONČENO |
| **Aktuální stav** | ✅ linkedin-mcp-custom (403 commits), MCP-Jobs (CZ portály), lichess-mcp-analyzer |

#### Metodická kostra — MCP jako diferenciace

```
STAV: 3 veřejné MCP servery hotové
══════════════════════════════════════════════════

1. linkedin-mcp-custom (638 KB, 403 commits)
   - LinkedIn saved jobs scraping + EROI scoring
   - 8 nástrojů, FastMCP framework
   - Featured project na GitHub profilu

2. MCP-Jobs (408 KB)
   - MCP pro CZ job portály: jobs.cz, prace.cz, bazos.cz
   - 5 nástrojů
   - Převod B2B job search workflow do opakovatelného nástroje

3. lichess-mcp-analyzer (969 KB)
   - Chess analytics: Stockfish, coaching reports
   - 8 nástrojů
   - Demonstrace transferability MCP patternu na odlišnou doménu

AKCE:
  - Zvážit publikaci jako open-source reference
  - Přidat do LinkedIn Skills: "MCP Server Development"
  - Přidat do LinkedIn About: zmínka o MCP toolingu
  - Zvážit B2B positioning: "MCP tooling pro industrial automation"
```

---

## FÁZE 3: MEDIUM_TERM — 6-16 týdnů (MEDIUM priority)

---

### ❼ RE Metodika — Publikace & Anonymizace

| Metrika | Hodnota |
|---------|---------|
| **EROI** | 🟡 STŘEDNÍ-VYSOKÝ (6.5/10) |
| **Časová investice** | 15-25 hodin |
| **Expected impact** | ↑ viditelnost portfolia, 50+ stars potenciál |
| **Success metric** | Nové public repo + LinkedIn článek |

#### Metodická kostra — RE publikace

```
KROK 1: ANONYMIZACE (8-10 h)
═══════════════════════════════════════════════════
  Co anonymizovat:
    - Názvy klientů → "Client A", "Client B"
    - Interní cesty, IP adresy, MAC adresy
    - Konkrétní zakázková data (rozměry, materiály)
    - .VCF soubory → generovat syntetické test sample

  Co ponechat:
    - Binární struktura (offset, typ, size, description)
    - IEEE 754 formát, hex vzory
    - Pair-diff diagnostická metodika
    - Golden master testy (s anonymizovanými baselines)

KROK 2: STRUKTURA REPO (4-6 h)
═══════════════════════════════════════════════════
  /vcf-parser-re
  ├── README.md
  ├── METHODOLOGY.md      ← hlavní dokument
  ├── docs/
  │   ├── binary-structure.md
  │   ├── pair-diff.md
  │   └── golden-master.md
  ├── src/
  │   └── parser.py
  └── tests/
      ├── golden_master/
      └── test_determinism.py

  README musí obsahovat:
    - Problem statement
    - Methodology overview
    - Results (99.98 % accuracy)
    - Business value
    - Odkazy na LinkedIn článek a live demo

KROK 3: LINKEDIN ČLÁNEK (3-5 h)
═══════════════════════════════════════════════════
  Titulek: "Jak jsem reverzně analyzoval binární formát bez dokumentace
            — případová studie systematického reverse engineeringu"

  Struktura:
    1. Problém: Klient závislý na proprietárním formátu a tacitním know-how
    2. Metodologie: Pair-diff, hex analýza, IEEE 754 reverse engineering
    3. Proces: 22 iterací, 29 dní, cross-validace
    4. Výsledek: 99.98 % přesnost, GCP Cloud Run, ERP integrace
    5. Business value: Nezávislost na jednotlivci, přenositelnost
    6. Call to action: Hledám podobné výzvy

KROK 4: DISTRIBUCE (1 h)
═══════════════════════════════════════════════════
  - Sdílet v LinkedIn relevantních groups (Reverse Engineering,
    Industrial Automation, Python)
  - Poslat 5-10 relevantním kontaktům s žádostí o feedback
  - Přidat do GitHub Featured repozitářů
```

---

### ❽ První B2B Kontrakt (diverzifikace)

| Metrika | Hodnota |
|---------|---------|
| **EROI** | 🟡 STŘEDNÍ-VYSOKÝ (6/10) |
| **Časová investice** | Variabilní (průběžně) |
| **Expected impact** | Cashflow + reference |
| **Target** | Toloka #024 nebo podobný freelance B2B projekt |

#### Metodická kostra — B2B kontrakt

```
KROK 1: IDENTIFIKACE (průběžně)
═══════════════════════════════════════════════════
  Filtry pro B2B projekty:
    - Remote / hybrid
    - Python + integrace + REST API
    - B2B / OSVČ model
    - Délka: 3-12 měsíců
    - Sazba: 600-1200 Kč/hod (B2B)

  Kanály:
    - LinkedIn (Open to Work + projektové nabídky)
    - Toloka / Upwork / Fiverr (pro start)
    - Osobní network (SYSTEQ kontakty)

KROK 2: NABÍDKA (2-4 h)
═══════════════════════════════════════════════════
  Pro Toloka #024 nebo podobný:
    - CV: One-pager EN s důrazem na integrační projekty
    - Portfolio: VCF parser (system integration), cad2llm, RAG-indexer
    - Rate: 800 Kč/hod (B2B)
    - Dostupnost: 15-20 h/týden

KROK 3: CONTRACTING (průběžně)
═══════════════════════════════════════════════════
  - Smlouva: SCOPE + MILESTONES + PAYMENT TERMS
  - Scope: Jasně definovaný deliverable (ne "time & material")
  - Milestones: 3-4 fáze s payoutem
  - Payment: Net 30 nebo Net 15 (ne Net 60+)
```

---

### ❾ PLC Basics & Industrial Protocols

| Metrika | Hodnota |
|---------|---------|
| **EROI** | 🟡 STŘEDNÍ (5.5/10) |
| **Časová investice** | 40-60 hodin |
| **Expected impact** | ↑ fit u Siemens/Rockwell |
| **Success metric** | Funkční PoC + README |
| **Aktuální stav** | PLC není doloženo GitHubem, chybí digitální stopa |

#### Metodická kostra — PLC basics

```
KROK 1: TEORETICKÝ ZÁKLAD (10-15 h)
═══════════════════════════════════════════════════
  Učební osnova:
    - Co je PLC: architektura, scan cycle, I/O mapping
    - Ladder logic vs Structured Text (ST) vs Function Block (FBD)
    - Siemens TIA Portal: projekt, HW konfigurace, tagy
    - Modbus TCP: read/write holding registers, coil access
    - PROFINET: device classes, topology, IO cycle

  Zdroje:
    - Siemens TIA Portal tutorials (YouTube: "TIA Portal for Beginners")
    - PLC Fiddle (online PLC simulator — zdarma)
    - "PLC Programming from Scratch" (Udemy)

  Autorova výhoda:
    - CNC/G-code background = koncepčně blízké
    - Rozumí průmyslovému prostředí, sensorům, aktuátorům
    - Už zná industrial protokoly koncepčně

KROK 2: PRAXE — SIMULÁTOR (10-15 h)
═══════════════════════════════════════════════════
  Nástroje:
    - PLC Fiddle (free, browser-based)
    - OpenPLC (open source PLC runtime)
    - Siemens S7-PLCSIM (s TIA Portal trial)

  Úkoly:
    1. Basic ladder: start-stop motor, timer, counter
    2. Structured Text: IF-THEN-ELSE, CASE, FOR loops
    3. Function Block: vytvořit vlastní FB (např. conveyor control)
    4. HMI: jednoduchý vizuální panel (start, stop, status)

KROK 3: PROTOTYP — Modbus PoC (10-15 h)
═══════════════════════════════════════════════════
  Cíl: Python ↔ PLC komunikace přes Modbus TCP

  Stack:
    - Python: pymodbus library
    - Simulátor: ModbusPal nebo OpenPLC jako slave
    - Docker: containerizovat

  Úkoly:
    1. Python client: read holding registers
    2. Python client: write coil
    3. Logging a monitoring (časové razítko, hodnoty)
    4. README s dokumentací

  Výstupní artefakt:
    - GitHub repo: plc-modbus-poc
    - 3+ test cases (read, write, error handling)
    - Dockerfile + docker-compose.yml

KROK 4: DOKUMENTACE A PORTFOLIO (5-10 h)
═══════════════════════════════════════════════════
  Co zdokumentovat:
    - Architektura: Python ↔ Modbus TCP ↔ PLC simulator
    - Výsledky: úspěšně načtené/zapsané registry
    - Poučení: rozdíly oproti CNC/CAM workflow
    - Next steps: reálný PLC (Siemens S7-1200)

  Kde publikovat:
    - GitHub (public repo)
    - LinkedIn (post o PLC + Python integraci)
    - Zmínit v profilu: "PLC basics + Modbus TCP"
```

---

## Master Timeline — Všechny fáze

```
Aktivita                      │ W1 │ W2 │ W3 │ W4 │ W5 │ W6 │ W7-10 │ W11-14 │ W15-16
──────────────────────────────┼────┼────┼────┼────┼────┼────┼───────┼────────┼───────
                               IMMEDIATE                      SHORT       MEDIUM
                               ─────────                      ─────       ──────
❶ LinkedIn opt. (8-12 h)      │ ██ │    │    │    │    │    │       │        │
❷ Aplikace (6-8 h)            │ ██ │ ░░ │ ░░ │    │    │    │       │        │
❸ TypeScript (15-25 h)        │ █░ │ ██ │ ██ │    │    │    │       │        │
                               │    │    │    │    │    │    │       │        │
❹ AZ-900 (10-15 h)            │    │    │    │ ░░ │ ██ │ ██ │       │        │
❺ GitHub Actions (12-18 h)    │    │    │    │ ██ │ █░ │    │       │        │
                               │    │    │    │    │    │    │       │        │
❻ RE publikace (15-25 h)      │    │    │    │    │    │    │ ████  │        │
❼ B2B kontrakt (variabilní)  │    │    │    │    │    │    │       │        │ ██
❽ PLC basics (40-60 h)        │    │    │    │    │    │    │       │ ████   │
                               │    │    │    │    │    │    │       │        │
LinkedIn review (každé 2t)    │    │ ░░ │    │ ░░ │    │ ░░ │ ░░    │ ░░     │ ░░
──────────────────────────────┼────┼────┼────┼────┼────┼────┼───────┼────────┼───────
Celkem hodin/týden            │ 21 │ 15 │ 12 │ 12 │ 13 │ 10 │ 8-12  │ 8-12   │ 5-10
```

---

## Monitoring Framework

| Metric | Frekvence | Cíl | Trigger |
|--------|-----------|-----|---------|
| LinkedIn Precision | 2 týdny | 35-45 % | < 30 % → review |
| Počet kvalitních aplikací | 2 týdny | 8-12/měsíc | < 4 → increase |
| Response rate | 2 týdny | 40-55 % | < 25 % → review CV |
| Fit skóre top 5 leadů | 2 týdny | > 50 % avg | < 40 % → reposition |
| GitHub commity | 2 týdny | 10+/týden | < 5 → increase |
| TypeScript PoC status | 1 týden | Hotovo do W3 | Zpoždění → escalate |
| AZ-900 certifikace | 1 týden | Hotovo do W6 | Zpoždění → replan |

### Review trigger (< 30 % precision nebo 0 odpovědí za 3 týdny)

```
1. Zkontrolovat LinkedIn preferences (nejsou moc široké?)
2. Zkontrolovat headline (obsahuje správné keywords?)
3. Zkontrolovat skills (je jich 18+?)
4. Zkontrolovat About (je technická vrstva?)
5. Aktivně aplikovat na 5+ nových leadů
6. Pokud stále 0 → změnit headline na "Open to Work" explicitně
```

---

## Risk & Mitigation Matrix

| Riziko | Pravděpodobnost | Dopad | Mitigace |
|--------|-----------------|-------|----------|
| Příliš pomalé tempo po initial burstu | Vysoká | Střední | Pevný týdenní time-box 12-15 h na korekce |
| Over-documentation vs. exekuce | Střední | Vysoká | 80/20 pravidlo — max 30 % času na docs |
| LinkedIn algoritmus drift | Střední | Střední | Pravidelná kalibrace preferences + aktivní aplikace |
| TypeScript učení trvá déle | Střední | Vysoká | Deadline W3, denní progress logging |
| Degree filtr u Siemens/Google | Vysoká | Vysoká | "Equivalent experience" argumentace, reference |
| Zero response na follow leads | Střední | Vysoká | Review CV + cover letter quality, zkusit jiné kanály |

---

## Kontrolní list — Týdenní review

```
Každé pondělí:
  □ Precision check (LinkedIn)
  □ Počet nových nabídek
  □ Počet odpovědí na aplikace
  □ Progress na TypeScript (h / celkem)
  □ GitHub commity za týden
  □ Time-box check (12-15 h?)

Týden 1:
  □ Headline změněn
  □ Skills přidány (18-25)
  □ GitHub propojen s Featured
  □ Open to Work nastaven
  □ Desoutter aplikováno
  □ Siemens aplikováno
  □ Thermo Fisher aplikováno
  □ TypeScript kurz started

Týden 2:
  □ TypeScript progress 50 %
  □ Precision check (>32 %?)
  □ Follow-up na aplikace (den 7)

Týden 3:
  □ TypeScript PoC hotovo
  □ Rockwell aplikováno (po TS kurzu)
  □ Precision review #2

Týden 4-5:
  □ GitHub Actions pipeline
  □ Docker multi-stage
  □ AZ-900 kurz started

Týden 6:
  □ AZ-900 certifikace
  □ Precision review #3 (>35 %?)
```

---

## EROI Revidovaný Skill Acquisition ROI (aktualizováno 2026-08-06)

| Investice | Náklady | Přínos | EROI | Status |
|-----------|---------|--------|------|--------|
| **LinkedIn optimalizace** | 8-12 h | ↑ Precision 40-70 %, odemkne follow lead konverzi | 🔥 **9/10** | PLÁN |
| **MCP ekosystém** | 0 h (hotovo) | Diferenciace, emerging trend, 3 servery | 🔥 **9/10** | ✅ HOTOTO |
| **Aplikace follow leads** | 6-8 h | 1-2 pohovory z top 3 leadů (76-82 % fit) | 🔥 **9/10** | PLÁN |
| **TypeScript + Playwright** | 15-25 h | Odstraní mismatch u Rockwell + Sky | 🟢 **8/10** | PLÁN |
| **AZ-900 Azure** | 10-15 h | Zvýší fit u 4× výskytu Azure | 🟢 **7.5/10** | PLÁN |
| **GitHub Actions + Docker** | 0 h (hotovo) | Profesionalizace repozitářů | 🟢 **7/10** | ✅ HOTOTO |
| **RE publikace** | 15-25 h | Důkaz expertizy, 50+ stars potenciál | 🟡 **6.5/10** | PLÁN |
| **B2B kontrakt** | variabilní | Cashflow + reference | 🟡 **6/10** | PLÁN |
| **PLC basics** | 40-60 h | Posílení core industrial match | 🟡 **5.5/10** | PLÁN |

---

*Report generován: 2026-08-06*
*Verze: 2.0 (aktualizace v1.0 z 2026-06-25)*
*Metodika: EROI ranking + chronologický Gantt + metodické kostry pro každou optimalizaci*
*Navazuje na: Korekce_vektoru_rozvoje_OS.json v2.0, portfolio_audit_v2.md, Live GitHub API audit*
*Provenance: Live GitHub API (2026-08-06), ověřeno proti skutečnému stavu repozitářů*
