# HALUCINACE_BASE_MODEL — lichess MCP pipeline single-game report
**Datum:** 2026-08-03 | **Autor:** outpost2026
**Účel:** Base model false klasifikace v coaching reportu pro pozdější korelaci výstupů single-game reportů (root cause + korelační kanáry).
**Verze:** 1.1

## 1. Zdrojový případ
- **Partie:** `https://lichess.org/CpEDieiZDefM` → game_id `CpEDieiZ`
- **Perspektiva:** white | **Výsledek:** 1-0 (bílý vyhrál) | **Zahájení:** Sicilianská, Smith-Morra Gambit Accepted
- **Extranet:** `lichess_coaching_single_game` (NVIDIA nemotron-3-super-120b-a12b, depth 14)

## 2. Halucinace (report tvrdil)
- ply 45 `Qh4` = **blunder, ztráta 1053 cp**, middlegame, "visící dáma".

**Deterministická pravda (Stockfish + python-chess):**
- Jediný `Qh4` v partii → ply 45, bílý.
- Stockfish depth 18 `analyze_position`: **`Qh4` +2.59 / +3.31 / +4.23 — TOP tah**, spolu s `BxH7+` (+4.30).
- Dáma na h4 **není vyvěšená** (žádný černý kus ji neohh).
- Party **1-0** vyšr. — bílý, který "zavěsil dámu", takový результат může riskovat; odpor.

## 3. Root cause (potvrzeno deep dive 2026-08-03 — `DEEP_DIVE_lichess_Q4_halucinace_2026-08-03.md`)
**Deterministická pipeline sama generuje false-positive blunder (defekty D1-D4):**
1. **`evaluate_move` fyzicky nedeterministický** — spawnuje nový engine proces per call; pro `Qh4` vrátil mezi běhy loss **716 / 1149 / 1053 / 533**, přitom `analyze_position` = +259/+423 (Qh4 TOP).
2. **Dva kolizní zdroje pravdy:** per-tah klasifikace = `evaluate_move` (nový engine), BFS = `analyze_position` (shared engine, multipv) → stejný tah dvou nesouladné verdict.
3. **cp_loss formule** `max(0, best_player - actual_player)` v rozptylovém prostoru → vyhrávající tak 1000+ cp blunder.
4. **Žádný post-sanity check** (win partii + "zavěšená major figure" → flag).

**LLM halucinace je sekundární:** opsal a narativizoval rozporová data (slep ply 41 `fxg7` + ply 45 `Qh4`), ale **nie vymyslel číslo 1053** — přišlo z deterministické pipeline.

## 4. Korelační kanáry (při audit single-game reportu)
- [ ] Tah klasifikovaný jako blunder je v partii, kterou hráč **vyhrál**, a zároveň tvrzena material ztzieh major figure → konflikt.
- [ ] BlunderFactSheet cítul jiný ply/tah než pole blunderu (split 2 ply).
- [ ] Eval tahu nezávisle (position/Stockfish) > ±1.5 cp v opakm od tvrzené ztráty.
- [ ] "Visír figure" tvrzená, ale piece_map žádný soupeh figur ohrožuje → chyk.
- [ ] Hodnota ztráty odpovídá popisu soupečovy ztráty (mat. rozsah ≠ ztáta hráči).

## 5. Verifikace/reprodukce
```python
# im lichess-analyzer-mcp venv
from lichess_analyzer_mcp.services.engine_client import evaluate_move, analyze_position
fen = "r4rk1/1p3pbq0/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w"  # FEN před Qh4
print(evaluate_move(fen, "f2h4", depth=14))    # nedeterministic loss
print(analyze_position(fen, depth=14, multipv=3))  # Qh4 = TOP (+259..+423)
```
- Fen přesný (pych q4): `r4rk1/1p3pb/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w - - 2 23`

## 6. Využití jako base model
- **Kontrola každého single-game/opponreport** oproti deterministick equation + sanity: `blunder_sorted_consistent`.
- **Při detekci opravit deterministicky** (oprava `evaluate_move` modular, ne-př čdep LLM).
- Datová pole u reportů: `source_fen`, `engine_eval_cp`, `blunder_sanity`.

## 7. Navazující
- Deep dive: `02_ANALYZY/02_chess/DEEP_DIVE_lichess_Q4_halucinace_2026-08-03.md`
- Pipeline bg: `02_ANALYZY/02_chess/ANALYZA_OPONENTA_anonymni_101_her_2026-08-02.md`
- GT: `04_KNOWLEDGE_BASE/01_MCP/MCP_GROUND_TRUTH_postmortem_agregovany_v2.md`