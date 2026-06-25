# DEFECT CATALOG V1 — Ontologická báze detekovatelných výrobních chyb
## SYSTEQ CAM Automation — VCF Parser Module

**Verze:** 1.0 (Červen 2026)
**Autor:** SYSTEQ DEV (analýza geometrie + rešerše průmyslových zdrojů)
**Určení:** B2B jednání, technická specifikace, vývojový backlog

---

## 1. ÚVOD — Proč ontologická báze defektů?

Každý VCF soubor je digitální dvojče fyzického CNC řezu. Obsahuje kompletní geometrii
(elementy, vektory, segmenty), metadata (vrstvy, nástroje, rychlosti) a topologické
vztahy (pořadí řezu, vnoření, sousednost). Až dosud byla tato data využívána pouze
pro predikci času řezu a základní sekvenční audit.

**Nový vektor:** Využít geometrickou a topologickou informaci k detekci výrobních chyb
ještě před spuštěním stroje. Tento katalog systematicky kategorizuje chyby, které jsou
detekovatelné výhradně analýzou VCF dat — bez nutnosti fyzické kontroly.

### Zdroje této báze

| Zdroj | Typ | Příspěvek |
|-------|-----|-----------|
| Vlastní empirická analýza (parent_child_01.VCF) | Reverzní inženýrství | Detekce chybějícího mergenu (EDGE_MERGE_MISSING) |
| logo.VCF — 6 mikrosegmentů (0.21–0.52 mm) | Analytické testy | Varování na mikrosegmenty (MICRO_SEGMENT) |
| Veřejný průmyslový korpus (RapidDirect, Fictiv, Xometry) | Průmyslová rešerše | Klasifikace fyzických defektů (chatter, burrs, BUE) |
| Odborná literatura (ISO 2768, DFM guidelines) | Normativní | Toleranční a DFM pravidla |
| Osobní znalostní báze operátorů CNC (z deníků, viz docs/deniky/) | Tacitní znalosti | Reálné výrobní scénáře |

---

## 2. TAXONOMIE DEFEKTŮ

```
                        ┌─────────────────────────────────┐
                        │     DETEKOVATELNÉ DEFEKTY        │
                        │        (VCF analýza)              │
                        └─────────────────────────────────┘
                                     │
            ┌────────────────────────┼────────────────────────┐
            │                        │                        │
   ┌────────▼────────┐    ┌─────────▼─────────┐    ┌─────────▼─────────┐
   │  TŘÍDA A        │    │  TŘÍDA B           │    │  TŘÍDA C           │
   │  GRAFIK /       │    │  TECHNOLOG          │    │  NC KÓD /         │
   │  DESIGNER       │    │  CNC OPERÁTOR       │    │  POST-PROCESS     │
   │  (vstupní       │    │  (nastavení,        │    │  (generování       │
   │   kresličské    │    │   sekvence,         │    │   drah, CAM        │
   │   chyby)        │    │   parametry)        │    │   export)          │
   └─────────────────┘    └─────────────────────┘    └────────────────────┘
```

### Třída A — Grafické/designerské chyby (vstupní výkres)

Chyby vzniklé při kreslení v CAD. Grafik/designér je vnáší do výkresu nevědomky —
přehlédnutím, nedodržením standardů, nebo chybou v pracovním postupu.

### Třída B — Technologické chyby (CNC operátor / nastavení)

Chyby vzniklé při přiřazování nástrojů, nastavování vrstev, sekvencí řezu a
technologických parametrů. Operátor nebo technolog je vnáší při přípravě CAM.

### Třída C — NC kód / Post-process chyby

Chyby vzniklé při exportu z CAM do strojového kódu, nebo při samotném generování
G-code. Detekovatelné pouze u VCF souborů, které obsahují stopy po post-processu.

---

## 3. KATALOG DEFEKTŮ — TŘÍDA A (Grafik / Designer)

### A01 — CHYBĚJÍCÍ MERGE (EDGE_MERGE_MISSING)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `EDGE_MERGE_MISSING` |
| **Název** | Nesloučený prvek — otevřená křivka uvnitř uzavřeného elementu |
| **Severity** | WARNING |
| **Frekvence** | Střední (odhad 5–15 % výkresů) |
| **Detekce** | Otevřená křivka (type_id=0) s bboxem uvnitř bboxu uzavřeného elementu |
| **Reálný case** | `parent_child_01.VCF` — Element_10 uvnitř Element_1 |
| **Priorita** | **P0** — implementováno |
| **Vizuální overlay** | V7 — purpurová #A855F7, tečkovaná čára |
| **Výstup** | `"Otevřená křivka ({id}) {leží uvnitř / navazuje na hranu} prvku ({parent}). Pravděpodobně nebyl mergován."` |

### A02 — NEDOKONČENÁ KŘIVKA (UNCLOSED_LOOP)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `UNCLOSED_LOOP` |
| **Název** | Neuzavřená smyčka — polygon s gapem mezi start a end |
| **Severity** | WARNING / CRITICAL (podle velikosti gapu) |
| **Frekvence** | Vysoká (zmíněno provozním manažerem na B2B jednání) |
| **Detekce** | Element deklarovaný jako uzavřený (type_id=1), ale |start - end| > 1 mm |
| **Mechanismus** | Porovnání prvního a posledního vertexu v seznamu |
| **Hraniční hodnoty** | 0.1–1.0 mm: INFO, 1.0–5.0 mm: WARNING, > 5.0 mm: CRITICAL |
| **Priorita** | **P1** |
| **Vizuální overlay** | V11 — červená přerušovaná čára mezi start a end + kroužek na gapu |

### A03 — MIKROSEGMENT (MICRO_SEGMENT)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `MICRO_SEGMENT` |
| **Název** | Segment kratší než 1 mm — zbytečný detail nebo chyba exportu |
| **Severity** | WARNING |
| **Frekvence** | Nízká (nalezeno v logo.VCF, 4 elementy) |
| **Detekce** | Scan všech segmentů všech elementů |
| **Reálný case** | `logo.VCF` — segmenty 0.21–0.52 mm v logu "S" a "O" |
| **Dopad** | Vibrace nástroje, nedorez, zvýšené opotřebení břitu |
| **Priorita** | **P1** |
| **Vizuální overlay** | V8 — oranžové kroužky na vrcholech mikrosegmentů |

### A04 — TÉMĚŘ NULOVÝ SEGMENT (ZERO_LENGTH_SEGMENT)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `ZERO_LENGTH_SEGMENT` |
| **Název** | Segment < 0.1 mm — degenerovaná geometrie |
| **Severity** | CRITICAL |
| **Frekvence** | Velmi nízká |
| **Detekce** | Scan segmentů, délka < 0.1 mm |
| **Dopad** | Stroj se zasekne, nekonečný mikropohyb, havárie |
| **Priorita** | **P2** |

### A05 — SEBE-PRŮNIK (SELF_INTERSECTION)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `SELF_INTERSECTION` |
| **Název** | Element protíná sám sebe — křivka se kříží |
| **Severity** | WARNING |
| **Frekvence** | Nízká |
| **Detekce** | Detekce průsečíků nepřilehlých segmentů v rámci 1 elementu |
| **Dopad** | Přetížení nástroje, dvojitý řez na stejném místě |
| **Priorita** | **P3** |

### A06 — DUPLICITNÍ ELEMENT (DUPLICATE_ELEMENT)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `DUPLICATE_ELEMENT` |
| **Název** | Dva totožné elementy na stejné pozici |
| **Severity** | WARNING |
| **Frekvence** | Nízká–střední (časté při kopírování vrstev) |
| **Detekce** | Porovnání párů: počet bodů, délka, centroid < 1 mm |
| **Dopad** | Dvojnásobný čas řezu, zničení materiálu v místě překryvu |
| **Priorita** | **P3** |

### A07 — ŠPIČATÝ ÚHEL (SPIKE_DETECT)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `SPIKE_DETECT` |
| **Název** | Úhel mezi segmenty < 15° nebo > 165° — kreslířská chyba |
| **Severity** | WARNING |
| **Frekvence** | Střední |
| **Detekce** | Úhel mezi vektory (již částečně implementováno v complexity) |
| **Dopad** | Trhání materiálu, vytržení nástroje |
| **Priorita** | **P3** |

### A08 — PŘEKRYV ELEMENTŮ (ELEMENT_OVERLAP)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `ELEMENT_OVERLAP` |
| **Název** | Dva uzavřené elementy se kříží (nejsou soustředné) |
| **Severity** | CRITICAL |
| **Frekvence** | Nízká |
| **Detekce** | Detekce průsečíků segmentů napříč elementy |
| **Dopad** | Zničení obou dílů, kolize nástroje |
| **Priorita** | **P4** |

### A09 — DEGENEROVANÝ TVAR (DEGENERATE_SHAPE)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `DEGENERATE_SHAPE` |
| **Název** | Polygon s < 3 unikátních vrcholů — nemá plochu |
| **Severity** | CRITICAL |
| **Frekvence** | Velmi nízká |
| **Detekce** | Počet unikátních vrcholů v elementu |
| **Dopad** | Stroj neprovede žádný řez (ztráta času) nebo chyba |
| **Priorita** | **P4** |

---

## 4. KATALOG DEFEKTŮ — TŘÍDA B (Technolog / CNC operátor)

### B01 — CHYBA SEKVENCIE VRSTEV (SEQUENCE_LAYER_ERROR)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `SEQUENCE_LAYER_ERROR` |
| **Název** | Obvodový ořez probíhá před dekorativními operacemi |
| **Severity** | CRITICAL |
| **Frekvence** | Střední |
| **Detekce** | Porovnání offsetů vibrate vrstev vs. V-slot/dekor vrstev |
| **Reálný case** | `Ofset_bbox_vibrate_first.VCF` vs `_last.VCF` |
| **Stav** | **Implementováno** (KB engine: RULE_SEQ_OUTER_LAST) |
| **Vizuální overlay** | V2–V6 (stávající implementace) |

### B02 — CHYBA SEKVENCIE ELEMENTŮ (SEQUENCE_NESTING_ERROR)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `SEQUENCE_NESTING_ERROR` |
| **Název** | Vnitřní prvek se řeže po vnějším obvodu (špatné pořadí) |
| **Severity** | WARNING / CRITICAL |
| **Frekvence** | Střední |
| **Detekce** | Bbox containment + offset comparison |
| **Stav** | **Implementováno** (KB engine) |
| **Vizuální overlay** | V3 — Nesting BBOX, V4 — Anotace |

### B03 — RIZIKO VAKUOVÉ FIXACE (VACUUM_FIXATION_RISK)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `VACUUM_FIXATION_RISK` |
| **Název** | Malá plocha panelu — hrozí posun při řezu |
| **Severity** | WARNING / CRITICAL |
| **Frekvence** | Střední |
| **Detekce** | Canvas area < threshold (1.67 m² / 0.5 m²) |
| **Stav** | **Implementováno** (KB engine: RULE_FIX_SMALL_PANEL) |
| **Vizuální overlay** | V5 — Canvas-level oranžový border |

### B04 — SUBOPTIMÁLNÍ H2 (H2_SUBOPTIMAL / H2_NO_CUT_THROUGH)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `H2_SUBOPTIMAL`, `H2_NO_CUT_THROUGH` |
| **Název** | Výška hrotu H2 není v ideálním rozsahu |
| **Severity** | INFO / WARNING / CRITICAL |
| **Frekvence** | Vysoká |
| **Detekce** | Porovnání H2 s ideálním rozsahem dle tloušťky materiálu |
| **Stav** | **Implementováno** (KB engine: RULE_H2_VIBRATE_12MM, RULE_H2_VIBRATE_24MM) |

### B05 — NEDOSTATEČNÁ VŮLE VNOŘENÍ (NESTING_CLEARANCE)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `NESTING_CLEARANCE` |
| **Název** | Příliš těsné vnoření — vzdálenost mezi hranami < kerf nástroje |
| **Severity** | WARNING |
| **Frekvence** | Střední (časté u složitých tvarů) |
| **Detekce** | Minimální vzdálenost mezi segmenty vnořených elementů |
| **Mechanismus** | Vzdálenost: `min(outer_path - inner_path) < tool_kerf (např. 2 mm)` |
| **Dopad** | Průnik do sousedního dílu, zničení obou |
| **Priorita** | **P2** |
| **Vizuální overlay** | V12 — červená výplň v kritické zóně |

### B06 — PŘESAH MŮSTKŮ (TAB_OVERLAP)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `TAB_OVERLAP` |
| **Název** | Můstky dvou sousedních elementů ve stejné Y pozici |
| **Severity** | WARNING |
| **Frekvence** | Nízká–střední |
| **Detekce** | Identifikace můstkového patternu (7-segment: 3.23/10.12/10.5/14.82...) + porovnání Y pozic u sousedících elementů |
| **Reálný case** | `parent_child_01.VCF` — můstkový pattern ve všech 10 elementech |
| **Dopad** | Oba elementy se uvolní současně — posun/vibrace |
| **Priorita** | **P3** |

### B07 — NEKONZISTENTNÍ VRSTVY (LAYER_INCONSISTENCY)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `LAYER_INCONSISTENCY` |
| **Název** | Podobná geometrie na různých typech nástrojů |
| **Severity** | INFO / WARNING |
| **Frekvence** | Nízká |
| **Detekce** | Porovnání geometrických příznaků napříč vrstvami (počet bodů, délka, bbox poměr stran) |
| **Dopad** | Možná chyba v přiřazení nástroje |

### B08 — SIROTEK (ORPHAN_ELEMENT)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `ORPHAN_ELEMENT` |
| **Název** | Element izolovaný od zbytku výkresu |
| **Severity** | WARNING |
| **Frekvence** | Nízká |
| **Detekce** | Bbox centroid vzdálen > 500 mm od všech ostatních |
| **Dopad** | Zapomenutý díl na desce, nečekaný řez |
| **Priorita** | **P4** |
| **Vizuální overlay** | V10 — modrý obdélník okolo osamoceného elementu |

### B09 — NESYMETRICKÝ PÁR (ASYMMETRIC_PAIR)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `ASYMMETRIC_PAIR` |
| **Název** | Očekávaná symetrie není dokonalá |
| **Severity** | WARNING |
| **Frekvence** | Nízká |
| **Detekce** | Porovnání elementů s podobným bboxem v symetrických pozicích |
| **Dopad** | Díly nesedí při montáži |

### B10 — TĚSNÁ MEZERA (NEAR_MISS_GAP)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `NEAR_MISS_GAP` |
| **Název** | Endpointy dvou elementů se téměř dotýkají (gap 1–5 mm) |
| **Severity** | INFO / WARNING |
| **Frekvence** | Střední (zmíněno provozním manažerem) |
| **Detekce** | Vzdálenost endpointů napříč elementy |
| **Mechanismus** | Gap 0.5–1 mm: INFO, 1–5 mm: WARNING, > 5 mm: samostatný element |
| **Dopad** | Vizuálně neviditelná mezera, díl nesedí |
| **Priorita** | **P3** |
| **Vizuální overlay** | V13 — žlutá spojnice mezi endpointy s popisem gapu |

---

## 5. KATALOG DEFEKTŮ — TŘÍDA C (Post-process / NC kód)

### C01 — DEFEKTNÍ IMPORT BAREV (COLOR_MAP_MISMATCH)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `COLOR_MAP_MISMATCH` |
| **Název** | Barva elementu neodpovídá žádné vrstvě |
| **Severity** | WARNING |
| **Detekce** | `mapped_layer_idx == -1` při parsování geometrie |
| **Stav** | **Implementováno** (parser přiřadí -1) |

### C02 — AGRESIVNÍ DATA (AGGREGATED_JOB)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `AGGREGATED_JOB` |
| **Název** | Soubor obsahuje data z více zakázek |
| **Severity** | WARNING |
| **Detekce** | BFS clustering na základě bbox vzdáleností |
| **Stav** | **Implementováno** (vcf_parser_v20.py) |

### C03 — NOVÁ VERZE VCF (UNKNOWN_VERSION)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `UNKNOWN_VERSION` |
| **Název** | Detekována nová verze VCF formátu |
| **Severity** | CRITICAL |
| **Detekce** | Chybějící magic header `RDVCUT`, `VER1.0.012`, `VER1.0.013` |
| **Stav** | **Implementováno** (fail-safe mód) |

### C04 — CHYBĚJÍCÍ NEBO POŠKOZENÁ GEOMETRIE (CORRUPT_GEOMETRY)

| Atribut | Hodnota |
|---------|---------|
| **Kód** | `CORRUPT_GEOMETRY` |
| **Název** | Binární data nelze přečíst — poškozený soubor |
| **Severity** | CRITICAL |
| **Detekce** | Výjimka při `struct.unpack_from` v parsování geometrie |
| **Stav** | **Implementováno** (try/except v parse_geometry_v18_2) |

---

## 6. MATICE SEVERITY × FREKVENCE

```
                    FREKVENCE
               ┌──────┬──────┬──────┐
               │NÍZKÁ │STŘED │VYSOKÁ│
      ┌────────┼──────┼──────┼──────┤
      │INFO    │ C04  │ B07  │ B04  │
      │        │ C03  │      │(H2)  │
      ├────────┼──────┼──────┼──────┤
S E V │WARNING │ A03  │ A01  │ A02  │
E R I │        │ A05  │ B05  │(uncl.)│
T Y   │        │ A07  │ B10  │      │
      │        │ B06  │ B01  │      │
      │        │ B08  │      │      │
      ├────────┼──────┼──────┼──────┤
      │CRITICAL│ A04  │ B02  │  -   │
      │        │ A08  │ B03  │      │
      │        │ A09  │ (nest)      │
      │        │ C02  │ (fix)       │
      └────────┴──────┴──────┴──────┘
```

### Priority implementace

| Priorita | Kód | Důvod |
|----------|-----|-------|
| **P0** | A01 | EDGE_MERGE_MISSING — reálný case, již rozpracováno |
| **P1** | A02 | UNCLOSED_LOOP — požadavek provozního manažera na B2B |
| **P1** | A03 | MICRO_SEGMENT — reálný case v logo.VCF |
| **P2** | A04 | ZERO_LENGTH_SEGMENT — potenciální havárie stroje |
| **P2** | B05 | NESTING_CLEARANCE — ochrana nástroje i materiálu |
| **P3** | A05, A06, A07, B06, B10 | Střední priorita |
| **P4** | A08, A09, B08 | Nízká priorita, složitější implementace |

---

## 7. IMPLEMENTAČNÍ ARCHITEKTURA — DETEKČNÍ PIPELINE

```
                    ┌─────────────────────┐
                    │   VCF binary data    │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  vcf_binary_reader   │
                    │  (extract layers,    │
                    │   strings, colors)   │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   vcf_geometry.py    │
                    │  (parse_geometry,   │
                    │   group, classify,  │
                    │   adjacency check)  │◄── NOVÉ: is_point_near_path()
                    └──────────┬──────────┘    │   detect_unmerged_tabs()
                               │               │   detect_micro_segments()
                    ┌──────────▼──────────┐    │   detect_self_intersection()
                    │  vcf_parser_v20.py   │    │   detect_duplicate_elements()
                    │  (engine, bbox       │    │   detect_gaps()
                    │   containment,       │    │   detect_orphans()
                    │   parent-child)      │    └── detect_clearance()
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Knowledge_base/     │
                    │  engine.py           │
                    │  (validate_all)      │◄── NOVÉ: validate_edge_merge()
                    │                      │    │   validate_micro_segments()
                    │                      │    │   validate_clearance()
                    └──────────┬──────────┘    │   validate_orphans()
                               │
                    ┌──────────▼──────────┐
                    │   app.py             │
                    │  (vizualizace,       │
                    │   overlay vrstvy)    │◄── NOVÉ: V7, V8, V9, V10, V11, V12, V13
                    └─────────────────────┘
```

---

## 8. VIZUÁLNÍ PALETA — ROZŠÍŘENÍ OVERLAY VRSTEV

| Vrstva | Kód | Barva | Hex | Tailwind | Typ zvýraznění |
|--------|-----|-------|-----|----------|----------------|
| V1 | BASE | Dle vrstvy | — | — | Element path |
| V2 | SEVERITY LINE | Červená/Oranžová | #F43F5E / #F59E0B | rose/amber | Tlustá čára (lw=4) |
| V3 | NESTING BBOX | Červená/Oranžová | #F43F5E / #F59E0B | rose/amber | Čárkovaný obdélník + text |
| V4 | ANNOTATION | Červená | #F43F5E | rose-500 | Text u centroidu |
| V5 | CANVAS | Oranžová | #F59E0B | amber-500 | Canvas border |
| V6 | LEGEND | Dle potřeb | — | — | Mimo kresbu |
| **V7** | **MERGE MISSING** | **Purpurová** | **#A855F7** | **purple-500** | **Tečkovaná čára + "MERGE?"** |
| **V8** | **MICRO SEGMENT** | **Oranžová** | **#F59E0B** | **amber-500** | **Kroužky na vrcholech** |
| **V9** | **SELF-INTERSECTION** | **Červená** | **#F43F5E** | **rose-500** | **X v místě křížení** |
| **V10** | **ORPHAN** | **Modrá** | **#3B82F6** | **blue-500** | **Obdélník okolo sirotka** |
| **V11** | **UNCLOSED LOOP** | **Červená** | **#F43F5E** | **rose-500** | **Přerušovaná spojnice gapu** |
| **V12** | **CLEARANCE** | **Červená výplň** | **#F43F5E** | **rose-500** | **Výplň kritické zóny** |
| **V13** | **NEAR-MISS GAP** | **Žlutá** | **#EAB308** | **yellow-500** | **Spojnice + popis gapu** |

---

## 9. SROVNÁNÍ S PRŮMYSLOVÝM STANDARDEM

Konkurenční nástroje a jejich schopnost detekce defektů:

| Schopnost | SYSTEQ VCF | VCarve Pro | LightBurn | Ruida nativní | Poznámka |
|-----------|-----------|------------|-----------|---------------|----------|
| Detekce chybného pořadí řezu | ✅ | ❌ | ❌ | ❌ | Vlastní KB engine |
| Detekce H2 mimo toleranci | ✅ | ❌ | ❌ | ❌ | Vlastní KB engine |
| Vakuová fixace | ✅ | ❌ | ❌ | ❌ | Vlastní KB engine |
| Detekce mikrosegmentů | 🚧 P1 | ❌ | ❌ | ❌ | Nová detekce |
| Neuzavřené křivky | 🚧 P1 | ❌ | ❌ | ❌ | Nová detekce |
| Chybějící merge | 🚧 P0 | ❌ | ❌ | ❌ | **Unikátní** |
| Predikce času řezu | ✅ ±2-5% | ✅ (hrubá) | ❌ | ❌ | Vlastní model |
| 2D overlay vizualizace | ✅ | ✅ | ✅ | ❌ | Vlastní vrstvy |
| Detekce překryvu elementů | 🚧 P4 | ❌ | ❌ | ❌ | |
| Detekce sirotků | 🚧 P4 | ❌ | ❌ | ❌ | |
| Detekce přesahu můstků | 🚧 P3 | ❌ | ❌ | ❌ | **Unikátní** |
| ERP/Odoo export | ✅ | ❌ | ❌ | ❌ | B2B vrstva |
| Automatická detekce formátu panelu | ✅ | ❌ | ❌ | ❌ | Vlastní geometrie |

---

## 10. B2B HODNOCENÍ — OBCHODNÍ DOPAD

### 10.1 Kvantifikace úspor

| Metrika | Odhad | Zdroj |
|---------|-------|-------|
| Náklady na 1 zmetek (materiál + čas) | 2 000–15 000 Kč | Provozní data |
| Frekvence zmetků z chyb ve výkresu | 3–8 % zakázek | Průmyslový odhad |
| Úspora při detekci 50 % zmetků | 30–200 Kč/zakázka | Konzervativní odhad |
| Roční úspora při 1000 zakázkách | 30 000–200 000 Kč | Pro malou dílnu |

### 10.2 Prodejní argumenty pro CEO

1. **"První nástroj na trhu"** — Žádný z konkurenčních nástrojů (VCarve, LightBurn, Ruida native) neumožňuje automatickou detekci grafických chyb ve VCF. SYSTEQ by byl první.

2. **"Z metku do zisku"** — Detekce chyb PŘED řezem. Jediná zachráněná zakázka zaplatí licenci na rok.

3. **"Inženýrský storytelling"** — Každý defekt má reálný case study (parent_child_01.VCF = skutečná výrobní havárie, kterou parser odhalil).

4. **"Škálovatelná báze znalostí"** — Nová KB pravidla lze přidávat bez zásahu do jádra parseru. Každá další detekce zvyšuje hodnotu nástroje.

5. **"Důvěra skrze transparentnost"** — Vizuální overlay ukazuje operátorovi PŘESNĚ kde je chyba. Žádné "červené tlačítko bez kontextu".

### 10.3 Rizika a limity

| Riziko | Mitigace |
|--------|----------|
| False positive (falešný poplach) | Každé pravidlo má confidence skóre; CLASS_D = hypotéza |
| Různá verze VCF formátu | Fail-safe mód, parser se nezasekne |
| Výkon u velkých souborů | Batch zpracování (LineCollection, numpy) |
| Uživatelská adopce | Overlay se zobrazí JEN při varování (High SNR princip) |

---

## 11. ZDROJE A REŠERŠE

### Veřejné zdroje

| Zdroj | Popis |
|-------|-------|
| RapidDirect — CNC Machining Defects Guide (2026) | Typy defektů: chatter, burrs, BUE, thermal damage |
| Fictiv — CNC Machining Tolerances & Errors | Toleranční analýza, ISO 2768-m |
| CNC Cookbook — Common CNC Mistakes | Praktické chyby operátorů |
| Wikipedia — CNC router | Základní technologie |

### Interní zdroje

| Zdroj | Popis |
|-------|-------|
| `docs/deniky/` | Digitalizované deníky z provozu CNC |
| `docs/handoffs/` | JSON specifikace VCF formátu |
| `src/Knowledge_base/rules.json` | Existující KB pravidla |
| `demo_data/` | 21 testovacích VCF souborů |

---

## 12. VERZOVÁNÍ A DALŠÍ VÝVOJ

| Verze | Datum | Změny |
|-------|-------|-------|
| v1.0 | Červen 2026 | První vydání — 20 defektů ve 3 třídách |
| v1.1 | Q3 2026 | Implementace P0–P2, testování na reálných datech |
| v2.0 | Q4 2026 | Zpětná vazba z provozu, kalibrace thresholdů |
| v3.0 | 2027 | ML model pro predikci defektů na základě historie |

---

*Katalog je živý dokument — bude aktualizován na základě nových nálezů z provozu,
zpětné vazby operátorů a výsledků testování.*

*SYSTEQ CAM Automation — Deterministic CNC Parser — Červen 2026*
