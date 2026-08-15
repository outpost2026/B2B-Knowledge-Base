# Adopční metodologie SWE/IT — optimální stack metod pro 2026 Q3+
**Datum:** 2026-08-15 | **Autor:** outpost2026
**Účel:** Kanonická formalizace adopční metodologie pro rozvoj SWE/IT kompetencí — vychází z kritické analýzy SWE_GLOSSARY a transfer-learning matice SKILL_GAPS. Živý dokument.
**Typ:** metodika | **Doména:** skill acquisition, kognitivní věda, SWE edukace | **EROI:** 9/10
**Návaznost:** SWE_GLOSSARY_zive_v1.md, SKILL_GAPS_ROZBOR_Q3_2026_v2.md, Epistemicky_kotvici_ramec_a_operacni_modus.md, eroi_chronologicky_plan_s_metodikou.md, brain_geometric_processor_summary_v2.1.md, chess_mcp_strategy_v1.md

---

## 1. Východisko: proč tato metodika vznikla

Kritická analýza SWE_GLOSSARY odhalila paradox: **glossary definuje termíny, ale nepředává porozumění.** Terminologie je index, ne učební metoda. Dokument (571 řádků, 19 sekcí) je vynikající referenční nástroj, ale sám o sobě vede k "pasivní znalosti" — víš co je Singleton, ale nevíš kdy ho použít a kdy NE.

Tato metodika definuje **jak** se má terminologie + dovednosti adopotovat v éře LLM. Vychází z empiricky podložených metod (Ebbinghaus, spaced repetition, Feynman, Novak) a z autorova transfer-learning profilu (tacitní expert CNC/CAM → SWE).

**Anti-blackbox paradigma je jádro:** cíl není "umět opsat definici", ale "umět reprodukovat logiku a rozhodovat architektonicky".

---

## 2. Optimální stack metod (60/20/10/10)

| Podíl | Metoda | Role | Empirická báze |
|:-----:|--------|------|----------------|
| **60 %** | Project-Based Learning (PBL) | Primární — získávání dovedností řešením reálných problémů | Dewey, Kolb (experiential learning); autor má 600+ commitů, 14+ repů — praxe = hlavní zdroj |
| **20 %** | Feynman Technique → SWE_GLOSSARY | Doplňková — vysvětli vlastními slovy, zapiš do glossary | Feynman; struktura CO/PROČ/JAK/EFEKT = aplikace Feynman |
| **10 %** | Spaced Repetition (SRS) | Udržovací — prevence zapomínání terminologie | Ebbinghaus křivka zapomínání (70 % ztráta za 24 h); autorova vlastní epistemická báze: "krásné zapomínání" a sémantická eroze (brain_geometric_processor); implementace: FSRS engine (py-fsrs, viz chess_mcp_strategy_v1 Phase 5) |
| **10 %** | Concept Mapping | Vizualizace — mapy vztahů mezi pojmy | Novak (concept maps) — retence +20-30 % oproti pasivnímu čtení |

### 2.1 Proč právě tento poměr

1. **PBL dominuje (60 %)** — dovednosti se NEučí z dokumentů, ale z řešení problémů. LLM zrychluje implementaci, ale architektonické myšlení vzniká jen z vlastní zkušenosti. Autorův kontext (VCF parser, MCP servery) to potvrzuje: nejhlubší porozumění vzniklo při debugování reálných bugů (race condition, zombie thread).
2. **Feynman → Glossary (20 %)** — glossary je Feynman aplikace: "vysvětli race condition jako bys vysvětloval neprogramátorovi". Psaní vlastními slovy vynucuje pochopení. Bez zápisu do glossary je porozumění prchavé.
3. **SRS (10 %)** — terminologie se zapomíná. Ebbinghaus: bez opakování 70 % ztráta za 24 h. SRS s optimálními intervaly (1→3→7→14 dní) udrží 90 %+ s minimem času. LLM generuje flashcards z glossary. **Epistemická báze (autorova vlastní):** brain_geometric_processor — mozek je krajina vektorů; dráhy, které nejsou pravidelně aktivovány, slábnou (sémantická eroze, retroaktivní interference). TOT stav (na jazyku) = plochý gradient v cílovém bodě — "znám pojem, ale nevybavím si ho". SRS = pravidelná reaktivace drah (konsolidace, replay) = investice do údržby krajiny. **Implementace:** FSRS engine (py-fsrs) je plánovaný v chess_mcp_strategy_v1 (Phase 5) — stejný engine se použije pro glossary flashcards (1 balíček, 2 domény: šachy + SWE terminologie).
4. **Concept Mapping (10 %)** — glossary popisuje termíny izolovaně. Mapa vztahů (race condition → lock → mutex → deadlock → timeout) zvyšuje retenci a ukazuje ontologii.

---

## 3. Kognitivní mezera, kterou každá metoda adresuje

| Mezera | Metoda | Mechanism |
|--------|--------|-----------|
| "Nevím, co nevím" (unknown unknowns) | PBL + koncept mapy | Narazíš na problém → objevíš existenci pojmu → zmapuješ vztahy |
| "Znám termín, nechápu logiku" | Feynman → Glossary | Psaní vlastními slovy odhalí mezery v porozumění |
| "Chápal jsem včera, zapomněl dnes" | SRS | Opakování v optimálních intervalech; mozek = krajina vektorů (brain_geometric_processor) — neaktivované dráhy slábnou (sémantická eroze) |
| "Na jazyku, ale nevybavím" (TOT stav) | SRS | Plochý gradient v cílovém bodě krajiny — reaktivace vytvoří strmý atraktor (viz brain_geometric_processor) |
| "Umím pojmy, neumím rozhodovat" | PBL (architektonické rozhodování) | Reálné trade-offy (Singleton vs statická třída) se učí jen praxí |
| "Slyším pojem v komunikaci, nerozumím" | Glossary jako referenční index | Rychlé dohledání v živém dokumentu |

---

## 4. Aplikace na SKILL_GAPS (6 gapů, Q3+ 2026)

### 4.1 Pravidlo nasazení metod per gap

| Gap | Metoda primární | Metoda doplňková | Proč |
|-----|-----------------|------------------|------|
| ❶ TypeScript+Next.js+monorepo | PBL (PoC: dashboard z output/*.json) | Feynman→Glossary | Nejvyšší EROI (9/10) — učit tvorbou reálného artefaktu |
| ❷ PostgreSQL | PBL (schema.sql + 1 reálný run do DB) | Concept Mapping (vztahy tabulek) | DB = vztahy → koncept mapy jsou přirozené |
| ❸ DevOps (Docker, cron, monitoring) | PBL (cron + healthchecks + CI) | Feynman→Glossary | Automatizace = praxe; terminologie → glossary |
| ❹ AZ-900 | SRS (cvičné testy + flashcards) | PBL (1 Azure PoC) | Certifikace = paměťová zkouška → SRS je ideální |
| ❺ PLC Basics | PBL (TIA Portal + Modbus PoC) | Concept Mapping | Průmyslová doména = fyzikální vztahy |
| ❻ Kubernetes | PBL (minikube + MCP deployment) | Concept Mapping | Orchestrace = vztahy komponent |

### 4.2 Sekvenční pravidlo

1. **Začni PBL** — vždy s reálným artefaktem (PoC, test, deployment). Teorie až potřeba.
2. **Během PBL zaznamenávej** nové termíny do glossary (Feynman).
3. **Po PBL generuj flashcards** z nových glossary termínů → SRS.
4. **Čtvrtletně reviduj** koncept mapy napříč gapy (integrace, ne izolace).

---

## 5. Integrace s existujícími artefakty

| Artefakt | Role v metodice |
|----------|-----------------|
| `SWE_GLOSSARY_zive_v1.md` | Feynman výstup (20 %) + referenční index + SRS zdroj |
| `SKILL_GAPS_ROZBOR_Q3_2026_v2.md` | Cílový rozbor gapů + trajektorie (CO učit) |
| `Epistemicky_kotvici_ramec_a_operacni_modus.md` | Kognitivní mantinely (komprese vs akumulace, anti-rabbit-hole) |
| `eroi_chronologicky_plan_s_metodikou.md` | Metodické kostry per gap (KROK 1-3: základy → nástroj → PoC) — implementační detail PBL |
| `brain_geometric_processor_summary_v2.1.md` | Epistemická báze SRS (sémantická eroze, TOT, reaktivace drah) |
| `chess_mcp_strategy_v1.md` | FSRS engine (py-fsrs, Phase 5) — infrastruktura SRS, sdílená mezi šachy a glossary |
| `MCP_GROUND_TRUTH_postmortem` | Zdroje reálných případů (termíny z GT → glossary s kontextem) |

**Guardrail (z Epistemického rámce):** Složitost je parazit. Adopční metodika nesmí sklouznout do "akumulace termínů" — glossary roste jen o termíny z REÁLNÉHO kontextu, ne o akademický balast. Kvalita > kvantita.

---

## 6. Měřitelné metriky úspěchu

| Metrika | Cílová hodnota | Měření |
|---------|----------------|--------|
| Glossary: poměr kontextovaných termínů | >80 % (každý termín má reálný kontext) | Audit sekcí |
| SRS: denní opakování | 10 min/den, 5 dní/týden | FSRS engine stats (py-fsrs — chess_mcp Phase 5, sdílený balíček) |
| PBL: PoC artefakt per gap | 1 reálný artefakt per gap do 90 dní | GitHub audit |
| Transfer: rychlost adopce nové domény | První funkční artefakt < 14 dní od startu gapu | Session logy |
| B2B signál: rozhovor v SWE terminologii | Schopnost mluvit 10 min o gapu bez "ehm" | Sebehodnocení / mock interview |

---

## 7. Rizika a mitigace

| Riziko | Pravděpodobnost | Dopad | Mitigace |
|--------|:---------------:|:-----:|----------|
| **Glossary > praxe** (vibecoding s glosářem) | Střední | Vysoký | Pravidlo 60/20 — glossary nikdy nepřesáhne 20 % času |
| **Akumulace termínů bez kontextu** (rabbit hole) | Vysoká | Střední | Guardrail z Epistemického rámce: jen kontextované termíny |
| **SRS opuštěno po 2 týdnech** | Vysoká | Střední | Autonomie: 10 min/den fixní, LLM generuje karty |
| **PBL přepisování LLM kódu bez pochopení** | Střední | Vysoký | Anti-blackbox: každý LLM výstup projít a vysvětlit vlastními slovy (Feynman) |
| **Koncept mapy = otrava** | Střední | Nízký | Mermaid diagramy generované LLM, ne ruční kreslení |

---

## 8. Trajektorie (Q3+ 2026) — časová osa s metodami

```
Q3 (TÝDEN 1-6): Gap ❶ TS+Next.js + ❷ PostgreSQL
  └── PBL: PoC dashboard (output/*.json → Next.js) + schema.sql do DB (60 %)
  └── Feynman: nové termíny (Next.js, monorepo, SQL, JSONB...) → glossary (20 %)
  └── SRS: flashcards z nových termínů (10 %)
  └── Concept map: vztah web ↔ DB ↔ ETL (10 %)

Q3 (TÝDEN 7-8): Gap ❸ DevOps + ❹ AZ-900
  └── PBL: cron + healthchecks + GitHub Actions + 1 Azure PoC (60 %)
  └── SRS: AZ-900 cvičné testy dominují (paměťová doména)

Q4: Gap ❺ PLC (40-60 h) + ❻ K8s (volitelné)
  └── PBL: TIA Portal + Modbus PoC (60 %)
  └── Concept map: PLC ↔ CNC transfer (10 %)

Průběžně: SWE_GLOSSARY roste živě; každý měsíc 1 revize koncept map napříč gapy
```

---

## 9. Finální principy (7 pravidel adopce)

1. **Praxe > dokumentace.** Termín adoptuješ, když ho POUŽIJEŠ, ne když ho přečteš.
2. **Vysvětli vlastními slovy.** Pokud nemůžeš vysvětlit jednoduše, nerozumíš (Feynman).
3. **Opakuj, nebo zapomeň.** Bez SRS je 70 % terminologie pryč do 24 h (Ebbinghaus) — neaktivované dráhy v krajině slábnou (sémantická eroze, brain_geometric_processor). SRS = údržba krajiny. Implementace: FSRS engine (py-fsrs).
4. **Mapuj vztahy.** Izolovaný termín je mrtvý termín; ontologie = vztahy.
5. **Anti-blackbox.** Každý LLM výstup projít a pochopit — nikdy nezkopírovat naslepo.
6. **Kvalita > kvantita.** 30 kontextovaných termínů > 300 načtených definic.
7. **Živý systém.** Glossary, koncept mapy, flashcards — vše průběžně aktualizovat, ne jednorázově.

---

## Metadata

- **Tags:** `#metodika`, `#skill-acquisition`, `#pbl`, `#feynman`, `#srs`, `#concept-mapping`, `#learning`, `#adopce`, `#swe`
- **EROI:** 9/10 (formalizace metodiky; náklad = 1× zápis, benefit = trvalá adopce kompetencí → cíl: nezávislý SWE/B2B AI augmented inženýr)
- **Živý dokument:** aktualizovat při změně gapů, metod nebo zjištění z praxe.