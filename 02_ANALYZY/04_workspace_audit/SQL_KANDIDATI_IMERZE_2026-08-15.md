# SQL Kandidáti imerze — cross-repo audit portfolia
**Datum:** 2026-08-15 | **Autor:** outpost2026
**Účel:** Identifikace repozitářů, kde lze imerzně adoptovat SQL rodinu (PBL na vlastních projektech) — vychází z plného scanu master diru `_github\` (19 repů, T+4 měsíce IT sprintu).
**Typ:** analýza | **Doména:** skill acquisition, SQL, workspace audit | **EROI:** 8/10
**Návaznost:** SKILL_GAPS_ROZBOR_Q3_2026_v2.md (gap ❷ PostgreSQL), ADOPCNI_METODOLOGIE_2026_v1.md, sql_ontologie_mechanismy_2026-08-15.md (MCP-Jobs), IT_gramotnost_hranice_SQL_databazi_2026-08-15.md (E18), eroi_chronologicky_plan_s_metodikou.md, CONTEXT_REPOS.md (master dir struktura)

> **V2 (2026-08-15):** De novo deep-dive master diru (59 401 souborů, 2,59 GB) + rešerše trhu (9 analogických nástrojů). Revize: KROK 0 (master dir index) přechází z PostgreSQL na **SQLite + FTS5** — konvergence trhu, simple > complicated.
> **V3 (2026-08-15):** Sekce 12 — analýza live index souborů (INDEX.md + CONTEXT_REPOS.md) vs SQL DB. Verdikt: MD zůstává kanon, SQLite = materialized view (2 parser tabulky v KROK 0).

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
KROK 0: master dir index → SQLite+FTS5 (metadata + fulltext + dedup; viz sekce 9-11)
KROK 1: scrapers        → INSERT + ON CONFLICT (url) dedup, UNION ALL master index
KROK 2: linkedin-mcp    → upsert A/B (ruční _find_entry_index vs ON CONFLICT UPDATE)
KROK 3: lichess-analyzer → JOIN hra↔pattern, subquery, indexy, časová okna (SRS due/interval)
KROK 4 (vzor): outprep   → studium kanonického schema designu (10 tabulek, alias relace)
```

Každý krok = PBL na reálných datech + Feynman zápis nových termínů (JOIN, index, transaction, FK) do glossary + koncept mapa vztahů (ADOPCNI_METODOLOGIE 60/20/10/10).

**Klíčový poznatek:** Posloupnost 0→1 je téměř 1:1 přenos z MCP-Jobs (stejná ETL doména). Krok 3 je kognitivní milník — tam se JOIN naučí doopravdy (navazuje na sql_ontologie sekci 5.4).

---

## 7. Deep-dive master diru (V2 — doménová znalost)

De novo analýza celého `_github\` (2 subagenti + ověření klíčových struktur):

| Fakta | Hodnota |
|-------|---------|
| Velikost | **59 401 souborů, 2,59 GB** (dominují cizí klony: outprep 950 MB, lichess 437 MB, linkedin 247 MB, GCP 172 MB) |
| Vrstvy | master root + `.ci/.session/.scripts/.opencode` → 19 sub-rep (gitlinky) → non-git artefakty (KB 61 souborů, B2B 56, VCF_files_moodpasta 35× .VCF, github_mirror 3 generace snapshotů) |
| Master git repo | lokální, `main`, bez remote; `.git/` 147,9 MB; **working tree není clean** (6× MACHA_PRAHA_* untracked + 4 gitlinky) |
| `mcp_audit.log` | 6 631 řádků — smíšený formát (plain + JSONL), 2 331× ListTools, 1 588× CallTool |
| `github_digital_twin_context.json` | 46,9 KB, 17 klíčů — **obsahuje case-duplicitní klíče (`VCF`/`vcf`) → parsovatelný jen Pythonem, ne PowerShell ConvertFrom-Json** |
| SQL soubory | žádné `*.sqlite`; 3 skutečná schémata (MCP-Jobs schema.sql, outprep schema.sql + migrace); 16× SQLite = jen `.mypy_cache` |

### 7.1 Klíčové zjištění: neexistuje žádný index

| Součást | Jak funguje dnes | Důsledek |
|---------|------------------|----------|
| `tool_kb_search` | **plný scan všech souborů při každém volání** (booleovské skórování slov, bez TF/IDF), TTL cache jen 300 s | O(N) na volání — s 90+ artefakty už hraniční |
| `tool_cross_repo_search` | `git grep` subprocess na každý repo (4 vlákna, timeout 15 s) | Rychlý, ale bez struktury (jen řádky) |
| `rag_indexer` | **mrtvý artefakt** — nikdy nespouštěn na `_github`; taxonomie vázaná na starou diskovou strukturu (IOT, GCP); ale obsahuje cenné mechanismy (kaskádové dekódování, SHA-256 dedup, smart snippets) | Střední kandidát se přesouvá do "zdroje mechanismů pro KROK 0" |
| `INDEX.md` (KB) | 450 řádků, řádkový lookup, tag systém | De-facto index — ruční, per-řádek |

---

## 8. Rešerše trhu: analogická řešení (V2)

Prohledány veřejné zdroje + GitHub portfolia řešící "index celého workspace/repo sbírky do DB". **9 nalezených nástrojů, konvergence na SQLite + FTS5:**

| Nástroj | Stack | Řešení | Relevance |
|---------|-------|--------|-----------|
| **repo-indexer** (GusBedasi) | Python + SQLite | walk repo → metadata (path, extension, language, size, line_count, depth, mtime) + **FTS5 tokenized path** (MATCH místo LIKE) | ★★★ Přímý vzor pro KROK 0 |
| **ffts-grep** (mneves75) | Rust, single binary | SQLite FTS5 + BM25, ~10 ms na 10K souborů, **inkrementální reindex**, gitignore-aware, JSON stdin protokol | ★★★ Nejčistší architektura |
| **kdex** (urbanisierung) | Rust + SQLite FTS5 | index repos → sub-ms search, **MCP server výstup**, .gitignore respect, remote repo sync | ★★★ MCP nativní — sedí na autorův stack |
| **Srclight** | Rust, SQLite FTS5 + tree-sitter + embeddings | symboly + fulltext + volitelné embeddings (Ollama), **multi-repo ATTACH** | ★★ tree-sitter = nad rámec (symboly), embeddings volitelné |
| **CodeIndex** (Widthdom) | Rust, SQLite FTS5 | decision table: one-off → rg, **repeated investigation → index**; MCP + LSP | ★★ Kritérium "kdy index, kdy ne" |
| **repoindex** (queelius) | Python + SQLite | DB = **materialized view filesystemu**, refresh-only writer, read-only SQL API, MCP server | ★★ Koncepčně shodné s master dir indexem |
| **repogrep** (fernandoabolafio) | TS, SQLite FTS5 + **LanceDB vektory** | hybrid keyword+semantic (MiniLM embeddings) | ★ Vektorová vrstva jako doplněk, ne jádro |
| **GitQL** (AmrDeveloper, ⭐3.5K) | Rust, in-memory | SQL-like dotazy **přímo na .git** (commits, branches, refs, authors), multi-repo `repository_path` | ★★ Alternativa pro git-metadata bez DB |
| **gitquery** (sqle) | Go | SQL interface na .git (commits, blobs, refs, tags, tree_entries) | ★ Niche, GitQL silnější |

### 8.1 Verdict rešerše (hSNR, simple > complicated)

1. **Konvergence trhu:** 9/9 nástrojů pro "index workspace do DB" používá **SQLite + FTS5**. Žádný nepoužívá PostgreSQL server ani vektorovou DB jako jádro.
2. **PostgreSQL revize:** Vhodný pro write-side produkční ETL (MCP-Jobs — autorův případ), NE pro lokální index čtení. Server + auth + network = zbytečná vrstva pro read-only index 2,6 GB.
3. **Vektorová DB:** Ne. Trh ji používá jen jako volitelný doplněk (embeddings) nad FTS5; autorův use case (exaktní metadata, dedup, fulltext) je deterministický. Odložit.
4. **GitQL:** Zajímavá alternativa pro git-metadata dotazy (bez budování DB), ale nepokrývá filesystem metadata + fulltext obsahu. Do budoucna možný doplněk.

---

## 9. Rozhodnutí: KROK 0 = master dir index (revize)

**Změna oproti V1:** Postgres → **SQLite + FTS5** (jeden soubor, žádný server, plnohodnotný SQL: CREATE/INSERT/UNIQUE/JOIN/GROUP BY/FTS5 MATCH).

**Model (syntéza repo-indexer + ffts-grep + autorův vzor):**

```sql
CREATE TABLE files (
  id INTEGER PRIMARY KEY,
  repo TEXT NOT NULL,            -- sub-repo název (nebo 'root')
  path TEXT NOT NULL,
  extension TEXT, language TEXT,
  size_bytes INTEGER, line_count INTEGER,
  sha256 TEXT,                   -- dedup napříč repy
  mtime TEXT, is_tracked INTEGER, -- git ls-files stav
  UNIQUE(repo, path)
);
CREATE VIRTUAL TABLE files_fts USING fts5(path, content);
CREATE TABLE repos (name TEXT PRIMARY KEY, last_commit TEXT, commit_count INTEGER, remote TEXT);
```

**Plnící skript (~100 řádků Pythonu):** `git ls-files` + `git log --all` + file stat per repo → INSERT + FTS5 index.

**Dotazy, které řeší reálné problémy (z deep-dive):**
- Cross-repo duplicity: `GROUP BY sha256 HAVING count(*) > 1` (VCF soubory napříč vcf_integrace/Vcf-compiler/vcf_parser_b2b)
- Mrtvé repo: `WHERE last_commit < date('now','-3 months')`
- Fulltext cesty: `files_fts MATCH 'vcf'` (místo LIKE '%vcf%')
- Commit velocity per repo: `GROUP BY repo, strftime('%Y-%m', ...)`

**Guardrails:** DB soubor do `.gitignore` (derivát, ne zdroj); respektovat autorovo `EXCLUDE_EXTENSIONS` rozhodnutí (neindexovat cizí binární obsah); `.git` diry skip.

---

## 10. Analýza overengineering / scope creep (V2)

| Riziko | Pravděpodobnost | Dopad | Mitigace |
|--------|:---------------:|:-----:|----------|
| **Postgres cluster pro lokální index** (původní návrh) | Vysoká (u jiných) | Vysoký | Eliminováno — SQLite+FTS5 (sekce 8.1) |
| **Scope creep do embeddingů / vektorů** | Střední | Střední | Odloženo; trh je používá jako doplněk, ne jádro; přidatelnost bez migrace později |
| **Scope creep do UI/dashboardu** (Datasette/Streamlit) | Střední | Střední | KROK 0 = CLI dotazy; UI až když 3 analytické dotazy prokáží hodnotu |
| **Reinventing ffts-grep/kdex** | Vysoká | Střední | Kompromis: **učit se na vlastním PBL** (autorův cíl) — převzít mechaniky (FTS5, inkrementální reindex), ne psát od nuly vlastní engine |
| **Indexace cizích klonů (outprep 950 MB, GCP 172 MB)** | Vysoká | Nízký | Skip dle gitignore (cizí repa už jsou vyloučená v root .gitignore) |
| **Nečistý working tree při startu** | Okamžitá | Nízký | Checkpoint commit před KROK 0 (6× MACHA_PRAHA_* untracked) |

**Verdikt: riziko PŘIJATELNÉ** při zachování rozsahu: 1 crawler + 1 schema + 5 analytických dotazů, žádný server, žádné UI, žádné embeddings. Práh zastavení: pokud KROK 0 přesáhne 1 session, scope se redukuje na FTS5-path index bez commit historie.

---

## 11. Metriky úspěchu (revize V2)

| Metrika | Cíl |
|---------|-----|
| KROK 0: master dir index funkční (SQLite+FTS5, 1 schema + 1 crawler) | < 1 session; 5 analytických dotazů zodpovězeno |
| KROK 0: cross-repo duplicity nalezené | GROUP BY sha256 HAVING count(*) > 1 — reálný počet duplicit (VCF napříč repy) |
| První funkční artefakt (scrapers → SQL) | < 14 dní od startu (transfer metrika z ADOPCNI_METODOLOGIE) |
| JOIN v praxi (lichess) | Funkční join hra→pattern v produkčním dotazu |
| A/B demonstrace (linkedin) | Ruční upsert nahrazen ON CONFLICT se stejným chováním |
| Glossary termíny z SQL imerze | 5+ nových kontextovaných termínů (JOIN, index, transaction, FK, ON CONFLICT, FTS5, BM25) |

---

## 12. Live index soubory vs SQL DB — rozhodnutí (V3)

Analýza dvou ručně editovaných live indexačních souborů workspace a jejich vztahu k SQL rodině.

### 12.1 Přehled obou souborů

| Atribut | `B2B-Knowledge-Base/INDEX.md` | `CONTEXT_REPOS.md` (root `_github\`) |
|---------|-------------------------------|-------------------------------------|
| Role | Registr artefaktů KB (jediný INDEX.md ve workspace) | **Master indexační soubor stavu/statusu master diru** (19 repů, 25 sekcí) |
| Velikost | 450 řádků, v2.2 | 825 řádků |
| Obsah | 6 modulových tabulek `\| # \| Soubor \| Zdroj \| Typ \| Účel \| EROI \|`, tag lookup (20 řádků), statistiky, maintenance log | Per-repo sekce (verze, status, stack, commity, testy), vztahy mezi repy, CI/CD, non-git adresáře, `.ai_state` kontext, **bezpečnostní pravidla (ř. 37–92)**, poznámky k workflow |
| Konzumenti | 3 MCP nástroje: `kb_overview`, `kb_by_module`, `kb_read_doc` (řádkový lookup `_lookup_metadata`, split na `\|`) | Povinný kontext pro agenty dle AGENTS.md (čtení, ne parsování nástroji) |
| Struktura vs narativ | ~70 % strukturované tabulky, ~30 % narativ (maintenance log) | ~60 % strukturované fakta, ~40 % narativ (bezpečnost, workflow poznámky, hodnocení adopce) |
| Drift kontrola | P5 drift check (`git ls-files` vs registrace) | Žádný automatický check — aktualizace per session |

### 12.2 Argumenty contra nahrazení (oba soubory)

| # | Argument | INDEX.md | CONTEXT_REPOS.md |
|---|----------|:--------:|:----------------:|
| 1 | **Objem triviální** — 110 artefaktů / 19 repů; SQL indexy se vyplatí až při 10 000+ záznamech | ✔ | ✔ |
| 2 | **Lidská čitelnost** — high-SNR profil, anti-blackbox; MD = transparentní vrstva, DB = černá skříň s klientem | ✔ | ✔ |
| 3 | **Git audit trail** — `git diff` na MD = čitelné řádky; SQL dump diff = binární šum | ✔ | ✔ |
| 4 | **Bezpečnostní obsah** — CONTEXT_REPOS nese bezpečnostní pravidla (ř. 37–92), která musí být čitelná bez nástrojů | — | ✔ (kritické) |
| 5 | **MCP regrese** — 3 nástroje + 67/67 testů parsují INDEX.md | ✔ | (nekonsumován nástroji) |
| 6 | **P1/P5 mechanismy** — zákaz klonů a drift check staví na git trackování MD | ✔ | ✔ |

### 12.3 Argumenty pro (nadstavba, ne náhrada)

| # | Argument | Síla |
|---|----------|:----:|
| 1 | **Strukturální dotazy nad CONTEXT_REPOS** — "které repo je AKTIVNÍ vs LEGACY", "kolik repů má >100 commitů", "EROI distribuce per modul" = `SELECT ... GROUP BY` místo očního prohlížení 825 řádků | Střední |
| 2 | **Vynucení integrity** — UNIQUE (anti-klon, P1), CHECK (EROI enum) strojově | Střední |
| 3 | **Join obou zdrojů** — artefakt ↔ repo (kb_read_doc metadata + repo status v jedné query) | Nízká |

### 12.4 Verdikt (simple > complicated, hSNR)

| Varianta | Verdikt | EROI |
|---|---|---|
| Nahradit INDEX.md / CONTEXT_REPOS.md SQL DB | **NE** — ztráta čitelnosti, bezpečnostní pravidla v MD, audit trail, MCP regrese, overkill na objem | Záporné |
| **Nadstavba: MD = kanon, SQLite = materialized view** | **ANO, omezeně** — 2 parser tabulky v KROK 0: `artifacts` (z INDEX.md) + `repos_status` (z CONTEXT_REPOS.md sekcí) | 7/10 |
| DB = kanon, MD = generovaný export | **NE teď** — narušuje live workflow; zvážit až při 10× objemu nebo opakovaném driftu | 4/10 |

**Pravidlo:** Tok dat **MD → DB, nikdy DB → MD**. Ruční soubory zůstávají jediným zdrojem pravdy — autorova editace, git historie, MCP nástroje beze změny. SQLite+FTS5 je čistě odvozená dotazovací vrstva. **CONTEXT_REPOS.md je mimo SQL nadstavbu z hlediska obsahu** (bezpečnost + workflow narativ), ale jeho **strukturované hlavičky sekcí** (status, verze) jsou vstupem pro `repos_status` tabulku.

### 12.5 Dopad na KROK 0 (rozšíření)

```
KROK 0 schéma se rozšiřuje o:
  artifacts(id, module, file, type, purpose, eroi, tags)   ← parser INDEX.md tabulek
  repos_status(name, version, status, stack, last_commit)   ← parser CONTEXT_REPOS.md sekcí
Dotaz č. 6: SELECT module, count(*), avg(eroi) FROM artifacts GROUP BY module
Dotaz č. 7: SELECT name, status FROM repos_status WHERE status LIKE '%AKTIVN%'
```

Práh zastavení zůstává: 1 session, žádný server/UI/embeddings.