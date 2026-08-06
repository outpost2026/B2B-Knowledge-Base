# R&D Evoluce Portfolia — Bod 0 do současného stavu

**Autor:** Ondřej Soušek
**Datum:** 2026-08-06
**Verze:** 2.0 (aktualizace v1.0 z 2026-07-03)
**Rozsah:** 2026-03-24 → 2026-08-06 (135 dní)
**Celkem commitů:** ~600+ napříč 14+ repozitáři
**Provenance:** Live GitHub API audit (2026-08-06), ověřeno proti skutečnému stavu repozitářů
**Struktura:** 6 fází, každá s definovaným triggerem, výstupem a kognitivním patternem


## Fáze 0 — Pre-GitHub: Tacitní baseline (před březen 2026)

### Výchozí bod

Autor vstupuje do GitHub arény nikoli jako "junior developer začínající s Hello World", ale jako **tacitní expert** se zkušeností v CNC výrobě, CAM workflow a provozní automatizaci. Klíčová charakteristika: znalosti existují, ale nejsou externalizované — nejsou v kódu, nejsou v git historii, nejsou formalizované.

### Co autor uměl před prvním commitem (rekonstrukce z dokumentace)

| Dovednost | Úroveň | Způsob nabytí |
| - | - | - |
| CNC obsluha a programování | Produkční | Praxe u vodního paprsku, oscilačního nože |
| CAM workflow (VCutWorks, LightBurn) | Produkční | Každodenní provoz |
| Ruida VCF formát (mentální model) | Tacitní expert | Intuitivní porozumění z provozu |
| DXF formát a ACI barvy | Provozní | Práce s grafickými předlohami |
| Python základy | Samouk | Vlastní RPA a scraping scripty |
| GCP Cloud | Experimentální | Auto-bootstrapping: Python skript vydělal 2 000 Kč → Dell server |


### Trigger pro vstup do GitHubu

Autor narazil na **limitaci tacitního režimu**: LLM model (Gemini) mu přepisoval instrukce a obsah, behaviorální nekonzistence modelů ho frustrovala. Potřeboval:

1. Externalizovat svou metodiku práce s LLM
2. Zdokumentovat případy selhání modelů
3. Vytvořit opakovatelný framework

První commit nebyl "Hello World" — byla to **kazuistika selhání AI modelu** (kazuistiky\_llm\_sprint, 24. 3. 2026).


## Fáze 1 — Epistemická explorace (24. 3. – 3. 4. 2026, 10 dní)

### Charakteristika

Dominantně **dokumentační fáze**. 93 % obsahu tvoří markdown, 7 % Python kód. Autor nebuduje software — buduje **kognitivní framework** pro práci s LLM.

| Repo | Datum založení | Commitů | Charakter |
| - | - | - | - |
| `rag_indexer` | 24. 3. 2026 | 15 | RAG preprocessing prototyp |
| `kazuistiky_llm_sprint` | 24. 3. 2026 | 128 | Metodologie, case studies, manifesty |
| `cad2llm` | 31. 3. 2026 | 17 | SketchUp → JSON deterministic parser |
| `outpost_security_perimeter` | 1. 4. 2026 | 20 | IoT koncept (ESP32, dokumentace) |
| `outpost2026_profile` | 1. 4. 2026 | 45 | Profilový README |


### Klíčové události

1. **První commit vůbec** (24. 3., rag\_indexer): `universal_indexer_v7.py` — preprocessing nestrukturovaných dat pro RAG.

2. **Case study: Gemini přepisuje instrukce** (25. 3.): Autor dokumentuje, jak Gemini model modifikuje uživatelský prompt. **Zakladatelský moment** celé epistemiky.

3. **Metodika práce s LLM** (26. 3.): Vzniká `metodika_prace_s_LLM.md` — systematický rámec pro agentní workflow.

4. **Self-bootstrapping case** (2. 4.): Dokumentace příběhu "Python RPA → Dell server za 2 000 Kč".

5. **cad2llm** (31. 3.): Deterministický parser SketchUp→JSON s 4×4 maticemi. Princ "0 % halucinací".

### Kognitivní pattern Fáze 1

```
Frustrace z AI → Dokumentace selhání → Formalizace metodiky →
Aplikace na reálný problém (CAD parser, IoT koncept)
```


## Fáze 2 — Reverzní inženýrství a VCF parser (7. 6. – 11. 6. 2026, 4 dny)

### Trigger

Po 65denní pauze (3. 4. → 7. 6.) se autor vrací s konkrétním cílem: **zformalizovat tacitní znalost VCF formátu do kódu**.

### Exploze aktivity

| Repo | Založeno | Commitů | Hustota |
| - | - | - | - |
| `dxf_integrace` | 7. 6. 2026 | 48 | 48 commitů za 24 dní |
| `vcf_integrace` | 9. 6. 2026 | 15 | Celý RE backlog v1-v20 |
| `web_integrace_systeq` | 10. 6. 2026 | 75 | Web + Three.js |
| `vcf_parser_b2b` | 11. 6. 2026 | 73 | B2B produkt |


### Klíčové události

1. **dxf_integrace: První produkční kód** (7. 6.): DXF Geometry Indexer V2.2.0. 2 259 LOC.

2. **P0-P2 fixy během jediného dne** (7. 6.): nondeterminismu, geometry kritické fixy, ACI color priority.

3. **Semantic embedding dashboard** (8. 6.): Streamlit UI s drag-drop DXF.

4. **ACI Color Blindness crisis** (8. 6.): LightBurn používá jinou ACI paletu než AutoCAD. Euklidovská RGB interpolace.

5. **VCF parser backlog v1-v20** (9. 6.): 22 verzí parseru, 29 dní RE práce, 99.98% přesnost.

6. **Architektonická chyba: god class** (9. 6.): `RuidaVcfEngineV20` — 19k LOC monolit. Autor archivuje a refaktoruje.

### Kognitivní pattern Fáze 2

```
Tacitní znalost → Externalizace do kódu → Debugování →
Rozpoznání technického dluhu → Rozhodnutí refaktorovat
```


## Fáze 3 — B2B produktizace a kvalita (11. 6. – 28. 6. 2026, 17 dní)

### Trigger

Autor zakládá `vcf_parser_b2b` jako **produktový fork** — oddělený od R&D repa. **Z výzkumníka se stává dodavatel.**

### Exploze systematického testování

| Iterace | Datum | Obsah |
| - | - | - |
| It0 (HYGIENE) | 11. 6. | Structured logging, fix bare excepts |
| It1 (TESTS) | 11. 6. | Golden master regression + coverage |
| It2 (DEDUP) | 11. 6. | Extrakce modulů z god class |
| v21-v30 | 11.-16. 6. | 10 iterací, 45 testů, SNR kalibrace |


### Klíčové události

1. **Golden master metodologie** (11. 6.): Baseline JSON diff — místo unit testů.

2. **DEFECT_CATALOG V1** (14. 6.): Ontologická báze 20 detekovatelných výrobních chyb.

3. **SNR kalibrace** (16. 6.): Poměr signál-šum pro geometrickou analýzu.

4. **GCP deployment** (15. 6.): Streamlit app na Cloud Run. 6 deployů během jediného dne.

5. **B2B pricing a komunikace**: 70 000 Kč za Phase 1. Executive summary v2.1 odeslána.

### Kognitivní pattern Fáze 3

```
Produkt → Kvalita → Detekce šumu → SNR kalibrace →
Systematizace → B2B komunikace
```


## Fáze 4 — VCF kompilátor a cross-repo architektura (27. 6. – 2. 7. 2026, 5 dní)

### Trigger

Pokud parser umí číst VCF, proč neumí psát? Autor zakládá `Vcf-compiler` — zpětný proces: DXF → VCF.

### Intenzita RE výzkumu

38 commitů za 5 dní. Každý commit je experiment.

#### Evoluce writeru (den po dni)

| Den | Objev | Status |
| - | - | - |
| 27. 6. 08:27 | Initial VcfWriter implementation | Funkční, nevalidní |
| 27. 6. 17:16 | Geometry encoding — native header template bytes | Breakthrough |
| 29. 6. 12:28 | **3 root causes fixed** (trailer, element\_count@92, direction@104) | Writer OK |
| 30. 6. 14:20 | Least-squares circle fit | Matematický upgrade |


### Klíčové objevy

1. **Paradox tolerance**: Syntetická VCF jsou validní pro vlastní parser, ale invalidní pro VCutWorks GUI. **Autorův parser je lepší než nástroj, který reverse-engineeruje.**

2. **RE tooling** (30. 6.): 5 nových RE analýz nástrojů.

3. **Cross-repo dependency**: `compile_dxf()` volá `dxf_integrace.index_dxf()`. První závislost mezi repy.

4. **ACI Color Service** (2. 7.): `vcf_color_service` — pip balíček jako jediný zdroj pravdy pro ACI barvy.

### Kognitivní pattern Fáze 4

```
Paradox → Hypotéza → Experiment → Validace →
Systematizace do nástrojů → Architektonické uvědomění
```


## Fáze 5 — CI/CD a infrastruktura (1. 7. – 3. 7. 2026, 3 dny)

### Trigger

Po 3 měsících vývoje má autor 5 aktivních Python repozitářů s 0 CI/CD. Rozhodnutí: implementovat Tier 1 pipeline přes celé portfolio.

### Implementace

| Komponenta | Pokrytí |
| - | - |
| CI matrix | 3.10/3.11/3.12 — všechna aktivní repa |
| Nightly cron | 6:00 UTC — všechna aktivní repa |
| CodeQL | Security scanning — všechna aktivní repa |
| Dependabot | Dependency monitoring — všechna aktivní repa |
| workflow\_dispatch | Manuální trigger — všechna aktivní repa |
| Cross-repo dispatch | dxf\_integrace → Vcf-compiler |
| Badge | Pytest badge na main — všechna aktivní repa |

### Edu artifact

Vzniká `CI_GitHub_Actions_imerzni_edu_v1.md` — imerzní výklad CO/PROČ/JAK/EROI.

### Archivační rozhodnutí

`vcf_integrace` → **LEGACY** (god class, 0 testů).

### Kognitivní pattern Fáze 5

```
Detekce mezery (chybí CI/CD) → Transfer learning (co/proč/jak) →
Implementace napříč portfoliem → Edu artifact →
Systematická údržba
```


## Fáze 6 — MCP ekosystém a agentic workflow (7. 7. – 6. 8. 2026, 30 dní)

### Trigger

Autor má lokální MCP server (mcp-local-server) pro CNC nástroje. Rozhodnutí: **zpublishovat MCP servery jako veřejné produkty** a demonstrovat schopnost stavět agentic tooling.

### Exploze MCP ekosystému

| Server | Založeno | Commits | Charakter |
| - | - | - | - |
| `linkedin-mcp-custom` | ~7. 7. 2026 | 403 | LinkedIn scraper s EROI scoringem |
| `lichess-mcp-analyzer` | ~18. 7. 2026 | ~50+ | Chess analytics MCP server |
| `MCP-Jobs` | ~13. 7. 2026 | ~10+ | MCP pro CZ job portály (jobs.cz, prace.cz, bazos.cz) |

### Klíčové události

1. **linkedin-mcp-custom** (7. 7.): MCP server pro LinkedIn saved jobs scraping + EROI scoring. 403 commits — druhý nejaktivnější repo. Tento nástroj je přímým důkazem schopnosti stavět agentic tooling.

2. **MCP-Jobs** (13. 7.): MCP server pro největší CZ job portály — jobs.cz, prace.cz, bazos.cz. 5 nástrojů. Autor převádí svůj B2B job search workflow do opakovatelného nástroje.

3. **lichess-mcp-analyzer** (18. 7.): MCP server pro šachovou analytickou pipeline — Stockfish integration, coaching reports, game analysis. 8 nástrojů. Autor aplikuje MCP pattern na kompletně odlišnou doménu (šachy), čímž demonstruje **transferabilitu** svého přístupu.

4. **CI/CD deklarován v README** (do 8. 8.): Autor přidává "CI/CD & DevSecOps" a "Actions, CodeQL, Dependabot" do profilového README. CI/CD gap z v1.0 je zacelen.

5. **MCP jako diferenciace** (8. 8.): Live audit potvrzuje 3 veřejné MCP servery. Žádný jiný kandidát na B2B trhu nemá tuto kompetenci.

### Kognitivní pattern Fáze 6

```
Existující nástroj (lokální MCP) → Produktizace (3 servery) →
Transfer na odlišné domény (šachy, job search) →
Demonstrace transferability → Diferenciace na trhu
```

### Význam Fáze 6

Fáze 6 je **klíčová pro tržní positioning**:
- MCP = emerging trend v AI/ML ekosystému
- Autor má 3 produkční servery = důkaz, ne slib
- Transferabilita (CNC → LinkedIn → šachy → job search) = univerzální pattern
- Toto je nejsilnější diferenciace oproti konkurenci


## AI/IT Adopce: Trajektorie (aktualizováno)

### Fáze 0: Skeptický uživatel
- Používá Gemini, zažívá přepisování instrukcí
- **Vztah k AI:** Nedůvěřivý, ale zvídavý

### Fáze 1: Metodolog
- Vytváří golden rules pro LLM práci
- Testuje 5 modelů (DeepSeek, Gemini, Claude, Groq, ChatGPT)
- **Vztah k AI:** Instrumentální — AI je nástroj, ne autorita

### Fáze 2: Ko-pilot
- LLM používá jako párový programátor pro RE výzkum
- **Vztah k AI:** Kolaborativní — AI rozšiřuje kapacitu

### Fáze 3: Systematik
- Formalizuje AI workflow do epistemického rámce
- **Vztah k AI:** Řízený — AI pracuje v definovaných mantinelech

### Fáze 4: Architekt
- AI orchestruje cross-repo pipeline
- **Vztah k AI:** Hierarchický — člověk je architekt, AI je vykonavatel

### Fáze 5: Infrastrukturátor
- CI/CD napříč portfoliem, automated quality gates
- **Vztah k AI:** Systémový — AI je součástí pipeline, ne pilot

### Fáze 6: Produktizátor (NOVÁ)
- MCP servery jako veřejné produkty
- Agentic tooling pro odlišné domény
- **Vztah k AI:** Produktový — autor staví nástroje, které používají AI jako backend

### Trajektorie: AI Adoption Maturity Model

```
Nedůvěra → Dokumentace → Metodika → Orchestrace →
Epistemický rámec → Agentní workflow → Produktizace
```


## Celková statistika portfolia (aktualizováno)

### Commitová aktivita (chronologicky)

| Měsíc | Commity | Dominantní repo |
| - | - | - |
| Březen (24.–31.) | ~45 | kazuistiky\_llm\_sprint, rag\_indexer |
| Duben (1.–5.) | ~65 | kazuistiky\_llm\_sprint, outpost2026\_profile |
| Duben–červen (6.4.–6.6.) | 0 | Pauza (lokální RE výzkum) |
| Červen (7.–30.) | ~310 | vcf\_parser\_b2b (73), dxf\_integrace (48), web\_integrace\_systeq (75), Vcf-compiler (38) |
| Červenec (1.–31.) | ~120 | CI/CD, linkedin-mcp-custom, MCP-Jobs, lichess-mcp-analyzer |
| Srpen (1.–6.) | ~60 | Audit, aktualizace KB, Vcf-compiler pokračování |

### Trend: dokumentace → kód → infrastruktura → produkce

```
Březen:   ████████░░ 80% dokumentace, 20% prototypy
Duben:    ██████░░░░ 60% README, 40% koncepty
Červen:   ██░░░░░░░░ 20% docs, 80% produkční kód
Červenec:  ░░░░░░░░░░ 5% docs, 40% CI/CD, 55% MCP tooling
Srpen:    ░░░░░░░░░░ 30% audit/KB, 70% vývoj
```

### Vývoj test coverage

| Fáze | Testy | Metodika |
| - | - | - |
| F1 (březen) | 0 testů | Žádné |
| F2 (7.–11. 6.) | 0 testů | Pouze empirická validace |
| F3 early (11. 6.) | Golden master (10) | Baseline JSON diff |
| F3 mid (14. 6.) | 45 unit testů | Pytest + golden master |
| F3 late (15. 6.) | Smoke testy (6) | Deploy pipeline |
| F4 (27.–30. 6.) | 28 testů | Vcf-compiler pytest |
| F5 (1.–3. 7.) | 89+24+28+6 | CI matrix všechna repa |
| F6 (7.7.–6.8.) | 50+ (MCP servery) | MCP server testy |

### Vývoj architektonické zralosti

| Fáze | Architektura | Problém |
| - | - | - |
| F2 | 58 func / 0 tříd (dxf\_integrace) | Procedurální spaghetti |
| F2 | 19k LOC god class (vcf\_integrace) | Monolit, hardcoded values |
| F3 | 2 třídy (vcf\_parser\_b2b) | Částečná OOP |
| F4 | 6 tříd, 5 modulů (Vcf-compiler) | Plná OOP |
| F4 | pip balíček (vcf\_color\_service) | Modularizace |
| F5 | Cross-repo dispatch | Distribuovaná architektura |
| F6 | 3 MCP servery (FastMCP) | Agentic ekosystém |


## Kognitivní vzorce napříč portfoliem

### Pattern 1: Problém → Nástroj → Framework
1. Narazí na problém (např. ACI color divergence)
2. Napíše skript na detekci
3. Zobecní do pip balíčku
4. Vytvoří epistemický rámec

### Pattern 2: Session-based workflow
Každý commit je výsledek LLM session. Formát: `feat/fix/docs: popis`.

### Pattern 3: Transfer learning napříč doménami
- SNR kalibrace → z audio technologie do CNC detekce vad
- Golden master testování → z RE metodologie do software testingu
- Co/Proč/Jak/Efekt/Riziko → z epistemiky do CI/CD
- **MCP pattern** → z CNC nástrojů na LinkedIn/šachy/job search (NOVÉ)

### Pattern 4: Nízká tolerance k nejednoznačnosti
- Deterministický parser (cad2llm) — "0 % halucinací"
- Golden master testy — baseline JSON diff, žádné flaky testy
- Roundtrip validace — parser musí přečíst co napsal

### Pattern 5: Tooling jako produkt (NOVÝ)
- Lokální nástroj → Veřejný MCP server
- Jedna doména → Multi-doménový transfer
- Interní použití → B2B diferenciace


## Regresivní momenty

1. **God class anti-pattern** (vcf\_integrace): 19k LOC, 0 testů. **Regrese → korekce (archivace).**

2. **65denní pauza** (6. 4. – 6. 6.): **Mitigováno:** autor pracoval lokálně a vrátil se s 22 verzemi parseru.

3. **ACI color chaos**: 4× duplicitní nekonzistentní mapy. **Řešení:** dedikovaný pip balíček.

4. **Vcf-compiler není produkčně ready**: Modul D (35 000 Kč) zrušen z B2B nabídky. **Rozhodnutí:** kompilátor je výzkumný bonus.


## Závěr: Trajektorie za 135 dní

### Odkud kam

| Metrika | Bod 0 (24. 3.) | v1.0 (3. 7.) | v2.0 (6. 8.) |
| - | - | - | - |
| Repozitáře | 0 | 12 | 14+ |
| Commitů | 0 | ~494 | ~600+ |
| Testy | 0 | 147+ | 200+ |
| CI/CD | 0 | Matrix 3.10/3.11/3.12 | + deklarováno v README |
| Architektura | Žádná | Cross-repo dispatch | + 3 MCP servery |
| B2B | 0 | Nabídka 70 000 Kč | Čeká na rozhodnutí |
| AI modely | 1 (Gemini) | 5 | 5 + MCP tooling |
| Kvalita ověření | 0 | Golden master + roundtrip | + MCP jako důkaz |

### Nejvýznamnější milníky

| Datum | Milník | Dopad |
| - | - | - |
| 24. 3. | První git commit | Vstup do formalizace |
| 25. 3. | Gemini case study | Základ epistemiky |
| 7. 6. | DXF Geometry Indexer | První produkční kód |
| 9. 6. | VCF RE backlog (v1-v20) | Externalizace tacitní znalosti |
| 11. 6. | vcf\_parser\_b2b | Přechod z R&D do produktu |
| 14. 6. | DEFECT\_CATALOG V1 | Tacitní → explicitní pravidla |
| 15. 6. | GCP deployment | Cloud production |
| 25. 6. | B2B-Knowledge-Base | Centralizace knowledge |
| 27. 6. | Vcf-compiler | Syntéza (čtení + psaní) |
| 2. 7. | vcf\_color\_service | Single source of truth |
| 3. 7. | CI/CD Tier 1 | Infrastrukturní zralost |
| 7. 7. | linkedin-mcp-custom | První veřejný MCP server |
| 13. 7. | MCP-Jobs | Multi-doménový MCP |
| 18. 7. | lichess-mcp-analyzer | Transferabilita MCP patternu |
| 6. 8. | Portfolio audit v2.0 | Korekce KB artefaktů |

### Signatura autora

Ondřej Soušek není "člověk, který se naučil programovat". Je to **systémový stavitel**, který použil programování jako nástroj k externalizaci tacitních znalostí z CNC výroby do explicitního, testovatelného, nasaditelného kódu. Jeho trajektorie není "junior → senior" — je to **tacitní expert → formalizující architekt → produktizátor agentic toolingu**.

Rychlost adopce (135 dní od 0 do 14+ repů s 3 MCP servery) není anomálie — je to přímý důsledek:

1. Hluboké doménové znalosti (CNC/CAM)
2. Systematické metodologie (epistemický rámec)
3. Efektivního využití AI jako force multiplier
4. Vysoké tolerance k hloubce a nízké tolerance k šumu
5. **Schopnosti transferu patternů napříč doménami** (CNC → LinkedIn → šachy → job search)


*Report v2.0 vytvořen: 2026-08-06*
*Zdroje: Live GitHub API audit (14+ repozitářů, ~600+ commitů), .ai_state.json, CONTEXT_REPOS.md, KB/*, B2B-Knowledge-Base/*
*Předchůdce: R&D_evoluce_portfolia_03_2026-07_2026.md (v1.0, 2026-07-03)*
*Metodika: fázová analýza + kognitivní pattern matching + kvantitativní trendy + live GitHub audit*
