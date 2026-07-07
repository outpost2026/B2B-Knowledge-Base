# Ondřej Soušek

**Systémový integrátor** — formalizace, reverse engineering a automatizace pro CAM/CNC a výrobní provozy

Praha | +420 735 045 256 | [sousek@systeq.cz](mailto:sousek@systeq.cz) | github.com/outpost2026 | linkedin.com/in/ondrejsousek | systeq.cz


## Profil

Specializuji se na převod neformalizovaných, tacitních a proprietárních systémů na explicitní, přenositelné modely — deterministické parsery, automatizační pipeline, MCP nástroje, dokumentaci a datové struktury.

Tento mechanismus jsem v roce 2026 demonstroval reverzním inženýrstvím nedokumentovaného binárního formátu .VCF (CAM software Ruida/VCutWorks): bez veřejné specifikace a SDK jsem ve 22 vývojových cyklech vytvořil deterministický parser s přesností extrakce dráhy \>99,98 % cross-validovanou proti referenčnímu CAM nástroji, a nasadil jej na GCP Cloud Run pro reálného B2B klienta.

Stejný mechanismus stojí za 14 lety praxe v průmyslové výrobě a CNC obrábění — ta mi dává schopnost rozpoznat, kde v provozu vznikají informační asymetrie a závislosti na jednotlivcích — i za vývojem vlastní off-grid energetické infrastruktury a datových/znalostních pipeline. Python, GCP, Docker a CAD/CAM nástroje používám jako prostředky této transformace, nikoli jako cíl sám o sobě.


## Co přináším

### Jádro: extrakce a formalizace komplexních systémů

- **Reverzní inženýrství** nedokumentovaných binárních formátů a proprietárních datových struktur (hex analýza, IEEE 754, pair-diff diagnostika) bez specifikace či SDK.

- **Systematické mapování a dokumentace** tacitního provozního know-how — typicky vázaného na odcházející klíčové pracovníky — do strukturovaných znalostních korpusů.

- **Identifikace informačních asymetrií**, gatekeeperů a single-points-of-failure v provozních procesech a návrh jejich formalizace nebo eliminace (bus-factor zero).

- **Návrh deterministických datových modelů** z heuristických či expertních odhadů — např. predikce strojového času a klasifikace komplexity zakázky z CAM dat (±19% CI).

### Implementace — nástroje, kterými mechanismus realizuji

- **Python 3.12** (struct, math — deterministické binární parsery), pytest, golden master regrese, determinism testy, type hints, strukturovaný logging.

- **GCP**: Cloud Run, Artifact Registry, Cloud Build, Cloud Scheduler, Firestore; Docker (python:3.12-slim); Streamlit; Flask REST API.

- **MCP & Agentic**: FastMCP server s tool registry, cross-repo vyhledávání, EROI scoring LinkedIn nabídek.

- **CI/CD & DevSecOps**: GitHub Actions (ci.yml, codeql.yml, Dependabot), CodeQL security analysis, multi-matrix testing (Python 3.10-3.12).

- **CAM/CNC**: G-kód, NCstudio 10, VCutWorks, LightBurn, DXF pipeline processing, řešení barevné divergence CAM palet (euklidovská RGB interpolace).

- **ETL a data engineering**: web scraping (Playwright, BeautifulSoup, Requests), API integrace (JSON/XML), RAG pipeline s deduplikací a klasifikační taxonomií.


## Klíčové projekty

### VCF/DXF Parser Engine (03-07/2026) — vlajkový B2B projekt

**Vstupní stav** (vysoká informační entropie): Výrobní B2B klient (CNC zpracování) byl závislý na proprietárním binárním formátu .VCF (Ruida/VCutWorks) bez veřejné specifikace a SDK a na tacitním know-how odcházejícího klíčového technika.

**Proces** (extrakce a formalizace): 22 vývojových cyklů parseru (V1-V22) s paralelní dokumentací provozního know-how (materiály, kalibrace, workflow) a cross-validací proti referenčnímu CAM softwaru.

**Výsledek** (explicitní model): Deterministický parser s přesností extrakce délky dráhy \>99,98 %, predikční pole pro odhad strojového času a klasifikaci komplexity zakázky. Paralelní DXF indexer řešící barevnou divergenci CAM palety. **Test coverage**: golden master regrese (17 test cases), determinism testy (6 test cases), 10/10 PASS. **Deployment**: GCP Cloud Run (Docker, Artifact Registry) + Streamlit dashboard + Flask REST API pro ERP integraci.

**Živé demo**: vcf-parser-demo-537446704644.europe-west1.run.app

### MCP & Agentic Tooling (07/2026)

- **mcp-local-server**: FastMCP server s 20+ nástroji pro cross-repo vyhledávání, git operace, session state management — paralelní ThreadPoolExecutor architektura.

- **linkedin-mcp-custom**: EROI scoring engine pro LinkedIn nabídky — 6dimenzionální scoring (domain, tech, role, growth, formal, location) s KB write-back a automatickým git commit.

### DXF Pipeline & CAD Bridge (06/2026)

- **dxf\_integrace**: OOP refaktor DXF pipeline, layer card extraction, ML-ready vektory, golden master testing.

- **cad2llm**: SketchUp/COLLADA → sémantický JSON s 0% geometrických chyb na 30 testovacích uzlech.


## Trajektorie

| Období | Role | Poznámka |
| - | - | - |
| 2010–2023 | Technické a manuální profese | 14 let ve výrobních provozech, samostudium, zahraničí pobyty |
| 2022–2024 | Off-grid stavitel | Outpost — FVE, LiFePO4, IoT telemetrie, kompletní DIY |
| 2025–2026 | CNC (waterjet, ploter knifes) | Vstup do výrobního prostředí, mapování tacitního know-how |
| 03/2026 | První commit na GitHub | 0 Python, 0 Git, 0 Cloud → 14 repo ekosystém |
| 06/2026 | B2B jednání | První NDA, produkční VCF parser, vývoj kompilátoru |
| 07/2026 | Modular engineering ecosystem | OOP refaktor, CI/CD, MCP, 465+ commits, 4 repo s CI |



## Vzdělání a jazyky

- **14 let praktické kvalifikace** v průmyslové výrobě a CNC obrábění — doménová báze pro identifikaci a formalizaci informačních asymetrií

- **Samostudium** zaměřené na nástroje transformace: Python, GCP, reverzní inženýrství, MCP, LLM-asistovaný vývoj (2025–2026)

- **Čeština** — rodilý jazyk | **Angličtina** — C1 (technická dokumentace, komunikace) | **Francouzština** — komunikativní úroveň


## Hledám

B2B spolupráci a projekty zaměřené na formalizaci a digitalizaci výrobních a provozních procesů — zejména situace s proprietárními formáty, tacitním know-how vázaným na jednotlivce nebo neformalizovanými workflow, kde vzniká prostor pro převod implicitního systému na explicitní, přenositelné aktivum.

Otevřen dlouhodobé B2B spolupráci (konzultace, licencování IP), OSVČ projektům i HPP v oblasti průmyslové automatizace, CAM/CNC software, MCP/agentic vývoje nebo ERP integrace. Praha a okolí / remote.


*Poslední aktualizace: červenec 2026*
