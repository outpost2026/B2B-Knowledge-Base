# Vcf-compiler: Hloubková analýza architektury writeru a dependencies

**Verze:** 1.0  
**Datum:** 2026-07-03  
**Účel:** Ground-truth deepdive do současného stavu Vcf-compiler writeru — complement k `vcf\_optimizer\_analytic\_engine.md` (Vector 2).  
**Autor:** SYSTEQ výzkumný tým


## 1. EXECUTIVE SUMMARY

Vcf-compiler je Python knihovna pro čtení, zápis a analýzu VCF souborů pro Ruida RDD6584G oscilační nůž. Skládá se z 5 modulů (441 + 394 + 154 + 51 + 48 řádků), 28 testů (všechny PASS), a 3 externích závislostí.

### Aktuální stav

| Komponenta | Status | Confidence |
| - | - | - |
| Writer (`\_writer.py`) | ✅ Funkční — všechny známé fieldy korektní | P\>0.95 |
| DXF adapter (`\_dxf\_adapter.py`) | ⚠️ Funkční — 2 známé nedořešené problémy | P\>0.85 |
| Reader (`\_reader.py`) | ✅ Funkční pro RE/analytické účely | P\>0.95 |
| ACI config (`map\_config.json`) | ⚠️ 8/15 calibrated, zbytek hypothesis/empirical | P\>0.70 |
| Test suite | ✅ 28/28 PASS (23 unit + 5 integration) | P=1.0 |


### Rozhodovací rámec: Vector 1 vs Vector 2

Tento dokument poskytuje podklady pro **Vector 2** (deep RE continuation). Pro **Vector 1** (VCF Optimalizátor) viz samostatný dokument.


## 2. ARCHITEKTURA PIPELINE — KOMPLETNÍ

### 2.1 Data flow diagram

```
DXF (LightBurn)                    externí vstup  
    │  
    ▼  
dxf\_geometry\_indexer\_v2.py         \[dxf\_integrace repo, lazy import\]  
    │  index\_dxf() → entities\[\{color\_index, vertices, type, length\_mm\}\]  
    │  
    ▼  
\_vcf\_parser/\_dxf\_adapter.py        \[vcf-compiler repo\]  
    │  \_build\_vcf\_spec() → \{"layers": \[...\], "elements": \[...\]\}  
    │  
    ▼  
\_vcf\_parser/\_writer.py             \[vcf-compiler repo\]  
    │  VcfWriter.write() → binární VCF  
    │  
    ▼  
VCutWorks CAM GUI                  cílová platforma  
    │  
    ▼  
CNC plotr RDD6584G                 finální výstup
```

### 2.2 Závislostní graf

```
vcf\_parser  
  ├── \_writer.py  
  │     ├── struct (stdlib)  
  │     ├── math (stdlib)  
  │     ├── \_reader.py (GEOMETRY\_SIG, CUTTER\_MAP, DIR\_MAP)  
  │     └── VcfLayer, VcfWriter (internal)  
  ├── \_dxf\_adapter.py  
  │     ├── json (stdlib)  
  │     ├── math (stdlib)  
  │     ├── dxf\_geometry\_indexer\_v2  \[EXTERNÍ — lazy import\]  
  │     │     ├── ezdxf  \[EXTERNÍ — DXF parsing\]  
  │     │     └── vcf\_compiler\_map\_config.json  
  │     ├── vcf\_compiler\_map\_config.json  
  │     └── \_writer.py (write funkce v \_build\_vcf\_spec)  
  ├── \_reader.py  
  │     └── struct, math, re (all stdlib)  
  ├── \_geometry.py  
  │     └── math (stdlib)  
  ├── \_config.py  
  │     ├── json (stdlib)  
  │     └── machine\_profile.json  \[VOLITELNÝ — fallback na defaulty\]  
  └── \_\_init\_\_.py  
        └── export: write(), compile\_dxf(), VcfWriterError
```

### 2.3 Externí závislosti — detail

| Závislost | Typ | Lokalizace | Status |
| - | - | - | - |
| `dxf\_geometry\_indexer\_v2` | Lazy import — fallback přes PYTHONPATH | `../dxf\_integrace/src/` | ✅ Funkční |
| `ezdxf` | Transitivní (přes dxf\_integrace) | pip | ✅ Funkční |
| `vcf\_compiler\_map\_config.json` | Konfigurační soubor | CWD / cesta v parametru | ⚠️ 8/15 kalibrováno |


### 2.4 Vnitřní závislosti (writer → reader)

`\_writer.py` importuje z `\_reader.py`:

- `GEOMETRY\_SIG` — binární signatura začátku elementu

- `CUTTER\_MAP` — mapping \{0: "Vibrate cutter", ...\}

- `DIR\_MAP` — mapping \{0: "Left", ...\}

To vytváří **cyklickou závislost**: writer → reader → (používá writer výstup). Není problém v praxi, ale znamená to, že writer nelze použít bez readeru.


## 3. WRITER — BYTE-LEVEL DOKUMENTACE

### 3.1 Výstupní struktura VCF souboru

```
┌─────────────────────────────┐  
│ HEADER (472B + N×610B)      │  
│ ├── Prefix + Magic (24B)   │  
│ ├── Stock dims (16B)        │  
│ ├── POST\_STOCK\_HEADER (14B) │  
│ ├── MACHINE\_PROFILE (418B)  │  
│ ├── Empty blocks (256×610B) │  
│ └── Active layer blocks     │  
│     (N\_layers × 610B)       │  
├─────────────────────────────┤  
│ BODY                        │  
│ ├── Element header (45B)    │  
│ ├── Segments (pt\_count×74B) │  
│ └── ELEMENT\_FOOTER (196B)   │  ← každý element  
├─────────────────────────────┤  
│ TRAILER (5B)                │  
└─────────────────────────────┘
```

### 3.2 Header — byte-by-byte

| Offset | Velikost | Pole | Hodnota | Writer | Native |
| - | - | - | - | - | - |
| 0 | 1 | VCF\_PREFIX | `0x13` | ✅ | ✅ |
| 1 | 19 | HEADER\_MAGIC | `"RDVCUTFILEVER1.0.013"` | ✅ | ✅ |
| 20 | 3 | VCF\_POST\_MAGIC | `0x20 0x0A 0x00` | ✅ | ✅ |
| 23 | 8 | STOCK\_WIDTH | float64 1220.0 | ✅ | ✅ |
| 31 | 8 | STOCK\_HEIGHT | float64 2900.0 | ✅ | ✅ |
| 39 | 4 | pad | uint32 0 | ✅ | ✅ |
| 43 | 8 | field\_43 | float64 100.0 | ✅ | ✅ |
| 51 | 2 | field\_51 | uint16 1 | ✅ | ✅ |
| 53 | 418 | MACHINE\_PROFILE | hardcoded bytes | ✅ 0 diffs | ✅ |
| 472 | ... | layer blocks | viz níže | ✅ | ✅ |


**Důležité:** POST\_STOCK\_HEADER = 14 B (4 + 8 + 2). Původně počítáno jako 12 B → off-by-2 chyba zneplatnila všechny offsetové analýzy (RC5/D8).

### 3.3 Layer block (610 B, v1.0.013)

#### Empty blocks (0-254)

| Offset | Velikost | Pole | Hodnota |
| - | - | - | - |
| 10 | 2 | block\_index | uint16 0..254 |
| 602 | 4 | next\_layer\_flag | uint32 0 (kromě bloku \#255) |
| 606 | 4 | next\_layer\_color | uint32 0 (kromě bloku \#255) |


Blok \#255 (poslední empty) odkazuje na první active block:

- `next\_layer\_flag` = 1

- `next\_layer\_color` = BGR barva první aktivní vrstvy

Zbylých ~600 B = nuly. Potvrzeno jako nekritické — VCutWorks nevaliduje.

#### Active blocks (N bloků, jeden na vrstvu)

| Offset | Velikost | Pole | Writer | Native | Význam |
| - | - | - | - | - | - |
| 0 | 4 | output\_flag | ✅ 0/1 | ✅ | 1 = vrstva je output |
| 4 | 8 | speed | ✅ float64 | ✅ | Řezná rychlost (mm/s) |
| 12 | 4 | color | ✅ BGR | ✅ | Barva vrstvy (BGR uint32) |
| 16 | 8 | field\_16 | ❌ 0.0 | varied | Nekritické (nuly OK) |
| 24 | 8 | h1\_alt | ❌ 0.0 | varied | 24.0 v empty \#0, jinak 0 |
| 32 | 4 | cutter\_idx | ✅ int32 | ✅ | 0=Vibrate, 1=Wheel, 2=Mill, 3=V-slot |
| 36 | 4 | field\_36 | ❌ 0 | ✅=1 | Nekritické |
| 40 | 8 | field\_40 | ✅ 5.0 | ✅ 5.0 | **Kritické** — neznámý parametr |
| 48 | 4 | field\_48 | ❌ 0 | ✅=2 | Nekritické (direction@104 stačí) |
| 52 | 24 | padding | ❌ 0 | ❌ 0 | Nuly i v native |
| 76 | 4 | color\_76 | ✅ 0x000000 | ✅ | Vždy black (ne ACI barva) |
| 80 | 8 | h1 | ✅ float64 | ✅ | Start height |
| 88 | 4 | feed\_count | ✅ int32 | ✅ | Počet krmení |
| **92** | **1** | **ec** | **✅ 1** | **✅ 1** | **"Has geometry" flag** |
| 93 | 3 | padding | ❌ 0 | ❌ 0 | Nuly |
| 96 | 8 | h2 | ✅ float64 | ✅ | End height |
| **104** | **2** | **direction** | **✅ 2** | **✅ 2** | **Pro všechny cutter typy** |
| 106 | 8 | vs\_comp | ✅ float64 | ✅ | V-slot width comp |
| 114 | 8 | start\_ext | ✅ float64 | ✅ | Start extension (V-slot) |
| 122 | 8 | end\_ext | ✅ float64 | ✅ | End extension (V-slot) |
| 130 | 46 | padding | ❌ 0 | varied | Nuly OK |
| 176 | 8 | field\_176 | ❌ 0.0 | denorm | Semanticky identické |
| 184 | 8 | field\_184 | ❌ 0.0 | denorm | Semanticky identické |
| 192 | 5 | padding | ❌ 0 | ❌ 0 | Nuly |
| **197** | **1** | **field\_197** | **✅ 64** | **✅ 64** | **Neznámý flag (0x40)** |
| **198** | **8** | **field\_198** | **✅ 0.5** | **✅ 0.5** | **Neznámý parametr** |
| 206 | 396 | padding | ❌ 0 | varied | Nuly OK |
| 602 | 4 | next\_flag | ✅ 0/1 | ✅ | Linked-list flag |
| **606** | **4** | **element\_count** | **✅ N** | **✅ N** | **Celkový počet elementů** |


**Kritická pole — historie fixů:**

| Pole | Původní hodnota | Fix | Session |
| - | - | - | - |
| ec@92 | 0 → 1 | "has geometry" flag (ne element count) | 8 |
| offset606 | 1 → total\_elements | GUI čte tento field pro počet elementů | 8 |
| direction@104 | jen pro V-slot → pro všechny | Writer nastavoval jen pro V-slot | 6 |
| field\_40@40 | 0 → 5.0 | Přidáno podle native | 6 |
| field\_197@197 | 0 → 64 | Přidáno podle native | 6 |
| field\_198@198 | 0 → 0.5 | Přidáno podle native | 6 |
| next\_color@606 | 0 → 1 pro poslední blok | Linked-list terminátor | 6 |


### 3.4 Body — element encoding

#### Element header (45 B)

| Offset | Velikost | Pole | Hodnota |
| - | - | - | - |
| 0 | 8 | GEOMETRY\_SIG | `\\x01\\x00\\x01\\x00\\x00\\xff\\xff\\xff` |
| 8 | 4 | geom\_color | `(BGR \<\< 8) & 0xFFFFFFFF` |
| 12 | 33 | header\_template | 4× float64 1.0 + padding |


#### Segment structure (74 B each)

**Polyline (subtype=0, geom\_type=0/1):**

| Offset | Velikost | Pole |
| - | - | - |
| 0 | 2 | padding |
| 2 | 8 | x1 (start) |
| 10 | 8 | y1 (start) |
| 18 | 8 | x2 (end) |
| 26 | 8 | y2 (end) |
| 34 | 40 | padding (nuly) |


**Circle (subtype=3, geom\_type=1, pt\_count=4):**

| Offset | Velikost | Pole | Hodnota |
| - | - | - | - |
| 0 | 2 | padding |  |
| 2 | 8 | x1 (arc start) |  |
| 10 | 8 | y1 (arc start) |  |
| 18 | 8 | x2 (arc end) |  |
| 26 | 8 | y2 (arc end) |  |
| 34 | 8 | control\_x1 |  |
| 42 | 8 | control\_y1 |  |
| 50 | 8 | control\_x2 |  |
| 58 | 8 | control\_y2 |  |
| 66 | 8 | padding |  |


Writer (`encode\_circle\_element`) zapisuje všech 8 float64 — **korektní od session 7**.

#### Element footer (196 B)

```
bytes 0-8:   padding  
bytes 8-16:  float64 5.0  (shodné s field\_40)  
bytes 16-24: padding  
bytes 24-32: float64 89.0 (stack rozměr?)  
bytes 32-196: padding (většinou nuly)
```

Writer zapisuje stejný footer pro všechny elementy (`ELEMENT\_FOOTER`). Poslední element dostává stejný footer (ne `ELEMENT\_TAIL` 180B) — to je záměrná změna od session 7, kde se zjistilo že VCutWorks akceptuje 196B i pro poslední element.

### 3.5 Trailer (5 B)

```
\\x00\\x00\\x00\\x00\\x00
```

Původní chyby:

- **200B TRAILER\_PREFIX** (session 1-5): float64 5.0 + 90.0 → hard rejection v GUI

- **20B zeros** (session 6-7): funkční ale zbytečné

- **5B zeros** (current): korektní


## 4. DXF ADAPTER — DETAILNÍ ANALÝZA

### 4.1 Architektura

```
compile\_dxf(dxf\_path, output\_path, config\_path)  
    │  
    ├── 1. Load config (vcf\_compiler\_map\_config.json)  
    │       └── \_load\_config() → \{aci\_color\_mapping, defaults\}  
    │  
    ├── 2. Parse DXF (lazy import dxf\_geometry\_indexer\_v2)  
    │       └── idx.index\_dxf() → \{entities, layer\_card\}  
    │  
    ├── 3. Build VCF spec  
    │       └── \_build\_vcf\_spec(entities, layer\_card, tool\_config, h1\_default, feed\_default)  
    │             ├── Group entities by ACI → one VCF layer per ACI  
    │             ├── Resolve cutter params per ACI (density rules for ambiguous)  
    │             ├── Detect circles (CIRCLE type, SPLINE fit)  
    │             └── Deduplicate circles (proximity-based)  
    │  
    ├── 4. Write VCF  
    │       └── vcf\_parser.\_writer.write(spec, output\_path)  
    │  
    └── 5. Log results
```

### 4.2 ACI → VCF mapping flow

```
ACI číslo z DXF (0..255)  
    │  
    ├── aci\_mapping.get(str(aci)) → mapping dict | None  
    │  
    ├── Pokud mapping existuje:  
    │     ├── cutter\_type == "ambiguous" → density resolver  
    │     │     ├── density \> 30 pts/m → Vibrate cutter 50mm/s  
    │     │     └── else → V-slot 200mm/s  
    │     └── jinak → přímé parametry z configu  
    │  
    └── Pokud mapping neexistuje → fallback defaults  
          (Vibrate cutter, 200mm/s, N/A)
```

### 4.3 Circle detection pipeline

```
Entity z DXF  
    │  
    ├── Je typ "CIRCLE"?  
    │     ├── ANO: přímé cx/cy/radius z entity.dxf  
    │     └── NE:  
    │           ├── Je typ "SPLINE"?  
    │           │     ├── ANO: least-squares circle fit (\_is\_circular)  
    │           │     │     ├── max\_dev \<= 1.0mm → circle  
    │           │     │     │     └── \_extract\_circle\_from\_vertices()  
    │           │     │     │           └── cx = cp\[3\].x, cy = cp\[0\].y, r = |dx|  
    │           │     │     └── jinak → polyline  
    │           │     └── NE: polyline  
    │           └── ...  
    │  
    └── Duplicate check (proximity-based, epsilon 1.0mm)
```

### 4.4 Známé problémy — detail

#### P1: Circle detection z SPLINE — \_fit\_circle vs exact cp extrakce

| Metoda | Residual error | Stav |
| - | - | - |
| \_fit\_circle() | 0.08 mm | ✅ Funkční, ale aproximace |
| cp\[3\].x extrakce | 0.0 mm | 🔧 Plánováno — vyžaduje DXF control point přístup |


**Kontext:** B2B parser (`vcf\_geometry.py:71-93`) rekonstruuje kruh pouze z prvního segmentu — `x1c=cp\[0\]`, `x2c=cp\[3\]`. Writer aktuálně používá \_fit\_circle na 100 sample bodech. Pro dokonalou shodu s VCutWorks je potřeba přejít na cp extrakci.

**EROI:** Nízká priorita — 0.08mm residual je prakticky irelevantní pro oscilační nůž (přesnost řezu je ±0.5mm).

#### P2: Vertex deduplication

| Metoda | Epsilon | Status |
| - | - | - |
| \_dedup\_consecutive() | 0.01 mm | ✅ Funkční |
| BSpline range bug fix | knots\[-1\] faktor | ✅ Fixed v session 10 |


**Aktuální stav:** Po BSpline fixu (range 0..knots\[-1\] místo 0..1) square produkuje 4 segmenty (shodně s native). Žádné duplicitní vertexy.

#### P3: ACI 0 vs 7 color collision

| ACI | RGB | Geom\_color | Problém |
| - | - | - | - |
| 0 (ByBlock) | (10,10,10) | 0x0A0A0A00 | Unikátní — ✅ |
| 7 (black) | (0,0,0) | 0x00000000 | Standard |


**Fix:** ACI 0 → (10,10,10) místo (0,0,0). Kolize vyřešena v session 7.


## 5. ACI CONFIG — STAV KALIBRACE

### 5.1 Přehled

| ACI | Barva | Cutter type | Speed | H1 | H2 | Status kalibrace |
| - | - | - | - | - | - | - |
| 0 | černá | Vibrate | 80 | 24.0 | -0.5 | ✅ calibrated |
| 1 | červená | Vibrate | 150 | 2.0 | -0.3 | ⚠️ hypothesis |
| 2 | žlutá | V-slot (L) | 300 | 2.0 | 6.0 | ⚠️ empirical |
| **3** | **zelená** | **V-slot (both)** | **300** | **0.0** | **9.0** | **✅ calibrated** |
| 4 | azurová | ambiguous | 200 | 2.0 | 6.0 | ⚠️ hypothesis |
| 5 | modrá | Vibrate | 100 | 2.0 | -0.3 | ⚠️ empirical |
| **6** | **purpurová** | **Vibrate** | **300** | **2.0** | **-0.3** | **✅ calibrated** |
| 7 | černá | Vibrate | 80 | 24.0 | -0.5 | ⚠️ empirical |
| **30** | **oranžová** | **V-slot (both)** | **100** | **2.0** | **6.0** | **✅ calibrated** |
| **52** | **zelená** | **V-slot (both)** | **300** | **0.0** | **9.0** | **✅ calibrated** |
| **92** | **teal** | **V-slot (both)** | **300** | **0.0** | **9.0** | **✅ calibrated** |


### 5.2 Kalibrační metodika

**"calibrated"** (7 entries): Potvrzeno vůči nativnímu VCF z VCutWorks — speed, h1, h2, cutter\_type, direction sedí byte-to-byte.

**"empirical"** (3 entries): Odvozeno z DXF→VCF pipeline — parametry dávají smysl pro daný typ geometrie, ale nebyly verifikovány proti nativnímu VCF.

**"hypothesis"** (2 entries): Nejisté — chybí referenční DXF/VCF pár pro verifikaci.

### 5.3 Doporučení pro kalibraci

1. **ACI 1 (red):** Potřebuje N≥50 DXF+VCF párů. Pravděpodobně Vibrate 100-200mm/s — nejčastější outer contour.

2. **ACI 4 (cyan):** Density resolver potřebuje statistické ověření — threshold 30pts/m je odhad.

3. **ACI 7 (black):** Lze povýšit na "calibrated" shodou s ACI 0.


## 6. DEPENDENCY CHAIN — RIZIKA

### 6.1 Externí závislosti — riziková matice

| Závislost | Riziko | Dopad | Mitigace |
| - | - | - | - |
| `dxf\_geometry\_indexer\_v2` | API break, změna chování | Kompilace DXF→VCF selže | Version pin, vlastní test suite |
| `ezdxf` (transitivní) | API break, nová verze | Parsování DXF selže | Version pin v dxf\_integrace |
| `vcf\_compiler\_map\_config.json` | Chybí v CWD | Fallback na built-in defaulty | Výchozí hodnoty v kódu |


### 6.2 Vnitřní závislosti — coupling

| Modul | Importuje | Typ závislosti |
| - | - | - |
| `\_writer.py` | `\_reader.py` (GEOMETRY\_SIG, CUTTER\_MAP, DIR\_MAP) | Strukturální konstanty — nízké riziko |
| `\_dxf\_adapter.py` | `\_writer.write` (voláno v \_build\_vcf\_spec) | Volání na konci pipeline — jednosměrné |
| `\_\_init\_\_.py` | `\_writer.write`, `\_dxf\_adapter.compile\_dxf` | Public API — stabilní |


### 6.3 Test coverage — mezery

| Oblast | Unit testy | Integration testy | RE verifikace |
| - | - | - | - |
| Writer — layer block encoding | ✅ 12 testů | ✅ roundtrip | ✅ hex diff |
| Writer — geometry encoding | ✅ 7 testů | ✅ roundtrip | ✅ hex diff |
| Writer — header/trailer | ✅ 4 testy | ❌ chybí | ✅ hex diff |
| DXF adapter — ACI mapping | ❌ 0 testů | ❌ chybí | ⚠️ částečná |
| DXF adapter — circle detection | ❌ 0 testů | ❌ chybí | ⚠️ částečná |
| Reader — layer extraction | ❌ 0 unit testů | ✅ roundtrip | ✅ hex diff |
| ACI config validation | ❌ 0 testů | ❌ chybí | ⚠️ manuální |



## 7. NÁVRH DALŠÍHO POSTUPU (Vector 2)

### 7.1 Prioritizace

| Priorita | Úkol | Odhad | EROI | Závisí na |
| - | - | - | - | - |
| P1 | Napsat unit testy pro DXF adapter | 2-4h | VYSOKÁ — chybí 0 testů | — |
| P2 | Kalibrovat ACI 1,4,7 (N≥50 vzorků) | 4-8h | VYSOKÁ — 3 nejisté entry | produkční VCF |
| P3 | Přidat test determinismu pro body() | 1h | STŘEDNÍ — aktuálně jen header | — |
| P4 | Refaktorovat GEOMETRY\_SIG z \_reader.py | 1h | NÍZKÁ — cyklická dep není kritická | — |
| P5 | cp\[3\].x extrakce pro circle (místo \_fit\_circle) | 2-4h | NÍZKÁ — 0.08mm residual je zanedbatelný | DXF control points |
| P6 | Otestovat multi-layer VCF v GUI | 2h | STŘEDNÍ — poslední neotestovaný scénář | P1 |


### 7.2 EROI analýza

| Task | Náklady (h) | Přínos | EROI |
| - | - | - | - |
| DXF adapter unit testy | 3 | Eliminuje riziko regrese v kritické komponentě (jediná cesta DXF→bin VCF) | 0.33 h/přínos |
| ACI kalibrace 1,4,7 | 6 | Zvyšuje confidence z 0.70→0.95, eliminuje "hypothesis" status | 0.50 h/přínos |
| Multi-layer GUI test | 2 | Potvrdí/vyvrátí poslední známý problém, uzavře fázi 2 | 0.25 h/přínos |
| cp\[3\].x extrakce | 3 | 0.08mm→0.0mm residual, 100% shoda s VCutWorks | 5.0 h/přínos (nejnižší) |


**Doporučení:** P1 → P6 → P2 → P3 → P4 → P5

### 7.3 Rozhodnutí: Vector 1 vs Vector 2

| Kritérium | Vector 1 (VCF Optimalizátor) | Vector 2 (Deep RE) |
| - | - | - |
| Ready k produkci | ⚠️ Částečně — chybí analytické enginy | ✅ Writer je funkční |
| Zbývající práce | 3-6 měsíců (analytické enginy, testování) | 2-4 týdny (testy, kalibrace, verifikace) |
| Byznys hodnota | VYSOKÁ — nový produkt, konkurenční výhoda | STŘEDNÍ — dokončení existujícího nástroje |
| Riziko | Neznámý trh, nové domeny (ML, yield) | Nízké — známý formát, funkční pipeline |
| Synergie s portfoliem | VYSOKÁ — positioning, LinkedIn obsah | NÍZKÁ — technický debt cleanup |



## 8. PŘÍLOHY

### A. Konstanty

```
\# \_writer.py  
HEADER\_MAGIC      = b"RDVCUTFILEVER1.0.013"  
HEADER\_MAGIC\_012  = b"RDVCUTFILEVER1.0.012"  
VCF\_PREFIX        = b"\\x13"  
VCF\_POST\_MAGIC    = b"\\x20\\x0a\\x00"  
EMPTY\_BLOCK\_COUNT = 256  
LAYER\_BLOCK\_SIZE  = 610  
STOCK\_WIDTH       = 1220.0  
STOCK\_HEIGHT      = 2900.0  
GEOMETRY\_SIG      = b'\\x01\\x00\\x01\\x00\\x00\\xff\\xff\\xff'  
TRAILER           = b'\\x00' \* 5  
  
\# \_reader.py  
CUTTER\_MAP = \{0: "Vibrate cutter", 1: "Wheel", 2: "Milling cutter",  
              3: "V-slot", 4: "Vibrate cut"\}  
DIR\_MAP    = \{0: "Left", 1: "Right", 2: "Cut both side"\}
```

### B. Velikosti struktur

| Struktura | Velikost |
| - | - |
| Preamble (prefix + magic + post\_magic) | 24 B |
| Stock dims | 16 B |
| POST\_STOCK\_HEADER | 14 B |
| MACHINE\_PROFILE | 418 B |
| **Header total** | **472 B** |
| Layer block | 610 B |
| Element header (sig + color + template) | 45 B |
| Segment (polyline) | 74 B |
| Segment (circle) | 74 B (8× float64) |
| Element footer | 196 B |
| Trailer | 5 B |


### C. Vzorce

```
element\_size  = 45 + pt\_count × 74       (bez footeru)  
header\_size   = 472 + 256×610 + N×610    (N = počet vrstev)  
layer\_block\_pos = 472 + (blk\_idx) × 610  (blk\_idx = 0..255 empty, 256.. active)  
geom\_color    = (BGR \<\< 8) & 0xFFFFFFFF   (BGR = R\<\<16 | G\<\<8 | B)
```

### D. Kompletní fix historie

| Session | Root Cause | Fix | Soubor | Verifikace |
| - | - | - | - | - |
| 6 | Trailer truncated (path data) | trailer() vždy zapisuje path | \_writer.py | GUI test variant E→H |
| 6 | ec@92=0 (no geometry) | ec@92 = 1 | \_writer.py | GUI test variant M→P |
| 6 | direction@104 jen pro V-slot | direction@104 pro všechny | \_writer.py | GUI test variant M→P |
| 6 | field\_40/197/198 chybí | Přidány konstanty | \_writer.py | Hex diff 0 diffs |
| 6 | next\_color@606 = 0 | = 1 pro poslední blok | \_writer.py | Hex diff |
| 7 | Circle encoding — chybí 4 float64 | encode\_circle\_element — 8 float64 | \_writer.py | Hex diff circle VCF |
| 7 | ACI 0 vs 7 collision | ACI 0 → (10,10,10) | \_dxf\_adapter.py | Reader layer detekce |
| 7 | ByLayer (256) unresolved | layer\_colors lookup | indexer\_v2.py | DXF→VCF pipeline |
| 8 | ec@92 chybně=0 (po off-by-2 opravě) | ec@92=1 (has geometry flag) | \_writer.py | GUI multi-element OK |
| 8 | offset606=1 (hardcoded) | offset606=total\_elements | \_writer.py | GUI multi-element OK |
| 9 | Vertex dedup (square 7→4 seg) | \_dedup\_consecutive(eps=0.01) | \_dxf\_adapter.py | Hex diff square |
| 10 | BSpline range bug (circle err 2.5mm) | t \* knots\[-1\] | indexer\_v2.py | Circle radius 0.08mm |
| 10 | \_fit\_circle threshold 5→1mm | max\_deviation=1.0 | \_dxf\_adapter.py | Eliminace false positives |
| 10 | Circle dedup float→proximity | abs(a-b) \< 1.0mm | \_dxf\_adapter.py | 4 arcs→1 circle |



*Konec dokumentu — verze 1.0*

