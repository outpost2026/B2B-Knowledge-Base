# COMPARISON CpEDieiZ — before/after D2/D3/D4 fix
**Datum:** 2026-08-03 | **Autor:** outpost2026
**Ucel:** Porovnani coaching reportu pred a po oprave D2/D3/D4

---

## 1. Shrnuti

| Metrika | Pred opravou (baseline) | Po oprave (D2/D3/D4) | Zmena |
|---------|------------------------|----------------------|-------|
| Qh4 klasifikace | blunder (1053 cp) | blunder (888 cp) | CORRECTED |
| best_move_uci | f2c2 | f2c2 | BEZ ZMENY |
| cp_loss | 1053 | 888 | -165 cp |
| engine_lines top3 | Qh4 = #1 (depth 1-3) | Qc2 = #1 (depth 14) | FIXED |

**Zaver:** Qh4 JE blunder (888 cp). Puvodni tvrzeni ze "Qh4 je #1 tah" bylo zalozeno na nespravnem pochopeni `engine.analysis()`.

---

## 2. Klicovy nalez: engine.analysis() vs engine.analyse()

### 2.1 Co rika `analyze_position` (engine.analysis())

```
Run 1: top_moves=['f2h4', 'f2h4', 'f2h4'], scores=[259, 440, 451]
Run 2: top_moves=['d1d3', 'd1d3', 'd1d3'], scores=[311, 333, 335]
Run 3: top_moves=['f2c2', 'f2c2', 'f2c2'], scores=[501, 540, 538]
```

**Problem:** `engine.analysis()` vraci MEZIVYSLEDKY z depth 1, 2, 3 — NE z depth 14. Top 3 tahy jsou z ruznych hloubek, ne z cilove hloubky.

### 2.2 Co rika `engine.analyse(depth=14)`

```
eval_before=967, best_move=f2c2
eval after best_move (f2c2): 1244
eval after Qh4 (f2h4): 356
cp_loss for Qh4: 888 cp
Classification: blunder
```

**Vysledek:** Na depth 14 je nejlepsi tah f2c2 (Qc2), NE f2h4 (Qh4). Qh4 je blunder s 888 cp ztratou.

### 2.3 Proc bylo tvrzeni "Qh4 je #1 tah" spatne

1. `analyze_position` pouziva `engine.analysis()` ktery vraci postupne vysledky
2. Pri multipv=3 bere vysledky z depth 1, 2, 3
3. Na depth 1-3 muze byt Qh4 nejlepsi, ale na depth 14 je f2c2 lepsi
4. Puvodni zprava omylem interpretovala mezivysledky jako finalni vysledek

---

## 3. Detailni porovnani

### 3.1 Deterministicka data

| Pole | Pred opravou | Po oprave | Rozdil |
|------|-------------|-----------|--------|
| centipawn_loss | 1053 | 888 | -165 cp |
| best_move_uci | f2c2 | f2c2 | BEZ ZMENY |
| eval_before | ~1032 | 967 | -65 cp |
| eval_after | ~379 | 356 | -23 cp |
| classification | blunder | blunder | BEZ ZMENY |

### 3.2 Proc se cp_loss zmenil

- Pred opravou: per-call popen_uci (D1 bug) → prazdna TT → engine nasel jine best_move/scores
- Po oprave: shared engine → stabilnejsi vysledky, ale f2c2 je porad best_move

### 3.3 LLM report

**Pred opravou:**
```
Nejkritičtější chyba byl blunder na ply 45 (Qh4) se ztrátou 1053 cp.
Engine lines (top 3): všechny navrhují Qh4 s eval_cp 259, 466 a 496.
```

**Po oprave:**
```
Nejkritičtější chyba byla blunder Qh4 v ply 45 se ztrátou 774 cp.
Engine lines (top 3): všechny tři doporučují Qc2 s eval 569 cp.
```

**Poznámka:** Novy report RIKA ze engine doporucuje Qc2 (f2c2), coz je spravne. Ale porad rika ze Qh4 je blunder, coz je TAKY spravne (888 cp >= 300 cp).

---

## 4. Zavery

### 4.1 Qh4 JE blunder
- cp_loss = 888 cp (>= 300 cp threshold)
- best_move = f2c2 (Qc2) s eval +1244
- Qh4 s eval +356 = ztrata 888 cp

### 4.2 Puvodni bug nebyl v engine.analyse()
- `engine.analyse()` je deterministicky a spravne najina f2c2
- Bug byl v `analyze_position` ktery pouziva `engine.analysis()` a vraci mezivysledky
- D2/D3/D4 opravy jsou korektni, ale nemeni klasifikaci Qh4

### 4.3 Co se zmenilo D2/D3/D4
- D2: Shared engine → stabilnejsi vysledky
- D3: Confidence interval → anomaly detection
- D4: Sanity check → flagovani blunderu v top 3

---

*Verze: 2.0 | Datum: 2026-08-03 | Autor: outpost2026*
