# Plán adopce SQL — na míru
**Datum:** 2026-08-16 | **Autor:** outpost2026
**Účel:** Kanonický plán imerzní adopce SQL domény (gap ❷ PostgreSQL) rámovaný aktuální úrovní autora, jeho prací (MCP-Jobs, standalone pivot) a CZ edukačními zdroji — sekvence S1–S6 + metody 60/20/10/10.
**Typ:** plán | **Doména:** skill acquisition, SQL, databáze | **EROI:** 9/10
**Návaznost:** SKILL_GAPS_ROZBOR_Q3_2026_v2.md (gap ❷), ADOPCNI_METODIKA v1 (60/20/10/10), SQL_KANDIDATI_IMERZE_2026-08-15.md (KROK 0–4, V3), IT_gramotnost_hranice_SQL_databazi (E18, dvě vrstvy), MCP-Jobs docs (sql_ontologie, postgresql_zakladni_prikazy, edukace_faze1)

---

## 0. Rozhodnutí (schváleno autorem 2026-08-16)

| ID | Otázka | Verdikt | Důvod |
|----|--------|---------|-------|
| **B.1** | Umístění KROK 0 (master dir index) | **Samostatný nástroj v `_github\`** (nový sub-repo `workspace-index` / lokální tool) | MCP-Jobs produkt drží PostgreSQL (V3 §13 — učební investice gap ❷); SQLite+FTS5 = read-only master index, neprodukční ETL |
| **B.2** | Rozsah nasazení | **Celá sekvence S2–S5 najednou** (2 týdny) | JOIN (S5) je kognitivně levnější před tsunami Next.js (Fáze 2); nekolizuje s Q3 osou TÝDEN 1–6 (gap ❶+❷) |
| — | Workspace 6× `MACHA_PRAHA_*` untracked | **Smazáno uživatelem** | Checkpoint commit před KROK 0 NENÍ potřeba (riziko z SQL_KANDIDATI §10 odstraněno) |

---

## 1. Diagnóza — kde autor stojí (jistota P>0.8, source-read)

| Vrstva | Stav | Evidence |
|--------|------|----------|
| Query-layer, single-table (SELECT/WHERE/ILIKE/ORDER BY/GROUP BY/HAVING/UPDATE/RETURNING, psql meta `\l \dt \d \timing \x`) | **OSVOJENO** | `MCP-Jobs/docs/postgresql_zakladni_prikazy_2026-08-15.md` (ověřeno na 26 ads, 12 firem, 2 portály) |
| Ops-layer (Docker, kontejner, port 5432, volume, psql, db.ps1) | **OSVOJENO** | `edukace_db_prvni_kontakt` + `edukace_faze1_postgresql`; E18 model dvou vrstev |
| Ontologie (DDL/DML/DQL, forma vs odlitek, dependency DDL→DML→DQL, set-based vs buňkový) | **OSVOJENO** | `sql_ontologie_mechanismy` (467 ř., ⚠KOREKCE/✓POTVRZENO) |
| INSERT/ON CONFLICT dedup (upsert_ads, xmax=0 trik) | **OSVOJENO v 1 repo** | `src/mcp_jobs/db.py` — přenos do dalších rep = nízký práh |
| **JOIN (multi-table)** | **NEOVČIČENO** | nepřítomno v referenci; lichess KROK 3 = kognitivní milník |
| **Subquery / CTE** | **NEOVČIČENO** | jen koncept v ontologii |
| **Indexy (mimo UNIQUE), EXPLAIN/VACUUM** | **NEOVČIČENO** | jen UNIQUE z dedup |
| **Transakce** (BEGIN/COMMIT/ROLLBACK) | **NEOVČIČENO** | pojem ano, praxe ne |
| **SQLite + FTS5** (MATCH, BM25) | **NEOVČIČENO** | KROK 0 (V3 revize) |
| **Schema design / normalizace / FK / kardinalita** | **NEOVČIČENO** | KROK 4 — studium outprep + VŠE skripta |

**Klíčový závěr:** autor prošel 1. den adopce (Faze 1 Postgres) za jednu session — query-layer je transfer z Excelu (E18). Zbývá 6 mechanismů; jediná skutečně nová kognitivní investice je **JOIN (set-based propojení entit)**. Ostatní jsou variace osvojeného vzoru (INSERT/ON CONFLICT → dedup → JOIN).

---

## 2. Sekvence adopce (kanon SQL_KANDIDATI V3 + ADOPCNI 60/20/10/10)

| Fáze | PBL úkol (60 %) | Nové mechanismy | Feynman→Glossary (20 %) | Čas |
|---|---|---|---|---|
| **S1** Upevnění | 10 drill dotazů nad live MCP-Jobs DB (26 ads) dle UPOL cvičení | potvrzení GROUP BY/HAVING/ILIKE/LIMIT | — | 1–2 h |
| **S2** KROK 0 | **Master dir index SQLite+FTS5** — 1 schema + 1 crawler + 5 analyt. dotazů (nový nástroj v `_github\`) | SQLite, FTS5, MATCH, BM25, `GROUP BY sha256 HAVING count(*)>1`, inkrementální reindex | `FTS5`, `BM25`, `materialized view`, `INSERT OR IGNORE`, `ON CONFLICT DO NOTHING` | 3–4 h (práh 1 session) |
| **S3** KROK 1 | **scrapers** → SQLite: `INSERT ... ON CONFLICT (url)` dedup + `UNION ALL` master index | dedup přenos 1:1 z MCP-Jobs, UNION ALL | `UNION`, `UNION ALL`, `ON CONFLICT DO NOTHING` | 2–3 h |
| **S4** KROK 2 | **linkedin-mcp**: upsert A/B — `_find_entry_index()` vs `ON CONFLICT DO UPDATE` | upsert pattern, `RETURNING` | `upsert`, `RETURNING` | 2 h |
| **S5** KROK 3 | **lichess-analyzer**: JOIN hra↔pattern, subquery, indexy, časová okna SRS (due/interval) | **JOIN (INNER/LEFT)**, subquery, CREATE INDEX | `JOIN`, `LEFT JOIN`, `subquery`, `index`, `window` | 6–8 h ⭐ |
| **S6** KROK 4 | **outprep** schema studium (10 tabulek, alias relace) + normalizace | FK, normalizace 1NF–3NF, relace 1:N/M:N, ERD | `FK`, `normalizační formy`, `kardinalita` | 2–3 h |

**Průběžně (10 %) — Concept Mapping:** mapa vztahů JOIN→FK→index→výkon; DB↔ETL↔UI (Mermaid, LLM generované).
**Průběžně (10 %) — SRS:** flashcards z nových glossary termínů, FSRS engine (py-fsrs, sdílený balíček s chess Phase 5), 10 min/den, 5 dní/týden.
**Cíl glossary (Feynman 20 %):** +6 kontextovaných termínů dle metriky SQL_KANDIDATI §11: JOIN, LEFT JOIN, index, transaction, FK, ON CONFLICT, FTS5, BM25.

### 2.1 Sled závislostí (DDL→DML→DQL — princip z ontologie)

```
S1 (drill na existující DB) → S2 (navrhni schéma 0→1, crawler plní) → S3 (dedup = ON CONFLICT, UNION ALL)
→ S4 (upsert A/B demonstrace) → S5 (relace: JOIN, subquery, indexy) → S6 (návrh schématu: FK, normalizace)
```

Dependency: každá fáze staví na mechanismu předchozí (S5 potřebuje relace = FK z S6? NE — JOIN na existujících relačních datech lichess funguje i bez FK; FK se doučí v S6 jako integrita, JOIN v S5 jako dotaz). Pořadí S5→S6 je dotaz-před-návrhem: nejdřív osvoj dotazování relací, pak integritu jejich návrhu.

---

## 3. Mapa CZ zdrojů per fáze (integrace rešerše 2026-08-16)

| Fáze | CZ zdroj | Role | URL |
|------|----------|------|-----|
| S1 | **UPOL — Pomůcka pro výuku SQL** | interaktivní drill + SQL editor (0 setup, browser) | https://vyukasql.inf.upol.cz/ |
| S1/S5 | **ITnetwork — PostgreSQL krok za krokem** (lekce 9–13: JOIN, M:N, poddotazy) | strukturovaný CZ výklad — číst před lichess PBL | https://www.itnetwork.cz/postgresql |
| S2 | vzory `repo-indexer` (GusBedasi), `ffts-grep` (mneves75) | mechaniky FTS5 + inkrementální reindex (převzít, ne kopírovat) | EN GitHub (z rešerše V3 §8) |
| S3–S4 | MCP-Jobs `src/mcp_jobs/db.py` (upsert_ads) | přenosový vzor 1:1 (source-read) | — |
| S5 | **MFF UK Lab-05 SQL Querying PDF** (Svoboda) | schema + JOIN/subquery cvičení (teorie před PBL) | https://www.ksi.mff.cuni.cz/~svoboda/courses/202-B0B36DBS/labs/Lab-05-SQL-Querying.pdf |
| S5 | **ČVUT FEL B0B36DBS lab-06 SQL** | dotazovací cvičení (JOIN, vnořený SELECT) | https://cw.fel.cvut.cz/b242/_media/courses/b0b36dbs/lab-06-sql-data.pdf |
| S5 | **Lovely Data: SQL pro každý den** (e-kniha, 115 s.) | praktické SQL vzory (CTE, subquery, STRING_AGG, JOIN) | https://www.lovelydata.cz/mooc/kurz/LDO052-sql-pro-kazdy-den/ |
| S6 | **VŠE: Datové modelování a návrh relační databáze** (Chlapek, Kučera, Palovská — řešené úlohy) | normalizace + ERD + relační návrh | https://ipac.kvkli.cz/arl-li/cs/detail-li_us_cat-1263457-Datove-modelovani-a-navrh-relacni-databaze/ |
| S6 | **postgres.cz wiki** (CSPUG, Pavel Stěhule) | CZ referenční dokumentace PostgreSQL | https://postgres.cz/wiki/PostgreSQL |
| Ref | **odinuv.cz — Database & SQL** | most web app ↔ PostgreSQL (využít až ve Fázi 2 Next.js GUI) | https://odinuv.cz/walkthrough/database-intro/ |
| Ref | **VŠB-TUO — Database Systems I** | relační algebra — prohloubení set-based myšlení (volitelné) | https://edison.sso.vsb.cz/ |
| Ref | **Lovely Data — SQL pro analytiky** (26 lekcí video) | rychlý video přehled jako syntéza (začátečník, autor je za ním) | https://www.lovelydata.cz/mooc/kurz/LDO005-sql-pro-analytiky/ |

**Vyloučeno (nízká hodnota pro tuto úroveň):** Khan Academy (základy), Umíme informatiku (základy), Czechitas (začátečník, teorie), Naučmese (začátečník), P2D2/CSPUG (až jako networking po adopci), GISMentors PostGIS (mimo doménu), skoleni-ict.cz / pckurzy.cz / Pumpedu (placené školení — PBL nahrazuje).

---

## 4. Časový budget a milníky (ověřitelné)

| Milník | Horizont | Metrika (falsifikovatelná) |
|--------|----------|----------------------------|
| S1 + S2 hotovo | do 1 session (den 1) | 5 analyt. dotazů zodpovězeno; cross-repo duplicity VCF nalezeny (`GROUP BY sha256 HAVING count(*)>1`) |
| S3 + S4 hotovo | +3 dny | A/B demonstrace: ruční upsert nahrazen `ON CONFLICT DO UPDATE`, stejné chování (test) |
| **S5 JOIN funkční** | +7–10 dní | produkční dotaz hra↔pattern v lichess; metrika "JOIN v praxi" ✓ |
| S6 + glossary + SRS balíček | +14 dní | +6 kontextovaných termínů v glossary; SRS běží 5 dní/týden 10 min |

**Celkem: ~15–20 h = přesně budget gapu ❷ PostgreSQL (SKILL_GAPS v2, 8.5/10).**
**Práh zastavení (z SQL_KANDIDATI §10):** pokud KROK 0 (S2) přesáhne 1 session → scope redukce na FTS5-path index bez commit historie.

---

## 5. Artefaktový výstup (při exekuci, dle kb-workflow)

| Artefakt | Modul | Commit template |
|----------|-------|-----------------|
| tento plán (kanon) | `00_STRATEGIE/01_positioning/` | `[STRATEGIE] add: SQL_ADOPCE_PLAN (EROI 9/10)` |
| S2 nástroj: schema.sql + crawler + 5 dotazů | nový sub-repo `workspace-index` (B.1) | `[docs] add: KROK 0 master index (EROI 8/10)` |
| S3–S4: dedup/upsert implementace | `scrapers`, `linkedin-mcp-custom` | `[feat] add: SQL dedup ON CONFLICT (EROI 8/10)` |
| S5: JOIN query hra↔pattern | `lichess-analyzer-mcp` | `[feat] add: JOIN pattern query (EROI 9/10)` |
| Glossary termíny | `01_METODIKY/06_SWE_glossary/SWE_GLOSSARY_zive_v1.md` | `[METODIKY] update: glossary SQL terms (EROI 8/10)` |
| Koncept mapa DB↔ETL↔UI + JOIN→FK→index | `05_EPISTEMIKA/03_kognitivni_ontologie_nastroju/` | `[EPISTEMIKA] add: SQL concept map (EROI 7/10)` |
| SRS flashcards | sdílený FSRS balíček (chess Phase 5) | `[feat] add: glossary SRS cards (EROI 8/10)` |

---

## 6. Guardrails

- **Anti-blackbox (pravidlo 5 adopce):** každý SQL výstup z LLM projít a vysvětlit vlastními slovy (Feynman) — zejména JOIN plán v S5.
- **SQLite DB soubor do `.gitignore`** (derivát, ne zdroj); schema.sql commitovat.
- **`origin`/`is_foreign` z `git remote`, nikdy ručně** (oprava V3 — prevence subagentní chyby).
- **MD = kanon, DB = materialized view; tok MD→DB, nikdy DB→MD** (SQL_KANDIDATI §12.4).
- **ASCII-NOM** názvy souborů, header dle šablony, bez emoji/Unicode symbolů (cp1250).
- **Termíny jen z reálného kontextu** (guardrail Epistemického rámce — kvalita > kvantita).
- **Žádná data na skládku:** každý mechanismus má produkční repo (S2–S5 mapováno).

---

## 7. Rizika a mitigace

| Riziko | Pravděpodobnost | Dopad | Mitigace |
|--------|:---------------:|:-----:|----------|
| S2 scope creep (server/UI/embeddings) | Střední | Střední | Práh 1 session; CLI dotazy, žádné UI |
| S5 JOIN → rabbit hole (window/analytic) | Střední | Nízký | S5 rozsah = INNER/LEFT JOIN + subquery; window funkce až později |
| Glossary > praxe (pravidlo 60/20) | Střední | Vysoký | Glossary nikdy přes 20 % času |
| SRS opuštěno po 2 týdnech | Vysoká | Střední | 10 min/den fixní, LLM generuje karty |
| Kolize s Fází 2 (Next.js) | Střední | Střední | B.2: sekvence S2–S5 najednou vpředu; S6+glossary+SRS leží souběžně, ne blokuje |

---

## 8. Trajektorie v kontextu Q3

```
Q3 TÝDEN 1–2:  S1 drill → S2 KROK 0 (workspace-index, SQLite+FTS5) → S3 scrapers dedup
Q3 TÝDEN 3:    S4 linkedin upsert A/B → S5 lichess JOIN (milník)
Q3 TÝDEN 4:    S6 outprep schema studium + normalizace + VŠE úlohy
Průběžně:      glossary +Feynman, koncept mapy, SRS 10 min/den
Následně:      Fáze 2 Next.js (gap ❶) — odinuv.cz jako most web↔DB
```

*Dokument vytvořen: 2026-08-16 | Autor: outpost2026 | Verze: 1.0*
*Návaznost: SKILL_GAPS v2, ADOPCNI_METODIKA, SQL_KANDIDATI_IMERZE V3, IT_gramotnost_hranice (E18), MCP-Jobs edu docs*