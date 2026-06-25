# SYSTEQ VCF Stack — Kompletní softwarová disekce & refaktoringový plán

**Verze nástroje:** v20.0.0 | **Datum:** 2026-06-25 | **Autor:** outpost2026
**Účel:** Architektonická analýza celého vyvinutého stacku, vymezení vůči technickému zadání Moodpasta, identifikace bugs/issues, návrh konkrétních mitigačních kroků

---

## ČÁST 0: Východiska

### 0.1 Kontext analýzy

Tento dokument vznikl jako výsledek kompletního read-through zdrojového kódu repozitáře `vcf_parser_b2b/src/` (6 Python souborů, 2 JSON konfigurace, 1 adresář Knowledge_base). Analyzováno:
- `vcf_binary_reader.py` (155 ř.) — binární extrakce VCF
- `vcf_geometry.py` (1197 ř.) — parsování geometrie + detekce defektů
- `vcf_time_predictor.py` (71 ř.) — kinematický model predikce času
- `vcf_parser_v20.py` (810 ř.) — engine orchestrace (RuidaVcfEngineV20)
- `vcf_config.py` (149 ř.) — načítání konfigurace
- `Knowledge_base/engine.py` (564 ř.) — sémantický audit
- `Knowledge_base/models.py` (103 ř.) — datové modely
- `Knowledge_base/rules.json` (101 ř.) — pravidla s epistemickou metadatovou vrstvou
- `app_config.json` (77 ř.) — obchodní konfigurace
- `machine_profile.json` (74 ř.) — kinematický profil stroje

### 0.2 Stav toolchainu

| Metrika | Hodnota |
|---|---|
| Verze | v20.0.0 |
| GitHub první commit | 03/2026 |
| Počet iterací | 22+ (v0 → v23) |
| Počet testů | 10 files, 2 determinism testy OK |
| Počet trénovacích VCF | 23 (z toho 13 timestampovaných) |
| Golden Master baseline | 7 |
| Demo souborů | 23 VCF |
| Repo velikost | ~5 000 ř. Python |

---

## ČÁST 1: Architektura nástroje

### 1.1 Vrstvená architektura (6 Layers)

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 5: UI / Streamlit                                    │
│  app.py (~1600 ř.) ─ 2 role, 2D viz, KB override panel     │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: Knowledge Base Engine (sémantický audit)          │
│  Knowledge_base/{engine.py, models.py, rules.json}          │
│  6 detekčních pravidel (SEQUENCE, H2, FIXATION, GEO, ...)   │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: Engine Facade (orchestrace)                       │
│  RuidaVcfEngineV20.parse_bytes() — 680ř. monolit            │
│  Volá L0→L1→L2→L4, sestavuje parsed_data dict (750+ polí)  │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Time Predictor (kinematický model)                │
│  predict_cut_time() — setup + cut + corners + traverse      │
│  Konstanty z machine_profile.json                           │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Geometry Engine (parsování + detekce)             │
│  parse_geometry_v18_2() — elementy, bbox, centroid          │
│  DETEKČNÍ FUNKCE (6x) — v témže souboru !!!                │
├─────────────────────────────────────────────────────────────┤
│  Layer 0: Binary Reader (RE jádro)                          │
│  extract_active_layers_details() — VCF binární formát       │
│  extract_strings() — metadata z blobu                       │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Data flow (aktuální stav)

```
VCF soubor (binární)
    │
    ▼
Layer 0: binary_reader → layers_details (list), strings (list)
    │
    ▼
Layer 1: geometry → elements (list s tvary, bbox, centroidy)
                      → shape_groups, symmetry, density_grid, layout
                      → DETEKCE (open paths, micro segs, unclosed, orphans, decor)
    │
    ▼
Layer 2: time_predictor → predicted_seconds
    │
    ▼
Layer 3: engine orchestrace:
           → sub_jobs detekce (BFS clustering)
           → thickness inference (V-slot H2 → material thickness)
           → element nesting tree (parent/child)
           → operation sequence validation
           → ml_features (55+ featů)
           ↓
           Layer 4: KnowledgeBaseEngine.validate_all()
                    → H2, SEQUENCE, FIXATION, EDGE_MERGE, MICRO,
                      UNCLOSED, ORPHAN, UNCONNECTED_DECOR
                    → risk_score
           ↓
           parsed_data dict (750+ polí)
    │
    ▼
Layer 5: Streamlit → HUD, 2D viz, warnings, Layer Card, download
```

---

## ČÁST 2: Vymezení vůči technickému zadání

### 2.1 Co je předmětem vyjednávání (Fáze 1 — 43 000 Kč)

| Komponenta | V scope | Stav | Dodáno |
|---|---|---|---|
| `vcf_binary_reader.py` — layer extrakce | ✅ Modul A | Stabilní | ✅ Hotovo |
| `vcf_geometry.py` — `parse_geometry_v18_2` | ✅ Modul A | Stabilní | ✅ Hotovo |
| `vcf_time_predictor.py` — `predict_cut_time` | ✅ Modul A | ⚠️ 13 trénovacích dat | ✅ Hotovo |
| `vcf_parser_v20.py` — `RuidaVcfEngineV20` | ✅ Modul A | Monolit | ✅ Hotovo |
| `vcf_config.py` — načítání konfigurace | ✅ Modul A | OK | ✅ Hotovo |
| `machine_profile.json` | ✅ Modul A | ❌ Hypotéza | ✅ Exists |
| `from vcf_parser import parse` | ✅ Modul A | ❌ **Neexistuje** | ❌ Chybí |
| `app_config.json` | ✅ Modul A | ⚠️ Obsahuje GCP secret | ✅ Exists |
| File watcher + GSheets ETL | ✅ Modul B-A | ❌ **Neexistuje** | ❌ Chybí |
| DXF Web UI (Streamlit) | ✅ Modul C2 | ❌ **Neexistuje** | ❌ Chybí |

### 2.2 Co je mimo scope (autorův IP, upsell)

| Komponenta | Kde je | Upsell cena | Stav |
|---|---|---|---|
| QC Suite — 6 detekčních pravidel | `vcf_geometry.py` (detekce) + `Knowledge_base/` | 12 000 Kč | ✅ Hotovo |
| 2D Vizualizace — severity overlay, nesting BBOX | `app.py` (Matplotlib) | 8 000 Kč | ✅ Hotovo |
| Layer Card — nástroje per vrstva | `app.py` + `vcf_parser_v20.py` | 4 000 Kč | ✅ Hotovo |
| Risk Score — 0-15 sémantické riziko | `vcf_parser_v20.py` | 3 000 Kč | ✅ Hotovo |
| Golden Master test suite | `tests/` + `golden_master/` | 5 000 Kč | ✅ Hotovo |
| KB Override panel — live toggling | `app.py` sidebar | 4 000 Kč | ✅ Hotovo |
| ML Feature vektor (55+ featů) | `vcf_parser_v20.py` | — | ✅ Hotovo |
| CNC Knowledge Corpus + DEFECT CATALOG | `docs/` | 15 000 Kč | ✅ Hotovo |
| RE Case Study | `docs/` | — | ✅ Hotovo |
| Kalkulátor marží | `app_config.json` | — | ✅ Hotovo |
| Odoo CSV export | `vcf_parser_v20.py` | — | ✅ Hotovo |

**Souhrnný upsell potenciál bez dalšího vývoje: ~46 000 Kč**

### 2.3 Co je hotovo, ale není nikde nabízeno

| Položka | Problém |
|---|---|
| Streamlit VCF dashboard (celý, ~1600 ř.) | Není v zadání, ale je funkční. Může být součástí upsellu nebo "value-add" při fázi 1 |
| KB Override panel (CNC role) | Nástroj pro Karla — live toggling pravidel. Pokud klient neví, že existuje, neprohloubí závislost |
| ML Feature vektor (55 featů) | Základ pro C1. Pokud není explicitně řečeno, že existuje, klient nevidí hodnotu pro budoucí DXF inferenci |

---

## ČÁST 3: Bugs & Issues — kompletní katalog

### 3.1 Kritické (blokující smlouvu nebo způsobující spor)

#### B‑CRIT‑01: Chybí `from vcf_parser import parse` API

**Lokalizace:** Celý repozitář — neexistuje `vcf_parser/__init__.py`
**Popis:** Technické zadání Modulu A explicitně požaduje:
```python
from vcf_parser import parse
result = parse("/cesta/k/souboru/3780_deska_2.VCF")
```
Engine je aktuálně dostupný pouze jako třída `RuidaVcfEngineV20`, která vyžaduje `bytes` (ne cestu). Neexistuje funkce `parse()`.
**Riziko:** Při předávce klient obdrží engine, který neodpovídá specifikaci. Možný spor o nesplnění deliverable.
**Mitigace:** Vytvořit `vcf_parser/__init__.py` a `vcf_parser/engine.py` s wrapperem:

```python
def parse(filepath: str) -> dict:
    with open(filepath, "rb") as f:
        engine = RuidaVcfEngineV20(f.read(), filename=os.path.basename(filepath))
    return engine.parsed_data
```
**Odhad času:** 30 min.

---

#### B‑CRIT‑02: Time prediction kalibrován na 13 datech, `epistemic_confidence_index = 0.0`

**Lokalizace:** `vcf_time_predictor.py`, `machine_profile.json`
**Popis:** Všechny kinematické konstanty mají `validation_status = "empirical"` nebo `"hypothesis"`. `epistemic_confidence_index` je 0.0. Model nebyl nikdy validován proti reálnému stroji.
**Dopad:** Accuracy claim "95-99 %" je neobhajitelný bez kalibrace. Reálná chyba je neznámá — odhad ±20-30 %.
**Riziko:** Pokud klient spoléhá na predikci pro nacenění zakázek a parser systematicky chybuje, je to základ sporu.
**Mitigace:**
1. Před podpisem: Přidat do nabídky explicitní disclaimer o kalibraci
2. Při podpisu: Naplánovat 2-4 h měření na Moodpasta stroji
3. Vytvořit `scripts/calibrate.py` — interaktivní průvodce:
   - Měření max_speed (1000 mm, stopky)
   - Měření t_corner (10× L-cut)
   - Měření setup_overhead
   - Měření t_lift
4. Automatický update `machine_profile.json` + výpočet `epistemic_confidence_index`
5. Po kalibraci: Record 100+ VCF timestamp pairs pro finální model
**Odhad času:** 2-4 h měření + 3 h vývoj kalibrační utility.

---

#### B‑CRIT‑03: app_config.json obsahuje GCP credentials

**Lokalizace:** `src/app_config.json` — ř. 70-76
```json
"gcp": {
    "project_id": "project-4ac30110-41b1-4783-a5d",
    "project_number": "537446704644",
    "region": "europe-west1",
    "service_name": "vcf-parser-demo",
    "image": "europe-west1-docker.pkg.dev/.../vcf-parser:v1.7"
}
```
**Riziko:** Pokud je tento soubor součástí dodávaného balíčku (a aktuálně je v `src/`), klient získá přístup k produkční GCP infrastruktuře autora.
**Mitigace:**
1. GCP blok přesunout do `.env` nebo samostatného `deploy_config.json` (mimo git)
2. `app_config.json` v repu bude obsahovat pouze: panel_formats, analysis, auth
3. Přidat `.env` do `.gitignore`
**Odhad času:** 15 min.

---

### 3.2 Vysoká priorita (IP ochrana, architektura)

#### B‑HIGH‑01: Monolit vcf_geometry.py — míchá parsování s detekcí

**Lokalizace:** `vcf_geometry.py` (1197 ř.)
**Popis:** Jeden soubor obsahuje:
- Geometrický parser (`parse_geometry_v18_2`, `group_elements`, `detect_panel_format`, atd.) — **TOTO dodáváno v Modulu A**
- 6 detekčních funkcí (`detect_open_paths_in_parents`, `detect_micro_segments`, `detect_unclosed_loops`, `detect_orphan_elements`, `detect_unconnected_internal_decor`, `filter_micro_segment_clusters`, `filter_unclosed_decor_loops`) — **TOTO není v Modulu A**
- 5 pomocných geometrických funkcí (`_catmull_rom_centripetal`, `_linear_subdivide`, `_fit_circle_through_three_points`, atd.)
- 3 podpůrné utility (`_build_endpoint_kdtree`, `_compute_global_canvas_bbox`, `_find_nearest_endpoint`)
- 1 filtrační funkci (`_merge_consecutive_arcs`)
- Detekci endpoint (`_is_endpoint_on_bbox_edge`, `_min_distance_to_segments`)

**Riziko:** Pokud klient obdrží celý soubor (a aktuálně engine importuje `vcf_geometry` jako celek), získá detekční pravidla zdarma. Autor ztrácí upsell potenciál QC Suite 12 000 Kč.
**Mitigace:**
1. Vytvořit `vcf_parser/geometry_parser.py` — pouze parse funkce (ř. 16-371, cca 350 ř.)
2. Vytvořit `systeq_kb/geometry_detection.py` — detekční funkce (ř. 654-1197, cca 540 ř.)
3. Upravit importy v `vcf_parser_v20.py`:
   - `vcf_parser_v20.py` importuje z `vcf_parser/geometry_parser.py` (vždy)
   - `Knowledge_base/engine.py` importuje z `systeq_kb/geometry_detection.py` (volitelně)
**Odhad času:** 2 h.

---

#### B‑HIGH‑02: Monolitická orchestrace v parse_bytes()

**Lokalizace:** `vcf_parser_v20.py` — metoda `parse_bytes()` (ř. 72-752, ~680 ř.)
**Popis:**
- Jediná metoda obsahuje: fail-safe detection, thickness inference, sequence validation, sub_jobs clustering, element tree building, proximity matrix, ml_features assembly, KB invocation
- KB invocation je pevně provázaná (ř. 622-681) — nelze engine dodat bez KB
- Parsed_data dict je sestavován ručně (ř. 683-751) — 750+ polí, žádná validace schématu
- Chybové stavy jsou ošetřeny jedním velkým `try/except` (ř. 731-752) — vrací fail-safe dict, ale ztrácí diagnostiku
**Riziko:** Nelze licencovat engine bez KB. Nelze unit-testovat jednotlivé fáze. Každá změna riziková.
**Mitigace:**
1. Rozdělit `parse_bytes()` na sekvenci volání:
   ```python
   def parse_bytes(self):
       self._read_binary()
       self._parse_geometry()
       self._predict_time()
       self._build_metadata()
       if self._kb_available:
           self._run_kb_audit()
       self._assemble_output()
   ```
2. KB invocation podmínit:
   ```python
   if KB_AVAILABLE and not fail_safe_flag:
       try:
           from systeq_kb import KnowledgeBaseEngine
           ...
   ```
   Toto částečně existuje (ř. 34-39, 622), ale parsed_data dict již obsahuje KB výsledky v `manufacturing_intelligence`. Nutno:
   - KB výsledky do samostatného klíče `systeq_kb: {...}` nebo je engine vůbec negeneruje
   - Engine musí vracet konzistentní output bez ohledu na přítomnost KB
3. Nahradit ruční assembly dict builderem nebo Pydantic modelem
**Odhad času:** 3-4 h.

---

#### B‑HIGH‑03: Dvě nezávislé implementace nesting detekce

**Lokalizace:**
1. `vcf_parser_v20.py` (ř. 289-376) — `_bbox_contains()` + `element_sequence_violations`
2. `Knowledge_base/engine.py` (ř. 215-242) — `validate_sequence()` s `check_nesting_hierarchy`
**Popis:** Stejná logika (detekce outer-before-inner) implementovaná dvakrát, s odlišnými kritérii:
- V engine: používá `bbox_contains` + area sorting
- V KB: používá offset comparison
- Výsledky se mohou lišit
**Riziko:** Inkonzistentní warningy, matoucí pro klienta.
**Mitigace:**
1. Sjednotit na jednu implementaci v `systeq_kb/`
2. V engine ponechat pouze základní layer-level sequence check (ř. 234-268)
3. Element-level nesting (ř. 277-376) přesunout do KB
**Odhad času:** 1 h.

---

### 3.3 Střední priorita (strukturální)

#### B‑MED‑01: machine_profile.json obsahuje nekalibrované hypotézy

**Lokalizace:** `machine_profile.json`
**Konkrétní položky s `"validation_status": "hypothesis"`:**
- `material_damping.materials.pet_felt_24mm.speed_multiplier: 0.85`
- `material_damping.materials.plywood_6mm.speed_multiplier: 0.70`
- `material_damping.materials.acrylic_3mm.speed_multiplier: 0.60`
- `density_penalties.vibrate_curve_threshold_mm: 0.2` (empirický threshold bez měření)
- `density_penalties.vibrate_curve_point_penalty_seconds: 1.2`

**Riziko:** Pokud klient řeže jiný materiál než 12mm PET felt, predikce času je založena na neověřených hypotézách.
**Mitigace:**
1. Ponechat `"validation_status": "hypothesis"` — transparentní
2. Do kalibrační utility přidat i material damping measurement
3. Pro fázi 1 použít pouze PET felt profily — ostatní explicitně označit jako nepodporované
**Odhad času:** 30 min (dokumentace) + součást kalibrace.

---

#### B‑MED‑02: Fail-safe režim vrací zavádějící data

**Lokalizace:** `vcf_parser_v20.py` (ř. 733-751)
**Popis:** Při chybě parsování engine vrací fail-safe dict s placeholder hodnotami:
```python
"ml_features": {},
"elements_parsed": 0,
"erp_time_prediction": {"predicted_time_seconds": 0, ...}
```
Tento dict je strukturou identický s úspěšným výsledkem. Volající kód (app.py, API) nemá spolehlivý způsob, jak poznat, že parsing selhal — musí kontrolovat `fail_safe_flag`.
**Riziko:** Pokud API wrapper nezkontroluje `fail_safe_flag`, klient uvidí "predikce: 0 s" a může to interpretovat jako "žádný čas".
**Mitigace:**
1. V fail-safe dict explicitně uvést:
   ```python
   "_error": True,
   "_error_message": str(e)
   ```
2. Nebo raise výjimku v `parse()` wrapperu (lepší — fail fast)
3. Volající kód pak řeší výjimku → log + uživatelsky srozumitelná hláška
**Odhad času:** 30 min.

---

#### B‑MED‑03: app.py je monolit s embedovaným CSS/HTML

**Lokalizace:** `app.py` (~1600 ř.)
**Popis:** Streamlit app obsahuje:
- ~260 ř. CSS ve `st.markdown()` (ř. 23-258)
- ~20 ř. HTML header
- ~1200 ř. aplikační logiky (HUD, 2D viz, warnings, Layer Card, metadata, pricing)
- Veškerá logika v jednom skriptu, žádná modularizace
**Riziko:** C2 (DXF Web UI) bude vyžadovat Streamlit. Pokud se začne stavět na stejném monolitickém základu, naroste nepřehlednost.
**Mitigace:**
1. Extrahovat CSS do samostatného `styles.py`
2. Extrahovat 2D vizualizaci do `viz/visualization.py`
3. Vytvořit `dashboard_vcf.py` (VCF) a `dashboard_dxf.py` (C2) jako samostatné entry pointy
**Odhad času:** 2-3 h.

---

### 3.4 Nízká priorita (kosmetické, dokumentace)

#### B‑LOW‑01: Chybí typové anotace v některých funkcích

**Lokalizace:** `vcf_binary_reader.py` (ř. 24, 33), `vcf_geometry.py` (pomocné funkce)
**Popis:** Směs typovaných a neotypovaných funkcí.
**Mitigace:** Přidat typové anotace postupně při refactoringu.
**Odhad času:** Průběžně.

---

#### B‑LOW‑02: Duplicitní konstanta PANEL_FORMATS

**Lokalizace:**
- `vcf_config.py` — `_default_app_config()["panel_formats"]`
- `app_config.json` — `panel_formats`
**Popis:** Stejná data na dvou místech. Pokud je JSON načten, překryje default. Ale default je fallback. Konzistentní, ale matoucí při editaci.
**Mitigace:** Dokumentovat v `app_config.json` že přepisuje default. Případně odstranit default z kódu a ponechat jen JSON.
**Odhad času:** 15 min.

---

### 3.5 Souhrnná tabulka bugů a issue

| ID | Název | Priorita | Čas (h) | Dopad na smlouvu |
|---|---|---|---|---|
| B‑CRIT‑01 | Chybí `from vcf_parser import parse` API | **Kritická** | 0.5 | Nesplnění deliverable |
| B‑CRIT‑02 | Time prediction kalibrován na 13 datech | **Kritická** | 2-4 + 3 | Spor o accuracy |
| B‑CRIT‑03 | GCP credentials v app_config.json | **Kritická** | 0.25 | Security incident |
| B‑HIGH‑01 | Monolit vcf_geometry.py | **Vysoká** | 2 | Ztráta IP (QC Suite) |
| B‑HIGH‑02 | Monolitická parse_bytes() | **Vysoká** | 3-4 | Nelze licencovat bez KB |
| B‑HIGH‑03 | Duplicitní nesting detekce | **Vysoká** | 1 | Inkonzistentní výstupy |
| B‑MED‑01 | Nekalibrované hypotézy v machine_profile | **Střední** | 0.5 | Accuracy na jiných materiálech |
| B‑MED‑02 | Fail-safe režim vrací zavádějící data | **Střední** | 0.5 | Špatná interpretace výstupu |
| B‑MED‑03 | app.py monolit | **Střední** | 2-3 | Ztížený vývoj C2 |
| B‑LOW‑01 | Chybí typové anotace | **Nízká** | — | Kosmetika |
| B‑LOW‑02 | Duplicitní panel formats | **Nízká** | 0.25 | Matoucí |

---

## ČÁST 4: Refaktoringový plán

### 4.1 Cílová architektura (po refactoringu)

```
vcf_parser/                      ← Modul A — pip installovatelný, dodávaný klientovi
├── __init__.py                   ← from vcf_parser import parse(filepath) → dict
├── engine.py                     ← RuidaVcfEngineV20 (refaktorovaný, bez KB)
├── binary_reader.py              ← RE jádro (beze změny)
├── geometry.py                   ← Pouze parse_geometry (detekce odstraněna)
├── time_predictor.py             ← beze změny
├── machine_profile.json          ← kalibrovaný pro daný stroj
├── app_config.json               ← bez GCP secret, bez KB overrides
└── config.py                     ← vcf_config (beze změny)

systeq_kb/                        ← Samostatný balíček — NE dodávaný v Modulu A
├── __init__.py
├── engine.py                     ← KnowledgeBaseEngine (beze změny)
├── models.py                     ← EpistemicMetadata, Severity (beze změny)
├── rules.json                    ← Pravidla CLASS_A-D (beze změny)
└── geometry_detection.py         ← Extrakt z vcf_geometry (6 detekčních funkcí)

dashboard/                        ← Samostatný balíček — upsell
├── styles.py                     ← CSS (extrakt z app.py)
├── viz.py                        ← 2D visualizace (extrakt z app.py)
├── vcf_dashboard.py              ← VCF Streamlit app (refaktorovaná)
└── dxf_dashboard.py              ← C2 (bude implementováno)

scripts/
└── calibrate.py                  ← Kalibrační průvodce

tests/
└── ...                           ← beze změny
```

### 4.2 Fáze refaktoringu

#### Fáze 0 — Před podpisem smlouvy (TEĎ, 2-3 h)

| Krok | Akce | Čas | Výstup |
|---|---|---|---|
| 0.1 | Vytvořit `vcf_parser/__init__.py` + `vcf_parser/engine.py` | 30 min | Splňuje `from vcf_parser import parse` |
| 0.2 | Odstranit GCP secret z `app_config.json` | 15 min | Žádné credentials v dodávaném kódu |
| 0.3 | Přidat do `machine_profile.json` `"_warning": "Nekalibrováno"` | 5 min | Ochrana před sporem |
| 0.4 | Vytvořit `systeq_kb/` adresář s kopií KB engine | 1 h | IP ochrana |

#### Fáze 1 — Při podpisu (1. týden)

| Krok | Akce | Čas |
|---|---|---|
| 1.1 | Refaktorovat `vcf_parser/engine.py` — rozdělit `parse_bytes()` | 3-4 h |
| 1.2 | Extrahovat detekční funkce z `vcf_geometry.py` → `systeq_kb/geometry_detection.py` | 2 h |
| 1.3 | Upravit importy — engine neimportuje detekce | 1 h |
| 1.4 | Sjednotit nesting detekci (přesunout do KB) | 1 h |
| 1.5 | Vytvořit `scripts/calibrate.py` | 3 h |
| 1.6 | Přidat `vcf_parser` do `pyproject.toml` | 30 min |

#### Fáze 2 — Po akceptaci (2.-3. týden)

| Krok | Akce | Čas |
|---|---|---|
| 2.1 | Refaktorovat `app.py` → `dashboard/vcf_dashboard.py` + `dashboard/styles.py` + `dashboard/viz.py` | 2-3 h |
| 2.2 | Implementovat file watcher + GSheets (Modul B-A) | 14-24 h |
| 2.3 | Implementovat DXF Web UI (Modul C2) | 16-27 h |
| 2.4 | Kalibrovat `machine_profile.json` na Moodpasta stroji | 2-4 h |

### 4.3 Co NEDĚLAT (anti-patterns)

1. **Nepřepisovat celý engine** — refaktorovat postupně, zachovat funkčnost
2. **Nedávat KB modul do stejného balíčku jako engine** — oddělit pro licencování
3. **Necommitovat GCP credentials** — přesunout do `.env`
4. **Neslibovat accuracy před kalibrací** — přidat disclaimer do nabídky
5. **Nedělat pevnou cenu na C1** — risk je příliš vysoký (57-114 h, 40 % nejistota)

---

## ČÁST 5: Vazba na cenovou nabídku

### 5.1 Co se mění v nabídce po této analýze

| Položka | Původní | Po analýze |
|---|---|---|
| Modul A — stav | "85 % hotovo" | "85 % hotovo, ale chybí API wrapper (30 min)" |
| Time prediction | "95-99 % accuracy" | "±20-30 % bez kalibrace, cíl ±5-10 % po kalibraci" |
| GCP credentials | V app_config.json | Vyčištěno před dodáním |
| KB moduly | Součást engine | Odděleno, upsell |
| QC Suite | Zdarma (v engine) | Samostatný produkt 12 000 Kč |
| 2D Vizualizace | Zdarma (v app.py) | Samostatný produkt 8 000 Kč |

### 5.2 Revidovaná struktura nabídky

```
Fáze 1 — VCF automatizace                    43 000 Kč
  A: VCF Engine API                          10 000 Kč
     - from vcf_parser import parse
     - Deterministický parser, 22 iterací
     - machine_profile.json (po kalibraci)
  B-A: ETL lokální .exe                      15 000 Kč
  C2: DXF Web UI                             18 000 Kč
  ----------------------------------------------------
  Poznámka: Accuracy po kalibraci ±5-10 %
            (bez kalibrace ±20-30 %)

SYSTEQ Product Add-ons (volitelné, samostatná licence):
  QC Suite VCF (6 detekcí, risk score)       12 000 Kč
  2D Vizualizace s overlay defektů            8 000 Kč
  Layer Card + Risk Score report              4 000 Kč
  CNC Knowledge Corpus                       15 000 Kč

Fáze 2 — DXF Inference (samostatný projekt)  55 000 Kč
  C1: DXF Inference Engine
  Podmínka: přístup k 100+ párům DXF/VCF dat
  Poznámka: Jedná se o výzkumnou úlohu (expertní systém),
            nikoliv parser. ±20-30 % accuracy.
```

### 5.3 Argumentace pro upsell

Pro klienta (ne pro nabídku, ale pro jednání):

> "Parser vám dá číslo. QC Suite vám řekne, kde dělá Karel chyby dřív, než stroj začne řezat.
>
> Na ukázkovém souboru 1ks.VCF parser detekoval SEQUENCE_NESTING_ERROR — vnitřní prvek se řeže po vnějším. Confidence 0.891. Karel by to poznal až když stroj zajel do materiálu.
>
> QC Suite je samostatný produkt, není součástí parseru. Můžete si ho dokoupit kdykoliv."

---

## ČÁST 6: Akční plán — konkrétní kroky

### Dnes (25.6.)

| # | Akce | Čas |
|---|---|---|
| 1 | Vytvořit `vcf_parser/__init__.py` a `vcf_parser/engine.py` s `parse()` wrapperem | 30 min |
| 2 | Z `app_config.json` odstranit GCP credentials → `.env` | 15 min |
| 3 | Přidat disclaimer do `machine_profile.json` | 5 min |
| 4 | Commit + push (samostatný commit před refactoringem) | 5 min |

### Zítra (26.6.) — před odesláním nabídky

| # | Akce | Čas |
|---|---|---|
| 5 | Vytvořit `systeq_kb/` adresář s kopií KB engine | 1 h |
| 6 | Upravit nabídku — přidat poznámku o kalibraci | 30 min |
| 7 | Odeslat nabídku Františkovi | — |

### Po podpisu (1. týden)

| # | Akce | Čas |
|---|---|---|
| 8 | Refaktorovat `vcf_parser/engine.py` — rozdělit `parse_bytes()` | 3-4 h |
| 9 | Extrahovat detekční funkce → `systeq_kb/` | 2 h |
| 10 | Vytvořit `scripts/calibrate.py` | 3 h |
| 11 | Kalibrovat na Moodpasta stroji | 2-4 h |

---

## Metadata dokumentu

| Atribut | Hodnota |
|---|---|
| **Verze** | 1.0 |
| **Datum** | 2026-06-25 |
| **Autor** | outpost2026 |
| **Klasifikace** | Interní — není určeno pro klienta |
| **Vychází z** | Kompletní read-through vcf_parser_b2b/src/ (11 souborů, ~5 000 ř.) |
