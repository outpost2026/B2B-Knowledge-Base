# META-ANALÝZA: Dev prostředí, workflow, epistemika a AI orchestrace

**Datum:** 2026-07-31 | **Autor:** opencode LLM agent (self-audit via cnc-tools MCP)
**Účel:** Podrobný report o metodologii, workflow, myšlení a epistemice vývojáře (Ondřej Soušek / SYSTEQ) na základě analýzy lokálních git repos v `_github`
**Typ:** meta-analýza / workspace audit | **EROI:** 9/10 | **Tags:** #meta-audit, #workflow, #epistemika, #orchestrace, #cross-llm, #self-audit

---

## 0. Executive summary (P>0.9)

1. **Epistemika je funkční architektura, ne deklarace.** Fyzikální realita je jediná metrika pravdy; kompresní realismus (hledání minimálního generátoru reality) řídí jak návrh kódu, tak rozhodování o práci samotné (EROI).
2. **Vývojář si instrumentuje vlastní vývoj.** `.ai_state.json`, pitevní kniha, mcp_audit.log, session state — proces je pozorován a dokumentován v reálném čase. Vzniká tak zpětná smyčka, kde metodologie je produktem analýzy vlastního procesu (dual-loop učení).
3. **Ground truth = fyzické prostředí, ne měření.** Klíčová meta-lesson z VCF RE: hex diff (kvantita rozdílů) selhal; GUI VCutWorks (kvalitativní chování) byl jediný spolehlivý orákulum. "Měřit ≠ rozumět."
4. **Cross-LLM 3. pohled je formalizovaný proces.** `CROSS_AUDIT_HANDOFF` → de novo audit konkurenčním LLM → verifikace nálezů proti kódu → `FIX_BALIK` → fresh test verifikace. Nález je hypotéza, nikdy fakt, dokud neprojde kódovou verifikací.
5. **Incidenty se transformují na pravidla.** Incident 16.06.2026 (destrukce systému agentem) → 10 sekcí epistemických pravidel → guardrails → permission matrix → PreToolUse hook. Každý incident generuje artefakt a pravidlo.
6. **Orchestrace je vrstvená a specializovaná.** 4 vlastní MCP servery (cnc-tools, linkedin, jobs, lichess), model routing per doménu (kalibrační matice), 20+ RE nástrojů, skills, guardrails, kontext files. AI není jeden nástroj, ale distribuovaná infrastruktura rolí.

---

## 1. Profil vývojáře (evidence: `.ai_guardrails.json`, workspace-guardrails skill)

| Atribut | Hodnota |
|---|---|
| Identita | Třída-3 systémový stavitel: fyzická realita + analytická architektura + epistemická rigor |
| Kognitivní styl | analytic + systematic; rychlý transfer learning (tacit → explicit) |
| Metrika pravdy | Fyzikální realita (napětí na baterii, kód v Cloud Run, proříznutí materiálu) |
| Hnací principy | Determininismus, closure, explicitní znalost; komprese reality (minimální algoritmus) |
| Senzitivity | Behaviorální nekonzistence, informační šum, unresolved loops |
| Původ | Radikální autodidaktismus: 0 Python/Git → B2B cloud produkt za ~90 dní přes LLM augmentaci |
| Osobní kontext | Off-grid Outpost 2026 (2500 Wp FV, 16 kWh LiFePO4) = anti-fragilní ekonomický buffer |

Klíčový rys: **nízká tolerance k šumu a ambiguu** se projevuje v každé vrstvě systému — od komunikačních pravidel (SNR, žádná sycophancy) přes technické guardrails až po architekturu (separace deterministických pravidel od ML).

---

## 2. Prostředí (fyzická vrstva)

### 2.1 Struktura `_github` (master dir)

- **21 git repozitářů**, 4 aktivní MCP servery, non-git adresáře (KB/, B2B/, VCF_files_moodpasta/, github_mirror/, GCP/)
- **Master git repo** (lokální, bez remote): sleduje root config + non-git adresáře, sub-repa jako gitlinky — historie + rollback kořenové konfigurace
- **Kontext files:** `AGENTS.md` (master pravidla), `CONTEXT_REPOS.md` (per-repo metadata + session timeline), `.ai_state.json` (master session state), `.ai_guardrails.json` (kognitivní profil), `mcp_audit.log` (instrumentace MCP)
- Organizační vrstva: `.ci/`, `.session/`, `.scripts/`

### 2.2 MCP infrastruktura (vlastní vývoj)

| Server | Repo | Nástroje | Doména |
|---|---|---|---|
| cnc-tools | mcp-local-server | 20 | filesystem, git, VCF analýza, RE pipeline, KB search, ACI lookup |
| linkedin-analyzer | linkedin-mcp-custom | 8 | LinkedIn saved jobs, Playwright |
| mcp-jobs | MCP-Jobs | 5 | CZ job portály, boolean AST, EROI scoring |
| lichess-analyzer | lichess-analyzer-mcp | 8 | Šachová analýza, Stockfish, pattern detekce |

MCP servery jsou produktem stejné metodiky jako veškerý kód: testy, pitevní kniha, audit log, README, guardrails, deterministická validace.

---

## 3. Pracovní workflow (cyklus session)

### 3.1 Kanonický cyklus (evidence: `AGENTS.md`, `B2B-KB/AGENTS.md`, commit vzory)

```
1. CHECKPOINT   Get-Location + git status → pokud ne-clean: "[checkpoint] pred:" commit
2. KONTEXT      načti AGENTS.md → CONTEXT_REPOS.md → relevantní modul → skill workspace-guardrails
3. ÚKOL         zpracování v povoleném modulu (zákaz cest mimo _github)
4. IMPLEMENTACE kód s testy, read-after-write verifikace každé FS operace
5. TESTOVÁNÍ    pytest, determinismus, fresh run
6. DOKUMENTACE  artefakt s hlavičkou + EROI + commit "[MODUL] akce: popis (EROI x/10)"
7. REVIEW       git status + git diff --stat; push jen na vyžádání
```

### 3.2 Fázová metodika komplexního úkolu (evidence: `kazuistiky_llm_sprint/metodika_prace_s_LLM.md`)

| Fáze | Název | Princip |
|---|---|---|
| 0 | Kotvení v realitě | explicitní popis výchozího stavu ("mám na stole"), co vím / nevím |
| 1 | Celek — rámcování | **Binární MVP kritérium** ("hotovo" = binární stav, ne kvalitativní) |
| 2 | Abstrakce — struktura | handoff JSON, BOM tabulky, strojově čitelná dokumentace |
| 3 | Dílčí zpřesnění | detailní návod pro jeden segment |
| 4 | Identifikace bottleneck | explicitní pojmenování blokátoru, separace fyzický/znalostní |
| 5 | Sumarizace — syntéza | rozhodovací podklad |
| 6 | Fyzická akce | objednávka, dokumentace |
| 7 | Verifikace a iterace | testovací protokol, zpětná vazba |

Protiklad: **vibe coding je odmítnut explicitně** ("zeptám se, zkopíruju, modlím se") — nahrazen kotvením, binárním MVP a RAW_FIRST (ověř surový vstup před kódem).

### 3.3 Session tracking (evidence: `.ai_state.json`, session_state)

Každá session má: id s datem, souhrn, stav, fázi, commit referenci. Verzovaná historie (Vcf-compiler `.ai_state.json` v1.13.0, 14+ sessions). Session_state napříč repos: 21 klíčů (2026-07-23 → 07-31). Kontinuita mezi session = handoff JSON + .ai_state + CONTEXT_REPOS timeline.

---

## 4. Metodologie a dokumentace

### 4.1 EROI jako unifying metrika

Každý artefakt i úkol se hodnotí poměrem hodnoty k nákladu:
- Doménová pravidla pro scoring jobs: domain 35%, tech 25%, role 20%, growth 10%, formal 5%, location 5%
- **EROI hodnocení dokumentů v KB** (7/10 → 10/10) — dokumentace sama je optimalizační objekt
- Pozoruhodné: EROI se aplikuje i na epistemiku (manifesty 10/10), tj. **i myšlení se měří EROI**

### 4.2 KB architektura (evidence: `B2B-Knowledge-Base`)

| Modul | Obsah | Artefaktů |
|---|---|---|
| 00_STRATEGIE | positioning, manifesty | 14 |
| 01_METODIKY | opakovatelné postupy | 20 |
| 02_ANALÝZY | audity, reporty, srovnání | 15 |
| 03_PROVOZ | emaily, kontrakty, business | 20 |
| 04_KNOWLEDGE_BASE | doménová znalost | 16 |
| 05_EPISTEMIKA | kognitivní rámce | 35 |

Každý artefakt: hlavička (Datum/Autor/Účel/EROI/Tags), INDEX.md registrace, commit template. **Znalost se neukládá ad hoc, ale podle modulů s povinnou metadátovou kostrou.** ~21 artefaktů vzniklo "iterační syntézou" — tj. dokumentace je samostatný vývojový cyklus.

### 4.3 Ground Truth artefakty

- MCP GROUND TRUTH agregovaný postmortem (GT-001…GT-077 + P1…P61 číslované poznatky)
- VCF/DXF GROUND TRUTH semantická kompilace (JSON)
- GT/pattern číslování s provenance tagy (cross-audit v4: konfabulace opraveny, transparentní statistiky)

Vzorec: **každá doména má verzovaný Ground Truth dokument, který je auditován, opravován a číslovaně rozšiřován.** Pseudo-relační znalostní model v Markdown.

---

## 5. Debugging metodologie (hlavní výstup: VCF RE)

### 5.1 Evoluce metod (evidence: `research_docs/REPORT_dev_phase_evolution.md`)

| Fáze | Metoda | Výsledek | Failure mode |
|---|---|---|---|
| 1-2 | Intuitivní implementace ("co vidím") | strukturně správné, sémanticky chybné soubory | přidání struktury zhoršilo chování (více ≠ lépe) |
| 3-4 | Hex diff analýza | 1055 diff regionů, 5 hypotéz | **kvantitativní ≠ kvalitativní** — 3740 B padding rozdílů utopilo 12 B kritických |
| 5-6 | **Binární search varianty** | 3 root causes identifikovány + opraveny | — |

### 5.2 Binární search variant (breakthrough, LLM navrhl)

- Generování VCF s inkrementálně přidanými strukturálními feature (varianty A-S)
- Testování v **reálném VCutWorks GUI** (orákulum = fyzické chování, ne hex diff)
- Patched varianty (vložení nativních dat do syntetického těla) — variant M definitivní důkaz
- "Variant G reduced diffs to 11 regions" = falešná hypotéza H6 — diffs klesly, ale trailer stále rozbitý

**Meta-lesson:** kvantitativní optimalizace metriky (hex diff) neměří kvalitativní cíl (loadability). Jediná správná metrika je chování cílového systému.

### 5.3 Pitevní kniha (evidence: `mcp-local-server/pitevni_kniha_mcp_v1.md`, 12+ záznamů)

Strukturovaná pitva každého incidentu:
```
Symptom → Příčina (fyzikální realita mechanismu) → Korekce (pravidlo) → Mitigace
```
Příklady záznamů: sekvenční bottleneck (Timeout → ThreadPoolExecutor), vnořené timeouty (fail fast < client timeout), chybějící `--no-optional-locks`, JSON corruption (defenzivní deserializace + auto-repair), absent duration metriky (povinný @auditable dekorátor), timeout guard wrapper, LLM blind path navigation (workspace discovery → tool_workspace_info), cp1250 encoding, pre-release Python deadlock, stderr pipe buffer deadlock.

Vzorec: **každý incident → pojmenovaný mechanismus (fyzikální podstata) → opakovatelné pravidlo (P#)**. Pravidla se číslují (P24, P25…) a jsou součástí KB.

### 5.4 RE Toolkit (evidence: `Vcf-compiler/dev_scripts/`, 14 nástrojů)

decode_subtype_bits, dissect_footers, dissect_layer_blocks, segment_geometry_stats, batch_correlate_dxf_vcf, vcf_binary_search, build_element_types_catalog, hex_diff_v2, run_all_re_tools (orchestrátor)…

**Vývojář si píše nástroje pro analýzu svého vlastního debugování** — RE analýza je automatizovaná pipeline nad korpusem 62 souborů, s RESULT_* výstupy a katalogem element typů.

---

## 6. Reakce na bugy a incidenty

### 6.1 Incident → pravidlo → guardrail pipeline

1. **16.06.2026:** agent smazal systémové soubory při "trimming" úkolu (Remove-Item -Recurse)
2. **Výstup:** `EPISTEMICKE-PRAVIDLA-AGENTNI-PRACE.md` — 10 sekcí: povolené/zakázané cesty, git pravidla, API klíče, read-after-write, destruktivní operace, PreToolUse hook, backup, nouzový postup, poučení z 4 incidentů (Gemini CLI, PocketOS, Claude rm -rf, NTFS junctions)
3. **Materializace:** permission matrix v opencode config, PreToolUse hook (blockuje rm -rf / Remove-Item -Recurse -Force / find -delete / git reset --hard), zákaz čtení .env
4. **Zpětná vazba do architektury:** FORBIDDEN_PATTERNS v MCP serveru, root .gitignore

### 6.2 Post-mortem kultura (blameless)

- MCP postmortem v5 (GT-066 → GT-070, P50-P54)
- Chyba = "nekalibrovaný datový bod nutný pro update vnitřního modelu" — ne ohrožení identity
- Retraction discipline: `[ANALYZY] update: retract API key finding (false positive)` — zjištění se korigují

### 6.3 Reakce na bugy z cross-auditu (evidence: FIX_BALIK)

Audit → fix → verifikace → test → dokumentace je kompletní smyčka: C1 dedup data loss → fuzzy_key rozšířen + logování; C2 silent errors → logger nahrazen; M1 malformed boolean → raise (fail-fast); 103 → **123 testů PASS**; determinismus ověřen fresh ETL runem (26 matched identické).

---

## 7. Cross-LLM 3. pohled (klíčová metodika)

### 7.1 Proces (evidence: `02_ANALÝZY/05_mcp_jobs/`)

```
1. CROSS_AUDIT_HANDOFF      LLM-ready kontext: architektura, metriky, ukázky kódu, audit prompt
2. DE NOVO AUDIT             konkurenční LLM (Claude, Grok/xAI) čte live remote, NEPŘEBÍRÁ teze
3. CROSS_AUDIT report        nálezy (ID | závažnost | umístění | dopad | jistota) + verdikt + top5 + chybějící testy
4. VERIFIKACE autorem        každý nález ✅/⚠️/❌ proti zdrojovému kódu v pracovní kopii
5. FIX_BALIK                 P0/P1 fixy + fresh test verifikace + determinismus check
6. KB zápis                  vstupní artefakty s EROI hodnocením
```

### 7.2 Klíčové principy 3. pohledu

- **De novo princip:** auditor dostane kontext k orientaci, ale žádný závěr nepřebírá jako pravdivý. "Známé gapy" jsou označeny jako autorovy hypotézy, ne fakta.
- **Verifikace jako samostatný krok:** nález je hypotéza do verifikace. Audit report má verifikační sloupce (✅/⚠️/❌).
- **Konvergentní validace:** dva nezávislé audity (Claude + Grok) konvergují → zvýšená jistota. Rozpory se řeší (Grokova chybná interpretace M4 byla vyvrácena kódem).
- **Fix není okamžitý:** nález → návrh fixu → samostatný rozhodovací krok autora (Phase 09+ pending list).
- **Antihalucinační rámec:** DATA-FABRICATION-001 — každé tvrzení o datech musí mít deterministický zdroj; jinak se neuvádí. "Halucinace není chyba pipeline — je chyba agentní disciplíny."

### 7.3 Třetí pohled v dalších doménách

- lichess-analyzer-mcp: CHESS_PATTERNS_AUDIT (W1-W10, CRITICAL W1 game_ids dropped), HALUCINACE_ROOT_CAUSE_ANALYSIS, kontext injekty pro audit
- B2B-KB: cross-audit v4 opravy konfabulací GT-063/065
- Vcf-compiler: DEV_REPORT pro LLM cross-validaci, kognitivní transfer RE analýza

---

## 8. Epistemika (myšlení)

### 8.1 Kompresní realismus (evidence: `05_EPISTEMIKA/00_kompresni_realismus/`)

- **Pravidlo 0:** "Složitost je parazit. Dokonalosti není dosaženo, když už není co přidat, ale když už nelze nic odebrat."
- Inteligence = minimální algoritmus vysvětlující realitu; akumulace proměnných = overfitting
- Rozpracováno do kognitivní neuro-architektury (Mozek jako geometrický procesor, thermodynamický upgrade) — esej + manifest

### 8.2 Epistemický kotvící rámec (evidence: `Epistemicky_kotvici_ramec_a_operacni_modus.md`)

- Model hrozby "The Rabbit Hole": pokušení detailu → explozí pravidel → statistický drift → ztráta kontextu
- Ohraničení LLM: **Architekt (autor) = fyzikální baseline, LLM = syntaktický kompilátor**. LLM nesmí přidávat logickou komplexitu bez příkazu; nesmí generovat fyzikální dogmata
- KROK 1: absolutní fyzikální determinismus → KROK 2: redukce dimenzionality (makro-desktriptory) → KROK 3: graceful degradation (pod 85% jistotu → FLAG: HUMAN_REVIEW) → KROK 4: sanitizace vstupů (nová proměnná musí snižovat entropii)
- **Invariant při kognitivním zahlcení:** "Tvou rolí není ošetřit všechny chyby. Je tvou rolí postavit síto s exaktní geometrií."

### 8.3 Kalibrační matice (evidence: `01_kalibracni_matice/`)

LLM routing per doménu (verze 3.0 "Autonomous System Era"):
- **Doména A (epistemika/analýza):** gpt-oss-120b (sokratovský puritán), Hermes 3 405B, Nemotron 3 Ultra (1M kontext, nulový drift), Llama 3.3 70B (red team), MiMo V2.5
- **Doména B (SWE/RE):** Qwen3-Coder 480B (geometrie/CAD), DeepSeek V4 Flash (exekuce, 1M kontext), Gemma 4 31B (multimodální), Nemotron 3 Super (QC validátor binárních vzorců)

Vzorec: **role-based routing — model se vybírá podle kognitivního profilu a domény, ne podle popularity.** Požadavky: potlačená servilita, sémantická rigidita, masivní kontext pro 150k+ seance.

---

## 9. AI orchestrace a syntéza

### 9.1 Architektura rolí

| Role | Prostředek | Odpovědnost |
|---|---|---|
| Architekt | vývojář | fyzikální baseline, ground truth, rozhodování, verifikace |
| Exekutor | DeepSeek V4 Flash (opencode) | strojové zpracování, testy, ETL |
| Oponent/red team | gpt-oss, Llama, Grok, Claude | de novo audity, falsifikace tezí |
| Oči | Gemma 4 | převod vizuální reality na kód |
| Validátor | Nemotron 3 Super | QC binárních vzorců, logické díry |

### 9.2 Syntéza nástrojů (self-instrumentation)

- **cnc-tools MCP** = exterioryzace vlastní metodiky do nástrojů (git status all, cross-repo search, KB search s tag lookup, VCF validate/analyze/diff, RE pipeline, ACI lookup, session state)
- **Vcf-compiler RE toolkit** = automatizace debugovací metodiky (14 nástrojů + orchestrátor)
- **Pitevní kniha** = znalostní báze incidentů MCP serverů (pitva = chirurgická analýza selhání)
- **Kontext files hierarchie** = AGENTS.md → KB/AGENTS.md → CONTEXT_REPOS.md → per-repo kontext → skill

### 9.3 Prompt caching / determinismus

- Kód optimalizován pro KV cache (prompt caching friendly), 150k+ token sessions
- `-X utf8`, PYTHONIOENCODING, sys.stdout.reconfigure — deterministické encoding mitigace
- Testovací data POUZE ASCII + Central European (cp1250 constraint)

---

## 10. Kritická reflexe (3. pohled na metodologii samotnou)

### 10.1 Silné stránky

1. **Self-instrumentace je ojedinělá.** Málokterý vývojář dokumentuje svůj vlastní proces s pitevní knihou, session state a verzovaným .ai_state. To umožňuje meta-analýzy právě tohoto typu.
2. **Verifikace nad důvěrou.** Tři nezávislé LLM (Claude, Grok, DeepSeek) + autor — žádný nález neprojde bez kódové verifikace. Antihalucinační disciplína je kodifikovaná (DATA-FABRICATION-001).
3. **Epistemika je provozní, ne dekorativní.** Kompresní realismus přímo řídí rozhodování (graceful degradation pod 85%, odmítnutí ML kde stačí fyzika, sanitizace vstupů).
4. **Incidenty se kapitálizují.** Guardrails a pravidla rostou s historií selhání; je doložená kauzalita incident → pravidlo.
5. **Determinismus nad heuristikou.** Fyzikální pravidla s Confidence 1.0 oddělena od statistických modelů s confidence score — 100% traceability.

### 10.2 Rizika / slabiny (P>0.7, hypotézy)

1. **Artefaktová inflace.** 90 artefaktů KB + desítky reportů může překročit bod klesajících výnosů — samotný management znalostí spotřebovává čas měřitelný EROI. Riziko: dokumentace dokumentace (meta-norová smyčka).
2. **Single-point-of-failure:** závislost na autoprofi lu a lokální infrastruktuře; repos bez remote (master repo) = riziko ztráty celé historie.
3. **Overfitting metodologie na RE doménu.** Kvalitní vzory (hex diff lekce, GUI oracle) jsou kalibrovány na binární RE; u rychlých web/IT úkolů (linkedin, jobs) může být proces zbytečně těžký — pozorovatelné v rozdílu hustoty dokumentace mezi repos (Vcf-compiler 20+ doc vs linkedin-mcp-custom ~6).
4. **LLM routing matice je subjektivní typologie** — bez kvantitativního měření (zřejmě existuje Empirická evaluace, ale matice je expertní odhad).
5. **Cross-audit závisí na externí frontiere modely** (Claude, Grok) — kvalita 3. pohledu je funkce kvality modelu + disciplíny autora při verifikaci.

---

## 11. Závěr (P>0.85)

Workflow vývojáře je **vrstvená epistemická architektura**, kde každá vrstva řeší specifickou kognitivní slabinu:

| Vrstva | Slabina, kterou řeší | Mechanismus |
|---|---|---|
| Guardrails + permissions | destruktivní agent | povolené cesty, PreToolUse hook, read-after-write |
| AGENTS.md chain | zapomnětlivost agenta | povinný kontext před každým úkolem |
| Kalibrační matice | generický LLM balast | role-based model routing |
| Kompresní realismus | overfitting / rabbit hole | Pravidlo 0, redukce dimenzionality |
| Cross-LLM 3. pohled | slepá místa autorova modelu | de novo audity konkurenčními modely + kódová verifikace |
| Pitevní kniha + postmortem | opakování chyb | incident → mechanismus → pravidlo |
| .ai_state / session state | ztráta kontinuity | verzovaný stav napříč session |
| EROI scoring | alokace času | unifying metrika hodnoty vs nákladu |

**Ústřední insight:** vývojář nevyužívá AI jako generátor kódu, ale jako **distribuovaný kognitivní exoskelet s explicitně oddělenými rolemi** (exekutor, oponent, validátor, oči). Zároveň sám sobě staví nástroje pro pozorování vlastního vývoje — čímž metodologie práce s AI se stává produktem analyzovaným stejnými epistemickými nástroji jako kód. Tato **sebe-reference + verifikace + komprese** je funkční definice vysoce SNR vývojového workflow.

---

## Odkazy

- Master pravidla: `_github/AGENTS.md`
- Kognitivní profil: `_github/.ai_guardrails.json`
- Epistemická pravidla: `B2B-KB/05_EPISTEMIKA/02_agentni_pravidla/EPISTEMICKE-PRAVIDLA-AGENTNI-PRACE.md`
- Kotvící rámec: `B2B-KB/05_EPISTEMIKA/02_agentni_pravidla/Epistemicky_kotvici_ramec_a_operacni_modus.md`
- Kalibrační matice: `B2B-KB/05_EPISTEMIKA/01_kalibracni_matice/kalibracni_matice.json`
- RE evoluce: `Vcf-compiler/research_docs/REPORT_dev_phase_evolution.md`
- Pitevní kniha: `mcp-local-server/pitevni_kniha_mcp_v1.md`
- Cross-audit MCP-Jobs: `B2B-KB/02_ANALÝZY/05_mcp_jobs/` (HANDOFF + v1 + FIX_BALIK)
- Metodika 8 fází: `kazuistiky_llm_sprint/metodika_prace_s_LLM.md`
- Repo přehled: `_github/CONTEXT_REPOS.md`
