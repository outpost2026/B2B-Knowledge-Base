# ARCHITEKTURA B2B-Knowledge-Base — cílový stav (post-trim)

**Datum:** 2026-08-01 | **Autor:** outpost2026
**Účel:** Závazná cílová struktura repa po trimmingu inflace metadokumentace; definuje kanonické lokace a vrstvení
**Typ:** proces / governance | **Návaznost:** SEMANTICKA_ANALYZA_METADOKUMENTACE_2026-08-01.md, AGENTS.md §4.5

---

## 1. Principy

1. **Jedna kanonická lokace na artefakt** — žádné `_KB`/`_v1.1` klony, žádné cross-modul duplicity.
2. **Public/private vrstva = gitignore jako politika** — typ obsahu určuje vrstvu: GT/strategie/business/citlivé = private (lokální); metodiky/analýzy/znalost = public (tracked).
3. **Kanon ve veřejné vrstvě, pokud je obsah veřejný** — veřejný artefakt nesmí mít kanon v privátní vrstvě (ztratil by se z public repa).
4. **Jeden retenční prostor** — `_ARCHIVE/` je jediná zóna pro superseded/transient; přesun (move), nikdy delete (AGENTS.md §4.4).
5. **Live data ≠ dokumentace** — data/logy zůstávají v doménovém podadresáři, označené LIVE, nearchivují se.
6. **INDEX.md = jediný registr** — každý tracked soubor registrovaný; drift check (AGENTS.md §4.5 P5).

## 2. Cílová struktura

```
B2B-Knowledge-Base/
├── AGENTS.md · README.md · INDEX.md · .gitignore
│
├── 00_STRATEGIE/        [PRIVATE]  GT + privátní strategie; ŽÁDNÉ duplicity veřejného obsahu
│   └── 00_manifesty/                (Mikolov originály, GROUND_TRUTH)
│
├── 01_METODIKY/         [PUBLIC]
│   ├── 00_procesy/                  governance (architektura, standardy, trimming plány)
│   ├── 01_eroi/                     EROI metodika (živá)
│   └── 02_CV_a_profil/   kanon: 1× aktuální one-pager + 1× full CV + 1× guide — bez starých generací
│
├── 02_ANALYZY/          [PUBLIC]
│   ├── 00_linkedin/                  analýzy + LIVE data (metadata_stacku.json, agregovany_report.md)
│   ├── 02_chess/                     analýzy; dev artefakty → archiv (kanon vzorů = 04_KB/02_chess)
│   ├── 04_workspace_audit/           repo audity
│   ├── 05_mcp_jobs/                  kanon: DE_NOVO_AUDIT + srovnani_architektur + PHASE09_HOTFIX
│   └── 01_portfolio_audit/ [PRIVATE] zůstává lokální
│
├── 03_PROVOZ/           [PRIVATE]  business evidence, transkripty, emaily — lokální
│
├── 04_KNOWLEDGE_BASE/   [PUBLIC]  čistá doménová znalost (trim F1-F5 dokončen 2026-08-01)
│   ├── 01_MCP/ · 02_chess/
│
├── 05_EPISTEMIKA/       [PUBLIC]
│   ├── 00_kompresni_realismus/      KANON manifestů (jedna verze) + ontologie jen _appendix
│   └── 01_kalibracni_matice/
│
└── _ARCHIVE/            [PRIVATE]  JEDINÁ retenční zóna
    ├── 00_STRATEGIE/ 01_METODIKY/ 02_ANALYZY/ 04_KNOWLEDGE_BASE/ 05_EPISTEMIKA/
```

## 3. Mapování kanonických lokací (reference)

| Obsah | Kanon (jediné umístění) | Archivace |
|-------|-------------------------|-----------|
| Mikolov manifesty | `00_STRATEGIE/00_manifesty/` (private) | `_ARCHIVE/00_STRATEGIE/` |
| Sousek manifest (Hardened B2B v1.1) | `05_EPISTEMIKA/00_kompresni_realismus/Sousek_Manifest_kompresniho_realismu_v1.1.json` | `_ARCHIVE/05_EPISTEMIKA/` |
| Ontologie komprese | `..._appendix.md` (final RAG) | base → `_ARCHIVE/05_EPISTEMIKA/` |
| CV | 1× one-pager + 1× full + 1× guide | staré generace → `_ARCHIVE/01_METODIKY/` |
| Chess vzory | `04_KNOWLEDGE_BASE/02_chess/player_pattern_library_v1.json` | dev artefakty → `_ARCHIVE/02_ANALYZY/` |
| MCP-Jobs | DE_NOVO_AUDIT + srovnani_architektur + PHASE09_HOTFIX | per-iterace → `_ARCHIVE/02_ANALYZY/` |
| Live data LinkedIn | `02_ANALYZY/00_linkedin/` (metadata_stacku.json, agregovany_report.md) | nikdy (LIVE) |

## 4. Strukturální prevence (odkaz)

Pravidla P1-P5 jsou závazná — viz `AGENTS.md` §4.5. Tento dokument je jejich zdůvodnění a cílová architektura.

## 5. KPI dopad

| Metrika | Před | Po (cílově) |
|---------|------|-------------|
| Trackovaných souborů | 86 | ~50 |
| Duplicitní páry | 4 | 0 |
| Dev/transient v public | ~17 | 0 |
| Kanonický soubor na téma | variabilní | 1 |

## 6. Metadata

- **Tags:** `#governance`, `#architektura`, `#trimming`, `#repo-audit`
- **EROI:** 8/10 (prevence regrese inflace; náklad = zápis jednou, benefit trvalý)
