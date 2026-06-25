---
title: "Deterministic CNC Format Intelligence — Methodology & Validation Framework"
author: Ondřej Soušek
version: 1.0
date: 2026-06
classification: CONFIDENTIAL — B2B partners & auditors
repository: outpost2026/Kazuistiky-LLM-sprint
---

# Deterministic CNC Format Intelligence

## Methodology & Validation Framework

**Autor:** Ondřej Soušek — SYSTEQ  
**Verze:** 1.0  
**Datum:** červen 2026  
**Klasifikace:** CONFIDENTIAL — pro B2B partnery a auditory  



## Obsah

1. [Problém a kontext](#1-problém-a-kontext)

2. [Metodika reverse inženýrství](#2-metodika-reverse-inženýrství)

3. [Epistemický rámec](#3-epistemický-rámec)

4. [Architektura systému](#4-architektura-systému)

5. [Validace a důkazní body](#5-validace-a-důkazní-body)

6. [Detekční taxonomie](#6-detekční-taxonomie)

7. [Transferovatelná metodika](#7-transferovatelná-metodika)


## 1. Problém a kontext

### 1.1 Proprietární formáty jako bariéra

Průmyslové CNC stroje často komunikují v proprietárních binárních formátech, jejichž dokumentace neexistuje veřejně. To vytváří:

- **Vendor lock-in:** Operátor je vázán na jeden software (VcutWorks, LightBurn, RDWorks) bez možnosti exportu do jiných systémů

- **Ztráta datové prostupnosti:** Výrobní parametry (rychlost, nástroj, sekvence) jsou uzavřeny v binární struktuře

- **Nemožnost validace:** B2B partner nemůže ověřit, zda tvrzení dodavatele softwaru odpovídají skutečnosti

- **Absence auditní stopy:** Problémové řezy nelze systematicky analyzovat zpětně

### 1.2 Mezera na trhu

Pro formát `.VCF` používaný řadiči Ruida (VCutWorks, RDWorks) **neexistuje žádný veřejně dostupný parser**. Existující nástroje:

| Nástroj | Formát | Parser VCF | Detekce defektů | ERP integrace |
| - | - | - | - | - |
| VcutWorks (Ruida) | VCF nativní | Ano (uzavřený) | Ne | Ne |
| LightBurn | DXF/LBRN | Ne | Ne | Ne |
| VCarve | DXF/PLT | Ne | Základní | Ne |
| **Vcut-Parser** | **VCF** | **Ano (otevřený)** | **20 typů** | **Odoo CSV** |


### 1.3 Cílový trh

- **Český trh:** 50–150 firem s CNC plotry Ruida (oscilating knife, wheel, milling)

- **EU trh:** 500–1000 firem

- **TAM (Total Addressable Market):** 10–20M CZK ročně

- **Bariera vstupu:** ~200 hodin reverse inženýrství + hluboká doménová znalost CNC

### 1.4 Motivace

Tento dokument popisuje metodiku, která umožňuje:

1. **Systematicky dekódovat** proprietární binární formát

2. **Validovat přesnost** vůči etalonu (LightBurn)

3. **Dokumentovat epistemickou jistotu** každého parametru

4. **Prokázat determinismus** výstupu (stejný vstup = stejný výstup)

5. **Transferovat metodiku** na další formáty


## 2. Metodika reverse inženýrství

### 2.1 Šestifázový proces

Reverse engineering proprietárního formátu není náhodný proces. Používáme strukturovanou 6-fázovou metodiku:

```
Fáze 0: Tacit Knowledge Acquisition  
    ↓  
Fáze 1: Synthetic Ground Truth  
    ↓  
Fáze 2: Differential Analysis  
    ↓  
Fáze 3: Physical Validation  
    ↓  
Fáze 4: Ground Truth Export  
    ↓  
Fáze 5: Regression Testing
```

#### Fáze 0: Tacit Knowledge Acquisition

**Cíl:** Nasbírat implicitní znalosti od zkušeného operátora/strojvedoucího.

- **Metoda:** Stínování hlavního technologa (9 dní v provozu)

- **Výstup:** Ruční zápisky, deníky z provozu, kalibrace nuly, oscilační frekvence, barevná nomenklatura vrstev

- **Klíčový insight:** Operátor ví, že "červená = řez kolmým nožem skrze celou desku" a "modrá = dekorativní řez tangenciálním nožem" — tato znalost není nikde formálně zdokumentována

**Přínos:** Bez této fáze by parser extrahoval čísla bez sémantiky. Binární data říkají "rychlost = 200 mm/s", ale tacit knowledge říká "rychlost 200 mm/s na 12mm PET feltu = optimální řez plynulých křivek bez rizik degradace kvality řezu".

#### Fáze 1: Synthetic Ground Truth

**Cíl:** Vytvořit testovací soubory s known geometry.

- **Metoda:** Vytvoření jednoduchých tvarů (obdélník, kruh, diamant) v trial verzi VcutWorks

- **Kontrola:** Známé rozměry (100×100 mm čtverec) → ověření, zda parser extrahuje správné souřadnice

- **Výstup:** Testovací VCF soubory s přesně definovanou geometrií

**Princip:** Pokud vím, že soubor obsahuje čtverec 100×100 mm, a parser vrátí 100.00 × 100.01 mm, odchylka je 0.01 mm — akceptovatelná. Pokud vrátí 500 × 500 mm, parser je chybný.

#### Fáze 2: Differential Analysis

**Cíl:** Identifikovat strukturu binárního formátu porovnáním dvou téměř identických souborů.

- **Metoda:** Párový hex diff — dva soubory lišící se v jednom parametru (např. barva vrstvy, rychlost)

- **Princip:** `hex\_diff(soubor\_A, soubor\_B)` → odlišné bajty = hledaný parametr

- **Iterace:** Opakujeme pro každý parametr (barva, rychlost, nástroj, směr, výška)

**Ukázka:**

| Pár souborů | Změněný parametr | Odlišné bajty | Identifikace |
| - | - | - | - |
| rectangle\_01 vs rectangle\_02 | Barva vrstvy | Offset +8 v bloku vrstvy | `color\_val` (uint32) |
| rectangle\_01 vs rectangle\_03 | Rychlost řezu | Offset +4 v bloku vrstvy | `speed\_mms` (float64) |
| circle\_01 vs circle\_02 | Počet bodů | Offset +4 v geometrii | `pt\_count` (uint32) |


#### Fáze 3: Physical Validation

**Cíl:** Ověřit, že parserovaná data odpovídají skutečnému chování stroje.

- **Metoda:** Porovnání predikovaného času řezu s reálným časem na stroji

- **Kritérium:** Odchylka ≤ 10% je akceptovatelná pro B2B použití

- **Výstup:** Kalibrovaný kinematický model s měřitelnými konstantami

**Kalibrační protokol:**

| Parametr | Metoda měření | Jednotka |
| - | - | - |
| Max rychlost | Pohyb hlavy 1000 mm na max, stopky | mm/s |
| Rohová penalizace | 10× L-cut (100 mm ramena), celkový čas / 10 | s/roh |
| Lift time | Čas zvednutí hlavy mezi elementy | s |
| Materiálový damping | Násobič rychlosti pro různé materiály | - |


#### Fáze 4: Ground Truth Export

**Cíl:** Vytvořit neměnné baseline srovnání pro regresní testy.

- **Metoda:** Parser zpracuje VCF → uloží kompletní JSON výstup jako "golden master"

- **Formát:** Strukturovaný JSON se 40+ poli (geometrie, vrstvy, varování, predikce času, ML feature vektory)

- **Počet:** 7 golden master baselinů pro různé typy souborů

**Co golden master dokazuje:**

1. **Determinismus:** Stejný vstup → identický výstup (prokázáno testem `test\_determinism.py`)

2. **Regresní ochrana:** Jakákoliv změna kódu = odchylka od golden masteru = selhání testu

3. **Reprodukibilitat:** Kdokoliv se stejným kódem dostane stejný výstup

#### Fáze 5: Regression Testing

**Cíl:** Automaticky ověřovat, že změny kódu nezhoršují přesnost.

- **Metoda:** pytest srovnávající aktuální výstup s golden master JSONy

- **Kritérium:** Exaktní shoda (kromě volatile fields: file\_hash, filename)

- **Výsledek:** 8/8 PASS (smoke + determinism + golden master + geometry + config + binary reader + KB overrides + time predictor)

### 2.2 Pair Diff Metoda — Detail

Klíčová technologie pro reverse engineering binárních formátů:

```
1. Vytvořit soubor A s parametrem X = hodnota\_1  
2. Vytvořit soubor B s parametrem X = hodnota\_2 (vše ostatní identické)  
3. hex\_diff(A, B) → seznam odlišných offsetů  
4. Identifikovat: offset = místo, kde je parametr X uložen  
5. Opakovat pro každý parametr
```

**Výhoda:** Tato metoda funguje bez znalosti formátu. Nepotřebuji vědět, že formát je little-endian — hex diff ukáže přesný bajt, který se mění.

**Omezení:** Vyžaduje možnost vytvářet testovací soubory (trial verze softwaru). Pokud software neumožňuje experimenty, je nutné použít analýzu existujících souborů.

### 2.3 Clean Room Testing

Syntetické VCF soubory s known geometry:

| Soubor | Geometrie | Účel |
| - | - | - |
| rectangle\_01.vcf | Obdélník 100×100 mm | Validace základních souřadnic |
| circle\_01.vcf | Kruh r=50 mm | Validace kruhové geometrie |
| diamond\_01.vcf | Diamant (rotovaný čtverec) | Validace uhlových souřadnic |


### 2.4 Transfer Learning

Zkušenosti z CNC watercutingu přeneseny na oscillating knife:

- **Watercut:** Voda řeže bez kontaktu → jiná kinematika

- **Oscillating knife:** Mechanický kontakt → rohová penalizace, lift time, materiálový damping

- **Princip:** Základní parsing (binární → geometrie) je identický; kinematický model se kalibruje nově


## 3. Epistemický rámec

### 3.1 Proč epistemická kontrola?

V průmyslové automatizaci nestačí vědět, že "parser funguje". Je nutné vědět:

- **Jak jistě víme**, že funguje? (conf: 0.99 nebo 0.70?)

- **Na základě čeho** to víme? (empirické měření nebo odhad?)

- **Co by mohlo být špatně?** (známé limity, edge cases)

### 3.2 Čtyřúrovňová klasifikace pravidel

Každé pravidlo v Knowledge Base nese epistemický metadata:

| Třída | Popis | Confidence | Příklad |
| - | - | - | - |
| **CLASS\_A** | Fyzikální zákon | 0.99 | "Vibrace cutter musí být poslední vrstva" (fyzika: jinak posun dílů) |
| **CLASS\_B** | Empirické ověření | 0.90–0.95 | "H2 = 0.0 mm pro 12mm PET felt" (měřeno na stroji) |
| **CLASS\_C** | Heuristika | 0.80–0.90 | "Malá plocha \< 1.67 m² potřebuje pásku" (zkušenost) |
| **CLASS\_D** | Hypotéza | 0.70–0.85 | "Micro-segmenty \< 1 mm = potenciální defekt" (neověřeno) |


### 3.3 Validation Status

Každé pravidlo má jeden ze stavů:

- **accepted** — ověřeno empiricky i teoreticky

- **conditional** — platí za předpokladů (specifikovaných v kontextu)

- **rejected** — vyvráceno, ale ponecháno pro historickou referenci

- **unknown** — dosud neověřeno

### 3.4 SNR Princip (Signal-to-Noise Ratio)

**Jádrová axioma:** Hlavní hodnota není počet nalezených chyb, ale **jistota, že nalezená chyba = skutečný fyzikální defekt.**

Důsledky:

1. **Nulový vizuální stav = čistý výkres.** Výchozí stav je klid.

2. **INFO se nikdy nezobrazuje na obrazovce.** (Prevence alarm overload — Three Mile Island 1979)

3. **Max 3 typy varování na objekt.** (Miller's Law: 7±2 chunks)

4. **Podmíněné potlačení:** Pokud 5+ micro-segmentů tvoří křivku, degradeWARNING → INFO (density filter)

### 3.5 Epistemic Confidence Index

Automaticky vypočítaný podíl empiricky ověřených konstant:

```
ECI = (počet empirických konstant) / (celkový počet konstant)
```

Pokud ECI \< 0.5, systém je stále ve fázi vývoje. Pokud ECI \> 0.8, systém je produkčně spolehlivý.


##   
4. Architektura systému

### 4.1 Pipeline

```
┌─────────────────────────────────────────────────────────────────┐  
│                    VCF BINARY INPUT                              │  
│                    (proprietární binární formát)                 │  
└──────────────────────────────┬──────────────────────────────────┘  
                               │  
                               ▼  
┌─────────────────────────────────────────────────────────────────┐  
│  LAYER EXTRACTION                                               │  
│  • Detekce magické signatury                                     │  
│  • Verze formátu (block\_size)                                    │  
│  • Zpětné prohledávání od první geometrie                        │  
│  • Validace: rychlost 1–2000 mm/s, %5 == 0, barva match         │  
└──────────────────────────────┬──────────────────────────────────┘  
                               │  
                               ▼  
┌─────────────────────────────────────────────────────────────────┐  
│  GEOMETRY PARSING                                                │  
│  • Scan GEOMETRY\_SIG occurrences                                 │  
│  • Type dispatch: Circle / Polygon / Polyline / Line             │  
│  • 74B segment records: IEEE 754 double coordinates             │  
│  • Arc/spline reconstruction (3-point circle, Catmull-Rom)      │  
│  • Layer mapping: color-to-layer bit shift                       │  
└──────────────────────────────┬──────────────────────────────────┘  
                               │  
                               ▼  
┌─────────────────────────────────────────────────────────────────┐  
│  POST-PROCESSING                                                 │  
│  • Cut order assignment                                          │  
│  • Canvas bbox computation                                       │  
│  • Coordinate normalization \[0,1\]                                │  
│  • Material thickness detection (H2 values / filename regex)    │  
│  • Operation type classification (through-cut / kiss-cut / V-groove) │  
│  • Complexity computation (curvature index, sharp corners)      │  
│  • Aggregated job detection (BFS clustering)                    │  
│  • Spatial analysis (grouping, panel format, symmetry, density) │  
│  • Topology tree (parent-child bbox containment)                │  
│  • ML feature extraction (50+ numerických features)             │  
└──────────────────────────────┬──────────────────────────────────┘  
                               │  
                               ▼  
┌─────────────────────────────────────────────────────────────────┐  
│  KNOWLEDGE BASE VALIDATION                                       │  
│  • H2 rules (tool height vs material thickness)                 │  
│  • Sequence rules (outer cut must be last)                      │  
│  • Fixation rules (small panel → tape requirement)              │  
│  • Geometry rules (open paths, micro-segments, orphans)         │  
│  • Risk score computation (3× CRITICAL + 1× WARNING)           │  
│  • Override system (per-customer threshold tuning)              │  
└──────────────────────────────┬──────────────────────────────────┘  
                               │  
                               ▼  
┌─────────────────────────────────────────────────────────────────┐  
│  TIME PREDICTION                                                │  
│  • cut\_time = Σ(path\_length / speed) per active layer           │  
│  • lift\_time = N\_elements × t\_lift                              │  
│  • corner\_time = Σ(N\_points × t\_corner) per element             │  
│  • curve\_penalty = N\_points × t\_curve (if avg\_seg \< threshold) │  
│  • traverse\_time = (N\_active - 1) × dist / speed               │  
│  • setup\_overhead + return\_home\_time                            │  
│  • Material-specific speed multipliers                          │  
└──────────────────────────────┬──────────────────────────────────┘  
                               │  
                               ▼  
┌─────────────────────────────────────────────────────────────────┐  
│  OUTPUT (parsed\_data)                                            │  
│  • elements\[\] — geometrie, vertices, bbox, centroid, cut\_order │  
│  • layers\[\] — cutter, speed, H1/H2, cut\_length, extensions    │  
│  • manufacturing\_intelligence — warnings, risk\_score            │  
│  • operation\_sequence — layer & element ordering                │  
│  • erp\_time\_prediction — predicted\_time, path\_length            │  
│  • topology\_tree, proximity\_matrix, ml\_features                │  
│  • canvas\_bbox, complexity\_index, detected\_panel\_format         │  
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Knowledge Base Engine

Dvouvrstvý validační systém:

**Vrstva 1: Deterministická pravidla** (bez ML)

- Fyzikální omezení (min radius, max element size)

- Vakuový přítlak (plocha → riziko posunu)

- V-groove geometrie (standards)

- Sekvence řezu (inner → outer)

**Vrstva 2: ML pravidla** (interpretovatelné modely)

- Decision tree (max\_depth=3) — předvídání nástroje z geometrie

- Case-based reasoning — cosine similarity s historickými daty

- Inverse conditional analysis — frekvenční křížová validace

**Klíčový princip:** ML nikdy nepřekračuje fyzikální baseline. Pokud ML navrhuje fyzikálně nemožný parametr, systém ho zamítne.

### 4.3 Machine Calibration Model

Kalibrační protokol s epistickým sledováním:

```
\{  
  "kinematic\_speed\_ceiling": \{  
    "max\_speed\_mms": 800.0,  
    "validation\_status": "empirical"  
  \},  
  "corner\_brake": \{  
    "measured\_time\_per\_corner\_seconds": 0.66,  
    "validation\_status": "empirical"  
  \},  
  "material\_damping": \{  
    "pet\_felt\_12mm": \{ "speed\_multiplier": 1.0, "validation\_status": "empirical" \},  
    "pet\_felt\_24mm": \{ "speed\_multiplier": 0.85, "validation\_status": "hypothesis" \},  
    "plywood\_6mm":   \{ "speed\_multiplier": 0.70, "validation\_status": "hypothesis" \}  
  \}  
\}
```

**Poznámka:** Pouze `pet\_felt\_12mm` je empiricky ověřen. Ostatní materiály jsou hypotézy vyžadující kalibraci.

### 4.4 Override Systém

Umožňuje per-customer tuning bez změny kódu:

- **Per-rule enable/disable:** Vypnout pravidlo, které generuje false positives pro konkrétního zákazníka

- **Threshold overrides:** Změnit prahovou hodnotu (např. `max\_unmerged\_length\_mm: 200 → 80`)

- **Density filter:** Potlačit micro-segment varování na organických křivkách

- **Session overrides:** Dočasné nastavení z UI (Streamlit sidebar)


## 5. Validace a důkazní body

### 5.1 Testovací infrastruktura

| Test | Soubor | Co ověřuje | Kritérium |
| - | - | - | - |
| `test\_smoke.py` | 5 VCF souborů | Parser nedepadá na žádném vstupu | `elements \> 0` |
| `test\_determinism.py` | Všechny demo soubory | Stejný vstup = identický výstup | `dictdiff == \{\}` |
| `test\_golden\_master.py` | 7 baselinů | Regresní ochrana | Exaktní JSON shoda |
| `test\_geometry.py` | Unit tests | Geometrické utilty | bbox, containment, symmetry |
| `test\_config.py` | Unit tests | Konfigurace | pricing, formats, kinematic |
| `test\_binary\_reader.py` | Unit tests | Binární reader | COLOR\_MAP, CUTTER\_MAP |
| `test\_kb\_overrides.py` | Unit tests | Override systém | Density filter, edge detection |
| `test\_time\_predictor.py` | Unit tests | Predikce času | format\_time, predict\_cut\_time |


### 5.2 Výsledky

```
tests/test\_smoke.py::test\_parse\_1ks PASSED  
tests/test\_smoke.py::test\_parse\_ofset\_3x PASSED  
tests/test\_smoke.py::test\_parse\_fluenz\_l PASSED  
tests/test\_smoke.py::test\_parse\_knight PASSED  
tests/test\_smoke.py::test\_parse\_logo\_afdc PASSED  
tests/test\_determinism.py::test\_determinism\_single PASSED  
tests/test\_determinism.py::test\_determinism\_all PASSED  
tests/test\_golden\_master.py::test\_golden\_master\[1ks\] PASSED  
tests/test\_golden\_master.py::test\_golden\_master\[25\_circles\_only\] PASSED  
tests/test\_golden\_master.py::test\_golden\_master\[arbyd\_simple\] PASSED  
tests/test\_golden\_master.py::test\_golden\_master\[fluenz\_l\] PASSED  
tests/test\_golden\_master.py::test\_golden\_master\[logo\_AfdC\] PASSED  
tests/test\_golden\_master.py::test\_golden\_master\[Ofset\_3x\] PASSED  
tests/test\_golden\_master.py::test\_golden\_master\[vyrobni\_data\_pernerka...\] PASSED  
... (8/8 testovacích kategorií PASS)
```

### 5.3 Přesnost geometrie

| Metrika | Hodnota | Metoda |
| - | - | - |
| Přesnost geometrie | **99.99%** | Validace vůči LightBurn |
| Odchylka na element | **\< 0.02%** | Porovnání délek drah |
| Odchylka celkem | **\< 0.008%** | Agregace přes všechny elementy |
| Predikce času | **± 2–10%** | Porovnání s reálným časem na stroji |


### 5.4 Golden Master Princip

```
         ┌─────────────────┐  
         │   VCF soubor    │  
         └────────┬────────┘  
                  │  
                  ▼  
         ┌─────────────────┐  
         │     Parser      │  
         └────────┬────────┘  
                  │  
                  ▼  
         ┌─────────────────┐  
         │  JSON výstup    │ ← golden\_master/baseline.json  
         └────────┬────────┘  
                  │  
                  ▼  
         ┌─────────────────┐  
         │  pytest diff    │ ← jakákoliv odchylka = FAIL  
         └─────────────────┘
```

**Co je chráněno:**

- Přesnost geometrie (vertices, bbox, centroid)

- Správnost vrstev (cutter type, speed, H1/H2)

- Seřazení řezu (cut order, sequence validation)

- Predikce času (predicted\_time\_seconds)

- Varování (semantic\_warnings, risk\_score)

**Co je volatile (záměrně):**

- `file\_hash` — závisí na timestamp

- `filename` — závisí na vstupu

- `erp\_time\_prediction.predicted\_time\_formatted` — string reprezentace

### 5.5 Co tyto důkazy PROKAZUJÍ

1. **Determinismus:** 100% reprodukovatelnost výstupu

2. **Přesnost:** 99.99% geometrie, ±2–5% čas

3. **Regresní ochrana:** Změna kódu = automatické selhání testu

4. **Systémová integrita:** Všechny komponenty otestovány izolovaně i integrovaně

5. **Produkční spolehlivost:** 23 demo souborů bez selhání


## 6. Detekční taxonomie

### 6.1 Třídy defektů

Systém detekuje **20 typů defektů** organizovaných do 3 tříd:

#### Třída A: Grafické / Designérské chyby

Detekované před nasazením na stroj. Zachrání zakázku před ztrátou.

| \# | Kód | Popis | Severity |
| - | - | - | - |
| 1 | EDGE\_MERGE\_MISSING | Chybějící napojení hran (otevřený segment u zavřeného tvaru) | WARNING |
| 2 | UNCLOSED\_LOOP | Neuzavřená smyčka (gap mezi prvním a posledním bodem) | INFO–CRITICAL |
| 3 | MICRO\_SEGMENT | Micro-segmenty \< 1 mm (potenciální artefakty exportu) | WARNING |
| 4 | ZERO\_LENGTH\_SEGMENT | Segment s délkou = 0 (degenerace) | WARNING |
| 5 | SELF\_INTERSECTION | Křížení prvku se sebou samým | CRITICAL |
| 6 | DUPLICATE\_ELEMENT | Duplicitní element na stejných souřadnicích | WARNING |
| 7 | SPIKE\_DETECT | Náhlá změna směru \> 90° (potenciální chyba návrhu) | WARNING |
| 8 | ELEMENT\_OVERLAP | Překryv dvou elementů (riziko dvojitého řezu) | WARNING |
| 9 | DEGENERATE\_SHAPE | Degenerovaný tvar (body v jedné přímce) | WARNING |


#### Třída B: Technologické / CNC chyby

Detekované před nasazením na stroj. Předcházení fyzickým defektům.

| \# | Kód | Popis | Severity |
| - | - | - | - |
| 10 | SEQUENCE\_LAYER\_ERROR | Špatné pořadí vrstev (řez před dekorací) | CRITICAL |
| 11 | SEQUENCE\_NESTING\_ERROR | Špatné pořadí elementů (vnější před vnitřním) | CRITICAL |
| 12 | VACUUM\_FIXATION\_RISK | Malá plocha → nedostatečný vakuový přítlak | WARNING |
| 13 | H2\_SUBOPTIMAL | Suboptimální výška nástroje H2 | WARNING |
| 14 | NESTING\_CLEARANCE | Nedostatečná vůle mezi elementy | WARNING |
| 15 | TAB\_OVERLAP | Překryv upínacích tabů | WARNING |
| 16 | LAYER\_INCONSISTENCY | Nekonzistentní parametry vrstev | WARNING |
| 17 | ORPHAN\_ELEMENT | Sirotčí element bez přiřazení k grupě | INFO |
| 18 | ASYMMETRIC\_PAIR | Nesymetrický pár (u symetrických návrhů) | INFO |
| 19 | NEAR\_MISS\_GAP | Téměř uzavřená mezera (gap \< 0.1 mm) | INFO |


#### Třída C: NC code / Post-process chyby

Detekované při analýze výstupního souboru.

| \# | Kód | Popis | Severity |
| - | - | - | - |
| 20 | COLOR\_MAP\_MISMATCH | Barva neodpovídá žádné známé vrstvě | WARNING |
| 21 | AGGREGATED\_JOB | Agregovaná zakázka (více panelů v jednom souboru) | INFO |
| 22 | UNKNOWN\_VERSION | Neznámá verze formátu | WARNING |
| 23 | CORRUPT\_GEOMETRY | Poškozená geometrie (nevalidní souřadnice) | CRITICAL |


### 6.2 Severity Matrix

|  | Frekvence: Nízká | Frekvence: Střední | Frekvence: Vysoká |
| - | - | - | - |
| **Dopad: CRITICAL** | SEQUENCE\_LAYER\_ERROR | SELF\_INTERSECTION | — |
| **Dopad: WARNING** | TAB\_OVERLAP | VACUUM\_FIXATION\_RISK | MICRO\_SEGMENT |
| **Dopad: INFO** | ORPHAN\_ELEMENT | ASYMMETRIC\_PAIR | — |


### 6.3 Vizualní Overlay Metodika

Inspirováno leteckými HUD (Head-Up Display):

1. **Základní princip:** Overlay se zobrazuje POUZE pokud existují varování. Žádná varování = čistý výkres.

2. **Max 3 typy varování:** Miller's Law — více než 3 typy = alarm overload

3. **Pouze 2 úrovně:** CRITICAL (\#F43F5E) a WARNING (\#F59E0B). INFO se nikdy nezobrazí.

4. **Výkon:** LineCollection batching pro soubory s 755+ elementy

### 6.4 Kvantifikace ROI

| Parametr | Hodnota |
| - | - |
| Cena jednoho defektu | 500–5 000 CZK |
| Podíl detekovatelných defektů | ~50% |
| Úspora na zakázku | 30–200 CZK |
| Roční úspora (malá dílna) | 30 000–200 000 CZK |
| Cena parseru (one-time) | 60–80K CZK |
| Cena roční údržby | 15–20K CZK |


**Návratnost investice:** 1–3 zachráněné zakázky = zaplacení parseru.


## 7. Transferovatelná metodika

### 7.1 Mikolových 5 principů

Metodika je inspirována principy Tomáše Mikolova (compression, simplicity, interpretability):

#### Princip 1: Komprese jako extrakce struktury

Místo uchovávání surových dat definujeme **deskriptorové vektory** (5–20 numerických features):

- `mean\_radius\_mm` — průměr kruhů

- `fraction\_circles` — podíl kruhů vůči celku

- `median\_area\_mm2` — mediánová plocha

- `convex\_hull\_density` — hustota konvexního obalu

Tento přístup umožňuje:

- Porovnávání souborů pomocí cosine similarity

- Klasifikaci pomocí decision tree (max\_depth=3)

- Transfer na jiné formáty (stačí nový deskriptor)

#### Princip 2: Jednoduché a interpretovatelné modely

```
Decision Tree (max\_depth=3)    ≈ 94% přesnost  
Deep Neural Network (100+ params) ≈ 95% přesnost
```

**Rozhodnutí:** Používáme decision tree, protože:

- Je interpretovatelný (člověk pochopí pravidlo)

- Je rychlý (ms vs. sekundy)

- Nevyžaduje velký trénovací dataset

- Lze ho validovat analyticky

#### Princip 3: Základní principy před statistikou

```
1. Uplatnit všechna fyzikální/geometrická omezení (deterministická pravidla)  
2. Teprve poté přidat ML tam, kde deterministická nestačí  
3. ML NIKDY nepřekračuje fyzikální baseline
```

#### Princip 4: Novelty Search — Kontinuální učení

```
Novelty Buffer (10 odchylek)  
    ↓  
Trigger: buffer plný  
    ↓  
Auto-retraining modelu  
    ↓  
Validace na golden masteru  
    ↓  
Deploy (pokud PASS) nebo rollback (pokud FAIL)
```

#### Princip 5: Emergence z jednoduchých pravidel

Složité chování systému vzniká kombinací atomických pravidel:

- 4 kategorie pravidel × N pravidel v každé → komplexní diagnostika

- Žádné "super-inteligentní" pravidlo — jen kombinace jednoduchých

### 7.2 Přenositelné artefakty

| Artefakt | Popis | Čas na implementaci |
| - | - | - |
| Descriptor generator | Generuje numerické vektory z geometrie | 2–5 dní |
| Decision tree trainer | Natrénuje klasifikátor na datech | 1 den |
| Case-based reasoning engine | Najde podobné historické případy | 0.5 dne |
| Novelty buffer | Sleduje odchylky a triggeruje retraining | 1 den |


### 7.3 EROI Framework (Energy Return on Investment)

Prioritizace refaktoringu podle návratnosti energie:

| Iterace | EROI | Úsilí | Popis |
| - | - | - | - |
| 0 (Hygiene) | High | 2–3 h | Logging, odstranění `except: pass` |
| 1 (Testing) | Critical | 4–6 h | Golden master testy, determinism |
| 2 (Dedup) | High | 8–12 h | Odstranění duplicitního kódu |
| 3 (Modules) | Medium | 12–16 h | Oddělení parseru, geometrie, predikce |
| 4 (Production) | Medium | 4–6 h | Docker, GCP, monitoring |
| 5 (CI/CD) | Low | 6–8 h | Automatické testy při commitu |


### 7.4 Blameless Post-Mortem

Selhání není hrozba identitě — je to datový bod vyžadující aktualizaci modelu.

**Framework:**

1. Co se stalo? (fakta, bez obviňování)

2. Proč se to stalo? (root cause, ne symptomy)

3. Jak se tomu předejde? (systémová změna, ne lidská)

4. Co jsme se naučili? (aktualizace epistemického rámce)

###   
  
  
7.5 LLM Interakční Protokol

LLM je autonomní mikroservis pro transformaci kódu, ne konverzační partner.

**Hranice:**

- LLM píše: Python logiku pro config loading, Streamlit UI

- LLM Nepíše: "chytřejší statistiky" pro detekci (okamžitě zamítnout)

- LLM Nepíše: Změny v epistemickém rámci (doménová expertíza člověka)

**Princip:** LLM je nástroj, ne architekt. Architekt rozhoduje, které anomálie jsou akceptovatelné (např. segmenty \< 0.5 mm v písmech) a které ničí panely.


## Závěr

Tento dokument popisuje metodiku, která umožňuje:

1. **Systematicky dekódovat** proprietární binární formát pomocí strukturovaného 6-fázového procesu

2. **Validovat přesnost** pomocí golden master testů a fyzikální kalibrace

3. **Dokumentovat epistemickou jistotu** každého parametru (CLASS\_A–D)

4. **Prokázat determinismus** výstupu (8/8 testů PASS, 99.99% přesnost)

5. **Transferovat metodiku** na další formáty (DXF, PLT, LBRN)

**Klíčový princip:** Transparentnost vytváří důvěru. Ne tvrzení "náš parser je nejlepší", ale důkaz "zde je metodika, zde jsou testy, zde jsou výsledky".


