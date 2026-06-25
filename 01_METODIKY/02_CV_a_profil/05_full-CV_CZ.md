# ONDŘEJ SOUŠEK

**Systémový integrátor — formalizace, reverse engineering a automatizace pro CAM/CNC a výrobní provozy**

Praha | +420 735 045 256 | [sousek@systeq.cz](mailto:sousek@systeq.cz) | github.com/outpost2026 | systeq.cz

## PROFIL

Specializuji se na převod neformalizovaných, tacitních a proprietárních systémů na explicitní, přenositelné modely — deterministické parsery, automatizační pipeline, dokumentaci a datové struktury. Tento mechanismus jsem v roce 2026 demonstroval reverzním inženýrstvím nedokumentovaného binárního formátu .VCF (CAM software Ruida/VCutWorks): bez veřejné specifikace a SDK jsem ve 22 iteracích vytvořil deterministický parser s přesností extrakce dráhy \>99,98 % a nasadil jej na GCP Cloud Run pro reálného výrobního B2B klienta (200+ zakázek/měsíc).

Stejný mechanismus stojí za 14 lety praxe v průmyslové výrobě a CNC obrábění — ta mi dává schopnost rozpoznat, kde v provozu vznikají informační asymetrie a závislosti na jednotlivcích — i za vývojem vlastní off-grid energetické infrastruktury a datových/znalostních pipeline. Python, GCP, Docker a CAD/CAM nástroje používám jako prostředky této transformace, nikoli jako cíl sám o sobě.

## CO PŘINÁŠÍM

**Jádro: extrakce a formalizace komplexních systémů**

- Reverzní inženýrství nedokumentovaných binárních formátů a proprietárních datových struktur (hex analýza, IEEE 754, pair-diff diagnostika) bez specifikace či SDK.

- Systematické mapování a dokumentace tacitního provozního know-how — typicky vázaného na odcházející klíčové pracovníky — do strukturovaných znalostních korpusů.

- Identifikace informačních asymetrií, gatekeeperů a single-points-of-failure v provozních procesech a návrh jejich formalizace nebo eliminace.

- Návrh deterministických datových modelů z heuristických či expertních odhadů — např. predikce strojového času a klasifikace komplexity zakázky z CAM dat.

**Implementace — nástroje, kterými mechanismus realizuji**

- Python 3.11/3.12 (struct, math — deterministické binární parsery), pytest, golden master regrese, determinism testy, type hints, strukturovaný logging.

- GCP: Cloud Run, Artifact Registry, Cloud Build, Cloud Scheduler, Firestore; Docker (python:3.11-slim); Streamlit; Flask REST API.

- CAM/CNC: G-kód, NCstudio 10, VCutWorks, LightBurn, DXF pipeline processing, řešení barevné divergence CAM palet.

- ETL a data engineering: web scraping (Playwright, BeautifulSoup, Requests), API integrace (JSON/XML), RAG pipeline s deduplikací a klasifikační taxonomií.

## KLÍČOVÝ PROJEKT — demonstrace mechanismu: VCF/DXF Parser Engine (2026)

**Vstupní stav (vysoká informační entropie)**

Výrobní B2B klient (CNC zpracování, 200+ zakázek/měsíc) byl závislý na proprietárním binárním formátu .VCF (Ruida/VCutWorks) bez veřejné specifikace a SDK a na tacitním know-how odcházejícího klíčového technika.

**Proces (extrakce a formalizace)**

Souběžně jsem systematicky zdokumentoval provozní know-how (materiály, kalibrace, workflow) a reverzně analyzoval binární strukturu .VCF — 22 iterací parseru (V1–V22), cross-validace proti referenčnímu CAM softwaru.

**Výsledek (explicitní model)**

Deterministický parser s přesností extrakce délky dráhy \>99,98 % (cross-validace proti LightBurn, odchylka \<0,02 %), počítaná pole pro odhad strojového času a klasifikaci komplexity zakázky. Paralelní DXF indexer řešící barevnou divergenci CAM palety (euklidovská RGB interpolace, block explosion pro INSERT entity). Nasazení: GCP Cloud Run (Docker, Artifact Registry) + Streamlit dashboard + Flask REST API pro ERP integraci. Golden master regrese 10/10 PASS, determinism testy 2/2 PASS.

**Hodnota pro klienta**

Nezávislost na jednotlivci a jeho odchodu, přenositelná dokumentace a kód jako nové firemní aktivum, automatizovaný datový vstup pro plánování výroby a ERP.

🔗 Live demo: vcf-parser-demo-537446704644.europe-west1.run.app

## PRACOVNÍ ZKUŠENOSTI

**SYSTEQ / Freelance technický realizátor (OSVČ) — Outpost, Praha** | 2023 – současnost

- VCF/DXF Parser Engine — viz klíčový projekt výše.

- Vývoj a provoz off-grid technického uzlu  — převod 14 let praktických zkušeností s energetikou a stavbou na dokumentovaný, funkční systém infrastruktury: FVE 2,5 kWp, LiFePO4 8S2P 630 Ah, BMS s aktivním balancováním. Stejný mechanismus formalizace implicitních zkušeností do explicitního systému, aplikovaný na fyzickou infrastrukturu.

- Datové a znalostní pipeline na GCP: ETL pro meteorologická a senzorová data, RAG pipeline pro migraci dokumentů s deduplikací a klasifikační taxonomií — formalizace nestrukturovaných dat do strukturovaných, dotazovatelných systémů.

**CNC operátor (vodní paprsek) — Praha** | 2025 – 2026

- Vstup do výrobního prostředí s vysokou informační entropií: obsluha CNC stroje (vodní paprsek), editace G-kódu v NCstudio 10, příprava výrobních dat dle 2D výkresů.

- Mimo formální náplň práce mapování implicitního provozního rozhodování — volby řezných parametrů, kritérií kontroly kvality, optimalizace průtoku materiálu — a jeho převod do explicitních pravidel. Role jako vstupní brána k pozdější formalizační práci, nikoli jako konečný cíl.

**Technické a manuální profese — výroba, stavebnictví** | 2010 – 2023

- 14 let praxe ve výrobních a stavebních provozech: čtení výkresové dokumentace, práce s materiálem, root-cause analýza výrobních problémů.

- Opakovaná expozice systémům s vysokou informační entropií vytvořila doménovou bázi, ze které vychází schopnost rozpoznávat a formalizovat informační asymetrie v dalších kontextech.

## VZDĚLÁNÍ A ODBORNÁ PŘÍPRAVA

- 14 let praktické kvalifikace v průmyslové výrobě a CNC obrábění (vodní paprsek, frézování) — doménová báze pro identifikaci a formalizaci informačních asymetrií.

- Samostudium zaměřené na nástroje transformace: Python, GCP, reverzní inženýrství binárních formátů, LLM-asistovaný vývoj (2025–2026).

## JAZYKY

Čeština — rodný jazyk | Angličtina — C1 (technická dokumentace, komunikace) | Francouzština — komunikativní úroveň

## HLEDÁM

B2B spolupráci a projekty zaměřené na formalizaci a digitalizaci výrobních a provozních procesů — zejména situace s proprietárními formáty, tacitním know-how vázaným na jednotlivce nebo neformalizovanými workflow, kde vzniká prostor pro převod implicitního systému na explicitní, přenositelné aktivum. Otevřen dlouhodobé B2B spolupráci (konzultace, licencování IP), OSVČ projektům i HPP v oblasti průmyslové automatizace, CAM/CNC software nebo ERP integrace. Praha a okolí / remote.

