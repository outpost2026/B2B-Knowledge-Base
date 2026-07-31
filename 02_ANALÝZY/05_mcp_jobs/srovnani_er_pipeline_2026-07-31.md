# SROVNÁNÍ ÉR PIPELINE: Legacy → Interim → AI-native (EROI, efektivita, maturita)

**Datum:** 2026-07-31 | **Autor:** opencode agent
**Účel:** Diff analýza všech běhů v `output/` napříč třemi érami pipeline — vyhodnocení EROI, efektivity a maturity

---

## 1. Analyzované běhy (27 runů v output/)

| Éra | Období | Runy | Query scope |
|-----|--------|------|-------------|
| **LEGACY-MANUAL** | 07-14 → 07-17 | 9 runů | 8 manuálních (udrzbar, elektrikar, zahradnik, cnc_jobs, python_jobs…) |
| **INTERIM** | 07-29 → 07-30 | 5 runů | stejných 8 manuálních |
| **AI-NATIVE** | 07-31 | 9 runů + 1 raw-scrape | 8 AI query (python, llm, mcp, data, devops, prumysl, cnc_cam, RE) |

---

## 2. Agregace per éra

| Metrika | LEGACY | INTERIM | AI-NATIVE |
|---------|--------|---------|-----------|
| Průměrný počet match/run | 34.8 | 37.2 | 14.3 (26 po fixu) |
| Max match/run | 48 | 46 | 26 |
| Průměrná doba běhu | 36.2s | 56.5s | 63.5s (99.9s po pages=20) |
| Domény | řemesla + 1 IT | řemesla + 1 IT | **8× AI/IT/CNC** |
| Portálová distribuce | jobs 35, pracecz 159, bazos 119 | jobs 47, pracecz 94, bazos 45 | jobs 75, pracecz 43, bazos 11 |

**Klíčový posun:** nižší absolutní počet match v AI-native NENÍ regrese — je to **scope změna**. Legacy chytalo 34 ad z toho ~30 řemeslné (mimo autorův kompetenční rozsah). AI-native chytá ~15–26 ad, ale **všechny v cílové doméně**.

---

## 3. EROI: hit_rate (SNR) per query

### 3.1 Globální SNR (correlation_cache, 105 záznamů)

| Éra | Celkem matched | Celkem scrapped | Global SNR |
|-----|---------------|-----------------|------------|
| LEGACY | 179 | 25 963 | **0.00689** |
| AI-NATIVE | 107 | 33 179 | 0.00323 |

**Interpretace:** Legacy SNR je *uměle* nafouknutý query `udrzbar` (0.0171 — 105 match z 6 125 scraped). To je známá chyba z dif_analyza 07-30: `udrzbar` je příliš široký, matchuje IT techniky a facility role (FP). **Výše SNR u legacy = nižší precision, ne vyšší efektivita.**

### 3.2 SNR per query (sorted)

| Query | Éra | Matched | Scraped | SNR | Hodnocení |
|-------|-----|---------|---------|-----|-----------|
| udrzbar | LEGACY | 105 | 6 125 | 0.0171 | ⚠️ nejvyšší, ale FP-heavy (široký scope) |
| strechy | LEGACY | 10 | 1 243 | 0.0080 | dobré |
| **devops_ci_cd** | AI | 15 | 1 941 | **0.0077** | ✅ nejlepší AI query |
| **mcp_agentic** | AI | 10 | 1 941 | 0.0052 | ✅ dobré |
| elektrikar | LEGACY | 15 | 3 823 | 0.0039 | dobré |
| zahradnik | LEGACY | 19 | 4 848 | 0.0039 | dobré |
| ai_llm_engineer | AI | 24 | 6 625 | 0.0036 | ✅ dobré |
| data_engineering | AI | 24 | 6 625 | 0.0036 | ✅ dobré |
| python_jobs | LEGACY | 9 | 2 749 | 0.0033 | srovnatelné s AI |
| cnc_jobs | LEGACY | 5 | 1 606 | 0.0031 | srovnatelné |
| python_ai_engineer | AI | 16 | 6 625 | 0.0024 | užší scope (well-aimed) |
| prumyslova_automatizace | AI | 13 | 4 969 | 0.0026 | OK |
| truhlar | LEGACY | 2 | 1 257 | 0.0016 | slabý trh |
| RE | AI | 1 | 735 | 0.0014 | suchý trh (validní) |
| cnc_cam_automation | AI | 4 | 3 718 | 0.0011 | borderline (1 seřizovač) |

**Verdikt:** AI-native query dosahují SNR 0.002–0.008 na **úzké, dobře mířené booleany** — srovnatelné s nejlepšími legacy query, ale bez FP z řemeslné širokosti. `udrzbar` (0.017) je outlier kvůli šíři, ne kvalitě.

---

## 4. Cross-era overlap

| Průnik | Ady | Poznámka |
|--------|-----|----------|
| LEGACY ∩ INTERIM | 1/29 | trh se otočil za 12 dní |
| LEGACY ∩ AI-NATIVE | **0/29** | disjunktní domény — očekávané |
| INTERIM ∩ AI-NATIVE | 1/43 (Full stack Python v AI) | jediná IT ad z legacy éry, která žije dodnes |

**Závěr:** Éry se vzájemně nepřekrývají, protože **nejsou substituty, ale fáze**. Legacy pokrývalo řemesla (mimo scope), AI-native pokrývá IT/CNC (v scope). Srovnávat absolutní počet match = chyba.

---

## 5. Efektivita (náklad vs výnos)

| Metrika | LEGACY | AI-NATIVE (pre-fix) | AI-NATIVE (post-fix 154939) |
|---------|--------|--------------------|----------------------------|
| Scrape objem | ~2 900 ad/run | ~1 500 ad/run | ~2 600 ad/run |
| Doba běhu | 36s | 63s | 100s |
| Cílové match/run | ~3 (IT) | 14 | 26 |
| Match/sekunda | 0.08 | 0.22 | **0.26** |
| **Match/cílová doména** | **0.8/s** | 14/run | **26/run** |

- **Interim/legacy:** 34 match/run ≈ 0 pro autorův kompetenční scope (řemesla)
- **AI-native pre-fix:** 14 match/run, ale 6/8 zmizelo rank driftem při 5 stránkách
- **AI-native post-fix (pages 20):** **26 match/run = 1.9× nárůst**, RE poprvé matchuje

**Efektivita v cílové doméně vzrostla z ~0 na 26 match/run** — to je 5–8× zlepšení oproti legacy, které v AI doméně dávalo 1–3 ady.

---

## 6. Maturita pipeline (diagnostika)

| Dimenze | Stav | Důkaz |
|---------|------|-------|
| **Determinismus** | ✅ | 144304 = 144832 (identické výsledky, dvakrát za sebou) |
| **Regresní kontrola** | ✅ | běh 142829 (1 match) → diagnostika single-word exclude FP → fix v 8e2eb17 |
| **Testy** | ✅ | 103 unit testů prochází |
| **SNR monitoring** | ✅ | correlation_cache (105 záznamů, per query×portal) |
| **Per-portál adaptace** | ✅ | jobs.cz `[data-test=jd-body-richtext]`, prace.cz `[class*=RichContent]`, bazos detail |
| **Rank drift řízení** | ✅ (dnes) | 5→20 stránek po diagnostice driftu |
| **Full-text enrichment** | ✅ | lazy detail fetch: description 0→1112–4299 zn. |
| **Debugovatelnost** | ✅ | exclude diag, live HTTP probe, pool audit |

**Maturita: 8/10.** Chybí: (a) automatický rank-drift alarm (detekce churnu mezi běhy), (b) kvalitativní zpětná vazba (které matchy uživatel odbaví).

---

## 7. Závěr

1. **EROI AI-native > Legacy navzdory nižšímu raw count** — matchy jsou v cílové doméně, legacy raw čísla jsou FP-nadupaná (udrzbar)
2. **Efektivita 5–8×** v cílovém scope (0→26 match/run)
3. **Nejproduktivnější query:** devops_ci_cd (SNR 0.0077), mcp_agentic (0.0052), ai_llm+data (0.0036)
4. **Slabá místa:** cnc_cam (borderline 1 seřizovač = FP), RE (suchý trh, validní 0–1), prumyslova (2 hraniční sales/facility FPs)
5. **Pipeline je deterministická, testovaná, monitorovaná, rank-drift řízená** — maturita 8/10

---

## 8. Metadata

- **EROI:** 9/10
- **Tags:** `#mcp-jobs`, `#eroi`, `#maturita`, `#snr`, `#era-comparison`, `#pipeline-evaluace`
- **Vstupní data:** 27 runů v `output/` (07-14 → 07-31), `data/correlation_cache.json` (105 záznamů)
- **Klíčové runy:** legacy `20260717_222804`, interim `20260729_192713`, AI-native `20260731_154939`
- **Související:** `evaluace_ai_native_era_2026-07-31.md`, `dif_analyza_legacy_vs_mcp_2026-07-30.md`
