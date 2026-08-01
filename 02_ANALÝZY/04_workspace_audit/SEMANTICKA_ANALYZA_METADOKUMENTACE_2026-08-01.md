# SEMANTICKÁ ANALÝZA INFLACE METADOKUMENTACE — B2B-Knowledge-Base (repo-wide)

**Datum:** 2026-08-01 | **Autor:** outpost2026 (agent, dle vlákna trimming)
**Typ:** analýza / audit | **Rozsah:** celý repozitář (7 modulů, ~159 souborů na disku, ~3.8 MB)
**Účel:** identifikace inflačních clusterů metadokumentace (duplicity, superseded verze, transient work-process artefakty, raw data, prázdné soubory) + návrh trimming plánu
**Návaznost:** TRIMMING_PLAN_04_KNOWLEDGE_BASE_2026-08-01.md (F1-F5 done), INDEX.md v2.0

---

## 0. METODIKA

- Sémantická klasifikace každého souboru: K (keep/canonical), D (duplicitní 100%), S (superseded verze), T (transient/work-process), R (raw data), M (meta o dokumentech/procesu), E (prázdný), B (binárka)
- Duplicity ověřeny MD5 hash, supersession podle obsahu + verzí v hlavičce
- Dvouvrstvá architektura: **public (git-tracked, 86 souborů)** vs **lokální (gitignored)** — viz .gitignore:46-49

## 1. ARCHITEKTURA REPO (2 VRSTVY)

| Vrstva | Rozsah | Soubory | Obsah |
|--------|--------|---------|-------|
| **Public (git)** | 01_METODIKY (18), 02_ANALÝZY (31), 04_KNOWLEDGE_BASE (10), 05_EPISTEMIKA (21), root (4) | **86** | Metodiky, analýzy, doménová znalost |
| **Lokální (gitignored)** | 00_STRATEGIE (29), 03_PROVOZ (19), _ARCHIVE (20), 02_ANALÝZY/01_portfolio_audit (5), *.docx/pdf (6) | **~79** | Strategie/GT, business/provoz, archiv, binárky |

> Důsledek: inflace v lokální vrstvě nezatěžuje public repo, ale zatěžuje workspace; trimming pro trackované soubory = filesystem move + commit deletů (pattern z F1).

## 2. KVANTITATIVNÍ PŘEHLED

| Modul | Souborů | Velikost | Z toho inflace (kandidáti) |
|-------|---------|----------|---------------------------|
| 00_STRATEGIE (lokální) | 29 | 421 KB | 8 (2×D pár, roadmap v1, 4× handoff, index_Github) |
| 01_METODIKY (public) | 18 | 178 KB | 5 (4× CV stará generace, workflow json) |
| 02_ANALÝZY (public+lok) | 42 | 1481 KB | ~20 (synteticky snapshoty, dev notes, audit řetězce, workspace audit) |
| 03_PROVOZ (lokální) | 19 | 397 KB | 4 (exec v1, VCF handoff v1, transkript duál, emaily) |
| 04_KNOWLEDGE_BASE (public) | 10 | 247 KB | 0 (již trim F1-F5) |
| 05_EPISTEMIKA (public) | 21 | 239 KB | 6 (2×D manifest, OpenRouter v2, ontologie base, semanticka analyza, LLM_free_models 0B) |
| _ARCHIVE (lokální) | 20 | 817 KB | — (archiv, neaktivní) |

## 3. INFLACE CLUSTERS (DETAIL)

### 3.1 Duplicity 100% (MD5 identické) — 8 souborů → 4 kanonické
| Pár | MD5 | Kanon (zachovat) | Duplikát (archiv) |
|-----|-----|------------------|-------------------|
| Mikolov_Manifest / _KB | 7DC8AE53 | `00_STRATEGIE/00_manifesty/Mikolov_Manifest.md` (lokální) | `Mikolov_Manifest_KB.md` |
| Mikolov_Sousek_prunik / _KB | E790839A | `.../Mikolov_Sousek_prunik.md` | `Mikolov_Sousek_prunik_KB.md` |
| Sousek_Manifest_kompresniho_realismu.json / 05_EPISTEMIKA _KB.json | 4F48E342 | `00_STRATEGIE/00_manifesty/...realismu.json` | `05_EPISTEMIKA/00_kompresni_realismus/..._KB.json` (tracked!) |
| Sousek_Manifest_B2B_Edition.json / 05_EPISTEMIKA v1.1.json | A610FA53 | `00_STRATEGIE/...B2B_Edition.json` | `05_EPISTEMIKA/..._v1.1.json` (tracked!) |

### 3.2 Versioned superseded (stará verze zůstala) — 9 souborů
| Stará (archiv) | Nová (kanon) |
|----------------|--------------|
| roadmap_github.md | roadmap_github_v2.md |
| OpenRouter_Model_Analysis_v2.md | OpenRouter_Model_Analysis_v3.md |
| executive_summary_moodpasta.md | executive_summary_moodpasta_v2.md |
| VCF_Parser_SYSTEQ_handoff.json (v1.0) | VCF_Parser_SYSTEQ_bussiness_value.json (v2.0, executive_ready) |
| synteticky_report_analyza.md (v3) | synteticky_report_2026-07-09.md (v4) |
| CV_Ondrej_Sousek_B2B_onepager.md + _en | 01-04 one-pagery (kanonická sada) |
| CV_Ondrej_Sousek_redesign.md | 07_design-implementation-guide (sada 01-07) |
| Sousek_CV_portfolio_cs.md | sada 01-07 |
| ontologie_kompresnich_modelu_reality.md (base) | _appendix (final RAG verze, "připravený finální MD") |

### 3.3 Transient / work-process artefakty — ~17 souborů
- **Lichess-MCP dev proces v KB:** chess_diagnosis_07-18/07-19, chess_self_analysis_baseline_2026-04, aspirational_patterns_from_47games (kanon = player_pattern_library_v1.json v 04_KNOWLEDGE_BASE/02_chess)
- **LinkedIn MCP dev:** FIX_REPORT_batch_pipeline_timeout, linkedin_mcp_deep_dive_dev_notes
- **Workspace audit (meta o práci):** META_ANALYZA_dev_workflow_epistemika, free_tier_llm_katalog, optimalizace_high_eroi_plan (+3 docx binárky)
- **MCP-Jobs audit řetězec (per-iterace):** CROSS_AUDIT_HANDOFF, CROSS_AUDIT_v1, FIX_BALIK, dif_analyza_legacy_vs_mcp, evaluace_ai_native_era, semanticka_analyza_legacy_profil, srovnani_er_pipeline → kanon: DE_NOVO_AUDIT (syntéza), srovnani_architektur (cross-arch insight), PHASE09_HOTFIX (aktivní stav)
- **Handoffs:** handoff_github01-04.json (lokální), GitHub_portfolio_dev_workflow.json (tracked)
- **Meta analýza artefaktů:** 05_EPISTEMIKA/2026-07-20_semanticka_analyza_artefakty_v1-vs-mcp.md

### 3.4 Dated snapshoty (md+json páry) — 8 souborů
- synteticky_report 07-09/15/16 (md+json), 07-17 (md+json) — generátor L1 produkuje týdenní snapshoty; zachovat poslední nebo sloučit

### 3.5 Raw/live data (NE inflace — evidence)
- metadata_stacku.json (804 KB) — **živé pipeline data** (git log: batch commity 2026-07-17), registrované v INDEX (L03)
- agregovany_report.md (105 KB) — živý log EROI hodnocení (K01/L02)
- github_portfolio_digital_twin.json (27 KB, lokální), call_transkripty, Emaily (lokální, citlivé)

### 3.6 Prázdné soubory
- `05_EPISTEMIKA/01_kalibracni_matice/LLM_free_models.md` (0 B, tracked!)

### 3.7 Binárky (gitignored, lokální) — 6 souborů ~856 KB
- docx ×4 (EVALUACE, workspace audit ×2, DE_NOVO MCP-Jobs), pdf (Sousek_summary), docx (iteracni_plan) — záměrně mimo git

## 4. TOP NÁLEZY (EROI trimming)

| # | Nález | Zásah | Úspora |
|---|-------|-------|--------|
| 1 | 4 páry 100% duplicit (2 tracked v 05_EPISTEMIKA) | dedup | −4 soubory (1 tracked pár = −2) |
| 2 | MCP-Jobs audit řetězec (7 per-iteračních reportů) | archiv, kanon 3 | −7 souborů |
| 3 | Lichess-MCP dev artefakty v 02_ANALÝZY/02_chess (4) | archiv | −4 |
| 4 | Staré CV generace (4) | archiv | −4 |
| 5 | Synteticky snapshoty md+json (6 starších) | archiv, kanon poslední | −6 |
| 6 | Workspace audit md (3) + semanticka_analyza (1) | archiv | −4 |
| 7 | Versioned superseded (9) | archiv starších | −9 |
| 8 | Empty LLM_free_models.md | archiv | −1 |
| 9 | Handoffs (5) | archiv | −5 |
| 10 | index_Github.md (110 KB stale snapshot, 2026-04-29, neregistrovaný v INDEX) | archiv | −110 KB |

## 5. KPI BASELINE (před trimem)

| Metrika | Hodnota |
|---------|---------|
| Trackovaných souborů | 86 |
| Duplicitních párů | 4 (8 souborů) |
| Prázdných souborů | 1 |
| Kandidátů na archiv (tracked) | ~35 |
| Kandidátů na archiv (lokální) | ~19 |
| INDEX drift (neregistrované soubory) | index_Github, handoff_github01-04 (lokální) |

## 6. NÁVRH TRIM PLANU (po schválení)

- **F1 Dedup:** 2 tracked duplicity v 05_EPISTEMIKA → archiv; 2 lokální páry → vyčištění disku; empty LLM_free_models
- **F2 Superseded:** archiv 9 starších verzí (tracked: OpenRouter v2, synteticky_analyza v3, CV ×4, ontologie base; lokální: roadmap v1, exec_summary v1, VCF handoff v1, index_Github)
- **F3 Transient:** archiv ~16 work-process souborů (chess, linkedin dev, workspace audit, mcp-jobs řetězec, handoffs, meta analýza)
- **F4 Snapshoty:** synteticky 07-09/15/16 (md+json) → archiv; kanon = 07-17 (+agregovany jako trvalý log)
- **F5 Verifikace + INDEX regenerace + KPI report + commit `[TRIM]`**

> Rozhodovací body pro autora: (1) rozsah MCP-Jobs řetězce — 3 kanonické vs 1 sloučený; (2) metadata_stacku/agregovany = KEEP (live data); (3) synteticky snapshoty — kolik generací ponechat; (4) lokální vrstva — čistit na disku bez git dopadu.

## 7. Metadata

- **Tags:** `#repo-audit`, `#trimming`, `#meta-dokumentace`, `#inflace`, `#phase09`
- **Návaznost:** TRIMMING_PLAN_04_KNOWLEDGE_BASE_2026-08-01.md, DE_NOVO_AUDIT_public_ready
