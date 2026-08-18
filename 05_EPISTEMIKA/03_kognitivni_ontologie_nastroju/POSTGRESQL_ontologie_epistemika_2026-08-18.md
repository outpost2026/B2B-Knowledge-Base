# PostgreSQL: ontologie a epistemika pro deva
**Datum:** 2026-08-18 | **Autor:** outpost2026
**Účel:** Fundamentální ontologická mapa + epistemické pasti SQL/PostgreSQL pro deva při adopci domény — převod *unknown unknowns* na *known unknowns* (ontologie = co existuje, epistemika = jak poznáš, že máš pravdu)
**Typ:** esej / kognitivní rámec | **Doména:** epistemika, kognitivní ontologie nástrojů, SQL, databáze | **EROI:** 8/10
**Návaznost:** `05_EPISTEMIKA/03_kognitivni_ontologie_nastroju/IT_gramotnost_hranice_SQL_databazi_2026-08-15.md` (E18, dvě vrstvy), `00_STRATEGIE/01_positioning/SQL_ADOPCE_PLAN_2026-08-16.md` (S1–S6), `MCP-Jobs/docs/sql_ontologie_mechanismy_2026-08-15.md` (mechanismy: DDL/DML/DQL, forma vs odlitek), `MCP-Jobs/docs/postgresql_zakladni_prikazy_2026-08-15.md` (praxe)
**Provenance:** summary (konceptuální odvození z adopce gapu ❷ PostgreSQL; kontext dedup cvičení ověřen live psql na MCP-Jobs DB — 93 ads, 7 pipeline_runs, 2026-08-18)

---

## 1. Ontologie — co ve světě SQL *existuje*

Ontologie = mapa entit a jejich vztahů. Bez ní se dotazy píšou naslepo.

### 1.1 Vrstvy (zvenku dovnitř)

| Vrstva | Co to je | Příklad z praxe |
|--------|----------|-----------------|
| **Cluster** | jeden běžící server, hostí více databází | kontejner `mcp-jobs-postgres` |
| **Database** | izolovaný prostor uvnitř clusteru | `mcpjobs` |
| **Schema** | namespace uvnitř DB, seskupuje tabulky | `public` (výchozí) |
| **Tabulka** | relace = strukturovaná fakta | `ads` |
| **Řádek / sloupce** | entita + atributy | 1 inzerát, 1 URL |
| **Typy** | kontrakt hodnot | `integer`, `text`, `timestamp`, `boolean`, `jsonb`, `numeric` |

Jistota: P>0.9. Pořadí vrstvení je pevné (database nemůže být uvnitř tabulky).

### 1.2 Datové typy a NULL — trojhodnotová logika

- Každý sloupec má **typy** → DB hlídá, co se do něj smí uložit.
- **NULL ≠ 0, ≠ prázdný řetězec.** NULL = "hodnota není známa".
- Důsledek: logika v SQL je **trojhodnotová** — `TRUE / FALSE / UNKNOWN`.
- `x != 5` vrací pro NULL-x hodnotu `NULL` (UNKNOWN), ne `TRUE`. To je nejčastější zdroj špatných SQL závěrů.

### 1.3 Constraints — DB vymáhá fakta za tebe

| Constraint | Co hlídá | Důsledek |
|------------|----------|----------|
| `PRIMARY KEY` | jednoznačná identita řádku | `id` se nesmí opakovat |
| `UNIQUE` | hodnota sloupce se nesmí opakovat | nativní dedup (např. `url`) |
| `FOREIGN KEY` | odkaz na řádek jiné tabulky | vymáhá relace a pořadí mazání |
| `CHECK` | podmínka na hodnotu | např. `score >= 0` |

Integrity constraints dělají část tvé logiky **za tebe** — je to delegace fakt, ne obrana.

### 1.4 Transakce a ACID

**Transakce** = dávka operací, která je *buď celá, nebo vůbec*.

| Vlastnost | Význam |
|-----------|--------|
| **A**tomicity | vše nebo nic |
| **C**onsistency | DB přejde z platného stavu do platného |
| **I**solation | souběžné transakce se nevidí uprostřed |
| **D**urability | po COMMIT přežije pád stroje (díky WAL) |

### 1.5 DDL vs DML vs DQL

| Třída | Příkazy | Účel |
|-------|---------|------|
| **DDL** | `CREATE`, `ALTER`, `DROP` | definice struktury (schéma) |
| **DML** | `INSERT`, `UPDATE`, `DELETE` | manipulace s daty |
| **DQL** | `SELECT` | dotazování (čtení) |

Závislost: DDL → DML → DQL. Nemůžeš vkládat do tabulky, která neexistuje.

### 1.6 Pořadí vyhodnocení SELECT

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

Toto pořadí ≠ pořadí psaní. Je to důvod, proč:
- **WHERE** vidí jen řádky (ne agregace) → `WHERE COUNT(*) > 5` selže,
- **HAVING** vidí skupiny (agregace) → `HAVING COUNT(*) > 5` funguje,
- aliasy z `SELECT` nelze použít v `WHERE` (ještě neexistují).

### 1.7 Klient-server a vstupní bod

- **psql** = klient, **PostgreSQL server** = server. Dva různé programy.
- Vstupní bod je přes **port 5432** (ne soubor, ne ikona) — viz E18, ops-layer.
- `docker exec -it mcp-jobs-postgres psql -U mcpjobs -d mcpjobs` = vstup do klienta uvnitř kontejneru.

---

## 2. Epistemika — jak *poznáš*, že máš pravdu (8 pastí)

Epistemika = jak ověřuješ tvrzení o datech. SQL se na pravdu ptát umí, ale i klame.

| # | Past | Pravidlo | Příklad z cvičení dedup |
|---|------|----------|--------------------------|
| 1 | **NULL** | porovnání s NULL je vždy `UNKNOWN` → používej `IS NULL` / `IS NOT NULL` / `COALESCE` | `matched` prázdné u orphan runu |
| 2 | **MVCC / snapshoty** | každý dotaz vidí "obrázek" z okamžiku začátku → po zápisu vždy znovu čti | po DELETE ověř `COUNT(*)` |
| 3 | **Intuice vs data** | neodsuzuj, měř — `COUNT(*)` je základní soud | 93 vs 93 url |
| 4 | **SELECT \*** | nikdy bez `LIMIT` — data převyšují intuici | průzkum šumu s `LIMIT 10` |
| 5 | **Plán vs realita** | tvoje představa o běhu dotazu = teorie; `EXPLAIN ANALYZE` = empirie | index na `profile` |
| 6 | **Integrity constraints** | FK/UNIQUE vymáhají pořadí mazání a dedup *za tebe* | `ads`↔`pipeline_runs` bez FK |
| 7 | **Transakce jako airbag** | ROLLBACK je jediný reverzní mechanismus pro DML | cvičný let: 93 → 62 → zpět 93 |
| 8 | **Metadata jako pravda** | `\d`, `information_schema`, `pg_catalog` — ne paměť | `\d ads` |

**Read-after-write:** po každé DML operaci znovu přečti a ověř. To je jediná jistota, že operace proběhla tak, jak sis představoval.

---

## 3. Unknown unknowns → known unknowns (7 konceptů)

Unknown unknowns = koncepty, které nevíš, že nevíš. Dokud je nepřejmenuješ na known unknowns, nemůžeš se je naučit.

| Koncept | Co řeší | Proč je fundament |
|---------|---------|-------------------|
| **MVCC** | Multi-Version Concurrency Control — jak Postgres izoluje souběžné čtení/zápis | proč DELETE neodstraní "duplicitu napříč profily" a proč čtení v transakci je konzistentní |
| **Isolation levels** | jak moc se transakce navzájem vidí (READ COMMITTED, REPEATABLE READ, SERIALIZABLE) | proč ROLLBACK vrátí "vše" a paralelní transakce se nevidí |
| **Indexy** | datová struktura pro rychlé vyhledání | proč `WHERE profile='default'` je rychlé i na velkých datech — a kdy není |
| **VACUUM / bloat** | MVCC zanechává mrtvé řádky; úklid | deletuješ, ale disk se neuvolní okamžitě |
| **WAL** | Write-Ahead Log — trvanlivost | jak COMMIT přežije pád stroje |
| **TOAST** | komprese velkých polí mimo hlavní tabulku | proč velké texty nezpomalí tabulku |
| **role / privileges** | kdo smí co (user vs superuser) | proč je `-U mcpjobs` a co by superuser mohl pokazit |

---

## 4. Kontext: dedup cvičení jako zhmotnění modelu

Reálný případ (ověřeno live psql 2026-08-18): **31 ads s `profile='default'`** napříč 5 query (udrzbar 16, elektrikar 5, spravce 5, truhlar 3, cnc_jobs 1, zahradnik 1) z runu 7 (config smazán).

**Pedagogický klíč:** *dedup v SQL není vždy jen DELETE duplicitních URL.* Někdy je to identifikace **redundantní podmnožiny** přes agregace, JOIN a subqueries.

| Nástroj | Role v dedup | Výsledek |
|---------|--------------|----------|
| `COUNT(DISTINCT url)` | ověření, že UNIQUE hlídá duplicity | 93 = 93, žádné duplicitní URL |
| `GROUP BY profile, query_name` | definice redundantní skupiny | default = 31 napříč 6 query |
| `HAVING COUNT(*) > 5` | filtrace skupin (ne řádků) | identifikuje šumové profily |
| self-JOIN `ads a JOIN ads b ON a.url=b.url` | hledání duplicit mezi profily | **0 řádků** = URL UNIQUE nedovolí totéž url pod dvěma profily; šum je v profilu/query, ne v url |
| `DELETE ... RETURNING` | bezpečné mazání s reportem | co přesně bylo smazáno |
| `BEGIN/ROLLBACK/COMMIT` | airbag | cvičný let (ROLLBACK) vs ostrý běh (COMMIT) |

**Kandidát na GT záznam:** schema NEMÁ foreign key mezi `ads` a `pipeline_runs` (run 7 je orphan). FK by vymáhalo pořadí mazání (nejdřív děti, pak rodič) samo — to je oprava do schématu, mimo toto cvičení.

---

## 5. Další krok (actionable)

1. **`\d ads`** — přečti si skutečné schema (sloupce, typy, constraints), ne paměť.
2. **`EXPLAIN ANALYZE`** na libovolném dotazu — srovnej plán s realitou (past č. 5).
3. Pokračovat adopční sekvencí: S5 = **JOIN** (cvičení 4 je základem), S6 = FK/normalizace.

---

## 6. Slovníček (7 termínů)

| Pojem | Význam |
|-------|--------|
| **MVCC** | Multi-Version Concurrency Control — souběžné transakce čtou konzistentní snapshot bez zamykání čtení |
| **Snapshot isolation** | každá transakce vidí data v okamžiku svého startu |
| **Isolation level** | míra vzájemné viditelnosti transakcí (READ COMMITTED je default PostgreSQL) |
| **VACUUM** | úklid mrtvých řádků, které MVCC zanechává |
| **WAL** | Write-Ahead Log — zápis změn do logu před commitem; základ durability |
| **TOAST** | komprese velkých polí mimo hlavní tabulku |
| **EXPLAIN ANALYZE** | skutečné provedení dotazu s plánem a měřenými časy — empirie výkonu |

---

*Dokument vytvořen: 2026-08-18 | Autor: outpost2026 | Verze: 1.0*
*Provenance: summary (konceptuální; dedup kontext ověřen live psql na MCP-Jobs DB — 93 ads, 7 runs)*
*Návaznost: IT_gramotnost_hranice_SQL_databazi (E18), SQL_ADOPCE_PLAN, sql_ontologie_mechanismy, postgresql_zakladni_prikazy*