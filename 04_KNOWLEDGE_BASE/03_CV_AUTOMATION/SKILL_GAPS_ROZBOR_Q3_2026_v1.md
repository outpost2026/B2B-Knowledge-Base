# SKILL GAPS: Rozbor identifikovaných mezer v autorově stacku pro Q3+ 2026

**Datum:** 2026-08-06 | **Autor:** outpost2026
**Účel:** Strukturovaný rozbor 4 identifikovaných skill gapů — co je, proč se to poptává, kde se to používá, glossary, ontologie, praktické příklady
**Kontext:** Autor dosud nezná tyto domény — dokument slouží jako úvod a praktický průvodce
**Zdroje:** Live GitHub audit (2026-08-06), LinkedIn analýzy (24 nabídek), EROI plán v2.0
**Provenance:** Summary (zdroj: tržní analýza + technologický průzkum)

---

## Executive Summary

Z 24 analyzovaných LinkedIn nabídek a live GitHub auditu (14+ repů, 3 MCP servery) se identifikovaly **4 kritické mezery** v autorově stacku. Tyto mezery přímo blokují přístup k 35–45 % analyzovaných rolí.

| # | Gap | EROI | Čas | Blokuje |
|:-:|-----|:----:|:---:|---------|
| ❶ | TypeScript + Playwright | 8/10 | 15–20 h | Rockwell, Sky (2×) |
| ❷ | AZ-900 Azure Fundamentals | 7.5/10 | 10–15 h | Azure role (4×) |
| ❸ | PLC Basics & Industrial Protocols | 5.5/10 | 40–60 h | Siemens, Rockwell (3×) |
| ❹ | Kubernetes | 4/10 | 40+ h | Enterprise role (3×) |

**Autorův kontext:** Autor je systémový integrátor s hlubokou doménou CNC/CAM, expertním Python stackem a 3 MCP servery. Tyto gapy nejsou "chybějící základy" — jsou to **specifické nástroje**, které otevírají dveře k vysoce placeným rolím v industrial automation a enterprise IT.

---

## ❶ TypeScript + Playwright

### 1.1 Co je TypeScript

TypeScript (TS) je **typový nadmnožinový jazyk** postavený nad JavaScriptem (JS). Přidává statický typový systém, který se při kompilaci převádí do čistého JS. TS byl vyvinut společností Microsoft a je standardem pro velké frontendové i backendové projekty.

**Klíčový insight pro autora:** TS ≠ nový jazyk. TS = JS + typy. Autor umí Python OOP → TS interfaces, generics, type narrowing jsou koncepčně identické s Python typing + dataclasses.

#### Ontologie TypeScript

```
TypeScript
├── Typový systém
│   ├── Interfaces (analogie: Python Protocol/ABC)
│   ├── Type aliases (analogie: Python TypeVar)
│   ├── Generics (analogie: Python TypeVar + Generic)
│   ├── Union types (analogie: Python Union[])
│   ├── Type narrowing (analogie: Python isinstance())
│   └── Utility types (Partial, Pick, Omit, Record)
├── Async/await
│   ├── Promises (analogie: Python asyncio)
│   ├── async/await syntax (analogie: Python async/await)
│   └── Promise.all / Promise.race (analogie: asyncio.gather)
├── Module system
│   ├── ES modules (import/export)
│   ├── CommonJS (require/module.exports)
│   └── npm/yarn/pnpm package management
├── Runtime
│   ├── Node.js (server-side, analogie: Python CPython)
│   ├── Deno (alternativa k Node.js)
│   └── Bun (rychlejší alternativa)
└── Tooling
    ├── tsconfig.json (konfigurace překladu)
    ├── tsc (TypeScript compiler)
    └── ESLint + Prettier (linting + formatting)
```

### 1.2 Co je Playwright

Playwright je **framework pro automatizaci prohlížeče** vyvinutý Microsoftem. Umožňuje programově ovládat Chromium, Firefox a WebKit — testovat webové aplikace, scrapovat data, automatizovat interakce s webovými stránkami.

**Analogie pro autora:** Playwright = Python Playwright/Selenium, ale nativně v TS/JS s lepší typovou podporou a paralelním během.

#### Ontologie Playwright

```
Playwright
├── Browser management
│   ├── chromium, firefox, webKit (3 enginey)
│   ├── headless / headed mode
│   └── browser context (izolované sessiony)
├── Page interaction
│   ├── Locators (getByRole, getByText, getByTestId)
│   ├── Actions (click, fill, press, selectOption)
│   ├── Assertions (toBeVisible, toHaveText, toHaveValue)
│   └── Wait mechanisms (waitForSelector, waitForLoadState)
├── Test structure
│   ├── test() / test.describe() (analogie: pytest test / class)
│   ├── beforeEach / afterEach hooks
│   ├── Fixtures (sdílené zdroje mezi testy)
│   └── expect() assertions
├── Advanced
│   ├── Page Object Model (POM) — struktura testů
│   ├── API testing (APIRequestContext)
│   ├── Tracing (nahrávání průběhu testu)
│   └── Visual comparison (screenshot diff)
└── CI integration
    ├── GitHub Actions
    ├── Azure DevOps
    └── Parallel test execution
```

### 1.3 Proč se to poptává (tržní kontext)

| Důvod | Vysvětlení |
|-------|-----------|
| **Playwright = standard pro test automation** | GitHub Actions + Playwright = nejčastější kombinace v job nabídkách pro test enginery |
| **TypeScript = dominantní jazyk pro frontend** | React, Angular, Vue — vše píše v TS. Firma whichá frontend = potřebuje TS |
| **Playwright = náhrada za Selenium** | Selenium je legacy, Playwright je modernější, rychlejší, spolehlivější |
| **Cross-platform** | Playwright testuje na 3 enginech = 1 napsaný test běží na Chromium, Firefox, WebKit |
| **Integrace s CI/CD** | Playwright má nativní podporu pro GitHub Actions, Azure DevOps, Jenkins |

### 1.4 Kde se to používá (praktické příklady)

#### Příklad 1: Testování webového dashboardu
```
Firma má Streamlit/FastAPI dashboard.
Playwright: spustí prohlížeč → načte stránku → ověří že tlačítko "Export" existuje
→ klikne na něj → stáhne soubor → ověří obsah.
Celý test = 20 řádků TS kódu. Běží v CI na každém pushi.
```

#### Příklad 2: Web scraping CNC portálů
```
Firma potřebuje sbírat ceny nástrojů z CNC e-shopů.
Playwright: otevře stránku → vyplní formulář → klikne "Hledat"
→ parsne výsledky → uloží do JSON.
Alternativa k Python requests/BS4, ale s podporou JavaScript rendering.
```

#### Příklad 3: E2E testování B2B aplikace
```
Moodpasta dashboard: Playwright simuluje uživatele.
1. Otevře stránku
2. Nahraje VCF soubor
3. Ověří že se zobrazí geometrie
4. Klikne "Export CSV"
5. Ověří že CSV obsahuje správné sloupce
= Regresní test celého workflow.
```

#### Příklad 4: Autorovo využití
```
Autorův Vcf-compiler má Streamlit dashboard na GCP Cloud Run.
Playwright test: ověří že dashboard se načte → nahraje VCF → ověří vizualizaci
→ klikne export → ověří soubor. Běží v GitHub Actions na každém pushi.
= Golden master test + E2E test = kompletní regresní pokrytí.
```

### 1.5 Přínos pro autora

| Přínos | Dopad |
|--------|-------|
| **Odemkne Rockwell-like role** | 2× výskyt v nabídkách = 2 konkrétní příležitosti |
| **Posílí test automation** | Golden master + Playwright = kompletní test stack |
| **E2E testy pro Streamlit dashboard** | Regresní testování B2B produktu |
| **Cross-platform scraping** | Alternativa k Python playwright pro JS-renderované stránky |
| **CI/CD integrace** | Playwright v GitHub Actions = automatické E2E testy |

### 1.6 Glossary

| Termín | Definice |
|--------|----------|
| **TypeScript (TS)** | Typový nadmnožinový jazyk nad JavaScriptem, překládá se do JS |
| **JavaScript (JS)** | Skriptovací jazyk pro prohlížeče a Node.js |
| **Interface** | Definice struktury objektu (analogie: Python Protocol) |
| **Generic** | Parametrický typ (analogie: Python TypeVar) |
| **Type narrowing** | Omezení typu v běhu (analogie: Python isinstance) |
| **async/await** | Syntaktický cukr pro asynchronní kód (analogie: Python async/await) |
| **Promise** | Objekt reprezentující budoucí výsledek (analogie: Python asyncio.Future) |
| **Node.js** | Runtime pro JS na serveru (analogie: Python CPython) |
| **npm** | Package manager pro Node.js (analogie: pip) |
| **Playwright** | Framework pro automatizaci prohlížeče |
| **Headless mode** | Prohlížeč bez grafického rozhraní (pro CI/CD) |
| **Locator** | Způsob nalezení prvku na stránce (getByRole, getByText) |
| **Page Object Model (POM)** | Design pattern pro strukturu testů |
| **Fixture** | Sdílený zdroj mezi testy (analogie: pytest fixtures) |
| **E2E test** | End-to-end test = test celého workflow od A do Z |
| **Regression test** | Test který ověřuje že se staré věci nerozbily |
| **CI/CD** | Continuous Integration / Continuous Deployment |

---

## ❷ AZ-900 Azure Fundamentals

### 2.1 Co je AZ-900

AZ-900 je **základní certifikace od Microsoftu** pro cloudovou platformu Azure. Není to technická certifikace — je to **konceptuální certifikace** která ověřuje že kandidát rozumí cloudovým konceptům, službám Azure a správě governance.

**Klíčový insight pro autora:** Autor už zná GCP (Cloud Run, Firestore, Scheduler). AZ-900 = převod GCP znalostí na Azure terminologii. Cloud = cloud, jen se to jinak jmenuje.

#### Ontologie AZ-900

```
AZ-900 Azure Fundamentals
├── Cloud Concepts (20-25 % zkoušky)
│   ├── Cloud computing definice
│   ├── CAPEX vs OPEX (Capital vs Operational expenditure)
│   ├── Cloud service models
│   │   ├── IaaS (Infrastructure as a Service) — virtuální stroje
│   │   ├── PaaS (Platform as a Service) — App Service, Cloud Run
│   │   └── SaaS (Software as a Service) — Microsoft 365, Gmail
│   ├── Cloud deployment models
│   │   ├── Public cloud (Azure, GCP, AWS)
│   │   ├── Private cloud (Azure Stack, on-premises)
│   │   └── Hybrid cloud (Azure Arc)
│   └── Výhody cloudu: HA, Scalability, Elasticity, Agility, DR
│
├── Azure Architecture & Services (35-40 %)
│   ├── Regions & Availability Zones
│   │   ├── Region = geografická oblast (analogie: GCP region)
│   │   ├── Availability Zone = datacentrum v regionu
│   │   └── Paired regions = pro disaster recovery
│   ├── Resource Groups
│   │   └── Logická skupina zdrojů (analogie: GCP Project)
│   ├── Compute
│   │   ├── Virtual Machines (analogie: GCP Compute Engine)
│   │   ├── App Service (analogie: GCP Cloud Run)
│   │   ├── Azure Container Instances (ACI) (analogie: GCP Cloud Run)
│   │   ├── Azure Kubernetes Service (AKS) (analogie: GKE)
│   │   └── Azure Functions (analogie: GCP Cloud Functions)
│   ├── Storage
│   │   ├── Blob Storage (analogie: GCP Cloud Storage)
│   │   ├── Disk Storage (analogie: GCP Persistent Disk)
│   │   ├── File Storage (analogie: GCP Filestore)
│   │   └── Queue Storage (analogie: GCP Pub/Sub)
│   ├── Networking
│   │   ├── Virtual Network (VNet) (analogie: GCP VPC)
│   │   ├── Load Balancer (analogie: GCP Load Balancing)
│   │   └── VPN Gateway (analogie: GCP Cloud VPN)
│   └── Databases
│       ├── Azure SQL Database (analogie: GCP Cloud SQL)
│       ├── Cosmos DB (analogie: GCP Firestore/Datastore)
│       └── Azure Database for PostgreSQL/MySQL
│
├── Azure Management & Governance (30-35 %)
│   ├── Azure AD (Active Directory)
│   │   └── Identity management (analogie: GCP IAM)
│   ├── RBAC (Role-Based Access Control)
│   │   └── Přístupová práva (analogie: GCP IAM roles)
│   ├── Azure Policy
│   │   └── Compliance rules (analogie: GCP Organization Policy)
│   ├── Cost Management
│   │   └── Fakturace, rozpočty, alerts
│   ├── Azure Monitor
│   │   └── Logging, metrics, alerts (analogie: GCP Cloud Monitoring)
│   └── Compliance
│       └── GDPR, ISO, NIST, SOC
│
└── Zkouška
    ├── 45 minut, 30-40 otázek
    ├── Score: 700/1000 = pass
    ├── Online proctored (z domova)
    └── Platnost: 1 rok (renewal zdarma)
```

### 2.2 Proč se to poptává (tržní kontext)

| Důvod | Vysvětlení |
|-------|-----------|
| **Azure = #2 cloud provider** | Po AWS je Azure největší cloud. Mnoho firem používá Azure místo GCP |
| **Certifikace = filtr v HR** | Mnoho firem filtruje kandidáty podle certifikací. AZ-900 je gatekeeper |
| **4× výskyt v analyzovaných nabídkách** | Rockwell, Thermo Fisher, Siemens — všechny mají Azure v tech stacku |
| **Hybridní cloud** | Azure má nejsilnější hybridní řešení (Azure Arc, Azure Stack). Průmyslové firmy = hybridní |
| **Microsoft ekosystém** | Office 365, Active Directory, Teams — firmy whiché Microsoft = potřebují Azure |
| **Gateway k dalším certifikacím** | AZ-900 → AZ-104 (Admin) → AZ-400 (DevOps) → AZ-204 (Developer) |

### 2.3 Kde se to používá (praktické příklady)

#### Příklad 1: Hybridní cloud v průmyslu
```
Výrobní firma má:
- On-premises: PLC, SCADA, historická data (10 let)
- Azure: nové aplikace, AI modely, reporting
- Azure Arc: správa on-premises zdrojů z Azure portalu
- Azure IoT Hub: sběr dat z čidel na strojích

AZ-900 dává kontext: proč firma používá hybridní cloud
místo přesunu všeho do veřejného cloudu.
```

#### Příklad 2: CI/CD pipeline na Azure DevOps
```
Firma má aplikaci nasazenou na Azure App Service.
Pipeline: Azure DevOps → Build → Test → Deploy na App Service
= Analogie: GitHub Actions → Build → Test → Deploy na Cloud Run

AZ-900: porozumění Azure DevOps jako CI/CD platformě.
```

#### Příklad 3: IoT data pipeline
```
Senzory na CNC stroji → Azure IoT Hub → Azure Stream Analytics
→ Azure Cosmos DB → Power BI dashboard

AZ-900: porozumění jednotlivým službám a proč se používají.
Autor už toto dělá v GCP (Cloud IoT → BigQuery → Looker).
AZ-900 = ekvivalentní knowledge pro Azure.
```

#### Příklad 4: Autorovo využití
```
Autor má GCP Cloud Run deployment.
AZ-900: naučit se ekvivalentní Azure služby.
- Cloud Run → App Service / Container Instances
- Firestore → Cosmos DB
- Cloud Scheduler → Azure Logic Apps
- Cloud Storage → Blob Storage

Při pohovoru: "Mám GCP zkušenost. AZ-900 mi dá kontext
pro přechod na Azure, pokud firma používá Microsoft ekosystém."
```

### 2.4 Přínos pro autora

| Přínos | Dopad |
|--------|-------|
| **Odemkne Azure role (4×)** | 4 konkrétní příležitosti z 24 analyzovaných |
| **Certifikace = důkaz** | LinkedIn Licenses & Certifications = viditelný signál |
| **GCP → Azure transfer** | Autor už zná cloud = přechod je jen přejmenování terminologie |
| **Hybridní cloud kontext** | Průmyslové firmy = hybridní. AZ-900 dává framework |
| **Gateway k AZ-104/AZ-400** | AZ-900 je první krok k pokročilejším certifikacím |

### 2.5 Glossary

| Termín | Definice | GCP analogie |
|--------|----------|-------------|
| **Azure** | Cloudová platforma od Microsoftu | GCP (Google Cloud Platform) |
| **AZ-900** | Základní certifikace pro Azure | Google Cloud Digital Leader |
| **IaaS** | Infrastructure as a Service — virtuální stroje | Compute Engine |
| **PaaS** | Platform as a Service — hosting bez správy infrastruktury | Cloud Run, App Engine |
| **SaaS** | Software as a Service — hotový software (Gmail, Office 365) | Google Workspace |
| **Region** | Geografická oblast s datacentry | GCP Region |
| **Availability Zone** | Datacentrum v regionu | GCP Zone |
| **Resource Group** | Logická skupina Azure zdrojů | GCP Project |
| **Azure AD** | Identity a access management | GCP IAM |
| **RBAC** | Role-Based Access Control | GCP IAM Roles |
| **Virtual Machine** | Virtuální počítač v cloudu | Compute Engine |
| **App Service** | Hosting webových aplikací (PaaS) | Cloud Run |
| **Container Instances** | Spouštění kontejnerů bez orchestrace | Cloud Run |
| **AKS** | Azure Kubernetes Service | GKE |
| **Blob Storage** | Objektové úložiště (soubory, obrázky) | Cloud Storage |
| **Cosmos DB** | Globálně distribuovaná NoSQL databáze | Firestore |
| **Azure SQL** | Spravovaná SQL databáze | Cloud SQL |
| **VNet** | Virtuální síť v Azure | VPC |
| **Load Balancer** | Rozložení zátěže mezi servery | Cloud Load Balancing |
| **Azure Monitor** | Logging a metriky | Cloud Monitoring |
| **Azure Policy** | Compliance pravidla | Organization Policy |
| **Cost Management** | Správa nákladů na cloud | Billing & Budgets |
| **Azure Arc** | Správa hybridních/zdrojů mimo Azure | Anthos |
| **Azure DevOps** | CI/CD platforma od Microsoftu | GitHub Actions |
| **Power BI** | BI nástroj od Microsoftu | Looker, Data Studio |
| **IoT Hub** | Brána pro IoT zařízení | Cloud IoT Core |
| **CAPEX** | Capital Expenditure — investice do hardware | — |
| **OPEX** | Operational Expenditure — provozní náklady (cloud) | — |
| **DR** | Disaster Recovery — zotavení po havárii | — |
| **HA** | High Availability — vysoká dostupnost | — |

---

## ❸ PLC Basics & Industrial Protocols

### 3.1 Co je PLC

PLC (Programmable Logic Controller) je **průmyslový počítač** navržený pro řízení automatizovaných procesů — výrobní linky, čerpadla, ventily, motory, senzory. PLC je srdce každého průmyslového automatu.

**Klíčový insight pro autora:** Autor zná CNC stroje = ví co PLC dělá (řídí pohyb, čte senzory). PLC = programovatelný reléový ovladač. Autorův G-code = instrukce pro CNC. PLC program = instrukce pro řízení celého provozu.

#### Ontologie PLC

```
PLC (Programmable Logic Controller)
├── Hardware
│   ├── CPU modul (procesor + paměť)
│   ├── I/O moduly
│   │   ├── Digital Input (DI) — binární vstupy (tlačítko, senzor)
│   │   ├── Digital Output (DO) — binární výstupy (relé, motor ON/OFF)
│   │   ├── Analog Input (AI) — spojité hodnoty (teplota, tlak, proud)
│   │   └── Analog Output (AO) — spojité výstupy (rychlost motoru)
│   ├── Napájecí modul
│   ├── Komunikační modul (Ethernet, PROFINET, Modbus)
│   └── Backbone (sběrnice propojující moduly)
│
├── Programování (IEC 61131-3)
│   ├── Ladder Diagram (LD) — grafický, vypadá jako elektrický schéma
│   │   ├── Relays (NO/NC kontakty)
│   │   ├── Coils (výstupy)
│   │   ├── Timers (TON, TOF, TP)
│   │   ├── Counters (CTU, CTD)
│   │   └── Comparators (EQU, GRT, LES)
│   ├── Structured Text (ST) — textový, vypadá jako Pascal
│   │   ├── IF-THEN-ELSE
│   │   ├── CASE OF
│   │   ├── FOR / WHILE loops
│   │   └── FUNCTION / FUNCTION_BLOCK
│   ├── Function Block Diagram (FBD) — grafický, bloky propojené signály
│   ├── Instruction List (IL) — assembly-like (zastaralý)
│   └── Sequential Function Chart (SFC) — stavový automat
│
├── Komunikační protokoly
│   ├── Modbus TCP/RTU
│   │   ├── Master/Slave architektura
│   │   ├── Holding Registers (16-bit data)
│   │   ├── Coils (binární výstupy)
│   │   └── Input Registers (read-only data)
│   ├── PROFINET
│   │   ├── Real-time Ethernet
│   │   ├── Device classes (RT, IRT)
│   │   └── Topologie (star, line, ring)
│   ├── EtherCAT
│   │   ├── High-speed industrial Ethernet
│   │   ├── Master/Slave
│   │   └── Distribuované hodiny
│   ├── OPC UA
│   │   ├── Platform-independent data exchange
│   │   ├── Client/Server model
│   │   └── Bezpečnost (certifikáty, šifrování)
│   └── MQTT
│       ├── Publish/Subscribe model
│       ├── Lehký protokol pro IoT
│       └── Broker (Mosquitto, Azure IoT Hub)
│
├── Scan Cycle (cyklus PLC)
│   ├── 1. Read Inputs (čtení vstupů)
│   ├── 2. Execute Program (spuštění programu)
│   ├── 3. Write Outputs (zápis výstupů)
│   └── 4. Housekeeping (komunikace, diagnostika)
│   └── Typická doba: 1-100 ms
│
└── Výrobci
    ├── Siemens (S7-1200, S7-1500, TIA Portal) — dominantní v Evropě
    ├── Rockwell/Allen-Bradley (ControlLogix, CompactLogix) — dominantní v USA
    ├── Mitsubishi (FX, Q series) — dominantní v Asii
    ├── Schneider Electric (Modicon M580) — silný v energetice
    └── Beckhoff (CX series, TwinCAT) — PC-based PLC
```

### 3.2 Proč se to poptává (tržní kontext)

| Důvod | Vysvětlení |
|-------|-----------|
| **PLC = srdce průmyslové automatizace** | Každá výrobní linka, potrubi, dopravník = řízeno PLC |
| **3× výskyt v analyzovaných nabídkách** | Siemens, Rockwell, Thermo Fisher — všechny hledají PLC zkušenosti |
| **PLC + Python = unikátní kombinace** | Málo lidí umí obojí. Autor = CNC expert → PLC je přirozený next step |
| **Industry 4.0 = PLC + IT** | Průmysl 4.0 = propojení PLC (OT) s IT systémy. Autor = přesně tento most |
| **SCADA/MES integrace** | PLC sbírá data → SCADA zobrazuje → MES řídí výrobu. Autor = integrace |
| **Legacy systems** | Většina průmyslu běží na starších PLC. Potřeba lidí kteří je rozumí |

### 3.3 Kde se to používá (praktické příklady)

#### Příklad 1: Řízení výrobní linky
```
PLC (Siemens S7-1500) řídí:
- Dopravník (motor ON/OFF, rychlost)
- Čidlo přítomnosti (DI: materiál dorazil?)
- Vřeteno frézy (AO: otáčky 12000 RPM)
- Chladicí kapalina (DO: čerpadlo ON)
- Bezpečnostní senzory (DI: otevřený kryt? → STOP)

Ladder program: IF (tlačítko START) AND (safety OK) THEN (motor ON)
= Autor zná G-code. Ladder = analogický koncept pro řízení celého provozu.
```

#### Příklad 2: Sběr dat z PLC do Python
```
Python skript (pymodbus) → čte Modbus registry z PLC:
- Holding Register 100: teplota (float16)
- Holding Register 101: proud motoru (float16)
- Coil 50: stav čerpadla (ON/OFF)

Data → Google Sheets / Cloud Firestore / Power BI
= Autor už dělá ETL z VCF do GSheets. PLC = další zdroj dat.
```

#### Příklad 3: SCADA dashboard
```
PLC → OPC UA server → SCADA klient (WinCC, Ignition)
- Zobrazuje aktuální stav linek
- Historické grafy (teplota, tlak, rychlost)
- Alarmy (mimo toleranci → notifikace)
- Reporty (shift report, OEE)

Autorův Streamlit dashboard pro VCF = analogický koncept
pro vizualizaci dat z CNC. SCADA = vizualizace dat z PLC.
```

#### Příklad 4: Autorovo využití
```
Autorův CNC_2_LLM projekt: DXF → ML feature vektor.
PLC rozšíření: PLC sbírá data z CNC stroje (otáčky, proud, vibrace)
→ Python (pymodbus) → ML feature vektor → predikce opotřebení nástroje
= Integrace PLC do autorova ML pipeline.
```

### 3.4 Přínos pro autora

| Přínos | Dopad |
|--------|-------|
| **Odemkne Siemens/Rockwell role (3×)** | 3 konkrétní příležitosti |
| **PLC + Python = unikátní profil** | Málo lidí umí obojí. Autor = most mezi OT a IT |
| **Industry 4.0 = přirozený positioning** | PLC + Python + ML = přesně to co firmy hledají |
| **SCADA/MES integrace** | Autor už dělá vizualizaci (Streamlit). SCADA = průmyslová verze |
| **CNC → PLC transfer** | Autor zná CNC. PLC = přirozený next step v doméně |

### 3.5 Glossary

| Termín | Definice |
|--------|----------|
| **PLC** | Programmable Logic Controller — průmyslový programovatelný ovladač |
| **Ladder Diagram (LD)** | Grafický programovací jazyk pro PLC, vypadá jako elektrický schéma |
| **Structured Text (ST)** | Textový programovací jazyk pro PLC, vypadá jako Pascal |
| **Function Block (FB)** | Opakovaně použitelný blok programu s interním stavem |
| **Scan Cycle** | Cyklus PLC: read inputs → execute → write outputs → housekeeping |
| **I/O Module** | Vstupně/výstupní modul připojovací senzory/aktuary k PLC |
| **Digital Input (DI)** | Binární vstup (0/1): tlačítko, senzor, přepínač |
| **Digital Output (DO)** | Binární výstup (0/1): relé, motor, světlo |
| **Analog Input (AI)** | Spojitý vstup: teplota, tlak, proud, napětí |
| **Analog Output (AO)** | Spojitý výstup: rychlost motoru, polohování |
| **Holding Register** | 16-bitový registr pro čtení/zápis dat (Modbus) |
| **Coil** | Binární výstup (Modbus) |
| **Modbus** | Průmyslový komunikační protokol (master/slave) |
| **PROFINET** | Industrial Ethernet protokol od Siemens |
| **EtherCAT** | High-speed industrial Ethernet protokol |
| **OPC UA** | Platform-independent data exchange protokol |
| **MQTT** | Publish/subscribe protokol pro IoT |
| **SCADA** | Supervisory Control and Data Acquisition — vizualizace a řízení |
| **MES** | Manufacturing Execution System — řízení výroby |
| **OEE** | Overall Equipment Effectiveness — efektivita zařízení |
| **TIA Portal** | IDE pro programování Siemens PLC |
| **Studio 5000** | IDE pro programování Rockwell/Allen-Bradley PLC |
| **Pymodbus** | Python knihovna pro Modbus komunikaci |
| **IEC 61131-3** | Standard pro programovací jazyky PLC |
| **OT** | Operational Technology — průmyslová technologie (PLC, SCADA) |
| **IT** | Information Technology — informační technologie (servery, sítě) |
| **Industry 4.0** | Čtvrtá průmyslová revoluce = digitalizace výroby |

---

## ❹ Kubernetes

### 4.1 Co je Kubernetes

Kubernetes (K8s) je **open-source platforma pro orchestraci kontejnerů**. Řídí nasazení, škálování a provoz aplikací v kontejnerech (Docker) napříč klastry strojů. Vytvořil ho Google, dnes je standardem pro云 native aplikace.

**Klíčový insight pro autora:** Autor už používá Docker (python:3.11-slim → Cloud Run). K8s = "Cloud Run na steroidech" — běží na vašem vlastním hardwaru nebo libovolném cloudu, s větší kontrolou.

#### Ontologie Kubernetes

```
Kubernetes (K8s)
├── Architektura
│   ├── Control Plane (manažerský uzel)
│   │   ├── API Server (vstupní bod pro všechny příkazy)
│   │   ├── etcd (distribuovaná key-value databáze — stav klastru)
│   │   ├── Scheduler (přiřazování Podů na Nody)
│   │   ├── Controller Manager (udržování požadovaného stavu)
│   │   └── Cloud Controller Manager (integrace s cloudem)
│   └── Worker Nody (pracovní uzly)
│       ├── kubelet (agent na každém nodu)
│       ├── kube-proxy (síťování na nodu)
│       └── Container Runtime (Docker, containerd, CRI-O)
│
├── Základní objekty
│   ├── Pod
│   │   ├── Nejmenší jednotka nasazení
│   │   ├── Obsahuje 1+ kontejnerů
│   │   ├── Sdílí síť + storage
│   │   └── Analogie: "virtuální počítač" pro kontejnery
│   ├── Deployment
│   │   ├── Spravuje repliky Podů
│   │   ├── Rolling updates (postupné nasazování)
│   │   ├── Rollback (návrat předchozí verze)
│   │   └── Analogie: Docker Compose, ale na klastru
│   ├── Service
│   │   ├── Síťový endpoint pro skupinu Podů
│   │   ├── Types: ClusterIP, NodePort, LoadBalancer
│   │   └── Analogie: reverse proxy / load balancer
│   ├── Ingress
│   │   ├── HTTP/HTTPS routing na Services
│   │   ├── TLS termination
│   │   └── Analogie: nginx reverse proxy
│   ├── ConfigMap
│   │   ├── Konfigurační data (key-value)
│   │   └── Analogie: .env soubor
│   ├── Secret
│   │   ├── Citlivá data (hesla, API klíče)
│   │   └── Analogie: .env.local (šifrovaný)
│   ├── Volume
│   │   ├── Trvalý storage pro Pody
│   │   └── Analogie: Docker volume, Persistent Disk
│   └── Namespace
│       ├── Logická izolace v klastru
│       └── Analogie: "virtuální cluster" v jednom fyzickém
│
├── Škálování
│   ├── Horizontal Pod Autoscaler (HPA)
│   │   └── automatické přidávání Podů podle zátěže
│   ├── Vertical Pod Autoscaler (VPA)
│   │   └── automatická změna CPU/memory pro Pod
│   └── Cluster Autoscaler
│       └── automatické přidávání Worker Nodů
│
├── Síť (Networking)
│   ├── Pod Network (flat síť — každý Pod má IP)
│   ├── Service Network (virtuální síť pro Services)
│   ├── DNS (automatické jméno: service.namespace.svc.cluster.local)
│   └── Network Policies (firewall rules mezi Pody)
│
└── Storage
    ├── Persistent Volume (PV) — fyzický storage
    ├── Persistent Volume Claim (PVC) — požadavek na storage
    ├── StorageClass (typ storage: SSD, HDD, NFS)
    └── CSI (Container Storage Interface) — pluginy pro různé storage
```

### 4.2 Proč se to poptává (tržní kontext)

| Důvod | Vysvětlení |
|-------|-----------|
| **K8s = standard pro cloud-native** | Většina velkých firem používá K8s pro provoz aplikací |
| **3× výskyt v analyzovaných nabídkách** | Siemens, Thermo Fisher, Google — všechny hledají K8s zkušenosti |
| **Portabilita** | K8s běží na AWS, GCP, Azure i on-premises. Kód = stejný všude |
| **Škálovatelnost** | Automatické škálování podle zátěže. 10 uživatelů → 10 000 = K8s to řeší |
| **Microservices** | K8s = nativní platforma pro microservices architekturu |
| **DevOps culture** | K8s = součást DevOps kultury. Kdo umí K8s = umí moderní infrastrukturu |
| **Enterprise adoption** | 96 % organizací podle CNCF survey používá nebo plánuje K8s |

### 4.3 Kde se to používá (praktické příklady)

#### Příklad 1: Nasazení webové aplikace
```
Firma má 3 mikroservisy: API, frontend, worker.
K8s: 3 Deployments + 3 Services + 1 Ingress
- API: 3 repliky (vysoce dostupné)
- Frontend: 2 repliky
- Worker: 1 replika (background úlohy)
- Ingress: routuje /api → API, / → Frontend

Automatické škálování: API 3→10 replik při zátěži.
= Autor má Streamlit na Cloud Run. K8s = nasazení na vlastní klastr.
```

#### Příklad 2: ML model serving
```
Firma má ML model pro predikci opotřebení nástrojů.
K8s: Deployment s GPU node pool
- Model: TensorFlow Serving v kontejneru
- Auto-scaling: 0→5 replik podle requestů
- GPU: speciální node pool s NVIDIA GPU
- Inference API: REST endpoint pro predikce

Autorův CNC_2_LLM = ML pipeline. K8s = nasazení modelu do produkce.
```

#### Příklad 3: IoT data pipeline
```
Tisíce senzorů → MQTT broker → K8s
- Kafka Streams (zpracování toků dat)
- TimescaleDB (časové řady)
- Grafana (dashboards)
- AlertManager (alarmy)

K8s řídí: auto-scaling podle objemu dat, self-healing pokud padne pod.
Autor už sbírá data z ESP32. K8s = škálovatelná infrastruktura.
```

#### Příklad 4: Autorovo využití
```
Autor má MCP servery jako Python aplikace.
K8s nasazení:
- linkedin-mcp: Deployment (2 repliky) + Service
- mcp-jobs: Deployment (1 replika) + Service
- lichess-mcp: Deployment (1 replika) + Service
- Ingress: routování podle URL prefixu

= Autor se učí K8s na vlastních projektech. MCP = idealní Learning ground.
```

### 4.4 Přínos pro autora

| Přínos | Dopad |
|--------|-------|
| **Odemkne enterprise role (3×)** | 3 konkrétní příležitosti |
| **Portabilita mezi cloudy** | Autor už umí GCP. K8s = stejný na Azure/AWS |
| **Self-healing** | Aplikace se automaticky restartuje při selhání |
| **Auto-scaling** | Automatické škálování podle zátěže |
| **MCP + K8s = produkce** | MCP servery nasazené na K8s = enterprise-ready |
| **DevOps credibility** | K8s = součást DevOps. Autor = DevOps ready |

### 4.5 Glossary

| Termín | Definice |
|--------|----------|
| **Kubernetes (K8s)** | Open-source platforma pro orchestraci kontejnerů |
| **Container** | Izolovaná běhová jednotka aplikace (Docker) |
| **Pod** | Nejmenší jednotka nasazení v K8s, obsahuje 1+ kontejnerů |
| **Deployment** | Správce replik Podů s rolling updates |
| **Service** | Síťový endpoint pro skupinu Podů |
| **Ingress** | HTTP/HTTPS routing na Services |
| **ConfigMap** | Konfigurační data (key-value) |
| **Secret** | Citlivá data (šifrovaná) |
| **Volume** | Trvalý storage pro Pody |
| **Persistent Volume (PV)** | Fyzický storage přidělený klastru |
| **Persistent Volume Claim (PVC)** | Požadavek na storage od uživatele |
| **Namespace** | Logická izolace v klastru |
| **Node** | Fyzický nebo virtuální stroj v klastru |
| **Control Plane** | Manažerská vrstva K8s (API server, etcd, scheduler) |
| **Worker Node** | Pracovní uzel kde běží Pody |
| **kubelet** | Agent na každém Worker Node |
| **Cluster** | Soubor Node propojených K8s |
| **Helm** | Package manager pro K8s (analogie: pip pro Python) |
| **kubectl** | CLI nástroj pro správu K8s |
| **HPA** | Horizontal Pod Autoscaler — auto-scale Podů |
| **VPA** | Vertical Pod Autoscaler — auto-scale CPU/memory |
| **Cluster Autoscaler** | Auto-scale Worker Nodů |
| **Rolling Update** | Postupná aktualizace Podů bez downtime |
| **Rollback** | Návrat k předchozí verzi |
| **Self-healing** | Automatická oprava selhaných Podů |
| **Liveness Probe** | Kontrola zda žije kontejner (restart pokud ne) |
| **Readiness Probe** | Kontrola zda je kontejner připraven přijímat traffic |
| **Docker** | Platforma pro tvorbu a běh kontejnerů |
| **containerd** |轻ší container runtime (alternativa k Docker) |
| **CNCF** | Cloud Native Computing Foundation — organizace za K8s |
| **Microservices** | Architektura = aplikace rozdělená na malé služby |
| **Cloud-native** | Aplikace navržené pro běh v cloudu (K8s, Docker, CI/CD) |

---

## EROI porovnání — všechny gapy

| Gap | EROI | Čas | Tržní signál | Přínos | Priorita |
|-----|:----:|:---:|:------------|:-------|:--------:|
| **TypeScript + Playwright** | ⭐⭐⭐⭐ | 15–20 h | 2× výskyt | E2E testy, Rockwell-like role | 🥇 |
| **AZ-900** | ⭐⭐⭐⭐ | 10–15 h | 4× výskyt | Certifikace, Azure match | 🥈 |
| **PLC Basics** | ⭐⭐⭐ | 40–60 h | 3× výskyt | Industrial credibility, OT/IT most | 🥉 |
| **Kubernetes** | ⭐⭐ | 40+ h | 3× výskyt | Enterprise, portabilita | 4. |

### Důvod pořadí

1. **TypeScript** = nejkratší čas (15–20 h), nejvyšší EROI, odemkne 2 role
2. **AZ-900** = nejkratší čas (10–15 h), certifikace = okamžitý signál, 4 role
3. **PLC** = delší čas (40–60 h), ale přirozený transfer z CNC. Unikátní kombinace PLC + Python
4. **Kubernetes** = nejdelší čas (40+ h), nejnižší EROI. Důležité pro enterprise, ale ne urgentní

### Transfer learning matrix

| Zdroj (autor umí) | Cíl (gap) | Podobnost | Přenos znalostí |
|-------------------|-----------|:---------:|:---------------:|
| Python OOP | TypeScript | 70 % | Interfaces ≈ Protocol, async/await ≈ Python async |
| Pytest fixtures | Playwright fixtures | 80 % | Prakticky identický pattern |
| GCP Cloud Run | AZ-900 Azure | 60 % | Cloud koncepty = stejné, jiná jména |
| Docker | Kubernetes | 50 % | K8s = Docker orchestrace |
| CNC/G-code | PLC/Ladder | 40 % | CNC = pohyb. PLC = řízení celého provozu |
| Streamlit dashboard | SCADA/MCM | 30 % | Vizualizace dat = podobný koncept |

---

## Doporučená Trajektorie (Q3+ 2026)

```
TÝDEN 1-2: TypeScript základy (5-8 h)
  └── Udemy kurz + přepis jednoho Python scriptu do TS

TÝDEN 2-3: Playwright základy (5-8 h)
  └── 1 PoC test pro Vcf-compiler Streamlit dashboard

TÝDEN 3: TypeScript PoC projekt (5-7 h)
  └── API test suite pro VCF parser nebo MCP server

TÝDEN 4-5: AZ-900 kurz (10-12 h)
  └── Microsoft Learn + cvičné testy

TÝDEN 6: AZ-900 zkouška (1 h)
  └── Online proctor + certifikace

TÝDEN 7-12: PLC základy (40-60 h)
  └── TIA Portal trial + Modbus PoC + dokumentace

TÝDEN 13+: Kubernetes (40+ h, volitelné)
  └── minikube + deployment MCP serveru na K8s
```

---

*Dokument vytvořen: 2026-08-06*
*Zdroje: Tržní analýza (24 LinkedIn nabídek), Live GitHub audit, EROI plán v2.0*
*Provenance: Summary (zdroj: technologický průzkum + tržní analýza)*
