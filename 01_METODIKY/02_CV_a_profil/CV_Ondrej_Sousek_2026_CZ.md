# Ondřej Soušek

## Automation & Integration

**Python · Data/ETL · SQL/PostgreSQL · MCP/LLM integrace · Reverse engineering · Industrial systems**

Praha, Česko · +420 735 045 256 · [sousek@systeq.cz](mailto:sousek@systeq.cz)  
[github.com/outpost2026](https://github.com/outpost2026) · [systeq.cz](https://www.systeq.cz/) · [LinkedIn](https://www.linkedin.com/in/ondrejsousek)

## Profil

Automation & Integration Engineer s výrobním a CNC zázemím. Navrhuji Pythonové automatizační a datové systémy pro prostředí, kde jsou procesy neformální, data neúplná nebo software proprietární. Kombinuji ingestion a transformace dat, SQL/PostgreSQL, deterministickou validaci a MCP/LLM integrační vrstvu s praktickým porozuměním fyzickým omezením výroby =  Specializuji se na převod tacitních pravidel a nesourodých zdrojů do strukturovaných a testovatelných systémů.

## Klíčové kompetence

| Oblast | Dovednosti a praktický rozsah |
| - | - |
| **Software a data** | Python, CLI nástroje, datové modely, YAML konfigurace, ETL pipeline, HTTP/API integrace, normalizace, deduplikace a reportování. |
| **Databáze** | SQL/PostgreSQL: relační schéma, dotazy, upsert/persistence, lokální provoz a testovací databáze v CI. |
| **MCP a applied AI** | FastMCP: tools, resources a prompts; návrh transparentních workflow, kde LLM/MCP vrstva pracuje nad deterministickými pravidly a daty. |
| **Kvalita a delivery** | pytest, regresní a deterministické testy, Ruff, CI workflow, strukturované logování, technická dokumentace a reprodukovatelné výstupy. |
| **Reverse engineering** | Analýza proprietárních binárních formátů, hex/pair-diff diagnostika, IEEE 754, serializace a ověřování proti referenčním datům. |
| **Průmyslová doména** | CNC/CAM, CAD/DXF, G-kód, NCstudio 10, VCutWorks, LightBurn, práce podle 2D výkresů a digitalizace výrobních workflow. |
| **Infrastruktura** | Git, Docker; projektová zkušenost s GCP Cloud Run, Artifact Registry, Cloud Build, Cloud Scheduler a Firestore. |


## Vybrané technické projekty

### [MCP-Jobs](https://github.com/outpost2026/MCP-Jobs) — multi-provider market-intelligence ETL | 2026

Pythonový MCP server pro práci s českými pracovními portály. Řešení kombinuje šest providerů, HTTP scraping, boolean AST matching, URL a fuzzy deduplikaci, strukturované výstupy, PostgreSQL persistence, asynchronní joby a MCP tools/resources/prompts.

Projekt prokazuje praktickou schopnost navrhnout datovou pipeline od ingestion přes transformace až po persistenci a AI-facing interface. Zahrnuje CLI, CI, linting, telemetry/logging a 189 automatizovaných testů.

### [VCF/DXF Parser Engine](https://github.com/outpost2026/Vcf-compiler) — reverse engineering a automatizace výroby | 2026

Reverse-engineering nástroje pro nezdokumentovaný binární formát `.VCF` v ekosystému Ruida/VCutWorks a paralelní DXF zpracování. Bez veřejné specifikace či SDK jsem ve 22 iteracích vytvořil deterministický parser, jehož původní validační případ uvádí přesnost extrakce dráhy nad 99,98 % při cross-validaci proti LightBurn.

Součástí řešení jsou golden-master regrese, deterministické testy, 2D vizualizace, odhad strojového času, ERP-ready exporty a Docker/GCP Cloud Run deployment. Projekt vznikal v kontextu výrobního B2B využití pod NDA; klientské údaje a obchodní metriky nezveřejňuji.

### [LinkedIn MCP Analyzer](https://github.com/outpost2026/linkedin-mcp-analyzer) — career intelligence a rozhodovací podpora | 2026

Konfigurovatelný MCP workflow pro převod uložených pracovních nabídek na strukturované hodnocení fitu, gapů a priorit. Kombinuje deterministický EROI model, reportování, automatizovaný zápis do knowledge base, testy, pre-commit a lockovaný vývojový stack.

Projekt ukazuje applied-AI přístup: LLM/MCP není pouze generátor textu, ale integrační vrstva nad transparentními pravidly a měřitelnými rozhodovacími kritérii.

## Profesní zkušenost

### SYSTEQ / OSVČ — Automation & Integration Projects

**Praha · 2026–současnost**

Rozvoj nástrojů pro výrobní digitalizaci, datová workflow a technické B2B integrace. Pracuji na formalizaci procesů, prototypování a implementaci nástrojů pro CAD/CAM data, strukturování neformálních informací, automatizované scoringy a rozhodovací podporu.

Výstupy zahrnují VCF/DXF tooling, Pythonové CLI a pipeline nástroje, PostgreSQL persistence, MCP rozhraní, testovací automatizaci, dokumentaci a projektovou práci s Dockerem a GCP.

### CNC

**Praha · 2025–2026**

Obsluha CNC strojů pro vodní paprsek a řezných plotrů, editace G-kódu v NCstudio 10 a práce s DXF/CAD; samostatná příprava výrobních dat a realizace zakázky od vstupu po výrobu 

Tato role vytvořila přímý doménový základ pro návrh software, který respektuje fyzická omezení, kvalitu vstupních dat a provozní návaznosti.

## Odborný rozvoj

### Self-directed Software Engineering

**2025–2026**

Samostatně vybudovaná praxe v Pythonu, software architecture, data/ETL pipelines,  SQL/PostgreSQL, Dockeru, CI, MCP/LLM integracích a reverse engineeringu. Důkazy jsou dostupné ve veřejných repozitářích (github.com/outpost2026) a jejich testovacích, dokumentačních a release artefaktech.

## Jazyky

| Jazyk | Úroveň |
| - | - |
| Čeština | Rodný jazyk |
| Angličtina | C1 — technická dokumentace a komunikace |
| Francouzština | Komunikativní úroveň |


## Cílové role a spolupráce

Automation Engineer · Integration Engineer · Industrial Digitalization Engineer · Data/AI Automation Developer · Technical Solutions Engineer. Otevřen HPP, dlouhodobé B2B spolupráci nebo OSVČ projektům v Praze, hybridně nebo remote.

