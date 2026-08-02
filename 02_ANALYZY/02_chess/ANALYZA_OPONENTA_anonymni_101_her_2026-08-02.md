# ANALÝZA OPONENTA — anonymní hry (101 her)
**Datum:** 2026-08-02 | **Autor:** outpost2026 + LLM (NVIDIA cascade)
**Účel:** Pattern fingerprint anonymních oponentů + exploitable vzorce + countermeasures pro autorovu hru.

## Zdroj dat (deterministické)
- Dataset: `lichess-analyzer-mcp/data/lichess_anonymni_partie_opponent_perspective.txt` (101 her, hlavička `perspective: opponent`)
- Report: `lichess-analyzer-mcp/data/anonymous_batch_20260802_194453.json` (Stockfish d12, oponent perspektiva)
- Fingerprint: `lichess-analyzer-mcp/data/pattern_fingerprint_opponent_101.json`
- Opponent pool report: `lichess-analyzer-mcp/data/reports/opponent_pool_pool_101_20260802_185218.json`
- Všechna tvrzení ověřena z cache/tool (AGENTS.md DATA-FABRICATION-001), žádná game_id bez affected_games zdroje.

## Agregát (oponent perspektiva, 101 her)
- Rekord oponenta: **15W / 84L / 2D**
- Průměrná ACPL oponenta: **51.2**
- Celkem blunderů oponenta: **98**
- n1 (hry, kde oponent nevyhrál): 86 her, ACPL **54.0**, blunder rate 2.70/hra
- n2 (hry, kde oponent vyhrál): 15 her, ACPL **34.6**, blunder rate 2.53/hra
- ACPL diferenciál n1→n2: **–19.4 cp** (oponent hraje výrazně lépe, když vyhrává)

## Pattern fingerprint oponenta (seřazeno dle frekvence)
| ID | Pattern | Severity | Frekvence | % her | Prům. conf |
|----|---------|----------|-----------|-------|-----------|
| O | Stagnační panika | critical | 60/101 | 59.4 % | 83.0 |
| B | Automatic grab | high | 36/101 | 35.6 % | 78.0 |
| C | Attention tunneling | medium | 27/101 | 26.7 % | 74.2 |
| R | Endgame relaxation | high | 14/101 | 13.9 % | 67.0 |
| J | Impulsive check block | high | 11/101 | 10.9 % | 64.0 |
| G | Color as modulator | high | 10/101 | 9.9 % | 85.0 |
| Q1 | Desperate Gambit Mode | low | 5/101 | 5.0 % | 55.7 |
| Q2 | Win despite blunder | low | 5/101 | 5.0 % | 57.5 |
| N | X-ray pin violation | high | 4/101 | 4.0 % | 57.0 |
| P | Visual misrecognition | high | 2/101 | 2.0 % | 57.0 |

## Co oponenti dělají špatně (systémová slabost)
1. **Stagnační panika (O)** — dominantní: 59 % her. Po 3+ tazích s plochým evalem (<30 cp swing) oponent vynutí prohrávající tah do 6 tahů. Pozice, kde "nic se neděje", spouští u oponentů nucené komplikace, které kolabují.
2. **Automatic grab (B)** — 36 % her. Slepé braní bez vyhodnocení soupeřovy protihry.
3. **Attention tunneling (C)** — 27 % her. Fixace na jednu oblast desky, přehlédnutí protihry jinde.
4. **Endgame relaxation (R)** — 14 % her. Ztráta koncentrace při materiální výhodě v koncovce.

## Exploitable patterns (co využít proti oponentům)
- Vytvářet **dlouhé rovnoměrné eval plošiny** (výměna hlavních figur → uzavřená struktura) → spouští pattern O.
- Vyvolávat **vícepruhové taktické hrozby** na různých částech desky → pattern C (tunneling).
- Nabízet **zdánlivě volné figury** skryté za x-ray/útok → patterny B a N.
- V koncovce udržovat **aktivní tlak** (aktivní král/věž) → brání pattern R.
- Šachy, které jde řešit **výměnou nebo útěkem krále** → nutí k impulsivnímu bloku (J).
- Oponent po velké chybě občas vyhraje (Q2) — soupeř nevyužívá příležitosti; tlak snižuje tuto odolnost.

## Countermeasures (autorova hra proti těmto oponentům)
- Po 2+ tazích s plochým evalem se ptát "Je to opravdu stagnace, nebo jen pozicní klid?" — nedopřát oponentovi stagnaci, na kterou panikaří.
- Udržovat aktivní, dynamické pozice s konkrétními hrozbami — minimalizovat rovnoměrné plošiny.
- Vytvářet vícetematické taktické pozice, kde oponent tunnelingem ztrácí.
- Kontrolovat vlastní automatic grab — 3s pauza + "A CO ON?" před každým braním.
- Když oponent panikaří (flat eval), nebranit mu — nechat ho zničit pozici sám.

## n2 study (když oponent vyhrál)
- ACPL 34.6 vs 54.0 v prohrách — oponent v výhrách dělá podstatně méně velkých chyb.
- Méně panických reakcí, přesnější taktické hodnocení.
- Implikace: autorův tlak na oponenty funguje — prohrané hry oponentů mají výrazně horší rozhodování.

## Metodická poznámka (oprava pipeline)
- `lichess_coaching_opponent_pool` je pro anonymní hry **nepoužitelný** — fallback author=white/opponent=black dává inverzní n1/n2 (oba hráči "Anonymous"). Použit offline skript s deterministickými barvami z reportu.
- Opraveny bugy: `coaching_base.py` mitigation lookup (PatternMatch nemá `.mitigation`), `coaching_opponent_pool.py` chybějící klíče n1/n2 v prompt_data.
