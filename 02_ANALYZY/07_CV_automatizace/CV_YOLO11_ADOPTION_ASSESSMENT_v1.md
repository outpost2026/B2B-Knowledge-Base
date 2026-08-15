# CV/YOLO11 Adopce — Kompetenční fit analýza & GO/NO-GO

**Autor:** Ondřej Soušek | **Datum:** 2026-08-05 | **Verze:** 1.0
**Kontext:** Zhodnocení akvizice nové domény (Computer Vision / YOLO11) vůči stávajícímu portfoliu. Cíl = kvalifikované rozhodnutí GO/NO-GO s měřitelnými metrikami.

---

## 1. STÁVAJÍCÍ STACK — Co už autor umí (z KB + GitHub)

### 1.1 Core kompetence (doloženo kódem)

| Skill | Level | Důkaz | Relevance pro CV |
|-------|:-----:|-------|:-----------------|
| **Python 3.11/3.12** | Expert | 7 repů, ~18K LOC, 2 produkční parsery | ✅ Přímý — YOLO11 = Python |
| **Reverzní inženýrství** | Expert | VCF RE, 29 dní, 22 iterací, IEEE 754 | ✅ Transfer — RE obrazu = CV |
| **GCP Cloud** | Produkční | Cloud Run, Firestore, 6 služeb | ✅ Přímý — backend pro CV data |
| **Docker** | Produkční | python:3.11-slim → Cloud Run | ✅ Přímý — deploy modelu |
| **IoT/ESP32** | Produkční | Security perimeter, PIR, Doppler | ✅ Přímý — kamera jako senzor |
| **Golden Master Testing** | Expert | Baseline JSON diff, determinism | ✅ Transfer — validace modelu |
| **Data Pipeline (ETL)** | Produkční | Meteo miner, RAG, scraping | ✅ Přímý — zpracování snímků |
| **Streamlit** | Produkční | Dashboard na GCP | ✅ Přímý — vizualizace výsledků |

### 1.2 Know-how z CNC/CAM domény

| Znalost | Relevance pro garden CV |
|---------|------------------------|
| VCutWorks / Ruida controller | Pochopení proprietárních systémů → YOLO11 = další proprietární nástroj |
| DXF pipeline + ACI barvy | Mapování barev → detekce zdraví rostlin přes barvu |
| Materiály (PET felt, dřevo) | Pochopení fyzikálních vlastností → světlo, odraz, stíny |
| Vodní paprsek (kerf, tolerances) | Měření ±2mm → přesná kalibrace kamery |

### 1.3 Kognitivní profil (z portfolio auditu)

| Dimenze | Hodnota | Dopad na CV adopci |
|---------|:-------:|-------------------|
| **Otevřenost** | 95% | ✅ Vysoká — ochota učit se novou doménu |
| **Svědomitost** | 85% | ✅ Vysoká — systematický přístup k tréninku |
| **Učení** | Imersivní, learning-by-doing | ✅ Ideální pro CV (projekt řízený) |
| **Myšlení** | Systémové, bottom-up, first-principles | ✅ RE = stejný pattern jako CV pipeline |
| **Determinismus** | Velmi vysoký | ⚠️ CV je pravděpodobnostní — nutná adaptace |

---

## 2. GAP ANALÝZA — Co autor NEUMÍ (a co potřebuje)

### 2.1 Technické gapy

| Gap | Úroveň autora | Požadavek CV | Čas na zacelení |
|-----|:-------------:|:------------|:---------------:|
| **ML/CV frameworky** | 0 (nikdy nepoužil) | YOLO11, OpenCV, PyTorch | 20–30 h |
| **Annotace datasetů** | 0 | LabelImg, Roboflow, SAM 2 | 5–10 h |
| **Hardware (kamera)** | 0 (má ESP32, ne kameru) | Pi Camera, USB kamera | $50 + 2 h |
| **Edge computing (RPi)** | 0 (má ESP32, ne RPi) | Raspberry Pi 5 | $35 + 2 h |
| **Pravděpodobnostní myšlení** | Deterministický | mAP, confidence, thresholdy | 5–10 h |

### 2.2 Co NEBLOKUJE implementaci

| Položka | Proč neblokuje |
|---------|---------------|
| TensorFlow/PyTorch expert | YOLO11 = Ultralytics API, nepotřebuješ PyTorch přímo |
| GPU na trénink | Google Colab T4 = zdarma |
| Enterprise ML pipeline | hobby projekt, stačí cron + Python skript |
| Kubernetes | RPi = edge, žádná orchestrace |

---

## 3. TRANSFER SKILL MATRIX — Co se přenáší

### 3.1 Přímý transfer (0 h přípravy)

| Existující skill | Aplikace v CV |
|-------------------|---------------|
| Python OOP + testing | Tréninkový pipeline, inference kód |
| GCP Cloud Run + Firestore | Backend pro uložení výsledků |
| Dockerfile | Deploy modelu |
| ETL pipeline (meteo miner) | Zpracování snímků → data |
| Streamlit dashboard | Vizualizace přírůstků |
| Telegram bot (IoT) | Denní reporty |

### 3.2 Near-transfer (5–10 h přípravy)

| Existující skill | Aplikace v CV |
|-------------------|---------------|
| RE binárních formátů | RE obrazu — hledání struktur v pixelech |
| Golden master testing | Validace modelu (baseline snímky) |
| ACI barevné mapování | Detekce zdraví přes barvu koruny |
| ESP32 senzory | Kamera = další senzor v pipeline |
| Deterministický pipeline | Kombinace CV výstupů + deterministická pravidla |

### 3.3 Novel learning (20–30 h přípravy)

| Nová dovednost | Proč ji potřebuje | Zdroj učení |
|----------------|-------------------|-------------|
| YOLO11 API (Ultralytics) | Trénink + inference | docs.ultralytics.com |
| OpenCV (základy) | Zpracování obrázků | learnopencv.com |
| Bounding box + reference object | Měření výšky v cm | Roboflow tutorial |
| Annotace datasetu | Trénovací data | Roboflow / LabelImg |
| Edge inference (NCNN/ONNX) | Běh na RPi | ultralytics export docs |

---

## 4. ADAPTAČNÍ KŘIVKA — Odhad času

### 4.1 Fáze učení (paralelní s implementací)

```
Den 1–2: YOLO11 basics (5 h)
  ├── Ultralytics install + first inference (1 h)
  ├── Pochopení bounding box, confidence, NMS (2 h)
  └── Roboflow tutorial: Plant Height Measurement (2 h)

Den 3–4: Dataset + annotace (5 h)
  ├── Nasnímat 50 obrázků (1 h)
  ├── Annotace na Roboflow (3 h)
  └── Augmentace + rozdělení (1 h)

Den 5: Trénink (3 h)
  ├── Google Colab T4 (1 h)
  ├── Trénink YOLO11n-seg (1 h)
  └── Validace mAP (1 h)

Den 6–7: Deploy + integrace (5 h)
  ├── Export modelu na RPi (1 h)
  ├── Inference pipeline (2 h)
  └── Integrace s GCP + Telegram (2 h)
```

**Celkem: ~18–25 h** (3–4 dny soustředěné práce)

### 4.2 Srovnání s historickými adaptacemi

| Adaptace | Čas | Výsledek |
|----------|:---:|----------|
| Python 0 → VCF parser | ~120 h (3 měsíce) | Produkční, 99.98% |
| GCP 0 → Cloud Run deploy | ~45 h (6 týdnů) | 6 služeb, produkční |
| ESP32 0 → Security perimeter | ~30 h | Produkční koncept |
| **YOLO11 0 → Garden Monitor** | **~25 h (odhad)** | **Hobby produkt** |

**Pattern:** Autor se učí nové domény za 25–120 h v závislosti na složitosti. YOLO11 = jednodušší než VCF RE (není třeba dešifrovat binární formát bez dokumentace).

---

## 5. RIZIKA A MITIGACE

### 5.1 Klíčové riziko: Determinismus vs. pravděpodobnostnost

| Aspekt | Autorův přístup | CV realita | Mitigace |
|--------|----------------|-----------|----------|
| Výstup | "0% halucinací" | "95% mAP" | Akceptovat, že CV = pravděpodobnostní |
| Testování | Golden master (100% match) | mAP > 80% = OK | Definovat "dostatečnou" přesnost |
| Kalibrace | Přesný výpočet | ±2–3 cm tolerance | Referenční objekt + kalibrace |

**Mitigace:** Kombinace CV (probabilistický) + deterministická pravidla. Např.:
- CV řekne "toto je AP3, výška 101 cm, confidence 0.92"
- Deterministický filtr: "pokud confidence < 0.7, přeskočit"
- Deterministický trend: "pokud Δ výška > 10 cm/den, anomálie"

### 5.2 Ostatní rizika

| Riziko | Pravděpodobnost | Dopad | Mitigace |
|--------|:--------------:|:-----:|----------|
| Selhání tréninku (nízký mAP) | Střední | Střední | Retrénovat s více daty, augmentace |
| Hardware selže (RPi, kamera) | Nízká | Nízký | Záložní SD karta, watchdog |
| Špatné osvětlení (outdoor) | Vysoká | Střední | Fixní čas snímání (12:00) |
| Autor ztratí zájem (scope creep) | Nízká | Vysoký | Držet se MVP: 1 kamera, 9 rostlin |

---

## 6. FIT SCÓRE — Kvantitativní hodnocení

### 6.1 Skill match matrix

| Požadavek CV | Autorův match | Skóre |
|-------------|:-------------:|:-----:|
| Python | Expert | 10/10 |
| Hardware (kamera, RPi) | 0 (má ESP32) | 3/10 |
| ML/CV framework | 0 | 2/10 |
| Annotace/dataset | 0 | 2/10 |
| GCP/backend | Produkční | 9/10 |
| Edge computing | 0 (má koncept) | 4/10 |
| Data pipeline | Produkční | 9/10 |
| Testování | Expert | 10/10 |
| **Průměr** | | **6.1/10** |

### 6.2 Learning capacity score

| Metrika | Hodnota |
|---------|:-------:|
| Čas na adaptaci (odhad) | 25 h |
| Historická rychlost učení | 120 h → produkce (VCF) |
| Poměr složitosti CV / VCF RE | ~0.3 (CV je jednodušší) |
| Predikovaný čas na MVP | 3–4 dny |
| **Learning Capacity Score** | **8/10** |

### 6.3 Celkové skóre

| Faktor | Váha | Skóre | Vážené |
|--------|:----:|:-----:|:------:|
| Skill match | 40% | 6.1/10 | 2.44 |
| Learning capacity | 30% | 8/10 | 2.40 |
| Doménová relevance (CNC→CV) | 20% | 7/10 | 1.40 |
| Infrastruktura (GCP, IoT) | 10% | 8/10 | 0.80 |
| **CELKEM** | | | **7.04/10** |

---

## 7. GO/NO-GO ROZHODNUTÍ

### ✅ VERDICT: GO — S podmínkami

**Důvody pro GO:**
1. **Python = 10/10** — YOLO11 je čistě Python API
2. **Rychlost učení = 8/10** — historicky adaptuje nové domény za 25–120 h
3. **IoT infrastruktura existuje** — ESP32, GCP pipeline, Telegram = stačí přidat kameru
4. **CNC transfer = 7/10** — měření, kalibrace, barevné mapování = přímý crossover
5. **Náklady = minimální** — $105 HW + 25 h času

**Podmínky GO:**
1. **Držet se MVP** — 1 kamera, 9 rostlin, 1 metrika (výška). Žádný scope creep.
2. **Akceptovat pravděpodobnostnost** — CV není RE. Confidence 90% = úspěch, ne selhání.
3. **Referenční objekt = povinný** — bez kalibrace jsou čísla k ničemu.
4. **Fixní čas snímání** — 12:00, fixní úhel, žádné experimenty s úhlem.

### 📊 Metriky úspěchu

| Metrika | Cíl | Minimální |
|---------|:---:|:---------:|
| mAP50 na test setu | > 85% | > 70% |
| Přesnost výšky (vs. ruční) | ±3 cm | ±5 cm |
| Detekce všech 9 rostlin | 9/9 | 7/9 |
| Denní uptime | > 90% | > 70% |
| Čas na MVP | 4 dny | 7 dní |

### 🚫 NO-GO podmínky (kdyby selhalo)

- Po 7 dnech žádný funkční inference → retrénovat nebo ukončit
- mAP50 < 50% ani po retrénování → doména příliš složitá pro hobby projekt
- Autor ztratí zájem → uložit do KB jako "budoucí projekt"

---

## 8. DOPORUČENÍ — Implementační plán

### 8.1 Týden 1: MVP (DEN 1–4)

| Den | Úkol | Čas |
|:---:|------|:---:|
| 1 | YOLO11 install, první inference, pochopení API | 3 h |
| 2 | Nasnímat 50 snímků, annotace na Roboflow | 4 h |
| 3 | Trénink na Colab T4, validace | 3 h |
| 4 | Deploy na RPi, inference pipeline, Telegram report | 4 h |

### 8.2 Týden 2: Kalibrace + integrace

| Den | Úkol | Čas |
|:---:|------|:---:|
| 5–6 | Kalibrace (porovnání CV vs. ruční měření) | 2 h |
| 7 | Integrace s GCP pipeline (iot-ingest-beta) | 2 h |
| 8 | Finalizace, dokumentace do KB | 1 h |

### 8.3 Investiční přehled

| Položka | Cena | Čas |
|---------|:----:|:---:|
| RPi 5 + kamera | $85 | – |
| MicroSD | $10 | – |
| Mount (tyč) | $10 | – |
| **Celkem HW** | **$105** | – |
| Dataset + annotace | $0 | 5 h |
| Trénink (Colab) | $0 | 3 h |
| Deploy + integrace | $0 | 6 h |
| **Celkem SW** | **$0** | **14 h** |
| **CELKEM** | **$105** | **~25 h** |

---

## 9. ZÁVĚR

**CV/YOLO11 je pro autora vhodná adopce z následujících důvodů:**

1. **Skill overlap je vysoký** — Python, GCP, IoT, data pipeline, testování = vše přenositelné
2. **Historická rychlost učení** — 0 → produkce za 3 měsíce (VCF). CV = jednodušší doména.
3. **Náklady minimální** — $105 + 25 h = nejlevnější hobby projekt v portfoliu
4. **Doménová synergicnost** — měření, kalibrace, barevné mapování = přímý crossover z CNC
5. **Přidaná hodnota** — nový skill v portfoliu (CV/ML), diferenciace od ostatních Python developerů

**Hlavní riziko:** Autorův deterministický mindset může kolidovat s pravděpodobnostní povahou CV. Mitigace: kombinace CV výstupů s deterministickými pravidly.

**Celkové skóre: 7.04/10 = GO**

---

*Assment vychází z: portfolio_audit_a_match.md, github_portfolio_digital_twin.json, github_portfolio_analysis.md, GROUND_TRUTH, R&D_evoluce_portfolia, SMALL_MODELS_CV_ASPIRACNI_PROJEKTY_v1.md, YOLO11_GARDEN_MONITOR_GLOSSARY_KONCEPT_v1.md*
