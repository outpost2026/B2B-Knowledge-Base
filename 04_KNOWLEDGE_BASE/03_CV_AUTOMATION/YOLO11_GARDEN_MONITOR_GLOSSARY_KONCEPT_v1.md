# YOLO11 Garden Monitor — Glossář, ontologie a konceptuální návrh

**Datum:** 2026-08-05 | **Autor:** outpost2026 | **Verze:** 1.0
**Účel:** Doménová ontologie pro začátečníka v CV/YOLO11 + konceptuální návrh systému pro monitorování přírůstků konopné kultury (9 rostlin, Zdiby).
**Kontext:** Autor je IoT junior, CV začátečník. Cíl = pochopení technologie před implementací.

---

## ČÁST 1: GLOSSÁŘ — Slovník pojmů pro CV začátečníka

### 1.1 Základní pojmy Computer Vision

| Pojem | Česky | Vysvětlení "jako pro dítě" |
|-------|-------|---------------------------|
| **Computer Vision (CV)** | Počítačové vidění | Naučit počítač, aby "viděl" a chpal obrázky/video, stejně jako člověk. |
| **Image** | Obrázek | Mřížka čísel (pixelů). Každý pixel = jedno číslo (0–255) pro barvu. |
| **Pixel** | Bod | Nejmenší stavební kámen obrázku. Obrázek 640×480 = 307 200 pixelů. |
| **Resolution** | Rozlišení | Kolik pixelů má obrázek. Vyšší = více detailů, ale větší soubor. |
| **Frame** | Snímek | Jeden obrázek z kamery. Video = 25–30 snímků za sekundu (FPS). |
| **FPS** | Snímků za sekundu | Jak rychle počítač "vidí". 30 FPS = plynulé video. 5 FPS = cukání. |
| **Inference** | Odhad / běh modelu | Okamžik, kdy AI model zpracuje jeden obrázek a řekne "toto je rostlina". |
| **Latency** | Zpoždění | Jak dlouho trvá jedno inference. 16 ms = rychlé. 500 ms = pomalé. |
| **Dataset** | Datová sada | Sada obrázků + odpovědi ("na tomto obrázku je rostlina AP1 na souřadnicích x,y"). |

### 1.2 YOLO specifické pojmy

| Pojem | Česky | Vysvětlení |
|-------|-------|-----------|
| **YOLO** | "You Only Look Once" | Rodina AI modelů, která se dívá na obrázek JEDNOU a okamžitě řekne, co je kde. Starší modely (YOLOv5, v8) se dívaly vícekrát. |
| **YOLO11** | Nejnovější verze | Verze z roku 2024/2025. Rychlejší + přesnější než YOLOv8. |
| **Backbone** | Hřbet / základna | Část modelu, která "dívá se" na obrázek a hledá znaky (hrany, barvy, textury). |
| **Head** | Hlava | Část modelu, která říká "toto je rostlina, tady je". |
| **Neck** | Krk | Propojuje backbone s headem. Filtruje a zjemňuje informace. |
| **Epoch** | Epocha | Jedno kompletní pročtení celého datasetu během tréninku. 50 epoch = model viděl každý obrázek 50×. |
| **mAP** | Mean Average Precision | Hlavní metrika přesnosti. mAP50 = 95% znamená, že model se trefí v 95 případech ze 100. |
| **Confidence** | Důvěra | Jak si je model jistý. 0.95 = "95% jistý, že tohle je rostlina". 0.3 = "nevím". |
| **NMS** | Non-Maximum Suppression | Odstraňuje duplicitní detekce ("našel jsem rostlinu 5× na stejném místě, ponechám jen jednu"). |

### 1.3 Typy CV úloh (co YOLO11 umí)

| Úloha | Co dělá | Příklad pro zahradu |
|-------|---------|-------------------|
| **Object Detection** | Najde objekty a nakreslí kolem nich čtverec (bounding box) | "Tady je rostlina AP1, tady je GG4" |
| **Instance Segmentation** | Jako detection, ale přesně obkreslí tvar (maska) | "Tady je přesný tvar listů AP1" |
| **Image Classification** | Řekne, CO je na obrázku (bez souřadnic) | "Tento obrázek = zdravá rostlina" |
| **Pose Estimation** | Najde klouby/body na objektu | "Tento list má 3 internodie" (pokročilé) |
| **OBB** | Oriented Bounding Box — čtverec se může otáčet | "Rostlina se naklání o 30°" |

### 1.4 Bounding Box — klíčový koncept

```
Bounding box (mezující čtverec) = nejjednodušší způsob, jak říct "tady je něco".

     x1,y1 ──────────────── (x1+w), y1
       │                      │
       │    ROSTLINA AP1      │  ← výška (height)
       │                      │
     x1, (y1+h) ────────── (x1+w), (y1+h)
              ← šířka (width) →

YOLO vrací: x_center, y_center, width, height
  x_center = x1 + width/2
  y_center = y1 + height/2
```

### 1.5 Referenční objekt — klíč pro přepočet na cm

```
Proč potřebujeme referenční objekt?
Protože obrázek = mřížka pixelů, nikoli centimetrů.

Příklad:
  Lahev 30 cm = 150 pixelů na snímku
  → 1 pixel = 30 cm / 150 = 0,2 cm
  → Rostlina 400 pixelů = 400 × 0,2 = 80 cm

Bez referenčního objektu víme JEN:
  "Rostlina je 2× vyšší než lahev"
  (ne kolik cm)
```

### 1.6 Trénink modelu — jak se "učí"

```
Postup:
1. Nasbírat obrázky (50–100 ks)
2. Ručně označit ("toto je AP1", "toto je GG4") = ANOTACE
3. Rozdělit: 70% trénink / 20% validace / 10% test
4. Spustit trénink (GPU, 30–60 minut)
5. Model se naučí rozpoznávat tvary, barvy, kontexty
6. Výsledek: soubor .pt (váhy modelu, 5–50 MB)
```

### 1.7 Edge vs. Cloud

| Přístup | Kde běží | Výhoda | Nevýhoda |
|---------|----------|--------|----------|
| **Cloud** | GCP/AWS server | Výkonné GPU, snadný start | Platíš za čas, závislost na internetu |
| **Edge** | Raspberry Pi / Jetson u kamery | Offline, rychlé, žádný internet | Méně výkonné, složitější setup |
| **Hybrid** | Edge inference + cloud uložení | Nejlepší z obou | Dvě platformy, větší složitost |

---

## ČÁST 2: DOMÉNOVÁ ONTOLOGIE — Mapa pojemů

### 2.1 Strom znalostí

```
Computer Vision (CV)
├── Object Detection
│   ├── YOLO rodina (YOLO11 = nejnovější)
│   │   ├── Backbone (feature extraction)
│   │   ├── Neck (FPN, C3k2, C2PSA)
│   │   └── Head (detekce + klasifikace)
│   ├── SSD (starší, pomalejší)
│   └── EfficientDet (pomalý, přesný)
├── Instance Segmentation
│   ├── YOLO11-seg (YOLO + maska)
│   ├── SAM 2 (Segment Anything)
│   └── Mask R-CNN (starší)
├── Image Classification
│   ├── YOLO11-cls (YOLO + klasifikace)
│   └── ResNet / EfficientNet
├── Pose Estimation
│   └── YOLO11-pose
└── Hardware
    ├── Raspberry Pi 5 (CPU, $35)
    ├── NVIDIA Jetson (GPU, $249–1999)
    ├── ESP32-CAM (ultra-low cost, $5)
    └── Kamery (USB, GigE, Pi Camera)
```

### 2.2 Pipeline: Od obrázku k číslu

```
KAMERA snímá (1× denně)
    ↓
OBRÁZEK (JPEG, 640×480)
    ↓
YOLO11n inference (5–50 ms)
    ↓
DETEKCE: [{class: "AP1", bbox: [x,y,w,h], conf: 0.94}, ...]
    ↓
REFERENČNÍ OBJEKT → pixel-to-cm přepočet
    ↓
METRIKY: výška (cm), plocha koruny (cm²), barva (zdraví)
    ↓
LOG do Firebase/BigQuery
    ↓
TELEGRAM report (denní)
```

---

## ČÁST 3: REFERNČNÍ IMPLEMENTACE — Co už existuje

### 3.1 Roboflow: Plant Height Measurement (2023)

**Zdroj:** [blog.roboflow.com/monitor-plant-growth](https://blog.roboflow.com/monitor-plant-growth/)
**GitHub:** [github.com/tim3in/plant_height_measurement](https://github.com/tim3in/plant_height_measurement)
**Dataset:** [Roboflow Universe – plantmo](https://universe.roboflow.com/tim-4ijf0/plantmo)

**Architektura:**
- Referenční objekt: 6-inch (15.24 cm) marker ve snímku
- Model: Object detection (YOLOv8/11)
- Metrika: pixel-to-inch conversion
- Přesnost: ±2 mm při stabilním úhlu kamery

**Klíčový kód (Python):**
```python
def establish_conversion_factor(reference_height, reference_pixel_height):
    return reference_height / reference_pixel_height

reference_height_inches = 6
conversion_factor = establish_conversion_factor(reference_height_inches, reference_pixel_height)
plant_height_inches = plant_pixel_height * conversion_factor
```

**Pro naši aplikaci:** 1:1 aplikovatelné. Referenční objekt = lahev 30 cm nebo pravítko.

### 3.2 FutureAIPlanet: Microgreens Height + YOLO11 (12/2025)

**Zdroj:** [futureaiplanet.com](https://www.futureaiplanet.com/2025/12/automated-microgreens-height-yolo11.html)

**Klíčové poznatky:**
- YOLO11 má vylepšenou detekci malých objektů (mikrobyliny)
- OpenCV contour detection selže při měnícím se světle (LED) — YOLO11 se učí features, ne threshold
- Referenční objekt = 2 cm blok → pixel-to-cm faktor
- Přesnost: ±2 mm při bočním pohledu (side-view)
- **Side-view > top-down** pro měření výšky

**Pro naši aplikaci:** Side-view kamera je klíčová. Top-down snímá plochu koruny, ne výšku.

### 3.3 Mendeley: Cannabis Growth Dataset (2025)

**Zdroj:** [data.mendeley.com/datasets/z2fp5kbgbh](https://data.mendeley.com/datasets/z2fp5kbgbh/1)

**Dataset obsahuje:**
- **Cannabis Dataset:** 24 hodin, hodinové intervaly, fixní úhel, COCO bounding box formát
- Tomato, Pepper, Cucumber datasety (stejný formát)
- Anotace: bounding boxes pro detekci a tracking růstu

**Pro naši aplikaci:** Přímo použitelný jako referenční dataset pro trénink. Cannabis obrázky = stejná doména.

### 3.4 Springer: Dual Model Approach (2025)

**Zdroj:** [link.springer.com/chapter/10.1007/978-3-031-97313-0_22](https://link.springer.com/chapter/10.1007/978-3-031-97313-0_22)

**Architektura:**
- YOLOv8s → detekce růstové fáze (germination, vegetative, flowering)
- YOLOv11cls → identifikace rostliny (druh/odrůda)
- Dual model = vyšší přesnost než jeden model na vše

**Pro naši aplikaci:** YOLO11-seg pro detekci + YOLO11-cls pro identifikaci AP/GG variant.

### 3.5 ScienceDirect: RGB-D + SAM Phenotyping (2026)

**Zdroj:** [sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S1537511026000164)

**Architektura:**
- RGB-D kamera (hloubková) + IoT
- SAM / FastSAM pro segmentaci
- Cloud pipeline pro analýzu
- Řeší překrývající se rostliny v hustém porostu

**Pro naši aplikaci:** Pokročilé. SAM řeší překryvy, ale pro 9 rostlin na záhonu stačí YOLO11-seg.

---

## ČÁST 4: KONCEPUÁLNÍ NÁVRH — Garden Monitor pro konopí

### 4.1 Systémový kontext

**Východiska z KB:**
- 9 rostlin: AP1, AP3, AP4, AP5, AP6, GG2, GG3, GG4, GG5
- 2 záhony (188×95 cm, 200×100 cm) + 1 květináč (AP1, ~40L)
- Stávající měření: 1× týdně ručně (výška cm + internodie)
- IoT infrastruktura: ESP32 + GCP pipeline (iot-ingest-beta)
- Cíl: každodenní log stavu a nárůstu

### 4.2 Architektura systému

```
┌─────────────────────────────────────────────────────────────────┐
│                    GARDEN CV NODE                                │
│                                                                  │
│  HARDWARE:                                                       │
│  ├── Raspberry Pi 5 (8 GB) — $35                                │
│  ├── Pi Camera 3 Wide nebo USB kamera (IMX477) — $50            │
│  ├── Pevný mount (tyč + držák) — $10                            │
│  ├── Referenční objekt (lahev 30 cm) — $0                       │
│  └── Napájení z 24V LiFePO₄ přes DC-DC — $0                    │
│                                                                  │
│  SOFTWARE:                                                       │
│  ├── Raspberry Pi OS Bookworm 64-bit                            │
│  ├── Python 3.11 + ultralytics + opencv-python                  │
│  ├── YOLO11n-seg (nano, instance segmentation)                  │
│  └── Cron job: 1× denně ve 12:00                                │
│                                                                  │
│  PIPELINE:                                                       │
│  ├── 1. Pořídit snímek (12:00, fixní úhel)                     │
│  ├── 2. YOLO11n-seg inference (~50 ms na CPU)                   │
│  ├── 3. Detekce 9 rostlin + referenční objekt                   │
│  ├── 4. Výpočet výšky (pixel → cm přes referenci)              │
│  ├── 5. Výpočet plochy koruny (pixel² → cm²)                   │
│  ├── 6. Detekce barvy (zdraví / stres)                          │
│  ├── 7. Log do Firebase (přes GCP pipeline)                     │
│  └── 8. Telegram denní report                                   │
│                                                                  │
│  SPOTŘEBA: ~5W (RPi 5 idle) + ~2W (kamera) = ~7W               │
│  Z 24V/15kWh baterie = 0.003% denně = zanedbatelné              │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Umístění kamery — dvě varianty

#### Varianta A: Side-view (boční pohled) — pro výšku

```
          KAMERA (boční pohled)
              ↓
    ┌─────────────────────┐
    │                     │
    │  AP6    GG3    GG4  │  ← Záhon 1 (188×95 cm)
    │                     │
    └─────────────────────┘
              ↑
         REFERENCE (lahev 30 cm)
```

**Výhody:** Přesné měření výšky (cm)
**Nevýhody:** Vidí jen 1 záhon, ostatní za rostlinami

#### Varianta B: Top-down (shora) — pro plochu koruny

```
    KAMERA (shora)
        ↓
    ┌─────────────────────┐
    │  AP6    GG3    GG4  │  ← Záhon 1
    │                     │
    └─────────────────────┘
    ┌─────────────────────┐
    │  AP3    AP4    GG2  │  ← Záhon 2
    │                     │
    └─────────────────────┘
```

**Výhody:** Vidí všechny rostliny, plocha koruny = přesná proxy pro biomasu
**Nevýhody:** Výška jen nepřímo (přes plochu)

#### Varianta C: Hybrid (doporučeno) — 2 kamery

```
Kamera 1 (side-view): Jeden záhon + reference → výška
Kamera 2 (top-down): Obě záhony → plocha koruny
```

**Cena:** 2× RPi Camera = +$50
**Alternativa:** Jedna kamera + otočný mount (servo, +$10)

### 4.4 Dataset — jak získat trénovací data

#### Fáze 1: Ruční anotace (1–2 hodiny)

```
1. Pořídit 50–100 snímků (1× denně × 50–100 dní, nebo
   nasnímat vícekrát denně v prvních dnech)
2. Nahrát do Roboflow (zdarma, 1000 obrázků/měsíc)
3. Označit bounding boxy:
   - Třída: AP1, AP3, AP4, AP5, AP6, GG2, GG3, GG4, GG5
   - Referenční objekt: "reference_30cm"
4. Rozdělit: train/val/test = 70/20/10
```

#### Fáze 2: SAM 2 auto-annotace (urychlení)

```
1. Ručně anotovat 5 snímků (1 rostlina = 1 snímek)
2. SAM 2 auto-annotace zbytku:
   from ultralytics.data.annotator import auto_annotate
   auto_annotate(data="images/", det_model="yolo11x.pt", sam_model="sam2_b.pt")
3. Zkontrolovat a opravit (~10% chybovost)
```

#### Fáze 3: Augmentace (rozšíření datasetu)

```
Automatizované transformace pro robustnost:
- Rotace: ±15° (vítr naklání rostliny)
- Jas: 80–120% (měnící se slunce)
- Kontrast: 90–110%
- Gaussian blur: σ=0.5 (mlha, rosa)
- Horizontal flip: ne (rostliny mají fixní pozici!)
```

### 4.5 Trénink modelu

```python
from ultralytics import YOLO

# Načíst předtrénovaný nano model
model = YOLO("yolo11n-seg.pt")

# Trénink na vlastním datasetu
model.train(
    data="garden_dataset.yaml",
    epochs=50,
    batch=4,           # malý batch = malá GPU (Colab T4)
    imgsz=640,
    lr0=1e-3,
    cos_lr=True,
    patience=10,       # early stopping
    device=0,          # GPU (0 = první GPU)
)

# Výsledek: runs/detect/train/weights/best.pt (~5 MB)
```

### 4.6 Inference pipeline (denní běh)

```python
from ultralytics import YOLO
import cv2
import json
from datetime import datetime

# Načíst natrénovaný model
model = YOLO("best.pt")

# Načíst snímek
img = cv2.imread("garden_snapshot.jpg")

# Inference
results = model(img)

# Zpracování výsledků
reference_height_cm = 30.0  # lahev
measurements = []

for r in results[0].boxes:
    cls_name = results[0].names[int(r.cls)]
    bbox = r.xywh[0].tolist()  # [x_center, y_center, width, height]
    
    if cls_name == "reference":
        reference_pixel_height = bbox[3]
        conversion_factor = reference_height_cm / reference_pixel_height
    else:
        measurements.append({
            "plant_id": cls_name,
            "height_cm": bbox[3] * conversion_factor,
            "canopy_area_cm2": bbox[2] * bbox[3] * (conversion_factor ** 2),
            "confidence": float(r.conf)
        })

# Uložit do Firebase
payload = {
    "timestamp": datetime.now().isoformat(),
    "measurements": measurements,
    "conversion_factor": conversion_factor
}
# POST na iot-ingest-beta...
```

### 4.7 Telegram report (denní)

```
🌿 Garden CV Report – 5.8.2026

Rostliny (9/9 detekováno):
  AP3: 101 cm (+4 cm) | plocha: 4200 cm² | ✅ zdravá
  AP4:  92 cm (+4 cm) | plocha: 3800 cm² | ✅ zdravá
  AP5:  76 cm (+4 cm) | plocha: 3100 cm² | ✅ zdravá
  AP6:  95 cm (+4 cm) | plocha: 4000 cm² | ✅ zdravá
  GG2:  97 cm (+4 cm) | plocha: 4100 cm² | ✅ zdravá
  GG3:  88 cm (+4 cm) | plocha: 3600 cm² | ✅ zdravá
  GG4: 107 cm (+4 cm) | plocha: 4500 cm² | ✅ zdravá
  GG5:  76 cm (+4 cm) | plocha: 3200 cm² | ✅ zdravá
  AP1:  74 cm (+4 cm) | plocha: 3000 cm² | ⚠️ nižší (květináč)

Průměr: 88 cm | Ø přírůstek: +4 cm/den
⚠️ AP1 (květináč) zaostává — zkontrolovat zálivku
```

### 4.8 Náklady a časová náročnost

| Položka | Cena | Čas |
|---------|:----:|:---:|
| Raspberry Pi 5 (8 GB) | $35 | – |
| Pi Camera 3 Wide nebo USB kamera | $50 | – |
| Pevný mount (tyč + držák) | $10 | – |
| MicroSD 64 GB | $10 | – |
| **Celkem HW** | **$105** | – |
| Dataset (50–100 snímků) | $0 | 2 h |
| Anotace (Roboflow) | $0 (free tier) | 2–3 h |
| Trénink (Google Colab T4) | $0 (free tier) | 1 h |
| Integrace s pipeline | $0 | 2 h |
| **Celkem SW** | **$0** | **5–6 h** |
| **CELKEM** | **$105** | **5–6 h** |

### 4.9 Srovnání s ručním měřením

| Metrika | Ručně (nyní) | CV (YOLO11) | Rozdíl |
|---------|:------------:|:-----------:|:------:|
| Frekvence | 1× týdně | 1× denně | 7× častěji |
| Přesnost výšky | ±1 cm | ±2–3 cm | Méně přesné |
| Plocha koruny | – | ±5% | Nová metrika |
| Barva / zdraví | Vizuálně | Kvantifikované | Lepší |
| Čas na měření | 15–20 min | 0 min (automat) | Ušetřeno |
| Data historie | Tabulka v Excelu | Firebase + Grafana | Lepší vizualizace |
| Náklady | $0 | $105 jednorázově | Investice |

### 4.10 Rizika a mitigace

| Riziko | Pravděpodobnost | Dopad | Mitigace |
|--------|:--------------:|:-----:|----------|
| Špatné osvětlení (ráno/večer) | Vysoká | Střední | Snímat ve 12:00 (plné slunce) |
| Déšť/mlha | Střední | Nízký | Přeskočit snímek, logovat "no data" |
| Rostliny se překrývají | Střední | Střední | YOLO11-seg řeší překryvy |
| AP1 květináč mimo záběr | Nízká | Nízký | Oddělená kamera nebo širší úhel |
| Model se "naučí" špatně | Nízká | Vysoký | Validace na test setu, průběžný monitoring |
| Hardware selže (RPi, kamera) | Nízká | Střední | Záložní SD karta, watchdog timer |

---

## ČÁST 5: IMPLEMENTAČNÍ ROADMAPA

### Fáze 0: Příprava (den 1, 2 h)
- [ ] Pořídit RPi 5 + kamera + MicroSD
- [ ] Nainstalovat Raspberry Pi OS
- [ ] Nainstalovat `ultralytics` + `opencv-python`
- [ ] Otestovat kameru (nasnímat 10 testovacích snímků)

### Fáze 1: Dataset (den 2–3, 3 h)
- [ ] Nasnímat 50–100 snímků (fixní úhel, 12:00)
- [ ] Nahrát na Roboflow
- [ ] Anotovat: 9 rostlin + 1 reference
- [ ] Rozdělit train/val/test

### Fáze 2: Trénink (den 4, 1 h)
- [ ] Spustit trénink na Google Colab (T4 GPU, zdarma)
- [ ] Validace: mAP50 > 80%?
- [ ] Export modelu: `best.pt` → ONNX pro RPi

### Fáze 3: Deploy (den 5, 2 h)
- [ ] Nahrát model na RPi
- [ ] Spustit inference pipeline
- [ ] Napojit na GCP pipeline (iot-ingest-beta)
- [ ] Nastavit Telegram report

### Fáze 4: Kalibrace (týden 2, 1 h denně)
- [ ] Porovnat CV výsledky s ručním měřením
- [ ] Odladit conversion_factor
- [ ] Případně retrénovat model s dalšími daty

---

## ČÁST 6: KLÍČOVÉ ZDROJE

| Zdroj | URL | Typ |
|-------|-----|-----|
| Roboflow Plant Height Tutorial | [blog.roboflow.com/monitor-plant-growth](https://blog.roboflow.com/monitor-plant-growth/) | Tutorial + kód |
| Plant Height GitHub | [github.com/tim3in/plant_height_measurement](https://github.com/tim3in/plant_height_measurement) | Zdrojový kód |
| Cannabis Growth Dataset | [data.mendeley.com/datasets/z2fp5kbgbh](https://data.mendeley.com/datasets/z2fp5kbgbh/1) | Dataset (COCO) |
| Microgreens + YOLO11 | [futureaiplanet.com](https://www.futureaiplanet.com/2025/12/automated-microgreens-height-yolo11.html) | Tutorial |
| YOLO11 na RPi | [learnopencv.com/yolo11-on-raspberry-pi](https://learnopencv.com/yolo11-on-raspberry-pi/) | Tutorial |
| RPi + YOLO11 Starter | [github.com/Blackluffy2k4/rpi-yolo11-packaged](https://github.com/Blackluffy2k4/rpi-yolo11-packaged) | Balíček |
| Ultralytics Docs | [docs.ultralytics.com](https://docs.ultralytics.com) | Dokumentace |
| Roboflow Universe | [universe.roboflow.com](https://universe.roboflow.com) | Databáze datasetů |

---

*Verze dokumentu: 1.0 | Poslední aktualizace: 2026-08-05*
