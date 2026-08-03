# PLAN_OPRAVY_pipeline_determinismus_2026-08-03
**Datum:** 2026-08-03 | **Autor:** outpost2026
**Ucel:** Plan opravy deterministicky vrstvy v MCP-lichess pipeline — vratit sdilenou engine, overit determinismus, zajistit stabilitu
**Verze:** 1.0

---

## 1. Cil opravy

**GOAL:** Deterministicka vrstva v pipeline **musi** byt principialne deterministicky.

**Kriterium uspechu:**
- Stejny FEN + stejne depth → stejny best_move (100% shoda)
- Stejny FEN + stejne depth → cp_loss v rozmezi +/- 10 cp (95% interval)
- Zadny hang/timeout pri analize legalnich tahu
- Zadny regression v existujicich testech

---

## 2. Analiza soucasneho stavu

### 2.1 Co je rozbitne

| Funkce | Soubor | Stav | Problem |
|--------|--------|------|---------|
| `evaluate_move` | `engine_client.py:180-255` | Per-call `popen_uci()` | Nedeterministicky — prazdna TT |
| `analyze_position` | `engine_client.py:126-167` | Shared `get_engine()` + lock | OK — deterministicky |
| `get_best_move` | `engine_client.py:258-281` | Shared `get_engine()` + lock | OK — deterministicky |

### 2.2 Proc byla zmena (4a55f1f) potrebna

Commit message rika:
```
Root cause: evaluate_move hung when move_uci was syntactically valid
but not legal for the position (e.g., black move g8f6 on white's turn).
engine.analyse() received a nonsensical board state and hung.
```

**Duvod:** Na Windows zpusoboval sdileny engine **zaseknuti** pri analyze **nelegalniho tahu**.

### 2.3 Proc uz to neni problem

Aktualni kod jiz ma **legal-move guard** (`engine_client.py:187-194`):
```python
if move not in board.legal_moves:
    return {
        "eval_before": 0,
        "eval_after": 0,
        "centipawn_loss": 0,
        "best_move_uci": None,
        "error": f"Move {move_uci} not legal in position {fen}",
    }
```

Tento guard **zabranuje** analize nelegalniho tahu. Tim padem se hang nemoze vratit.

---

## 3. Plan opravy

### Krok 1: Upravit `evaluate_move` v `engine_client.py`

**Zmena:** Vratit sdilenou engine + lock misto per-call popen_uci.

**Pred (soucasny stav — NEDETERMINISTICKY):**
```python
def evaluate_move(fen: str, move_uci: str, depth: int = 0) -> dict:
    # ... validace ...
    
    sf_path = _get_sf_path()
    engine = chess.engine.SimpleEngine.popen_uci(sf_path)  # NOVY engine
    engine.configure({"Threads": 6, "Hash": 512, ...})
    try:
        # ... analyza ...
    finally:
        engine.quit()  # ZNIC engine
```

**Po (opraveny — DETERMINISTICKY):**
```python
def evaluate_move(fen: str, move_uci: str, depth: int = 0) -> dict:
    # ... validace (legal-move guard zustava) ...
    
    engine = get_engine()              # SDILENA engine (singleton)
    _acquire_analysis_lock()           # MUTEX
    try:
        # ... analyza ...
    finally:
        _analysis_lock.release()       # UVOLNI zamek
```

**Specificke zmeny v `engine_client.py`:**

| Radek | Pred | Po | Duvod |
|-------|------|-----|-------|
| 204-206 | `sf_path = _get_sf_path()` + `popen_uci()` + `configure()` | `engine = get_engine()` | Vrati sdilenou engine |
| 207 | (zadny lock) | `_acquire_analysis_lock()` | Zajisti exkluzivni pristup |
| 239-243 | `engine.quit()` | `_analysis_lock.release()` | Uvolni zamek misto niceni engine |

**Co zustava beze zmeny:**
- Legal-move guard (radky 187-194) — KLIB pro fix hang
- Cloud fallback (radky 196-202) — nemeni se
- Cela logika vypoctu cp_loss (radky 245-248) — nemeni se
- Vystupni format (radky 250-255) — nemeni se

### Krok 2: Pridat deterministic test suite

**Soubor:** `tests/test_engine_client.py` (novy test)

**Test: determinismus evaluate_move**
```python
class TestEvaluateMoveDeterminism:
    def setup_method(self):
        # FEN z CpEDieiZ pred Qh4
        self.fen = "r4rk1/1p3pbp/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w - - 2 23"
        self.move = "f2h4"
        self.depth = 14
        self.runs = 10

    def test_best_move_deterministic(self):
        """10 behu na stejnem FEN musi dat stejny best_move."""
        results = []
        for _ in range(self.runs):
            result = evaluate_move(self.fen, self.move, depth=self.depth)
            results.append(result["best_move_uci"])
        
        # Vsechny vysledky musi byt stejne
        assert len(set(results)) == 1, f"Best move se lisi: {results}"

    def test_cp_loss_consistent(self):
        """10 behu na stejnem FEN musi dat cp_loss v rozmezi +/- 10 cp."""
        results = []
        for _ in range(self.runs):
            result = evaluate_move(self.fen, self.move, depth=self.depth)
            results.append(result["centipawn_loss"])
        
        # Rozptyl max 20 cp
        assert max(results) - min(results) <= 20, f"Prilis velky rozptyl: {results}"

    def test_no_hang_on_legal_move(self):
        """Legalni tah nesmi zpusobit hang."""
        result = evaluate_move(self.fen, self.move, depth=self.depth)
        assert "error" not in result
```

### Krok 3: Overit ze hang se nevrati

**Test: legalni tah nehanguje**
```python
class TestNoHang:
    def test_legal_move_no_hang(self):
        """Legalni tah nesmi zpusobit hang (originalni problem 4a55f1f)."""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        result = evaluate_move(fen, "e2e4", depth=8)
        assert "error" not in result
        assert result["best_move_uci"] is not None

    def test_illegal_move_returns_error(self):
        """Nelegalni tah musi vratit error (nenechat engine hang)."""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        # g8f6 je black move, ale pozice je na tahu bileho
        result = evaluate_move(fen, "g8f6", depth=8)
        assert "error" in result
```

### Krok 4: Smazat nepouzivane funkce

Po oprave nebudou potreba:
- `_get_sf_path()` — jiz se nepouziva (bylo jen pro per-call popen_uci)
- `_SF_PATH` globalni promenna — jiz se nepouziva

**Poznámka:** `_get_sf_path()` se nepouziva jinde v kodu, ale nechame ji pro pripad budouciho vyuziti (je private, nezatezuje).

### Krok 5: Cache invalidace

Po oprave je potrebna **prefrost_cache** — vsechny existujici cache soubory by mely byt pregenerovane s novym (deterministickym) engine.

**Doporučeni:** Spustit `analyze_pgn` na vsechny hry v cache s `use_cache=False` a ulozit nove vysledky.

---

## 4. Rizika a mitigace

| Riziko | Mitigace |
|--------|----------|
| Hang se vrati | Legal-move guard (radky 187-194) zabranuje analize nelegalniho tahu. Test overi. |
| Regresi v jinych funkcich | `analyze_position` a `get_best_move` uz pouzivaji shared engine — bez zmeny |
| Cache nesynchronizovana | Prefrost cache po oprave |
| Performance regression | Shared engine je rychlejsi (neni nutne startovat novy proces) |

---

## 5. Poradi implementace

1. **Upravit `engine_client.py`** — vratit shared engine v `evaluate_move`
2. **Pridat testy** — deterministic test suite
3. **Spustit testy** — overit ze vsechny existujici + nove testy prochazeji
4. **Prefrost cache** — pregenerovat cache soubory
5. **Smoke test** — spustit `analyze_pgn` na CpEDieiZ a overit ze Qh4 neni blunder

---

## 6. Ocekavane vysledky

### Pred opravou (soucasny stav)
```
FEN: r4rk1/1p3pbp/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w
evaluate_move(f2h4, depth=14):
  Beh 1: best_move=f2c2, cp_loss=1149
  Beh 2: best_move=f2c2, cp_loss=716
  Beh 3: best_move=f2c2, cp_loss=533
  Rozptyl: 616 cp (NEDETERMINISTICKY)
```

### Po oprave (oczekavany stav)
```
FEN: r4rk1/1p3pbp/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w
evaluate_move(f2h4, depth=14):
  Beh 1: best_move=f2h4, cp_loss=0
  Beh 2: best_move=f2h4, cp_loss=0
  Beh 3: best_move=f2h4, cp_loss=0
  Rozptyl: 0 cp (DETERMINISTICKY)
```

**Proc best_move=f2h4 a cp_loss=0:** `analyze_position` (sdilena, deterministicky) uz rika ze Qh4 je TOP tah. Po oprave bude `evaluate_move` souhlasit.

---

## 7. Dalsi kroky (mimo tento plan)

1. **D2 oprava:** Pouzit jeden zdroj pravdy — `analyze_position`/multipv pro klasifikaci i BFS
2. **D3 oprava:** Confidence interval ke cp_loss — spustit evaluate_move 3x, vzit median
3. **D4 oprava:** Sanity check — partii 1-0 + blunder "hanging piece" = warning

---

## 8. LLM Machine-Readable Summary

```json
{
  "plan_type": "pipeline_determinism_fix",
  "target_file": "engine_client.py",
  "target_function": "evaluate_move",
  "commit_to_revert": "4a55f1f",
  "changes": [
    {
      "line_range": "204-206",
      "action": "replace",
      "from": "popen_uci() per-call engine",
      "to": "get_engine() shared singleton"
    },
    {
      "line_range": "207",
      "action": "add",
      "content": "_acquire_analysis_lock()"
    },
    {
      "line_range": "239-243",
      "action": "replace",
      "from": "engine.quit()",
      "to": "_analysis_lock.release()"
    }
  ],
  "tests_to_add": [
    "test_best_move_deterministic (10 runs, same result)",
    "test_cp_loss_consistent (10 runs, +/- 10 cp)",
    "test_no_hang_on_legal_move",
    "test_illegal_move_returns_error"
  ],
  "expected_outcome": {
    "determinism": "100% best_move consistency, cp_loss variance < 20 cp",
    "hang_fix": "Legal-move guard prevents original hang",
    "performance": "Shared engine faster than per-call"
  },
  "cache_action": "prefrost after fix"
}
```

---

*Verze: 1.0 | Datum: 2026-08-03 | Autor: outpost2026*
