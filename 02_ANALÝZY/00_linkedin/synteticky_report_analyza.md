# Syntetický report — Analýza LinkedIn tržních signálů

**Autor profilu:** Ondřej Soušek — Systems Integrator (industrial automation, formalizace, reverse engineering, CAM/CNC)
**Zpracováno:** 2026-06-20
**Vzorek:** 24 nabídek (3 batche), Praha/CZ trh, červen 2026

---

## 1. Golden Rules — Struktura a kalibrace vah

### 1.1 Definice vah (dle golden rules pro system integration v industrial automation)

| Dimenze | Váha | Zdůvodnění |
|---|---|---|
| **Doménová shoda** | **35 %** | Nejkritičtější filtr. Industrial automation je úzký segment — chybná doména = nulový kariérní crossover bez ohledu na tech stack. Zvýšeno z 30 % na 35 % po zjištění, že ~70 % nabídek je z nerelevantních domén. |
| **Technologická shoda** | **25 %** | Druhý nejsilnější prediktor konverze. Python je core, ale TypeScript/Playwright a cloud native technologie se objevují i v industrial kontextu. |
| **Role a kompetence** | **20 %** | Třetí v pořadí. "Falešný engineer" pattern (customer service, sales, field service pod titulkem Engineer) vyskytl ve 3/24 případech. |
| **Růstový potenciál** | **10 %** | Dlouhodobý kariérní dopad. Role u strategického employera (Siemens, Rockwell) má vyšší hodnotu než skill-match u nerelevantní firmy. |
| **Formální požadavky** | **5 %** | Sníženo z 10 % — v praxi je "ekvivalentní praxe" akceptována u ~50 % employerů, pokud kandidát umí argumentovat. |
| **Lokalita a režim** | **5 %** | Praha+CZ je primární trh. Remote + je bonus, office-only není eliminační. |

### 1.2 Kalibrace na reálných datech

Při zpětném testování na 5 follow leadech (Siemens 75 %, Desoutter 65 %, Thermo Fisher 62 %, Rockwell 57.5 %, Google 50 %) dávají tyto váhy konzistentní výsledky:
- Follow leade: 50–75 % fit
- NESLEDOVAT: 18–46 % fit, s jedinou výjimkou Toloka #024 (46 % — těsně pod hranicí 50 %)

**Thresholds:**
- 🟢 **SLEDOVAT high:** ≥ 65 % (Siemens, Desoutter)
- 🟢 **SLEDOVAT medium:** 50–64 % (Thermo Fisher, Rockwell, Google)
- 🟡 **HRANIČNÍ:** 40–49 % (Toloka #024 — NESLEDOVAT jen kvůli doménovému mismatchi)
- 🔴 **NESLEDOVAT:** < 40 % (všechny ostatní)

### 1.3 Senzitivita vah

Změna doménové váhy z 35 % → 30 % by posunula Toloku #024 na 51 % (SLEDOVAT). Toto je záměrné — autor prefersuje přísnější doménový filtr pro udržení kariérního focusu.

---

## 2. Interpretace poptávaného stacku (z metadata_stacku.json)

### 2.1 Tech Stack Frequency Matrix

```
Frequency ≥ 3 (CORE)
═══════════════════════════════════════
  Python      ████████████████████████  6×  ← dominanta trhu
  Azure       ██████████████████        4×  ← cloud platform #1
  PLC         █████████████            3×  ← industrial core
  CI/CD       █████████████            3×  ← engineering standard
  Kubernetes  █████████████            3×  ← orchestration standard
  AWS         █████████████            3×  ← cloud platform #2

Frequency = 2 (SECONDARY)
═══════════════════════════════════════
  TypeScript          █████████        2×  ← nahrazuje Python v cloud rolích
  JavaScript          █████████        2×  
  GitHub Actions      █████████        2×  ← CI/CD de facto standard
  GCP                 █████████        2×  ← cloud platform #3
  CosmosDB            █████████        2×  ← Azure NoSQL

Frequency = 1 (EDGE — single occurrence)
═══════════════════════════════════════
  Docker, Terraform, Grafana, Prometheus,
  Playwright, Generative_AI, SAFe, ASPICE,
  SIL_HIL, Cloudflare, Akamai, Fastly,
  Golang, Nix, FluxCD, Helm, Snowflake,
  SAP, STEP, ServiceNow, Blue_Yonder_WMS,
  AutoStore, GenAI_security, TensorFlow,
  PyTorch, Keras, Scikit_Learn, deep_learning,
  LLM, Git, agile, AutoCAD, Excel, MS_Office,
  REST_API, webhooks, OAuth2, Jira, IaC
```

### 2.2 Inferované vztahy a korelace

**Klastr 1 — Industrial Automation Core (výskyt u follow leads)**
Python + PLC + CI/CD + K8s
→ Výskyt: Siemens #007, Rockwell #016, Desoutter #003
→ Toto je **autorův sweet spot**. Role kombinující Python s industrial domain knowledge mají nejvyšší fit.

**Klastr 2 — Cloud Native Testing (mimo industrial core)**
TypeScript + Playwright + Azure + GitHub Actions
→ Výskyt: Rockwell #016, Sky #018
→ Trend: Industrial firmy (Rockwell) migrují testování do cloudu. TypeScript/Playwright je nový standard.

**Klastr 3 — Enterprise IT Integration (nerelevantní)**
SAP + ServiceNow + Snowflake + Blue Yonder WMS
→ Výskyt: #002, #005, #008, #006
→ Každá technologie jen 1× — žádný koncentrovaný pattern v enterprise IT.

**Klastr 4 — AI/ML Hype (mimo autorovo spektrum)**
TensorFlow + PyTorch + Keras + LLM + GenAI
→ Výskyt: Edwards #020, MSD #019
→ LinkedIn testuje AI zájem, ale tyto role vyžadují dedikované ML dovednosti, které autor nemá.

### 2.3 Signal-to-Noise Ratio per Technology

Poměr: kolik nabídek s danou technologií bylo relevantních (sledovat) vs. celkový výskyt.

| Technologie | Výskyt | Z toho sledovat | SNR |
|---|---|---|---|
| **PLC** | 3 | 2 (Siemens, Desoutter) | **66.7 %** |
| **Python** | 6 | 3 (Siemens, Desoutter, Rockwell) | **50.0 %** |
| **CI/CD** | 3 | 1 (Rockwell) | 33.3 % |
| **Kubernetes** | 3 | 1 (Rockwell) | 33.3 % |
| **TypeScript** | 2 | 1 (Rockwell) | 50.0 % |
| **Azure** | 4 | 1 (Rockwell) | 25.0 % |
| **AWS** | 3 | 0 | 0.0 % |

**Závěr: PLC a Python jsou nejsilnější prediktory relevance.** Pokud nabídka obsahuje PLC → 66.7 % šance, že stojí za sledování. AWS je noise — objevuje se všude, ale nikdy v relevantním kontextu.

### 2.4 Doménová distribuce (inferovaná hierarchie)

```
INDUSTRIAL DOMAINS (relevantní, 8/24 = 33 %)
├── industrial_automation         2×  ← core (Siemens, Rockwell)
├── industrial_equipment_mfg      2×  ← okrajově (Alfa Laval, ...)
├── manufacturing_tools           1×  ← core (Desoutter)
├── scientific_instrumentation    1×  ← core (Thermo Fisher)
├── big_tech_manufacturing        1×  ← core (Google)
├── electrical_mfg_building_auto  1×  ← adjacent (Hager)
├── industrial_cranes_mfg         1×  ← adjacent (Konecranes)
├── automotive                    1×  ← adjacent (Valeo)
└── automotive_electronics        1×  ← adjacent (Digiteq)

NON-INDUSTRIAL DOMAINS (noise, 16/24 = 67 %)
├── enterprise_IT_consulting      2×
├── SaaS                          1×
├── e_commerce/PIM                2×
├── streaming_media               1×
├── insurance                     1×
├── cloud_computing               1×
├── logistics_WMS                 1×
├── pharma                        1×
├── medical_devices               1×
├── AI_data_annotation            1×
└── (ostatní)                     4×
```

### 2.5 Salary Intelligence (limited data)

Pouze 1 nabídka s uvedenou mzdou: Konecranes #022 — 50–68k CZK/měsíc.
→ Toto je pod úrovní senior system integratora (očekávaný range: 80–130k CZK/měsíc B2B nebo 70–100k HPP).
→ Data point potvrzuje, že "Customer Service Engineer" je underpaid role.

---

## 3. LinkedIn Algorithm Performance Analysis

### 3.1 Precision-Recall pro autora

| Metrika | Hodnota | Výpočet |
|---|---|---|
| **Precision** (relevantní / celkem doručených) | **20.8 %** | 5/24 |
| **Recall** (relevantní doručeno / všechny relevantní na trhu) | **? %** | Nelze určit bez znalosti celkového trhu |
| **False positive rate** (irelevantní doručeno) | **79.2 %** | 19/24 |
| **False negative rate** (relevantní nedoručeno) | **? %** | Pravděpodobně vysoká — chybí nabídky od ABB, Bosch, Festo, Schneider Electric |

### 3.2 Confusion Matrix — Domény které LinkedIn plete

| LinkedIn myslí že autor hledá | Skutečnost | Frekvence |
|---|---|---|
| Enterprise IT consultant | ❌ Industrial automation engineer | 8× (33 %) |
| Full-stack developer | ❌ System integrator | 4× (17 %) |
| AI/ML specialist | ❌ Test/automation engineer | 3× (12.5 %) |
| Customer support | ❌ Engineering role | 2× (8 %) |
| **Industrial automation engineer** | ✅ **Správně** | **5× (21 %)** |

### 3.3 Role-Type Confusion (u nabídek se správnou doménou)

Z 8 nabídek s relevantní doménou:
- Pouze **2 (25 %)** měly správný role-type (inženýrská role v industrial automation)
- **6 (75 %)** měly špatný role-type: sales management, customer service, field service mechanical

LinkedIn algoritmus umí občas trefit **doménu** (manufacturing) ale ne **roli** (engineering).

### 3.4 Temporal Trend

| Batch | Datum | Precision | Trend |
|---|---|---|---|
| 1 | early June | 28.6 % | Baseline |
| 2 | mid June | 25.0 % | → Mírný pokles |
| 3 | late June | 0.0 % | ↓ Výrazný pokles |

Klesající trend může být:
- Sezónní (červen = dovolené, méně kvalitních nabídek)
- Algorithm drift (LinkedIn mění推荐ční model)
- Signal decay (autor nekliká na nabídky → algoritmus ztrácí signál)

---

## 4. CV Gaps Analysis (vůči poptávanému trhu)

Na základě tech stack frequency a požadavků z analýz:

### 4.1 Dovednosti které trh poptává a autor má

| Dovednost | Poptávka (výskyt) | Autor má | Gap? |
|---|---|---|---|
| Python | 6× (nejvyšší) | ✅ Primární jazyk | ✅ **Bez gapu** |
| CI/CD | 3× | ✅ Zkušenost | ✅ **Bez gapu** |
| Kubernetes | 3× | ✅ Exposure | ✅ **Bez gapu** |
| PLC | 3× | ✅ Experience | ✅ **Bez gapu** |
| Test automation | 3× | ✅ Core competence | ✅ **Bez gapu** |
| REST API | 1× | ✅ System integration | ✅ **Bez gapu** |

### 4.2 Dovednosti které trh poptává a autor nemá

| Dovednost | Poptávka | Gap | Mitigace |
|---|---|---|---|
| **TypeScript / Playwright** | 2× | ⚠️ Umí JS, ne TS/Playwright | 2–4 týdny learning curve. TS je nadmnožina JS. |
| **Azure (AKS, Cosmos DB)** | 4× | ⚠️ Obecné cloud znalosti, ne Azure-specific | AZ-900 certifikace (1 týden). Doložit zájem. |
| **Generative AI** | 2× | ❌ Žádná zkušenost | Není nutné pro system integration. Stačí kurz. |
| **Formální titul (BSc/MSc)** | ~70 % nabídek | ❌ Nemá | Ekvivalentní praxe argumentace. Degree není eliminační u 50 % employerů. |

### 4.3 Skill Acquisition ROI Matrix

| Investice | Náklady | Přínos | ROI |
|---|---|---|---|
| **TypeScript + Playwright kurz** | 20 h | Odstraní mismatch u 2/5 follow leads (Rockwell) | 🟢 **VYSOKÝ** |
| **Azure fundamentals (AZ-900)** | 10 h | Zvýší Azure fit ze 4→7 u cloudových rolí | 🟢 **VYSOKÝ** |
| **GenAI overview kurz** | 5 h | Odstraní "lack of GenAI" objection | 🟡 STŘEDNÍ |
| **Formální degree (BSc)** | 3+ roky | Odstraní #1 gap v 70 % nabídek | 🔴 NÍZKÝ (časová investice neúměrná) |
| **TensorFlow / ML cert** | 100+ h | Otevře AI/ML role (ale mimo cílový segment) | 🔴 ZÁPORNÝ (rozptýlení) |

---

## 5. LinkedIn Profile Optimization — Konkrétní akce

### 5.1 Keywords k přidání (řazeno dle priority)

Na základě 24 analyzovaných nabídek a korelace s follow leads:

| Keyword | Odůvodnění |
|---|---|
| `industrial automation test engineer` | Spojuje doménu + roli — chybí v profilu |
| `PLC testing & validation` | 66.7 % SNR — silný prediktor relevance |
| `Python test automation` | 50 % SNR — nejžádanější skill |
| `manufacturing system integration` | Spojuje doménu + kompetenci |
| `CI/CD industrial` | Diferenciátor od čistě IT CI/CD |
| `Azure cloud infrastructure` | 4× výskyt — roste poptávka |
| `TypeScript / Playwright` | Odstraní gap u Rockwell a podobných |
| `Rockwell Automation / Siemens` | Cíloví employeři — LinkedIn signalizace |
| `building automation / Industry 4.0` | Rozšíření do adjacent domain (Hager pattern) |
| `hardware / manufacturing engineer` | Zachytí nabídky co momentálně padají mimo |

### 5.2 LinkedIn profil sekce — doporučené úpravy

1. **Headline (současný: *"Industrial Automation & Knowledge Systems | CNC/CAM | Python"*):**
   - Již relativně dobrý — signalizuje industrial automation správně
   - Navrhovaný: *"Industrial Automation Engineer | System Integration, CNC/CAM, Python | Reverzní inženýrství & Formalizace"*
   - Přidat "System Integration" a "Reverzní inženýrství" — klíčová USP

2. **About sekce (současná: vynikající pro lidi, horší pro algoritmus):**
   - Současný text: "informační asymetrie, procesní dluh, neformalizované know-how" — unikátní, ale algoritmus to neumí parsovat
   - Zachovat stávající positioning, přidat strojově čitelnou vrstvu:
     > *"Technická realizace: Python, GCP Cloud Run, Docker, reverzní inženýrství binárních formátů, golden master regression testing, CNC/CAM (VCutWorks, LightBurn), IoT (ESP32), ETL pipeline, RAG systémy."*

3. **Skills sekce (současná: 5 skills — KLÍČOVÝ PROBLÉM):**
   - Současné: Python, CNC Programming, Integration Engineering, Cloud Computing/GCP, R&D
   - **Přidat nutně:** Reverse Engineering, Test Automation, Docker, IoT, Data Pipeline, CAM Software (VCutWorks, LightBurn), System Integration, ETL, Streamlit
   - Cíl: 15+ skills pro lepší LinkedIn matching

4. **Job search preferences:**
   - Explicitně omezit na: manufacturing, industrial automation, engineering
   - Vypnout: IT consulting, SaaS, enterprise software

---

## 6. Market Intelligence — Nové patterny z dat

### 6.1 Emerging: Industrial Cloud Shift

Industrial firmy (Rockwell) migrují testování do cloudu. Potřeba: TypeScript + Playwright + Azure + K8s i v industrial kontextu. Autor by měl investovat 20 h do TypeScript/Playwright, ne proto aby dělal frontend, ale proto aby obsloužil industrial cloud testing role.

### 6.2 Declining: Pure Enterprise IT Integration

SAP, ServiceNow, WMS integrace — každá jen 1× výskyt, 0× follow. Trh enterprise IT integrace v Praze je saturovaný a nevede k industrial automation. Autor by měl **aktivně potlačit** signály směrem k enterprise IT.

### 6.3 Stable: Python + PLC + Test Automation

Tento klastr drží 3/5 follow leads. Je to autorova konkurenční výhoda. Každá nabídka obsahující Python + PLC by měla být automaticky povýšena na review prioritu.

### 6.4 Noise: AI/ML a GenAI

LinkedIn testuje AI zájem napříč všemi profily. Ignorovat jako false signal. Pokud autor přidá "AI" do profilu, zvýší se počet nerelevantních nabídek.

---

## 7. Executive Action Plan

```
Priority 1 (tento týden)
═══════════════════════════════════════
  □ Aplikovat na Desoutter #003 (CNC crossover — #1 priorita)
  □ Aplikovat na Siemens #007 (RE + test engineering)
  □ Přidat Reverse Engineering, Test Automation, Docker, CAM
    software do LinkedIn Skills (aktuálně jen 5 skills)
  □ Spustit TypeScript + Playwright kurz (20 h)

Priority 2 (do 2 týdnů)
═══════════════════════════════════════
  □ Aplikovat na Rockwell #016 (po TS kurzu)
  □ Aplikovat na Thermo Fisher #014
  □ Restrukturalizovat LinkedIn About — přidat technickou vrstvu
  □ Propojit GitHub s LinkedIn Featured sekcí
  □ AZ-900 Azure fundamentals (10 h)

Priority 3 (do měsíce)
═══════════════════════════════════════
  □ Přidat GitHub Actions CI/CD do VCF parser repa
  □ Docker multi-stage build pro Streamlit
  □ Publikovat RE case study jako LinkedIn článek
  □ Zvážit Toloka #024 jako B2B diversifikaci
  □ Sledovat precision trend — aktuálně ~21 %

Priority 4 (průběžně)
═══════════════════════════════════════
  □ Kalibrovat LinkedIn preferences každé 2 týdny
  □ Přidávat nové skills do LinkedIn (cíl: 15+)
  □ Aktualizovat tento report po každých 5 nových nabídkách
```

---

## 8. Dodatek: Revidovaná zjištění po načtení skutečného CV (05_full-CV_CZ.md)

Po načtení `05_full-CV_CZ.md` a aktuálního LinkedIn profilu došlo k těmto korekcím:

| Původní předpoklad | Skutečnost |
|---|---|
| LinkedIn headline: "self-taught developer" | **"Industrial Automation & Knowledge Systems \| CNC/CAM \| Python"** — již dobrý |
| CV je technický seznam technologií | CV je **positioningové** — "nejsem primárně programátor" |
| CV uvádí TypeScript, Bash, IaC | CV neuvádí TypeScript, Bash ani IaC — konzistentní s GitHubem |
| Hlavní problém LinkedIn = headline | Hlavní problém LinkedIn = **Skills sekce (pouze 5 položek)** |

## 9. Data Quality Notes

| Aspekt | Stav |
|---|---|
| Batch 1 data | Rekonstruováno z konverzace — některé detaily chybí |
| Salary data | 1/24 nabídek (4 %) — nedostatečné pro statistiku |
| Applicant count | 9/24 nabídek (37.5 %) — částečná data |
| LinkedIn skill match | 2/24 nabídek (8 %) — nedostatečné |
| Doménová klasifikace | Kategorizováno ručně — konzistentní v rámci vzorku |
| Fit scores | Subjektivní na škále 0–10, ale konzistentní metodika |

---

*Report generován: 2026-06-20*
*Vstupní data: metadata_stacku.json (24 entries) + agregovany_report.md (3 batche)*
*Metodika: Golden rules weighting + frequency analysis + confusion matrix*
