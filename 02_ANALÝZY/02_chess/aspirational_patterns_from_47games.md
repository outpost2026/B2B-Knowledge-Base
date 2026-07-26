# Aspiracni patterny z 47 her (2026-07-26)
**Datum:** 2026-07-26 | **Autor:** outpost2026
**Ucel:** Katalog patternu identifikovanych v originalni knihovne (A-Q1), ktere nejsou implementovany, s vyhodnocenim proveditelnosti na 47-hrove datove sade.

## Soucasny stav (feat branch)

| ID | Name | Stav | Detektor |
|----|------|------|----------|
| A | Anonymous effect | Implementovan | `_detect_a` |
| B | Automatic grab | Implementovan | `_detect_b` |
| C | Attention tunneling | Implementovan | `_detect_c` |
| G | Color as modulator | Implementovan | `_detect_g` |
| I | Bait trap | Implementovan | `_detect_i` |
| I2 | Opponent's gift exploitation | Implementovan | `_detect_i2` |
| J | Impulsive check block | Implementovan | `_detect_j` |
| N | X-ray pin violation | **NOVE** (feat) | `_detect_n` |
| O | Repetition avoidance greed | Implementovan | `_detect_o` |
| P | Visual misrecognition | Implementovan | `_detect_p` |
| Q | Active defense | Implementovan | `_detect_q` |
| Q1 | Desperate Gambit Mode | Implementovan | `_detect_q1` |
| Q2 | Win despite blunder | Implementovan | `_detect_q2` |
| R | Endgame relaxation | Implementovan | `_detect_r` |
| S | Capture aversion under check | Implementovan | `_detect_s` |

Celkem: **15 patternu** (14 hlavnich + 1 novy na feat)

## Chybejici patterny (D, E, F, H, K, L, M)

### D -- Controlled vs. Uncontrolled Risk
| Atribut | Hodnota |
|---------|---------|
| **Typ** | dichotomy |
| **Priorita (plan)** | P4 -- odlozeno |
| **Detekce** | Vyzaduje multi-PV analyzu (2+ tahy na pozici) |
| **47 her** | Nedostatecna data -- pattern vyzaduje kognitivni atribuci (umysl vs nahoda) |
| **Bloker** | Multi-PV infrastructure + intent classifier |
| **EROI** | 2/10 |

### E -- Metacognitive Activation
| Atribut | Hodnota |
|---------|---------|
| **Typ** | performance_switch |
| **Priorita (plan)** | P4 -- odlozeno |
| **Detekce** | Vyzaduje casova data + move quality trend |
| **47 her** | Priblizitelne heuristic detection z moznych Lichess timestampu |
| **Bloker** | Nema ground truth bez self-reportu |
| **EROI** | 3/10 |

### F -- Resilience After Mistake
| Atribut | Hodnota |
|---------|---------|
| **Typ** | recovery |
| **Priorita (plan)** | P4 -- odlozeno |
| **Detekce** | Post-blunder okno (3-5 tahu), prumer cp_loss trend |
| **47 her** | ~50-90 blunder eventu -- **dostatecna data** |
| **Bloker** | Castecny prekryv s Q (Active Defense) -- F je pasivni stabilizace |
| **EROI** | 6/10 (implementovatelny, ale nizky signal oproti Q) |

### H -- Systematic Strangulation
| Atribut | Hodnota |
|---------|---------|
| **Typ** | strategy |
| **Priorita (plan)** | P4 -- odlozeno |
| **Detekce** | Vyzaduje positional evaluator (mobilita, space, pawn structure) |
| **47 her** | Extremne vzacne v rapid hrach -- nedostatecna data |
| **Bloker** | Chybi PositionalSqueezeAnalyzer modul |
| **EROI** | 1/10 |

### K -- Passive-Active Role Confusion
| Atribut | Hodnota |
|---------|---------|
| **Typ** | author_error |
| **Priorita (plan)** | P4 -- odlozeno |
| **Detekce** | Move intent classifier + eval-context alignment |
| **47 her** | ~2-4 eventy -- hranicne detekovatelne |
| **Bloker** | Chybi move-type classifier |
| **EROI** | 3/10 |

### L -- Early Queen Exchange for Technical Win
| Atribut | Hodnota |
|---------|---------|
| **Typ** | strategy |
| **Priorita (plan)** | P3 -- blokovano motif detection |
| **Detekce** | Queen trade detection + eval trend before/after |
| **47 her** | ~2-5 strategickych queen exchanges -- **hranicne dostatecne** |
| **Bloker** | `is_tactical_motif` je dead code (vzdy False) -- potreba motif detection engine |
| **EROI** | 5/10 (po odblokovani motif detection) |

### M -- Provocation Sacrifice for Open File
| Atribut | Hodnota |
|---------|---------|
| **Typ** | strategy |
| **Priorita (plan)** | P3 -- blokovano motif detection |
| **Detekce** | Material sacrifice + compensation tracker (eval recovery) |
| **47 her** | ~0-2 eventy -- vysoké FPR |
| **Bloker** | Multi-PV + compensation estimator |
| **EROI** | 2/10 |

## Shrnuti implementacni priority

| Poradi | Pattern | EROI | Zavislost | Poznamka |
|--------|---------|------|-----------|----------|
| 1 | N (X-ray pin) | 9/10 | None | **HOTOVO** na feat |
| 2 | F (Resilience) | 6/10 | None | P4, ale jednoduchy |
| 3 | L (Queen exchange) | 5/10 | Motif detection engine | Blokovano P1 infra |
| 4 | K, E | 3/10 | Move classifier | Nizka priorita |
| 5 | D, H, M | 1-2/10 | Multi-PV, positional eval | Aspiracni |
