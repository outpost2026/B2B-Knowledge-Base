# Srovnání architektur: MCP-Jobs vs Legacy Scrapers

**Datum:** 2026-07-31
**Typ:** 02_ANALÝZA — porovnání dvou pipeline
**EROI:** ~8.5/10 (výsledek: rozhodnutí o konsolidaci / zachování parity)

---

## 1. Účel testu

Otestovat dvě architektury lovu pracovních nabídek na **stejných datech téhož dne (2026-07-31)**:

| Architektura | Lokace | Matcher | Datový model |
|---|---|---|---|
| **MCP-Jobs** (pipeline) | `MCP-Jobs\` | boolean AST parser (AND/OR/NOT, NFKD) | Snapshot per run (etl_{PROFILE}_{ts}.json) |
| **Scrapers** (legacy) | `scrapers\` | keyword CSV (topics.csv, 94 kw) + AND `+` / exclude `|` | **Incrementální** Master_Prace_Index.csv (od dubna 2026) |

MCP-Jobs je testován ve dvou profilech:
- **AI-NATIVE** (`config.yaml`) — 14 AI/IT/CNC dotazů, jobs 20 str. + pracecz, bazos jen CNC
- **LEGACY-MANUAL** (`config_legacy_manual.yaml`) — 7 řemeslných dotazů, včetně bazos; po korekčním balíku (run 162838)

---

## 2. Objemy (stejný den 31.7.)

| Architektura | uniq ad | match záznamů | runtime | match/s |
|---|---|---|---|---|
| MCP-AI-NATIVE (154939) | 15 | 26 | 99.9 s | 0.150 |
| MCP-LEGACY-MANUAL (162838) | 48 | 54 | 116.6 s | 0.412 |
| Scrapers Master (celkem) | 168 | 169 | ~180 s | 0.117 |
| **Scrapers fresh (jen 31.7.)** | **21** | 21 | — | — |

> **Klíčový rozdíl datového modelu:** Scrapers Master je **kumulativní úložiště** (data od 29.4.2026, jen 21/168 záznamů je z dnešního běhu). MCP je čistý snapshot — každý run reprezentuje "teď". Pro férové srovnání pokrytí je nutné porovnat Scrapers-fresh (21 ad) vs MCP (63 uniq).

## 3. Průniky

| Průnik | Počet | % z 1. množiny |
|---|---|---|
| MCP-AI ∩ Scrapers (celkem) | 4/15 | 27 % |
| MCP-LEG ∩ Scrapers (celkem) | 14/48 | 29 % |
| MCP-AI ∩ MCP-LEG | 1 | 7 % |
| **MCP-AI ∩ Scrapers-fresh (31.7)** | **1/15** | **7 %** |
| **MCP-LEG ∩ Scrapers-fresh (31.7)** | **7/48** | **15 %** |
| **Scrapers-fresh ∩ (MCP-AI ∪ MCP-LEG)** | **8/21** | **38 %** |

Interpretace: MCP a Scrapers se **vzájemně málo překrývají** (7–15 %). Obě architektury loví částečně odlišný trh:
- MCP-LEG chytí facility-management, údržbáře, elektrikáře přes **plný popis inzerátu** (Solution B).
- Scrapers chytí ady, které MCP nezachytil: `Cost Manager - elektroinstalace/TZB`, `Provozní elektrikář`, `Elektromontér`, `Specialista řízení zakázek - elektroinstalace`, `Brigádník/Junior Data Analyst & AI Developer`, `Montážník stínící techniky`.

## 4. Kvalita (semantická)

| Metrika | MCP-LEG (162838) | Scrapers |
|---|---|---|
| Nemecko/ubytování spam | **0** (korekce 5→0) | **stále chytá** (`💥DLAŽDIČ - ZAHRADNÍK - PRÁCE V NĚMECKU💥`) |
| Popis inzerátu | 38/48 ad (79 %) | 70/168 (42 %) |
| FP (z dřívější analýzy) | ~17 % (hlavně široké servisní techniky) | n/a |

Korekční balík (blokace nemecko, strechy=[praha], facility scope, elektrotechnik, CNC split) **potvrzen jako funkční**: spam 5→0, spravce_budov chytil facility, elektrikar našel pracecz trh. Uživatel balík commitnul samostatně.

## 5. Maturita / architektura

| Aspekt | MCP-Jobs | Scrapers |
|---|---|---|
| Testy | 103 unit testů ✅ | nemá (n/a) |
| Matcher | boolean AST + NFKD, word-boundary | keyword CSV, word_boundary jen title |
| Popis | Solution B (enrichment desc) | desc = jen surové |
| Profile izolace | ✅ profile tag v JSON/MD/CorrelationRecord | ❌ jeden Master index |
| Encoding | UTF-8 ✅ | **cp1250→UTF-8 bug** (UnicodeDecodeError v reader-threadech orchestrátoru) |
| Datový model | snapshot | kumulativní (stagnace: duben→červenec) |

## 6. Závěr

1. **Obě architektury zůstávají komplementární** — MCP chytí ~38 % z toho, co Scrapers vidí čerstvě; 62 % fresh ad je pouze ve Scrapers (široká keyword krytí). Oboustranné doplnění zvyšuje pokrytí trhu.
2. **MCP je zralejší** (testy, snapshot, profile izolace, boolean matcher, popisová enrichace), **Scrapers má širší surové pokrytí** (94 keywordů, 4 portály vč. Nyx).
3. **Scrapers má 2 konkrétní deficity**: (a) kumulativní Master index bez freshness filtru, (b) cp1250/UTF-8 decode bug. Doporučeno opravit `read.decode('cp1250')` fallback a přidat `scraped_at` filtr pro "fresh" pohled.
4. **Nemecko-spam blokaci importovat i do Scrapers topics.csv/exclude** (scrapers ji stále chytá).
5. Rozhodnutí: **ponechat obě** jako dva nezávislé zdroje, MCP jako primární (maturovaný), Scrapers jako raw rozšíření. Konsolidace na jednu architekturu by ztratila ~62 % fresh pokrytí.

---

**Metodika:** norm URL (netloc + path bez trailing /), průniky na uniq adách, fresh filtr dle `scraped_at: 2026-07-31`. Zdrojová data: `MCP-Jobs/output/etl_20260731_154939.json`, `etl_LEGACY_MANUAL_20260731_162838.json`, `scrapers/orchestrator/Master_Prace_Index.csv`.
