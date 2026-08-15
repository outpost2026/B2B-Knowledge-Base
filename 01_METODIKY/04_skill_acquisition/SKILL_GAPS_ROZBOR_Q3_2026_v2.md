# SKILL GAPS: Rozbor identifikovaných mezer v autorově stacku pro Q3+ 2026 — v2 (aktualizováno o standalone/DevOps dimenzi)

**Datum:** 2026-08-15 | **Autor:** outpost2026
**Účel:** Strukturovaný rozbor skill gapů — co je, proč se to poptává, kde se to používá, glossary, ontologie, praktické příklady
**Verze:** 2.0 | **Nahrazuje:** SKILL_GAPS_ROZBOR_Q3_2026_v1 (2026-08-06)
**Kontext:** v1 rozebrala 4 gapy (TS+Playwright, AZ-900, PLC, K8s). Nový input — imerzní analýza `outprep` (Next.js monorepo standalone web app) pro aspirační port MCP serveru na standalone produkt → v2 **přidává 2 nové gapy (DB, DevOps/Deployment)** a **rozšiřuje stávající** (TS→Next.js+monorepo, K8s→kontext lehčí PaaS vrstvy)
**Zdroje:** Edukační dokument `docs/edukace_port_standalone_2026-08-15.md` (MCP-Jobs), live GitHub audit `outprep` (2026-08-15), SKILL_GAPS_ROZBOR_Q3_2026_v1, SWE_GLOSSARY_zive_v1
**Provenance:** Summary (zdroj: technologický průzkum outprep + edukační analýza) + source-read (schema.sql, docker-compose.yml, package.json, .env.example, vercel.json)

---

## Executive Summary

Z 24 analyzovaných LinkedIn nabídek (v1) + nové imerzní analýzy `outprep` (2026-08-15) se identifikovalo **6 mezer** v autorově stacku (4 původní + 2 nové z DevOps/standalone dimenze).

| # | Gap | EROI | Čas | Blokuje / umožňuje |
|:-:|-----|:----:|:---:|---------|
| ❶ | TypeScript + Next.js + monorepo | 9/10 | 25–35 h | Standalone produkt, GUI na systeq.cz, E2E testy |
| ❷ | PostgreSQL + schema + migrace | 8.5/10 | 15–20 h | Produkční perzistence, dedup, historie, dotazování |
| ❸ | DevOps: Docker, cron, monitoring | 8/10 | 15–20 h | Automatizace ELT bez IDE, healthchecks.io, CI/CD |
| ❹ | AZ-900 Azure Fundamentals | 7.5/10 | 10–15 h | Azure role (4×) |
| ❺ | PLC Basics & Industrial Protocols | 5.5/10 | 40–60 h | Siemens, Rockwell (3×) |
| ❻ | Kubernetes | 3.5/10 | 40+ h | Enterprise role (3×) — **sníženo**: overkill pro single-user |

**Klíčová změna oproti v1:** aspirace **port MCP serveru na standalone produkt** (dokázáno reálným `outprep` repem) vytáhla na povrch **databázovou a DevOps vrstvu**, které v v1 chyběly. Autorovi nechybí jen "nástroje pro role" — chybí mu **produkční architektura** (DB, deployment, automatizace). To je nová dimenze gapů, oddělená od tržních požadavků.

**Autorův kontext:** systémový integrátor (CNC/CAM), expertní Python, 3 MCP servery, GCP zkušenost. Praxe v SWE < 5 měsíců — učení imerzní metodou (řešení vlastního problému → objev nové domény).

---

## Sémantická analýza — nový input vs v1

Tato sekce je nová oproti v1. Mapuje, co přinesla imerzní analýza `outprep` (viz edukační dokument) do rozboru gapů.

| Nový pojem z edukace/outprep | Sémantická vazba na stack | Gap | Verdikt |
|-------------------------------|--------------------------|:---:|:-------:|
| **Standalone produkt** = samostatná app s UI, DB, cronem, monitoringem | Autorův stack je MCP server (knihovna/STDIO) → chybí celá produkční vrstva | nový | Motivace pro celé v2 |
| **Deliverable** = forma, ve které produkt běží | Autor dosud posuzoval "co pipeline dělá", ne "jak/kde běží" | nový | Paradigm shift |
| **Monorepo + npm workspaces** (`packages/*`) | Autor zná multi-repo (každý MCP zvlášť). Workspaces = sdílený node_modules | ❶ | Rozšířit TS |
| **Next.js App Router + API routes** (`src/app/api/`) | Autor nezná web backend. Route = HTTP endpoint | ❶ | Rozšířit TS |
| **PostgreSQL schema, JSONB, indexy, UNIQUE** | Autor má jen `output/*.json,.md`. Soubory ≠ databáze | **❷ nový** | Nový gap |
| **pipeline_runs tabulka** (audit ETL) | Autor má correlation_cache. DB = plný audit | ❷ | Příklad |
| **Provider-agnostic DB** (postgres pkg, DATABASE_URL) | Autor zná konfig. Provider lock-in = nový koncept | ❷ | Příklad |
| **Cron / Vercel Cron / scheduler** (`vercel.json`) | Autor spouští ETL ručně z IDE. Produkční ELT běží sám | **❸ nový** | Nový gap |
| **healthchecks.io** (dead-man's-switch) | Monitoring = vědět o selhání dřív než uživatel | ❸ | Nový gap |
| **Docker / docker-compose** (`postgres:16`, `5432:5432`) | Autor zná Docker→Cloud Run. Compose multi-service = nové | ❸/❻ | Rozšířit |
| **CI/CD (GitHub Actions, husky, lint-staged)** | Autor nemá CI. Build+test na push = chytí regrese | ❸ | Nový gap |
| **Porty** (80/443/5432/3000) | Základ síťové ontologie, autor neznal | ❸ | Edukace |
| **Environment variables (.env)** | Autor už zná (AGENTS.md security) | — | Potvrzeno |
| **K8s = "Cloud Run na steroidech"** | Autor zná Cloud Run (serverless). K8s = kontrola navíc | ❻ | **Sníženo** |

### Závěr sémantické analýzy

1. **Aspirace portu** posunula rozbor od "co poptávají role" k "co potřebuje produkční software". Dva nové gapy (DB, DevOps) jsou **architektonické**, ne tržní — ale bez nich standalone produkt nevznikne.
2. **TypeScript gap se rozšířil**: už to není jen jazyk pro testy — je to **jazyk celého standalone frontendu** (Next.js, React, API routes, monorepo). EROI vzrostlo (9/10).
3. **K8s priorita klesla** (3.5/10): edukační analýza jasně ukázala, že pro single-user job-hunt je orchestrátor **overkill**. `outprep` zpracovává miliony her *bez* orchestrátoru — jen CLI + cron. K8s zůstává volitelný enterprise výstup.

---

## ❶ TypeScript + Next.js + monorepo

### 1.1 Co je TypeScript (v2 rozšíření)

(v1: TS = JS + typy, analogie Python OOP. Ontologie TS — interfaces, generics, narrowing, async/await, module system, tooling — **beze změny, viz v1**.)

### 1.2 Co je Next.js (NOVÉ)

Next.js je **React framework** od Vercelu. React = knihovna pro UI komponenty, Next.js = framework, který přidává:
- **App Router** — souborové routování (`src/app/` → stránky + API routes)
- **API routes** (`src/app/api/.../route.ts`) — backend ve stejném projektu (HTTP endpointy)
- **Server Components / Client Components** — kód běžící na serveru vs prohlížeči
- **Serverless deployment** — běží na Vercelu bez správy serveru
- **File-based routing** — složka = URL cesta

**Analogie pro autora:** Next.js = "Streamlit pro produkční web, ale s plným backendem a TS". Autor zná Streamlit (dashboard = stránky). Next.js je stejný koncept s mnohem větším ekosystémem.

#### Ontologie Next.js (NOVÁ)

```
Next.js (React framework)
├── App Router
│   ├── src/app/                  # souborová struktura
│   │   ├── page.tsx              # stránka (URL: /)
│   │   ├── layout.tsx            # sdílený layout
│   │   └── api/                  # API routes (backend)
│   │       └── [param]/route.ts  # dynamický endpoint (/api/profile/magnus)
│   ├── Client vs Server Components
│   └── Streaming (NDJSON)        # postupné posílání dat
├── Data fetching
│   ├── SSR (Server-Side Rendering)
│   ├── ISR (Incremental Static Regeneration)
│   └── CSR (Client-Side Rendering)
├── Styling
│   ├── Tailwind CSS (utility-first)
│   └── CSS Modules
└── Deployment
    ├── Vercel (native, serverless)
    ├── self-hosted (Docker)
    └── edge functions
```

### 1.3 Monorepo + npm workspaces (NOVÉ)

**Monorepo** = jedno git repo s více balíčky. **npm workspaces** = mechanismus npm pro monorepo.

```
outprep/
  src/                    # Next.js web
  packages/engine/        # @outprep/engine — core logika (TS lib)
  packages/fide-pipeline/ # @outprep/fide-pipeline — ETL/CLI
  packages/harness/       # CLI pro accuracy testy
```

**Proč:** oddělení zodpovědnosti (web ≠ ETL), sdílená instalace závislostí, samostatná testovatelnost.

**Pro autora:** analogie = oddělit `run_etl.py` (ETL) od web UI v samostatných balíčcích, sdílet `core` logiku (matcher, report renderer).

### 1.4 Proč se to poptává (v1 + doplnění)

| Důvod | Vysvětlení |
|-------|-----------|
| **Playwright = standard pro test automation** | (v1, beze změny) |
| **TypeScript = dominantní jazyk pro frontend** | React, Angular, Vue — vše v TS |
| **Next.js = nejpopulárnější React framework** | Vercel, default pro nové projekty |
| **Standalone produkt vyžaduje UI** | GUI na systeq.cz = Next.js/React je volba č.1 |
| **Cross-platform Playwright** | (v1) |
| **Integrace s CI/CD** | (v1) |

### 1.5 Kde se to používá (praktické příklady)

#### Příklad 1–3 (v1, beze změny): testování dashboardu, scraping, E2E B2B

#### Příklad 4 (v2, aktualizováno): Standalone job-hunt produkt
```
Aspirace: MCP-jobs → standalone web app na systeq.cz
Monorepo:
  src/            # Next.js UI (dashboard inzerátů, priority, dedup)
  packages/etl/   # Python CLI (dnešní run_etl.py)
  packages/core/  # sdílená logika (matcher, report renderer)

API routes:
  GET  /api/jobs          → seznam inzerátů z DB
  POST /api/scrape        → spustit ETL
  GET  /api/jobs/[id]     → detail inzerátu
  GET  /api/report        → report (PDF export — autor má HTML+CSS renderer!)

Cron: denně 5:00 → scrape portálů → uložit do DB → generovat report
= Přesně outprep model, ale pro job-hunt.
```

### 1.6 Přínos pro autora

| Přínos | Dopad |
|--------|-------|
| **Standalone produkt** | Port MCP-jobs na web app s GUI na systeq.cz |
| **GUI nad stávající pipeline** | Dashboard inzerátů, filtry, PDF export (Calibri/A4 renderer existuje) |
| **Odemkne Rockwell-like role** | (v1, 2× výskyt) |
| **E2E testy pro Streamlit/dashboards** | (v1) |
| **Monorepo = organizace projektů** | Oddělení ETL/UI/core, sdílené závislosti |

### 1.7 Glossary (v2 doplnění)

| Termín | Definice |
|--------|----------|
| **Next.js** | React framework (App Router, API routes, serverless) |
| **React** | Knihovna pro UI komponenty |
| **App Router** | Souborové routování v Next.js (`src/app/`) |
| **API route** | HTTP endpoint v Next.js (`src/app/api/.../route.ts`) |
| **Server Component** | Komponenta běžící na serveru |
| **Monorepo** | Jedno repo s více balíčky |
| **npm workspaces** | Mechanismus monorepo v npm |
| **Tailwind CSS** | Utility-first CSS framework (analogie: bez Bootstrap) |
| **Vercel** | Hosting platforma pro Next.js (serverless) |
| **SSR/ISR/CSR** | Způsoby renderování stránek |
| **NDJSON streaming** | Postupné posílání dat po řádcích |

*(Zbytek TS/Playwright glossary — viz v1.)*

---

## ❷ PostgreSQL + schema + migrace (NOVÝ GAP)

### 2.1 Co je PostgreSQL

PostgreSQL (Postgres) je **relační databáze** (open-source). Data v tabulkách, dotazování SQL. Standard pro produkční aplikace. Zvládá i **JSONB sloupce** (flexibilní data bez strict schématu) → hybrid relační + NoSQL.

**Klíčový insight pro autora:** autor ukládá výstupy do `output/*.json,.md` souborů. **Soubory nejsou databáze.** Pro historii, dedup, vztahy mezi daty a dotazování potřebuje DB.

| Soubory (`output/*.json`) | PostgreSQL |
|---------------------------|------------|
| Žádná historie s dotazováním | Dotazy: "co bylo minulý týden?" |
| Žádné vztahy (inzerát ↔ query) | JOIN tabulek |
| Dedup ručně (correlation_cache) | UNIQUE index (nativní) |
| Soubory se hromadí | Řádky s metadaty, mazání podle relevance |

#### Ontologie PostgreSQL (NOVÁ)

```
PostgreSQL
├── Základy
│   ├── Tabulka (rows + columns)
│   ├── PRIMARY KEY (jedinečný identifikátor)
│   ├── SERIAL (auto-increment ID)
│   ├── FOREIGN KEY (vztah mezi tabulkami)
│   └── SQL (SELECT, INSERT, UPDATE, DELETE)
├── Typy
│   ├── TEXT, INTEGER, SMALLINT, DATE, TIMESTAMPTZ
│   ├── JSONB (flexibilní JSON sloupec)
│   └── BOOLEAN
├── Indexy
│   ├── CREATE INDEX (zrychlení dotazů)
│   ├── UNIQUE INDEX (dedup — hodnota se neopakuje)
│   └── GIN (fulltext, trigramy)
├── Migrace
│   ├── CREATE TABLE IF NOT EXISTS (idempotentní)
│   └── ALTER TABLE (evoluce schématu)
├── Vztahy
│   ├── 1:1, 1:N, N:M
│   └── REFERENCES (cizí klíče)
└── Provoz
    ├── docker-compose (postgres:16)
    ├── Provider-agnostic client (porsager/postgres)
    └── DATABASE_URL env (lokální Docker / Neon / Supabase / Railway)
```

### 2.2 Proč se to poptává / proč je to nutné pro produkci

| Důvod | Vysvětlení |
|-------|-----------|
| **Produkční perzistence** | Standalone produkt bez DB neexistuje |
| **Dedup napříč runy** | Ten samý inzerát se objeví každý den. UNIQUE index na URL = nativní dedup |
| **Historie** | "Kdy jsem tento inzerát viděl poprvé?", "byl jsem na něm?" |
| **Dotazování** | SQL: filter podle company, location, salary, status |
| **Vztahy** | inzerát ↔ query ↔ profil ↔ report |
| **Audit ETL (pipeline_runs)** | Kdy běh proběhl, jak dopadl (running/completed/failed) |

### 2.3 Kde se to používá (praktické příklady)

#### Příklad 1: Dedup inzerátů (autorovo využití — vzor)
```sql
CREATE TABLE ads (
  id SERIAL PRIMARY KEY,
  url TEXT NOT NULL UNIQUE,          -- nativní dedup!
  title TEXT, company TEXT, location TEXT, salary TEXT,
  description TEXT,
  matched_keyword TEXT,
  first_seen DATE, last_seen DATE,   -- "znovu nabídnout po týdnu"
  status TEXT                         -- new / seen / applied / rejected
);
```

#### Příklad 2: Audit ETL běhů (z outprep — `pipeline_runs`)
```sql
CREATE TABLE pipeline_runs (
  id SERIAL PRIMARY KEY,
  run_type TEXT,          -- 'twic' | 'fide_ratings' (analogie: 'ai_native' | 'legacy')
  identifier TEXT,
  status TEXT DEFAULT 'running',  -- 'running' | 'completed' | 'failed'
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  metadata JSONB DEFAULT '{}'
);
```

#### Příklad 3: Cache (z outprep — `online_profiles`)
```sql
CREATE TABLE online_profiles (
  platform TEXT, username TEXT,
  profile_json JSONB,      -- celý objekt
  game_count INTEGER,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE UNIQUE INDEX ON online_profiles (platform, username);  -- dedup lookup
```

### 2.4 Přínos pro autora

| Přínos | Dopad |
|--------|-------|
| **Perzistence standalone produktu** | MCP-jobs dostane skutečnou produkční vrstvu |
| **Nativní dedup** | UNIQUE index na URL nahradí correlation_cache |
| **Historie inzerátů** | "Znovu nabídnout po týdnu", lifecycle status |
| **Audit ELT** | pipeline_runs = kdy/dokdy/jak běh proběhl |
| **Přenositelnost znalostí** | SQL = univerzální dovednost (platí pro všechny DB) |

### 2.5 Glossary (NOVÝ)

| Termín | Definice |
|--------|----------|
| **PostgreSQL** | Relační open-source databáze |
| **Relační DB** | Data v tabulkách s vztahy, SQL |
| **SQL** | Structured Query Language — jazyk pro dotazování |
| **Tabulka** | Struktura (sloupce = typy, řádky = data) |
| **PRIMARY KEY** | Jedinečný identifikátor řádku |
| **SERIAL** | Auto-increment ID (analogie: autoincrement v Python) |
| **FOREIGN KEY / REFERENCES** | Vztah mezi tabulkami |
| **INDEX** | Zrychlení dotazů |
| **UNIQUE INDEX** | Dedup — hodnota se neopakuje |
| **JSONB** | JSON sloupec v Postgres (flexibilní data) |
| **Migrace** | Evoluce schématu (idempotentní — bezpečně opakovatelná) |
| **Provider-agnostic** | Funguje s jakýmkoli hostem (Neon, Supabase, Railway, Docker) |
| **Neon / Supabase** | Serverless Postgres hostingy (gratis tier) |
| **DATABASE_URL** | Env proměnná s připojovacím řetězcem |
| **TOAST** | Komprese velkých polí v Postgres (např. PGN) |

---

## ❸ DevOps: Docker, cron, monitoring (NOVÝ GAP)

### 3.1 Co je DevOps vrstva

DevOps = **propojení vývoje (Dev) a provozu (Ops)**. Pro autora konkrétně:
- **Scheduling** — automatizace ELT (cron)
- **Monitoring** — vědět, že pipeline běží (healthchecks.io)
- **Deployment** — nasazení aplikace (Docker, Vercel)
- **CI/CD** — automatický build+test na push (GitHub Actions)
- **Konfigurace mimo kód** — .env, porty

**Klíčový insight pro autora:** MCP-jobs spouští ručně z IDE. **Produkční ELT běží sám** — denně v noci scrapne, zpracuje, uloží. Ráno otevře web a vidí výsledky. To je esence automatizace.

### 3.2 Ontologie DevOps (NOVÁ)

```
DevOps vrstva
├── Scheduling
│   ├── Cron (plánovač, formát "0 6 * * 1" = pondělí 6:00)
│   ├── Vercel Cron (serverless cron v vercel.json)
│   └── cloud scheduler (GCP, Azure Logic Apps)
├── Monitoring
│   ├── healthchecks.io (dead-man's-switch — ping = živý)
│   ├── Uptime checks
│   └── Logging (když selže, vědět proč)
├── Deployment
│   ├── Docker (image, container)
│   ├── docker-compose (multi-service: postgres + web + etl)
│   ├── Vercel / Neon / Railway (serverless)
│   └── Porty (80/443 HTTP, 5432 Postgres, 3000 Next dev)
├── CI/CD
│   ├── GitHub Actions (.github/workflows/)
│   ├── husky + lint-staged (pre-commit)
│   └── Playwright CI integration
└── Konfigurace
    ├── .env (mimo kód, nikdy v gitu)
    ├── ConfigMap (K8s analogie)
    └── CRON_SECRET (auth pro cron endpointy)
```

### 3.3 Proč se to poptává / proč je to nutné

| Důvod | Vysvětlení |
|-------|-----------|
| **ELT musí běžet sám** | Ruční spouštění z IDE ≠ produkční pipeline |
| **Vědět o selhání** | Cron mlčí = nevíš, jestli běží. healthchecks.io pošle email |
| **CI chytí regrese** | Build+test na push dřív, než se rozbije produkce |
| **Reprodukovatelnost** | Docker = stejné prostředí všude (lokal, server, cloukd) |
| **Standalone produkt = nasazení** | Aplikace musí běžet někde stabilně |

### 3.4 Praktické příklady (z outprep — source-read)

#### Příklad 1: Vercel Cron (vercel.json)
```json
{
  "crons": [
    { "path": "/api/cron/twic-update", "schedule": "0 6 * * 1" },
    { "path": "/api/cron/fide-ratings", "schedule": "0 6 1 * *" }
  ]
}
```

#### Příklad 2: healthchecks.io (route.ts)
```ts
if (!hasErrors && process.env.HEALTHCHECKS_TWIC_URL) {
  fetch(process.env.HEALTHCHECKS_TWIC_URL).catch(() => {});
}
```

#### Příklad 3: docker-compose (lokální dev)
```yaml
services:
  postgres:
    image: postgres:16
    ports:
      - "5432:5432"
    volumes:
      - ./schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
```

#### Příklad 4: Env proměnné (.env.example)
```
DATABASE_URL=postgres://outprep:outprep@localhost:5432/outprep
CRON_SECRET=...
```

### 3.5 Přínos pro autora

| Přínos | Dopad |
|--------|-------|
| **Automatizace ELT** | Cron → denní scrape bez IDE |
| **Monitoring** | healthchecks.io → vědomí o selhání |
| **CI/CD** | GitHub Actions na push = regrese odhaleny hned |
| **Reprodukovatelnost** | Docker compose = postgres + etl + web jedním příkazem |
| **Porty & konfigurace** | Základní síťová/konfig ontologie |

### 3.6 Glossary (NOVÝ)

| Termín | Definice |
|--------|----------|
| **DevOps** | Propojení vývoje a provozu |
| **Cron** | Plánovač úloh (formát minuta hodina den měsíc den_tydne) |
| **Scheduler** | Automatický plánovač |
| **healthchecks.io** | Dead-man's-switch monitoring |
| **Monitoring** | Sledování stavu systému |
| **Docker** | Zabalená aplikace + závislosti |
| **Image / Container** | Obraz / běžící instance |
| **docker-compose** | Více služeb v jednom souboru |
| **CI/CD** | Continuous Integration / Continuous Deployment |
| **GitHub Actions** | CI/CD platforma na GitHubu |
| **husky / lint-staged** | Git hooks (před commit) |
| **Port** | Číslo, na kterém služba poslouchá (80/443/5432/3000) |
| **Loopback (localhost)** | Jen lokální počítač |
| **Serverless** | Běží na cloudu bez správy serveru |
| **Dead-man's-switch** | Pokud nedorazí ping = alarm |

---

## ❹ AZ-900 Azure Fundamentals (v2: rozšířeno o PaaS/deployment kontext)

### 4.1–4.4 (v1, beze změny + doplnění)

**Doplnění v2:** imerzní analýza outprep ukázala **PaaS vrstvu**, která je analogická Azure službám. Autor vidí reálné příklady:

| outprep nástroj | Azure analogie (AZ-900) |
|-----------------|--------------------------|
| Vercel (Next.js hosting) | App Service (PaaS) |
| Neon (serverless Postgres) | Azure Database for PostgreSQL |
| Docker compose | Container Instances (ACI) |
| Vercel Cron | Logic Apps / Scheduler |
| healthchecks.io | Azure Monitor |

**Insight:** autor už používá PaaS koncepty (Vercel, Neon, Docker) *bez vědomí, že to jsou PaaS*. AZ-900 mu dá **názvosloví a framework** pro tyto služby — a přechod na Azure (pokud firma používá Microsoft) je pak jen přejmenování terminologie.

### 4.5 Glossary (v1 + doplnění PaaS)

| Termín | Definice | Analogie |
|--------|----------|----------|
| **PaaS** | Platform as a Service — hosting bez správy infrastruktury | Cloud Run, Vercel, App Service |
| **Serverless** | Běží na cloudu bez správy serveru | Vercel, Neon, Cloud Functions |
| **Azure Database for PostgreSQL** | Spravovaný Postgres v Azure | Neon, Cloud SQL |

---

## ❺ PLC Basics & Industrial Protocols (v1, beze změny)

Viz SKILL_GAPS_ROZBOR_Q3_2026_v1 — plná ontologie (hardware, IEC 61131-3, protokoly, scan cycle, výrobci), tržní kontext, 4 příklady, glossary. **Žádné změny** — nový DevOps/DB input se domény PLC netýká.

---

## ❻ Kubernetes (v2: priorita snížena)

### 6.1–6.3 (v1, beze změny — plná ontologie architektury, objektů, škálování, sítě, storage)

### 6.4 Snížení priority — klíčové zjištění v2

Edukační analýza outprep ukázala: **`outprep` zpracovává miliony her a 80K+ hráčů BEZ orchestrátoru** — jen CLI + cron + Postgres. 

| Argument | Závěr |
|----------|-------|
| Single-user job-hunt = desítky inzerátů/den | K8s je pro tuto zátěž **overkill** |
| outprep (produkční, velká data) nemá orchestrátor | K8s není nutný ani pro střední data |
| Autor neumí ani Docker compose multi-service | Skok Docker → K8s je obrovský |
| K8s = "Cloud Run na steroidech" | Autor neovládá ani základní vrstvu |

**Priorita:** 4/10 → 3.5/10. Doporučení: **nejdřív lehčí PaaS/DevOps vrstvu** (gap ❸: Docker compose, Vercel, cron, monitoring), pak teprve K8s jako volitelný enterprise výstup.

---

## EROI porovnání — všechny gapy (v2)

| Gap | EROI | Čas | Tržní signál | Přínos | Priorita |
|-----|:----:|:---:|:------------|:-------|:--------:|
| **TypeScript + Next.js + monorepo** | ⭐⭐⭐⭐⭐ | 25–35 h | 2× + standalone | GUI na systeq.cz, E2E testy | 🥇 |
| **PostgreSQL + schema + migrace** | ⭐⭐⭐⭐⭐ | 15–20 h | produkce | Perzistence, dedup, historie, audit ELT | 🥈 |
| **DevOps: Docker, cron, monitoring** | ⭐⭐⭐⭐ | 15–20 h | produkce | Automatizace ELT, healthchecks, CI | 🥉 |
| **AZ-900** | ⭐⭐⭐⭐ | 10–15 h | 4× | Certifikace, Azure match, PaaS názvosloví | 4. |
| **PLC Basics** | ⭐⭐⭐ | 40–60 h | 3× | Industrial credibility, OT/IT most | 5. |
| **Kubernetes** | ⭐⭐ | 40+ h | 3× | Enterprise — **volitelné**, overkill pro single-user | 6. |

### Důvod pořadí (v2 aktualizace)

1. **TypeScript+Next.js** = **enabler standalone produktu** — aspirace portu to dělá nejhodnotnější (9/10). GUI na systeq.cz = deliverable, který autor chce posuzovat.
2. **PostgreSQL** = **architektonický základ** — bez DB není produkční standalone. 15–20 h je nejefektivnější investice (8.5/10).
3. **DevOps vrstva** = **automatizace** — cron + monitoring + CI okamžitě zvyšují produkční kvalitu stávající pipeline, bez velkého refaktoru (8/10).
4. **AZ-900** = krátký čas, certifikace = okamžitý signál, 4 role (7.5/10).
5. **PLC** = delší čas, ale přirozený transfer z CNC. Unikátní kombinace PLC + Python (5.5/10).
6. **Kubernetes** = nejdelší čas, nejnižší EROI pro tuto fázi. Volitelné (3.5/10).

### Transfer learning matrix (v2 aktualizace)

| Zdroj (autor umí) | Cíl (gap) | Podobnost | Přenos znalostí |
|-------------------|-----------|:---------:|:---------------:|
| Python OOP | TypeScript | 70 % | Interfaces ≈ Protocol, async/await ≈ Python async |
| Pytest fixtures | Playwright fixtures | 80 % | Prakticky identický pattern |
| Streamlit dashboard | Next.js (React) | 50 % | Komponenty ≈ stránky, ale jiný model |
| Soubory JSON | PostgreSQL | 40 % | Nový koncept (dotazování, vztahy) |
| Python ETL (run_etl.py) | pipeline_runs tabulka | 60 % | Logika běhu → audit v DB |
| GCP Cloud Run | PaaS/DevOps (Vercel, Neon) | 70 % | Serverless koncepty = stejné |
| GCP Cloud Run | AZ-900 Azure | 60 % | Cloud koncepty = stejné, jiná jména |
| Docker | docker-compose | 60 % | Single → multi-service |
| Docker | Kubernetes | 40 % | K8s = Docker orchestrace |
| CNC/G-code | PLC/Ladder | 40 % | CNC = pohyb. PLC = řízení celého provozu |
| Streamlit dashboard | SCADA/MCM | 30 % | Vizualizace dat = podobný koncept |

---

## Doporučená Trajektorie (Q3+ 2026, v2)

```
TÝDEN 1-3: TypeScript + Next.js základy (15-20 h)
  └── Udemy kurz + přepis jednoho Python scriptu do TS
  └── 1 Next.js PoC: dashboard čtoucí output/*.json z MCP-jobs

TÝDEN 4-5: PostgreSQL (15-20 h)
  └── Docker compose postgres + schema.sql (ads, pipeline_runs)
  └── Uložit 1 reálný run MCP-jobs do DB

TÝDEN 6: DevOps vrstva (10-15 h)
  └── Cron pro run_etl.py + healthchecks.io + GitHub Actions (lint+test)

TÝDEN 7-8: AZ-900 kurz (10-12 h)
  └── Microsoft Learn + cvičné testy → zkouška (1 h)

TÝDEN 9-12: PLC základy (40-60 h)
  └── TIA Portal trial + Modbus PoC + dokumentace

TÝDEN 13+: Kubernetes (40+ h, VOLITELNÉ)
  └── minikube + deployment MCP serveru na K8s — až po DevOps vrstvě
```

**Milník (nový v v2):** na konci týdne 6 by měl autor umět **standalone MCP-jobs produkt v minimální verzi**: DB + cron + monitoring + web dashboard. To je deliverable, který lze posoudit.

### Metodologická vrstva (nová v2.1 — viz ADOPCNI_METODOLOGIE_2026_v1)

**Formalizovaná metodika adopce:** optimální stack metod 60/20/10/10 — PBL (60 %), Feynman→SWE_GLOSSARY (20 %), Spaced Repetition/SRS (10 %), Concept Mapping (10 %). Kanon: `01_METODIKY/04_skill_acquisition/ADOPCNI_METODOLOGIE_2026_v1.md`.

| Gap | Primární metoda | Doplňková | Proč |
|-----|-----------------|-----------|------|
| ❶ TS+Next.js | PBL (PoC dashboard) | Feynman→Glossary | Nejvyšší EROI — učit tvorbou reálného artefaktu |
| ❷ PostgreSQL | PBL (schema.sql + reálný run) | Concept Mapping | DB = vztahy → koncept mapy přirozené |
| ❸ DevOps | PBL (cron + CI + monitoring) | Feynman→Glossary | Automatizace = praxe |
| ❹ AZ-900 | SRS (cvičné testy + flashcards) | PBL (1 Azure PoC) | Certifikace = paměťová zkouška → SRS ideální |
| ❺ PLC | PBL (TIA Portal + Modbus PoC) | Concept Mapping | Průmyslová doména = fyzikální vztahy |
| ❻ K8s | PBL (minikube + MCP deployment) | Concept Mapping | Orchestrace = vztahy komponent |

**Sekvenční pravidlo:** PBL → zaznamenej nové termíny do glossary (Feynman) → generuj flashcards → SRS (FSRS engine, py-fsrs — viz chess_mcp_strategy_v1 Phase 5). Čtvrtletně reviduj koncept mapy napříč gapy.

---

## Slovník pojmů — nové termíny z v2 (odkazy na SWE_GLOSSARY)

Viz `01_METODIKY/06_SWE_glossary/SWE_GLOSSARY_zive_v1.md` (živá učebnice terminologie). Klíčové nové pojmy z v2:

| Pojem | Odkaz |
|-------|-------|
| Standalone, deliverable, monorepo, workspaces | sekce 1, 3 |
| Porty, loopback, serverless, PaaS | sekce 3, 4 |
| PostgreSQL, SQL, schema, migrace, JSONB, index | sekce 2 |
| Cron, scheduler, healthchecks.io, monitoring | sekce 3 |
| CI/CD, GitHub Actions, husky, lint-staged | sekce 3 |
| Next.js, API routes, App Router, Vercel | sekce 1 |

---

*Dokument vytvořen: 2026-08-15 | Nahrazuje: SKILL_GAPS_ROZBOR_Q3_2026_v1 (2026-08-06)*
*Zdroje: Edukační dokument docs/edukace_port_standalone_2026-08-15.md, live GitHub audit outprep (2026-08-15), SKILL_GAPS_ROZBOR_Q3_2026_v1, SWE_GLOSSARY_zive_v1*
*Provenance: Summary (technologický průzkum + edukační analýza) + source-read (schema.sql, docker-compose.yml, package.json, .env.example, vercel.json)*