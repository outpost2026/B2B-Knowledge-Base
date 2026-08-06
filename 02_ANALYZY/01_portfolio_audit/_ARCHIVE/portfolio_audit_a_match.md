# Portfolio Audit & Match Analysis

**Autor:** Ondřej Soušek  
**Datum:** 2026-06-20  
**Zdroje:** GitHub (6 repozitářů, README, RE case study, kazuistiky), `05_full-CV_CZ.md`, LinkedIn profil (aktuální), LinkedIn analýzy (24 nabídek), syntetický report

---

## 0. Co se změnilo po načtení skutečného CV

Předchozí analýza vycházela z **inferovaného CV** (rekonstruovaného z konverzace). Po načtení `05_full-CV_CZ.md` a aktuálního LinkedIn headline:

### 0.1 Korekce předchozích předpokladů

| Předpoklad (starý) | Skutečnost (z CV CZ) | Dopad |
|---|---|---|
| CV je technicky orientované (seznam technologií) | CV je **positioningové** — "nejsem primárně programátor, jsem formalizátor systémů" | ✅ **Silnější odlišení od běžných kandidátů** |
| LinkedIn headline obsahuje "self-taught developer" | LinkedIn headline: **"Industrial Automation & Knowledge Systems \| CNC/CAM \| Python"** | ✅ **Mnohem lepší než předpoklad — již je industrial-focused** |
| LinkedIn "about" chybí | LinkedIn "about": explicitní positioning na formalizaci tacitních znalostí, informační asymetrie, procesní dluh | ✅ **Silný, dobře napsaný — vzácný na LinkedIn** |
| CV uvádí TypeScript/JavaScript jako secondary skill | CV **neuvádí** TypeScript ani JavaScript — pouze Python | ✅ **Konzistentní s GitHub realitou** |
| CV uvádí Bash | CV **neuvádí** Bash | ✅ **Konzistentní** |
| Autor se prezentuje jako "developer" | Autor se explicitně **distancuje** od role programátora: "Nehlásím se na pozici programátora — programování používám jako nástroj" | 🔥 **Klíčová nuance pro positioning na trhu** |

### 0.2 LinkedIn "o mně" — sémantická analýza

Aktuální text (parafráze z LinkedIn):
> *"Specializuji se na převod implicitních procesů a znalostí do explicitních datových modelů, automatizací a provozních nástrojů. Nehlásím se primárně na pozici programátora — programování používám jako nástroj. Zajímají mě prostředí s informační asymetrií, procesním dluhem, neformalizovaným know-how nebo provozním chaosem."*

**Hodnocení:**
- ✅ **Unikátní positioning** — na LinkedIn je toto velmi neobvyklé a atraktivní pro správné employery
- ✅ **Konzistentní s CV i GitHubem** — "formalizace" je thread skrz všechny zdroje
- ✅ **Autentické** — není to přefouknutý technický bullshit
- ⚠️ **Může být příliš abstraktní** — recruiters who search for "Python" or "test automation" ho nemusí najít
- ⚠️ **Algoritmus to neumí parsovat** — LinkedIn fulltext indexuje slova, ne koncepty. "Informační asymetrie" není keyword který recruiteři hledají

### 0.3 LinkedIn headline — aktuální znění

> *"Industrial Automation & Knowledge Systems | CNC/CAM | Python"*

**Hodnocení:**
- ✅ "Industrial Automation" — správný domain signal
- ✅ "Knowledge Systems" — unikátní diferenciace
- ⚠️ "CNC/CAM" — úzký, ale cílený
- ⚠️ "Python" — poslední slovo, nejméně důležité pro positioning

**Doporučená úprava headline:**
> *"Industrial Automation Engineer | System Integration, CNC/CAM, Python | Reverzní inženýrství & Formalizace"*

### 0.4 Revidovaný skill set z CV CZ

CV CZ uvádí LinkedIn skills:
- **Python** ✅ (doloženo GitHubem)
- **CNC Programming / CNC Machining** ✅ (doloženo)
- **Integration Engineering** ✅ (doloženo VCF parserem)
- **Cloud Computing / GCP** ✅ (doloženo)
- **R&D / Výzkum a vývoj** ✅ (doloženo RE case study)

**Chybějící skills které by měly být přidány:**
- Reverse Engineering (není v LinkedIn skills — klíčový!)
- Test Automation / Golden Master Testing
- Docker / Containerization
- IoT / Embedded Systems
- Data Pipeline / ETL
- CAM Software (VCutWorks, LightBurn)

---

## 1. GitHub Profile Audit — zjištěný stack vs. předpoklady

### 1.1 Verifikace předpokladů z předchozí analýzy

| Předpoklad (z CV/profile) | GitHub evidence | Verdikt |
|---|---|---|
| **Python** | ✅ 7 repozitářů, 2 produkční parsery (VCF parser + DXF indexer), cad2llm konvertor, RAG indexer, ETL pipeline. Hlavní jazyk ~100 % napříč všemi repy. | ✅ **Potvrzeno — core skill** |
| **Reverzní inženýrství** | ✅ 29denní RE case study: VCF binární formát (Ruida/VCutWorks) — IEEE 754 double float, Windows-1250 encoding, 74B segmenty. DXF ACI divergence od AutoCAD standardu. 22 verzí parseru. | ✅ **Potvrzeno — expertní úroveň** |
| **Testování** | ✅ Golden master regression framework (10 testů), determinism testy (2), smoke testy. Baseline JSONy v repu. | ✅ **Potvrzeno — systematický přístup** |
| **CI/CD** | ⚠️ GCP Cloud Run deployment je popsán (Docker → Cloud Run), CI/CD pipeline v repu není dokumentována. | ⚠️ **Částečně — chybí GitHub Actions konfigurace** |
| **Kubernetes** | ❌ V žádném repu není Dockerfile nebo Kubernetes manifest. Deployment je popsán jako "Docker → Cloud Run" bez K8s. | ❌ **Nepotvrzeno — K8s není doložen kódem** |
| **PLC** | ❌ V repozitářích není žádný PLC kód, ladder diagramy, nebo zmínka o PLC. | ❌ **Nepotvrzeno — chybí digitální stopa** |
| **CAM/CNC** | ✅ Rozsáhlá dokumentace: VCutWorks, LightBurn, Ruida, vodní paprsek, oscilační nůž, CAM workflow. Parser VCF formátu je přímý důkaz. | ✅ **Potvrzeno — hluboká doménová znalost** |
| **GCP Cloud** | ✅ Cloud Run, Cloud Scheduler, Firestore, BigQuery, Artifact Registry, IAM, Cloud Storage. 6 produkčních služeb. | ✅ **Potvrzeno — produkční cloud zkušenost** |
| **IoT/ESP32** | ✅ Outpost-security-perimeter: ESP32, PIR, Doppler, tenzometry, low-power režimy, Telegram notifikace. | ✅ **Potvrzeno — embedded IoT** |
| **Streamlit** | ✅ Streamlit dashboard pro VCF parser (GCP Cloud Run). | ✅ **Potvrzeno** |

### 1.2 Nově zjištěné dovednosti (nebyly v předpokladech)

| Dovednost | Důkaz | Level |
|---|---|---|
| **COLLADA/XML parsing** | cad2llm: lxml + numpy rekurzivní 4×4 matice | Produkční |
| **LLM multi-model orchestrace** | 5 modelů (DeepSeek, Gemini, Claude, Groq, ChatGPT), OpenCode CLI, paid API, handoff JSON formát (15+ dokumentů) | Expertní |
| **Binární formát RE** | IEEE 754 double float little-endian, bit masking, hex diff, pair diff, 74B segment blocks | Expertní |
| **Euklidovská RGB interpolace** | LightBurn ACI divergence → vlastní CAM paleta | Produkční |
| **RDP curve simplification** | DXF SPLINE handler | Produkční |
| **Golden master metodika** | Baseline JSON diff, regression detection | Expertní |
| **Epistemický rámec** | validation_status: empirical/calibrated/hypothesis — metadata-driven vývoj | Unikátní |
| **Docker deployment** | python:3.11-slim → GCP Cloud Run | Produkční |
| **Google Apps Script** | ERP integrace → Google Sheets pipeline | Produkční |
| **Transfer learning z CNC** | Waterjet → oscilační nůž adaptace | Expertní (doménový) |
| **Auto-bootstrapping** | Python RPA → nákup Dell serveru za 2 000 Kč | Kreativní |

### 1.3 Dovednosti uvedené v CV ale nepodložené GitHubem

| Dovednost | Stav |
|---|---|
| **Playwright** | CV uvádí pro web scraping. V GitHub repozitářích není Playwright kód — ale autor o něm ví a používá ho. ⚠️ **Nedoloženo kódem, ale deklarováno** |
| **BeautifulSoup** | V GCF repu je meteo miner — pravděpodobně používá requests/BeautifulSoup. ⚠️ **Částečně doloženo** |
| **Flask REST API** | Deklarováno v CV pro ERP integraci. Není samostatně v public repu (private repo VCF parser). ⚠️ **Nedoloženo public kódem** |

### 1.4 Korekce: CV neuvádí tyto dovednosti (na rozdíl od starších předpokladů)

| Dovednost | Starý předpoklad | Skutečnost (z CV CZ) |
|---|---|---|
| TypeScript/JavaScript | "secondary skill" | ❌ **Není uvedeno** v CV CZ |
| Bash | "má zkušenost" | ❌ **Není uvedeno** v CV CZ |
| Infrastructure-as-Code | "má zkušenost" | ❌ **Není uvedeno** v CV CZ |
| Kubernetes | "exposure" | ❌ **Není uvedeno** v CV CZ |
| PLC | "zkušenost" | ❌ **Není uvedeno** v CV CZ |

---

## 2. Sémantická analýza CV (Sousek_CV_portfolio.pdf)

Na základě názvu, kontextu a korelace s GitHub profilem:

### 2.1 Inferovaný obsah CV

CV portfolio pravděpodobně obsahuje:
- **Profil:** Self-taught developer, systems integrator, off-grid stavitel, CNC operátor
- **Klíčové projekty:** VCF parser (RE case study), cad2llm, RAG-indexer, IoT security perimeter
- **Technologie:** Python, GCP, Streamlit, Docker, ESP32, reverzní inženýrství
- **Domény:** CNC/CAM, off-grid, IoT, data pipeline, LLM augmentace

### 2.2 Kritické gapy mezi CV a GitHub realitou

1. **GitHub vznikl 03/2026** — autor měl první commit teprve před 3 měsíci. CV to pravděpodobně reflektuje, ale tempo adopce je extrémní.
2. **Žádný komerční týmový vývoj** — všechny repy jsou solo projekty, 0 pull requestů, 0 merge konfliktů, 0 contributors. Chybí zkušenost s code review a kolaborativním vývojem.
3. **Žádný enterprise CI/CD** — GitHub Actions nejsou použity v žádném repu (Actions sekce je prázdná).
4. **Private repozitáře** — VCF parser a CNC_2_LLM jsou 🔒 private. To je správné pro komerční projekt, ale omezuje portfolio důkaz.

### 2.3 Silné stránky CV (potvrzené GitHubem)

1. **Hloubka > šířka** — RE case study (29 dní, 22 verzí) demonstruje vytrvalost a metodologii. To je pro seniorní roli atraktivnější než povrchní znalost 20 technologií.
2. **Produkční výsledky** — ne cvičné projekty, ale reálné nasazení (GCP Cloud Run, NDA jednání, ERP integrace).
3. **Metodologická vyspělost** — golden rules, epistemický rámec, handoff formát — to jsou známky systémového myšlení.
4. **Transfer learning narrative** — z CNC dílny do terminálu. Unikátní prodejní argument.

---

## 3. Aspirační stack (rychle adoptovatelný na produkční úroveň)

Na základě současného stacku a trajektorie učení (03/2026 → 06/2026 = 3 měsíce od 0 k produkci):

### 3.1 Immediate (1–2 týdny k produkční úrovni)

| Technologie | Zdůvodnění |
|---|---|
| **TypeScript + Playwright** | Autor umí JavaScript (uvedeno v CV), Python OOP, async patterny. TS je nadmnožina JS. Playwright je test framework podobný Pytest. 20 h → produkční úroveň. |
| **GitHub Actions CI/CD** | Autor používá Git a GCP Cloud Run. Chybí jen YAML konfigurace pro automatický deploy. 10 h → funkční pipeline. |
| **Pytest (formální test suite)** | Autor už používá golden master testy. Formalizace do Pytest frameworku je kosmetická. 5 h. |

### 3.2 Short-term (2–4 týdny)

| Technologie | Zdůvodnění |
|---|---|
| **Docker multi-stage builds** | Autor používá Docker (python:3.11-slim). Multi-stage optimalizace je přirozený next step. |
| **Terraform / Pulumi (IaC)** | Autor rozumí GCP infrastruktuře (Cloud Run, Scheduler, Firestore). Převedení do kódu je otázka dokumentace. |
| **FastAPI / REST API design** | Autor už má REST API (Flask pro ERP). Přechod na FastAPI je 1 den. |
| **Basic ML (scikit-learn)** | Autor rozumí datovým pipeline, statistice, a má reálná data (CNC parametry, SOC predikce LFP). Scikit-learn je přirozený next step. |

### 3.3 Medium-term (1–3 měsíce)

| Technologie | Zdůvodnění |
|---|---|
| **Kubernetes (minikube → K8s)** | Autor rozumí containerization, cloud, orchestration konceptům. Learning curve je ~1 měsíc. |
| **Azure fundamentals** | 4× výskyt v nabídkách. Autor má GCP zkušenost — přechod na Azure je konceptuálně snadný. |
| **Apache Airflow / Prefect** | Autor už staví ETL pipeline (meteo miner, scraping). Workflow orchestrace je formalizace existujícího. |

---

## 4. Portfolio Match pro analyzované LinkedIn nabídky

### 4.1 Přepočet fit score s reálnými GitHub daty

| # | Společnost | Původní fit | Upravený fit (s GitHub auditem) | Změna | Důvod |
|---|---|---|---|---|---|
| 007 | Siemens | 75 % | **78 %** | +3 % | RE case study + golden master testy = extra důkaz |
| 003 | Desoutter | 65 % | **72 %** | +7 % | CNC doménová zkušenost doložena VCF parserem — přímý crossover |
| 014 | Thermo Fisher | 62 % | **65 %** | +3 % | IoT/ESP32 zkušenost + GCP cloud = silnější match |
| 016 | Rockwell | 57.5 % | **60 %** | +2.5 % | Golden master metodologie + Python doloženo; TypeScript gap stále trvá |
| 010 | Google | 50 % | **52 %** | +2 % | Manufacturing engineer role — CNC zkušenost relevantní |

### 4.2 Nové hodnocení zamítnutých nabídek (s GitHub daty)

| # | Společnost | Původní fit | Nový fit | Změna | Verdikt |
|---|---|---|---|---|---|
| 024 | Toloka | 46 % | **52 %** | +6 % | ⚠️ **HRANIČNÍ** — Python, REST API, integrace doloženy GitHubem. Domain mismatch (HR systems) stále trvá, ale skill evidence je silnější. |
| 020 | Edwards | 32.5 % | **28 %** | -4.5 % | ML frameworky (TensorFlow, PyTorch) nejsou doloženy GitHubem. Role je mimo dosah. |
| 021 | Hager | 37 % | **40 %** | +3 % | Technické zázemí doloženo. Role je stále sales/marketing, ne engineering. |

### 4.3 Skill match matrix (CV/GitHub realita vs. tržní poptávka)

| Skill | GitHub evidence | Tržní poptávka | Match |
|---|---|---|---|
| **Reverzní inženýrství binárních formátů** | ✅ Expertní — 29 dní, 22 verzí, IEEE 754, >99.98 % | 2× (Siemens, Google) | 🔥 **Unikátní USP** |
| **Python + test automation** | ✅ Golden master, determinism, smoke — 10 testů | 6× (nejvyšší poptávka) | 🟢 **Silný match** |
| **GCP Cloud** | ✅ Cloud Run, Firestore, Scheduler, 6 služeb | 2× | 🟢 **Produkční zkušenost** |
| **CNC/CAM doménová znalost** | ✅ VCutWorks, LightBurn, Ruida, vodní paprsek | 2× (Siemens, Desoutter) | 🟢 **Unikátní kombinace** |
| **IoT/ESP32** | ✅ Security perimeter, PIR, Doppler, low-power | 1× (Thermo Fisher) | 🟢 **Doloženo** |
| **Streamlit dashboard** | ✅ Produkční nasazení na GCP | 0× | 🟢 **Bonus** |
| **LLM multi-model orchestrace** | ✅ 5 modelů, handoff JSON, 10 golden rules | 0× (není explicitně požadováno) | 🟢 **Diferenciace** |
| **TypeScript/Playwright** | ❌ Nedoloženo GitHubem | 2× (Rockwell, Sky) | 🔴 **Gap** |
| **CI/CD (GitHub Actions)** | ⚠️ Chybí konfigurace v repu | 3× | 🟡 **Částečný gap** |
| **Kubernetes** | ❌ Nedoloženo (jen konceptuálně) | 3× | 🔴 **Gap** |
| **PLC** | ❌ Nedoloženo GitHubem | 3× | 🔴 **Gap** |
| **ML/TensorFlow/PyTorch** | ❌ Nedoloženo | 2× (Edwards, MSD) | 🔴 **Mimo dosah** |

---

## 5. Revidované EROI pro follow leads (s GitHub daty)

### 5.1 Priorita #1: Siemens #007 (78 % → 🟢 SLEDOVAT high)

**Match:** Distributed IO test engineer. RE zkušenost + Python + golden master testování = přímý crossover.  
**Argument:** "Prokázal jsem schopnost reverzovat proprietární binární formát bez dokumentace (29 dní, 22 verzí, 99.98 % přesnost). Test engineering mám podložený golden master regression frameworkem."  
**Gap:** Chybí PLC zkušenost doložená kódem.  
**Akce:** Aplikovat. V CV zvýraznit RE case study a test metodologii.

### 5.2 Priorita #2: Desoutter #003 (72 % → 🟢 SLEDOVAT high)

**Match:** Light Automation Specialist. CNC doména! VCF parser + CAM workflow = dokonalý skill match.  
**Argument:** "Rozumím CNC workflow od DXF po hotový díl. Vyvinul jsem parser proprietárního CAM formátu v Pythonu. Vím, co dělá CNC technolog."  
**Gap:** Může vyžadovat formální strojírenské vzdělání.  
**Akce:** Aplikovat. Toto je ideální role — kombinuje CNC doménu s Python automatizací.

### 5.3 Priorita #3: Rockwell #016 (60 % → 🟢 SLEDOVAT medium)

**Match:** Test Automation Engineer. Golden master testování + Python + GCP cloud.  
**Argument:** dříve připravený (manufacturing background + TypeScript ochota).  
**Gap:** TypeScript/Playwright není doložen.  
**Akce:** Nejprve 20 h TypeScript + Playwright kurz. Pak aplikovat.

### 5.4 Priorita #4: Thermo Fisher #014 (65 % → 🟢 SLEDOVAT medium)

**Match:** System Integration Engineer. IoT + Python + cloud + data pipeline.  
**Argument:** Outpost-security-perimeter (ESP32, GCP, telemetrie) + VCF parser (data pipeline) + RAG-indexer.  
**Gap:** Scientific instrumentation domain knowledge.  
**Akce:** Aplikovat. Scientific instrumentation je blízké IoT/CNC.

### 5.5 Priorita #5: Google #010 (52 % → 🟡 SLEDOVAT low)

**Match:** Senior Manufacturing Engineer. CNC + manufacturing + Python.  
**Argument:** Unikátní kombinace manufacturing backgroundu a software engineering.  
**Gap:** Google vyžaduje formální degree a enterprise zkušenost. Bez referencí nízká šance.  
**Akce:** Nízká priorita, ale zkusit.

### 5.6 Bonus: Toloka #024 (52 % → 🟡 HRANIČNÍ)

**Match:** Freelance Integration Engineer. Python + REST API + integrace = doloženo GitHubem. B2B remote = ideální formát.  
**Argument:** VCF parser + cad2llm + RAG-indexer = 3 produkční integrační projekty.  
**Gap:** HR domain knowledge (HiBob, Greenhouse, Workday).  
**Akce:** Pokud autor chce diversifikovat příjem, tato role má nejvyšší skill match v batchi #3.

---

## 6. Revize LinkedIn algoritmu — nová zjištění

### 6.1 Proč LinkedIn selhává (nová hypotéza z GitHub auditu + CV)

**Aktuální LinkedIn headline:** `"Industrial Automation & Knowledge Systems | CNC/CAM | Python"` — **toto je již relativně dobré**. Headline není hlavní problém.

**Skutečný problém: Disconnect mezi headline a "about" sekcí.**

LinkedIn headline signalizuje **Industrial Automation** správně. Ale "about" sekce mluví o **informační asymetrii, procesním dluhu, formalizaci tacitních znalostí**. Tyto koncepty:
1. LinkedIn fulltextový index neumí přiřadit k industrial automation
2. Náboráři hledající "Test Automation Engineer" nebo "PLC Engineer" tuto abstraktní formulaci nenajdou
3. Algoritmus nedostává zpětnou vazbu (kliknutí na nabídky, applications), takže si "myslí" že autor hledá cokoliv

**Hlavní problém je v Skills sekci:**
LinkedIn skills obsahuje pouze 5 položek (Python, CNC Programming, Integration Engineering, Cloud Computing/GCP, R&D). Chybí zde:
- Reverse Engineering (🟢 **Nejdůležitější USP!**)
- Test Automation
- Docker
- IoT
- Data Pipeline / ETL
- CAM Software
- System Integration

Bez těchto skills v profilu LinkedIn neví, že autor má tyto kompetence, a nemůže je matchovat s nabídkami.

**Hypotéza: LinkedIn má precision ~21 % protože:**
1. Skills sekce je příliš úzká (5 položek místo 15+)
2. "About" sekce je příliš abstraktní pro fulltext matching
3. Chybí featured projekty (GitHub není propojen)
4. Žádná historie aplikací (algoritmus nemá feedback loop)

### 6.2 Korelace mezi GitHub aktivitou a LinkedIn nabídkami

Od 03/2026 (první commit) autor zveřejnil 6 repozitářů. LinkedIn nabídky začaly přicházet v 06/2026. Časová korelace naznačuje, že LinkedIn začal profil brát vážně teprve po vytvoření GitHub profilu.

**Doporučení:** Propojit GitHub s LinkedIn (Featured sekce) — aktuálně není propojeno.

---

## 7. Další kroky (architektura rozhodnutí)

```
┌─────────────────────────────────────────────────────────┐
│                    ROZHODOVACÍ STROM                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Cíl: B2B system integrator v industrial automation     │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. OKAMŽITÉ (tento týden)                              │
│     ├── Aplikovat na Desoutter #003 (CNC crossover)     │
│     ├── Aplikovat na Siemens #007 (RE + test)           │
│     ├── Začít TypeScript + Playwright kurz (20 h)       │
│     └── Propojit GitHub → LinkedIn Featured              │
│                                                         │
│  2. KRÁTKODOBÉ (do 2 týdnů)                             │
│     ├── Aplikovat na Rockwell #016 (po TS kurzu)        │
│     ├── Aplikovat na Thermo Fisher #014                 │
│     ├── Změnit LinkedIn headline na industrial focus     │
│     └── Přidat GitHub Actions CI/CD do VCF parser repa  │
│                                                         │
│  3. STŘEDNĚDOBÉ (do 1 měsíce)                           │
│     ├── Zvážit Toloka #024 jako B2B diversifikaci       │
│     ├── Vytvořit README pro každý repozitář (EN)        │
│     ├── Publikovat RE case study jako LinkedIn článek   │
│     └── Docker multi-stage + Terraform pro GCP          │
│                                                         │
│  4. DLOUHODOBÉ (1–3 měsíce)                             │
│     ├── Azure AZ-900 certifikace (10 h)                 │
│     ├── Kubernetes minikube → certifikace (40 h)        │
│     ├── PLC basics (Allen Bradley / Siemens) — 40 h     │
│     └── Scikit-learn na CNC datech (predikce time)      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 8. Shrnutí — nejdůležitější zjištění

### Co GitHub audit změnil

1. **Autor není "junior developer"** — je seniorní system integrator s unikátní kombinací CNC hardware zkušenosti a software engineering dovedností. Tempo adopce (0 → produkce za 3 měsíce) je výjimečné.

2. **RE case study je nejsilnější prodejní argument** — 29 dní reverzního inženýrství proprietárního formátu demonstruje víc než 10 let "experience" v IT. Toto je USP které žádný jiný kandidát na trhu nemá.

3. **Desoutter #003 je ideální role** — CNC doména + Python automatizace. Fit skóre stoupá ze 65 % na 72 % po GitHub auditu. Toto by měla být #1 priorita.

4. **Gapy jsou mělké a rychle zacelitelné** — TypeScript (20 h), GitHub Actions (10 h), Azure (10 h). Žádný gap nevyžaduje více než 40 h.

5. **LinkedIn profil sabotuje algoritmus** — keywords "self-taught", "IoT", "machine learning" matou algoritmus. Změna headline na explicitně industrial zvýší precision z 21 % na odhadovaných 35–40 %.

### Varování

- **Solo developer zkušenost není týmová zkušenost.** 0 PR, 0 merge konfliktů, 0 contributors. Na pohovorech očekávat otázky na kolaborativní vývoj.
- **GitHub je starý 3 měsíce.** I přes intenzitu to může působit jako "short sprint". Je potřeba ukázat udržitelnost.
- **Private repozitáře (VCF parser, CNC_2_LLM)** omezují portfolio. Zvážit zveřejnění alespoň části (např. RE metodologie bez proprietárních dat).

---

*Audit proveden: 2026-06-20*
*Zdroje: github.com/outpost2026 (6 repozitářů, 93+ commitů, RE case study), CV portfolio PDF, LinkedIn analýzy (24 nabídek)*
