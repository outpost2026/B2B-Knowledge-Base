# HANDOFF — Kompresní Realismus · Agentní Workflow · Dev Stack

**Verze:** 1.0-compact | **Datum:** 2026-06-22 | **Účel:** Sémantická komprese KB pro rychlou synchronizaci LLM agenta

---

## 1. Epistemické Axiomy (Jádro)

| Axiom | Formulace |
|-------|-----------|
| **Inteligence = Komprese** | Minimální model reality při zachování predikční schopnosti. Co nelze zkomprimovat a rekonstruovat, nebylo pochopeno. |
| **Occamova břitva** | Při srovnatelné prediktivní síle = jednodušší model. Složitost je projev nepochopení. |
| **Fyzika jako finální validační vrstva** | Napětí na baterii, kód v Cloud Run, proříznutý materiál = jediná absolutní metrika pravdy. Text je abstrakce. |
| **Falsifikovatelnost** | Každý model musí umožňovat empirické ověření. Nefalsifikovatelné = mimo kernel. |
| **Exekuce před abstrakcí** | Informace bez možnosti intervence nemá operační hodnotu. |

---

## 2. Tři Režimy Geometrického Procesoru

```
Režim 1: OSTRÝ GRADIENT          Režim 2: ORBITÁLNÍ PRŮZKUM        Režim 3: TOPOLOGICKÝ DISENTANGLEMENT
├─ Nízká entropie                 ├─ Střední entropie                ├─ Vysoká entropie
├─ Rychlý, nízké náklady          ├─ Hledání, vysoké náklady         ├─ Pomalé, masivní náklady
├─ 100% traceabilita              ├─ Confidence + CBR                ├─ Emergence, nové dimenze
├─ Fyzikální pravidla (rules.json)├─ Decision Tree + CBR fallback    ├─ Manuální review + disentanglement
└─ Mozek + LLM excelují           └─ Mozek + rané LLM                └─ Jen mozek (2026)
```

**Přepínač:** Entropie vstupní vrstvy (PCA variance ratio + KMeans separation)

| Entropie | Režim | Akce |
|----------|-------|------|
| 0.0–0.3 | Režim 1 | Physics Baseline ONLY |
| 0.3–0.7 | Režim 2 | Decision Tree + CBR |
| 0.7–1.0 | Režim 3 | Alert + SPLIT_LAYER + manuální review |

---

## 3. Asymetrie Křemík vs. Uhlík

| Vlastnost | Křemík (LLM) | Uhlík (mozek) |
|-----------|--------------|---------------|
| Trénink/inference | Odděleny, zmrazené | NEROZLIŠITELNÉ |
| Zapomínání | Žádné (dokonalý archiv) | funkce (prevence přeplnění) |
| Plasticita | Statická (interpolace) | Dynamická (emergence) |
| Slabina | Mimo-distribuční vstupy | Eroze stop, energetická daň |

**Architektura budoucnosti = hybridní:**
1. **Stabilní jádro** (silicon-like) — deterministická pravidla
2. **Plastická periferie** (carbon-like) — ML modely, CBR
3. **Konsolidační protokol** — offline retraining (EWC, experience replay)

---

## 4. Agentní Workflow — Epistemická Pravidla

### Bezpečnostní hranice
- **Zakázané cesty:** `C:\Program Files\`, `C:\Windows\`, `C:\Users\PC\AppData\`
- **Povolené cesty:** `C:\Users\PC\Documents\Repozitar_Dev\_github\`
- **Před úkolem:** `git stash` / `git commit` checkpoint
- **Po úkolu:** `git status` + `git diff --stat` + `git log`

### Destruktivní operace
- `Remove-Item -Recurse -Force` = **ZAKÁZÁNO** bez potvrzení
- `git reset --hard`, `git clean -fd` = **ZAKÁZÁNO** bez potvrzení
- `rm -rf /`, `find / -delete` = **TRVALE ZAKÁZÁNO**

### Read-after-write principle
```
PŘED: Test-Path "zdroj"
PO:   Test-Path "cíl" + ověř obsah
Při selhání = OKAMŽITĚ přestat, nikdy nepokračovat
```

---

## 5. Role LLM v SYSTEQ

### Povolené (Syntactic Offloading Only)
- Generování boilerplate kódu
- Transformace datových struktur
- Dokumentace a komentáře
- Red Team analýza (při explicitním požadavku)

### Zakázané
- Generování architektonických konceptů (LLM není architekt)
- Zavádění ML tam, kde stačí euklidovská geometrie
- Naivní O(N²) cykly pro geometrické elementy
- Antropomorfizace (žádné "prosím", "děkuji")

### Povinné
- Plná interpretovatelnost kódu (max_depth stromů ≤ 3)
- Prostorové indexy (`scipy.spatial.cKDTree`)
- Explicitní float tolerance (`math.isclose abs_tol=1.0mm`)

---

## 6. Dev Stack & Repozitáře

| Repo | Účel | Stav |
|------|------|------|
| `vcut-parser` | RE proprietárního Ruida .VCF (binární reverse engineering) | PRIVATE, golden master tests |
| `CNC_2_LLM` | DXF geometrický indexer + sémantický embedding pro ERP | PRIVATE |
| `cad2llm` | COLLADA (SketchUp) → deterministický JSON (0% halucinací) | PUBLIC |

### Technologie
- **Jazyky:** Python, Pandas, Streamlit, lxml, numpy
- **Infra:** GCP (Cloud Run, Artifact Registry, Cloud Storage)
- **Testy:** Golden master regression, smoke testy, determinismus na baseline JSONech
- **Hardware cíl:** Ruida CNC (vodní paprsek, oscilační nůž, V-slot), ESP32 IoT

---

## 7. LLM Routing — Volba Modelu dle Domény

### Doména A: Analytický Deep-Dive
| Model | Typ | Kontext | Silná stránka |
|-------|-----|---------|---------------|
| gpt-oss-120b | Sokratovský puritán | — | Nezkreslené uvažování, falsifikace |
| Hermes 3 405B | Hermetický syntetik | — | Amorální deep-dives, Jung, Stoicismus |
| Nemotron 3 Ultra | Chladný systémový architekt | 1M | Nulový sémantický drift |
| Llama 3.3 70B | Rigidní racionalista | 128k | Red Team oponentura |
| MiMo V2.5 | Multimodální pragmatik | 200k | Thinking modus, vizuální schémata |

### Doména B: Praktický Dev
| Model | Typ | Kontext | Silná stránka |
|-------|-----|---------|---------------|
| Qwen 3 Coder 480B | Král kódování | 256k | CAD/WebGL/Three.js, velké soubory |
| DeepSeek V4 Flash | Blesková exekuce | 1M | ~100+ tok/s, unit testy, ETL |
| Gemma 4 31B | Multimodální inženýr | 256k | Vizuální realita → deterministický kód |
| Nemotron 3 Super | Logický validátor | — | QC, detekce anomálií v binárních vzorcích |

---

## 8. B2B Manifest — Ochrana Protidotrických Taktik

### Axiomy obrany
- **Metered Value Injection:** Hodnota dávkována v inkrementech, nikdy asymetricky dopředu
- **Velocity Illusion:** Rychlá odpověď CEO ≠ rychlost byznys aparátu (5+ dní viskozita)
- **Ghosting Protocol:** 3x follow-up bez reakce → finální deaktivace → blackout → Cold Leads blacklist
- **NDA Weaponization:** Exkluzivní licence + likvidační pokuty > 10:1 → okamžité zmrazení + kontra-návrh (neexkluzivní licence, fixní roční)

### Ceníková strategie
- **Demo:** 1x static report + 1x video (max 2 min), bez interaktivního uploadu
- **Cloud Run TTL:** 7 dní, auto-terminace
- **Auth wall:** Term Sheet nebo Gatekeeper deposit 5 000 Kč (odečitatelný z licence)
- **Zdrojový kód:** Nikdy před finančním vypořádáním (pyarmor/C-extenze)

---

## 9. Konsolidační Protokol (Spánek Architektury)

```
┌─────────────────────────────────────────────────┐
│  [JÁDRO: stabilní inference]                    │
│       ▲                                         │
│       │ konsolidace (offline, pomalý, EWC)      │
│  [PERIFERIE: plastická adaptace]                │
│       ▲                                         │
│       │ neuromodulace (kdy/kde se periferie     │
│       │ aktivuje, top-down pozornost)           │
│  [VSTUP: nová data, inference stopy]            │
└─────────────────────────────────────────────────┘
```

**Mechanismy:** EWC, slow/fast weights, experience replay, destilace z LoRA adapterů
**Účel:** Přenos emergentních poznatků z periferie do jádra bez katastrofálního zapomínání

---

## 10. Jádrové Teze

> **Inteligence je proces vytváření kompresních modelů generativních procesů, jejichž kvalita je určena predikční přesností při minimální komplexitě.**

> **Pravda a inteligence jsou v rovnováze mezi statickou dokonalostí křemíku a krásným zapomínáním uhlíku — a v eleganci pohybu mezi nimi.**

> **Přežívají pouze systémy schopné dynamické minimalizace vnitřního tření a kontinuální re-komprese reality.**

---

*Handoff generován z: brain_geometric_processor_summary_v2.1, Mikolov_Manifest, EPISTEMICKE-PRAVIDLA-AGENTNI-PRACE, ontologie_kompresnich_modelu_reality, kalibracni_matice, LLM_routing, emergentni_prostor_esej, Sousek_Manifest_kompresniho_realismu_v1.1.json*
