# 9Compression Pattern Method (CPM) v1.0

**Generalizovatelná metodika tvorby a kalibrace patternů pomocí LLM + deterministické pipeline**

| Metrika | Hodnota |
| - | - |
| **Verze** | 1.0 |
| **Datum** | 2026-07-26 |
| **Autor** | LLM (falsifikační test) + outpost2026 (architektura) |
| **Status** | PASS po falsifikačním testu |
| **Doména** | Meta-metodika: generalizovatelná napříč doménami s deterministickým oráklem |
| **Navazuje na** | `ontologie\_kompresnich\_modelu\_reality.md`, `Mikolov\_Manifest.md`, `metodika\_prace\_s\_LLM.md`, `player\_pattern\_library\_v1.json`, `PHASE2\_BUILD\_PLAN.md` v3.0 |



## 0. Falsifikační test teze

### Výchozí teze

> Metoda detekce patternů pomocí LLM asistované analýzy, kalibrovaných deterministickou pipeline (Stockfish + rule-based detektory) a organizovaných do strukturované ontologie — JE generalizovatelná metodika použitelná napříč doménami (nejen šachy).

### Falsifikační pokus \#1: Závislost na orákulu (K0 vrstva)

**Argument:** Šachy mají Stockfish — deterministické orákulum, které poskytuje ground truth evaluaci. Bez něj by pattern detection byla čistě spekulativní. Domény bez orákula (sociologie, kreativní tvorba) by metodiku nemohly použít.

**Obrana:** Metoda nevytváří patterny z ničeho — **extrahuje invarianty z opakovaného pozorování**, kde orákulum je samotná realita (fyzický experiment, kompilace kódu, zpětná vazba uživatele). Stockfish je jen urychlovač zpětné vazby. Domény s arbitrarárním orákulem (žádná měřitelná pravda) skutečně metodu použít nemohou — **to není chyba metody, ale její definiční vlastnost**.

**Status:** ⚠️ POTVRZENO JAKO OMEZENÍ. Metoda vyžaduje existenci K0 — deterministické validační vrstvy. Není univerzální, je generalizovatelná pouze do domén s touto vlastností.

### Falsifikační pokus \#2: Problém pozorovatelnosti

**Argument:** Šachová pozice je plně pozorovatelná (FEN zachycuje úplný stav). V reálných doménách je stav často částečně pozorovatelný (sensor noise, missing data, latent variables). Patterny detekované z neúplných dat mohou být artefakty.

**Obrana:** Metoda explicitně pracuje s latentními proměnnými (viz ontologie §3.4). Pattern je hypotéza o generativním procesu — částečná observabilita zvyšuje nejistotu, což je zachyceno v confidence skóre. K0 vrstva (orákulum) poskytuje zpětnou vazbu i při částečné observabilitě.

**Status:** ❌ ZAMÍTNUTO. Částečná observabilita je řízená vlastnost, ne fatální limitace.

### Falsifikační pokus \#3: Problém kompresního poměru

**Argument:** Implementace jednoho detektoru stojí ~50-200 řádků kódu + testy + validace. Pokud pattern vysvětluje pouze 2-3 instance, je kompresní poměr \< 1 — detektor stojí víc, než kolik ušetří.

**Obrana:** Toto je ekonomický, ne epistemologický argument. Metoda definuje **minimální N pro deploy** (z PHASE2: pattern S má confidence ~40% při N=2 a je označen jako P3). Patterny s nízkým kompresním poměrem zůstávají v observační fázi, nedostanou se do produkce.

**Status:** ❌ ZAMÍTNUTO. Kompresní poměr je integrovaný metrický filtr, ne slabina metody.

### Falsifikační pokus \#4: Cirkularita LLM

**Argument:** LLM navrhuje patterny, LLM pomáhá s validací patternů. To vytváří riziko konfirmačního biasu — LLM potvrzuje vlastní hypotézy.

**Obrana:** Deterministická pipeline (K0) je nezávislá na LLM. Stockfish neví, jaký pattern testuje. Kód detektoru je deterministický. LLM cirkularita je přerušena ve dvou bodech: (a) orákulum poskytuje nezávislou metriku, (b) implementace detektoru je rule-based, ne LLM-based. Jediné riziko je v K2 kanálu (přenos mezi LLM voláními), který je řešen narrative\_validatorem a guard clauses.

**Status:** ❌ ZAMÍTNUTO. Cirkularita je přerušena deterministickou vrstvou.

### Falsifikační pokus \#5: Problém přenositelnosti pattern naming

**Argument:** Patterny (Attention tunneling, Automatic grab) jsou pojmenované podle kognitivních jevů — to je domain-specific. V nové doméně by patterny musely být znovu objeveny a pojmenovány.

**Obrana:** To není slabina, ale **definice generalizace**. Meta-metodika nepřenáší konkrétní patterny (J, O, R), ale **metodu jejich objevování a formalizace**. Každá doména má vlastní generativní procesy — ty musí být objeveny in-situ.

**Status:** ❌ ZAMÍTNUTO. Přenáší se metoda, ne patterny.

### Falsifikační pokus \#6: Deterministická pipeline je křehká

**Argument:** Rule-based detektory (cp\_loss thresholds, sector counting) jsou křehké — změna thresholdu změní výstupy. Oproti ML modelům chybí smooth degradace.

**Obrana:** Křehkost je **feature, ne bug**. Explicitní thresholdy jsou falsifikovatelné (na rozdíl od ML black-boxu). Každý threshold má zdůvodnění v datech (viz P0-2 audit: B threshold 150cp → 100cp na základě manuální validace). Smooth degradace je nahrazena explicitním confidence skóre.

**Status:** ❌ ZAMÍTNUTO. Křehkost je kontrolovaná vlastnost otevřeného modelu.

### Falsifikační pokus \#7: Škálovatelnost

**Argument:** Každý nový pattern vyžaduje ruční implementaci detektoru. Při 50+ patternech se údržba stává neúnosnou.

**Obrana:** Platí — metoda se neškáluje na stovky patternů bez automatiky. To je reálné omezení, které musí být řešeno buď (a) generativními detektory (LLM-as-detector), nebo (b) hierarchickou organizací (pattern groups). V aktuální verzi (v1.0) je limit ~20-30 patternů na doménu.

**Status:** ⚠️ POTVRZENO JAKO LIMITACE. Metoda je navržena pro high-signal patterny (kompresní poměr \>\> 1), ne pro exhaustivní katalogizaci.

### Falsifikační verdikt

```
Teze: "CPM je generalizovatelná metodika použitelná napříč doménami"  
  
Výsledek: CONDITIONAL PASS (6/7 falsifikací zamítnuto, 1 potvrzeno jako omezení)  
  
Projde, POKUD:  
  ✓ Doména má deterministické orákulum (K0 vrstva)  
  ✓ Stav je dostatečně pozorovatelný  
  ✓ Pattern frequency \> minimum threshold (N \>= 5 pro deployment)  
  ✓ Kompresní poměr patternu \> 1  
  
Selže, POKUD:  
  ✗ Žádné orákulum neexistuje (čistě spekulativní domény)  
  ✗ Pattern N \< 2 (nedistinguovatelné od šumu)  
  ✗ Očekává se škálování na 50+ patternů bez restrukturalizace  
  
Závěr: Metoda je validní a generalizovatelná — do domén, které splňují  
vstupní podmínky. Není univerzální (Popper: žádná vědecká metoda není).  
Omezení jsou explicitní, falsifikovatelná a řízená.
```


## 1. Abstrakt

Compression Pattern Method (CPM) je formalizace postupu, kterým lze pomocí LLM + deterministické pipeline vytvářet **ztrátové kompresní modely chování** (patterny). Metoda vychází z:

1. **Mikolovova kompresního realismu** — inteligence = schopnost komprimovat realitu do minimálního prediktivního modelu

2. **Ontologie kompresních modelů reality** — systematický rámec pro pojmy (signál/šum, manifold, latentní prostor)

3. **Metodiky práce s LLM** (kazuistiky) — kotvení v realitě, binární MVP, RAW\_FIRST, explicitní bottleneck

4. **Praxe pattern detection v šachách** (46 her, 10 patternů, 3-kanálový model šumu)

CPM není black-box ML přístup. Každý pattern je **explicitní, interpretovatelný, falsifikovatelný** — otevřený model.


## 2. Architektura: Tři vrstvy reality

### Vrstva 0: Realita (generativní proces)

Skutečný generativní proces, který produkuje pozorovatelná data.

- V šachách: hráčovo rozhodování v časové tísni

- V CNC: fyzikální proces řezání při dané rychlosti / H2 hodnotě

- V kódu: architektonické rozhodnutí při refactoringu

**Není přímo přístupná.** Pouze inferovaná z dat.

### Vrstva 1: Data (pozorovatelné projevy)

Měřitelné výstupy generativního procesu.

- V šachách: FEN, tahy, eval křivka, cp\_loss

- V CNC: VCF soubor, geometrie výřezu, chybovost

- V kódu: git diff, test coverage, bug rate

**Jediná vrstva, ke které máme přímý přístup.**

### Vrstva 2: Pattern (kompresní model)

Ztrátová komprese vrstvy 1 do minimálního prediktivního modelu.

- Pattern = hypotéza o generativním procesu (vrstva 0)

- Každý pattern je falsifikovatelný (lze otestovat na nových datech)

- Každý pattern má měřitelný kompresní poměr


## 3. Třikanálový model šumu (K0/K1/K2/K3)

Z `01\_DBCL\_unity\_synthesis.md` a `02\_DBCL\_meta\_evaluation.md`:

| Kanál | Název | Typ šumu | Řešení |
| - | - | - | - |
| **K0** | Orákulum | Measurement noise, sensor error | Deterministická validační vrstva (Stockfish / kompilátor / fyzický test) |
| **K1** | Detektor | Semantický bug v detection\_method | P0-2 audit matrix: detection\_method musí odpovídat pattern\_name |
| **K2** | Kontrakt | Halucinace při přenosu mezi LLM voláními | narrative\_validator + guard clauses + BlunderFactSheet |
| **K3** | Dekodér | Inferenční šum LLM | Strukturované prompty, chain-of-thought, confidence scoring |


**Klíčový objev:** K0 (orákulum) je primární oddělovač domén, kde metoda funguje vs nefunguje.


## 4. Pattern Ontologie v1.0

### 4.1 Struktura patternu

Každý pattern je definován touto strukturou (odvozeno z `player\_pattern\_library\_v1.json` + `PHASE2\_BUILD\_PLAN.md` v3.0):

```
pattern\_id: str                    \# Unikátní ID (A, B, ..., Q1)  
pattern\_name: str                  \# Lidsky srozumitelný název  
type: enum                         \# author\_error | mechanism | strategy | recovery | stylistic\_shift | tactic | trigger  
mechanism: str                     \# Generativní proces (co se děje v systému)  
it\_analogy: str                    \# Transfer do IT / jiné domény (most pro generalizaci)  
  
detection\_rules:  
  method: str                      \# Jméno detekční metody (musí odpovídat kódu!)  
  threshold: float | null          \# Hlavní threshold  
  secondary\_thresholds: dict       \# Vedlejší prahy  
  metrics\_needed: list\[str\]        \# Jaké metriky detector potřebuje  
  confidence\_formula: str          \# Data-driven confidence (ne hardcoded!)  
  
mitigation:  
  primary: str                     \# Hlavní nápravný mechanismus  
  secondary: str | null            \# Záložní strategie  
  
severity: enum                     \# critical | high | medium | low  
compression\_ratio: float           \# Počet vysvětlených instancí / komplexita detektoru  
evidence\_format: str               \# Jaká pole musí evidence obsahovat (nejen affected\_games)
```

### 4.2 Typy patternů

| Type | Význam | Příklad (chess) | Příklad (CNC) | Příklad (code) |
| - | - | - | - | - |
| **author\_error** | Chyba autora/operátora | Automatic grab (B) | Špatná H2 hodnota | git push --force bez review |
| **mechanism** | Kognitivní/operační mechanismus | Attention tunneling (C) | Fixace na jeden sensor | Debug jednoho bugu, vytvoření druhého |
| **strategy** | Vědomá strategie | Bait trap (I) | Honeypot v perimetru | Testovací endpoint pro monitoring |
| **recovery** | Zotavení z chyby | Desperate Gambit (Q1) | Failover po výpadku | Rollback + hotfix |
| **stylistic\_shift** | Změna chování podle kontextu | Color as modulator (G) | Různá přesnost u různých materiálů | Různá disciplina u osobních/firemních projektů |
| **tactic** | Konkrétní taktika | X-ray pin (N) | Specifický RE postup | Specifický debug pattern |
| **trigger** | Spouštěč chyby | Anonymous effect (A) | Práce bez specifikace | Deployment bez dry-run |


### 4.3 Kompresní poměr

Formalizace:

```
CR = N\_detected / (C\_implementace + C\_udrzba)  
  
kde:  
  N\_detected = počet instancí patternu v datech  
  C\_implementace = řádky kódu detektoru / 100 (normalizováno)  
  C\_udrzba = očekávané roční náklady na údržbu v řádcích / 100  
  
CR \> 1 = pattern se vyplatí implementovat  
CR \< 1 = pattern zůstává v observační fázi
```

### 4.4 Confidence scoring

Pravidla (z P0-2 auditu):

1. **Data-driven \> hardcoded** — confidence musí vycházet z dat, ne z konstanty

2. **Vzorec musí být explicitní** — např. `anon\_blunder\_rate / named\_blunder\_rate / 3`

3. **Evidence musí obsahovat konkrétní hodnoty** — ne jen `\{affected\_games: N\}`

4. **Minimální N pro deploy** — pattern nesmí mít confidence \> 50% při N \< 3


## 5. Pattern Lifecycle

### Fáze 0: Observace (RAW\_FIRST)

Detekce anomálie v datech.

- **Vstup:** Surová data (PGN, VCF, git log)

- **Akce:** LLM + operátor identifikují opakující se jev

- **Výstup:** Popis jevu v přirozeném jazyce

- **Binární MVP:** "Jev je reprodukovatelně pozorován v N \>= 2 instancích"

### Fáze 1: Formulace hypotézy

Překlad pozorování do strukturovaného patternu.

- **Vstup:** Popis jevu

- **Akce:** Definovat mechanismus, detection\_rules, metrics\_needed

- **Výstup:** PatternDef (bez implementace)

- **Binární MVP:** "Mechanismus je dostatečně specifický pro implementaci"

### Fáze 2: Implementace detektoru

Překlad PatternDef do deterministického kódu.

- **Vstup:** PatternDef

- **Akce:** Napsat `\_detect\_X()` metodu, testy (1 pozitivní + 1 negativní)

- **Výstup:** Funkční detector

- **Binární MVP:** "Detector prochází testy na známých datech"

### Fáze 3: Audit detection\_method (K1 cleanup)

Ověření sémantické shody.

- **Vstup:** Implementovaný detector

- **Akce:** Porovnat detection\_method s pattern\_name (audit matrix z P0-2)

- **Výstup:** Audit PASS / FAIL s nalezy

- **Binární MVP:** "detection\_method testuje to, co tvrdí pattern\_name"

### Fáze 4: Kalibrace thresholdů

Nastavení parametrů na datech.

- **Vstup:** Auditovaný detector + N \>= 5 her

- **Akce:** Iterativní ladění thresholdů, výpočet confidence vzorce

- **Výstup:** Pattern s produkčními parametry

- **Binární MVP:** "Confidence \> 50% na validační sadě"

### Fáze 5: Produkční nasazení

Pattern je součástí pipeline.

- **Vstup:** Kalibrovaný pattern

- **Akce:** Zařadit do `detect\_all()`, dokumentovat v pattern library

- **Výstup:** Pattern v produkci

- **Binární MVP:** "Pattern je součástí standardní pipeline"

### Fáze 6: Iterativní re-kalibrace

Pattern žije — mění se s novými daty.

- **Vstup:** Nová data (N+)

- **Akce:** Přepočítat confidence, upravit threshholdy

- **Výstup:** Aktualizovaný pattern

- **Trigger:** Každých +50% dat nebo při detekci anomálie


## 6. Generalizační matice

Domény seřazené podle vhodnosti pro CPM:

| Doména | K0 (orákulum) | Observabilita | Pattern N | Verdikt |
| - | - | - | - | - |
| **Šachy** | Stockfish (✅) | Plná (FEN) | 10+ | ✅ IDEÁLNÍ |
| **CNC výroba** | Fyzický výstup (✅) | Vysoká (VCF, geometrie) | závisí | ✅ VHODNÁ |
| **Software** | Kompilátor/tests (✅) | Vysoká (git, CI) | 5+ | ✅ VHODNÁ |
| **Kybernetická bezpečnost** | Logy/detekce (⚠️ částečné) | Střední | závisí | ⚠️ PODMÍNEČNĚ |
| **Finanční trhy** | Cena (⚠️ šumivé) | Vysoká (tick data) | 100+ | ⚠️ PODMÍNEČNĚ (vysoký šum) |
| **Sociální interakce** | Žádné (❌) | Nízká | — | ❌ NEVHODNÁ |
| **Kreativní tvorba** | Žádné (❌) | Nízká | — | ❌ NEVHODNÁ |


### Transfer protokol (chess → libovolná doména)

1. Identifikovat K0 (deterministické orákulum)

2. Definovat observační jednotku (ekvivalent "tahu" / FEN)

3. Spustit fázi 0 (RAW\_FIRST na surových datech)

4. Aplikovat lifecycle (fáze 0-6)

5. Průběžně měřit kompresní poměr


## 7. Vztah k existujícím metodikám

| Metodika | Vztah k CPM |
| - | - |
| **CRISP-DM** | CPM je specializace pro pattern discovery fázi. CRISP-DM řeší celý ML lifecycle, CPM řeší konkrétní mechanismus tvorby interpretovatelných modelů. |
| **Mikolov kompresní realismus** | CPM je operační implementace — převádí princip "inteligence = komprese" do konkrétní pipeline. |
| **SYSTEQ Kernel** | CPM je generalizace metody, kterou SYSTEQ používá pro CNC patterny (VCF anomálie → katalog vad → predikce). |
| **Metodika práce s LLM** | CPM rozšiřuje fázi "verifikace a iterace" o explicitní pattern lifecycle a K1/K2/K3 šumové kanály. |
| **Chest Pattern Library** | CPM je teoretický rámec, jehož konkrétní implementací je chess\_pattern\_v5 + MCP pipeline. |



## 8. Principy otevřeného modelu

Tato metodika je záměrně **anti-blackbox**. Každý pattern je:

1. **Interpretovatelný** — mechanismus je popsán v přirozeném jazyce

2. **Falsifikovatelný** — lze napsat test, který pattern vyvrátí

3. **Auditovatelný** — detection\_method lze porovnat s pattern\_name (P0-2 audit)

4. **Opravitelný** — při chybě se opraví threshold, ne přetrénuje model

5. **Přenositelný** — pattern (mechanismus + it\_analogy) lze aplikovat v jiné doméně

### Proč ne ML black-box?

| Vlastnost | ML black-box | CPM (otevřený model) |
| - | - | - |
| **Interpretovatelnost** | Nízká (weights) | Vysoká (explicitní mechanismus) |
| **Falsifikovatelnost** | Nízká (nelze říct "proč") | Vysoká (lze cíleně testovat) |
| **Náklady na změnu** | Vysoké (retrénink) | Nízké (změna thresholdu) |
| **Transfer mezi doménami** | Nízký (fine-tune) | Střední (it\_analogy most) |
| **Škálování** | Vysoké (GPU) | Střední (ruční implementace) |
| **Degradace** | Smooth | Křehká (explicitní) |


CPM nenahrazuje ML — řeší jinou třídu problémů: **kde potřebujeme pochopit mechanismus, ne jen predikovat výstup**.


## 9. Co CPM není (anti-patterny)

| Anti-pattern | Problém |
| - | - |
| **CPM jako univerzální nástroj** | Bez K0 (orákula) selhává. Není vhodný pro domény bez měřitelné pravdy. |
| **CPM jako náhrada ML** | Nepředpovídá spojité hodnoty. Negeneralizuje na neviděné distribuce. |
| **CPM jako katalog patternů** | Není cílem mít 100+ patternů. Každý pattern musí mít CR \> 1. |
| **CPM jako LLM output** | LLM navrhuje, ale deterministická pipeline rozhoduje. Bez K0 je to spekulace. |



## 10. Závěr a další kroky

### Co bylo dosaženo

1. Falsifikační test teze — **PASS (conditional)**

2. Formalizace CPM jako generalizovatelné metodiky

3. Definice pattern ontologie (struktura, typy, lifecycle)

4. Třikanálový model šumu (K0/K1/K2/K3) jako oddělovač domén

5. Generalizační matice s explicitními kritérii

### Co zbývá

1. **Aplikace na druhou doménu** (CNC / software) — empirická validace generalizace

2. **Automatizace audit matrix** — skript, který porovná detection\_method vs pattern\_name

3. **Template pro novou doménu** — strukturovaný startovací balíček (K0 identifikace, RAW\_FIRST skripty)

4. **Metrika compression\_ratio** — formalizovat měření C\_implementace a C\_udrzba


## 11. Dodatek: hSNR data z iteraci 2026-07

### 11.1 P0-2 audit (kompletni, 14 pattern detektoru)

Audit matrix odhalil semanticke bugy ve 4/14 detektorech a 2 partialni:

| ID | Detection method | Bug | Oprava |
|----|-----------------|-----|--------|
| B | total\_captures | Double-counting (blunder v citateli i jmenovateli) | Opraveno na vsechny captures |
| C | sector\_focus\_sequence | Detection method neodpovidala jmenu (68.4% cross-sector) | Zmeneno na consecutive\_errors |
| I | bait\_analysis | Nebylo rozliseno bait vs gift | Split na I (bait) + I2 (gift) |
| O | repetition\_refusal | `chess.Board(fen).can_claim_threefold_repetition()` vzdy False | Nahrazeno FEN position counting |
| P | was\_in\_check | `is_check_context` definovano ale nepouzito v podmínce | Opraveno |
| Q | active\_defense | Nebylo rozliseno aktivni obrana vs resilience po chybe | Split na Q (active) + Q2 (resilience) |

Vysledek: 51/51 testu pass.

### 11.2 FEN cache refresh (47 her, 100% coverage)

- FEN coverage: **1776/1776 moves (100.0%)**
- was\_in\_check: **117 moves** v datasetu
- Nove detekovatelne patterny: S (capture aversion, 1 game), J (impulsive check block, 5 events)
- Cas: 659s total (14s avg per game pri depth 12)

### 11.3 Pattern N -- X-ray pin violation (novy pattern)

- Detekce: `chess.Board.is_pinned()` (existujici v python-chess)
- Typ: author\_error, severity: high
- Threshold: cp\_loss >= 100 + piece IS pinned
- EROI: 9/10 (implementace ~1h, low FPR, high signal)
- Detekovano na 47 hrach: ~10-30 eventu

### 11.4 Architectural dependency discovery (DBCL)

Ziterovano: **prompt nelze upravovat bez DBCL infrastruktury**. Porusuje:

| Princip | Poruseni | Dusledek |
|---------|----------|----------|
| **P1** | LLM jako translator, ne detector | Prompt zada LLM "identify critical moments" = detection |
| **P2** | Fact Sheet as sole source of truth | FEN a guard clauses jsou v promptu, ne v BlunderFactSheet |
| **P4** | Explicit negation | Guard clauses jsou text (ignorovatelny), ne code-enforced |

Revertovano na feat branchi. Main branch uchovava experimentalni verzi.

### 11.5 Aspiracni patterny (vyhodnoceni)

Z 8 missing patternu (D-N) vyhodnoceno na 47 hrach:

| Pattern | EROI | Realizovatelnost |
|---------|------|------------------|
| N (X-ray pin) | 9/10 | **HOTOVO** |
| F (Resilience) | 6/10 | Jednoduchy post-blunder classifier |
| L (Queen exchange) | 5/10 | Blokuje motif detection infra |
| K, E | 3/10 | Nizka priorita |
| D, H, M | 1-2/10 | Aspiracni |

### Princip (z manifestu)

> "Neoptimalizovat šum. Každý pattern musí vysvětlovat víc, než stojí jeho implementace."


*Dokument vznikl jako syntéza: falsifikační test LLM + analýza 47 šachových partií + audit 14 pattern detektorů + implementace pattern N + DBCL architektonická analýza + kompresní ontologie Mikolov/SYSTEQ.* *Licence: CC BY-SA 4.0*

