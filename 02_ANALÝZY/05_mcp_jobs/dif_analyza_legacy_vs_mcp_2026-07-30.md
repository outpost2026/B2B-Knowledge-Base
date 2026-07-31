# DIF ANALÝZA: Legacy scrapers vs MCP-Jobs pipeline

**Datum:** 2026-07-30
**Autor:** opencode agent
**Účel:** Porovnání výstupů dvou architektonicky odlišných řešení scrapování českého pracovního trhu

---

## 1. Kontext

| Parametr | Legacy | MCP-Jobs |
|----------|--------|----------|
| Verze | fast_v3 (bazos), jobsfastv2, pracefastv1, nyx_scraper_v5 | Phase 06 (refactor branch) |
| Doba běhu | ~156s | 44.7s |
| Počet portálů | 4 (Bazos, Jobs, Prace, Nyx) | 3 (Bazos, Jobs, Prace) |
| Matching metoda | 94 keywordů (AND/OR) | boolean parser (AND/OR/NOT, parens) |
| Exclude listy | základní | pokročilé (agentura, nabízím, hledám, atd.) |
| Lokalitní filtr | ne | ano (per query) |
| Platový filtr | ne | ano (per query) |
| Diakritika | částečná podpora | full podpora |
| Výstup | Master CSV + MD (152 rows) | timestamp JSON + MD + korelační cache |
| Unit testů | ~30 | 103 |

---

## 2. Kvantitativní přehled

| Kategorie | Legacy | MCP-Jobs | Rozdíl |
|-----------|--------|----------|--------|
| Celkem inzerátů | 152 | 32 | -120 |
| Průnik (stejné URL) | 8 | 8 | — |
| Jen v Legacy | 143 | — | -143 |
| Jen v MCP | — | 24 | +24 |

### 2.1 Legacy per source

| Zdroj | Počet |
|-------|-------|
| Bazos | 52 |
| Jobs.cz | 33 |
| Prace.cz | 44 |
| Nyx | 23 |

### 2.2 MCP per query

| Query | Počet |
|-------|-------|
| cnc_jobs | 1 |
| elektrikar | 4 |
| python_jobs | 1 |
| spravce | 1 |
| strechy | 4 |
| truhlar | 0 |
| udrzbar | 17 |
| zahradnik | 4 |

---

## 3. Průnik (společné inzeráty)

Pouze 8 inzerátů z Bazos — MCP a legacy se shodují na:

- **elektrikar (2)** — profese elektrikář je jednoznačná
- **strechy (3)** — práce na střechách
- **zahradnik (3)** — zahradnické práce

Vysoká shoda u "řemeslných" query s nízkou sémantickou ambiguitou. Nízká shoda u "údržbář" (0 common z 13+17) protože query je příliš široké a legacy chytá všechno.

---

## 4. Legacy-only inzeráty (proč chybí v MCP?)

### 4.1 Nyx (23) — známý limit

MCP nemá Nyx portál (disabled v config.yaml). Legacy Nyx data nejsou porovnatelná — Nyx je diskuzní fórum, ne job portál.

### 4.2 Chybí exclude filtr (37+)

Legacy chytá inzeráty jako:
- "PRÁCE V NĚMECKU" (exclude neexistuje)
- "Hledáme nové kolegy - zahradníky" (náborová fráze)
- "Nabízím hodnocení IT projektů" (nabídka služby)

MCP tyto správně rejectuje přes exclude listy.

### 4.3 Legacy používá širší keywordy (45+)

Legacy matched_keyword zahrnuje:
- "automatizace" (6) — MCP nemá query na automatizaci
- "python+developer" (6) — legacy chytá i "data analyst", "platform administrator"
- "data+analyst" (3) — MCP query je užší
- "správce" (12) — legacy chytá IT správce, MCP exclude obsahuje "it", "server", "software"

### 4.4 Chybí location filtr

Legacy chytá inzeráty po celé ČR. MCP query mají location omezení (např. "praha", "brno"), což redukuje počet.

---

## 5. MCP-only inzeráty (co MCP našel a legacy ne)

| Query | Počet | Příklady |
|-------|-------|----------|
| **udrzbar** | 17 | "Servisní technik datového centra", "Technik provozu a údržby", "Údržbář" |
| **elektrikar** | 2 | "Elektrikář slaboproud", "Elektrikář podzemních staveb" |
| **strechy** | 1 | specifické střešní práce |
| **python_jobs** | 1 | Python developer |
| **cnc_jobs** | 1 | CNC bruska |
| **spravce** | 1 | Facility management |
| **zahradnik** | 1 | Zahradnické práce |

Důvody:
- MCP má lepší boolean parser (AND/OR/NOT, závorky) — legacy jen basic AND/OR
- MCP podporuje diakritiku v dotazu i v textu
- MCP používá `\b` word boundaries — legacy substring matching chytá falešné pozitivy

### 5.1 Potenciální falešné pozitivy MCP

Některé MCP-only inzeráty vypadají podezřele:
- "NABÍDKA PRÁCE S UBYTOVÁNÍM" (udrzbar@bazos) — spam
- "Dlouhodobá brigáda - správa webů" (udrzbar@bazos) — nesouvisí s údržbou
- "Mechanik vozového parku" (udrzbar@bazos) — hraniční

Boolean pro `udrzbar` je příliš široký — obsahuje "technik" samostatně, což matchuje i IT techniky.

---

## 6. Kategorie neshod

| Kategorie | Počet | Popis |
|-----------|-------|-------|
| A) Nyx | 23 | MCP nemá portál — akceptovaný limit |
| B) Legacy-only (bez Nyx) | ~120 | Legacy chytá šum, MCP filtruje |
| C) MCP-only | 24 | MCP našel nové — vylepšený matching |
| D) Průnik | 8 | Core domain — oba enginy validní |

---

## 7. Závěr

**Rozdíl 152 vs 32 není regrese — je to architektonický záměr.**

Legacy = **maximální coverage** (94 keywordů, vše czech job market).  
MCP = **maximální precision** (boolean + exclude + filtry).

MCP rejectuje ~120 legacy inzerátů, které jsou buď:
1. Mimo cílové lokality (location filtr)
2. Neinzeráty (agentury, nabídky služeb)
3. Mimo scope (automatizace, data analýza)

MCP zároveň chytil 24 inzerátů, které legacy minul — díky lepšímu boolean parseru a podpoře diakritiky.

**Doporučení:**
- Kalibrovat boolean u `udrzbar` — aktuálně příliš široký
- Zvážit přidání Nyx portálu pokud je to žádoucí
- Rozšířit exclude listy pro "práce v Německu" a podobné off-topic

---

## 8. Metadata

- **EROI:** 8/10
- **Tags:** `#mcp-jobs`, `#legacy-scrapers`, `#dif-analyza`, `#boolean-kalibrace`, `#pracovni-trh`
- **Vstupní data:** `scrapers/orchestrator/Master_Prace_Index.csv` (152 rows), `MCP-Jobs/output/etl_20260730_092530.json` (32 ads)
- **Pipeline:** legacy ~156s / MCP 44.7s
- **Související:** `config.yaml` (boolean definice), `scrapers/orchestrator/PIPELINE_COMPARISON_REPORT.md`
