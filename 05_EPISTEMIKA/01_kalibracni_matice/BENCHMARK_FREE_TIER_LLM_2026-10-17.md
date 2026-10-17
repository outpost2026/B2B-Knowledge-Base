# Benchmark free-tier LLM modelů (opencode ZEN)

**Datum:** 2026-10-17 | **Autor:** outpost2026
**Účel:** Kvantitativní srovnání 4 free-tier modelů (deepseek-v4.1, glm-5.3, mimo-v2.6, longcat-2.5) na agentních dev úlohách T1–T4 jako podklad pro routing.

---

## 1. Metodika

**Protokol:** 1 test = 1 nová session (izolace paměti i kontextu). Běh přes `opencode run --attach` na běžící desktop server; marker testu je v uživatelské zprávě, verifikace se čte z `opencode.db` (ne z textu odpovědi).

**Prostředí:** opencode desktop 1.19.1 + portable CLI 1.19.3 (`.tools/opencode`). Free tier je vázán na klienta (raw CLI vrací 403 „can only be used from within OpenCode") → obcházeno attach na lokální server desktopu.

| ID | Zaměření | Vstup → Výstup |
|----|----------|----------------|
| T1 | API latence / dostupnost | smyčka 12× `Get-Date` → bench-report JSON |
| T2 | spec → implementace | `work/T2/bench_impl.py` (pytest grader) |
| T3 | bugfix + iterace | oprava `work/T3/broken_module.py` (pytest grader) |
| T4 | tool/MCP integrita | bench-report JSON (ACI 7 + první řádek CONTEXT_REPOS.md) |

**Metriky (RUBRIC M1–M12):** correctness `C` (0/100), reliability `R = clamp(100 − (5·api_errors + 3·rate_limit_hits + 2·tool_errors), 0, 100)`, speed `S`, efficiency `E`.
`Composite = 0.50·C + 0.25·R + 0.15·S + 0.10·E`.

**Anti-fabricace (T1):** correctness = 100 jen když `report.n == 12` **a** reálný počet volání `Get-Date` ≥ 12; jinak 0. Zamezilo průchodu modelu, který opsal šablonu bez vykonané práce.

**Rozsah:** 16 běhů (4 modely × 4 testy), 1 běh na buňku.

---

## 2. Výsledky

### 2.1 Souhrn per model

| Model | Pass | Mean comp | Mean correct | API errors | Mean avail | Mean wall |
|-------|------|-----------|--------------|------------|------------|-----------|
| `deepseek-v4.1-flash-free` | 4/4 | **100.0** | 100 | 0 | 1.00 | 45.4 s |
| `mimo-v2.6-flash-free` | 4/4 | **98.8** | 100 | 0 | 1.00 | 48.2 s |
| `longcat-2.5-preview-free` | 4/4 | **91.5** | 100 | 0 | 1.00 | 89.1 s |
| `glm-5.3-flash-free` | 3/4 | **67.7** | 75 | 32 | 0.44 | 109.8 s |

### 2.2 Detail per test

| Test | Model | Verdict | Comp | Corr | Wall (s) | Turns | API | API err | Avail |
|------|-------|---------|------|------|----------|-------|-----|---------|-------|
| T1 | deepseek-v4.1 | PASS | 100.0 | 100 | 60.5 | 14 | 15 | 0 | 1.00 |
| T1 | mimo-v2.6 | PASS | 97.7 | 100 | 86.2 | 13 | 14 | 0 | 1.00 |
| T1 | longcat-2.5 | PASS | 92.6 | 100 | 130.1 | 13 | 14 | 0 | 1.00 |
| T1 | glm-5.3 | **FAIL** | 31.4 | **0** | 113.6 | 10 | 21 | **12** | 0.43 |
| T2 | deepseek-v4.1 | PASS | 100.0 | 100 | 69.8 | 4 | 5 | 0 | 1.00 |
| T2 | mimo-v2.6 | PASS | 98.3 | 100 | 58.6 | 6 | 7 | 0 | 1.00 |
| T2 | longcat-2.5 | PASS | 91.4 | 100 | 111.0 | 5 | 6 | 0 | 1.00 |
| T2 | glm-5.3 | PASS | 77.8 | 100 | 154.7 | 6 | 15 | 9 | 0.40 |
| T3 | deepseek-v4.1 | PASS | 100.0 | 100 | 42.7 | 5 | 6 | 0 | 1.00 |
| T3 | mimo-v2.6 | PASS | 100.0 | 100 | 35.0 | 5 | 6 | 0 | 1.00 |
| T3 | longcat-2.5 | PASS | 91.4 | 100 | 81.5 | 5 | 6 | 0 | 1.00 |
| T3 | glm-5.3 | PASS | 78.0 | 100 | 115.1 | 7 | 14 | 7 | 0.50 |
| T4 | deepseek-v4.1 | PASS | 100.0 | 100 | 8.5 | 2 | 3 | 0 | 1.00 |
| T4 | mimo-v2.6 | PASS | 99.2 | 100 | 12.9 | 2 | 3 | 0 | 1.00 |
| T4 | longcat-2.5 | PASS | 90.7 | 100 | 33.7 | 2 | 3 | 0 | 1.00 |
| T4 | glm-5.3 | PASS | 83.5 | 100 | 55.6 | 2 | 7 | 4 | 0.43 |

---

## 3. Interpretace

- **deepseek-v4.1** — nejrychlejší (45 s ) + 100 % správnost + 0 chyb → jednoznačný default.
- **mimo-v2.6** — kvalitou rovnocenný (correctness 100 %, comp 98.8), ~6 % pomalejší; jediný rate-limit hit (T4). Plnohodnotná alternativa.
- **longcat-2.5** — 100 % správnost, 0 chyb, ale ~2× pomalejší (89 s); vhodný pro propustnost/dávky, ne pro rychlou interakci.
- **glm-5.3** — jediný FAIL (T1) a celkově nejnižší comp. Příčinou jsou **API errors (32 celkem, dostupnost 0.44)**, ne schopnost modelu: kde odpověděl, měl correctness 100 %. **Hypotéza (P≈0.7): transientní rate-limit / síťová chyba dané route, nikoli kapacita modelu.** Nutné ověřit re-runem.

---

## 4. Implikace pro use case (agentní dev: MCP servery, VCF RE, Python, KB)

| Role | Model | Odůvodnění |
|------|-------|-----------|
| Interaktivní agentní dev (default, free) | `deepseek-v4.1` | 100 % + nejnižší latence + 0 chyb |
| Paralelní / 2. volba | `mimo-v2.6` | stejná kvalita, mírně pomalejší |
| Dávkové / nekritické na čas | `longcat-2.5` | vysoká spolehlivost, nízká rychlost |
| Vyhnout se jako default | `glm-5.3` | 32 API chyb → riziko zaseknutí / retry smyčky |
| Dlouhý kontext (netestováno zde) | Nemotron 3 Ultra | fallback dle routing matice |

**Praktické:** pro iterativní smyčku (edit → test → fix), MCP pipeline a VCF RE držet `deepseek-v4.1`; GLM nasadit jen tam, kde je retry bezpečný a latence nevadí.

---

## 5. Limity

- **1 běh / buňku** → metriky S a E triviální (100); run-to-run variance nezměřena.
- Free tier má proměnlivou dostupnost; GLM výsledek může být artefakt časového okna.
- T1–T4 měří **agentní dev** schopnosti, ne hluboký reasoning ani dlouhý kontext.
- Wall clock zahrnuje i lokální overhead (i5-8350U, 8 GB RAM).

---

## 6. Další kroky

- **Re-run GLM** (2×) → rozlišení transient vs. systematická chyba.
- **2. plný běh matice** → smysluplné S/E a variance.

---

## Reference

- Kit: `_github/llm-bench/` — `README.md`, `RUBRIC.md`, `analyze.py`, `run_matrix.ps1`, `results.csv`.
- Raw výstupy: `_github/llm-bench/runs/`.
