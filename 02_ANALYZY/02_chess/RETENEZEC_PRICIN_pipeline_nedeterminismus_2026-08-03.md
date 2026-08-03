# RETEZEC_PRICIN_pipeline_nedeterminismus_2026-08-03
**Datum:** 2026-08-03 | **Autor:** outpost2026
**Ucel:** Podrobn vysvetleni mechanismu, jak commit 4a55f1f zmenil deterministickou pipeline na nedeterministickou — pro junior dev, bez black box
**Verze:** 1.0

---

## 1. Shrnuti (co se stalo)

Partie `CpEDieiZ` produkovala v coaching reportu false-positive: tah `Qh4` byl klasifikovan jako **1053 cp blunder** (ztrata 10.5 pionu). Realita: `Qh4` je TOP tah dle nezavisleho Stockfish hodnoceni (+259..+423 cp = bily vyhrava).

**Korenova pricina:** Commit `4a55f1f` (30.07.2026 16:38) zmenil funkci `evaluate_move` z pouzivani **sdilene engine** (deterministicka) na **lokalni engine per call** (nedeterministicky). Tim se rozbita deterministicka vrstva cele pipeline.

---

## 2. Zaklady: Jak Stockfish funguje (pro junior dev)

### 2.1 Co je Stockfish

Stockfish je sachovy engine — program, ktery na dane sachovnici (FEN) spocita nejlepsi tah. Komunikuje pres protokol **UCI** (Universal Chess Interface): posles pozici, engine odpovi nejlepsim tahem a evaluci.

### 2.2 Transposition Table (TT) = Hash tabulka

**Klicovy koncept:** Stockfish pouziva interni tabulku zvanou **Transposition Table** (TT), v nasi konfiguraci **512 MB**. TT je pamet, kde si engine uklada vysledky uz vypocitanych pozic.

**Proc je TT kriticke:** Sachove pozice se casto opakuji (napr. po tahu a protitahu se vracime do podobne pozice). Kdyz engine zna evaluci pozice X, muze ji znovu pouzit misto prepoctu. TT = pametova cache.

**Dulezite:** TT je **zavisla na historii** — cim vice pozic engine spocital, tim vice jich ma v TT, tim je presnejsi a konzistentnejsi. Prazdna TT = engine zacina od nuly = muze se vydat jinou cestou vyhodnocovani.

### 2.3 Threads (vlakna)

Stockfish pouziva **6 vlaken** (v nasi konfiguraci). Kazde vlakno muze prohledavat jinou cast stromu. Vlakna sdileji TT — vysledky jednoho vlakna jsou dostupne druhemu. To zvysuje kvalitu vyhledavani.

### 2.4 Determinismus vs Nedeterminismus

**Determinismus:** Stejny vstup → stejny vystup. Kdyz dvakrat zadas stejnou pozici se stejnou TT, dostanes stejny best_move a stejnou evaluci.

**Nedeterminismus:** Stejny vstup → ruzne vystupy. Kdyz je TT prazdna nebo rozdilna, engine muze prohledat jinou cast stromu a najit jiny best_move.

---

## 3. Stara architektura (PRED commitem 4a55f1f) —Deterministicka

### 3.1 Jak fungoval `evaluate_move` (stara verze)

```python
# STARA VERZE (pred 4a55f1f) — engine_client.py
def evaluate_move(fen: str, move_uci: str, depth: int = 0) -> dict:
    engine = get_engine()           # ← SDILENA engine (singleton)
    board = chess.Board(fen)
    move = chess.Move.from_uci(move_uci)

    _acquire_analysis_lock()        # ← MUTEX (zamek)
    try:
        # ... analyza tahu ...
    finally:
        _analysis_lock.release()    # ← UVOLNI zamek
```

**Kliceove prvky:**

1. **`get_engine()`** — vraci **jednu sdilenou instanci** Stockfish (globalni singleton). Tato instance bezi cely zivot aplikace. Ma **plnou TT** (512 MB historie).

2. **`_acquire_analysis_lock()`** — mutex (zamek). Zajistuje, ze **jen jedno vlakno** pristupuje k engine soucasne. Bez zamku by vlakna mohla kazit stav engine (UCI state leakage).

3. **`_analysis_lock.release()`** — po dokonceni analyzy uvolni zamek.

### 3.2 Proc to bylo deterministicky

Kdyz jsi zavolal `evaluate_move` na FEN `r4rk1/...` s `depth=14`:

1. Dostal jsi **stejnou engine** (ta sama instance)
2. Engine mela **stejnou TT** (512 MB historie z predchozich analyz)
3. Vlakna sdilela vysledky pres TT
4. **Vysledek:** Stejny FEN → stejny best_move → stejna evaluce → stejny cp_loss

**Analogie:** Je to jako kdyz pouzivas kalkulacku, ktera si pamatuje predchozi vypocty. Kdyz spocitas 2+2, kalkulacka si to pamatuje. Priste das 2+2 znovu a dostanes stejnou odpoved.

---

## 4. Commit 4a55f1f — Co se zmenilo a proc

### 4.1 Proc byla zmena potreba

Commit message rika:
```
Root cause: evaluate_move hung when move_uci was syntactically valid
but not legal for the position (e.g., black move g8f6 on white's turn).
engine.analyse() received a nonsensical board state and hung.

Fixes:
2. engine_client: evaluate_move creates local engine per call (singleton
   caused 2nd-call hang on Windows python-chess due to UPI state leakage)
```

**Problem:** Na Windows zpusoboval sdileny engine **zaseknuti** (hang) pri druhem volani. Duvod: python-chess UCI state leakage — engine si pamatoval spatny stav z predchoziho volani.

**Reseni v commitu:** Misto sdilene engine vytvarit **novy lokalni engine** pro kazde volani.

### 4.2 Presna diff (co se zmenilo v kodu)

```diff
 def evaluate_move(fen: str, move_uci: str, depth: int = 0) -> dict:
     if depth == 0:
         depth = DEPTH_DEFAULTS["standard"]["position"]
-    engine = get_engine()                    # ← SDILENA engine
+
+    sf_path = _get_sf_path()
     board = chess.Board(fen)
     move = chess.Move.from_uci(move_uci)
 
-    _acquire_analysis_lock()                 # ← MUTEX
+    if move not in board.legal_moves:        # ← NOVY: legal-move guard
+        return {...}
+
+    engine = chess.engine.SimpleEngine.popen_uci(sf_path)  # ← NOVY: LOKALNI engine
+    engine.configure({"Threads": 6, "Hash": 512, ...})
     try:
         # ... analyza ...
     finally:
-        _analysis_lock.release()             # ← UVOLNI zamek
+        engine.quit()                        # ← NOVY: ZNIC lokalni engine
```

### 4.3 Co presne se stalo (mechanicke)

| Pred (stara verze) | Po (nova verze) | Dopad |
|---------------------|-----------------|-------|
| `get_engine()` → sdilena instance | `popen_uci()` → nova instance | **Kazde volani = novy proces Stockfish** |
| `_acquire_analysis_lock()` → mutex | Zadny lock | **Vice vlaken muze soubezne** (ale my jen jedno volame) |
| TT = 512 MB historie | TT = **prazdna** (nove engine) | **Zadna pamat predchozich vypoctu** |
| `engine.quit()` na konci | `engine.quit()` na konci | Stejne — engine se znici |

---

## 5. Nova architektura (PO commitu 4a55f1f) — Nedeterministicka

### 5.1 Jak funguje `evaluate_move` (nova verze)

```python
# NOVA VERZE (po 4a55f1f) — engine_client.py:180-255
def evaluate_move(fen: str, move_uci: str, depth: int = 0) -> dict:
    # ... validace ...
    
    sf_path = _get_sf_path()
    engine = chess.engine.SimpleEngine.popen_uci(sf_path)  # NOVY engine
    engine.configure({"Threads": 6, "Hash": 512, ...})
    try:
        # analyza: 3x engine.analyse() na stejne FEN
        info_before = engine.analyse(board, Limit(depth=depth))
        # ... best_move, actual_move ...
    finally:
        engine.quit()  # ZNIC engine
```

### 5.2 Proc je to nedeterministicky

**Kazde volani `evaluate_move` spousti uplne novy Stockfish proces.** Tento proces:

1. **Ma prazdnou TT** — zadna historie z predchozich vypoctu
2. **Zacina od nuly** — musi prohledat cely strom od zacatku
3. **Vlakna nemaji historii** — kazde vlakno zacina s prazdny buffer

**Analogie:** Je to jako bys mel kalkulacku, kterou **po kazdem vypoctu resetnes**. Kdyz spocitas 2+2, kalkulacka zapomene. Priste das 2+2 a musis doufat, ze vypocet dopadne stejne. Ale kalkulacka muze mit jinou pociatecni hodnotu nebo jinou sekvenci operaci.

### 5.3 Mechanismus nedeterminismu (detailni)

Stockfish pouziva **stochasticke vyhledavani** (nahodne volby v algoritmu). Kdyz neni TT:

1. **Root move ordering** — engine radci tahy podle interni heuristiky. Bez TT muze poradi tahovat jine.
2. **Lazy SMP** — vice vlaken prohledava ruzne casti stromu. Bez TT nemaji sdilene vysledky = kazde vlakno jde jinou cestou.
3. **Aspiration windows** — engine pouziva uhodnutou evaluci jako startovni bod. Bez TT muze zacit s jinym odhadem.

**Vysledek:** Stejny FEN + depth=14 → muze dat rozdilne best_move a rozdilnou evaluci.

---

## 6. Dva zdroje pravdy — Proc se navzajem protireci

### 6.1 Zdroj 1: `evaluate_move` (klasifikace tahu)

- **Soubor:** `game_analyzer.py:329`
- **Ucel:** Klasifikovat kazdy tah hrace jako best/good/inaccuracy/mistake/blunder
- **Engine:** Lokalni, per-call (`popen_uci`) — **NEDETERMINISTICKY**
- **Vystup:** `centipawn_loss` (ztrata v centipawnach)

```python
# game_analyzer.py:329
eval_result = engine_client.evaluate_move(fen_before, move.uci(), depth=depth)
cp_loss = eval_result["centipawn_loss"]  # ← TOTO urcuje klasifikaci
```

**Jak spocita cp_loss:**
```python
# engine_client.py:245-248
cp_loss = max(0, best_player - actual_player)
```
- `best_player` = evaluce tahu, kterym by engine hral (jeho best_move)
- `actual_player` = evaluce tahu, kterym hral hrac
- Rozdil = ztrata

### 6.2 Zdroj 2: `analyze_position` (BlunderFactSheet)

- **Soubor:** `game_analyzer.py:376`
- **Ucel:** Poskytnout top 3 tahy (multipv=3) pro BlunderFactSheet — co mel hrac udelat
- **Engine:** Sdilena (`get_engine()` + lock) — **DETERMINISTICKY**
- **Vystup:** Seznam 3 nejlepsich tahu s evaluaci

```python
# game_analyzer.py:376
engine_lines_raw = engine_client.analyze_position(
    fen_before, depth=depth, multipv=3
)
```

### 6.3 Proc se protireci

| | evaluate_move (klasifikace) | analyze_position (BFS) |
|---|---|---|
| Engine | Lokalni, per-call | Sdilena, persistentni |
| TT | Prazdna | 512 MB historie |
| Determinismus | NE | ANO |
| Best_move | Muze byt jine | Konzistentni |

**Kdyz `evaluate_move` rekne "best_move = f2c2" a `analyze_position` rekne "best_move = Qh4", mas dva rozporne zdroje pravdy pro stejnou pozici.**

### 6.4 Pripad CpEDieiZ

```
FEN: r4rk1/1p3pbp/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w - - 2 23

evaluate_move (lokalni engine, nedeterministicky):
  best_move = f2c2 (Qf2-c2)
  cp_loss Qh4 = 1053 (v jednom behu), 716 (druhy beh), 533 (treti beh)
  → Klasifikace: BLUNDER

analyze_position (sdilena engine, deterministicky):
  rank 1: Qh4 (+259 cp)  ← TOP TAH
  rank 2: Qh4 (+400 cp)
  rank 3: Qh4 (+341 cp)
  → Qh4 je NEJLEPSI tah
```

**Tah Qh4 je zaroven BLUNDER (dle evaluate_move) i TOP TAH (dle analyze_position).** Toto je logicky nemozne — jeden tah nemoze byt zaroven nejhorsi i nejlepsi.

---

## 7. Retazec pricin (od commitu po halucinaci)

```
1. COMMIT 4a55f1f (30.07.2026 16:38)
   └─ evaluate_move: get_engine() → popen_uci()
      └─ Kazde volani = novy Stockfish proces
         └─ Prazdna Transposition Table (TT)
            └─ Nedeterminismus v best_move a evaluci

2. CACHE GENERACE (02.08.2026 23:39)
   └─ analyze_pgn zavola evaluate_move na ply 45 Qh4
      └─ Novy engine (prazdna TT) → best_move=f2c2, cp_loss=1053
         └─ Ulozeno do CpEDieiZ_white_d14.json
            └─ CHYBA ZAMRZNUTA v cache

3. COACHING REPORT (03.08.2026)
   └─ LLM dostava cache data jako kontext
      └─ BlunderFactSheet: Qh4 = blunder 1053cp
         ├─ evaluate_move reklo: Qh4 = blunder (z cache)
         └─ analyze_position reklo: Qh4 = TOP tah
            └─ ROZPOR v datech
               └─ LLM interpretuje rozpor
                  ├─ Opisuje: "Qh4 = blunder 1053cp" (z cache)
                  └─ Konfabuluje: "visici dama" (nepravda — neni v engine_lines)
                     └─ VYSLEDEK: False-positive blunder + halucinace
```

---

## 8. Cache a zamrznuti chyby

### 8.1 Jak cache funguje

```python
# game_analyzer.py:80-94
def _cache_path(game_id, depth, color):
    return f"{game_id}_{color}_d{depth}.json"

def _save_cached_analysis(game_id, depth, analysis):
    # Ulozi celou analyzu do JSON
```

Cache je **JSON soubor** s kompletni analyzi partie. Obsahuje:
- Seznam vsech tahu s evaluaci
- Klasifikaci (best/good/inaccuracy/mistake/blunder)
- BlunderFactSheet (detailni analyze chyb)
- Engine lines (multipv=3)

### 8.2 Proc je cache problem

Kdyz je v cache **zamrznuta chyba** (1053cp blunder), a LLM pozdeji cte tuto cache, bere tato data jako pravdu. Cache nema "zivotnost" — nema expiraci ani validaci.

**Analogie:** Je to jako bys mel ucebnici s chybnou informaci. Kdyz se z ni ucis, budes opakovat chybu. A kdyz tu ucebnici das dalsimu studentovi (LLM), bude ji taky opakovat.

---

## 9. LLM interpretace na rozporovych datech

### 9.1 Co LLM dostava

LLM dostava jako kontext:
1. Cache data (Qh4 = blunder, 1053cp, best_move=f2c2)
2. Engine lines z BlunderFactSheet (Qh4 = rank 1, +259cp)
3. Partii (1-0, bily vyhrava)

### 9.2 Jak LLM interpretuje

Degradovany model (free tier, 503 timeout) neni schopen:
- Kritickeho zhodnoceni rozporu
- Overeni dat oproti board state
- Oddeleni dat od narrativu

**Vysledek:**
- Opisuje cache data bez kontroly ("Qh4 = blunder 1053cp")
- Pridava narativ ktery neni dolozitelny ("visici dama")
- Spleje dva rozdilne ply do jednoho popisu

### 9.3 Proc "visici dama" neni pravda

Board state pred Qh4:
```
r4rk1/1p3pbp/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w
```

- Dama na f2 neni ohrozena zadnym cernym kusem
- Po tahu Qh4 neni dama na h4 ohrozena (cerno ma damu na a5, ale ta nema linii na h4)
- Engine lines ukazuji Qh4 jako rank 1 — engine by hral stejne

**"Visici dama" je czista halucinace** — neni podlozena daty.

---

## 10. Klicove pojmy (ontologie pro junior dev)

| Pojem | Definice |
|-------|----------|
| **Stockfish** | Sachovy engine, pocita nejlepsi tah na dane pozici |
| **UCI** | Universal Chess Interface — protokol pro komunikaci s engine |
| **FEN** | Forsyth-Edwards Notation — zapis sachovnice textovym retezcem |
| **Transposition Table (TT)** | Interni cache Stockfishe — pamatuje si vysledky uz vypocitanych pozic |
| **Hash** | Velikost TT v MB (u nas 512) |
| **Threads** | Pocet vlaken pro paralelni vyhledavani (u nas 6) |
| **Depth** | Hloubka prohledavani (u nas 14 pro single game) |
| **Centipawn (cp)** | Jednotka evaluce — 100 cp = 1 pion |
| **cp_loss** | Ztrata v centipavech oproti nejlepsimu tahu |
| **multipv** | Pocet top tahu ktere engine vraci (u nas 3) |
| **Best move** | Tah engine doporuceny jako nejlepsi |
| **Ply** | Polotah (jeden tah jednoho hrace) |
| **Singleton** | Design pattern — jedna instance na celou aplikaci |
| **Mutex (lock)** | Synchronizacni prvek — umoznuje pristup k prostredku jen jednomu vlaknu |
| **Nedeterminismus** | Stejny vstup muze dat rozdilny vystup |
| **Determinismus** | Stejny vstup = stejny vystup |
| **Cache** | Uloziste dat pro opakovane pouziti |
| **Halucinace (LLM)** | Model generuje informace ktere nejsou podlozene daty |
| **Konfabulace** | Aktivni vymysleni informaci na zaklade rozporovych dat |

---

## 11. LLM Machine-Readable Summary

```json
{
  "report_type": "pipeline_root_cause_analysis",
  "game_id": "CpEDieiZ",
  "date": "2026-08-03",
  "defects": [
    {
      "id": "D1",
      "name": "per_call_engine_nondeterminism",
      "file": "engine_client.py",
      "line": 205,
      "commit": "4a55f1f",
      "severity": "P0",
      "mechanism": "evaluate_move uses popen_uci() creating new Stockfish process per call with empty Transposition Table",
      "effect": "Same FEN produces different best_move and cp_loss across runs (spread 533-1149 cp)",
      "fix": "Reuse shared get_engine() with analysis_lock"
    },
    {
      "id": "D2",
      "name": "dual_truth_sources",
      "file": "game_analyzer.py",
      "line": "329,376",
      "severity": "P0",
      "mechanism": "evaluate_move (nondeterministic) used for classification, analyze_position (deterministic) used for BFS",
      "effect": "Same move can be classified as blunder AND as top move simultaneously",
      "fix": "Single truth source: use analyze_position/multipv for both classification and BFS"
    },
    {
      "id": "D3",
      "name": "cp_loss_formula_spread",
      "file": "engine_client.py",
      "line": "245-248",
      "severity": "P1",
      "mechanism": "cp_loss = max(0, best_player - actual_player) in high-variance space",
      "effect": "Winning positions can show 1000+ cp loss",
      "fix": "Normalize cp_loss with confidence interval from run variance"
    },
    {
      "id": "D4",
      "name": "missing_sanity_check",
      "file": "game_analyzer.py",
      "line": "N/A (missing)",
      "severity": "P1",
      "mechanism": "No correlation check between win result and 'hanging piece' claim",
      "effect": "Blunder in winning position passes without warning",
      "fix": "Add canary: win result + hanging major piece = flag"
    }
  ],
  "cache_artifact": {
    "file": "CpEDieiZ_white_d14.json",
    "created": "2026-08-02T23:39:00",
    "frozen_error": {
      "ply": 45,
      "move": "Qh4",
      "cp_loss": 1053,
      "best_move_uci": "f2c2",
      "classification": "blunder"
    }
  },
  "llm_degradation": {
    "model": "opencode/deepseek-v4-flash-free",
    "evidence": [
      "503 The request queue is full at 08:15:17",
      "503 The request queue is full at 08:42:13"
    ],
    "symptoms": ["language mixing", "hallucinated tokens", "grammatical collapse"],
    "root_cause": "Free tier rate limiting + context overflow without compaction"
  },
  "chain_of_causation": [
    "1. Commit 4a55f1f: get_engine() -> popen_uci() in evaluate_move",
    "2. Per-call engine = empty TT = nondeterministic best_move/cp_loss",
    "3. Cache frozen error: Qh4=1053cp blunder (one specific run)",
    "4. LLM receives contradictory data: blunder (cache) vs top move (analyze_position)",
    "5. Degraded model cannot critically evaluate contradiction",
    "6. LLM fabricates narrative: 'hanging queen' (not in engine_lines or board state)",
    "7. Result: false-positive blunder + hallucination in coaching report"
  ]
}
```

---

## 12. Srovnani: Pred vs Po

| Aspekt | Pred 4a55f1f | Po 4a55f1f |
|--------|-------------|------------|
| Engine instance | 1 sdilena (singleton) | Novy proces per call |
| Transposition Table | 512 MB historie | Prazdna |
| Determinismus | ANO (stejny FEN = stejny vysledek) | NE (stejny FEN = rozdilne vysledky) |
| Lock | Ano (mutex) | Ne (zadny lock) |
| Best_move | Konzistentni | Variabilni mezi behy |
| cp_loss | Konzistentni | Rozptyl 533-1149 cp |
| Duvod zmeny | — | Fix hang na Windows (UPI state leakage) |
| Nezamysleny dusledek | — | Nedeterminismus = false-positive blunders |

---

## 13. Doporucene reseni

1. **D1 (P0):** Vratit sdilenou engine v `evaluate_move` — `get_engine()` + `_acquire_analysis_lock()` misto `popen_uci()`. Fix hang resit jinak (napr. periodic restart engine po N volani).

2. **D2 (P0):** Pouzit **jeden zdroj pravdy** — `analyze_position`/multipv pro klasifikaci i BFS.

3. **D3 (P1):** Pridat confidence interval ke cp_loss — spustit evaluate_move 3x a vzit median.

4. **D4 (P1):** Pridat sanity check — partii 1-0 + blunder "hanging piece" = warning.

---

*Verze: 1.0 | Datum: 2026-08-03 | Autor: outpost2026*
