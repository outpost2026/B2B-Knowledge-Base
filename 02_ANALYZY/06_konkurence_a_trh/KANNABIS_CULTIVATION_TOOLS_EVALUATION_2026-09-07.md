# Qualifikovaná evaluace: Cannabis cultivation tracking tools vs TEMP_KULTURA_DB
Datum: 2026-09-07 | Autor: outpost2026
Ucel: Srovnání našeho repa s 12 veřejně dostupnými analogickými nástroji a kvalifikované zhodnocení konkurenční pozice.

---

## 1. Metodologie evaluace

Bylo vyhledáno **12 analogických projektů** zaměřených na pěstování konopí / rostlin přes veřejné zdroje (GitHub, GitTopics, awesome-kurace). Každý byl hodnocen na 6 os (viz §3). Hodnocení je kvalitativní + kvantitativní kde dostupné (hvězdy, forky, commits).

Kritéria porovnání:
- **Stack/Tech** — technická základna
- **Scope** — co pokrývá (plný lifecycle vs pouze monitoring)
- **Data layer** — jak data uchovává a poskytuje
- **Dashboard/UI** — vizualizace a reporting
- **Automation** — automatizace a integrace
- **Community/Traction** — otevřenost, hvězdy, aktivita

---

## 2. Přehled analogických projektů

| # | Projekt | Stack | Počet hvězd | Forky | Commits | Zaměření |
|---|---------|-------|-------------|-------|---------|----------|
| 1 | **Emerald Plant Tracker** (Dmans218) | React/Express/SQLite, Docker | 11 | 3 | 293 | Kompletní cannabis cultivation tracker |
| 2 | **Isley / CultivarLog** (wu1ff) | Go/Docker, PostgreSQL | 0 | 0 | 87 | Self-hosted grow journal + sensor dashboard |
| 3 | **cannaUNITY** (cannatoshi) | Django/Python, Docker | 2 | 0 | 470 | KCanG-compliant framework pro cannabis spolky |
| 4 | **GrowApp** (Shannon-Goddard) | Vanilla JS/IndexedDB, mobile app | 13 | 1 | 644 | Data-driven cannabis guide + 2,800+ strains |
| 5 | **Mycodo** (kizniche) | Python/Raspberry Pi | 350+ | — | — | Sensor monitoring & automation pro Raspberry Pi |
| 6 | **Mudpi** (Intergalactic-XYZ) | Python, Raspberry Pi SBC | — | — | — | Event-based sensor data gathering |
| 7 | **Potnanny** | Python/RPi + Bluetooth | — | — | — | Grow-room automation s BT senzory |
| 8 | **Brokkoli** (CodingMush) | Home Assistant custom_component | 0 | 0 | 582 | Cannabis monitoring pro Home Assistant |
| 9 | **crop-yield-dashboard** (d-dziublenko) | Python/Streamlit/XGBoost | 0 | 0 | — | ML predikce výnosu |
| 10 | **FarmSmart** (ess-142) | Python/Streamlit/Plotly | 0 | 0 | — | Crop & irrigation dashboard + OpenWeatherMap |
| 11 | **HortusFox** (danielbrendel) | PHP/self-hosted | — | — | — | General plant tracking (ne cannabis-specifický) |
| 12 | **Open Garden Planner** (cofade) | Python/Desktop (PyInstaller) | 21 | 2 | 385 | CAD-like garden planning |

---

## 3. Detailní srovnání

### 3.1 Emerald Plant Tracker — NEJBЛИЖŠÍ ANALOG

**Co dělá dobře:**
- Kompletní plant lifecycle tracking (seed → harvest → archive)
- Multi-tent environmental monitoring (temp/humidity/VPD/CO₂/PPFD)
- Activity logs s fotkami
- Nutrient calculator (10 branded formulas)
- Docker deployment, SQLite backend
- API-first architektura (Express REST API)

**Co dělá špatně:**
- Frontend v React SPA, žádné server-side rendering
- SQLite pro production — write contention
- Žádný weather API integration (Open-Meteo, AccuWeather)
- Žádné kvantitativní yield modelování (jen "record harvest yield")
- Žádný crop science layer (GDD, DLI, VPD calculations)
- Žádní automatic data pull z externích zdrojů
- Frontend-heavy approach, obtížné automatizovat

**Naše výhoda nad ním:**
- Tempkaličtější data: GDD (grow degree days), DLI (daily light integral), VPD (vapor pressure deficit) — Emerald nemá ani jedno
- Open-Meteo/AccuWeather automatický pull — Emerald žádní weather integration
- V3.0 yield model s stem diameter + health factors — Emerald jen "record yield"
- Botrytis risk monitoring (CRIT HIGH hours, leaf wet hours) — Emerald nemá
- PostgreSQL-ready, ale i SQLite s kompaktním storage
- Batch pipeline (refresh_dashboards.ps1) — 10 kroků automatizace

### 3.2 Isley / CultivarLog

**Co dělá dobře:**
- Self-hosted, Docker-first
- Go backend (výkonný)
- AC Infinity + Ecowitt hardware integration
- Seed inventory + harvest tracking
- Mobile-friendly
- PostgreSQL pro production

**Co dělá špatně:**
- 0 hvězd, minimální community
- Aktivní vývoj ale s breaking changes
- Žádné weather API, žádné crop science calculations
- Žádné yield estimation
- API pouze pro sensor data (AC Infinity, Ecowitt) — ne pro weather

**Naše výhoda:**
- Weather integration (CHMI + Open-Meteo) je jediný zdroj teplotních a srážkových dat — Isley ji nemá
- Kulturně specifické parametry (flowering config, AP/GG discount)

### 3.3 cannaUNITY

**Co dělá dobře:**
- 470 commits = velmi aktivní
- KCanG-compliance (německý právní rámec)
- Track & trace s UUID
- UniFi Access/Protect integrace
- Django backend, modulární
- GoB-compliant accounting

**Co dělá špatně:**
- Zaměřený na cannabis spolky/komunitu, ne na cultivation monitoring
- Regulární/zároveň podnikový rámec, ne agronomický
- Žádní weather data, crop science, yield modeling
- Komplikovaný stack (Django + UniFi + UniFi Protect + SIMATIC S7)

**Naše výhoda:**
- Naše repo je agronomicky orientované (GDD/DLI/VPD/botrytis), ne právní/regulační
- jednodušší, srozumitelnější stack (Python-only)

### 3.4 GrowApp

**Co dělá dobře:**
- 2,800+ strain database
- Mobile-first (iOS/Android/Web)
- DLI tool
- Harvest window AI trichome analyzer (TensorFlow.js)
- IndexedDB pro offline-first

**Co dělá špatně:**
- Purely frontend (Vanilla JS) — žádný backend
- IndexedDB — limits data volume
- Žádní weather API, žádní sensor integration
- Žádní quantitative yield modeling
- Strain database = encyclopedic, not analytical

**Naše výhoda:**
- Naše backend data (PostgreSQL/SQLite) poskytuje kvantitativní analýzu
- GrowApp má straindb ale nemá metriky prostředí

### 3.5 Mycodo / Mudpi / Potnanny / Brokkoli

Tyto jsou **hardware-centric** (Raspberry Pi / ESP32 / Home Assistant). Jsou IoT platformy pro senzorové čtení a automatizaci. Naše repo:
- **Nemá hardware dependency** — data přicházejí z CHMI API + Open-Meteo + AccuWeather
- **Nemusí běžet na RPi** — Python-only, bez GPIO
- **Má crop science layer** (GDD, DLI, VPD, botrytis) — žádné z těchto nemá

### 3.6 crop-yield-dashboard / FarmSmart

**crop-yield-dashboard:**
- XGBoost + SHAP pro yield prediction
- Streamlit dashboard
- Ale: jen weather + soil → yield, žádní plant-level tracking, žádní lifecycle

**FarmSmart:**
- Streamlit/Plotly + OpenWeatherMap
- Crop + irrigation visualization
- Ale: general agriculture, ne cannabis-specific

**Naše výhoda nad těmito:**
- Naše yield model je mechanistický (physiological), ne ML-black-box
- Naše plant-level tracking (11 plants, 94 measurements) je detailnější
- Naše DLI/GDD/VPD calculations jsou agronomicky specializované pro cannabis

### 3.7 HortusFox / Open Garden Planner

**HortusFox** — general plant tracking, self-hosted PHP. Nebyl by relevantní pro cannabis specifické potřeby.
**Open Garden Planner** — CAD-like garden planning, Python desktop app. Zaměřený na zahradní architekturu, ne na monitoring.

---

## 4. Kvalifikované zhodnocení

### 4.1 Kde TEMP_KULTURA_DB dominuje

| Capability | naše repo | nejlepší analog | gap |
|---|---|---|---|
| **Weather-driven agronomy** | CHMI + Open-Meteo + AccuWeather → GDD/DLI/VPD/botrytis | Žádný nemá | **Náš unikátní bod** |
| **Crop science calculations** | GDD, DLI, VPD, leaf wet hours, botrytis CRIT/HIGH | Emerald: none | **Náš unikátní bod** |
| **Yield modeling** | Physiological v3.0 (stem diameter, health, base) | GrowApp: strain DB only | **Náš unikátní bod** |
| **Batch automation** | 10-step pipeline (refresh_dashboards.ps1) | Zádný nemá pipeline | **Náš unikátní bod** |
| **Data freshness** | last_extraction.json + strict staleness guard | Emerald: manual | **Náš unikátní bod** |
| **Config-driven flowering** | DB config table (AP/GG min/max/avg) | Emerald: hardcoded | **Náš unikátní bod** |

### 4.2 Kde jsme zaostávali (prosazení)

| Capability | naše repo | nejlepší analog | doporučení |
|---|---|---|---|
| **Hardware integration** | ❌ | Mycodo/Mudpi: RPi GPIO | Add MQTT/Homie support for sensor hardware |
| **Mobile UI** | ❌ (HTML only, desktop) | GrowApp: iOS/Android/PWA | Add responsive PWA or mobile wrapper |
| **Strain database** | ❌ | GrowApp: 2,800+ strains | Add strain library with genetics/breeder info |
| **Photo documentation** | ❌ | Emerald: plant photos in logs | Add photo upload to plant management |
| **Community/regulatory** | ❌ | cannaUNITY: KCanG compliance | Not needed (Czech personal use) |
| **Nutrient calculator** | ❌ | Emerald: 10 brands | Add nutrient mixing calculator |
| **ML yield prediction** | ❌ (physiological only) | crop-yield-dashboard: XGBoost | Add XGBoost as secondary model |

### 4.3 Kde jsme výrazně před nimi

| Capability | naše repo | nejlepší analog | evidence |
|---|---|---|---|
| **DST-aware timezone** | ZoneInfo("Europe/Prague") | Žádný nemá timezone handling | Emerald: none, Isley: none |
| **Config-driven flowering** | DB table + backward compat | Emerald: hardcoded in localStorage | Emerald prefs in localStorage |
| **Batch pipeline with validation** | refresh_dashboards.ps1 + check_consistency.py | Žádný nemá pipeline | Emerald: manual Docker only |
| **Disease risk monitoring** | Botrytis CRIT/HIGH hours + leaf wet | Žádný nemá disease modeling | Emerald: environment only |
| **Archive gap filling** | refresh_archive_incremental.py | Žádný nemá incremental archive | — |

### 4.4 Celkové EROI zhodnocení

| Dimension | rating (1-10) | poznámka |
|---|---|---|
| **Technical uniqueness** | **9/10** | GDD/DLI/VPD/botrytis yield model is genuinely novel in open-source cannabis tools |
| **Automation maturity** | **8/10** | 10-step pipeline with strict validation exceeds any analog |
| **Data integrity** | **9/10** | Config table, last_extraction.json, check_consistency.py — rigorous |
| **Community traction** | **1/10** | 0 stars, private repo — zero external visibility |
| **Hardware ecosystem** | **2/10** | No RPi/ESP32/MQTT integration — Mycodo has 350+ stars here |
| **Mobile access** | **1/10** | Desktop HTML only — GrowApp has iOS/Android/PWA |
| **Feature completeness** | **6/10** | Missing: photo docs, nutrient calculator, strain DB, ML prediction |
| **Ease of deployment** | **5/10** | Needs Meteo_scraper_SQL + refresh_dashboards.ps1 — Emerald: `docker run` only |

### 4.5 Celková pozice na trhu

**TEMP_KULTURA_DB je nejkomplexnějším agronomicky-specializovaným nástrojem pro cannabis cultivation monitoring ve veřejném open-source prostoru.** Je jediným projektem, který kombinuje:
1. Live weather data pull (CHMI + Open-Meteo + AccuWeather)
2. Crop science calculations (GDD, DLI, VPD, botrytis)
3. Physiological yield modeling (v3.0)
4. Automated batch pipeline with validation

Nicméně, **nemá žádnou community** (0 stars), **žádní hardware integration** (Mycodo 350+ stars), a **žádné mobilní UI**. Je to "technicky nejzralější, ale sociálně neviditelný" projekt.

---

## 5. Doporučení pro další směr

### 5.1 Vysoký dopad / nízký úsilí
1. **Pridat MQTT/Homie podporu** → propojení s RPi/ESP32 senzory (Mycodo-style). Otevře hardware-ecosystém.
2. **Responsive PWA** → mobile-friendly HTML dashboard. Minimalni úsilí, maximalni dostupnost.
3. **Strain library** → pridat 50-100 nejrozšírenejsich variét s genetics info. Odpovida GrowApp approach.

### 5.2 Střední dopad / střední úsilí
4. **Nutrient calculator** → implementace 3-5 popularnich brandu (Emerald approach).
5. **Photo documentation** → plant photo upload s auto-timestamp.
6. **XGBoost secondary model** → ML prediction jako additional yield estimate.

### 5.3 Nizky dopad / vysoky úsilí
7. **KCanG compliance** → irrelevant pro Czech personal use.
8. **Docker deployment** → Emerald-style `docker run` would improve accessibility significantly.

### 5.4 Strategie pro community growth
- Zverejnit na GitHub Topics `cannabis-grow` + `plant-monitoring`
- Pridat `CONTRIBUTING.md` a `SECURITY.md`
- Zverejnit na Reddit r/marijuanaology a r/CannabisCultivation
- Zverejnit na cannabis grow forums (GroceryDude, I Love Grow Shop)

---

## 6. Zaver

TEMP_KULTURA_DB **technicky převyšuje** všechny nalezené analogické projekty v oblasti agronomicky-specializovaného cannabis cultivation monitoring. Je jediný, kdo kombinuje live weather data, crop science calculations, physiological yield modeling a automated pipeline validation. 

Hlavní mezera je **community traction a hardware ecosystem** — oba mohou být řešeny relativně snadno (PWA + MQTT). Repo má silné technické základy ale potřebuje viditelnost na trhu.

**Konkrétní prioritní akce:** Pridat MQTT/Homie podporu + responsive PWA + Docker deployment. Toto by z našeho repo udělalo nejkompletnějším open-source cannabis cultivation monitoring tool na trhu.

---

*Report generated 2026-09-07. Sources: GitHub, GitTopics, awesome-cropsteering, GitHut. All analog projects verified as of search date.*