# TRIMMING PLÁN — Sémantická optimalizace dokumentace 04_KNOWLEDGE_BASE

**Datum:** 2026-08-01 | **Autor:** outpost2026 | **Verze:** 1.0
**Účel:** Akční plán odlehčení, deduplikace a re-kategorizace doménové dokumentace v B2B-Knowledge-Base/04_KNOWLEDGE_BASE (25 souborů, ~950 KB vč. binárního duplikátu)
**Typ artefaktu:** plán + audit | **Navazuje na:** INDEX.md, AGENTS.md, MANIFEST_AUDIT (TEMP_TRIMMING)
**Umístění v repu:** 01_METODIKY/ (governance plán; 00_STRATEGIE/ je gitignored)

---

## 1. EXEKUTIVNÍ SHRNUTÍ

04_KNOWLEDGE_BASE je doménová vrstva KB s **6 sémantickými redundantními clustery** a **4 bitovými duplicitami** (verifikováno MD5). MCP GT dokument sám sebe deklaruje jako náhradu 4 dalších souborů — ty ale nebyly archivovány. Dva soubory dokumentují stejná KB pravidla ve dvou formách **s konfliktním registrem barev** (epistemický hazard). 1 binární duplikát (docx) zabírá 546 KB bez RAG hodnoty. INDEX.md (2026-06-25) nezaregistruje 8 aktuálních souborů a odkazuje na neexistující adresář.

**Výsledek po aplikaci:** 25 souborů → 10 aktivních v modulu (z toho 1 merge-výsledek) + 2 přesunuty mimo modul + 14 archivovaných, textová úspora ~30 %, binární úspora 100 %, eliminace 6 redundantních clusterů. Žádná informace se neztrácí — vše jde přes _ARCHIVE/ (pravidlo AGENTS.md: žádné mazání).

---

## 2. KATEGORIZACE SNR (všech 25 artefaktů)

### 2.1 Třída A — KANON (hSNR 8-10, zachovat bez změny)

| # | Soubor | KB | SNR | Zdůvodnění |
|---|--------|-----|-----|------------|
| A1 | KNOWLEDGE_CORPUS_VCUTWORKS_LIGHTBURN.md | 17 | 9 | Unikátní GT binárního formátu (offset mapy, 74B segmenty, paleta) — jediný zdroj |
| A2 | RE_CASE_STUDY_VCUTWORKS_LIGHTBURN_v2.md | 17 | 9 | 29denní empirická kronika RE, nulový balast |
| A3 | RE_Methodology.md | 33 | 8 | Přenositelná metodika + validace, používána v 01_METODIKY (INDEX R01) |
| A4 | MCP_GROUND_TRUTH_postmortem_agregovany_v1.md | 90 | 9 | Jediný zdroj pravdy postmortemů (GT-001..042); sám deklaruje supersede 4 souborů |
| A5 | GROUND_TRUTH_VCF_PARSER_ORIGIN_V1.0.json | 24 | 8 | Ontologický GT vzniku parseru; replikace do 3 rep (MD5 shoda) — deliberate, zachovat, deklarovat v INDEXu |
| A6 | High-SNR_knowhow_ML_methodology.json | 12 | 8 | Deterministická pravidla DET_* — jediná kodifikace fyzikálních constraintů |
| A7 | player_pattern_library_v1.json | 13 | 8 | Kánon 17 patternů (chess_pattern_v5 import) — živý zdroj pro lichess-analyzer |

### 2.2 Třída B — KOMPRESE (mSNR 5-7, zachovat po úpravě)

| # | Soubor | KB | SNR | Akce |
|---|--------|-----|-----|------|
| B1 | DEFECT_CATALOG_V1.md | 26 | 7 | Odstranit §9 (srovnání s trhem) a §10 (B2B prodejní argumenty) → nepatří do doménové KB; §8 paleta V7-V13 ponechat (nejúplnější verze) |
| B2 | Dokumentace_Zpracovani_PET_Feltu_v1.0.2.md | 21 | 9 | Sloučit s B3 do jediného kanonického registru; opravit konflikt barev (viz 3.2) |
| B3 | Znalostní báze a produkční ontologie v3.2.md | 7 | 7 | Sloučit s B2 + KB_moduly_RAG (B4) do 1 souboru; eliminuje konflikt barev |
| B4 | KB_moduly_RAG_v1.0.md | 15 | 8 | Sloučit s B2/B3 → jeden soubor "ONTOLOGIE_PET_FELT_RAG_v4" |
| B5 | CI_GitHub_Actions_imerzni_edu_v1.md | 25 | 7 | Přenést do 01_METODIKY/05_testing/ (metodika, ne doménová znalost) |
| B6 | Hluboky_ponor_do_rezerv_Frontiery_vyvoje_MCP_serveru_v1.md | 14 | 5 | Komprimovat na 3-week action plan; odstranit duplicity s GT bod 4 |

### 2.3 Třída C — ARCHIV (low SNR ≤5, přesun do _ARCHIVE/)

| # | Soubor | KB | SNR | Důvod |
|---|--------|-----|-----|-------|
| C1 | Dokumentace_Zpracovani_PET_Feltu_v1.0.2.docx | 546 | 1 | Binární duplikát MD verze, non-RAG, 546 KB zátěž |
| C2 | linkedin_mcp_pitevni_kniha_v1.md | 16 | 6 | Superseded GT (entries 007-024 plně převzaty, sám GT to deklaruje) |
| C3 | mcp_jobs_pitevni_kniha_v1.md | 14 | 6 | Superseded GT (022-035 převzaty) |
| C4 | sdilena_pitevni_kniha_mcp.md | 28 | 6 | Superseded GT (001-028 převzaty) |
| C5 | MCP_komplexni_analyza_a_strategie_v1.md | 51 | 4 | GT převzal postmortem části; zbývá historický kontext adopce (3/2026) |
| C6 | MCP_practical_workflow_guide_v1.md | 17 | 5 | GT převzal §7-8; scénáře popisují tooly s jinými názvy (tool_git_diff aj. neexistují) = zastaralé |
| C7 | SEVERITY_OVERLAY_WARNINGS_DESIGN.md | 7 | 3 | PoC design V1-V6, superseded paletou V1-V13 v DEFECT_CATALOG; implementováno |
| C8 | technicky_stav_vyvoje_operacni_jadro.md | 6 | 3 | Transient snapshot (v31, 2026-06-19); nahrazen reálným stavem kódu + dokumentací rep |
| C9 | player_patterns_Systeq_2026-07-18.json | 0.2 | 2 | Ephemeral výstup match_patterns (1 pattern), nikoli znalost |
| C10 | player_patterns_Systeq_2026-07-19.json | 0.2 | 2 | Ephemeral výstup match_patterns (1 pattern) |
| C11 | DXF_PREDICTIVE_PARSER_METHODOLOGY.md | 21 | 5 | BLUEPRINT plán (ne znalost); části implementovány (viz High-SNR completed); přesunout do _ARCHIVE jako historický návrh NEBO do 01_METODIKY/01_reverse_engineering (rozhodnutí autora, doporučen ARCHIVE) |
| C12 | metodika_pro_vyvoj_nastroju_prumyslove_automatizace.json | 15 | 5 | Meta-metodika (Mikolov komprese) — koncepčně patří do 05_EPISTEMIKA/00_kompresni_realismus, nikoli CNC domény |

---

## 3. IDENTIFIKOVANÉ DUPLICITY A REDUNDANCE

### 3.1 Bitové duplicity (MD5 verifikováno)

| Cluster | Výskyt | Doporučení |
|---|---|---|
| GROUND_TRUTH_VCF_PARSER_ORIGIN_V1.0.json (MD5 5252AF…) | 4×: KB + vcf_integrace + vcf_parser_b2b + web_integrace_systeq/docs | Zachovat (runtime závislosti rep), deklarovat replikaci v INDEXu → **žádná akce v KB** |
| VCF_Reverse_Engineering_Inference_Workflow_2026.md (MD5 DC5F06…) | 2×: KB/01_METODIKY + Vcf-compiler/docs | Zachovat obě (repo zrcadlí kanon), deklarovat v INDEXu → **žádná akce** |

### 3.2 Sémantické duplicity (identifikováno hloubkovým čtením)

| Cluster | Soubory | Charakter | Riziko |
|---|---|---|---|
| RAG ontologie pravidel | KB_moduly_RAG_v1.0.md (v32) + ontologie v3.2.md | Stejná pravidla (H2_12MM, H2_24MM, SEQ_OUTER_LAST, FIX_SMALL_PANEL, GEO_V1_*) ve dvou formách — plná a komprimovaná | Duplicita údržby; v3.2 barvy (Dark Knight, Silver Fox, Camel…) **kolidují** s registrem fDAR/fCAR v Dokumentace v1.0.2 |
| PET felt dokumentace | Dokumentace v1.0.2.md + .docx | MD/DOCX dvojče | Binární balast |
| Pitevní knihy MCP | 3 knihy + 2 strategie vs. GT (GT sám je nahradil) | GT deklaruje supersede — soubory ale zůstaly v active tree | Konfuzní navigace agenta (5 souborů se stejným účelem) |
| CI edukace | 04_KNOWLEDGE_BASE/02_testing/CI_GitHub_Actions vs 01_METODIKY/00_agentni_prace/CI_CD_INTEGRACE_PROTOKOL.md | Stejné téma, různé vrstvy (edukace vs protokol) | Mírný; řešit jen re-kategorizací |

### 3.3 Zastaralé / transient artefakty

- technicky_stav_vyvoje_operacni_jadro.md — snapshot k 19.6.2026, v31; kód ujel (v32+, features/2D_visual_warnigs merged)
- MCP_practical_workflow_guide — tool názvy (tool_git_diff, tool_run_tests) neodpovídají aktuálním toolům cnc-tools
- 2 chess snapshots — 13řádkové výstupy single-run

### 3.4 Meta-problémy

1. **INDEX.md drifuje** — 8 souborů neregistrováno, odkaz na neexistující 03_technologie/technologie_plotr_moodpasta
2. **03_technologie je prázdný** adresář
3. **Konflikt barevného registru** (viz 3.2) = epistemický hazard: RAG vrátí 2 různé pravdy
4. **Cross-repo závislosti** — DXF metodika odkazuje na SYSTEQ_DXF_PREDICTIVE_PARSER_B2B_VISION.md + Průmyslový korpus v1.0.1.docx, které v repu neexistují

---

## 4. FÁZOVÝ PLÁN IMPLEMENTACE (batch operace)

**Pravidla:** každá fáze = 1 batch (max 10 souborů), po každé fázi `git status` + read-after-write verifikace, commit dle AGENTS.md. Žádné mazání — jen přesun do `_ARCHIVE/`. Dočasné soubory jdou přes `_github/TEMP_TRIMMING/`.

### FÁZE 1 — Archív superseded (batch 1: 11 souborů, cca 660 KB)

| Akce | Soubory |
|---|---|
| Filesystem move → `_ARCHIVE/04_KNOWLEDGE_BASE/` + commit deletů | C1 (docx), C2, C3, C4, C5, C6, C7, C8, C9, C10, C11 |

- Poznámka: `git mv` není použitelné — `_ARCHIVE/` i `*.docx` jsou v .gitignore ("exclude z public repa"). Historie zůstává v gitu (staré cesty), archiv žije na disku.

- Verifikace: `git status` čistý po commitu, Test-Path na archivu
- Commit: `[TRIM] archive: superseded MCP knihy + PoC + snapshoty + docx (F1)`

### FÁZE 2 — Sémantický merge (batch 2: 4 soubory → 1)

| Akce | Soubory |
|---|---|
| Sloučit KB_moduly_RAG + ontologie v3.2 + Dokumentace v1.0.2 → **ONTOLOGIE_PET_FELT_RAG_v4.0.md** (jeden registr barev fDAR…, pravidla RULE_*, materiálová ontologie) | B2, B3, B4 |
| Originály → _ARCHIVE (git mv, zachování historie) | |

- Verifikace: grep konfliktních barev (Dark Knight vs fDAR) → 0 výskytů v aktivních souborech
- Commit: `[TRIM] merge: PET felt ontologie 3 soubory -> 1 (F2)`

### FÁZE 3 — Re-kategorizace (batch 3: 3 soubory)

| Akce | Soubory |
|---|---|
| `git mv` CI_GitHub_Actions → `01_METODIKY/05_testing/` | B5 |
| `git mv` metodika_pro_vyvoj → `05_EPISTEMIKA/00_kompresni_realismus/` | C12 |
| DEFECT_CATALOG komprese (odstranit §9-10, 40+ řádků) | B1 |
| Hluboky_ponor → komprimovat na akční plán (3 sekce) | B6 |

- Commit: `[TRIM] move: re-kategorizace + komprese (F3)`

### FÁZE 4 — INDEX regenerace + governance (batch 4)

| Akce | Detail |
|---|---|
| INDEX.md regenerace | Zaregistrovat 25 souborů aktuálního stavu (aktualní po trim), odstranit neexistující 03_technologie odkaz |
| Smazat prázdný 03_technologie | `git rm` prázdného adresáře (git nesleduje prázdné diry — stačí odstranit) |
| Deklarace replikací | GROUND_TRUTH json (4×), Inference Workflow (2×) — poznámka v INDEXu |

- Commit: `[TRIM] index: regenerace INDEX.md + governance (F4)`

### FÁZE 5 — Validace + KPI gate (batch 5)

- `git status` — čistý strom; `git log` — 4 trim commity
- KPI check: 25 → 12 souborů, ~950 KB → ~330 KB, 0 konfliktů barev
- Report do `_github/TEMP_TRIMMING/` + odstranění temp souborů
- Commit: `[TRIM] done: KPI report (F5)`

---

## 5. CÍLOVÝ STAV — 04_KNOWLEDGE_BASE po trimmování

```
04_KNOWLEDGE_BASE/
├── 00_CNC_CAM/
│   ├── KNOWLEDGE_CORPUS_VCUTWORKS_LIGHTBURN.md      [KANON]
│   ├── ONTOLOGIE_PET_FELT_RAG_v4.0.md               [MERGE: B2+B3+B4]
│   ├── DEFECT_CATALOG_V1.md                         [KOMPRESE]
│   └── High-SNR_knowhow_ML_methodology.json         [KANON]
├── 01_MCP/
│   └── MCP_GROUND_TRUTH_postmortem_agregovany_v1.md [KANON]
├── 01_reverse_engineering/
│   ├── RE_CASE_STUDY_VCUTWORKS_LIGHTBURN_v2.md      [KANON]
│   ├── RE_Methodology.md                            [KANON]
│   └── GROUND_TRUTH_VCF_PARSER_ORIGIN_V1.0.json     [KANON, replikace]
└── 02_chess/
    └── player_pattern_library_v1.json               [KANON]
```

*(Přesuny mimo modul: CI doc → 01_METODIKY/05_testing, metodika Mikolov → 05_EPISTEMIKA, DXF blueprint → _ARCHIVE)*

---

## 6. ZDŮVODNĚNÍ (proč tyto akce)

| Akce | Princip | Očekávaný přínos |
|---|---|---|
| Archivace 9 souborů | Žádné mazání, ale 4 pitevní knihy má nahrazovat 1 GT — 5 souborů = 5 cest k RAG konfuzi | Odstranění ~155 KB duplicitní textové režie; agent naviguje k 1 zdroji |
| Merge PET felt ontologie | Konflikt registru barev = dvě pravdy v RAG; jeden kanon = jedna pravda | Odstranění epistemického hazardu; ušetří údržbu 3 souborů → 1 |
| docx → archive | Binární duplikát bez RAG hodnoty, 546 KB | 100% binární úspora; RAG indexace rychlejší |
| Re-kategorizace CI/Mikolov | Doménová KB ≠ metodika/edukace; 05_EPISTEMIKA = epistemické rámce | Sémantická čistota modulů; hSNR při kb_search |
| INDEX regenerace | INDEX je navigační vrstva; drift = ztracený čas agenta | Orientační přesnost 100 % |

---

## 7. RIZIKA A MITIGACE

| Riziko | Pravděpodobnost | Mitigace |
|---|---|---|
| Ztráta unikátní informace při merge | Střední | Merge provést v TEMP_TRIMMING, diff proti originálům (git diff), schválení autora |
| Cross-repo odkazy na DXF metodiku | Nízká (žádné runtime závislosti) | grep napříč repy před archivací — verifikováno: pouze INDEX.md reference |
| Regrese INDEX.md | Nízká | Verze 2.0 s datem, diff kontrola |
| Autor chce zachovat pitevní knihy | Střední | Phase 1 je reverzibilní (git mv zpět); rozhodnutí na autorovi |

---

## 8. METRIKY ÚSPĚCHU (KPI)

| Metrika | Start | Cíl |
|---|---|---|
| Počet souborů 04_KNOWLEDGE_BASE | 25 | 12 |
| Textový objem | ~401 KB | ~280 KB (-30 %) |
| Binární objem | 546 KB | 0 KB |
| Konfliktních registrů barev | 1 | 0 |
| INDEX drift (neregistrované soubory) | 8 | 0 |
| Duplicitních clusterů | 6 | 0 |

---

*Plán je živý dokument. Schválení autorem = gate pro spuštění Fáze 1. Verifikace auditu: MANIFEST_AUDIT_04_KNOWLEDGE_BASE.md v TEMP_TRIMMING.*
