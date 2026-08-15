# KORELACE STRUKTURY KB S OBSAHEM — audit 2026-08-15
**Datum:** 2026-08-15 | **Autor:** outpost2026
**Účel:** Vyhodnocení struktury B2B-Knowledge-Base proti skutečnému obsahu — identifikace duplicit registrace, tematické rozptýlenosti, číselných kolizí a driftu INDEX registru. Výstup: návrh cílové struktury.
**Typ:** analýza | **Doména:** governance KB | **EROI:** 9/10 (struktura = podmínka použitelnosti KB)
**Návaznost:** ARCHITEKTURA_KB_2026-08-01.md, SEMANTICKA_ANALYZA_METADOKUMENTACE_2026-08-01.md, INDEX.md, ADOPCNI_METODOLOGIE_2026_v1.md

---

## 1. Metoda

1. `git ls-files` všech 6 modulů (fyzická realita, 56+ souborů)
2. Sken všech adresářů (fyzická realita, 36 složek)
3. Korelace s registrací v `INDEX.md` (verze 2.1, 2026-08-01)
4. MD5 kontrola duplicit (žádné fyzické duplicity .md — duplicity jsou pouze v registru)

---

## 2. Zjištění

### 2.1 Duplicitní registrace v INDEX (1 soubor, 2 kódy)

| Soubor | Fyzická lokace | Registrován jako |
|--------|----------------|------------------|
| `EPISTEMICKE-PRAVIDLA-AGENTNI-PRACE.md` | 05_EPISTEMIKA/02_agentni_pravidla/ | A01 (01_METODIKY/00_agentni_prace) + G01 (05_EPISTEMIKA) |
| `HANDOFF_COMPACT.md` | 05_EPISTEMIKA/02_agentni_pravidla/ | A02 + G02 |
| `kalibracni_matice.json` | 05_EPISTEMIKA/01_kalibracni_matice/ | A03 (01_METODIKY) + M01 (05_EPISTEMIKA) |
| `RE_Methodology.md` | 04_KNOWLEDGE_BASE/01_reverse_engineering/ | R01 (01_METODIKY) + RE02 (04_KB) |
| `RE_CASE_STUDY_VCUTWORKS_LIGHTBURN_v2.md` | 04_KNOWLEDGE_BASE/01_reverse_engineering/ | R02 + RE01 |
| `GROUND_TRUTH_VCF_PARSER_ORIGIN_V1.0.json` | 04_KNOWLEDGE_BASE/01_reverse_engineering/ | R03 + RE03 |
| `eroi_chronologicky_plan_s_metodikou.md` | 00_STRATEGIE/01_positioning/ | P02 (00_STRATEGIE) + L04 (02_ANALYZY/00_linkedin) |
| `GROUND_TRUTH_aktualni_stav_2026-08-06.md` | 00_STRATEGIE/00_manifesty/ | S08 + N01 (nově vytvořené) |

**Dopad:** registr matoucí pro autora i LLM — neví se, kde je kanon.

### 2.2 Chybějící registrace (fyzicky existuje, INDEX nezná)

| Fyzicky existuje | INDEX |
|------------------|-------|
| `02_ANALYZY/02_konkurence_a_trh/` — 5 souborů (SKILL_GAPS v1/v2, Strategicke_Vyhodnoceni, Navrh_Technicke_Architektury, Mechanizmy_Transformace) | sekce "Připraveno pro budoucí artefakty" — **prázdná deklarace** |
| `02_ANALYZY/02_chess/` — 11 souborů (chess_mcp_strategy, SUMMARY, RETENEZEC, DEGRADACE_HALLUCINACE aj.) | neregistrováno |
| `04_KNOWLEDGE_BASE/03_CV_AUTOMATION/` — 2 soubory (YOLO11, SMALL_MODELS) | neregistrováno |
| `02_ANALYZY/01_portfolio_audit/` v2 generace (github_portfolio_analysis_v2, digital_twin, portfolio_audit_a_match_v2, R&D_evoluce_v2) | registrovány jen v1 názvy |
| `CI_CD_INTEGRACE_PROTOKOL.md`, `Free_LLM_openrouter.txt` | A04, A06 ano — ale lokace v INDEX (KB/) neodpovídá fyzické (01_METODIKY/00_agentni_prace/) |

### 2.3 Číselné kolize podadresářů

| Modul | Kolize |
|-------|--------|
| 02_ANALYZY | `02_chess` + `02_konkurence_a_trh` (obě 02_) |
| 04_KNOWLEDGE_BASE | `01_MCP` + `01_reverse_engineering` (obě 01_); `02_chess` + `02_testing` (obě 02_) |
| 00_STRATEGIE | `02_chess` + `02_karierni_targety` (obě 02_) |

### 2.4 Prázdné složky (existují na disku, ne v gitu — matou)

- `00_STRATEGIE/02_chess/` (prázdná — chess obsah je v 02_ANALYZY/02_chess)
- `01_METODIKY/03_aplikacni_proces/` (prázdná — deklarace "připraveno" bez obsahu)
- `04_KNOWLEDGE_BASE/02_testing/` (prázdná — CI edu přesunut do 01_METODIKY/05_testing)

### 2.5 Tematická rozptýlenost (autorova stížnost — potvrzeno)

| Téma | Rozptýleno přes |
|------|-----------------|
| **RE / VCF** | 01_METODIKY/01_reverse_engineering + 04_KB/01_reverse_engineering + 02_ANALYZY/03_kodove_analyzy |
| **MCP** | 04_KB/01_MCP (GT postmortem) + 02_ANALYZY/05_mcp_jobs + 02_ANALYZY/00_linkedin (pipeline) |
| **Chess** | 02_ANALYZY/02_chess (11) + 04_KB/02_chess (pattern lib) + 00_STRATEGIE/02_chess (prázdná) |
| **Agentní pravidla** | 01_METODIKY/00_agentni_prace + 05_EPISTEMIKA/02_agentni_pravidla |
| **CI/CD** | 01_METODIKY/00_agentni_prace (CI_CD_PROTOKOL) + 01_METODIKY/05_testing (imerzní edu) |
| **LLM nástroje** | 05_EPISTEMIKA/01_kalibracni_matice + 01_METODIKY/00_agentni_prace (Free_LLM) |
| **Skill acquisition (poslední výstupy!)** | 01_METODIKY/04_skill_acquisition (ADOPCNI_METODOLOGIE) + 01_METODIKY/06_SWE_glossary (glossary) + 02_ANALYZY/02_konkurence_a_trh (SKILL_GAPS) |

### 2.6 Pozitivní nálezy (co funguje)

- **P4 dated snapshoty** v 01_portfolio_audit (v2 kanon + _ARCHIVE v1) — konzistentní
- **Žádné fyzické duplicity** souborů (MD5 kontrola — 0 párů)
- **_ARCHIVE** disciplína (X01-X34) — funguje
- **Replikace** (GROUND_TRUTH_VCF_PARSER 4×, VCF workflow 2×) — deliberate, dokumentovaná v INDEX

---

## 3. Korelace s posledními výstupy (adopční metodika)

Poslední výstup `ADOPCNI_METODOLOGIE_2026_v1.md` vytvořil nový tematický řetězec, který je rozptýlený přes 3 složky ve 2 modulech:

```
SKILL_GAPS (02_ANALYZY/02_konkurence_a_trh)     ← CO učit (tržní signál)
    ↓
ADOPCNI_METODOLOGIE (01_METODIKY/04_skill_acquisition)  ← JAK učit
    ↓
SWE_GLOSSARY (01_METODIKY/06_SWE_glossary)     ← terminologie (Feynman výstup)
    ↓
FSRS engine (02_ANALYZY/02_chess)               ← SRS infrastruktura (implementace!)
```

Tento řetězec by měl být **v jedné lokaci** — 01_METODIKY/04_skill_acquisition/ — aby šlo nalézt "učím se X" jedním pohledem. Aktuálně je rozptýlený a autor musí znát 4 cesty.

---

## 4. Návrh cílové struktury

### 4.1 Principy (nad rámec P1-P5)

| P | Princip |
|---|---------|
| **S1** | 1 téma = 1 složka. Pokud je téma ve 2+ složkách, jedna je kanon, ostatní se přesunou (git mv) |
| **S2** | Registr (INDEX) = zrcadlo fyzické reality. Žádné "zdroj" lokace z B2B/KB — jen skutečné cesty |
| **S3** | Žádné prázdné složky — prázdná deklarace = buď naplň, nebo smaž |
| **S4** | Číslování unikátní v rámci modulu |
| **S5** | Tematický řetězec (skill acquisition) = jeden celek v jedné složce |

### 4.2 Navrhované přesuny (git mv, s potvrzením autora)

| Soubor | Z | Do | Důvod |
|--------|---|----|-------|
| `SKILL_GAPS_ROZBOR_Q3_2026_v1.md` | 02_ANALYZY/02_konkurence_a_trh/ | 01_METODIKY/04_skill_acquisition/_ARCHIVE/ | Superseded v2; patří k tématu |
| `SKILL_GAPS_ROZBOR_Q3_2026_v2.md` | 02_ANALYZY/02_konkurence_a_trh/ | 01_METODIKY/04_skill_acquisition/ | Téma skill acquisition (S5) |
| `ADOPCNI_METODOLOGIE_2026_v1.md` | (již tam) | — | Kanon řetězce |
| `SWE_GLOSSARY_zive_v1.md` | 01_METODIKY/06_SWE_glossary/ | (zvážit sloučení do 04_skill_acquisition, nebo ponechat — viz otázka) | Terminologie = nástroj adopce |
| `chess_mcp_strategy_v1.md` | 02_ANALYZY/02_chess/ | 01_METODIKY/04_skill_acquisition/ (nebo zůstává — obsahuje FSRS infra pro adopci i chess) | SRS engine řetězce |
| `CI_CD_INTEGRACE_PROTOKOL.md` | 01_METODIKY/00_agentni_prace/ | 01_METODIKY/05_testing/ | CI/CD téma je v 05_testing (S1) |
| `Free_LLM_openrouter.txt` | 01_METODIKY/00_agentni_prace/ | 05_EPISTEMIKA/01_kalibracni_matice/ | LLM nástroje (S1) |

### 4.3 Registr (INDEX) — opravy

1. **Odstranit duplicitní kódy** — ponechat kanon lokaci: G01 (ne A01), G02 (ne A02), M01 (ne A03), RE02 (ne R01), RE01 (ne R02), RE03 (ne R03), P02 (ne L04), S08 (ne N01)
2. **Doplnit chybějící registrace**: SKILL_GAPS v1/v2, 02_chess (11), 03_CV_AUTOMATION (2), portfolio_audit v2 generace
3. **Aktualizovat "Zdroj" sloupce** na skutečné fyzické cesty
4. **Odstranit sekce "Připraveno pro budoucí artefakty"** pokud nemají obsah

### 4.4 Prázdné složky — akce

- `00_STRATEGIE/02_chess/` → odstranit (chess je v 02_ANALYZY)
- `04_KNOWLEDGE_BASE/02_testing/` → odstranit (CI je v 01_METODIKY/05_testing)
- `01_METODIKY/03_aplikacni_proces/` → odstranit, nebo naplnit (aplikace = EROI plán ❷ v 00_STRATEGIE/01_positioning — přesunout EROI sekci sem? Ne — ponechat odstranit)

---

## 5. Doporučení / otevřené otázky pro autora

| # | Otázka | Možnosti |
|---|--------|----------|
| 1 | Přesunout SKILL_GAPS v2 do 01_METODIKY/04_skill_acquisition? | A) Ano, sloučit řetězec (doporučeno) B) Ponechat v 02_ANALYZY/02_konkurence_a_trh |
| 2 | Sloučit SWE_GLOSSARY do 04_skill_acquisition? | A) Ponechat 06_SWE_glossary (glossary = samostatný artefakt) B) Sloučit |
| 3 | Provést přesuny CI_CD + Free_LLM dle 4.2? | A) Ano B) Ne — jen registr opravit |
| 4 | Opravit INDEX (dedup + doplnění + real lokace)? | A) Ano (doporučeno) B) Ne |
| 5 | Odstranit 3 prázdné složky? | A) Ano B) Ne |

---

## Metadata

- **Tags:** `#governance`, `#struktura`, `#audit`, `#index`, `#organizace`
- **EROI:** 9/10 (registr = podmínka manuálního vyhledávání autora; náklad = 1× oprava, benefit = trvalá orientace)
- **Navazuje na:** ARCHITEKTURA_KB_2026-08-01.md (governance), SEMANTICKA_ANALYZA_METADOKUMENTACE_2026-08-01.md (předchozí audit)