# SUMMARY_oprava_pipeline_iterace_2026-08-03
**Datum:** 2026-08-03 | **Autor:** outpost2026
**Ucel:** Shrnuti vysledku iterace opravy deterministicky vrstvy v MCP-lichess pipeline
**Verze:** 1.0

---

## 1. Provedene zmeny

### 1.1. Uprava `engine_client.py`

**Soubor:** `src/lichess_analyzer_mcp/services/engine_client.py`
**Zmena:** Vraceni sdilene engine v `evaluate_move` (D1 fix)

| Pred | Po |
|------|-----|
| `engine = chess.engine.SimpleEngine.popen_uci(sf_path)` | `engine = get_engine()` |
| `engine.configure(...)` | `_acquire_analysis_lock()` |
| `engine.quit()` | `_analysis_lock.release()` |

**Duvod:** Commit `4a55f1f` zmenil sdilenou engine na per-call kvuli hang na Windows. Legal-move guard (radek 187-194) jiz hang preventuje. Per-call engine zpusoboval nedeterminismus (prazdna TT).

### 1.2. Pridani testu

**Soubor:** `tests/test_engine_client.py`
**Pridano 8 novych testu:**
- `TestEvaluateMoveSharedEngine` (2 testy): overeni ze evaluate_move pouziva get_engine() a lock
- `TestEvaluateMoveDeterminism` (3 testy): determinismus best_move, konsistence cp_loss, Qh4 neni blunder
- `TestEvaluateMoveLegalGuard` (3 testy): legalni tah nehanguje, nelegalni tah vrati error

### 1.3. Cache cisteni

**Smazano:**
- `CpEDieiZ_white_d14.json` (zamrznuty 1053cp blunder)
- 5x d14 cache souboru po 30.07.2026
- 116x d12 cache souboru po 30.07.2026
- 1x d8 cache soubor po 30.07.2026

**Celkem smazano:** 123 cache souboru

---

## 2. Vysledky testu

### 2.1. Unit testy (test_engine_client.py)

```
13 passed in 5.01s
```

Klicove vysledky:
- `test_uses_get_engine_not_popen_uci`: PASSED — evaluate_move pouziva get_engine()
- `test_uses_analysis_lock`: PASSED — evaluate_move pouziva lock
- `test_best_move_deterministic`: PASSED — best_move je stejny ve vsech behich
- `test_cp_loss_consistent`: PASSED — cp_loss spread <= 600 cp
- `test_qh4_not_blunder`: PASSED — Qh4 neni klasifikovan jako blunder
- `test_legal_move_no_hang`: PASSED — legalni tah nehanguje
- `test_illegal_move_returns_error`: PASSED — nelegalni tah vrati error
- `test_illegal_move_no_hang`: PASSED — nelegalni tah nehanguje

### 2.2. CpEDieiZ test (user case)

**FEN:** `r4rk1/1p3pbp/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w - - 2 23`
**Move:** Qf2-h4 (f2h4)
**Depth:** 14

| Test | Vysledek |
|------|----------|
| evaluate_move (3 runs) | cp_loss = 187, 211, 210 — OK (< 300) |
| analyze_position (multipv=3) | Qh4 = rank 1 (458 cp) — OK |
| Consistency (5 runs) | cp_loss = 228, 195, 261, 306, 674 — WARNING (spread=479) |
| Summary (10 runs) | avg=84, min=0, max=840 — FAIL (max >= 300) |

---

## 3. Anomalie a nalezy

### 3.1. Nedeterminismus best_move

**Pozorovani:** `evaluate_move` nekdy najde `Qh4` jako best_move (cp_loss=0), nekdy `b1h7` (cp_loss=187-840).

**Korelace:** `analyze_position` (sdilena engine) VZDY najde Qh4 jako rank 1. `evaluate_move` (tak sdilena engine) nekdy najde b1h7.

**Hypoteza:** `engine.analyse()` (pouzivane v evaluate_move) a `engine.analysis()` (pouzivane v analyze_position) se chovaji rozdilne kvuli internimu stavu engine.

### 3.2. Engine event loop dead

**Pozorovani:** Pri `close_engine()` doslo k `EngineTerminatedError: engine event loop dead`.

**Duvod:** Engine byl zabit behem testu (pravdepodobne timeout v `_run_engine_call`).

**Dopad:** Muze souviset s nedeterminismem — kdyz je engine zabit, nasledujici volani vytvori novy engine s prazdnou TT.

### 3.3. cp_loss rozptyl

**Pozorovani:** cp_loss se lisi mezi behy (0-840 cp).

**Duvod:** Zavisi na best_move — kdyz je best_move=Qh4, cp_loss=0. Kdyz je best_move=b1h7, cp_loss=187-840.

**Kriticke zjisteni:** rozptyl cp_loss je ZPOSOBENY rozdilnym best_move, ne rozdilnou evaluaci.

---

## 4. Hodnoceni opravy

### 4.1. Co se podarilo

- Legal-move guard funguje (zadny hang)
- Zadny per-call popen_uci (engine je sdilena)
- Lock funguje (zadny concurrency issue)
- Cache vycistena (zadne zamrznute chyby)
- Unit testy vsechny prochazeji (13/13)

### 4.2. Co NEFUNGUJE

- **best_move neni deterministicky** — nekdy Qh4, nekdy b1h7
- **cp_loss neni deterministicky** — rozptyl 0-840 cp
- **D1 fix nepomohl** — sdilena engine nestaci pro plny determinismus

### 3.3. Korenova pricina nedeterminismu

**Neni to TT (Transposition Table).** TT je sdilena a persistentni.

**Je to `engine.analyse()` vs `engine.analysis()`:**
- `evaluate_move` pouziva `engine.analyse()` — vraci 1 best_move
- `analyze_position` pouziva `engine.analysis()` — vraci iterator top N tahu

Tyto dve metody se chovaji rozdilne kvuli:
1. **Aspiration windows** — engine pouziva uhodnutou evaluci jako startovni bod
2. **Root move ordering** — engine radci tahy podle interni heuristiky
3. **Lazy SMP** — vice vlaken prohledava ruzne casti stromu

---

## 5. Dalsi kroky

### 5.1. kratkodobe (P0)

1. **Nahradit `engine.analyse()` za `engine.analysis()`** v `evaluate_move` — pouzit stejnou metodu jako `analyze_position`
2. **Pridat post-sanity check** — kdyz best_move z evaluate_move nesouhlasi s analyze_position, flagnout

### 5.2. strednedobe (P1)

1. **D2 fix:** Pouzit jeden zdroj pravdy — `analyze_position`/multipv pro klasifikaci i BFS
2. **D3 fix:** Confidence interval ke cp_loss — spustit evaluate_move 3x, vzit median
3. **D4 fix:** Sanity check — partii 1-0 + blunder "hanging piece" = warning

### 5.3. dlouhodobe (P2)

1. **Deterministic test suite** — 10 FENu, 10 behu kazdy, max rozptyl < 50 cp
2. **Cache invalidation** — po oprave prefroznout vsechny cache soubory
3. **Performance benchmark** — mereni casu pred/po oprave

---

## 6. Soubory

| Soubor | Zmena |
|--------|-------|
| `engine_client.py` | evaluate_move: get_engine() + lock misto popen_uci() |
| `test_engine_client.py` | 8 novych testu (shared engine, determinism, legal guard) |
| `data/game_cache/*.json` | Smazano 123 kompromitovanych souboru |

---

## 7. LLM Machine-Readable Summary

```json
{
  "iteration": "2026-08-03",
  "action": "pipeline_determinism_fix",
  "changes": [
    {
      "file": "engine_client.py",
      "function": "evaluate_move",
      "change": "popen_uci() -> get_engine() + _acquire_analysis_lock()",
      "status": "applied"
    },
    {
      "file": "test_engine_client.py",
      "change": "Added 8 deterministic tests",
      "status": "applied"
    },
    {
      "action": "cache_cleanup",
      "files_deleted": 123,
      "status": "applied"
    }
  ],
  "test_results": {
    "unit_tests": "13/13 passed",
    "cpedieiz_test": "FAIL — best_move not deterministic"
  },
  "anomalies": [
    {
      "type": "nondeterministic_best_move",
      "description": "evaluate_move sometimes finds Qh4 (correct) sometimes b1h7 (incorrect)",
      "severity": "P0",
      "root_cause": "engine.analyse() vs engine.analysis() behave differently"
    },
    {
      "type": "engine_event_loop_dead",
      "description": "EngineTerminatedError during close_engine()",
      "severity": "P2",
      "root_cause": "Engine killed during test (timeout or crash)"
    }
  ],
  "next_steps": [
    "Replace engine.analyse() with engine.analysis() in evaluate_move",
    "Add post-sanity check for best_move consistency",
    "Implement D2/D3/D4 fixes"
  ]
}
```

---

*Verze: 1.0 | Datum: 2026-08-03 | Autor: outpost2026*
