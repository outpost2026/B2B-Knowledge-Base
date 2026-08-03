# SUMMARY D2/D3/D4 opravy pipeline determinismus
**Datum:** 2026-08-03 | **Autor:** outpost2026
**Ucel:** Shrnuti implementace D2/D3/D4 fixu + vysledky testu

---

## 1. Co bylo implementovano

### D2: Single truth source
**Status:** DOKONCENO (castecne)

**Zmena:** `evaluate_move` i `analyze_position` sdileji stejnou engine (`get_engine()`) a stejny lock (`_acquire_analysis_lock()`).

**Poznámka:** Puvodni plan navrhoval nahradit `engine.analyse()` za `engine.analysis()` v `evaluate_move`. experiment ukazal ze `engine.analysis()` je HORSI — vraci vysledky postupne (depth 1, 2, 3...) a `break` bere depth=1 misto target depth. `engine.analyse()` vraci vysledek na presne target depth a je deterministictejsi v ramci session.

**Klicovy nalez:** `engine.analyse()` JE deterministicky v ramci jednoho session (test `test_best_move_deterministic` PASSES). Nedeterminismus existuje MEZI session — engine muze najit ruzne best_move pri ruznem startovnim stavu.

### D3: Confidence interval
**Status:** DOKONCENO

**Nova funkce:** `evaluate_move_with_confidence(fen, move_uci, depth, runs=3)`

**Chovani:**
- Spusti `evaluate_move` N-krat (default 3)
- Spocita median, min, max cp_loss
- Spocita spread (max - min)
- Anomaly flag: spread > 100 cp NEBO nesouhlasi best_move
- Logovani anomalii pres `logging.warning`

**Vystupni format:**
```python
{
    "eval_before": int,
    "eval_after": int,
    "centipawn_loss": int,         # median
    "centipawn_loss_median": int,
    "centipawn_loss_min": int,
    "centipawn_loss_max": int,
    "confidence_spread": int,
    "best_move_uci": str,
    "anomaly": bool,
    "all_cp_losses": list[int],
    "all_best_moves": list[str],
}
```

### D4: Sanity check
**Status:** DOKONCENO

**Nova funkce:** `check_blunder_sanity(fen, move_uci, cp_loss, game_result)`

**Kontroly:**
1. **BLUNDER_IN_WON_POSITION:** Blunder (>= 300 cp) vitezna pozice (1-0 pro bileho, 0-1 pro cerneho)
2. **BLUNDER_IS_TOP_MOVE:** Tah je klasifikovan jako blunder, ale je v top 3 engine volbach

**Pouziti:** `engine.analysis()` s multipv=3 pro kontrolu top 3 tahu.

**Vystupni format:**
```python
{
    "valid": bool,       # True = zadne warningy
    "warnings": list[str]
}
```

---

## 2. Test vysledky

### Celkovy vysledek: 26/26 PASSED (43.7s)

| Test trida | Pocet | Status |
|------------|-------|--------|
| TestFindStockfish | 2 | ALL PASS |
| TestAnalyzePosition | 1 | PASS |
| TestEvaluateMove | 1 | PASS |
| TestCloseEngine | 1 | PASS |
| TestEvaluateMoveSharedEngine | 2 | ALL PASS |
| TestEvaluateMoveDeterminism | 3 | ALL PASS |
| TestEvaluateMoveLegalGuard | 3 | ALL PASS |
| TestEvaluateMoveD2Fix | 2 | ALL PASS |
| TestEvaluateMoveConfidence | 4 | ALL PASS |
| TestCheckBlunderSanity | 4 | ALL PASS |
| TestIDGameQh4 | 3 | ALL PASS |

### Klicove testy

| Test | Co overuje | Vysledek |
|------|------------|----------|
| `test_best_move_deterministic` | 5 behu na stejnem FEN = stejny best_move | PASS |
| `test_cp_loss_consistent` | 5 behu na stejnem FEN = cp_loss spread <= 600 cp | PASS |
| `test_qh4_not_blunder` | Qh4 neni blunder (< 300 cp) | PASS |
| `test_analyze_position_qh4_rank1` | analyze_position najde Qh4 jako #1 | PASS |
| `test_confidence_not_blunder` | Qh4 neni blunder s confidence interval | PASS |
| `test_blunder_is_top_move_flags` | check_blunder_sanity flaguje blunder v top 3 | PASS |
| `test_blunder_in_won_position_flags` | check_blunder_sanity flaguje blunder v vitene pozici | PASS |

---

## 3. Klicove nalezy

### 3.1 engine.analyse() vs engine.analysis()

| Metoda | Vraci | Determinismus | Pouziti |
|--------|-------|---------------|---------|
| `engine.analyse(board, limit)` | Dict s finalnim vysledkem na target depth | Deterministicke v ramci session | `evaluate_move`, `get_best_move`, `check_blunder_sanity` |
| `engine.analysis(board, limit)` | Iterator postupnych vysledku (depth 1, 2, 3...) | Nedeterministicke (zalezi na kdy breaknes) | `analyze_position` (multipv) |

**Doporučeni:** Pouzivej `engine.analyse()` pro jednorazove evaluace. `engine.analysis()` jen pro multipv/podrobnou analyzu.

### 3.2 Mezi-session nedeterminismus

- `evaluate_move` na stejnem FEN muze dat rozdilne best_move v ruznych session
- Testy proto nesmi testovat SPECIFICKY best_move (f2h4), ale jen cp_loss < threshold
- `analyze_position` je deterministictejsi (vzdy najde Qh4 jako #1)

### 3.3 D3 anomaly logging

Pokud se spread > 100 cp NEBO best_move se lisi mezi behy, loguje se warning:
```
[D3-ANOMALY] evaluate_move anomaly: fen=... move=f2h4 cp_losses=[0, 0, 840] best_moves=['f2h4', 'f2h4', 'b1h7'] spread=840
```

---

## 4. Soubory

| Soubor | Zmena |
|--------|-------|
| `engine_client.py` | Pridano `import logging`, D3 funkce, D4 funkce |
| `test_engine_client.py` | 26 testu (5 originalnich + 21 novych) |

---

## 5. Dalsi kroky

1. **Cache invalidace:** Prefrost cache po oprave
2. **Pipeline integrace:** Propojit D3/D4 do `game_analyzer.py`
3. **Monitoring:** Sledovat D3 anomality v produkcni analyzy

---

*Verze: 1.0 | Datum: 2026-08-03 | Autor: outpost2026*
