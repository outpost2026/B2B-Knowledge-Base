# OPRAVA: analyze_position — multipv z depth 1,2,3 na depth 14
**Datum:** 2026-08-03 | **Autor:** outpost2026
**Ucel:** Oprava kriticke chyby v analyze_position — engine_lines z nespravne hloubky

---

## 1. Problem

### 1.1 Kontradikce v coaching reportu

```
Blunders: Qh4, ztrata 936 cp          ← z engine.analyse(depth=14)
engine_lines top3: Qh4 = #1            ← z engine.analysis(depth=1,2,3)
```

Tyto data nepochazeji ze stejne hloubky! LLM dostava kontradikcni data.

### 1.2 Root cause

`analyze_position` pouzival `engine.analysis()` s `multipv=3`:

```python
# STARY KOD (CHYBNY):
with engine.analysis(board, Limit(depth=14)) as analysis:
    for line in analysis:
        items.append(line)
        if len(items) >= 3:  # multipv=3
            break            # ← BREAK na depth 3!
```

`engine.analysis()` vraci vysledky postupne (depth 1, 2, 3...). Pri `multipv=3` se bere depth 1, 2, 3 — NE depth 14.

### 1.3 Dopad

- **engine_lines** v BlunderFactSheet byly z depth 1, 2, 3
- **cp_loss** byl z depth 14
- **Kontradikce:** Qh4 zaroven "#1 tah" a "blunder"
- **SNR = 0** — data z D<12 jsou skum pro analyzu na D14

---

## 2. Oprava

### 2.1 Zmena v `engine_client.py`

```python
# NOVY KOD (SPRAVNY):
results = engine.analyse(board, Limit(depth=depth), multipv=multipv)
items = []
for info in results:
    items.append({
        "depth": info.get("depth", depth),
        "score_cp": info["score"].relative.score(),
        ...
    })
return items
```

### 2.2 Klicovy rozdil

| | Pred opravou | Po oprave |
|--|-------------|-----------|
| API | `engine.analysis()` | `engine.analyse()` |
| multipv | break po 3 items | multipv parametr |
| Vysledek | depth 1, 2, 3 | depth 14 (cilova) |
| engine_lines | #1 = Qh4 (D3) | #1 = Qc2 (D14) |

### 2.3 Overeni

```
analyze_position(fen, depth=14, multipv=3):
  Run 1: top_moves=['f2c2', 'f2c2', 'f2c2'], depths=[14, 14, 14]
  Run 2: top_moves=['f2c2', 'f2c2', 'f2c2'], depths=[14, 14, 14]
  Run 3: top_moves=['f2c2', 'f2c2', 'f2c2'], depths=[14, 14, 14]
```

Vsechny vysledky jsou z depth 14. Zadne D<12 skum.

---

## 3. Testy

### 3.1 Novy test

```python
def test_returns_results_from_target_depth(self):
    """analyze_position must return results from target depth."""
    fen = "r4rk1/1p3pbp/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w - - 2 23"
    result = analyze_position(fen, depth=14, multipv=3)
    for item in result:
        assert item.get("depth", 0) >= 12  # Ne z depth 1,2,3
```

### 3.2 Vysledek testu

27/27 PASSED (37.36s)

---

## 4. Doporuceni

### 4.1 OKamzite (P0)
- ✅ Opraveno: `analyze_position` nyni pouziva `engine.analyse()` s multipv
- ✅ Otestovano: 27/27 testu passing

### 4.2 Stredni (P1)
- Prefrost cache po oprave
- Overit ze coaching report nema kontradikce

### 4.3 Dlouhodobe (P2)
- Zvazit odstraneni `engine.analysis()` z celeho kodu (pouze `engine.analyse()`)
- Pridat validaci: pokud centipawn_loss > 300 ale engine_lines rikaji #1 tah, flag

---

*Verze: 1.0 | Datum: 2026-08-03 | Autor: outpost2026*
