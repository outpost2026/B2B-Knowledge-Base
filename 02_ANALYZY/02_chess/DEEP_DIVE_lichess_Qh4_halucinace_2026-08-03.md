# DEEP_DIVE_HALUCINACE_lichess_Qh4_1053cp
**Datum:** 2026-08-03 | **Autor:** outpost2026 (deep dive, reprodukované)
**Účel:** Root cause analýza false klasifikace `Qh4` = 1053 cp blunder v single-game reportu partie CpEDieiZ — rozlišení deterministické pipeline vs LLM halucinace.
**Verze:** 1.0

## 1. Fenomén (co report tvrdil)
- `lichess_coaching_single_game` (white, depth 14) klasifikoval ply 45 `Qh4` = blunder, ztráta **1053 cp**, "visící dáma", middlegame.
- Partie ale skončila **1-0** pro bílého. Bílý, který "zavěsil dámu", takový výsledek nemůže mít — základní signál nesouladu.

## 2. Deterministická pipeline NENÍ konzistentní (reprodukováno)
Stockfish depth 14 na stejném FEN `r4rk1/1p3pbp/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w`:

| Nástroj | best_move | loss Qh4 | Eval pozice |
|---------|-----------|----------|-------------|
| `analyze_position` (shared engine) | **Qh4** | — | +259 / +331 / +423 (Qh4 = TOP tah) |
| `evaluate_move` run 1 | `f2c2` | **1149** | eval_after Qh4 = 379 |
| `evaluate_move` (původní pipeline cache) | — | **1053** | — |
| `evaluate_move` run 2 | `f2c2` | **716** | eval_after Qh4 = 379 |
| `evaluate_move` run 3 | `f2c2` | **533** | — |

→ `evaluate_move` (per-tah klasifikace blunderů) je **fyzicky nedeterministický** (716/1149/1053/533) a **protiráží** `analyze_position` (dle něho je `Qh4` NEJLEPŠÍ tah +2.6..+4.2).

## 3. Root cause — deterministický bug v `engine_client.evaluate_move` (engine_client.py:180-256)
1. **Nový engine proces na každé volání** (`engine_client.py:205` `popen_uci`). Stockfish s multithreading/hash je **fyzicky nedeterministický** — stejný vstup → kolísavý best_move + cp_loss.
2. **Best-move rozpor:** `evaluate_move` vybere best=`f2c2`, ale `analyze_position` na stejném FEN dává `Qh4`. Dva navzájem kolizní zdroje pravdy pro původní tah.
3. **cp_loss formule** (`engine_client.py:245-248`): `max(0, best_player - actual_player)`. Když best_move je mimo kategorii "root" a hra má hluboké takt. Výměny → **vyhrané tah takté 1000+ cp blunder**.
4. **BFS vs klasifikace použít 2 různé zdroje:** BFS (`game_analyzer.py:376` `analyze_position`, shared engine) vs klasifikace (`game_analyzer.py:329` `evaluate_move`, nový engine). **Stejný tah = 2 nesouladné verdict -> v akci p říabsentní** patenty patří.

## 4. Hypotéza A — čistá AI halucinaia? → NE
LLM (NVIDIA) **věrne opsal data pipeline** (`blunders_list` obsahoval `Qh4 loss=1053` dle cache). LLM nevynhylýl číslo 1053 — přišlo z deterministické pipeline. Omezit to jako "halucinace" je nepřesné: je to **false-positive deterministické klasifikace z `evaluate_move`**.

## 5. Hypotéza B — sekundární AI konfabulace
- Report slepil dva tahy: `BlunderFactSheet` uvádí **ply 41 `fxg7` (153 cp)**, zatímco blunder identifikován **ply 45 `Qh4` (1053 cp)**. Dva nezříčiny z jednoho FEN → report nekonšíštr.
- K popisu "vísí dáma" přidal LLM nar z z vlast (není doložena BFS: engine_lines ukazuje Qh4=rank1+).
- → LLM **aktivně konfabutoval narativ** na elementary rozporových datech, ale **nebyl v generacQt1 gátor čísla 1053**. Zároveň porušujeme DATA-FABRICATIONS-001 (report neđask vви кор lisблил full chain: BFS detail vs blundr list).

## 6. Pipeline defekty (oprava doporučena)
| # | Defekt | Oprava |
|---|--------|--------|
| D1 | `evaluate_move` spawnuje engine per call → fyzicky nedeterminism | Reuse shared `get_engine()` + lock (jako `analyze_position`); zajistit deterministický eval |
| D2 | best-move klasifikace (evaluate_move) a BFS (analyze_position) z 2 zdrojů | Použít SAMA` analyze_position`/multipv pro klasifikaci i BFS — single zdroj pravdy |
| D3 | cp_loss `max(0,best-actual)` v kras spreadovém prostoru | Normalizovat/podpřa stostility; při podezřenív obou signálů → nepočítat blunder |
| D4 | bez sanity checks | Přidat korelační kanár z base model − win partii × "zavěšená major figure". Flagzy 되는가 |

## 6. Data
- FEN před `Qh4`: `r4rk1/1p3pbp/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w - - 2 23`
- Tah: `Qf2-h4` (ply 45, bílý)
- Eval bílého nezávislé (position): +2.6..+4.2 → vyhrávající prob du.

## 7. Navázání
- Base model: `02_ANALYZY/02_chess/HALUCINACE_BASE_MODEL_lichess_single_game_2026-08-03.md`
- Zobrazenová předpis nyní: **root cause = deterministický defect `evaluate_move` (engine per-call nondeterminismus + 2 kolizní zdroje pravdy) + sekundární AI konfabulace (нарутiv) na rozporových dataech.**

---
*Shrnutí: NENÍ to čistá halucinace — nýbrž deterministická false-positive klasifikace (engine nondeterminism + isolated truth sources) amplifikovává LLM naratifem. Base model pointer był opraven.*