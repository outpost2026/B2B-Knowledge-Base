# ONDŘEJ SOUŠEK

**Systémový integrátor — formalizace, reverse engineering a automatizace pro CAM/CNC, výrobní provozy a agentní infrastrukturu**

Praha | +420 735 045 256 | [sousek@systeq.cz](mailto:sousek@systeq.cz) | github.com/outpost2026 | systeq.cz | linkedin.com/in/ondrejsousek

## PROFIL

Specializuji se na převod neformalizovaných, tacitních a proprietárních systémů na explicitní, přenositelné modely — deterministické parsery, automatizační pipeline, dokumentaci a datové struktury. Tento mechanismus jsem v roce 2026 demonstroval reverzním inženýrstvím nedokumentovaného binárního formátu .VCF (CAM software Ruida/VCutWorks): bez veřejné specifikace a SDK jsem ve 22 iteracích vytvořil deterministický parser s přesností extrakce dráhy >99,98 % a nasadil jej na GCP Cloud Run pro reálného výrobního B2B klienta (200+ zakázek/měsíc).

Ve stejném roce jsem postavil kompletní agentní infrastrukturu: 4 vlastní MCP servery (40+ nástrojů), 7 testovacích sad s 228 testy, CI/CD pipeline a znalostní bázi řízenou vlastním EROI scoring modelem. Portfolio: 18 repozitářů, 690 commitů (průměr 4,5/den), 21 600+ produkčních řádků Pythonu za 17 týdnů.

Stejný mechanismus stojí za 14 lety praxe v průmyslové výrobě a CNC obrábění — ta mi dává schopnost rozpoznat, kde v provozu vznikají informační asymetrie a závislosti na jednotlivcích. Python, GCP, Docker, MCP a CAD/CAM nástroje používám jako prostředky této transformace, nikoli jako cíl sám o sobě.

## CO PŘINÁŠÍM

**Jádro: extrakce a formalizace komplexních systémů**

- Reverzní inženýrství nedokumentovaných binárních formátů a proprietárních datových struktur (hex analýza, IEEE 754, pair-diff diagnostika) bez specifikace či SDK.
- Systematické mapování a dokumentace tacitního provozního know-how — typicky vázaného na odcházející klíčové pracovníky — do strukturovaných znalostních korpusů.
- Identifikace informačních asymetrií, gatekeeperů a single-points-of-failure v provozních procesech a návrh jejich formalizace nebo eliminace.
- Návrh deterministických datových modelů z heuristických či expertních odhadů — např. predikce strojového času (±2–5 %) a klasifikace komplexity zakázky z CAM dat.

**Agentní inženýrství (2026)**

- 4 produkční MCP servery postavené za 17 dní: cnc-tools (21 nástrojů), linkedin-analyzer (EROI pipeline), mcp-jobs (job scraping), lichess-analyzer (17 nástrojů, Stockfish 18 integrace).
- Vlastní EROI scoring model (6 dimenzí s váhami: domain 35 %, tech 25 %, role 20 %, growth 10 %, formal 5 %, location 5 %) pro automatickou selekci nabídek.
- Řízení kvality LLM výstupů: narrative validator (anti-hallucination guard, 5 kategorií), kompresní validace patternů, deterministická data-first architektura.
- Znalostní báze s governance pravidly P1–P5 (zákaz klonů, archívní politika, drift check) — trim 86 → 56 souborů (−35 %), 0 duplicit.

**Implementace — nástroje, kterými mechanismus realizuji**

- Python 3.11/3.12/3.14 (struct, math — deterministické binární parsery), pytest (228 testů napříč 7 repy), golden master regrese, determinism testy, CI/CD (GitHub Actions, matrix 3 verzí Pythonu, CodeQL, Dependabot).
- MCP: FastMCP, MCP protocol stdio, Streamlit, Playwright/Patchright, Python SDK.
- GCP: Cloud Run, Cloud Functions, Cloud Scheduler (6 cron jobů), GCS, Firestore, BigQuery; Docker (python:3.12-slim).
- CAM/CNC: G-kód, NCstudio 10, VCutWorks, LightBurn, DXF pipeline processing, řešení barevné divergence CAM palet (ACI→RGB→Euclidean resolver).
- ETL a data engineering: web scraping (Playwright, BeautifulSoup, Requests), API integrace, RAG pipeline s deduplikací a klasifikační taxonomií.

## KLÍČOVÉ PROJEKTY

**1. VCF/DXF Parser Engine (2026) — reverse engineering, B2B**

Výrobní B2B klient (CNC zpracování, 200+ zakázek/měsíc) byl závislý na proprietárním binárním formátu .VCF bez veřejné specifikace a na tacitním know-how odcházejícího klíčového technika. Souběžně jsem zdokumentoval provozní know-how a reverzně analyzoval binární strukturu — 22 iterací parseru, cross-validace proti referenčnímu CAM softwaru.

Výsledek: deterministický parser s přesností extrakce délky dráhy >99,98 % (odchylka <0,02 % proti LightBurn), predikce strojového času ±2–5 %, klasifikace komplexity zakázky. DXF indexer s euklidovskou RGB interpolací barevné divergence a block explosion pro INSERT entity. Nasazení: GCP Cloud Run + Streamlit dashboard + Flask REST API pro ERP. Golden master regrese 10/10 PASS.

**2. MCP-Jobs v0.4.0 — job scraping pipeline**

MCP server pro scraping českých pracovních portálů (3 aktivní portály). Vlastní boolean AST parser s AND/OR/NOT syntaxí a LRU cache (8000 → 8 re-parsů na query), rate limiting 1,0 s, exclude/location/salary filtry. 125/125 testů PASS (66 % coverage), pipeline 4,5× rychlejší než legacy (46 s vs 210 s), 9 iteračních fází vč. de novo auditu (20 nálezů) a cross-LLM auditu.

**3. LinkedIn EROI Analyzer — tržní inteligence**

Automatizovaná pipeline: scrape saved jobs → EROI scoring (6 dimenzí) → report → KB write-back. Anti-bot inženýrství (adaptivní delay 3–7 s, fingerprint mix, session heartbeat). 71 sledovaných nabídek, 6 % relevantních (EROI ≥ 65) — kvantifikované zdůvodnění follow-upu. 66/66 testů, weekly CI cron.

**4. lichess-analyzer-mcp — LLM pattern engineering**

MCP server (17 nástrojů) s integrací Stockfish 18, pattern library 18 patternů (A–Q1), dual cache (Stockfish + LLM). ACPL MAE 3,9 proti Lichess referenci, 0 % silent fail, 88 analyzovaných her. Empirická evaluace LLM kaskády (DeepSeek V4 Flash SNR 93 %). 68/68 testů.

## PRACOVNÍ ZKUŠENOSTI

**SYSTEQ / Freelance technický realizátor (OSVČ) — Outpost, Praha** | 2023 – současnost

- VCF/DXF Parser Engine — viz klíčový projekt výše.
- Agentní infrastruktura: 4 MCP servery, EROI pipeline, znalostní báze (196 commitů, governance P1–P5).
- Vývoj a provoz off-grid technického uzlu — převod 14 let praktických zkušeností s energetikou a stavbou na dokumentovaný, funkční systém: FVE 2,5 kWp, LiFePO4 8S2P 630 Ah, BMS s aktivním balancováním.
- Datové a znalostní pipeline na GCP: ETL pro meteorologická a senzorová data, RAG pipeline pro migraci dokumentů, RE interního API ČHMÚ (42 endpointů).

**CNC operátor (vodní paprsek) — Praha** | 2025 – 2026

- Obsluha CNC stroje (vodní paprsek), editace G-kódu v NCstudio 10, příprava výrobních dat dle 2D výkresů.
- Mapování implicitního provozního rozhodování — volby řezných parametrů, kritérií kontroly kvality — a převod do explicitních pravidel.

**Technické a manuální profese — výroba, stavebnictví** | 2010 – 2023

- 14 let praxe ve výrobních a stavebních provozech: čtení výkresové dokumentace, práce s materiálem, root-cause analýza výrobních problémů.

## VZDĚLÁNÍ A ODBORNÁ PŘÍPRAVA

- 14 let praktické kvalifikace v průmyslové výrobě a CNC obrábění (vodní paprsek, frézování).
- Samostudium zaměřené na nástroje transformace: Python, GCP, reverzní inženýrství binárních formátů, LLM-asistovaný vývoj, MCP (2025–2026).

## JAZYKY

Čeština — rodný jazyk | Angličtina — C1 (technická dokumentace, komunikace) | Francouzština — komunikativní úroveň

## HLEDÁM

B2B spolupráci a projekty zaměřené na formalizaci a digitalizaci výrobních a provozních procesů — zejména situace s proprietárními formáty, tacitním know-how vázaným na jednotlivce nebo neformalizovanými workflow. Dále implementace agentní infrastruktury (MCP servery, EROI pipeline, automatizace) pro SME a startupy. Otevřen dlouhodobé B2B spolupráci (konzultace, licencování IP), OSVČ projektům i HPP v oblasti průmyslové automatizace, CAM/CNC software, ERP integrace nebo AI toolingu. Praha a okolí / remote.
