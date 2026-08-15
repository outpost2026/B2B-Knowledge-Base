# SQL Kandidáti imerze — cross-repo audit portfolia
**Datum:** 2026-08-15 | **Autor:** outpost2026
**Účel:** Identifikace repozitářů, kde lze imerzně adoptovat SQL rodinu (PBL na vlastních projektech) — vychází z plného scanu master diru `_github\` (19 repů, T+4 měsíce IT sprintu).
**Typ:** analýza | **Doména:** skill acquisition, SQL, workspace audit | **EROI:** 8/10
**Návaznost:** SKILL_GAPS_ROZBOR_Q3_2026_v2.md (gap ❷ PostgreSQL), ADOPCNI_METODOLOGIE_2026_v1.md, sql_ontologie_mechanismy_2026-08-15.md (MCP-Jobs), IT_gramotnost_hranice_SQL_databazi_2026-08-15.md (E18), eroi_chronologicky_plan_s_metodikou.md

---

## 1. Východisko a teze

**Kontext:** Existence SQL/RDBMS je pro autora nová (Fáze 1 MCP-Jobs = první SQL DB v životě, osvojeno za 1 den). Metodika adopce = imerzní PBL (60 % dle ADOPCNI_METODOLOGIE): dovednost se NEučí z dokumentů, ale řešením reálných problémů ve známém vývojovém prostředí.

**Teze:** SQL rodinu lze aplikovat u více repozitářů než jen u MCP-Jobs — vícevrstvé úkoly na vlastních datech povedou k pochopení principů SQL přirozeněji než prosté studium.

**Metoda auditu:** Plný scan `_github\` (19 repozitářů), per-repo analýza datových stavů (perzistence, dedup, historie, relace mezi entitami). Ověřeno čtením struktur (CSV hlavičky, resource store, cache adresáře) — ne jen názvy souborů.

**Verdikt teze:** POTVRZENO — 4 silní + 4 střední kandidáti; SQL imerze má v portfoliu přirozenou posloupnost rostoucí náročnosti.

---

## 2. Kritéria kandidatury

Repo je SQL kandidát, pokud jeho data vykazují ≥2 z:

| Kritérium | Signál v datech |
|-----------|-----------------|
| **Dedup** | ruční `set()` / `_find_entry_index` / content-hash — SQL nahradí `UNIQUE` + `ON CONFLICT` |
| **Historie** | snapshoty, `diff_*.md`, verzované analýzy — SQL dá query místo souborů |
| **Relace** | entita→subentita (kresba→vrstvy, hra→analýzy, hráč→hry) — SQL dá FK + JOIN |
| **Stav s nárokem na dotaz** | agregace, cross-zdrojové merge — SQL dá `GROUP BY` / `JOIN` místo merge skriptu |

---

## 3. Silní kandidáti (relace + dedup + historie)

| # | Repo | Datový stav dnes | SQL model | Imerzní hodnota |
|---|------|------------------|-----------|-----------------|
| 1 | **scrapers** | 4 portálové CSVs (`Jobs_RAG_Index.csv`, `PraceCZ_RAG_Index.csv`, `NotebookLM_Bazos_Index.csv`, `nyx_prace_inzeraty.csv`) + `Master_Prace_Index.csv` (agregace 4 zdrojů), `diff_YYYYMMDD_HHMM.md` (inkrementální historie), dedup `existing_urls = set()` → `fresh = [ad for ad in new if ad['url'] not in existing_urls]` (jobsfastv2.py:128-164, pracefastv1.py:116-148) | `ads(url UNIQUE, title, company, salary, location, source, category, scraped_at)`, `runs`, `categories`; dedup = `ON CONFLICT (url)`, diff = query, master index = `UNION ALL` + `GROUP BY` | **Nejnižší práh** — téměř 1:1 přenos z MCP-Jobs (stejný ETL pattern) |
| 2 | **lichess-analyzer-mcp** | `data/game_cache/*.json` (dual cache `{game_id}_{color}_d{depth}`), `resource_store/analysis_store.json` + `pattern_store.json`, `audit_YYYYMM.jsonl`, `srs_cards.json` (FSRS: due/reps/lapses), `reports/*.json` | `games`, `analyses(game_id, color, depth) UNIQUE`, `patterns` + join-tabulka hra↔pattern, `srs_cards(due, interval)`, `audit_events` | **Nejvíc relační náklad** — JOIN hra→pattern, subquery, indexy; navazuje na artefakt 5.4 "šanon s dotazníkem" |
| 3 | **linkedin-mcp-custom** | `analysis/metadata_stacku.json` s ručním upsertem `_find_entry_index()` (dedup dle `linkedin_job_id` + `title|company`), `docs/pipeline_YYYYMMDD_HHMMSS.json` snapshoty, audit navigací | `jobs(job_id UNIQUE)` + `ON CONFLICT UPDATE`, `eroi_results`, `pipeline_runs` | **A/B moment** — vlastní ruční upsert vs jeden SQL řádek; MCP-Jobs je jeho dvojče a SQL už má |
| 4 | **outprep** | Reference: už má Postgres 16 (docker-compose), 10 tabulek (`players`↔`player_aliases`, `games`↔`game_aliases`, `pipeline_runs`, `bot_data_cache`), ETL (TWIC PGN + FIDE ratings) | — (již SQL) | **Kanonicé schema** — vzor, jak vypadá kvalitní ETL-schema design; zdroj učení, ne implementace |

---

## 4. Střední kandidáti (relační data, chybí historie)

| Repo | Relační model | Limita | SQL přínos |
|------|---------------|--------|------------|
| **dxf_integrace** | kresba → vrstvy → entity → barvy (`*_layer_card.csv`, `master_index.json`), `GROUP BY` na dosah | Každý běh přepíše výstup — žádná historie | `GROUP BY` barva/vrstva; historie běhů by se musela přidat |
| **vcf_integrace** | soubor → vrstvy → entity → barvy, `rules.json` (pravidlový engine), verzované analýzy v12–v15 | Dávkový generátor artefaktů, žádné UNIQUE klíče | Verzovaná historie = přirozená tabulka `analysis_runs` |
| **rag_indexer** | `files(path, sha256 UNIQUE, category, indexed_at)` — dedup po content-hash už existuje | Jediný stateless skript, výstup = jeden JSON | UNIQUE(hash) dedup; přínos roste se škálováním indexu |
| **mcp-local-server** | `.ai_state.json` = KV state (atomický zápis + `.bak` recovery), `mcp_audit.log` | Záměrně file-based lightweight nástroj | Konceptuálně už SQL-like (KV + audit + cache); transakce by přidaly, ale infrastruktura je záměrná |

---

## 5. Slabí / bez přínosu (vyloučeno)

| Repo | Důvod vyloučení |
|------|-----------------|
| cad2llm | Pure convertor bez stavu, cache, historie či relací |
| vcf_color_service | Statická lookup tabulka ACI→barva (config.json stačí) |
| web_integrace_systeq | Statická integrace; jediný stav = triviální PHP counter |
| outpost_security_perimeter | Koncepční repo bez běžící data pipeline (SQL by dával smysl až při realizaci IoT telemetrie) |
| kazuistiky_llm_sprint | Obsahové MD repo; jediný skript běží externě (VM) |
| outpost2026_profile | Jen README, žádný kód |
| vcf_parser_b2b, Vcf-compiler, GCP (cloud-run-mcp, gcloud-mcp) | Klonované/starší artefakty mimo datový stav (vyloučeno bez deep dive — viz riziko v sekci 7) |

---

## 6. Imerzní posloupnost (rostoucí náročnost)

```
KROK 1: scrapers        → INSERT + ON CONFLICT (url) dedup, UNION ALL master index
KROK 2: linkedin-mcp    → upsert A/B (ruční _find_entry_index vs ON CONFLICT UPDATE)
KROK 3: lichess-analyzer → JOIN hra↔pattern, subquery, indexy, časová okna (SRS due/interval)
KROK 4 (vzor): outprep   → studium kanonického schema designu (10 tabulek, alias relace)
```

Každý krok = PBL na reálných datech + Feynman zápis nových termínů (JOIN, index, transaction, FK) do glossary + koncept mapa vztahů (ADOPCNI_METODOLOGIE 60/20/10/10).

**Klíčový poznatek:** Posloupnost 1→2 je téměř 1:1 přenos z MCP-Jobs (stejná ETL doména). Krok 3 je kognitivní milník — tam se JOIN naučí doopravdy (navazuje na sql_ontologie sekci 5.4).

---

## 7. Rizika a omezení auditu

| Riziko | Dopad | Mitigace |
|--------|:-----:|----------|
| Scan subagentem + ověření struktur, ne 100 % čtení kódu | Nízký | Klíčové vzory (dedup, upsert) ověřeny čtením zdrojů (jobsfastv2.py, kb_writer.py) |
| Repa vyloučená bez deep dive (vcf_parser_b2b, Vcf-compiler) | Nízký | Při zahájení KROKU na konkrétním repu provést plný read |
| Kandidát se může ukázat jako "SQL overkill" (file-based je dostačující) | Střední | Pravidlo CO/PROČ/JAK/EFEKT z CONTEXT_REPOS.md — SQL implementovat jen když EFEKT > náklady |
| determinismus vs distribuované systémy (nerelevantní zde, SQL je deterministický) | — | — |

---

## 8. Metriky úspěchu

| Metrika | Cíl |
|---------|-----|
| První funkční artefakt (scrapers → Postgres) | < 14 dní od startu (transfer metrika z ADOPCNI_METODOLOGIE) |
| JOIN v praxi (lichess) | Funkční join hra→pattern v produkčním dotazu |
| A/B demonstrace (linkedin) | Ruční upsert nahrazen ON CONFLICT se stejným chováním |
| Glossary termíny z SQL imerze | 5+ nových kontextovaných termínů (JOIN, index, transaction, FK, ON CONFLICT) |