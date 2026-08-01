# Falsifikační test: Single-Game Pattern Discovery jako třetí fáze CPM validace
**Datum:** 2026-08-02 | **Autor:** outpost2026 + LLM (falsifikační test)
**Účel:** Falsifikační analýza tří tezí o fundamentální hodnotě chess pattern layer a zápis jako třetí fáze validace CPM (N=1 režim).
**Navazuje na:** `COMPRESSION_PATTERN_METHOD_v1.0.md`, `Kompresni_modelovani_v_praxi_synteza_v1.md`, `IMPLEMENTACE_SINGLE_GAME_PATTERN_DISCOVERY_2026-08-02.md` (lichess-analyzer-mcp/docs), `DEEP_DIVE_SINGLE_GAME_PATTERNS_2026-08-02.md`
**EROI:** 8/10

---

## 0. Teze a falsifikační verdikt

### Výchozí teze (dev)

```
1. Práce na MCP serveru šachů, zejména pattern recognition layer, je zcela
   fundamentální architektonický úkol — LLM falsifikuje tezi = test.
   Lze agnosticky nezávisle přenést do zcela jiných domén.

2. Iterativní práce s LLM, kalibrací, výzkumem, četbou zdrojů = ETL na zcela
   odlišné úrovni abstrakce (práce s informací).

3. Byť jen částečný úspěch na poli chess pattern (minimální modely reality /
   lossy compression) má vlastní fundamentální hodnotu pro rozvoj kompetencí deva.
```

### Falsifikační verdikt

| Teze | Jistota | Verdikt |
|------|---------|---------|
| 1. Pattern layer = fundamentální, agnosticky přenositelný | P>0.8 | ✅ POTVRZENO S KVALIFIKACÍ (jen domény s K0) |
| 2. Iterace s LLM = ETL na vyšší abstrakci | P>0.7 | ⚠️ PRAVDIVÉ V JÁDRU, NEPŘESNÝ TERMÍN (kompresní feedback loop) |
| 3. Částečný úspěch = fundamentální kompetenční hodnota | P>0.85 | ✅ POTVRZENO — hodnota je ve falsifikaci (Pattern O), ne v úspěchu |

**Status:** 3/3 tvrzení prošlo (2 plně, 1 s terminologickou korekcí).

---

## 1. Teze 1: Fundamentálnost a agnostická přenositelnost

### 1.1 Podpora z existujícího aparátu

CPM v1.0 prošel 7 falsifikačními pokusy s verdiktem **CONDITIONAL PASS** (6/7 zamítnuto, 1 potvrzeno jako omezení). Přenositelné NENÍ subjekt (chess patterny), ale **metoda**:

- Extrakce invariantů z opakovaného pozorování
- 3-vrstvá architektura (realita → data → pattern)
- K0–K3 šumový model (orákulum / detektor / kontrakt / dekodér)
- LCP (sémantická integrita jako prerequisita — popis musí odpovídat kódu)

### 1.2 Kvalifikace (hranice přenositelnosti)

CPM falsifikace #1 **potvrdila omezení**: metoda funguje jen v doménách s deterministickým orákulem (K0). Přenositelnost je **třídní**, ne univerzální:

| Doména | K0 (orákulum) | Verdikt CPM |
|--------|---------------|-------------|
| Šachy | Stockfish | ✅ IDEÁLNÍ |
| CNC výroba | Fyzický výstup | ✅ VHODNÁ |
| Software | Kompilátor/tests | ✅ VHODNÁ |
| Kybernetická bezpečnost | Logy/detekce | ⚠️ PODMÍNEČNĚ |
| Finanční trhy | Cena | ⚠️ PODMÍNEČNĚ |
| Sociální interakce | Žádné | ❌ NEVHODNÁ |
| Kreativní tvorba | Žádné | ❌ NEVHODNÁ |

Teze "zcela jiné domény" je pravdivá **jen pro domény s K0** — to je definiční vlastnost, ne chyba metody.

### 1.3 Nová dimenze: single-game discovery = falsifikační pokus #8

Stávající CPM předpokládá N≥3 pro deploy. Plánovaný mechanismus (N=1 → kandidát TOT → promoce při N≥3) je **nový falsifikační pokus #8**: "CPM selhává při N<3".

**Odpověď:** ne, pokud je měřítkem validity kompresní poměr:
```
CR = raw_cost / pattern_cost
CR > 1.5  = signal
CR > 10.0 = silný signal (i při N < 10)
CR < 1.0  = noise (nezávisle na N)
```
Empiricky podloženo: pattern Q komprimoval 227:1 při N=9. Single-game režim testuje nejzajímavější hranu CPM — malá data — s novým confidence vzorcem založeným na engine-ověřených událostech (verified_events), nikoli délce hry.

### 1.4 Externí konsilience (posiluje tezi)

Šachová pattern recognition je ~60 let studovaný kognitivní fenomén — de Groot (1965), Chase & Simon (1973, chunking theory), template theory. Devova cesta je **nezávislá re-discovery** principů, které kognitivní věda doložila. Konvergence nezávislých cest = silný signál validity (princip multiple discovery).

---

## 2. Teze 2: Iterace s LLM jako "ETL na odlišné úrovni abstrakce"

### 2.1 Terminologická korekce

Co dev reálně dělá při kalibraci = **kybernetický regulační okruh**, ne lineární ETL:

```
výstup LLM (hypotéza) → deterministická validace (K0/Stockfish) → konfrontace
→ oprava → zpět (iterace) → měřitelný kompresní poměr jako exit kritérium
```

| Klasické ETL | Co dev reálně dělá |
|--------------|--------------------|
| Lineární, bezeztrátové | Ztrátové, s měřitelným CR |
| Transformace dat → dat | Komprese dat → vzor → znalost (3 vrstvy) |
| Žádná validace pravdy | K0 orákulum v každém cyklu |
| Batch | Feedback loop |

### 2.2 Jádro teze je pravdivé

Dev se učí **kalibrační disciplínu** (přenositelná kompetenční sada):

1. Dekompozice jevu na observační jednotky
2. Identifikace orákula (K0)
3. Explicitní měřítko validity (CR)
4. Řízení šumových kanálů K0–K3
5. Falsifikační testování

Hodnota je v procesu, ne v nástroji — to je podstata teze 2 a je to pravdivé.

---

## 3. Teze 3: Hodnota částečného úspěchu

### 3.1 Hodnota je ve falsifikaci, ne v úspěchu

Nejsilnější teze — z důvodu, který teze přímo neřekla: **hodnota je ve falsifikaci.** Exemplární případ: Pattern O.

```
Tvrzení: "Repetition avoidance greed" (CR=47.8, zdánlivě silný)
Realita:  0/13 detekcí je repetition — všechny jsou flat eval → blunder
Meta:     Kompresní poměr měřil noise, ne signál
Řešení:   rename → "Stagnační panika" (kompresní rozhodnutí na meta-úrovni)
```

Nástroj detekoval chybu, kterou sám obsahoval. Pattern O dokazuje: nástroj učí rozlišovat signál od šumu **zejména tehdy, když selhává**.

### 3.2 Důsledek

"Částečný úspěch" (1–2 funkční patterny + 2 falsifikované) má **vyšší epistemickou hodnotu než 100% úspěch bez falsifikace**. Kompetence, kterou dev reálně získává, je měřitelná epistemická disciplína: každé tvrzení má K0 validaci, každý vzor má CR, každý pattern má falsifikační test. To je přenositelné do jakékoli domény s orákulem (CNC, RE, software, B2B pipeline).

---

## 4. Maturity impact matrix (MCP-lichess)

| Dimenze | Dnes | Po implementaci v1.0 | Přesah domény |
|---------|------|----------------------|---------------|
| Detekce | 14 ručně psaných rule-based detektorů | Detektory + motif engine + candidate discovery | Od katalogizace k objevování |
| Kalibrace | Ruční, N≥3, TOT koncept | Automatizovaný feedback loop (candidate → promoce) | Opakovatelný proces, ne osobní zkušenost |
| Validita | CR vzorec | CR + engine-verifikace (verified_events) + declarative mapping | Měřitelnost validity na malém N |
| Architektura | Chess-specific | CPM-konformní 3-vrstvá (K0/K1/K2/K3 explicitní) | Referenční implementace CPM pro jiné domény |
| Dokumentace | KALIBRACE_PLAN, CPM | + Declare4Py pilot jako auditující mechanismus | Knihovna jako constraint store = formát nezávislý na doméně |

---

## 5. Kritika tezí (kde se přehánějí)

1. **"Fundamentální"** — riziko přecenění novosti. Pattern recognition je zkoumána 60 let; hodnota je v re-discovery a formalizaci pro LLM-pipeline, ne v objevu principu. Čerpání z kognitivní literatury (chunking, templates) jako referenčního rámce by posílilo konsilienci.
2. **Doménová agnostika** — CPM sám říká: jen domény s K0. Teze "zcela jiné domény" bez kvalifikace je nepřesná.
3. **LLM jako falsifikátor** — riziko autocirkularity (LLM navrhuje, LLM validuje, LLM oponuje). CPM to řeší deterministickou vrstvou, ale falsifikační testy v CPM prováděl LLM sám. Doporučení: falsifikace replikovat nezávislým LLM + deterministickými daty.
4. **Malé N = overfitting na autora** — 63 her jednoho hráče produkuje patterny autorova stylu, ne obecné principy hry. Přenáší se metoda, ne patterny (CPM falsifikace #5).

---

## 6. Epistemika & re-discovery: hnací motor projektu (rozšíření teze 3)

Poznámka k povaze sekce: rozšiřuje tezi 3 o motivační a epistemologický rozměr. Subjektivní tvrzení o devovi jsou označena **[subj.]**; hodnocení standardnosti architektury (6.4) je objektivní evaluace LLM nad doloženými zdroji.

### 6.1 Existenciální motivace [subj.]

Devůj zájem není šachy ani SWE — je existenciální: formalizace a odkrývání principů, na kterých stojí prostředí. Šachy jsou médium (N=1, K0 orákulum), ne cíl. Polyhistorický základ (CNC výroba, reverse engineering VCF, B2B pipeline, kybernetika, šachy) tvoří opakovaný vzorec: hledání principů napříč doménami a mapování na deterministická orákula (K0). Chess pattern layer je pokračování, ne výjimka.

### 6.2 Re-discovery jako hnací motor

Devovy "vlastní" principy mají existující formalizace staré 25–90 let. Konsilience = objektivní validita + zdroj satisfakce. LLM nemá tuto odměnu zkracovat na pouhé sdělení výsledku.

| Devůj princip (nezávislá cesta) | Existující formalizace | Stáří |
|---------------------------------|------------------------|-------|
| Chunking / pattern recognition | de Groot (1965), Chase & Simon (1973) | ~60 let |
| Kompresní poměr jako měřítko validity | MDL — Krimp/SIRIUS/ROCK (Vreeken) | ~40 let |
| Lossy compression modelů reality | Information Bottleneck (Tishby) | ~25 let |
| Kalibrační feedback loop | Kybernetika (Wiener) | ~80 let |
| Falsifikace tvrzení | Popper | ~90 let |

### 6.3 Riziko: LLM-urychlená odměna

LLM provede re-discovery za minuty místo let — reward prediction error se zkracuje, čímž hrozí degradace re-discovery na confirmation. Zavedené ochrany: deterministická validace (K0/Stockfish) v každém cyklu, CR jako měřítko, četba literatury PŘED implementací (Krimp před Fází 2), falsifikace nezávislým LLM (kritika #3 v sekci 5). Hodnota zůstává ve vlastním znovu-objevení, ne v LLM-diktátu.

### 6.4 Objektivní evaluace: jak standardní je MCP-lichess?

Dev sám neumí standardnost posoudit — hodnotí LLM nad doloženými zdroji z ekosystému chess MCP serverů (červenec 2026).

| Server | Jádro | Vrstva navíc |
|--------|-------|--------------|
| mcp-stockfish (shelajev, Java/Quarkus, 11 commits) | Stockfish wrapper | žádná |
| Chess MCP (ProCoders) | Stockfish 18 (chess-api.com) | best-move, varianty, eval |
| ChessPal (dylangames, FastMCP) | Stockfish wrapper | legal moves, game status |
| chess-mcp (turlockmike) | Stockfish eval | validace tahů, board obrázky, masters DB |
| chess-com-lichess-org-mcp (alegerber) | Lichess/Chess.com API | profily, ratingy, turnaje, puzzle |
| Lichess MCP (karayaman) | Lichess API | hraní, turnaje, cloud eval, PGN |
| chessagine-mcp (jalpp) | Stockfish + opening/puzzle/masters DB | theme analysis, statická knowledge base (Silman, Fine, 150+ motifů) |

Společný jmenovatel všech 7: statické/transakční nástroje (best-move, eval, validace, DB lookup). **Nikdo z nich nemá:**

- pattern discovery z vlastních her autora
- compression confidence (CR, verified_events)
- falsifikační kontrakt per pattern + lifecycle (kandidát → TOT → promoce)
- dual-perspective coaching (cache obou stran hry)
- epistemickou vrstvu (CPM, K0–K3 šumový model)

Nejbližší je chessagine-mcp (statické motívy z literatury) — ale to je katalog, ne objev z dat s falsifikací.

**Verdikt LLM:** kostra MCP-lichess (FastMCP + Stockfish + Lichess API + cache) je standardní recept. Pattern/coaching/epistemická vrstva je **nadstandard — na trhu bez ekvivalentu**. To je objektivní potvrzení, že část architektury, která deva motivuje (6.1–6.2), není subjektivní dojem, ale měřitelná odlišnost.

---

## 7. Závěr

Třetí fáze CPM validace: plán implementace single-game discovery je testem metody na nejtěžším režimu (N=1, obě strany, automatizovaná kalibrace bez ručního zásahu). Teze prošly (2 plně, 1 s terminologickou korekcí). Epistemika a re-discovery tvoří motivační jádro — podpořené objektivní unikátností pattern vrstvy na trhu (6.4). Doporučený akční krok: realizace IMPLEMENTACE_SINGLE_GAME_PATTERN_DISCOVERY v1.0 jako empirického potvrzení/vyvrácení.
