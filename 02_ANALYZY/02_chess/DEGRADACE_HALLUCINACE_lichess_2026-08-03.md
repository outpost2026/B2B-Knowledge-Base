# DEGRADACE_HALLUCINACE_lichess_2026-08-03
**Datum:** 2026-08-03 | **Autor:** outpost2026
**Ucel:** Kompletni zprava o pricinach degradace/halucinaci v MCP-lichess pipeline (deterministicka + LLM vrstva)
**Verze:** 1.0

---

## 1. Shrnuti (executive summary)

Partie `CpEDieiZ` (lichess, white, result 1-0) produkovala v single-game reportu false-positive blunder: `Qh4` = 1053 cp. Tato zprava popisuje dva nezavisle koexistujici korenove problemy:

1. **Deterministicka pipeline** (`evaluate_move` v `engine_client.py`) generuje **fyzicky nedeterministicky** vysledky — stejny FEN vraci rozptyl cp_loss 533-1149 (6 behu, rozsah 616 cp). Dva kolizni zdroje pravdy (`evaluate_move` vs `analyze_position`) davaji opacne verdikty pro stejny tah.

2. **LLM model degradace** — opencode bezi na free-tier modelu `deepseek-v4-flash-free` bez explicitni konfigurace. Logy potvrzuji 503 "request queue is full" chyby (08:15:17, 08:42:13). Model produkuje degradovane vystupy: mix jazyku, gramaticky rozpad, halucinovane tokeny.

Klicovy nalez: **neni to pouze "halucinace AI"** — deterministicka pipeline sama generuje false-positive, LLM nasledne aktivne konfabuluje narativ na rozporovych datech.

---

## 2. Deterministicka pipeline — defekty D1-D4

### 2.1. D1: Per-call engine spawn (fyzicky nedeterminismus)

**Soubor:** `engine_client.py:205`
**Root cause:** Commit `4a55f1f` (2026-07-30 16:38) zmenil `evaluate_move` ze sdileneho `get_engine()+lock` na per-call `popen_uci`.

```python
# engine_client.py:205 — D1 defekt
sf_path = _get_sf_path()
engine = chess.engine.SimpleEngine.popen_uci(sf_path)
engine.configure({"Threads": 6, "Hash": 512, "NumaPolicy": "hardware"})
```

**Dopad:** Kazde volani `evaluate_move` spousti novy engine proces. Stockfish s prazdnou hash tabulkou (TT) neni deterministicky — best_move a cp_loss se lisi mezi behy.

**Dukaz (reprodukce):**
| Beh | best_move | cp_loss Qh4 | eval_after Qh4 |
|-----|-----------|-------------|----------------|
| Cache (zamrznuty) | f2c2 | 1053 | — |
| Reprodukce 1 | f2c2 | 1149 | 379 |
| Reprodukce 2 | f2c2 | 716 | 379 |
| Reprodukce 3 | f2c2 | 533 | — |
| Reprodukce 4 | f2c2 | 203 | — |
| Reprodukce 5 | f2c2 | 931 | — |
| Reprodukce 6 | f2c2 | 139 | — |

Rozptyl: 533-1149 cp (rozsah 616 cp). Prumerny cp_loss: ~619.

**Srovnani s `analyze_position` (sdilena engine):**
```python
# engine_client.py:131-145 — sdilena engine (deterministicka)
def analyze_position(fen, depth=0, multipv=3):
    engine = get_engine()  # sdilena instance
    _acquire_analysis_lock()  # mutex
    ...
```
`analyze_position` na stejnem FEN `r4rk1/1p3pbp/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w` vraci:
- Qh4 = rank 1 (+259 cp)
- Qh4 = rank 2 (+400 cp)  
- Qh4 = rank 3 (+341 cp)

**Qh4 je TOP tah dle `analyze_position`, ale `evaluate_move` ho klasifikuje jako 1053 cp blunder.** Dva zdroje pravdy davaji opacne verdikty.

### 2.2. D2: Dva kolizni zdroje pravdy

**Soubory:** `game_analyzer.py:329` vs `game_analyzer.py:376`

```python
# game_analyzer.py:329 — klasifikace tahu (per-move)
eval_result = engine_client.evaluate_move(fen_before, move.uci(), depth=depth)
cp_loss = eval_result["centipawn_loss"]

# game_analyzer.py:376 — BlunderFactSheet (position analysis)
engine_lines_raw = engine_client.analyze_position(
    fen_before, depth=depth, multipv=3
)
```

**Problemy:**
- `evaluate_move` (rada 329) pouziva **novou engine per call** — nedeterministicky
- `analyze_position` (rada 376) pouziva **sdilena engine** — deterministicky
- Klasifikace blunderu (`_classify_move` na rade 181) vychazi z `evaluate_move` cp_loss
- BFS (BlunderFactSheet) vychazi z `analyze_position` multipv
- Vysledek: stejny tah muze byt klasifikovan jako blunder v klasifikaci, ale jako TOP tah v BFS

**Dukaz z cache `CpEDieiZ_white_d14.json`:**
```json
{
  "ply": 45,
  "move_san": "Qh4",
  "centipawn_loss": 1053,
  "classification": "blunder",
  "best_move_uci": "f2c2",
  "engine_lines": [
    {"rank": 1, "move_san": "Qh4", "eval_cp": 262},
    {"rank": 2, "move_san": "Qh4", "eval_cp": 400},
    {"rank": 3, "move_san": "Qh4", "eval_cp": 341}
  ],
  "played_move_rank": 1
}
```

Tah `Qh4` je zaroven blunder (cp_loss=1053) i rank 1 v engine_lines. Tento rozpor je datova anomalia, ktera se dostava do LLM promptu.

### 2.3. D3: cp_loss formule v rozptylovem prostoru

**Soubor:** `engine_client.py:245-248`
```python
if best_player is not None and actual_player is not None:
    cp_loss = max(0, best_player - actual_player)
else:
    cp_loss = 0
```

**Problem:** Formule `best_player - actual_player` pocita rozdil mezi nejlepsim tahem a skutecne hranym tahem. Kdyz je best_move deterministicky rozdilny (D1), a pozice ma hluboke takticke vymeny, muze byt rozptyl best_player/actual_player extremni (>1000 cp), i kdyz hra je stabilne vyhravajici.

**Pripad CpEDieiZ:** eval_before = 1279 (bily vyhrava), Qh4 eval_after = 358 (porad vyhrava). Ztrata 921 cp v absolutnich hodnotach. Ale klasifikace znamena: "z 1279 na 358 = blunder". Realita: bily porad vyhrava s 88.7% win prob.

### 2.4. D4: Zadny sanity check (win position + hanging piece contradiction)

**Soubor:** `game_analyzer.py` — chybi kontrola
**Root cause:** Latentni od zacatku pipeline.

**Logika:** Pokud je partie klasifikovana jako "1-0" (bily vyhrava), a tah je oznacen jako blunder s "hanging piece" popisem, mel by existovat kanar (warning). Zaroven: pokud eval_before > +100 cp (silna vyhoda) a cp_loss > 300, mel by byt flag "pozice porad vyhravajici".

V cache: `eval_before=1279`, `eval_after=358`, `win_prob_after=0.887` — bily porad vyhrava s 88.7% sanci. Ztrata 1053 cp neni "blunder" v kontextu pozice.

---

## 3. LLM model degradace — 503 + free tier

### 3.1. Konfigurace

**Soubor:** `opencode.jsonc` (posledni zmena 2026-08-01)
- `default_agent: "plan"`
- Provider: cerebras (empty), nvidia (nemotron-3-super-120b)
- **Zadny `model` field** — fallback na default
- **Zadny `small_model` field** — compaction bezi na stejnem modelu

**Log potvrzuje:**
```
08:29:53.359Z llm.provider=opencode llm.model=deepseek-v4-flash-free
```

Model = `opencode/deepseek-v4-flash-free` (free tier, bez explicitni konfigurace).

### 3.2. 503 "request queue is full" — 2 potvrzene incidenty

**Zdroj:** `opencode.log`, run `f9a86072`, session `ses_03971901bffeAVj1QfyNBvIqTB`

| Timestamp | Typ | Detail |
|-----------|-----|--------|
| 2026-08-03 08:15:17 | ERROR | `Streaming response failed: [503] The request queue is full.` agent=build mode=primary |
| 2026-08-03 08:42:13 | ERROR | `Streaming response failed: [503] The request queue is full.` agent=plan mode=primary |

Oba incidenty na `deepseek-v4-flash-free` provideru. 503 = server-side rate-limit / queue overflow na free tieru.

### 3.3. Symptomy degradace

Uzivatel popsal vystup jako "1bit model" — typicke pro:
1. **Kvantizace + free tier throttling** — model bezi na minimalnich zdrojich
2. **Context overflow** — dlouhe session bez compaction
3. **Mix jazyku** (CS/EN/ZH) — token generatory ztraci koherenci
4. **Halucinovane tokeny** — "jako kdyz se kouknes na binarni data"
5. **Gramaticky rozpad** — nesouvisle vety, chybejici slovesa

**Korelace s logy:**
- Posledni uspesny krok pred 503: `08:12:52` (zobrazeni cache souboru)
- 503 na `08:15:17` — pravdepodobne prilis dlouha generace na preplnenem serveru
- Restart session na `08:22:16` — novy krok 0

### 3.4. Zaporna zpetna vazba (degradation loop)

```
Free tier preplneny -> 503 timeout
    -> Opencode retry -> znovu free tier
        -> Dlouha session + context kumulace
            -> Model degradace (mix jazyku, halucinace)
                -> Delsi vystupy -> vetsi zatez na server
                    -> Dalsi 503
```

---

## 4. Vzajemne působeni (pipeline + LLM)

Deterministicka degradace a LLM degradace se navzajem amplifuji:

1. **Cache obsahuje rozporova data** — Qh4 = blunder (1053) + rank 1 v engine_lines
2. **LLM dostava tyto data jako kontext** — musi interpretovat rozpor
3. **Degradovany model neni schopen kriticky zhodnotit data** — prijima je bezkontrolne
4. **LLM aktivne konfabuluje narativ** — "visici dama" (neni v engine_lines, neni v board state)
5. **Vysledny report je kombinace false-positive + halucinace** — nelze oddelit

**Pripad CpEDieiZ — rozpad:**
- BlunderFactSheet ply 41: fxg7 (153 cp) — blunder
- BlunderFactSheet ply 45: Qh4 (1053 cp) — blunder
- Report tvrdil: "Qh4 = visici dama" — **konfabulace** (engine_lines: Qh4=rank1, board: queen na h4 neni ohrozena)
- Report slepil dva ruzne ply do jednoho narrativu — **nekoherentni interpretace**

---

## 5. Timeline incidentu

| Datum | Cas | Udalost | Klicovy commit/dokument |
|-------|-----|---------|------------------------|
| 21.07.2026 | — | Package refactor (neutralni) | `99a4e80` |
| 30.07.2026 | — | `depth.py` centralizovan, single_game=14 | `f9f60b5` |
| 30.07.2026 | — | Auto-select depth by time control | `0c4e452` |
| 30.07.2026 | 16:38 | **D1 inject**: evaluate_move -> per-call popen_uci | `4a55f1f` |
| 30.07.2026 | — | Cloud fallback (disabled default) | `de16794` |
| 01.08.2026 | — | Code review: P1-P4 batch, 16 unit testu | `fc5fc69`, `552bc9d` |
| 02.08.2026 | 23:39 | Cache `CpEDieiZ_white_d14.json` vytvoren (zamrznuty 1053) | cache soubor |
| 03.08.2026 | 07:41 | Deep dive reprodukce — potvrzeno D1-D4 | session `f9a86072` |
| 03.08.2026 | 08:15:17 | **503 #1**: "request queue is full" (build agent) | opencode.log:101946 |
| 03.08.2026 | 08:42:13 | **503 #2**: "request queue is full" (plan agent) | opencode.log:102037 |
| 03.08.2026 | 08:29 | Model = deepseek-v4-flash-free (potvrzeno z logu) | opencode.log:101986 |

---

## 6. Doporuzeni

### 6.1. Okamzite (restart)

- **Restart opencode** — vymazani session state, novy context, odstraneni zmrzleho stavu
- Zadny kod se nemeni, jen restart procesu

### 6.2. Kratkodobe (config)

- Pridat explicitni `model` a `small_model` do `opencode.jsonc` — napr. `nvidia/nemotron-3-super-120b-a12b` nebo `cerebras`
- Free tier `deepseek-v4-flash-free` neni spolehlivy pro agenticni prace s dlouhym kontextem

### 6.3. Strednedobe (deterministicka pipeline)

| # | Oprava | Soubor | Priorita |
|---|--------|--------|----------|
| D1 | Reuse shared `get_engine()` + lock misto per-call popen_uci | `engine_client.py:205` | P0 |
| D2 | Single zdroj pravdy — pouzit `analyze_position`/multipv pro klasifikaci i BFS | `game_analyzer.py:329,376` | P0 |
| D3 | Normalizovat cp_loss; pridat confidence interval z rozptylu behu | `engine_client.py:245` | P1 |
| D4 | Sanity check: win position + hanging piece = flag | `game_analyzer.py` | P1 |

### 6.4. Dlouhodobe (testovani)

- Deterministic test suite: 10 FENu, 10 behu kazdy, max rozptyl < 50 cp
- Post-sanity check: kazdy blunder overit oproti `analyze_position` multipv
- Cache invalidation: po oprave D1 prefroznout vsechny cache soubory

---

## 7. Data

### FEN pred Qh4
```
r4rk1/1p3pbp/p7/q2pP3/3B2b1/P7/1P3QPP/1B1R1RK1 w - - 2 23
```

### Tah
- **Ply:** 45 (bily)
- **Move:** Qf2-h4 (f2h4)
- **Eval pred:** +1279 cp (bily vyhrava, 99.9% win prob)
- **Eval po:** +358 cp (bily porad vyhrava, 88.7% win prob)
- **cp_loss (cache):** 1053
- **Classification:** blunder (dle cache)
- **Realita:** Qh4 = TOP tah dle `analyze_position` (+259..+423 cp)

### Engine konfigurace
- Stockfish: `stockfish-bmi2.exe`
- Threads: 6, Hash: 512 MB, NumaPolicy: hardware
- Depth: single_game=14, position=18

### Opencode konfigurace
- Provider: opencode (deepseek-v4-flash-free)
- Zadny explicitni model/small_model
- MCP timeout: 300s (lichess-analyzer)
- Agent: plan (default)

---

## 8. Navazujici dokumenty

- `02_ANALYZY/02_chess/DEEP_DIVE_lichess_Qh4_halucinace_2026-08-03.md` — deterministicky deep dive
- `02_ANALYZY/02_chess/HALUCINACE_BASE_MODEL_lichess_single_game_2026-08-03.md` — base model halucinace
- `04_KNOWLEDGE_BASE/01_MCP/MCP_GROUND_TRUTH_postmortem_agregovany_v1.md` — MCP ground truth

---

*Verze: 1.0 | Datum: 2026-08-03 | Autor: outpost2026*
