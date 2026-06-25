# B2B-Knowledge-Base

**Jediný zdroj pravdy pro pivot z manuálních/CNC pozic na B2B automation & system integration**

| Metrika | Hodnota |
|---------|---------|
| **Verze** | 1.0 |
| **Datum založení** | 2026-06-25 |
| **Autor** | Ondřej Soušek (outpost2026) |
| **Účel** | Verzovaná DB znalostních & metodických artefaktů — integrace GitHub versioningu, agentního workflow a desktop IDE pro zvýšení SNR rozhodování |
| **Stack** | Markdown, JSON, Git, RAG-ready struktura, agentní přístup přes opencode / LLM CLI |

---

## Principy

1. **Jediný zdroj pravdy** — každý artefakt existuje právě jednou, referencovaný z INDEX.md
2. **Verzovaná evoluce** — každá změna = commit, každý commit = důvod (proč)
3. **RAG-ready** — struktura navržena pro sémantické vyhledávání LLM agenty
4. **EROI priorita** — obsah je řazen dle poměru dopad / náklady (ne dle objemu)
5. **Žádná data na skládku** — každý soubor prošel ontologickým ořezen (low-SNR artefakty jsou v `_ARCHIVE/`)

---

## Adresářová struktura

```
B2B-Knowledge-Base/
├── README.md                         ← tento soubor
├── AGENTS.md                         ← metodická kostra pro agentní přístup
├── INDEX.md                          ← fulltextový registr všech artefaktů
├── .gitignore
│
├── 00_STRATEGIE/                     ← směřování, positioning, manifesty
│   ├── 00_manifesty/                 ← autorovy manifesty a epistemické rámce
│   ├── 01_positioning/               ← EROI plány, korekce vektorů
│   └── 02_karierni_targety/          ← follow leade, role fit
│
├── 01_METODIKY/                      ← opakovatelné postupy a metodické kostry
│   ├── 00_agentni_prace/             ← epistemická pravidla pro LLM agenty
│   ├── 01_reverse_engineering/       ← RE metodologie, pair-diff, golden master
│   ├── 02_CV_a_profil/               ← CV templaty, LinkedIn optimalizace
│   ├── 03_aplikacni_proces/          ← jak aplikovat, cover letter templaty
│   └── 04_skill_acquisition/         ← learning path pro gapy (TS, Azure, PLC)
│
├── 02_ANALÝZY/                       ← tržní analýzy, audity, reporty
│   ├── 00_linkedin/                  ← LinkedIn analýzy, syntetické reporty
│   ├── 01_portfolio_audit/           ← GitHub audit, skill match matice
│   └── 02_konkurence_a_trh/          ← srovnání, tržní signály
│
├── 03_PROVOZ/                        ← provozní dokumenty, emaily, kontrakty
│   ├── 00_komunikace/                ← emaily, call transkripty, jednání
│   ├── 01_projekty/                  ← technická zadání, PoC dokumentace
│   └── 02_business/                  ← B2B hodnota, cenotvorba, NDA
│
├── 04_KNOWLEDGE_BASE/                ← doménová znalost (CNC, CAM, IoT)
│   ├── 00_CNC_CAM/                   ← CNC zpracování, CAM software
│   ├── 01_reverse_engineering/       ← RE case studies, binární formáty
│   ├── 02_testing/                   ← golden master, determinism testy
│   └── 03_technologie/               ← stack, nástroje, konfigurace
│
├── 05_EPISTEMIKA/                    ← kognitivní rámce, modely reality
│   ├── 00_kompresni_realismus/       ← Mikolov, ontologie, manifesty
│   ├── 01_kalibracni_matice/         ← LLM routing, model analysis
│   └── 02_agentni_pravidla/          ← bezpečnostní protokoly, guardrails
│
└── _ARCHIVE/                         ← low-SNR / superseded artefakty (nečistit)
    └── _INDEX_ARCHIVE.md             ← proč je co v archivu
```

---

## Modulární mapa — zdroj → cíl

Každý artefakt z původních zdrojových dirs (`B2B/` a `KB/`) je namapován do nové struktury:

| Zdrojový soubor | Cílový modul | Zdůvodnění |
|-----------------|-------------|------------|
| `B2B/Korekce_vektoru_rozvoje_OS.json` | `00_STRATEGIE/01_positioning/` | Akční kompresní framework — primární strategický dokument |
| `B2B/CV/CV_Ondrej_Sousek_redesign.md` | `01_METODIKY/02_CV_a_profil/` | CV jako metodický artefakt |
| `B2B/linkedin_analyzy/synteticky_report_analyza.md` | `02_ANALÝZY/00_linkedin/` | Tržní analýza |
| `B2B/linkedin_analyzy/eroi_chronologicky_plan_s_metodikou.md` | `00_STRATEGIE/01_positioning/` | EROI plán |
| `B2B/**/*` | dle obsahu | Viz INDEX.md pro úplný mapping |
| `KB/**/*` | `04_KNOWLEDGE_BASE/` a `05_EPISTEMIKA/` | Doménová znalost a kognitivní rámce |

---

## Pravidla pro přidávání artefaktů

1. **Každý nový soubor** musí mít v hlavičce:
   ```markdown
   # Název artefaktu
   **Datum:** YYYY-MM-DD | **Autor:** outpost2026 | **Modul:** XX_NAZEV/
   **Účel:** 1 věta co tento soubor dělá
   ```
2. **Žádný duplicitní obsah** — pokud něco existuje v `_ARCHIVE/`, referencuj, nekopíruj
3. **Commit message template:** `[MODUL] akce: krátký popis (EROI důvod)`
   - např. `[STRATEGIE] add: korekce vektoru pro Q3 2026 (EROI 9/10)`
4. **Low-SNR artefakty** (nepoužívané, superseded, experimentální) jdou do `_ARCHIVE/`
5. **Binární soubory** (.docx, .pdf, .mp3) nejdou do GitHubu — jde pouze reference v INDEX.md s poznámkou "lokálně v původním zdroji"

---

## Integrace s agentním workflow

Viz `AGENTS.md` pro detailní metodiku. Základní pravidla:
1. Před každým agentním úkolem: `git commit` checkpoint
2. Během úkolu: agent smí číst celou KB, psát jen do určeného modulu
3. Po úkolu: `git status` + `git diff --stat` + `git log`
4. Agent nesmí mazat soubory — pouze přesouvat do `_ARCHIVE/`
