# Hranice IT gramotnosti: SQL databáze jako epistemický fenomén

**Datum:** 2026-08-15 | **Autor:** outpost2026
**Účel:** Formalizovat tezi, že práce s SQL databází přesahuje standardní IT gramotnost, a rozlišit, CO přesně přesahuje — query-layer (přenositelná z Excelu) vs ops-layer (nová ontologie bez vstupního bodu)
**Typ:** esej / kognitivní rámec | **Doména:** epistemika, kognitivní ontologie nástrojů, skill acquisition | **EROI:** 8/10
**Návaznost:** `01_METODIKY/04_skill_acquisition/SKILL_GAPS_ROZBOR_Q3_2026_v2.md` (gapy ❷ PostgreSQL, ❸ DevOps), `01_METODIKY/04_skill_acquisition/ADOPCNI_METODOLOGIE_2026_v1.md` (60/20/10/10), `docs/edukace_db_prvni_kontakt_2026-08-15.md` (MCP-Jobs, praktický výstup)
**Provenance:** source-read (live docker inspect mcp-jobs-postgres, psql dotazy na reálných datech ETL běhů, docker volume inspect) + autoreflexe autora (30 min první DB v kontejneru)

---

## 1. Teze a verifikace

> **Teze:** Práce s SQL databází přesahuje standardní IT gramotnost, která se očekává od uchazečů o práci s požadavkem "znalost práce s PC". Práci s SQL DB nezvládá většina gaussovské křivky IT gramotné populace.

Verifikace s P-úrovněmi (pravděpodobnostní jistota):

| Tvzení | Verdikt | Jistota |
|--------|---------|:-------:|
| "Práci s SQL DB nezvládá většina uživatelsky IT gramotné populace" | PRAVDIVÉ | P > 0.9 |
| "Toto přesahuje standardní IT gramotnost" | PRAVDIVÉ, ale vyžaduje rozlišení vrstev | P > 0.8 |
| "Požadavek 'znalost práce s PC' ≠ SQL" | PRAVDIVÉ | P > 0.9 |
| "Autor (IT znalý) je ztracen i s 30 min zkušenosti" | PRAVDIVÉ — diagnostický signál, ne indictement | P > 0.95 |

**Klíčové zpřesnění:** teze je pravdivá, ale konflátuje dvě odlišné věci. Rozlišení je jádrem tohoto artefaktu.

---

## 2. Jádrový model: dvě vrstvy

```
┌─────────────────────────────────────────────────────────────┐
│  SQL QUERY-LAYER  (SELECT/FROM/WHERE)                       │
│  → MAPOVATELNÁ na Excel (tacitní znalost)                   │
│  → transfer, ne nová ontologie                              │
├─────────────────────────────────────────────────────────────┤
│  OPS-LAYER  (Docker, kontejner, port 5432, volume, psql)    │
│  → NOVÁ ONTOLOGIE: žádný soubor, žádná ikona                │
│  → přesahuje standardní IT gramotnost                       │
└─────────────────────────────────────────────────────────────┘
```

30minutová ztráta autora **nebyla v SQL**. Byla v ops-layeru. To je rozdíl mezi "naučím se nový vzorec v Excelu" a "zjistím, že Excel nemá ikonu ani soubor".

---

## 3. Ontologický šok: soubor vs server

Excel a kontejnerová databáze se liší v samotné **ontologii vstupního bodu**:

| Otázka nováčka | Excel | Kontejnerová DB |
|----------------|-------|-----------------|
| "Kde je soubor?" | `.xls` na disku, dvojklik | **Neexistuje žádný soubor** |
| "Jaký program spustím?" | Ikona Excelu (instalován) | **Žádný** — psql je uvnitř kontejneru |
| "Kde píšu příkazy?" | Do buněk | Do konzole, přes `docker exec` |
| "Kam se ukládají data?" | Do souboru | Do volume uvnitř Docker infrastruktury |

**Ontologický šok** = stav, kdy uživatel hledá vstupní bod pro entitu, která ho nemá v jeho dosavadní ontologii. Excel má ikonu a soubor — kontejnerová DB nemá ani jedno. Standardní IT gramotná populace nikdy nepřekonala krok "najdi vstupní bod", a proto nikdy nevstoupí do query-layeru.

Důsledek: **operativní mapa je prekurzorem jazyka.** Dokud uživatel nenajde dveře, nemůže se naučit, co je za nimi.

---

## 4. Gaussovská křivka rozlišená

Teze konflátuje dvě populace:

| Populace | Zvládá SQL? | Proč |
|----------|-------------|------|
| **Uživatelská IT gramotnost** (kancelář, Excel, Word, web) | Ne (majorita křivky) | SQL nikdy nebyl součást "práce s PC" |
| **Profesionální IT** (dev, SWE) | Ano (baseline) | SQL je jádro stacku, gauss střed to umí |

**Pozice autora:** tacitně patří do populace 1 (Excel), profesně míří do populace 2 (systémový integrátor, expert Python). Jeho gap je **transferový, ne inteligenční** — a to je trénovatelné.

Gaussovská křivka tedy neplatí jednotně: to, co křivka "IT gramotnosti" neumí, je **ops-layer**. Query-layer je dosažitelný pro každého, kdo tacitně ovládá tabulkový procesor.

---

## 5. Diagnostická hodnota 30-minutové ztráty

Pocit ztráty po 30 min běhu první DB je **empirický vstup**, ne selhání. Přesně vymezuje rozdělení:

| Co ztrácelo | Vrstva | Gap dle SKILL_GAPS |
|-------------|--------|--------------------|
| "Kde je soubor / program / data?" | ops-layer (Docker, port, volume) | ❸ DevOps |
| "Jak se připojím, jak se dotazuji?" | query-layer (psql, SQL) | ❷ PostgreSQL |

To potvrzuje SKILL_GAPS: ❷ a ❸ jsou **dva oddělené gapy**, ne jeden. Křivka učení DB = křivka ops-layeru (nová ontologie) + křivka query-layeru (transfer z Excelu). První je strmá a neznámá, druhá je mělká pro toho, kdo zná Excel.

Vazba na adopční metodiku (60/20/10/10): PBL je primární pro ops-layer (řešit reálný problém = najít vstupní bod), Feynman→Glossary pro query-layer terminologii, SRS pro udržení, concept mapping pro vztahy tabulek.

---

## 6. Přenosový model Excel → SQL

Tacitní znalost Excelu mapovaná na SQL — důkaz, že query-layer je transfer, ne nová doména:

| Tacitní znalost Excelu | SQL ekvivalent |
|------------------------|----------------|
| Otevřít soubor | Otevřít konzoli (psql) |
| Vybrat list | `FROM ads` |
| Vybrat sloupce | `SELECT title, company` |
| Auto filtr | `WHERE company = 'Firma'` |
| Ctrl+F | `WHERE title ILIKE '%python%'` |
| Řazení | `ORDER BY` |
| Počet | `COUNT(*)` |
| Kontingenční tabulka | `GROUP BY` |
| Uložit (Ctrl+S) | Automatické (DB ukládá sama) |

Závěr: kdo tacitně umí Excel, má 80 % query-layeru kognitivně předpřipraveno. Bariéra je čistě v ops-layeru.

---

## 7. Falsifikace

Teze je falzifikovatelná — to je její epistemická hodnota:

1. **Kvantitativně:** pokud by data ukázala, že majorita populace s "znalostí práce s PC" skutečně samostatně otevře kontejnerovou DB a dotáže se, teze padá. Očekávaný výsledek: opak.
2. **Mechanisticky:** pokud by vstupní bod DB existoval v uživatelské ontologii (ikona + soubor, jako Excel), ontologický šok mizí a teze se redukuje na "naučit se nový nástroj". To je ověřitelné myšlenkovým experimentem i praxí.
3. **Progresivně:** pokud by autor po osvojení ops-layeru zvládl query-layer bez výuky SQL (čistý transfer z Excelu), potvrzuje se model dvou vrstev. Toto je testovatelné v rámci adopce gapů ❷+❸.

---

## 8. Praktický výstup

Artefakt vznikl souběžně s `docs/edukace_db_prvni_kontakt_2026-08-15.md` (MCP-Jobs), který ops-layer převádí na "ikonu" (`scripts/db.ps1`) a query-layer na překladovou tabulku Excel→SQL. Edukace je **implementace** tohoto modelu; tento artefakt je jeho **teoretickým zdůvodněním**.

---

## 9. Slovníček

| Pojem | Význam |
|-------|--------|
| **Query-layer** | Vrstva dotazování (SQL) — přenositelná, transfer z Excelu |
| **Ops-layer** | Provozní vrstva (kontejner, port, volume) — nová ontologie |
| **Ontologický šok** | Neschopnost najít vstupní bod pro entitu mimo dosavadní ontologii |
| **Kontejner** | Izolovaný běžící program (databázový server) |
| **Volume** | Trvalé úložiště dat uvnitř Dockeru |
| **Port 5432** | Adresa, kde databáze poslouchá |
| **Transfer** | Přenos dovednosti z jedné domény do jiné (Excel → SQL) |

---

*Dokument vytvořen: 2026-08-15 | Autor: outpost2026 | Verze: 1.0*
*Provenance: source-read (docker inspect, docker volume inspect, live psql na reálných ETL datech) + autoreflexe autora*
*Návaznost: SKILL_GAPS_ROZBOR_Q3_2026_v2.md, ADOPCNI_METODOLOGIE_2026_v1.md, edukace_db_prvni_kontakt_2026-08-15.md*