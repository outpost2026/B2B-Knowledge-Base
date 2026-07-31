# EVALUACE AI-NATIVE ÉRY: 6 běhů, 3 portály, rank drift

**Datum:** 2026-07-31 | **Autor:** opencode agent
**Účel:** Statistické vyhodnocení efektivity MCP-Jobs pipeline v AI-native konfiguraci (config.yaml 8 query), per-portálová analýza chování, diff proti historickým běhům

---

## 1. Kontext měření

| Parametr | Hodnota |
|----------|---------|
| Konfigurace | `config.yaml` — 8 AI-native query (kompletní rewrite 2ace484 + kalibrace d72c6a2, 632ff47, ce51888) |
| Feature | Solution B (lazy detail fetch) aktivní od běhu 144304 (commit 8e2eb17) |
| Portály | jobs.cz (Praha 5 str., Brno 2 str.), prace.cz (Praha 25 str.), bazos (15+15 str., okr. 18000) |
| Měřené běhy | 6 běhů 2026-07-31 11:04 → 14:49 |
| Regression | Běh 142829 (14:29) = 1 match → REGRESE (diagnostikováno: single-word exclude na description); opraveno v 8e2eb17 |

---

## 2. Souhrn běhů

| Běh | Total | Uniq ads | jobs | pracecz | bazos | Poznámka |
|-----|-------|----------|------|---------|-------|----------|
| 110403 | 10 | 8 | 10 | 0 | 0 | prvotní, pracecz bez Fix A |
| 113158 | 13 | 10 | 13 | 0 | 0 | prumyslova_automatizace přidána |
| 115354 | 14 | 11 | 8 | 6 | 0 | prace.cz začala chytat (Fix A-D) |
| 120022 | 15 | 12 | 8 | 7 | 0 | baseline (bez Solution B) |
| 142829 | **1** | 1 | 1 | 0 | 0 | **REGRESE** — exclude FP na full-text |
| 144304 | 14 | 8 | 7 | 7 | 0 | Solution B + matcher fix |
| 144832 | 14 | 8 | 7 | 7 | 0 | fresh re-run (identický s 144304) |

**Verifikace fixu:** 144304 = 144832 (úplná identita výsledků) → matcher fix je deterministický, regrese vyřešena.

---

## 3. Dif: 120022 (baseline) vs 144832 (Solution B)

### 3.1 Co zmizelo (6 ad) — RANK DRIFT, ne regrese

| Ad | Query | Živost | Pozice v poolu |
|----|-------|--------|----------------|
| Data Analyst | Praha | data_engineering | **žije** (HTTP 200) | str. 14 |
| Automotive CI/CD Engineer (Digiteq) | devops_ci_cd | **žije** | str. 14 |
| Python SW Engineer AI Security (ESET) | python+ai_llm | **žije** | str. 13 |
| Medior M365 & Copilot | mcp_agentic | **žije** | str. 13 |
| Aplikační inženýr Kubernetes (Státní pokladna) | devops_ci_cd | **žije** | str. 13 |
| AI Architect (Gen Digital/Avast) | ai_llm_engineer | **žije** | str. — |

**Verdikt: VŠECHNY zmizelé ady jsou stále živé na portálu.** Důvod: jobs.cz řadí ady dynamicky (boosted/featured pozice + datum). Běh stahuje **5 stránek = 150 ad** z ~600 dostupných na Praha. Perzistentní relevantní ady (ESET, Medior, Kubernetes) se přesunuly na stránky 13–14 a vypadly z rozsahu.

**Důkaz:** pool 20 stránek = 600 ad, 77 IT-relevantních, z toho jen 17 na prvních 5 stránkách. 5 stránek pokrývá jen **22 %** IT inzerátů jobs.cz Praha.

### 3.2 Co přibylo (2 ad)

| Ad | Query | Poznámka |
|----|-------|----------|
| Data Engineer Big Data (ADASTRA) | data_eng+devops | nová, popsáno 4234 zn. |
| SW Developer Network Automation & AI | ai_llm_engineer | nová |

### 3.3 Solution B dopad (description enrichment)

Přeživší ady dostaly description: 0 → 1112–4299 znaků. Exclude nyní vidí full-text, ale bez FPs (multi-word fraze na description, single-word jen na title).

---

## 4. Per-portálové chování (MCP pipeline)

| Portál | Avg match/run | Rozptyl | SNR (avg hit_rate) | Pool | Hodnocení |
|--------|---------------|---------|--------------------|------|-----------|
| **jobs.cz** | 6.0 | 3–10 (vysoký) | **0.00842** (n=32) | 201 ad | nejkvalitnější zdroj, ale **rank drift = nestabilní** |
| **prace.cz** | 3.5 | 0–6 | 0.00149 (n=19) | 958 ad | stabilní záchyt, nízké SNR (široký pool) |
| **bazos** | **0.0** | 0 (konstantní) | — | ~600 ad | **0 match v AI-native éře** — dead portal pro IT |

### 4.1 bazos = 0 match (konstantní napříč 6 běhů)

- bazos Praha pool = montáže, rozvozy, stavební práce, brigády (viz pool_check: 20/20 vzorků = dělnické profese)
- IT/AI/CNC inzeráty se na bazos Praha prakticky nevyskytují
- **Závěr:** bazos je dead portal pro AI-native scope. Otázka: deaktivovat, nebo ponechat jako pojistku pro cnc/prumysl?

### 4.2 jobs.cz = high-SNR, ale rank drift

- **Nejvyšší hit_rate ze všech portálů** (0.00842) — boolean query míří přesně
- Ale záchyt je **churn-heavy**: 6/8 uniq ads v 110403 nejsou v 144832 (ne zmizely z trhu, ale z 5-stránkového rozsahu)
- **Doporučení:** zvýšit jobs.cz Praha na 15–20 stránek pro pokrytí driftu (5 str. = 22 % IT pokrytí)

### 4.3 prace.cz = stabilní, nízké SNR

- Hit_rate 0.00149 (5× nižší než jobs) — prace.cz má obří pool (958 ad avg)
- Ale záchyt stabilní: PLC programátoři (2), Python & Product Engineer, Brigádník Junior Data — přežily 4/6 běhů
- prace.cz je **jediný zdroj CNC** (seřizovač vstřikolisů) — nenahraditelná pro cnc_cam_automation

---

## 5. Churn / persistence analýza (6 běhů)

| Metrika | Hodnota |
|---------|---------|
| Unikátní ad napříč 6 běhů | 19 |
| Perzistentní (≥3 běhy) | 11 (58 %) |
| Tranzientní (1 běh) | 1 (5 %) |

**Perzistentní jádro (stabilní záchyt):**
- Full stack Developer - Python v AI (jobs) — **6/6 běhů**, 4 query zároveň (python+llm+mcp+data)
- Data Analyst | Praha, Automotive CI/CD, Python & Product Engineer, Brigádník Junior Data, PLC×2 — 4/6
- ESET AI Security, Medior Copilot, Kubernetes, seřizovač — 3/6

**Klíčový poznatek:** 11 ad tvoří stabilní jádro relevantního trhu. Churn je způsoben **rozsahem stránkování (5 str.)**, ne kvalitou matcheru.

---

## 6. Multi-query overlap (1 ad = více query)

| Ad | Query overlap | Hodnocení |
|----|---------------|-----------|
| Full stack Developer - Python v AI | **python+llm+mcp+data (4)** | správně — startup AI agenti/multiagenti, RAG, LLM |
| Python & Product Engineer (Skip Pay) | python+llm (2) | správně |
| Brigádník Junior Data & AI | llm+data (2) | správně (hraniční: brigádník) |
| Data Engineer Big Data | data+devops (2) | správně (Big Data + pipeline) |

Overlap je sémanticky korektní — bez zjevných FP.

---

## 7. Per-query výkon (144832)

| Query | Matches | Hodnocení |
|-------|---------|-----------|
| ai_llm_engineer | 4 | nejproduktivnější |
| data_engineering | 3 | solidní |
| python_ai_engineer | 2 | užší (dobře mířený) |
| prumyslova_automatizace | 2 | PLC programátoři = správný záchyt |
| mcp_agentic | 1 | malý trh, očekávané |
| devops_ci_cd | 1 | podzáchyt (Kubernetes ad mimo 5 str.) |
| cnc_cam_automation | 1 | seřizovač vstřikolisů (borderline FP) |
| reverse_engineering | **0** | suchý trh — očekávaný výstup |

**reverse_engineering = 0** je validní (trh nemá "reverse engineer" pozice na CZ portálech v rámci rozsahu), ne chyba.

---

## 8. Závěr a doporučení

### Co se změnilo mezi 120022 a 144832
1. **Solution B enrichment**: description 0→1112–4299 znaků u přeživších ad — matcher vidí full-text
2. **Matcher fix**: single-word exclude → title-only (odstraněna regrese 142829)
3. **Zmizení 6 ad ≠ regrese**: rank drift jobs.cz (ad žijí na str. 13–14, mimo 5stránkový rozsah)

### Doporučení (řazeno dle EROI)

| # | Akce | EROI | Důvod |
|---|------|------|-------|
| 1 | **jobs.cz Praha pages 5→20** | 9/10 | 5 str. = 22 % IT pokrytí; ESET/Medior/K8s ady unikají driftem |
| 2 | **bazos deaktivace pro AI query** (ponechat pro cnc/prumysl?) | 8/10 | 0 match v 6 bězích = 0 EROI na scraping ~600 ad/běh |
| 3 | Sledovat RE přes portálový search místo boolean | 5/10 | CZ trh nemá RE pozice v bullet rozsahu |
| 4 | Snížit pracecz pages 25→15 (při rostoucím poolu) | 4/10 | pool 958 ad, hit_rate 0.00149 — diminishing returns |

---

## 9. Metadata

- **EROI:** 8/10
- **Tags:** `#mcp-jobs`, `#evaluace`, `#rank-drift`, `#snr`, `#ai-native-era`, `#per-portal`
- **Vstupní data:** `output/etl_20260731_110403..144832.json` (6 běhů), `data/correlation_cache.json` (95 záznamů), live HTTP probe 8 URL
- **Pipeline:** fresh re-run 144832 (73.5s, 14 match)
- **Související:** `config.yaml` (8 query), `matcher.py` (has_exclude_terms fix), commit 8e2eb17
