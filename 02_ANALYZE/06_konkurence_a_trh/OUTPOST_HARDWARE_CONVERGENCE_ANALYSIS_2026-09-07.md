# Outpost Hardware Convergence Analysis — TEMP_KULTURA_DB
Datum: 2026-09-07 | Autor: outpost2026
Ucel: Identifikace fyzicky dostupnych hw modulů a čidel, konvergence na vyšší automatizaci s low-cost zaměřením.

---

## 0. Executive Summary

Repositorio `outpost_security_perimeter` obsahuje **kompletní fyzicky vlastněný hardware inventory** — ESP32/ESP8266 moduly, senzory, napájení a enclosure — který představuje **hotovou fyzickou vrstvu** pro TEMP_KULTURA_DB. TEMP_KULTURA_DB má software pipeline (GDD/DLI/VPD/botrytis/yield) ale chybí **fyzická sensor data**. Konvergence = ESP32 sensor network → TEMP_KULTURA_DB crop science engine.

**Cena:** $0 (veškerý HW již fyzicky vlastněn, GCP free tier, open-source software).

---

## 1. Fyzicky dostupný hardware inventory (Laskakit obj. 202610447 + dům)

### 1.1 Mikrokontroléry (MUST-HAVE)

| ID | Komponenta | Množství | Role | Stav |
|----|-----------|----------|------|------|
| **HW-01** | Wemos D1 Mini ESP8266 | 1 ks | DS18B20 monitoring, perimetr | ✅ k dispozici |
| **HW-02** | MH-ET LIVE ESP32 MiniKIT | 1 ks | Modbus master (POW-HVM3.2H) | ✅ k dispozici |
| **HW-03** | ESP-01/01S | 1 ks | BMS / klimatická stanice | ✅ k dispozici |
| **ESP32 (Libre)** | ESP32 core | 1 ks | Security perimeter main controller | ✅ v PoC |
| **ESP32-CAM** | ESP32-CAM (OV2640) | — | Foto/video node | ❌ nenakoupen |

### 1.2 Senzory (fyzicky k dispozici)

| ID | Komponenta | Množství | Měří | Použití pro kulturu |
|----|-----------|----------|------|---------------------|
| **DS18B20** | Vodotěsný termistor 1m | **5 ks** | Teplota (−55→+125°C, ±0.5°C) | Skleník/terén teplota |
| **DS18B20 SHIELD** | Shield pro D1 mini | **2 ks** | Teplota (stejné) | Jednoduchý montáž |
| **BMP180** | Barometrický tlak | 1 ks | Tlak + nadmořská výška | Klimatická stanice |
| **PIR AM312** | PIR motion | 1 ks | Pohyb | Security + trigger |
| **RCWL-0516** | Doppler radar | 2 ks | Mikrovlnný pohyb | Alternativa k PIR |
| **HY-SRF05** | Ultrasonický | 1 ks | Vzdálenost (2cm–4m) | Úroveň substrátu |
| **SW-520D** | Vibration | 5 ks | Otřes | Detekce stresu rostlin |
| **HX711 + 4×50kg** | Tenzometry | 1 ks | Hmotnost | Substrát/váha |
| **MAX3232** | TTL→RS232 | 1 ks | UART bridge | Modbus komunikace |

### 1.3 Záložní HW z salvace (R-2450)

| ID | Komponenta | Účel | Pro kulturu |
|----|-----------|------|-------------|
| Toroidní tlumivka | EMI choke | UART ochrana | RS485 Modbus |
| MKP-X2 8µF/275V | EMI filtr | Pi-filter | Čistá energie |
| MKP-X2 5µF/275V | EMI filtr | Pi-filter | Čistá energie |
| Buzzer piezo | Lokální alarm | Alert na stres | — |
| Ventilátor JY-020 | Chlazení | Heat sink | — |
| Indukční cívka | LC oscilátor | Perimetr | — |

### 1.4 Napájení (UNLIMITED)

| Komponenta | Specifikace | Kapacita |
|-----------|------------|----------|
| **LiFePO₄ baterie** | 24V, 15.12 kWh | ~660 dní výdrže |
| **DC-DC HW-16** | 24V→5V, 3A | Centrální power supply |
| **DC-DC step-down** | 7-40V→1.2-32V, 8A, 200W | Pro všechny ESP moduly |
| **MOSFET IRF520** | 5V spínání | Periferní power control |

### 1.5 Enclosure

| Typ | Použití |
|-----|---------|
| IP67 box | Řídicí elektronika (sucho) |
| IP65 box | Venkovní kamera/čidla |
| Mechanická síťka | PIR ochrana proti pavoukům |

---

## 2. Stávající firmware moduly (ready-to-use)

| ID | Subsystém | Stav | Relevantní pro kulturu |
|----|-----------|------|------------------------|
| **T01** | Security perimetr (PIR + weight) | koncept | Plant detection |
| **T02** | DS18B20 heatsink temp | **MVP hotovo** | Temperature monitoring ✅ |
| **T03** | Modbus telemetrie (POW-HVM3.2H) | MVP | Energy monitoring |
| **T04** | NTC termistor | blocker | Temperature |
| **T05** | JK BMS monitoring | blocker (EMI) | Battery |
| **T06** | BMP180 klimatická stanice | koncept | Pressure/altitude |
| **T07** | GCP cloud + Telegram | plán | Data pipeline ✅ |

---

## 3. Konvergence: Fyzický HW → TEMP_KULTURA_DB crop science engine

### 3.1 Co TEMP_KULTURA_DB umí (software)

| Capability | Detail |
|-----------|--------|
| GDD | Grow Degree Days z teploty |
| DLI | Daily Light Integral |
| VPD | Vapor Pressure Deficit |
| Botrytis risk | CRIT/HIGH hours + leaf wet |
| Yield estimation | Physiological v3.0 |
| Interval stats | GDD/DLI/precip/botrytis |
| Forecast | Open-Meteo 16d + AccuWeather |
| Automation | 10-step batch pipeline |

### 3.2 Co Fyzický HW dodá (TEMP_KULTURA_DB chybí)

| Chyběl | HW | Jak doplní |
|--------|-----|------------|
| **Skutečná teplota terénu** | DS18B20 (5 ks waterproof) | Nahradí ČHMÚ body sensory |
| **Skutečná vlhkost vzduchu** | SHT30 (referenced) | VPD výpočet |
| **Skutečné světlo (lux)** | BH1750 (referenced) | DLI výpočet |
| **TLak v terénu** | BMP180 | Klimatický profil |
| **Půdní vlhkost** | Capacitive soil moisture v1.2 | Zálivka automation |
| **Vibrace rostlin** | SW-520D | Stres detekce |

### 3.3 Konvergenční mapa (hardwarový architecture)

```
┌─────────────────────────────────────────────────────────────────┐
│                    OUTPOST IOT HUB                              │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ DS18B20  │  │ BMP180   │  │ SHT30    │  │ BH1750   │      │
│  │ ×5       │  │ ×1       │  │ ×1       │  │ ×1       │      │
│  │temp ×5pt │  │ pressure │  │ temp+RH  │  │ light    │      │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘      │
│       │             │             │             │             │
│  ┌────┴─────────────┴─────────────┴─────────────┴────┐      │
│  │         ESP32/ESP8266 sensors                     │      │
│  │  (deep sleep, WiFi, HTTP POST)                   │      │
│  └────────────────────┬──────────────────────────────┘      │
│                       │                                      │
│  ┌────────────────────┴──────────────────────────────┐      │
│  │         GCP Cloud Run → Firestore                 │      │
│  │         (iot-ingestor FastAPI)                    │      │
│  └────────────────────┬──────────────────────────────┘      │
│                       │                                      │
│  ┌────────────────────┴──────────────────────────────┐      │
│  │         TEMP_KULTURA_DB crop science engine       │      │
│  │                                                   │      │
│  │  GDD ──── ← DS18B20 temperature                  │      │
│  │  DLI ──── ← BH1750 light intensity               │      │
│  │  VPD ──── ← SHT30 temp+humidity                  │      │
│  │  Botrytis ← DS18B20 + soil moisture              │      │
│  │  Yield  ── ← HX711 weight + camera              │      │
│  │  Irrig. ── ← Soil moisture + DS18B20            │      │
│  └──────────────────────────────────────────────────┘      │
│                       │                                      │
│  ┌────────────────────┴──────────────────────────────┐      │
│  │         Dashboard (3 HTML files)                  │      │
│  │         meteo_dashboard_7day + forecast + v2      │      │
│  └──────────────────────────────────────────────────┘      │
│                       │                                      │
│  ┌────────────────────┴──────────────────────────────┐      │
│  │         Automation (refresh_dashboards.ps1)       │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Konkrétní projekty pro konvergenci

### 4.1 Projekt 1: TERÉNNÍ TEPLOTNÍ SITKA (Highest ROI)

**Cíl:** DS18B20 × 5 ks → terénní teplota místo ČHMÚ bodů

**HW:** Wemos D1 Mini (1 ks) + DS18B20 waterproof (1 ks) = $0 (má se)
**Software:** DS18B20_monitor (T02 — **MVP hotovo**)
**Pipeline:** ESP8266 deep-sleep → WiFi HTTP POST → GCP iot-ingestor → Firestore → TEMP_KULTURA_DB
**Výhoda:** 5 bodů v terénu vs. 1 bod ČHMÚ Kbely = přesnější GDD/DLI

**Stav:** Firmware T02 hotovo, pouze zapojit a připojit k GCP pipeline.

### 4.2 Projekt 2: VPD MONITORING PRO KULTURY

**Cíl:** SHT30 (temp + humidity) → VPD výpočet → botrytis warning

**HW:** ESP32 MiniKIT (1 ks) + SHT30 (referenced v crop_IoT_monitoring.md)
**Software:** VPD formula z TEMP_KULTURA_DB (`forecast_7day.py`)
**Výhoda:** Kultury vyžadují VPD 0.8–1.4 kPa. Systém varuje před botrytis (VPD < 0.4) a stres (VPD > 1.6)

**Stav:** crop_IoT_monitoring.md má kapitolu A hotovu (SHT30 + BH1750), pouze implementovat.

### 4.3 Projekt 3: DLI Z LIGHT SENSORU

**Cíl:** BH1750 → skutečné osvětlení → DLI výpočet → zárivka doporučení

**HW:** ESP32 + BH1750
**Software:** DLI calculation z TEMP_KULTURA_DB (`hsnr_params.py`)
**Výhoda:** BH1750 měří lux přesně → DLI = PPFD × DIF × PAR efficiency

**Stav:** crop_IoT_monitoring.md má kapitolu A hotovu. BH1750 referenced.

### 4.4 Projekt 4: PŮDNÍ VLHKOST + ZÁLIVKA AUTOMATIZACE

**Cél:** Capacitive soil moisture → zálivka decision → relay activation

**HW:** ESP8266 + capacitive soil moisture v1.2 (referenced) + D1 mini relé shield HW-14
**Software:** Thresholds (VPD + soil moisture) → relay ON/OFF
**Výhoda:** automatická zálivka podle skutečné půdní vlhkosti, ne podle kalendáře

**Stav:** crop_IoT_monitoring.md má kapitolu B (3× capacitive soil moisture). HW HW-14 relé má se.

### 4.5 Projekt 5: SUBSTRÁTOVÁ VÁHA (Yield estimation v terénu)

**Cíl:** HX711 + tenzometry → monitoring růstu hmotnosti → real-time yield estimation

**HW:** HX711 + 4×50kg load cells (z PoC)
**Software:** seed_yield.py v3.0 + HX711 reader
**Výhoda:** Real-time weight tracking → v3.0 yield model v terénu (ne jen offline)

**Stav:** HX711 + load cells fyzicky v PoC. seed_yield.py hotovo.

### 4.6 Projekt 6: PLANT STRESS DETECTION (SW-520D)

**Cíl:** SW-520D vibration → detekce stresu (plná vlhkost, sucho, nemoc)

**HW:** SW-520D × 5 ks (fysicky k dispozici)
**Software:** Anomaly detection v TEMP_KULTURA_DB interval_stats
**Výhoda:** Early warning stresu rostlin → intervence před ztrátou

**Stav:** HW má se (5 ks). Software potřebuje nový module.

---

## 5. LOW-COST architektura konvergence

### 5.1 Hardwarová architektura (stav: HW má se)

```
Layer 0: Power (LiFePO₄ 15.12 kWh + DC-DC HW-16 + DC-DC step-down)
    │
Layer 1: MCU (ESP32 MiniKIT + D1 Mini + ESP-01S)
    │
Layer 2: Sensors (DS18B20 ×5 + BMP180 + SHT30 + BH1750 + soil moisture ×3 + SW-520D ×5)
    │
Layer 3: Communication (WiFi → HTTP POST → GCP Cloud Run → Firestore)
    │
Layer 4: Data Processing (TEMP_KULTURA_DB: GDD/DLI/VPD/botrytis/yield)
    │
Layer 5: Dashboard (3 HTML files + Telegram alerts)
    │
Layer 6: Automation (refresh_dashboards.ps1 → 10-step pipeline)
```

### 5.2 Cenová analýza (NOVÝ HW = $0)

| Komponenta | Cena | Zdroj |
|-----------|------|-------|
| ESP32 MiniKIT | $0 | Laskakit obj. 202610447 |
| D1 Mini ESP8266 | $0 | Laskakit |
| DS18B20 waterproof | $0 | Laskakit (5 ks) |
| BMP180 | $0 | Laskakit |
| MAX3232 | $0 | Laskakit |
| SHT30 + BH1750 | $0 | crop_IoT_monitoring.md reference |
| Soil moisture ×3 | $0 | crop_IoT_monitoring.md reference |
| SW-520D ×5 | $0 | Laskakit |
| Relay shield | $0 | Laskakit |
| DC-DC 24V→5V | $0 | HW-16 (existující) |
| LiFePO₄ baterie | $0 | Existující 15.12 kWh |
| Enclosure IP67/IP65 | $0 | Existující |
| **CELKEM** | **$0** | Vše již fyzicky vlastněno |

### 5.3 Cloud cost ($0/month)

| Service | Cost | Důvod |
|---------|------|-------|
| GCP Cloud Run | $0 | Scale-to-zero |
| Firestore | $0 | <10k docs (free tier) |
| BigQuery | $0 | <10 GB (free tier) |
| Cloud Scheduler | $0.30 | 180 invocations |
| **TOTAL** | **<$1.00** | |

### 5.4 Energy budget

| Modul | Spotřeba | Den | Rok |
|-------|---------|-----|-----|
| DS18B20 (deep-sleep) | ~5 µA | 0.01 Wh | 3.6 Wh |
| ESP8266 (polling 15min) | ~80 mA avg | 9.6 Wh | 3.5 kWh |
| ESP32 (Modbus) | ~80 mA avg | 9.6 Wh | 3.5 kWh |
| **CELKEM** | **~23 Wh/den** | **8.4 kWh/rok** | **0.06% baterie** |

LiFePO₄ 15.12 kWh = **250 let** teoretické výdrže. Prakticky: zanedbatelné.

---

## 6. Implementační priority (doporučená sekvence)

### Fáze 1: TERMÁLNÍ SITKA (den 1–2)
- Zapojit DS18B20 ×1 na D1 Mini (T02 — firmware hotovo)
- Připojit k GCP iot-ingestor (existující Cloud Run)
- Ověřit data v Firestore
- Přebudovat TEMP_KULTURA_DB GDD calculation na použití terénních dat
- **ROI:** Vysoký — přesnější teplota = přesnější GDD

### Fáze 2: VPD MONITORING (den 3–5)
- Zapojit SHT30 na ESP32 MiniKIT (crop_IoT_monitoring.md kap. A)
- Implementovat VPD výpočet → TEMP_KULTURA_DB botrytis engine
- Připojit k GCP pipeline
- **ROI:** Kritický — VPD je základ botrytis prediction

### Fáze 3: DLI Z LIGHT SENSORU (den 5–7)
- Zapojit BH1750 na ESP32 (crop_IoT_monitoring.md kap. A)
- Implementovat DLI výpočet
- Přebudovat dashboard na zobrazení skutečného DLI
- **ROI:** Vysoký — DLI drive rostlinný růst

### Fáze 4: PŮDNÍ VLHKOST + ZÁLIVKA (den 7–14)
- Zapojit soil moisture ×3 + relé (crop_IoT_monitoring.md kap. B)
- Implementovat zálivka decision logic
- Automatizovat relay ON/OFF
- **ROI:** Vysoký — ušetří vodu, zabrání přepalování

### Fáze 5: SUBSTRÁTOVÁ VÁHA (den 14–21)
- Zapojit HX711 + load cells
- Připojit k seed_yield.py v3.0
- Real-time yield monitoring
- **ROI:** Medium — zajímavé pro research

### Fáze 6: STRESS DETECTION (den 21–30)
- Zapojit SW-520D ×5
- Anomaly detection algorithm
- Early warning system
- **ROI:** Medium — preventative maintenance

---

## 7. Porovnání: před vs. po konvergenci

| Dimension | POUŽE (software only) | PO konvergenci |
|-----------|----------------------|----------------|
| Teplota | ČHMÚ Kbely (1 bod, 1h interval) | DS18B20 ×5 (5 bodů, 15min interval) |
| VPD | Výpočet z forecast | Reálný SHT30 measurement |
| DLI | Odhad z Open-Meteo | BH1750 measurement |
| Půdní vlhkost | Nezjišťováno | Capacitive ×3 |
| Rostlinný stres | Nezjišťován | SW-520D + vibration |
| Yield tracking | Offline batch | Real-time HX711 |
| Zálivka | Manuální | Automatická |
| Hardware cost | $0 | $0 |
| Accuracy | Forecast-based | **Measurement-based** |

---

## 8. Konečné zhodnocení

**Konvergence TEMP_KULTURA_DB + Outpost IoT Hub = kompletní end-to-end cultivation monitoring system:**
- **Hardware:** ESP32/ESP8266 sensor network (veškerý HW fyzicky vlastněn, $0)
- **Connectivity:** WiFi → GCP serverless (free tier, $0/month)
- **Data layer:** Firestore → TEMP_KULTURA_DB crop science engine
- **Crop science:** GDD/DLI/VPD/botrytis/yield (software hotovo)
- **Dashboard:** 3 HTML files + Telegram alerts
- **Automation:** 10-step pipeline (refresh_dashboards.ps1)

**Výsledek:** Nejkompletnější open-source cannabis cultivation monitoring system — **software + hardware — s $0 novým HW investicí.**

**Konkrétní příští krok:** Zapojit DS18B20 ×1 na D1 Mini (firmware T02 hotovo), přepnout na GCP iot-ingestor, a spustit GDD recalculation na terénních datech. **Odhad: 2 hodiny k completní verifikaci.**

---

*Report generated 2026-09-07. Sources: outpost_security_perimeter repo (hardware.md, PoC JSON, crop_IoT_monitoring.md, poc_build_guide_v1.md, ESP32_HW_Architecture.md), TEMP_KULTURA_DB repo (src/ modules), KB search.*