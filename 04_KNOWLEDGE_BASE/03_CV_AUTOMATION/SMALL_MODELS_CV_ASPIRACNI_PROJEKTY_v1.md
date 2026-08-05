# Small Models pro Computer Vision — Aspirační projekty a rešerše

**Datum:** 2026-08-05 | **Autor:** outpost2026 | **Verze:** 1.0
**Účel:** Komplexní přehled veřejně dostupných nástrojů, modelů a projektů pro computer vision s důrazem na small/edge modely. Slouží jako vstup pro plánování aspiračních projektů v oblasti CV a automatizace.

---

## 1. ZÁKLADNÍ EKOSSISTÉM — Klíčové technologie

### 1.1 Ultralytics YOLO rodina (YOLO11/YOLO26)

| Model | Parametry | Velikost | Latence (TensorRT) | Použití |
|-------|-----------|----------|---------------------|---------|
| **YOLO11n** (nano) | 2.6M | 5.4 MB | ~1.5ms (GPU) | Edge, mobilní, průmysl |
| **YOLO11s** (small) | 9.4M | 11.5 MB | ~2.5ms (GPU) | Vyvážený výkon |
| **YOLO11m** (medium) | 20.1M | 25.8 MB | ~5ms (GPU) | Univerzální |
| **YOLO11l** (large) | 25.3M | 43.7 MB | ~8ms (GPU) | Vyšší přesnost |
| **YOLO11x** (xlarge) | 56.9M | 109.1 MB | ~15ms (GPU) | Max přesnost |

**Klíčové vlastnosti:**
- Multi-task: detekce, segmentace, klasifikace, pose estimation, OBB (oriented bounding boxes)
- C3k2 bloky + C2PSA attention mechanism
- Export: ONNX, TensorRT, RKNN, NCNN, OpenVINO, CoreML
- **Pre-trained na COCO** — lze fine-tune na 10-50 anotovaných snímků

**Zdroje:**
- [Ultralytics GitHub](https://github.com/ultralytics/ultralytics) — 131.6k stars
- [Ultralytics Platform](https://platform.ultralytics.com) — anotace, trénink, deploy
- [YOLO11 Documentation](https://docs.ultralytics.com/models/yolo11/)

### 1.2 Segment Anything Model (SAM / SAM 2 / SAM 3)

| Model | Velikost | FPS (CPU) | Popis |
|-------|----------|-----------|-------|
| **SAM 2 Tiny** | 38.9M | ~44 fps | Nejrychlejší, jednoduché objekty |
| **SAM 2 Small** | 46M | ~30 fps | Rychlý, běžné objekty |
| **SAM 2 Base** | 80.8M | ~15 fps | Vyšší přesnost |
| **SAM 2 Large** | 224.4M | ~5 fps | Max přesnost, složité shape |
| **SAM 3** | (nový) | — | Text + exemplar prompts |

**Klíčové vlastnosti:**
- **Zero-shot segmentace** — bez tréninku na nových objektech
- **Auto-annotace** — generování datasetů pomocí bounding box prompts
- **Video tracking** — propagace segmentace přes snímky
- **Promptable** — point, box, mask prompts

**Integrace s Ultralytics:**
```python
from ultralytics.data.annotator import auto_annotate
auto_annotate(data="path/to/images", det_model="yolo11x.pt", sam_model="sam2_b.pt")
```

**Zdroje:**
- [Meta SAM 2 GitHub](https://github.com/facebookresearch/sam2)
- [Ultralytics SAM Docs](https://docs.ultralytics.com/models/sam-2/)
- [Roboflow SAM 2 Integration](https://blog.roboflow.com/sam-2-roboflow)

### 1.3 Ultralytics Solutions (hotové aplikace)

| Solution | Popis | API |
|----------|-------|-----|
| **ObjectCounter** | Počítání objektů v regionu/linii | `solutions.ObjectCounter()` |
| **Heatmap** | Heatmapa pohybu/přítomnosti | `solutions.Heatmap()` |
| **SpeedEstimation** | Odhad rychlosti objektů | `solutions.SpeedEstimation()` |
| **QueueManager** | Správa front/zón | `solutions.QueueManager()` |
| **SecurityAlarm** | Detekce + email alert | `solutions.SecurityAlarm()` |
| **AIGym** | Monitoring cvičení (pose) | `solutions.AIGym()` |
| **VisionEye** | Mapování "vidění" kamery | `solutions.VisionEye()` |

**Příklad — ObjectCounter:**
```python
from ultralytics import solutions

counter = solutions.ObjectCounter(
    show=True,
    region=[(1603, 1012), (474, 1012), (0, 265), (6, 8), (465, 0)],
    model="./runs/detect/train6/weights/best.pt",
    tracker="botsort.yaml",
    tracker_conf=0.3,
)
results = counter(frame)
print(f"In: {results.in_count}, Out: {results.out_count}")
```

---

## 2. EDGE DEPLOYMENT — Hardware srovnání

### 2.1 NVIDIA Jetson (GPU-accelerated)

| Zařízení | TOPS | GPU | RAM | Cena | FPS (YOLO11n) |
|----------|------|-----|-----|------|---------------|
| **Jetson Orin Nano Super** | 67 | 1024 CUDA cores | 8GB LPDDR5 | ~$249 | 60-80 fps |
| **Jetson Orin NX 16GB** | 100 | 1024 CUDA cores | 16GB | ~$699 | 80-120 fps |
| **Jetson AGX Orin** | 275 | 2048 CUDA cores | 64GB | ~$1999 | 150+ fps |

**Klíčové:** TensorRT optimalizace, INT8/FP16 quantizace, Docker kontejnery s CUDA 12.6

**Zdroje:**
- [Jetson YOLO11 Guide](https://docs.ultralytics.com/guides/nvidia-jetson/)
- [YOLO11 Jetson Benchmark](https://github.com/smbunn/yolo11_jetson_orin_nano)

### 2.2 Rockchip RKNN (NPU, low-power)

| SoC | NPU TOPS | Cena | Použití |
|-----|----------|------|---------|
| **RK3588** | 6 TOPS | $50-100 | Výkonné edge zařízení |
| **RK3576** | 3 TOPS | $30-60 | Střední třída |
| **RK3566** | 0.8 TOPS | $15-30 | Low-cost, IoT |

**Export z YOLO11:**
```python
from ultralytics import YOLO
model = YOLO("yolo11n.pt")
model.export(format="rknn", imgsz=640)
```

**Benchmark:** YOLO11n na RK3588 → ~99.5ms/image (INT8)

**Zdroje:**
- [Rockchip RKNN Deploy](https://docs.ultralytics.com/integrations/rockchip-rknn/)
- [YOLO11 Rockchip Guide](https://www.ultralytics.com/blog/deploy-ultralytics-yolo11-on-rockship-for-efficient-edge-ai)

### 2.3 Raspberry Pi (CPU/NCNN)

| Optimální technika | Výsledek |
|-------------------|----------|
| NCNN model conversion | +62% rychlost |
| Hardware-aware quantization | ms latence |
| 240×240 rozlišení | 25+ FPS |

**Použití:** Nejlevnější entry point (~$35), ale omezený výkon

### 2.4 Srovnání platforem

| Platforma | Cena | FPS (YOLO11n) | Spotřeba | Ideální pro |
|-----------|------|---------------|----------|-------------|
| Jetson Orin Nano Super | $249 | 60-80 | 7-15W | Průmysl, robotika |
| Rockchip RK3588 | $50-100 | 10-15 | 3-5W | IoT, kamery |
| Raspberry Pi 5 | $35 | 5-10 | 5-10W | Prototypy, edukace |
| Intel N100 + OpenVINO | $100 | 20-30 | 10-25W | PC-based |

---

## 3. REAL-WORLD PROJEKTY — Veřejně dostupné

### 3.1 Conveyor Belt Counting (počítání na pásu)

**Projekt:** [potato_counting (NguyenHoangMinh1312)](https://github.com/NguyenHoangMinh1312/potato_counting)
- YOLO11 nano + ObjectCounter
- Polygon zone tracking
- BoT-SORT tracker
- 39 řádků kódu = kompletní řešení

**Projekt:** [Orange-Counter-Conveyor-Belt](https://github.com/IIIllllIlIlllII/Orange-Counter-Conveyor-Belt)
- Fine-tuned YOLO11 + ObjectCounter
- Real-time live count overlay

**Projekt:** [visionusecases (RizwanMunawar)](https://github.com/RizwanMunawar/visionusecases)
- Apple counting, bread counting, items counting
- SAM 2 auto-annotation
- 12 stars, 196 commits

**Academic:** [Real-Time Object Counting on Industrial Conveyor Belts (Springer 2026)](https://link.springer.com/chapter/10.1007/978-3-032-21625-0_24)
- YOLOv11 + zone-based algorithm
- 94.2% accuracy at 28.5 FPS
- 3-zónový přístup (robustní proti flickeringu)

### 3.2 Defect Detection (detekce defektů)

**Projekt:** [YOLO11 E-Waste Detection (Wiley 2025)](https://onlinelibrary.wiley.com/doi/full/10.1002/eng2.70459)
- 99% accuracy na e-waste kategorizaci
- YOLO11 nano na edge hardware

**Projekt:** [NEU Surface Defect Benchmark (arXiv 2026)](https://arxiv.org/abs/2606.07659)
- YOLOv8s pro automotive manufacturing
- NEU dataset + MVTec AD
- Edge deployment benchmark

**Projekt:** [Edge-Deployed DL for QC (ScienceDirect 2025)](https://www.sciencedirect.com/science/article/pii/S2212827125005724)
- YOLOv8-based assembly line QC
- Robotic process control integration

**Projekt:** [AI IoT Edge Vision (Springer 2026)](https://link.springer.com/chapter/10.1007/978-3-032-18042-1_25)
- Open-source system for AIoT hardware
- Low-power edge detection

### 3.3 SAM 2 Auto-Annotation (anotace dat)

**Workflow:**
1. Pořiď 10-50 snímků
2. Ručně anotuj 1-3 snímky (bounding box)
3. SAM 2 auto-annotace zbytku
4. YOLO11 nano trénink
5. Deploy na edge

**Projekt:** [YOLO-SAM2 Polyp Segmentation (arXiv 2024)](https://arxiv.org/html/2409.09484v1)
- Hybrid YOLO + SAM 2
- Self-prompting (bez manuálních promptů)
- +20.7% mIoU oproti SOTA

**Projekt:** [Roboflow SAM 2 Integration](https://blog.roboflow.com/sam-2-roboflow)
- Smart Polygon label assistant
- Workflows block s RF-DETR
- Hosted API

### 3.4 Pose Estimation (odhad polohy)

**Ultralytics řešení:**
- AIGym workout monitoring
- Physiotherapy tracking
- Worker safety monitoring
- Animal behavior research

**Modely:** YOLO11n-pose (2.6M params), YOLO11s-pose, YOLO11m-pose

### 3.5 Visual Inspection (vizuální inspekce)

**Projekt:** [Roboflow Conveyor Counting Tutorial](https://blog.roboflow.com/counting-objects-conveyor-belt)
- End-to-end: data → anotace → trénink → deploy
- ByteTrack + Line Counter workflow
- Grounding DINO pro auto-labeling

**Projekt:** [Ultralytics Defect Detection](https://www.ultralytics.com/use-cases/defect-detection)
- Hairline cracks, label misalignment
- Pass/fail classification
- 98-99.9% accuracy

---

## 4. ASPIRAČNÍ PROJEKTY — Mapování na domény SYSTEQ

### 4.1 CNC Defect Detection (PET Felt)

**Návaznost:** DEFECT_CATALOG_V1.md (497 řádků), ONTOLOGIE_PET_FELT_RAG

**Architektura:**
```
Kamera na výrobní lince (GigE Vision)
    ↓
NVIDIA Jetson Orin Nano Super ($249)
    ↓
YOLO11n-seg (nano, instance segmentation)
    ↓
Detekce tříd:
  - Třída A: EDGE_MERGE_MISSING, UNCLOSED_LOOP, MICRO_SEGMENT
  - Třída B: CHATTER, BURRS, BUE
  - Třída C: NC kód chyby
    ↓
ObjectCounter → počítání defektů/ks
    ↓
Alarm + logging do MES/SCADA
```

**Dataset:** SAM 2 auto-annotace z 1 snímku → finetune YOLO11n-seg
**Latence:** <10ms/frame (67 TOPS na Jetsonu)
**EROI:** VELMI VYSOKÝ — 15-35% úspora času na přípravě zakázek

### 4.2 Waterjet Kerf Quality Monitor

**Návaznost:** waterjet_intelligence_layer_poc.md

**Architektura:**
```
Kamera nad waterjet stolem (USB3/GigE)
    ↓
Rockchip RK3588 ($50) nebo Jetson Nano ($149)
    ↓
YOLO11n (detekce) + regresní head (kerf width)
    ↓
Vizuální data:
  - Kerf width (mm)
  - Edge roughness (trida 1-5)
  - Abrasive trace patterns
    ↓
Korelace s ML modelem (decision tree z High-SNR_knowhow)
    ↓
Feedback pro operátora + predikce výměny trysky
```

**Dataset:** 50-100 snímků řezů + manuální měření kerfu
**Latence:** <100ms (RKNN na RK3588)
**EROI:** VYSOKÝ — predikce kvality = snížení waste

### 4.3 VCF-to-Visual Validator

**Návaznost:** Vcf-compiler, vcf_color_service

**Architektura:**
```
VCF soubor → render do PNG (deterministický)
    ↓
Porovnání s reálným výřezem (kamera)
    ↓
YOLO11n-seg: overlay anomálií
    ↓
Color matching proti HUGO vzorníku (16 barev)
    ↓
Dimensional accuracy check (mm tolerances)
    ↓
Pass/Fail + report
```

**Dataset:** Párové snímky (VCF render + reálný výřez)
**Latence:** <50ms
**EROI:** STŘEDNÍ — okamžitá zpětná vazba pro operátora

### 4.4 Material Color Sorter (Moodpasta)

**Návaznost:** ONTOLOGIE_PET_FELT_RAG, vcf_color_service

**Architektura:**
```
Kamera na skládce/lince
    ↓
YOLO11n-cls ( image classification, 16 tříd)
    ↓
Třídy: fDAR, fCAR, fMAT, fREN, fSAV, fDUN, fFJORD, fSALMON, ...
    ↓
Batch consistency check (šarže)
    ↓
Automatická archivace + logging
```

**Dataset:** 10 snímků na barvu × 16 barev = 160 snímků
**Latence:** <5ms (YOLO11n-cls je extrémně rychlý)
**EROI:** STŘEDNÍ — ověření barvy před řezem

### 4.5 Tool Wear Detector (CNC)

**Návaznost:** High-SNR_knowhow_ML_methodology.json

**Architektura:**
```
Kamera na hlavici stroje (blízký záběr)
    ↓
SAM 2 segmentace opotřebení hrany
    ↓
YOLO11s: klasifikace stavu (1-5)
    ↓
Korelace s ML training data (decision tree)
    ↓
Predikce výměny nástroje
    ↓
Alert operátorovi
```

**Dataset:** 20-30 snímků nástrojů v různých stavech
**Latence:** <200ms
**EROI:** VYSOKÝ — předejítí poškození obrobku

---

## 5. IMPLEMENTAČNÍ WORKFLOW — Krok za krokem

### Fáze 1: Příprava dat (1-2 dny)

```
1. Pořídit 20-50 snímků z reálného prostředí
2. 1-3 snímky anotovat ručně (bounding box nebo polygon)
3. SAM 2 auto-annotace zbytku:
   from ultralytics.data.annotator import auto_annotate
   auto_annotate(data="images/", det_model="yolo11x.pt", sam_model="sam2_b.pt")
4. Rozdělit: train/val/test = 70/20/10
```

### Fáze 2: Trénink (30-60 minut)

```python
from ultralytics import YOLO

model = YOLO("yolo11n.pt")  # nano — nejmenší
model.train(
    data="dataset.yaml",
    epochs=50,
    batch=4,
    imgsz=640,
    lr0=1e-3,
    cos_lr=True,
    patience=10,
)
```

### Fáze 3: Validace (5 minut)

```python
metrics = model.val()
print(f"mAP50: {metrics.box.map50}")
print(f"mAP50-95: {metrics.box.map}")
```

### Fáze 4: Export na edge (5-15 minut)

```python
# NVIDIA Jetson (TensorRT)
model.export(format="engine", half=True)

# Rockchip RKNN
model.export(format="rknn", imgsz=640)

# Raspberry Pi (NCNN)
model.export(format="ncnn")
```

### Fáze 5: Deploy (1 hodina)

```python
from ultralytics import YOLO

model = YOLO("best.engine")  # nebo .rknn, .ncnn
results = model.predict(source="rtsp://camera_ip/stream", show=True)
```

---

## 6. KLÍČOVÉ ZDROJE A ODKAZY

### Dokumentace
| Zdroj | URL |
|-------|-----|
| Ultralytics Docs | https://docs.ultralytics.com |
| YOLO11 Models | https://docs.ultralytics.com/models/yolo11/ |
| SAM 2 Docs | https://docs.ultralytics.com/models/sam-2/ |
| Object Counting Guide | https://docs.ultralytics.com/guides/object-counting/ |
| Jetson Deploy | https://docs.ultralytics.com/guides/nvidia-jetson/ |
| Rockchip RKNN | https://docs.ultralytics.com/integrations/rockchip-rknn/ |

### GitHub projekty
| Projekt | URL | Popis |
|---------|-----|-------|
| Ultralytics | https://github.com/ultralytics/ultralytics | Core framework |
| SAM 2 | https://github.com/facebookresearch/sam2 | Segment Anything |
| visionusecases | https://github.com/RizwanMunawar/visionusecases | CV projekty |
| potato_counting | https://github.com/NguyenHoangMinh1312/potato_counting | Conveyor counting |
| YOLO11 Jetson | https://github.com/smbunn/yolo11_jetson_orin_nano | Edge benchmark |

### Tutorials & Blogy
| Zdroj | URL |
|-------|-----|
| Roboflow Blog | https://blog.roboflow.com |
| LearnOpenCV | https://learnopencv.com/yolo11 |
| Ultralytics Blog | https://www.ultralytics.com/blog |

### Akademické práce
| Práce | Rok | Key Insight |
|-------|-----|-------------|
| Real-Time Conveyor Counting (Springer) | 2026 | 94.2% accuracy, zone-based |
| YOLO11 E-Waste (Wiley) | 2025 | 99% classification |
| NEU Defect Benchmark (arXiv) | 2026 | Edge automotive QC |
| YOLO-SAM2 Polyp (arXiv) | 2024 | +20.7% mIoU |

---

## 7. CENOVÝ RÁMEC PROTOTYPU

| Komponenta | Cena | Poznámka |
|-----------|------|----------|
| NVIDIA Jetson Orin Nano Super | $249 | Dev kit s kamerou |
| USB3 kamera (IMX477) | $50-100 | 12MP, global shutter |
| Rockchip RK3588 SBC | $50-100 | Orange Pi 5 Ultra |
| Raspberry Pi 5 + HQ kamera | $100 | Entry level |
| GigE průmyslová kamera | $200-500 | Basler, FLIR |
| **Celkem (min. prototyp)** | **$300-400** | Jetson + kamera |
| **Celkem (průmyslový)** | **$500-1000** | Jetson + prům. kamera |

---

## 8. DOPORUČENÍ PRO SYSTEQ

### Nejrychlejší start
1. **CNC Defect Detection** — máš hotový katalog defektů
2. Stačí: 1 anotovaný snímek → SAM 2 → YOLO11n-seg → Jetson
3. Čas: 2-3 dny prototyp

### Nejvyšší business value
1. **Waterjet Kerf Quality** — přímo navazuje na WIL
2. Vizuální data = tréninková data z reálného provozu
3. ROI: 15-35% úspora času na přípravě zakázek

### Nejlevnější entry point
1. **Material Color Sorter** — 160 snímků = kompletní dataset
2. YOLO11n-cls na Raspberry Pi 5 ($100)
3. Čas: 1 den prototyp

---

*Verze dokumentu: 1.0 | Poslední aktualizace: 2026-08-05*
