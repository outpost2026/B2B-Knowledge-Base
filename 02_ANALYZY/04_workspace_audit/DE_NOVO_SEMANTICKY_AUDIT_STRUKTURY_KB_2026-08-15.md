# DE NOVO SÉMANTICKÝ AUDIT STRUKTURY KB — 2026-08-15
**Datum:** 2026-08-15 | **Autor:** outpost2026
**Účel:** Nezávislý hluboký audit struktury B2B-Knowledge-Base — fyzická realita vs git tracking vs INDEX registrace vs sémantická mise modulů. Výstup: návrh úprav adresářové struktury a relevance uložení dokumentace.
**Typ:** analýza | **Doména:** governance KB | **EROI:** 9/10
**Návaznost:** KORELACE_STRUKTURY_KB_2026-08-15.md (předchozí registr-úroveň audit), ARCHITEKTURA_KB_2026-08-01.md, INDEX.md v2.2
**Metoda:** de novo — bez výchozího předpokladu, že současná struktura je správná. Vrstvy: (1) fyzický disk, (2) git tracking, (3) INDEX registrace, (4) sémantický obsah souborů (hlavičky).

---

## 1. Čísla — co struktura skutečně je

| Vrstva | Počet | Poznámka |
|--------|------:|----------|
| Textové soubory fyzicky (mimo `_ARCHIVE`, mimo binárky) | 186 | Get-ChildItem |
| Binární soubory (docx/pdf/xlsx) fyzicky | ~8 | netrackované (.gitignore) |
| **Git tracked soubory** | **93** | `git ls-files` |
| Netrackované textové soubory mimo `_ARCHIVE` | ~90 | leží v `.gitignore` lokacích |
| Soubory v `_ARCHIVE/` | ~78 | kompletně v .gitignore |
| INDEX registrace (řádky tabulek) | 164 | 48× externí B2B/KB, 105× repo lokace |

**Klíčový nález:** `.gitignore` vylučuje z public repa **celé moduly** `00_STRATEGIE/`, `03_PROVOZ/`, `02_ANALYZY/01_portfolio_audit/`, `_ARCHIVE/`. Public repo (GitHub) tedy **neobsahuje** strategii ani provozní dokumenty, ale INDEX je registruje jako by existovaly. INDEX ≠ zrcadlo repa; INDEX = registr lokálního workspace (repo + osobní složky).

---

## 2. Sémantická mise modulů (jaká by měla být)

| Modul | Mise (definice z AGENTS.md + ARCHITEKTURA_KB) | Odchylky |
|-------|-----------------------------------------------|----------|
| `00_STRATEGIE` | směřování, positioning, manifesty, EROI plány | obsahuje technické analýzy (VCF compiler), metriky portfolia |
| `01_METODIKY` | opakovatelné postupy, kostry | obsahuje CV (artefakty, ne postupy), glossary (obsah, ne postup) |
| `02_ANALYZY` | analýzy, reporty, audity | obsahuje web projekt GT-pravidel (strategie!), skill gapy |
| `03_PROVOZ` | provozní: emaily, kontrakty, zadání | cenová metodika a pricing strategy = analýza |
| `04_KNOWLEDGE_BASE` | doménová znalost | obsahuje CV automatizaci (projekt/analýza, ne doména) |
| `05_EPISTEMIKA` | kognitivní rámce, modely reality | obsahuje falsifikační test (metodika), CPM (metodika) |

---

## 3. Zjištění

### 3.1 Tematická rozptýlenost — potvrzeno de novo (4+ řetězce)

| Téma | Rozptýleno přes | Kódů |
|------|-----------------|------|
| **Skill acquisition** (poslední výstupy!) | `01_METODIKY/04_skill_acquisition` (ADOPCNI) + `01_METODIKY/06_SWE_glossary` + `02_ANALYZY/02_konkurence_a_trh` (SKILL_GAPS v1/v2) + `02_ANALYZY/02_chess` (FSRS engine) | 4 |
| **RE / VCF** | `01_METODIKY/01_reverse_engineering` + `04_KB/01_reverse_engineering` + `02_ANALYZY/03_kodove_analyzy` + `00_STRATEGIE/02_karierni_targety` (vcf_compiler architektura) | 4 |
| **MCP** | `04_KB/01_MCP` (GT postmortem) + `02_ANALYZY/05_mcp_jobs` + `02_ANALYZY/00_linkedin` (pipeline) | 3 |
| **Chess** | `02_ANALYZY/02_chess` (11) + `04_KB/02_chess` (pattern lib) + `00_STRATEGIE/02_chess` (prázdná deklarace) | 3 |
| **CI/CD** | `01_METODIKY/00_agentni_prace` (CI_CD_PROTOKOL) + `01_METODIKY/05_testing` (imerzní edu) | 2 |
| **LLM nástroje** | `05_EPISTEMIKA/01_kalibracni_matice` + `01_METODIKY/00_agentni_prace` (Free_LLM) | 2 |

### 3.2 Mis-files — soubor sémanticky nepatří tam, kde fyzicky leží

| Soubor | Fyzicky | Sémanticky patří | Důvod |
|--------|---------|------------------|-------|
| `COMPRESSION_PATTERN_METHOD_v1.0.md` | 00_STRATEGIE/00_manifesty | 01_METODIKY (metodika tvorby patternů) | je to metodika, ne manifest |
| `EVALUACE_AUTORA_FALSIFIKACE_VIBECODING_v1.0.docx` | 00_STRATEGIE/00_manifesty | 02_ANALYZY | evaluace = analýza |
| `SYSTEQ_performance_analyza_v1.md` | 00_STRATEGIE/01_positioning | 02_ANALYZY/01_portfolio_audit | repo audit = analýza |
| `roadmap_github_v2.md` | 00_STRATEGIE/ | 02_ANALYZY/01_portfolio_audit | GitHub roadmapa = portfolio |
| `vcf_optimizer_analytic_engine.md` | 00_STRATEGIE/02_karierni_targety | 02_ANALYZY/03_kodove_analyzy | technická architektura |
| `vcf_compiler_architektura_deepdive.md` | 00_STRATEGIE/02_karierni_targety | 02_ANALYZY/03_kodove_analyzy | technická architektura |
| `VCF_compiler_dopad_analyza_v2.md` | 00_STRATEGIE/02_karierni_targety | 02_ANALYZY | dopadová analýza |
| `waterjet_intelligence_layer_poc.md` | 00_STRATEGIE/02_karierni_targety | 00_STRATEGIE (produktová strategie) | PoC = strategie, ne kariérní target |
| `market_research_stack_conversion.md` | 00_STRATEGIE/02_karierni_targety | 02_ANALYZY/02_konkurence_a_trh | tržní výzkum |
| `Strategicke_Vyhodnoceni_Projektu_Web_pro_GT-Pravidla.md` | 02_ANALYZY/02_konkurence_a_trh | 00_STRATEGIE (projekt) | strategie webu, ne analýza trhu |
| `Navrh_Technicke_Architektury_Web_pro_GT-Pravidla.md` | 02_ANALYZY/02_konkurence_a_trh | 01_METODIKY / projekt | technický návrh |
| `Mechanizmy_Transformace_Dat_Markdown_na_Strukturovana_Data.md` | 02_ANALYZY/02_konkurence_a_trh | 01_METODIKY / projekt | datová transformace |
| `CI_CD_INTEGRACE_PROTOKOL.md` | 01_METODIKY/00_agentni_prace | 01_METODIKY/05_testing | CI/CD = testování |
| `Free_LLM_openrouter.txt` | 01_METODIKY/00_agentni_prace | 05_EPISTEMIKA/01_kalibracni_matice | LLM katalog |
| `Falsifikacni_test_single_game_discovery_v1.md` | 05_EPISTEMIKA/00_kompresni_realismus | 01_METODIKY/05_testing | testovací metodika |
| `CV_YOLO11_ADOPTION_ASSESSMENT_v1.md` | 04_KB/03_CV_AUTOMATION | 02_ANALYZY | adopční assessment = analýza |
| `SMALL_MODELS_CV_ASPIRACNI_PROJEKTY_v1.md` | 04_KB/03_CV_AUTOMATION | 02_ANALYZY | rešerše = analýza |
| `YOLO11_GARDEN_MONITOR_GLOSSARY_KONCEPT_v1.md` | 04_KB/03_CV_AUTOMATION | (OSINT risk — .gitignore) | citlivé |

### 3.3 Duplicity fyzických souborů (verze v 2 lokacích)

| Duplicitní pár | Lokace 1 | Lokace 2 | Status |
|----------------|----------|----------|--------|
| `Mikolov_Manifest` | `00_STRATEGIE/00_manifesty/Mikolov_Manifest.md` | `_ARCHIVE/00_STRATEGIE/Mikolov_Manifest_KB.md` | 2 kopie |
| `Mikolov_Sousek_prunik` | `00_STRATEGIE/00_manifesty/` | `_ARCHIVE/00_STRATEGIE/` | 2 kopie |
| `Sousek_Manifest_kompresniho_realismu` | `05_EPISTEMIKA/00_kompresni_realismus/v1.1` | `_ARCHIVE/00_STRATEGIE/v1 + B2B_Edition` | v1.1 supersedes — OK |
| `synteticky_report_analyza` | INDEX L01 (B2B/) | `_ARCHIVE/02_ANALYZY/00_linkedin/` | INDEX ukazuje na archivovaný |

### 3.4 Číselné kolize podadresářů (4×)

| Modul | Kolize |
|-------|--------|
| `02_ANALYZY` | `02_chess` + `02_konkurence_a_trh` (obě 02_) |
| `04_KNOWLEDGE_BASE` | `01_MCP` + `01_reverse_engineering` (obě 01_); `02_chess` + `02_testing` (obě 02_) |
| `00_STRATEGIE` | `02_chess` + `02_karierni_targety` (obě 02_) |

### 3.5 Prázdné složky (deklarace bez obsahu)

- `00_STRATEGIE/02_chess/` — chess obsah je v `02_ANALYZY/02_chess`
- `01_METODIKY/03_aplikacni_proces/` — "připraveno" bez artefaktů
- `04_KNOWLEDGE_BASE/02_testing/` — CI edu přesunut do `01_METODIKY/05_testing`
- `00_STRATEGIE/01_positioning/_ARCHIVE/` — prázdný arch

### 3.6 INDEX drift (163 řádků, ale)

- **48 řádků** ukazuje na externí `B2B/` / `KB/` lokace — z toho ~20 souborů fyzicky existuje i v repo (netrackovaných, např. Mikolov_Manifest). INDEX registruje soubor 2× pod jinou lokací.
- INDEX má stále **K01/K02** (`agregovany_report`, `synteticky_report_analyza`) v `00_STRATEGIE/02_karierni_targety` — ale kanon je L02/L01 v `02_ANALYZY/00_linkedin`. Duplicita registrace přetrvává.
- **G01/G02** (EPISTEMICKE-PRAVIDLA, HANDOFF) — INDEX lokace `KB/`, fyzicky `05_EPISTEMIKA/02_agentni_pravidla/` (tracked). INDEX nelže o existenci, ale o lokaci.

### 3.7 Pozitivní nálezy

- **Žádné fyzické duplicity MD5** (0 párů) — duplicity jsou jen registrace/verze.
- **P4 dated snapshoty** v `01_portfolio_audit` (v2 kanon + `_ARCHIVE` v1) — konzistentní.
- **`_ARCHIVE` disciplína** (X01-X34 + podadresáře) — funguje.
- **Replikace dokumentovaná** (GROUND_TRUTH_VCF_PARSER 4×, VCF workflow 2×).
- **ASCII-NOM** názvy — s výjimkou `R&D_evoluce...` (ampersand) a 2 českých starších souborů v _ARCHIVE.

---

## 4. Návrh úprav — cílové adresářové uspořádání

### 4.1 Principy (nad rámec P1-P5)

| # | Princip |
|---|---------|
| **D1** | **1 téma = 1 složka.** Pokud téma má artefakty ve 2+ složkách, přesun na kanon lokaci (git mv). |
| **D2** | **INDEX = zrcadlo fyzické reality + tracking status.** Sloupec Zdroj = skutečná cesta. Přidat sloupec `[T]/[N]` (tracked/netrackovaný). |
| **D3** | **Metodika ≠ obsah.** Postupy (metodiky, testy, glossary-template) do `01_METODIKY`; obsah (knowledge, analýzy) do příslušného modulu. |
| **D4** | **Bez prázdných deklarací.** Prázdná složka = naplň, nebo smaž. |
| **D5** | **Číslování unikátní v rámci modulu.** Žádné 2 složky se stejným číslem. |

### 4.2 Konsolidace skill acquisition řetězce (D1 — nejvyšší priorita)

Cílový stav — vše o "učím se X" v jedné lokaci:

```
01_METODIKY/04_skill_acquisition/
├── ADOPCNI_METODOLOGIE_2026_v1.md          ← kanon (JAK učit)
├── SKILL_GAPS_ROZBOR_Q3_2026_v2.md         ← přesun z 02_ANALYZY/02_konkurence_a_trh (CO učit)
├── SKILL_GAPS_ROZBOR_Q3_2026_v1.md         → _ARCHIVE/ (superseded v2)
├── SWE_GLOSSARY_zive_v1.md                 ← přesun z 01_METODIKY/06_SWE_glossary (terminologie)
└── FSRS_reference.md                       ← odkaz na chess_mcp_strategy (SRS infra) NEBO přesunout chess_mcp_strategy sem
```

Alternativa (méně invazivní): ponechat lokace, v INDEXu řetězec označit tagem `acquisition` a v ADOPCNI_METODOLOGIE přidat mapu cest. **Doporučeno:** variantu přesunu SKILL_GAPS v2 (nejvyšší drift — "učení" uložené pod "konkurence a trh").

### 4.3 Přejmenování pro odstranění číselných kolizí (D5)

| Modul | Současný | Návrh |
|-------|----------|-------|
| `02_ANALYZY` | `02_konkurence_a_trh` | `06_konkurence_a_trh` (02 uvolněno pro chess — ale chess je analyzy, ne trh) |
| `02_ANALYZY` | `02_chess` | `02_chess` zůstává (majorita obsahu) — konkurence_a_trh dostane `06_` |
| `04_KNOWLEDGE_BASE` | `01_MCP` | `01_MCP` zůstává; `01_reverse_engineering` → `03_reverse_engineering` |
| `04_KNOWLEDGE_BASE` | `02_chess` | `02_chess` zůstává; `02_testing` → smazat (prázdná) |
| `00_STRATEGIE` | `02_chess` | smazat (prázdná); `02_karierni_targety` zůstává |

### 4.4 Přesuny mis-files (D1 + D3)

| Soubor | Z | Do |
|--------|---|----|
| `COMPRESSION_PATTERN_METHOD_v1.0.md` | 00_STRATEGIE/00_manifesty | 01_METODIKY/04_skill_acquisition (nebo 01_METODIKY/05_testing) |
| `SYSTEQ_performance_analyza_v1.md` | 00_STRATEGIE/01_positioning | 02_ANALYZY/01_portfolio_audit |
| `roadmap_github_v2.md` | 00_STRATEGIE/ | 02_ANALYZY/01_portfolio_audit |
| `vcf_optimizer_analytic_engine.md` | 00_STRATEGIE/02_karierni_targety | 02_ANALYZY/03_kodove_analyzy |
| `vcf_compiler_architektura_deepdive.md` | 00_STRATEGIE/02_karierni_targety | 02_ANALYZY/03_kodove_analyzy |
| `VCF_compiler_dopad_analyza_v2.md` | 00_STRATEGIE/02_karierni_targety | 02_ANALYZY/03_kodove_analyzy |
| `market_research_stack_conversion.md` | 00_STRATEGIE/02_karierni_targety | 02_ANALYZY/06_konkurence_a_trh |
| `Strategicke_Vyhodnoceni_Projektu_Web_pro_GT-Pravidla.md` | 02_ANALYZY/02_konkurence_a_trh | 00_STRATEGIE/03_web_GT_pravidla (nová) |
| `Navrh_Technicke_Architektury_Web_pro_GT-Pravidla.md` | 02_ANALYZY/02_konkurence_a_trh | 00_STRATEGIE/03_web_GT_pravidla |
| `Mechanizmy_Transformace_Dat_Markdown_na_Strukturovana_Data.md` | 02_ANALYZY/02_konkurence_a_trh | 00_STRATEGIE/03_web_GT_pravidla |
| `CI_CD_INTEGRACE_PROTOKOL.md` | 01_METODIKY/00_agentni_prace | 01_METODIKY/05_testing |
| `Free_LLM_openrouter.txt` | 01_METODIKY/00_agentni_prace | 05_EPISTEMIKA/01_kalibracni_matice |
| `Falsifikacni_test_single_game_discovery_v1.md` | 05_EPISTEMIKA/00_kompresni_realismus | 01_METODIKY/05_testing |
| `CV_YOLO11_ADOPTION_ASSESSMENT_v1.md` | 04_KB/03_CV_AUTOMATION | 02_ANALYZY/06_CV_automatizace (nová) |
| `SMALL_MODELS_CV_ASPIRACNI_PROJEKTY_v1.md` | 04_KB/03_CV_AUTOMATION | 02_ANALYZY/06_CV_automatizace |
| `waterjet_intelligence_layer_poc.md` | 00_STRATEGIE/02_karierni_targety | 00_STRATEGIE/02_karierni_targety (PONEHAT — produktová strategie) |

### 4.5 Mazání / archivace

| Složka / soubor | Akce |
|-----------------|------|
| `00_STRATEGIE/02_chess/` | smazat (prázdná) |
| `01_METODIKY/03_aplikacni_proces/` | smazat (prázdná) |
| `04_KNOWLEDGE_BASE/02_testing/` | smazat (prázdná) |
| `00_STRATEGIE/01_positioning/_ARCHIVE/` | smazat (prázdný) |
| `_ARCHIVE/00_STRATEGIE/Mikolov_Manifest_KB.md` | kanon je `00_STRATEGIE/00_manifesty/Mikolov_Manifest.md` — duplicitní kopii odstranit |
| `_ARCHIVE/00_STRATEGIE/Mikolov_Sousek_prunik_KB.md` | odstranit (duplicita) |
| `SKILL_GAPS_ROZBOR_Q3_2026_v1.md` | přesun do `_ARCHIVE` (superseded v2) |

### 4.6 INDEX — opravy (druhá fáze po přesunech)

1. Sloupec Zdroj → skutečná fyzická cesta (žádné `KB/`, `B2B/` pro soubory v repo).
2. Přidat tracking status `[T]` / `[N]` / `[ARCH]` ke každému řádku.
3. Odstranit přetrvávající duplicitu K01/K02 vs L01/L02.
4. Registrace nové složky `03_web_GT_pravidla` + `06_CV_automatizace`.
5. Tag lookup doplnit: `acquisition`, `gt_pravidla`, `cv_automation`.

---

## 5. Rozhodnutí / otevřené otázky pro autora

| # | Otázka | Doporučení |
|---|--------|------------|
| 1 | Konsolidovat skill acquisition (SKILL_GAPS v2 → 04_skill_acquisition)? | **ANO** — řetězec je rozptýlený na 4 lokace |
| 2 | Přejmenovat `02_konkurence_a_trh` → `06_konkurence_a_trh`? | ANO (odstranění kolize) |
| 3 | Provést přesuny mis-files dle 4.4? | ANO — 14 souborů, git mv |
| 4 | Smazat 4 prázdné složky? | ANO |
| 5 | Ponechat `.gitignore` (00_STRATEGIE/03_PROVOZ mimo public repo)? | ANO — osobní data; INDEX musí označit `[N]` |
| 6 | GT-pravidla web → samostatná složka `00_STRATEGIE/03_web_GT_pravidla`? | ANO — je to projekt, ne analýza trhu |
| 7 | Přesun CV automatizace z 04_KB do 02_ANALYZY? | ANO (s výjimkou GARDEN_MONITOR — OSINT) |

---

## Metadata
- **Tags:** `#governance`, `#struktura`, `#audit`, `#de_novo`, `#organizace`, `#mis_files`
- **EROI:** 9/10 (struktura = podmínka použitelnosti; náklad = 1× konsolidace, benefit = trvalá orientace)
- **Navazuje na:** ARCHITEKTURA_KB_2026-08-01.md (governance), KORELACE_STRUKTURY_KB_2026-08-15.md (registr-level), SEMANTICKA_ANALYZA_METADOKUMENTACE_2026-08-01.md