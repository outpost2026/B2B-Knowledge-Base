# R&D Evoluce Portfolia — Bod 0 do současného stavu

**Autor:** Ondřej Soušek **Datum:** 2026-07-03 **Rozsah:** 2026-03-24 → 2026-07-03 (101 dní) **Celkem commitů:** ~494 napříč 12 repozitáři **Struktura:** 5 fází, každá s definovaným triggerem, výstupem a kognitivním patternem


## Fáze 0 — Pre-GitHub: Tacitní baseline (před březen 2026)

### Výchozí bod

Autor vstupuje do GitHub arény nikoli jako "junior developer začínající s Hello World", ale jako **tacitní expert** se zkušeností v CNC výrobě, CAM workflow a provozní automatizaci. Klíčová charakteristika: znalosti existují, ale nejsou externalizované — nejsou v kódu, nejsou v git historii, nejsou formalizované.

### Co autor uměl před prvním commitem (rekonstrukce z dokumentace)

| Dovednost | Úroveň | Způsob nabytí |
| - | - | - |
| CNC obsluha a programování | Produkční | Praxe u vodního paprsku, oscilačního nože |
| CAM workflow (VCutWorks, LightBurn) | Produkční | Každodenní provoz |
| Ruida VCF formát (mentální model) | Tacitní expert | Intuitivní porozumění z provozu |
| DXF formát a ACI barvy | Provozní | Práce s grafickými předlohami |
| Python základy | Samouk | Vlastní RPA a scraping scripty |
| GCP Cloud | Experimentální | Auto-bootstrapping: Python skript vydělal 2 000 Kč → Dell server |


### Trigger pro vstup do GitHubu

Autor narazil na **limitaci tacitního režimu**: LLM model (Gemini) mu přepisoval instrukce a obsah, behaviorální nekonzistence modelů ho frustrovala. Potřeboval:

1. Externalizovat svou metodiku práce s LLM

2. Zdokumentovat případy selhání modelů

3. Vytvořit opakovatelný framework

První commit nebyl "Hello World" — byla to **kazuistika selhání AI modelu** (kazuistiky\_llm\_sprint, 24. 3. 2026).


## Fáze 1 — Epistemická explorace (24. 3. – 3. 4. 2026, 10 dní)

### Charakteristika

Dominantně **dokumentační fáze**. 93 % obsahu tvoří markdown, 7 % Python kód. Autor nebuduje software — buduje **kognitivní framework** pro práci s LLM.

| Repo | Datum založení | Commitů | Charakter |
| - | - | - | - |
| `rag\_indexer` | 24. 3. 2026 | 14 | RAG preprocessing prototyp |
| `kazuistiky\_llm\_sprint` | 24. 3. 2026 | 127 | Metodologie, case studies, manifesty |
| `cad2llm` | 31. 3. 2026 | 16 | SketchUp → JSON deterministic parser |
| `outpost\_security\_perimeter` | 1. 4. 2026 | 20 | IoT koncept (ESP32, dokumentace) |
| `outpost2026\_profile` | 1. 4. 2026 | 45 | Profilový README |


### Klíčové události

1. **První commit vůbec** (24. 3., rag\_indexer): `universal\_indexer\_v7.py` — preprocessing nestrukturovaných dat pro RAG. Už v tomto bodě autor řeší encoding hell (cp1250→utf-8) a filtraci balastu.

2. **Case study: Gemini přepisuje instrukce** (25. 3.): Autor dokumentuje, jak Gemini model modifikuje uživatelský prompt a obsah. Toto je **zakladatelský moment** celé epistemiky — zkušenost s modelem, který "lže" nebo "přebije" autorovu intenci, vede k vytvoření celého systému guardrails, golden rules a handoff formátu.

3. **Metodika práce s LLM** (26. 3.): Vzniká `metodika\_prace\_s\_LLM.md` — systematický rámec pro agentní workflow. Tento dokument je přímým předchůdcem `EPISTEMICKE-PRAVIDLA-AGENTNI-PRACE.md` (403 řádků).

4. **Self-bootstrapping case** (2. 4.): Dokumentace příběhu "Python RPA → Dell server za 2 000 Kč". První zmínka o transfer learningu z provozní reality do IT.

5. **Kariérní analýza v éře saturace AI** (3. 4.): Autor si uvědomuje, že trh s AI je saturovaný a píše analýzu kariérních přechodů. Toto je **první B2B uvažování** — ještě není produkt, ale už je positioning.

6. **cad2llm** (31. 3.): Deterministický parser SketchUp→JSON s 4×4 maticemi. Už zde autor aplikuje princip "0 % halucinací" — reakce na nespolehlivost LLM při práci s CAD geometrií.

### Kognitivní pattern Fáze 1

```
Frustrace z AI → Dokumentace selhání → Formalizace metodiky →   
Aplikace na reálný problém (CAD parser, IoT koncept)
```

Autor reaguje na **nedůvěryhodnost AI modelů** vytvořením epistemického rámce. Není to "AI adoption" v běžném smyslu — je to **obranná strategie**: jak používat AI, aniž by autor ztratil kontrolu nad výstupem.


## Fáze 2 — Reverzní inženýrství a VCF parser (7. 6. – 11. 6. 2026, 4 dny)

### Trigger

Po 65denní pauze (3. 4. → 7. 6.) se autor vrací s konkrétním cílem: **zformalizovat tacitní znalost VCF formátu do kódu**. Pauza není nečinnost — autor mezitím pracoval na lokálním RE výzkumu (22 verzí parseru mimo git).

### Exploze aktivity

| Repo | Založeno | Commitů | Hustota |
| - | - | - | - |
| `dxf\_integrace` | 7. 6. 2026 | 48 | 48 commitů za 24 dní |
| `vcf\_integrace` | 9. 6. 2026 | 15 | Celý RE backlog v1-v20 |
| `web\_integrace\_systeq` | 10. 6. 2026 | 75 | Web + Three.js |
| `vcf\_parser\_b2b` | 11. 6. 2026 | 73 | B2B produkt |


### Klíčové události

1. **dxf\_integrace: První produkční kód** (7. 6.): DXF Geometry Indexer V2.2.0. Už první commit obsahuje 2 259 LOC v jednom souboru (58 funkcí, 0 tříd). Procedurální spaghetti — ale **funkční**.

2. **P0-P2 fixy během jediného dne** (7. 6.):

   - P0: odstranění nondeterminismu (semantic\_layer\_mapping, filename\_overrides)

   - P1: geometry kritické fixy (vslot double-pass, shapely.contains, nesting\_tree)

   - P2: ACI color priority s conflict detection

   - Tento pattern je charakteristický: autor identifikuje kritické problémy (P0→P2) a řeší je v jednom session.

3. **Semantic embedding dashboard** (8. 6.): Streamlit UI s drag-drop DXF, KPI boxy, 2D PNG vizualizace. První **uživatelské rozhraní** v portfoliu.

4. **ACI Color Blindness crisis** (8. 6.): Celodenní debugging ACI barevného mapování. LightBurn používá jinou ACI paletu než AutoCAD standard. Autor vyvíjí euklidovskou RGB interpolaci pro přiřazení barev. Tento problém bude rezonovat celým portfoliem až do vzniku `vcf\_color\_service` (o 24 dní později).

5. **VCF parser backlog v1-v20** (9. 6.): `vcf\_integrace` obsahuje 22 verzí parseru, 29 dní RE práce, 99.98% přesnost. IEEE 754 double float little-endian, Windows-1250 encoding, 74B segment blocks — autor dešifruje proprietární binární formát **bez dokumentace**.

6. **Architektonická chyba: god class** (9. 6.): `RuidaVcfEngineV20` v `vcf\_integrace` je 19k LOC monolit s hardcoded values. Autor si uvědomuje dluh a o 2 dny později zakládá `vcf\_parser\_b2b` jako čistý reimport.

### Kognitivní pattern Fáze 2

```
Tacitní znalost → Externalizace do kódu → Debugování →  
Rozpoznání technického dluhu → Rozhodnutí refaktorovat
```

Autor přechází z "psaní dokumentace" do "psaní kódu", ale metodologie zůstává stejná: **systematická dekonstrukce problému**. RE VCF formátu je strukturálně identický proces jako psaní kazuistiky — jen cíl je jiný.


## Fáze 3 — B2B produktizace a kvalita (11. 6. – 28. 6. 2026, 17 dní)

### Trigger

Autor si uvědomuje, že VCF parser má komerční hodnotu. Zakládá `vcf\_parser\_b2b` jako **produktový fork** — oddělený od R&D repa (`vcf\_integrace`). Toto je klíčový moment: **z výzkumníka se stává dodavatel**.

### Exploze systematického testování

| Iterace | Datum | Obsah |
| - | - | - |
| It0 (HYGIENE) | 11. 6. | Structured logging, fix bare excepts |
| It1 (TESTS) | 11. 6. | Golden master regression + coverage |
| It2 (DEDUP) | 11. 6. | Extrakce modulů z god class |
| v21 | 11. 6. | Element-level cut sequence, KB nesting |
| v22 | 12. 6. | Circle center fix, layer-based PNG viz |
| v23 | 12. 6. | UI overhaul, engine cleanup |
| v24 | 13. 6. | Phase 1 bugfixes (6 commitů v 1 dni) |
| v25 | 14. 6. | Circle detection, Catmull-Rom, 45 testů |
| v26 | 14. 6. | DEFECT\_CATALOG V1 — 20 výrobních chyb |
| v27 | 15. 6. | KB rules engine, SNR calibration |
| v28 | 15. 6. | Deploy v1.2-demo, hero navigation |
| v29 | 16. 6. | SNR kalibrace — cross-layer filtrování |
| v30 | 16. 6. | Tech group merging, MICRO\_SEGMENT off |


### Klíčové události

1. **Golden master metodologie** (11. 6.): Místo unit testů autor nasazuje **baseline JSON diff** — porovnává parser output proti předem schváleným referenčním souborům. Toto je převzato z RE metodologie (empirická validace), ne z učebnic testování.

2. **DEFECT\_CATALOG V1** (14. 6.): Ontologická báze 20 detekovatelných výrobních chyb — EDGE\_MERGE\_MISSING, MICRO\_SEGMENT, UNCLOSED\_LOOP, ORPHAN\_ELEMENT. Autor převádí **tacitní znalost vadného řezání** do explicitních pravidel.

3. **SNR kalibrace** (16. 6.): Autor si uvědomuje, že ne všechny detekované "vady" jsou reálné problémy — některé jsou falešně pozitivní. Zavádí **poměr signál-šum** pro geometrickou analýzu. Toto je koncept přenesený z audio/radio technologie do CNC výroby.

4. **GCP deployment** (15. 6.): Streamlit app na Cloud Run. 6 deployů během jediného dne. Autor se učí Docker, Cloud Run config, websocket keepalive, XSRF ochranu — vše v produkčním režimu.

5. **B2B pricing a komunikace**:

   - 70 000 Kč za Phase 1 (A + B-A + C2)

   - Executive summary v2.1 odeslána Františku Sehnalovi 28. 6.

   - Follow-up plán: 7. 7.

6. **Vznik epistemické infrastruktury** (25. 6.): `B2B-Knowledge-Base` — 76 artifactů z B2B/, KB/ a kazuistik. Centralizace knowledge do RAG-ready struktury.

### Kognitivní pattern Fáze 3

```
Produkt → Kvalita → Detekce šumu → SNR kalibrace →   
Systematizace → B2B komunikace
```

Autor aplikuje provozní myšlení (SNR, falešné pozitivity) na software engineering. Nezavádí "best practices" z učebnic — zavádí **metriky z fyzické reality**.


## Fáze 4 — VCF kompilátor a cross-repo architektura (27. 6. – 2. 7. 2026, 5 dní)

### Trigger

Pokud parser umí číst VCF, proč neumí psát? Autor zakládá `Vcf-compiler` — zpětný proces: DXF → VCF. Tento projekt je **čistý R&D** (není součástí B2B dodávky).

### Intenzita RE výzkumu

38 commitů za 5 dní. Každý commit je experiment — hypotéza → test → výsledek.

#### Evoluce writeru (den po dni)

| Den | Objev | Status |
| - | - | - |
| 27. 6. 08:27 | Initial VcfWriter implementation | Funkční, nevalidní |
| 27. 6. 12:53 | Header format: 0x13 prefix, 257 blocks | Posun |
| 27. 6. 13:28 | number\_of\_feeding=0, geometry type=1 | Korekce |
| 27. 6. 15:05 | ACI 7 color mapping (white→black) | Fix |
| 27. 6. 17:16 | Geometry encoding — native header template bytes | Breakthrough |
| 27. 6. 19:23 | Fishbone + manchester DXF→VCF | První reálný výstup |
| 29. 6. 12:28 | **3 root causes fixed** (trailer, element\_count@92, direction@104) | Writer OK |
| 29. 6. 16:27 | Circle Bézier encoding (H11), 196B footer (H12), multi-layer (H13) | Phase 2 |
| 29. 6. 16:29 | Spurious 200-byte TRAILER\_PREFIX — root cause 'unknown element' | Breakthrough |
| 30. 6. 00:13 | Multi-element element count — ec@92=1, offset606=total\_elements | GUI detects 2nd element |
| 30. 6. 14:20 | Least-squares circle fit vs naive \_points\_on\_circle | Matematický upgrade |


### Klíčové objevy

1. **Paradox tolerance**: Syntetická VCF jsou validní pro vlastní parser (roundtrip OK), ale invalidní pro VCutWorks GUI. Vlastní parser je tolerantnější než Ruida rendering engine. **Autor zjistil, že jeho parser je lepší než nástroj, který reverse-engineeruje.**

2. **RE tooling** (30. 6.): 5 nových RE analýz nástrojů — decode\_subtype\_bits, dissect\_footers, dissect\_layer\_blocks, segment\_geometry\_stats, batch\_correlate\_dxf\_vcf. 62-file analýza.

3. **Cross-repo dependency**: `compile\_dxf()` volá `dxf\_integrace.index\_dxf()`. Vzniká první závislost mezi repy. Autor si uvědomuje, že potřebuje:

   - OOP refactor dxf\_integrace (58 func → třídy)

   - Centrální ACI color mapping (vcf\_color\_service)

   - Cross-repo CI/CD dispatch

4. **ACI Color Service** (2. 7.): `vcf\_color\_service` — pip balíček jako jediný zdroj pravdy pro ACI barvy. Řeší 4× duplicitní nekonzistentní mapy napříč repy. Statistická extrakce z 35 customer VCF odhaluje: **problém je organizační, ne technický** — operátoři přiřazují ACI barvy ad-hoc.

### Kognitivní pattern Fáze 4

```
Paradox → Hypotéza → Experiment → Validace →  
Systematizace do nástrojů → Architektonické uvědomění
```

Autor přechází od "řešení jednoho problému" k "navrhování systému řešení problémů". Vcf-compiler není samostatný projekt — je to **katalyzátor architektonického zrání**.


## Fáze 5 — CI/CD a infrastruktura (1. 7. – 3. 7. 2026, 3 dny)

### Trigger

Po 3 měsících vývoje má autor 5 aktivních Python repozitářů s 0 CI/CD. Rozhodnutí: implementovat Tier 1 pipeline přes celé portfolio.

### Implementace

| Komponenta | Pokrytí |
| - | - |
| CI matrix | 3.10/3.11/3.12 — všechna aktivní repa |
| Nightly cron | 6:00 UTC — všechna aktivní repa |
| CodeQL | Security scanning — všechna aktivní repa |
| Dependabot | Dependency monitoring — všechna aktivní repa |
| workflow\_dispatch | Manuální trigger — všechna aktivní repa |
| Cross-repo dispatch | dxf\_integrace → Vcf-compiler |
| Badge | Pytest badge na main — všechna aktivní repa |


### Edu artifact

Vzniká `CI\_GitHub\_Actions\_imerzni\_edu\_v1.md` — imerzní výklad CO/PROČ/JAK/EROI. Autor aplikuje svůj epistemický rámec (co/proč/jak/efekt/riziko) na CI/CD. **Nepřebírá best practice — analyzuje ji.**

### Archivační rozhodnutí

`vcf\_integrace` → **LEGACY** (god class, 0 testů, duplicitní, hardcoded passwords). Kód migrován do `vcf\_parser\_b2b`. Rozhodnutí je racionální a neemocionální.

### Kognitivní pattern Fáze 5

```
Detekce mezery (chybí CI/CD) → Transfer learning (co/proč/jak) →  
Implementace napříč portfoliem → Edu artifact →   
Systematická údržba
```


## AI/IT Adopce: Trajektorie

### Fáze 0: Skeptický uživatel

- Používá Gemini, zažívá přepisování instrukcí

- Reakce: frustrace, dokumentace selhání

- **Vztah k AI:** Nedůvěřivý, ale zvídavý

### Fáze 1: Metodolog

- Vytváří golden rules pro LLM práci

- Testuje 5 modelů (DeepSeek, Gemini, Claude, Groq, ChatGPT)

- Zavádí handoff JSON formát (15+ dokumentů)

- **Vztah k AI:** Instrumentální — AI je nástroj, ne autorita

### Fáze 2: Ko-pilot

- LLM používá jako párový programátor pro RE výzkum

- Každý commit je výsledek session: člověk rozhoduje, AI generuje varianty

- **Vztah k AI:** Kolaborativní — AI rozšiřuje kapacitu, ne nahrazuje úsudek

### Fáze 3: Systematik

- Formalizuje AI workflow do epistemického rámce

- Vytváří guardrails pro agentní práci

- **Vztah k AI:** Řízený — AI pracuje v definovaných mantinelech

### Fáze 4: Architekt

- AI orchestruje cross-repo pipeline

- Multi-model orchestrace: každý model pro specifickou doménu

- **Vztah k AI:** Hierarchický — člověk je architekt, AI je vykonavatel

### Trajektorie: AI Adoption Maturity Model

```
Nedůvěra → Dokumentace → Metodika → Orchestrace →   
Epistemický rámec → Agentní workflow
```

Autor neprošel standardním "AI adoption" cyklem (zvědavost → experiment → produkce). Prošel **inverzním cyklem**: selhání → analýza → formalizace → kontrola. To je konzistentní s jeho profilem "Třída-3 systémový stavitel".


## Celková statistika portfolia

### Commitová aktivita (chronologicky)

| Měsíc | Commity | Dominantní repo |
| - | - | - |
| Březen (24.–31.) | ~45 | kazuistiky\_llm\_sprint, rag\_indexer |
| Duben (1.–5.) | ~65 | kazuistiky\_llm\_sprint, outpost2026\_profile |
| Duben–červen (6.4.–6.6.) | 0 | Pauza (lokální RE výzkum) |
| Červen (7.–30.) | ~310 | vcf\_parser\_b2b (73), dxf\_integrace (48), web\_integrace\_systeq (75), Vcf-compiler (38) |
| Červenec (1.–3.) | ~55 | CI/CD implementace napříč všemi repy |


### Trend: dokumentace → kód → infrastruktura

```
Březen:   ████████░░ 80% dokumentace, 20% prototypy  
Duben:    ██████░░░░ 60% README, 40% koncepty  
Červen:   ██░░░░░░░░ 20% docs, 80% produkční kód  
Červenec:  ░░░░░░░░░░ 5% docs, 95% CI/CD kód
```

### Vývoj test coverage

| Fáze | Testy | Metodika |
| - | - | - |
| F1 (březen) | 0 testů | Žádné |
| F2 (7.–11. 6.) | 0 testů | Pouze empirická validace |
| F3 early (11. 6.) | Golden master (10) | Baseline JSON diff |
| F3 mid (14. 6.) | 45 unit testů | Pytest + golden master |
| F3 late (15. 6.) | Smoke testy (6) | Deploy pipeline |
| F4 (27.–30. 6.) | 28 testů | Vcf-compiler pytest |
| F5 (1.–3. 7.) | 89+24+28+6 | CI matrix všechna repa |


### Vývoj architektonické zralosti

| Fáze | Architektura | Problém |
| - | - | - |
| F2 | 58 func / 0 tříd (dxf\_integrace) | Procedurální spaghetti |
| F2 | 19k LOC god class (vcf\_integrace) | Monolit, hardcoded values |
| F3 | 2 třídy (vcf\_parser\_b2b) | Částečná OOP |
| F4 | 6 tříd, 5 modulů (Vcf-compiler) | Plná OOP |
| F4 | pip balíček (vcf\_color\_service) | Modularizace |
| F5 | Cross-repo dispatch | Distribuovaná architektura |



## Kognitivní vzorce napříč portfoliem

### Pattern 1: Problém → Nástroj → Framework

1. Narazí na problém (např. ACI color divergence)

2. Napíše skript na detekci (`vcf\_validate\_layers.py`)

3. Zobecní do pip balíčku (`vcf\_color\_service`)

4. Vytvoří epistemický rámec ("problém je organizační, ne technický")

### Pattern 2: Session-based workflow

Každý commit je výsledek LLM session. Formát: `feat/fix/docs: popis`. Handoff JSONy dokumentují reasoning. **Autor nepíše kód lineárně — píše ho v iteracích s AI feedback loopem.**

### Pattern 3: Transfer learning napříč doménami

- SNR kalibrace → z audio technologie do CNC detekce vad

- Golden master testování → z RE metodologie do software testingu

- Co/Proč/Jak/Efekt/Riziko → z epistemiky do CI/CD implementace

- Komprese reality (Mikolov) → z LLM teorie do architektury kódu

### Pattern 4: Nízká tolerance k nejednoznačnosti

- Deterministický parser (cad2llm) — "0 % halucinací"

- Golden master testy — baseline JSON diff, žádné flaky testy

- Roundtrip validace — parser musí přečíst co napsal

- Explicitní ground truth — "validation\_status: empirical/calibrated/hypothesis"


## Regresivní momenty

1. **God class anti-pattern** (vcf\_integrace): 19k LOC, 0 testů, hardcoded passwords. Autor přiznává chybu a archivuje celé repo. **Regrese → korekce (archivace).**

2. **65denní pauza** (6. 4. – 6. 6.): Žádný git commit. Riziko: ztráta momentum. **Mitigováno:** autor pracoval lokálně a vrátil se s 22 verzemi parseru.

3. **ACI color chaos**: 4× duplicitní nekonzistentní mapy napříč repy. **Root cause:** organizační, ne technický. **Řešení:** dedikovaný pip balíček + validation gate.

4. **Vcf-compiler není produkčně ready**: Modul D (35 000 Kč) zrušen z B2B nabídky. **Rozhodnutí:** upřímné — kompilátor je výzkumný bonus, ne modul.


## Závěr: Trajektorie za 101 dní

### Odkud kam

| Metrika | Bod 0 (24. 3.) | Současnost (3. 7.) |
| - | - | - |
| Repozitáře | 0 | 12 (5 aktivních) |
| Commitů | 0 | ~494 |
| Testy | 0 | 147+ (golden master + unit + smoke + CI) |
| CI/CD | 0 | Matrix 3.10/3.11/3.12 + nightly + CodeQL + Dependabot |
| Architektura | Žádná | Cross-repo dispatch, pip balíčky, OOP |
| B2B | 0 | Nabídka 70 000 Kč odeslána |
| AI modely | 1 (Gemini) | 5 (DeepSeek, Gemini, Claude, Groq, ChatGPT) |
| Kvalita ověření | 0 | Golden master + roundtrip + SNR kalibrace |


### Nejvýznamnější milníky

| Datum | Milník | Dopad |
| - | - | - |
| 24. 3. | První git commit | Vstup do formalizace |
| 25. 3. | Gemini case study | Základ epistemiky |
| 7. 6. | DXF Geometry Indexer | První produkční kód |
| 9. 6. | VCF RE backlog (v1-v20) | Externalizace tacitní znalosti |
| 11. 6. | vcf\_parser\_b2b | Přechod z R&D do produktu |
| 14. 6. | DEFECT\_CATALOG V1 | Tacitní → explicitní pravidla |
| 15. 6. | GCP deployment | Cloud production |
| 25. 6. | B2B-Knowledge-Base | Centralizace knowledge |
| 27. 6. | Vcf-compiler | Syntéza (čtení + psaní) |
| 2. 7. | vcf\_color\_service | Single source of truth |
| 3. 7. | CI/CD Tier 1 | Infrastrukturní zralost |


### Signatura autora

Ondřej Soušek není "člověk, který se naučil programovat". Je to **systémový stavitel**, který použil programování jako nástroj k externalizaci tacitních znalostí z CNC výroby do explicitního, testovatelného, nasaditelného kódu. Jeho trajektorie není "junior → senior" — je to **tacitní expert → formalizující architekt**.

Rychlost adopce (101 dní od 0 do CI/CD pipeline s cross-repo architekturou) není anomálie — je to přímý důsledek:

1. Hluboké doménové znalosti (CNC/CAM)

2. Systematické metodologie (epistemický rámec)

3. Efektivního využití AI jako force multiplier

4. Vysoké tolerance k hloubce a nízké tolerance k šumu


*Report vytvořen: 2026-07-03* *Zdroje: git log 12 repozitářů (494 commitů), .ai\_guardrails.json, .ai\_state.json, CONTEXT\_REPOS.md, KB/*, B2B-Knowledge-Base/\* *Metodika: fázová analýza + kognitivní pattern matching + kvantitativní trendy*

