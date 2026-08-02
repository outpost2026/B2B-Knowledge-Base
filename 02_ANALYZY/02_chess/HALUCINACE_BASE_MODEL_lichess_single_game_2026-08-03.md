# HALUCINACE_BASE_MODEL — lichess MCP pipeline single-game report
**Datum:** 2026-08-03 | **Autor:** outpost2026 + oprava LLM (korelace)
**Účel:** Base model halucinace MCP coaching pipeline pro pozdější korelaci výstupů single-game reportů (oprava mislabel/blunder klasifikace).
**Verze:** 1.0 | **Účel:** Falsifikovatelný vzor — co hledat při korelaci pipeline.

## 1. Zdrojový případ
- **Partie:** `https://lichess.org/CpEDieiZDefM` → game_id `CpEDieiZ`
- **Barva:** bílá | **Výsledek:** 1-0 (bílý vyhrál) | **Zahájení:** Sicilianská, Smith-Morra Gambit Accepted
- **Expof vertik:** `lichess_coaching_single_game` (NVIDIA nemotron-3-super-120b-a12b, depth 14)
- **Report path:** `lichess-analyzer-mcp/data/reports/single_game_*` (MCP live výstup)

## 2. Halucinace (konkrétní chyba)
MCP report klasifikoval tah **ply 45 `Qe4h4` (`Qh4`)** jako:
> Blunder 1 — ply 45 `Qh4`, ztráta **1053 cp**, fáze middlegame, "visící dáma".

**Nesprávné. Skutečnost (deterministicky, Stockfish + python-chess):**
- Pouze **jediný** `Qh4` v partii → plyt 45, move 23 (černý).
- **Stockfish depth 18/24:** `Qh4` = **+3.31** (~ vyhrávající), nejlepší tah na depth 1; alternativa `Bxh7+` = +4.30.
- Dáma po `Qh4` na h4 **není vyvěšená** — žádný černý kus ji nekryje (černý Sg4 nekryje h4, Qa5 směr nespojí).
- Výsledek partie **1-0** vyhraný bílým — v rozporu s tvrzením o 1053-cp blunderu (bílý, který "zavěsil dámu", nemůže tak vyhrát).

## 3. Root cause (rozpracovaná hypotéza pro korelaci)
1. **Mislabeled ply/tah:** Report v `BlunderFactSheet` zmiňuje **ply 41 `fxg7` (153 cp)** — report slepil chyby ze dvou platy; blundru `Qh4` přiřadil skóre/kontext jiného tahu (p.p. soupeřovy chyby).
2. **Barva/perspektiva:** V anonymní hrá (oba "Anonymous") je board perspektiva nejistá — report mohl vzít eval z cache opačné barvy (známý bug popsaný v ANALYZA_OPONENTA — `opponent_pool` fallback author=white). Zde to vysvětluje style "viscí dáa" pro tah, který je vyhrávající.
3. **Halucinace eval čísla:** 1053 cp neodpovídá žádnému tahu bíla v partii → pravděpodobně si LLM vygeneroval hodnotu z `fxg7`/soupečova tahu a přisouhodl `Qh4`.

## 4. Korelační ukazateľe (při auditu libovolném single-game reportu)
Kanáry, že tah v reportu je halutinovaný:
- [ ] Tah klasifikovaný jako blunder má partie result 1-0/0-1 **opotřebený** (hráč, který "zavěsá dáa", nyní tento výsledek)
- [ ] BlunderFactSheet citony **jiný ply/tah** než pole blunderu (nekonzistence dvou ply)
- [ ] Eval daného tahu (nezávisle, Stockfish/position) je > ±1.5 cp od tvrzené ztráty
- [ ] "visír dáma/věc" tvrzená, ale žádný soupeř kus kus ohružuje drah (verify piece_map)
- [ ] Hodnota ztráty (např. 1053) odpovídá popisu soupečova tahu typu "ztráta dámy" ≠ ztráta bílého

## 5. Verzocation postup (reprodukovatelné)
```python
# ve venovském repа lichess-analyzer-mcp
board=sar (+ hra PGN)  # ply 45 Q>P d4
print(board.fen())      # r4rk1/1p3pbp/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w - - 2 23
```
- FEN před `Qh4`: `r4rk1/1p3pbp/p7/q2pP3/3B2b1/P/1B1R1RK1 w`
- FEN po `Qh4`: `r4rk1/1p3pbp/p7/q2pP3/3B2bQ/P7/1P... b`
- Stockfish position tool depth 18 → +3.31 (Qh4), +4.34+ (Bxh7+).

## 6. Využití jako base model
- **Vstup do budoucí korelace:** porovnat každý single-game/opponent report oproti deterministickému FEN+Stockfish eval RRED tak, aby data platforma zruvals/LLM halucinační klasifikaa.
- **Datové pole k uložení u reportů:** `source_fen`, `engine_eval_cp` namespace (ex nex draw/ply), sanity: `blunder_result_consistent`.
- Při detekci → oprav lím not LLM opětovu, ale **determinismus (python-chess + Stockfish)**.

## 7. Navazující artefakty
- `02_ANALYZY/02_chess/ANALYZA_OPONENTA_anonymni_101_her_2026-08-02.md` (pipeline bug good overview)
- `04_KNOWLEDGE_BASE/01_MCP/MCP_GROUND_TRUTH_postmortem_agregovany_v1.md` (GT/P-pravidla MCP)