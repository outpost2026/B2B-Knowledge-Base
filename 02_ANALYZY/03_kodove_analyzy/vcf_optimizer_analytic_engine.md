# VCF Optimalizátor — Analytický a Úsporný Engine

**Status:** Plánovací dokument
**Datum:** 2026-07-03
**Kontext:** Pivot Vcf-compiler z generátoru VCF na pre-produkční analytický nástroj
**Pipeline:** Grafik/zákazník → DXF → **vyvíjené nástroje** → operátor/technolog CNC → VCF → Ruida → hotový výrobek

---

## 0. Marginální logika — proč tento vektor dává smysl

### Základní princip

Současný VCF parser (`vcf_parser_b2b`) již z CAM dat čte prakticky **všechny high-SNR hodnoty**. Produkční VCF soubor je již plně analyzovatelný — cut time, defekty, sequence, tool assignment, materiálové využití. To je **hotovo**.

Největší ROI automatizačního projektu není v produkční fázi (VCF → plotr), ale v **pre-produkční fázi** (DXF → VCF). Důvod:

| Fáze | Vstup | Výstup | ROI (současný stav) |
|------|-------|--------|---------------------|
| Pre-produkce | DXF (grafika) | Analytická data pro operátora | **NEJVYŠŠÍ** — žádný nástroj neexistuje |
| Produkce | VCF | Hotový díl | Nízké — parser již existuje a je OOP/testovaný |
| Post-produkce | Hotový díl | Zpětná vazba | Střední — manuální, neautomatizované |

### Proč pre-produkce?

1. **DXF je first touchpoint** — první okamžik, kdy digitální data vstupují do výrobního procesu. Jakákoli chyba zde propaguje celým řetězcem.
2. **Operátor CNC je bottleneck** — rozhoduje o tool assignmentu, sekvenci, parametrech. Bez nástrojů jede na tacitní znalost.
3. **Materiál a čas se spotřebovávají až ve výrobě** — chyba v DXF→VCF pipeline znamená zmetek. Chyba v pre-produkční analýze = oprava za pár sekund.
4. **VCF generátor selhal na fyzické realitě** (VCutWorks GUI) — ale analytická část je plně validní. Pivot není ústup, je to **přesun na místo s nejvyšší pákou**.

### Co se nemění

- `vcf_parser_b2b` zůstává primárním parserem (již produkční, OOP, 89 testů, CI/CD)
- `dxf_integrace` zůstává DXF indexerem (čeká na OOP refactor)
- `vcf_color_service` zůstává single source of truth pro ACI barvy
- VCF generation z Vcf-compileru zůstává jako **experimentální bonus** (ne produkce)

### Co se mění

- **Vcf-compiler přestává být "kompilátor"** — stává se analytickým enginem zaměřeným na DXF preprocessing
- Hlavní výstup není VCF soubor, ale **analytický report + optimalizační doporučení**
- Cílový uživatel není VCutWorks GUI, ale **operátor CNC / technolog**

---

## 1. Pipeline — kde engine sedí

```
současnost:
Grafik ─→ DXF ─→ [ruční práce operátora] ─→ VCF ─→ Ruida ─→ díl
                (tacitní znalost, žádné nástroje,
                 ad-hoc rozhodnutí, chybováno)

s VCF optimalizátorem:
Grafik ─→ DXF ─→ [OPTIMALIZÁTOR] ─→ report + doporučení ─→ operátor ─→ VCF ─→ Ruida ─→ díl
                  │                                        ↑
                  ├─ material yield analysis                │ (rozhoduje operátor,
                  ├─ time & cost prediction                 │  engine poskytuje data)
                  ├─ defect detection
                  ├─ tool assignment check
                  └─ what-if scénáře
```

**Klíčový princip:** Engine **nerozhoduje** — engine **poskytuje data**. Operátor/technolog má poslední slovo. Toto je zásadní rozdíl oproti Vcf-compileru, který se snažil VCutWorks nahradit.

---

## 2. Architektura engine

### 2.1 Vstupy

| Vstup | Zdroj | Formát | SNR |
|-------|-------|--------|-----|
| DXF soubor | Klient / grafik | .dxf (LightBurn export) | VYSOKÝ (deterministický) |
| ACI color config | `vcf_color_service` | JSON | VYSOKÝ (empiricky kalibrováno) |
| Machine profile | `machine_profile.json` | JSON | VYSOKÝ (fyzikální model) |
| Stock panel sizes | `app_config.json` | JSON | VYSOKÝ (standardní formáty) |
| Historie (volitelné) | Předchozí běhy | JSONL | STŘEDNÍ (statistická) |

### 2.2 Moduly

```
                    ┌──────────────────────────┐
                    │   PIPELINE ORCHESTRATOR   │
                    │   (řídí workflow, cache)  │
                    └──────────┬───────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
   ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
   │ MATERIAL YIELD │ │  TIME & COST   │ │   DEFECT       │
   │   ANALYZER     │ │   ANALYZER     │ │   PREDICTOR    │
   ├────────────────┤ ├────────────────┤ ├────────────────┤
   │ stock          │ │ cutting_time() │ │ EDGE_MERGE     │
   │ _utilization() │ │ cost           │ │ MICRO_SEGMENT  │
   │ nesting        │ │ _breakdown()   │ │ UNCLOSED_LOOP  │
   │ _efficiency()  │ │ overhead       │ │ ORPHAN_ELEMENT │
   │ scrap          │ │ _analysis()    │ │ H2_NO_CUT      │
   │ _classification│ │ what_if_speed()│ │ SEQUENCE_ERROR │
   │ what_if_stock()│ │ what_if_tool() │ │ VACUUM_RISK    │
   └────────────────┘ └────────────────┘ └────────────────┘
                               │                  │
                               ▼                  ▼
                    ┌──────────────────────────┐
                    │   OPTIMIZATION ENGINE    │
                    │                          │
                    │ tool_reassignment()      │
                    │ path_optimization()      │
                    │ panel_nesting()          │
                    │ parameter_tuning()       │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │      OUTPUT LAYER        │
                    │                          │
                    │ Executive Summary (MD)   │
                    │ Technical Report (MD)    │
                    │ What-If Scenarios (MD)   │
                    │ VCF (bonus, experimental)│
                    └──────────────────────────┘
```

### 2.3 Detail modulů

#### Modul A: Material Yield Analyzer

**Účel:** Analyzovat, jak efektivně je využit materiál na stock desce. Navrhnout optimální layout.

| Funkce | Vstup | Výstup | Stav |
|--------|-------|--------|------|
| `stock_utilization()` | DXF entities + stock_size | yield%, waste m², waste% | ⚠️ Částečně v `dxf_integrace`, chybí standalone wrapper |
| `nesting_efficiency()` | entity bounding boxes | utilization%, unused area popis | ❌ Nová |
| `scrap_classification()` | waste geometry + typy | reusable / scrap / edge-trim kategorie | ❌ Nová |
| `what_if_stock()` | entities + 6 stock formátů | srovnávací tabulka yield% per formát | ❌ Nová |

**Příklad výstupu:**
```json
{
  "current_stock": "3200x1950",
  "yield_percent": 68.3,
  "waste_m2": 1.24,
  "waste_breakdown": {
    "reusable_strips": { "m2": 0.42, "pct": 21.3 },
    "edge_trim": { "m2": 0.58, "pct": 29.4 },
    "internal_scrap": { "m2": 0.24, "pct": 12.2 }
  },
  "alternative_stocks": [
    { "stock": "2800x2070", "yield": 74.1, "delta_pct": 5.8 },
    { "stock": "3000x1500", "yield": 52.3, "delta_pct": -16.0 }
  ]
}
```

#### Modul B: Time & Cost Analyzer

**Účel:** Predikovat reálný výrobní čas a náklady ještě před řezáním. Umožnit what-if analýzu.

| Funkce | Vstup | Výstup | Stav |
|--------|-------|--------|------|
| `cutting_time()` | geometry + kinematics | čas v sekundách (2-5% přesnost) | ✅ Existuje v `vcf_parser_b2b` i `dxf_integrace` |
| `cost_breakdown()` | čas + materiál + režie | Kč za stroj, materiál, celkem | ✅ Existuje v `app.py`, chybí standalone |
| `overhead_analysis()` | traverse, lift, setup | skryté náklady v Kč | ⚠️ Částečně |
| `what_if_speed()` | feed_rate + acceleration | časové scénáře | ❌ Nová |
| `what_if_tool()` | vibrate vs v-slot reassignment | srovnání časů | ❌ Nová |

**Příklad výstupu:**
```json
{
  "baseline": {
    "total_time_s": 347,
    "total_time_formatted": "5m 47s",
    "cost_czk": 187,
    "cost_breakdown": {
      "machine": { "rate_kc_min": 18.5, "total_kc": 107 },
      "material": { "rate_kc_m2": 420, "used_m2": 0.19, "total_kc": 80 }
    }
  },
  "what_if": [
    { "scenario": "zvýšit feed o 20%", "time_s": 295, "savings_kc": 16, "risk": "nízké" },
    { "scenario": "přesunout decor na v-slot", "time_s": 312, "savings_kc": 11, "risk": "střední" }
  ]
}
```

#### Modul C: Defect Predictor

**Účel:** Detekovat výrobní chyby ještě před řezáním. Port KB engine z `vcf_parser_b2b` do samostatného modulu.

| Rule | Třída | Zdroj | Stav |
|------|-------|-------|------|
| EDGE_MERGE_MISSING | B (empirická) | `vcf_geometry.py` | ✅ Existuje |
| MICRO_SEGMENT | B (empirická) | `vcf_geometry.py` | ✅ Existuje + SNR filter |
| UNCLOSED_LOOP | B (empirická) | `vcf_geometry.py` | ✅ Existuje |
| ORPHAN_ELEMENT | C (heuristická) | `vcf_geometry.py` | ✅ Existuje |
| UNCONNECTED_INTERNAL_DECOR | C (heuristická) | `vcf_geometry.py` | ✅ Existuje |
| H2_NO_CUT_THROUGH | A (fyzikální) | `engine.py` | ✅ Existuje |
| SEQUENCE_LAYER_ERROR | B (empirická) | `engine.py` | ✅ Existuje |
| VACUUM_FIXATION_RISK | A (fyzikální) | `engine.py` | ✅ Existuje |

**Klíčová vlastnost:** Každá detekce je opatřena epistemic confidence (CLASS_A..D). Operátor vidí nejen "co je špatně", ale i **jak moc si tím můžeme být jisti**.

**Příklad výstupu:**
```json
{
  "defects": [
    {
      "rule_id": "EDGE_MERGE_MISSING",
      "severity": "WARNING",
      "confidence": 0.87,
      "rule_class": "B",
      "layer": 1,
      "element_id": 7,
      "description": "Open path inside parent, endpoint 3.2mm from edge"
    },
    {
      "rule_id": "SEQUENCE_LAYER_ERROR",
      "severity": "CRITICAL",
      "confidence": 0.94,
      "rule_class": "B",
      "description": "Outer contour cut (vibrate) occurs before decorative operations"
    }
  ],
  "risk_score": 2.3,
  "max_severity": "CRITICAL"
}
```

#### Modul D: Optimization Engine

**Účel:** Poskytnout akční doporučení — nejen "co je špatně", ale "jak to zlepšit".

| Funkce | Princip | EROI |
|--------|---------|------|
| `tool_reassignment()` | Mode-based statistika z 35 VCF + ACI color config | VYSOKÉ — opraví organizační chaos v barvách |
| `path_optimization()` | Topologické řazení (outer→inner) | STŘEDNÍ — time saving ~2-5% |
| `panel_nesting()` | Entity bounding box + stock size | VYSOKÉ — material saving ~5-15% |
| `parameter_tuning()` | Speed/H1/H2 trade-off analýza | NÍZKÉ — vyžaduje víc dat |

---

## 3. Vztah k existujícím repozitářům

```
vcf_color_service         dxf_integrace              vcf_parser_b2b
(pip balíček)             (DXF indexer)              (VCF parser)
     │                         │                          │
     │ ACI config              │ index_dxf()               │ parser engine
     │ color mapping           │ cutting_time              │ KB rules
     │ fallbacky               │ material_yield            │ defect catalog
     │                         │ tool_assignments          │ SNR kalibrace
     ▼                         ▼                          ▼
     ┌──────────────────────────────────────────────────────┐
     │               VCF OPTIMALIZÁTOR                      │
     │                    (nový)                            │
     │                                                      │
     │  Orchestruje: yield + time + defects + optimization  │
     │  Výstup:       report (MD/JSON) + doporučení         │
     │  Závislosti:   vcf_color_service (pip)               │
     │                dxf_integrace (funkce)               │
     │                vcf_parser_b2b (engine, rules)        │
     └──────────────────────────────────────────────────────┘
                               │
                               ▼
                    Operátor CNC / Technolog
                    (rozhoduje, engine poskytuje data)
```

---

## 4. Output formáty

### Executive Summary (primární — pro manažera/technologa)

Cca 1 A4, markdown (snadný export do PDF). Obsahuje:

```
┌─────────────────────────────────────────────────────┐
│              EXECUTIVE SUMMARY                       │
├─────────────────────────────────────────────────────┤
│ DXF: panel_lamela_12mm.dxf                          │
│ Datum: 2026-07-03                                   │
│                                                      │
│ ┌───────────────────────────────────────────┐       │
│ │ MATERIAL YIELD                            │       │
│ │ yield: 68.3%  │  waste: 1.24 m²          │       │
│ │ stock: 3200x1950                          │       │
│ │ doporučení: zvážit 2800x2070 (74.1%)      │       │
│ └───────────────────────────────────────────┘       │
│                                                      │
│ ┌───────────────────────────────────────────┐       │
│ │ TIME & COST                              │       │
│ │ cut time: 5m 47s  │  cost: 187 Kč        │       │
│ │ z toho: stroj 107 Kč, materiál 80 Kč     │       │
│ │ what-if: +20% feed → -16 Kč (nízké riz.)│       │
│ └───────────────────────────────────────────┘       │
│                                                      │
│ ┌───────────────────────────────────────────┐       │
│ │ DEFECTS                                  │       │
│ │ ● SEQUENCE_LAYER_ERROR (CRITICAL)        │       │
│ │ ● EDGE_MERGE_MISSING (WARNING)           │       │
│ │ ● ORPHAN_ELEMENT (INFO)                  │       │
│ └───────────────────────────────────────────┘       │
│                                                      │
│ Akce: opravit sequence error, zkontrolovat ACI barvy│
└─────────────────────────────────────────────────────┘
```

### Technical Report (sekundární — detail pro debug)

Kompletní JSON dump všech analyzovaných dat. Vhodný pro:
- Archivaci (ground truth)
- ML pipeline
- Cross-validaci mezi verzemi enginu
- Zpětné dohledání příčiny zmetku

### What-If Scenarios (terciární — pro rozhodování)

3-5 variant s doporučením. Např.:
1. Baseline (current state)
2. Optimalizace tool assignmentu
3. Změna stock formátu
4. Zvýšení feed rate
5. Kombinace výše uvedeného

---

## 5. Implementační strategie

### Fáze 0 — Pipeline orchestrator (2-3 dny)

**Cíl:** Spojit existující komponenty do jedné pipeline.

| Krok | Co | Závislost |
|------|----|-----------|
| 0.1 | Extract `predict_cut_time()` do standalone modulu | `vcf_parser_b2b` |
| 0.2 | Extract yield calculation z `dxf_integrace` wrapper | `dxf_integrace` |
| 0.3 | Vytvořit `Orchestrator` třídu (DXF → results dict) | 0.1 + 0.2 |
| 0.4 | Vytvořit `ExecutiveSummary` formatter (MD) | 0.3 |
| 0.5 | Základní testy (1 DXF → očekávaný výstup) | 0.4 |

**Výstup:** `python -m vcf_optimizer run panel.dxf` → executive summary MD

### Fáze 1 — Material Yield Analyzer (2 dny)

**Cíl:** Plně funkční yield analýza se všemi what-if scénáři.

| Krok | Co | Detail |
|------|----|--------|
| 1.1 | `stock_utilization()` | Z `dxf_integrace.material_yield`, přidat waste% |
| 1.2 | `nesting_efficiency()` | bounding box + entity area sum |
| 1.3 | `scrap_classification()` | Stripy >50mm = reusable, <50mm okraj = trim |
| 1.4 | `what_if_stock()` | Iterovat 6 stock formátů, porovnat yield |
| 1.5 | Výstup do Executive Summary | Tabulka + doporučený formát |

### Fáze 2 — Defect Predictor (2-3 dny)

**Cíl:** Portovat KB engine + geometry rules.

| Krok | Co | Detail |
|------|----|--------|
| 2.1 | Port KB engine tříd (`CLASS_A..D`, confidence) | Z `vcf_parser_b2b.Knowledge_base` |
| 2.2 | Port geometry rules | Z `features/2D_visual_warnigs` branch |
| 2.3 | Port SNR kalibraci | density filter, endpoint proximity |
| 2.4 | Integrovat do pipeline | Každý defect má confidence + severity |

### Fáze 3 — Optimization Engine (3-5 dní)

**Cíl:** První verze akčních doporučení.

| Krok | Co | Detail |
|------|----|--------|
| 3.1 | `tool_reassignment()` | Mode-based: z 35 VCF extrahovat typické ACI→tool |
| 3.2 | `path_optimization()` | Topologické řazení per layer |
| 3.3 | `panel_nesting()` | Jednoduchá verze (bounding box fit) |
| 3.4 | What-if engine | Propojit yield + time + defects |

### Fáze 4 — VCF generation downgrade (1 den)

| Krok | Co |
|------|----|
| 4.1 | Přesunout `write()` do `vcf_optimizer.vcf_bonus` |
| 4.2 | Explicitní warning: "research — not production ready" |
| 4.3 | Dokumentovat roundtrip limitace |

---

## 6. Rizika a mitigace

| Riziko | P | Dopad | Mitigace |
|--------|---|-------|----------|
| Scope creep (solo dev) | 0.5 | VYSOKÉ | Fáze striktně dle EROI. Žádný "ještě přidáme X". |
| Nevalidovaná optim. doporučení | 0.6 | STŘEDNÍ | Všechna doporučení = CLASS_C/D dokud nejsou empiricky potvrzena |
| Duplicita kódu | 0.4 | NÍZKÉ | Extract do pip balíčků (vcf_color_service pattern) |
| Operátor ignoruje report | 0.7 | STŘEDNÍ | Engine nediktuje — poskytuje data. Rozhodnutí je na operátorovi. |
| Zákazník chce VCF generátor | 0.5 | STŘEDNÍ | Jasná komunikace: analytický nástroj s bonusovým experimentálním modulem |

---

## 7. Srovnání: původní Vcf-compiler vs VCF optimalizátor

| Dimenze | Vcf-compiler (původní) | VCF optimalizátor (nový) |
|---------|----------------------|-------------------------|
| Primární účel | Generovat VCF z DXF | Analyzovat DXF a optimalizovat výrobu |
| Hlavní výstup | binary .VCF soubor | MD/JSON report + doporučení |
| Cílový uživatel | VCutWorks GUI | Operátor CNC / Technolog |
| Validace | Roundtrip self-consistency | Epistemic confidence + empirická data |
| Produkční ready | Ne (VCutWorks incompatibility) | Ano (deterministická analýza, žádné GUI závislosti) |
| Místo v pipeline | Konec (produkce) | Začátek (pre-produkce) |
| B2B hodnota | 35 000 Kč (zrušeno) | TBD — vyšší protože řeší reálný bottleneck |
| Závislost na `dxf_integrace` | Ano (compile_dxf) | Ano (index_dxf), ale volitelně |
| Riziko selhání | VYSOKÉ (GUI závislost) | NÍZKÉ (deterministické, žádné externí závislosti) |

---

## 8. Klíčové hodnoty pro B2B positioning

| Hodnota | Pro klienta | Měřítko |
|---------|-------------|---------|
| Úspora materiálu | 5-15% díky lepšímu nestingu | % yield improvement |
| Úspora času | 2-5% díky optimalizaci sekvence | minutes per panel |
| Snížení zmetkovitosti | Detekce defektů před řezáním | počet zachycených chyb |
| Snížení závislosti na tacitní znalosti | Formalizace know-how operátora | počet dní zaškolení |
| Rychlost kalkulace | Ihned po nahrání DXF | seconds |

**Unikátní prodejní argument:** Žádný nástroj na trhu neumí analyzovat DXF pro CNC oscillating knife cutting z hlediska yield, času, nákladů a defektů **zároveň**. Existují CAM nástroje (VCutWorks, LightBurn), ale ty generují dráhy — neanalyzují efektivitu. Existují ERP systémy, ale ty neznají geometrii. VCF optimalizátor je **první nástroj, který spojuje geometrickou analýzu s výrobní ekonomikou**.

---

## 9. Okamžité další kroky

1. **Rozhodnout:** Samostatný repozitář (`vcf_optimizer`) nebo rozšíření Vcf-compiler? (Doporučuji samostatný, aby nedošlo k záměně)
2. **Fáze 0:** Extrahovat `predict_cut_time()` a yield wrapper — 2-3 dny
3. **Fáze 1:** Implementovat `stock_utilization()` + `what_if_stock()` — 2 dny
4. **Validovat:** Spustit na 35 VCF z `VCF_files_moodpasta` — ověřit konzistenci s reálnými výrobními daty
5. **Prezentovat:** Ukázat Františkovi (Moodpasta) jako rozšíření stávající nabídky

---

*Dokument vytvořen: 2026-07-03*
*Navazuje na: R&D_evoluce_portfolia_03_2026-07_2026.md, portfolio_audit_a_match.md, .ai_state.json*
