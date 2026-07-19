# Chess Self-Analysis Baseline — 2026-04

**Datum:** 2026-04-10 | **Zdroj:** `chess_pattern_v5.json` (ruční LLM-asistovaná analýza)
**Autor:** Ondřej Soušek | **Status:** Baseline před MCP automatizací

## Metadata session

| Metrika | Hodnota |
|---------|---------|
| Celkem her | 21 (20 + 1 follow-up 2026-04-12) |
| Výhry | 19 |
| Prohry | 1 |
| Remízy | 0 |
| Blunderů (autor) | 10 |
| Blunderů jako White | 8 |
| Blunderů jako Black | 2 |
| Prům. ELO odhad White | 1950 |
| Prům. ELO odhad Black | 2010 |
| Best game all-time | 2023-04-26 vs GetRolled1342 (2136 ELO, ~2200+) |
| Second best | Game 19 vs john_spyro89 (2127 ELO, 82.8% acc, Chess.com rating 2150) |

## Pattern library (17 patternů, A-Q1)

| ID | Název | Typ | Frekvence |
|----|-------|-----|-----------|
| A | Anonymous effect | trigger | vysoká |
| B | Automatic grab | author_error | vysoká (3×) |
| C | Attention tunneling | mechanism | střední |
| D | Controlled vs. uncontrolled risk | dichotomy | — |
| E | Metacognitive activation | performance_switch | — |
| F | Resilience after mistake | recovery | vysoká |
| G | Color as modulator | stylistic_shift | střední |
| H | Systematic strangulation | strategy | vysoká |
| I | Poison pawn / Bait trap | strategy | vysoká (3×) |
| J | Impulsive check block | author_error | nízká (1×) |
| K | Passive-active role confusion | author_error | nízká |
| L | Early queen exchange for technical win | strategy | nízká (1×) |
| M | Provocation sacrifice for open file | strategy | nízká (1×) |
| N | X-ray pin exploitation | tactic | nízká (1×) |
| O | Repetition avoidance greed | author_error | střední (1× — první loss) |
| P | Visual pattern misrecognition | author_error | nízká (2×) |
| Q | Active defense under material deficit | recovery_strategy | vysoká (2×) |
| Q1 | Desperate Gambit Mode | recovery_strategy | nízká (1×) |

## Klíčové insighty

### Metacognition = +300 ELO
- `metacognition=true` → avg ~1975
- `metacognition=false` → avg ~1675
- Rozdíl 300 ELO bodů je největší páka pro zlepšení.

### White vs Black asymetrie
- Jako White: impulsivní, vyšší blunder rate, ale vyšší win rate v bait trapech
- Jako Black: trpělivý, systematičtější, nižší blunder rate
- Řešení: "Play White as if Black"

### Ritual effectiveness
- "A CO ON?" před každým capture = 100% účinnost když aplikován
- Problém: není aplikován pod tlakem nebo v casual módu
- Řešení: extendovat na ALL critical moves, ne jen captures

### Defenzivní resilience
- Game 20: přežil 33 tahů bez dámy a vyhrál na čas
- Pattern Q1 (Desperate Gambit Mode): z prohrané pozice vytvořit chaos
- Toto je unikátní skill — udržet klid pod tlakem

## Limitace baseline (řešeno MCP automatizací)

| Limitace | Důsledek | MCP řešení |
|----------|----------|------------|
| Ruční zápis 21 her = hodiny práce | Neškálovatelné | Automatický fetch z Lichess API |
| Subjektivní ELO odhady | Nepřesné | Stockfish eval + Lichess rating |
| Žádná SRS | Patterny neprocvičovány | FSRS spaced repetition |
| Žádná historie napříč sessionami | Snapshot, ne trace | KB persistence s timeline |
| Bez engine dat | "Blunder" bez centipawn loss | Stockfish per-move analysis |
