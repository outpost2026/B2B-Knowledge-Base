# Syntetický report — Analýza LinkedIn tržních signálů (v3)

**Autor profilu:** Ondřej Soušek — Systems Integrator (industrial automation, formalizace, reverse engineering, CAM/CNC)
**Zpracováno:** 2026-07-09 (aktualizace v2: 2026-07-07)
**Vzorek:** 59 nabídek (10× v1 + 49× v3 run), Praha/CZ trh, červenec 2026
**Pipeline:** parallel scraping (3 concurrent, 1.5s stagger), 49/50 success (98%), 445s

---

## 1. Přehledová statistika

| Metrika | v2 (07-07) | v3 (07-09) | Δ |
| --- | --- | --- | --- |
| Celkem nabídek | 49 | 59 | +10 |
| 🟢 SLEDOVAT (≥65 %) | 6 | 3 | −3 |
| 🟡 MEDIUM (50–64 %) | 27 | 31 | +4 |
| 🟡 HRANIČNÍ (40–49 %) | 12 | 9 | −3 |
| 🔴 NESLEDOVAT (<40 %) | 4 | 16 | +12 |
| Precision (SLEDOVAT / celkem) | 12.2% | **5.1%** | −7.1pp |
| Mean score | — | 49.0% | — |
| Median score | — | 51.9% | — |
| Míra inženýrských rolí | 82% | 46% (27/59) | −36pp |
| Falešný engineer rate | 0/40 | — | — |

**Klíčový posun:** Precision klesla z 12.2% na 5.1%. Důvod: pipeline nyní scrapuje VŠECHNY saved jobs (50+), včetně IT/AI/enterprise rolí, které nemají průnik s industrial automation profilem. v2 report byl založen na ručně filtrovaném vzorku.

---

## 2. Tech Stack Frequency Matrix (z 59 nabídek)

### CORE (≥4 výskyty)

```
  AI                        ████████████████████████████████████████████████████████████████ 59×
  Git                       ████████████████████████████████████████ 30×
  Python                    ████████████████████████████ 23×
  IoT                       ████████████ 10×
  CI/CD                     ███████████ 9×
  Linux                     █████████ 7×
  CAM                       ████████ 6×
  scripting                 ████████ 6×
  agentic                   ██████ 5×
  GCP                       █████ 4×
  Docker                    █████ 4×
  ETL                       █████ 4×
  data pipeline             ████ 3×
  CNC                       ████ 3×
```

### SECONDARY (2 výskyty)

```
  DevSecOps                 ██ 2×
  REST API                  ██ 2×
  MCP                       ██ 2×
```

### EDGE (1 výskyt)

`ESP32, deployment automation, test automation, middleware`

### Signal-to-Noise Ratio (technologie s ≥2 direct matches)

| Technologie | Výskyt | Z toho SLEDOVAT | SNR |
| --- | --- | --- | --- |
| scripting | 6 | 2 | 33% |
| CNC | 3 | 1 | 33% |
| IoT | 10 | 2 | 20% |
| CAM | 6 | 1 | 17% |
| Linux | 7 | 1 | 14% |
| CI/CD | 9 | 1 | 11% |
| Git | 30 | 2 | 7% |
| Python | 23 | 1 | 4% |
| agentic | 5 | 0 | 0% |
| GCP | 4 | 0 | 0% |
| Docker | 4 | 0 | 0% |
| ETL | 4 | 0 | 0% |
| data pipeline | 3 | 0 | 0% |
| DevSecOps | 2 | 0 | 0% |
| REST API | 2 | 0 | 0% |
| MCP | 2 | 0 | 0% |

**Pozoruhodné:** `scripting` a `CNC` mají nejvyšší SNR (33%). IoT druhý nejvyšší (20%). Tyto dovednosti jsou nejsilnějšími signály pro relevantní role.

---

## 3. Mismatch dimenze (kritické gapy)

| Dimenze | Počet výskytů | Podíl | v2 podíl | Δ |
| --- | --- | --- | --- | --- |
| growth | 52 | 88% | 86% | +2pp |
| tech | 32 | 54% | 41% | +13pp |
| formal | 28 | 47% | 65% | −18pp |
| domain | 20 | 34% | 18% | +16pp |
| location | 12 | 20% | 29% | −9pp |

**Klíčový posun:** `tech` mismatch vzrostl z 41% na 54% — více nabídek požaduje dovednosti mimo profil (C++, Azure, PLC, AWS). `formal` mismatch klesl z 65% na 47% — méně nabídek vyžaduje VŠ titul. `domain` mismatch vzrostl z 18% na 34% — více nabídek mimo industrial automation.

---

## 4. LinkedIn Algorithm Performance

| Metrika | v2 | v3 | Poznámka |
| --- | --- | --- | --- |
| Precision | 12.2% | **5.1%** | Pipeline scrapuje vše, nejen relevantní |
| Noise (mimo doménu) | 47% | ~63% | Enterprise IT + AI/ML + other |
| Falešný engineer rate | 0/40 | — | — |
| Strategický employer rate | 20% | 5% (3/59) | Siemens×3, MSM×2 |

---

## 5. Inferované klastry a patterny

### Klastr 1: Industrial Automation Core (sweet spot)

Python + IoT + CAM + CI/CD → nejvyšší EROI scory
Top scores: #003 Thermo Fisher 76.5%, #013 Siemens 73.6%, #059 Desoutter 65.7%
Tento klastr tvoří jádro autorovy konkurenční výhody. **SNR: 20-33%.**

### Klastr 2: AI/ML Hype (noise)

AI Engineer, ML Developer, Data Science — ~15 nabídek, vesměs MEDIUM až NESLEDOVAT
LinkedIn testuje AI zájem napříč všemi profily. **SNR: 0%.** Ignorovat jako false signal.

### Klastr 3: Enterprise IT (mimo focus)

Solution Architect, SW Developer, DevOps — ~12 nabídek
Většina v MEDIUM/HRANICNÍ pásmu. Nízký crossover do industrial automation. **SNR: 0-7%.**

### Klastr 4: Embedded & Manufacturing (adjacent)

Embedded SW Engineer, FW vývojář, Zkušební technik — role blízké industrial automation
Vyšší fit než enterprise IT, ale nižší než čistě industrial role.

### Klastr 5: Data Engineering (nový)

Data Integration Engineer, Data Pipeline — 4 nabídky
Etl + data pipeline + GCP/Azure. Adjacent k AI/ML, nízký SNR pro industrial profile.

---

## 6. Skill Gaps & CV Optimization

### Nejčastější no-match (gapy)

- **C++**: 15× — nejčastější chybějící skill
- **Azure**: 10× — nejčastější chybějící skill
- **PLC**: 8× — nejčastější chybějící skill
- **AWS**: 7× — nejčastější chybějící skill
- **Kubernetes**: 3× — chybějící skill
- **Terraform**: 3× — chybějící skill
- **TypeScript**: 2× — chybějící skill

### Nejčastější direct match (autorovy silné stránky)

- **Git**: 30× — tržně potvrzená kompetence
- **Python**: 23× — tržně potvrzená kompetence
- **IoT**: 10× — tržně potvrzená kompetence
- **CI/CD**: 9× — tržně potvrzená kompetence
- **Linux**: 7× — tržně potvrzená kompetence
- **CAM**: 6× — tržně potvrzená kompetence
- **scripting**: 6× — tržně potvrzená kompetence
- **agentic**: 5× — tržně potvrzená kompetence

---

## 7. Top 10 nabídek (dle EROI skóre)

| # | Titul | Firma | Skóre | Verdict |
| --- | --- | --- | --- | --- |
| 003 | System Integration Engineer | Thermo Fisher Scientific | 76.5% | SLEDOVAT |
| 013 | Technical Test Engineer / Automation Engineer | Siemens | 73.6% | SLEDOVAT |
| 059 | Light Automation Specialist | Desoutter Tools | 65.7% | SLEDOVAT |
| 007 | AI Integrator / AI Engineer | TD SYNNEX | 64.6% | MEDIUM |
| 026 | Senior Data Integration Engineer | EPAM Systems | 62.9% | MEDIUM |
| 031 | Senior Staff Digital Design Engineer | Renesas Electronics | 62.4% | MEDIUM |
| 024 | Artificial Intelligence Engineer | Carpiness s.r.o. | 62.0% | MEDIUM |
| 046 | DevOps Engineer for Embedded Systems | Adamantem HR | 61.2% | MEDIUM |
| 035 | Solution Architect | Element Logic | 61.0% | MEDIUM |
| 010 | Automation Systems Engineer IoT | Resideo | 60.9% | MEDIUM |

---

## 8. Závěr a doporučení

Ze 59 analyzovaných nabídek: **3 SLEDOVAT** (5.1% precision), **31 MEDIUM**, **9 HRANIČNÍ**, **16 NESLEDOVAT**.

Industrial automation + Python/CAM/IoT zůstává nejsilnější kombinací.
Strategičtí employeři: Siemens (3), MSM GROUP (2), Adamantem HR (2).
AI/ML role jsou konzistentní noise — nenechat se rozptýlit.

### Doporučené akce

- 🔴 Aplikovat na #003 Thermo Fisher (System Integration Engineer, 76.5%)
- 🔴 Aplikovat na #013 Siemens (Technical Test Engineer, 73.6%)
- 🔴 Aplikovat na #059 Desoutter (Light Automation Specialist, 65.7%)
- 🟡 Sledovat #007 TD SYNNEX/AI Integrator (64.6%) — AI integrace do enterprise
- 🟡 Sledovat #046 Adamantem/DevOps for Embedded (61.2%) — DevOps+embedded crossover
- 📊 Precision klesla z 12.2% (v2, 49 nabídek) na 5.1% (v3, 59 nabídek). Důvod: pipeline scrapuje všechny saved jobs, nejen relevantní.
- 📊 Přidat PLC jako dovednost — 8× no_match, přitom klíčová pro industrial automation role.
- 📊 `scripting` a `CNC` mají nejvyšší SNR (33%) — zvážit zvýraznění v profilu.

---

## 9. Pipeline Metadata

| Parametr | Hodnota |
| --- | --- |
| Větev | refactor (74abada) |
| Parallel config | 3 concurrent, 1.5s stagger |
| Duration | 445s (7.4 min) |
| Success rate | 49/50 (98%) |
| KB writes | 49 |
| Git commit | `[ANALÝZY] pipeline: 49 jobs (2026-07-09)` |

---

## 10. Návrh automatizace: syntetický report jako pipeline output

### Současný stav

Report se generuje **ručně** — uživatel spustí pipeline, pak LLM napíše report z `metadata_stacku.json`. Tento krok je repetitivní a kognitivně náročný: člověk musí načíst data, spočítat statistiky, identifikovat klastry, napsat doporučení.

### Cílový stav

Pipeline **automaticky** generuje syntetický report jako finální fázi. Uživatel dostane:
1. JSON report (strojově čitelný, pro další zpracování)
2. MD report (user-friendly, pro člověka)
3. Oba s kompletními statistikami, klastry, SNR tabulkou a doporučeními

### Architektura řešení

```
run_pipeline.py
  ├─ Phase 1-5: scrape → score → KB write (hotovo)
  ├─ Phase 6: git commit (hotovo)
  └─ Phase 7: generate_synthetic_report()  ← NOVÉ
       ├─ Načte metadata_stacku.json
       ├─ Vypočítá: verdict dist, skill freq, SNR, mismatch, clusters
       ├─ Vygeneruje: synthetic_report_{date}.md + .json
       └─ Zapíše do B2B-Knowledge-Base/02_ANALÝZY/00_linkedin/
```

### Implementační kroky

1. **Nový modul:** `src/linkedin_mcp_custom/analysis/report_generator.py`
   - `generate_synthetic_report(entries: list[dict]) -> SyntheticReport`
   - Deterministická část: frequency analysis, SNR, mismatch stats, cluster detection
   - Semi-deterministická část: LLM-powered narrative (volitelné)

2. **Integrace do `run_pipeline.py`:**
   - Nová fáze `generate_report` po `git_commit`
   - Volitelný parametr `--with-llm-report` pro LLM-powered narrative

3. **Integrace do MCP toolu:**
   - Nový tool `generate_report()` — volá se ručně nebo automaticky po batch analýzy
   - Vrací markdown report + cestu k souboru

### Dvě úrovně automatizace

| Úroveň | Popis | Implementation |
|--------|-------|----------------|
| **L1: Deterministický report** | Frequency tables, SNR, mismatch stats, top scores | Python — žádný LLM, ~100 LOC |
| **L2: LLM-enhanced report** | Narativní analýza, klastry, doporučení, reasoning | LLM API call, ~200 LOC |

L1 je priorita — pokryje 80% hodnoty. L2 je enhancement pro později.

---

## 10a. Dev Notes: Sémantická analýza jako klíčová hodnota pipeline

### Princip

LinkedIn pipeline generuje **deterministická/semi-deterministická data**:
- **Deterministická:** job ID, title, company, tech stack (keyword match), EROI skóre (6 dimenzí)
- **Semi-deterministická:** skill gaps (regex match), mismatch dimensions (prahové hodnoty)

Tyto data jsou **bohatá na informace, ale chudá na význam**. Člověk musí:
1. Přečíst 59 nabídek ( ~30 min)
2. Identifikovat patterny ( klastry, trendy )
3. Vyhodnotit relevance (které jsou pro mě důležité?)
4. Napsat akční plán (kam se přihlásit?)

To je **kognitivně náročná, ale repetitivní činnost** — přesně typ úkolu, který LLM zvládá lépe než člověk.

### Hodnota LLM-enhanced analýzy

| Aspekt | Manuální | LLM-enhanced |
|--------|----------|--------------|
| Čas na report | 30-60 min | ~10 min (pipeline + LLM call) |
| Konzistence | Závisí na náladě | Reprodukovatelná |
| Hloubka analýzy | Povrchní (člověk se unaví) | Hluboká (LLM neunaví) |
| Cluster detection | Intuitivní | Systematická (embedding similarity) |
| Reasoning | Omezený working memory | Plný kontext všech 59 nabídek |
| Doporučení | Založená na posledních 5 nabídkách | Založená na celém datasetu |

### Konkrétní přínosy pro tento pipeline

1. **Cross-offer reasoning:** LLM vidí všech 59 nabídek současně. Může říct: "Siemens má 3 nabídky — pokud se přihlásíš na jednu, zvaž i zbylé dvě, protože firma aktivně hledá."

2. **Pattern detection:** "Nabídky s IoT + CAM mají 3× vyšší SNR než nabídky s Python + Git. IoT je silnější signál než Python."

3. **Contextual recommendations:** "Thermo Fisher #003 je nejlepší fit (76.5%), ale MSM GROUP #002 (40.9%) je automotive — méně fit, ale firma má 2 nabídky, což signalizuje růst."

4. **Trend analysis:** "Oproti v2 (07-07) vzrostl tech mismatch z 41% na 54% — trh požaduje více cloud (Azure/AWS) a méně embedded. Zvaž přidání Azure do portfolia."

5. **Anomaly detection:** "Job #059 (Desoutter, 65.7%) je outlier — většina SLEDOVAT jsou velké firmy (Siemens, Thermo Fisher). Desoutter je střední firma, ale má nejvyšší tech fit."

### Technická реализace

```python
# Pseudocode pro LLM-enhanced report
def generate_llm_report(entries: list[dict], stats: ReportStats) -> str:
    prompt = f"""
    Jsi analytik trhu práce. Na základě {stats.total} nabídek z LinkedIn
    pro profil "Systems Integrator (industrial automation, CAM/CNC)":

    Statistiky: {stats.to_dict()}
    Top 10 nabídek: {stats.top_entries}
    Skill SNR: {stats.snr_table}
    Mismatch: {stats.mismatch}

    Napiš:
    1. Shrnutí (3 věty)
    2. Klíčové trendy (5 bullet points)
    3. Doporučené akce (top 5, s reasoningem)
    4. Red flags (co ignorovat)
    5. Skills gap analýza (co se naučit)
    """
    return llm.generate(prompt)
```

### Meta-pozorování

Celá tato pipeline je **meta-příklad** hodnoty automatizace:
- **Vstup:** 59 LinkedIn nabídek (text, strukturovaná data)
- **Deterministický krok:** EROI scoring (6 dimenzí, regex, prahy)
- **Sémantický krok:** LLM analýza (cluster detection, reasoning, recommendations)
- **Výstup:** Syntetický report s high SNR, statisticky bohatý, s doporučeními

 bez LLM kroku musí člověk dělat sémantickou analýzu ručně. S LLM krokem je pipeline **plně automatická** od scrapu po report.

---

*Report aktualizován: 2026-07-09 (v3)*
*Vstupní data: metadata_stacku.json (59 entries)*
*Metodika: EROI scoring (6 dimenzí) + frequency analysis + SNR computation*
*Automatizace: návrh integrace report_generator do run_pipeline.py (Phase 7)*
