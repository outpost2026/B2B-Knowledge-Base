# MCP v praxi — průvodce každodenním workflow pro solo dev

**Datum:** 2026-07-05 | **Autor:** outpost2026
**Verze:** v1.0 | **Navazuje na:** MCP_komplexni_analyza_a_strategie_v1.md
**Účel:** Praktický návod, jak integrovat MCP nástroje do každodenního vývojářského workflow — s konkrétními příklady, rozhodovacím frameworkem a falsifikací.

---

## Obsah

1. [Proč další MCP dokument?](#1-proč-další-mcp-dokument)
2. [MCP způsob vs. manuální způsob — paradigmatický posun](#2-mcp-způsob-vs-manuální-způsob)
3. [Každodenní scénáře — předtím a potom](#3-každodenní-scénáře)
4. [Tool recepty pro běžné úkoly](#4-tool-recepty-pro-běžné-úkoly)
5. [Workflow integrace — krok za krokem](#5-workflow-integrace)
6. [Prospektivní část — vývoj MCP a proč na něm záleží](#6-prospektivní-část)
7. [Falsifikace — kdy MCP NENÍ řešení](#7-falsifikace)
8. [Rozhodovací framework — MCP vs. manuální vs. skript](#8-rozhodovací-framework)
9. [Závěr a doporučení](#9-závěr)

---

## 1. Proč další MCP dokument?

Dokument `MCP_komplexni_analyza_a_strategie_v1.md` pokrývá **co je MCP, jak ho postavit a jaké má bezpečnostní aspekty**.

Tento dokument pokrývá **jak MCP používat v praxi** — ne jako teorii, ale jako každodenní nástroj. Cílová otázka není "co je MCP", ale **"jak vypadá můj den, když ho používám"**.

Rozdíl:
| | Analýza | Tento průvodce |
|---|---|---|
| Otázka | Co je MCP a proč? | Jak MCP používat teď? |
| Formát | Architektura, strategie | Scénáře, příkazy, workflow |
| Publikum | Rozhodování o adopci | Každodenní používání |
| Výstup | Plán | Návod |

---

## 2. MCP způsob vs. manuální způsob

### 2.1 Princip: od příkazů k záměrům

**Manuální způsob:** Dev zadává příkazy do terminálu, čte výstup, interpretuje, rozhoduje se.

```
"zkontroluju git status" → cd repo → git status → čtu výstup → "změnil se soubor X"
"podívám se na diff" → git diff → čtu → "aha, přidal jsem import"
"zkontroluju testy" → pytest → čekám → "prošly"
```

**MCP způsob:** Dev vyjádří záměr, LLM (s MCP nástroji) ho vykoná a rovnou interpretuje.

```
"co je v repu?" → LLM zavolá tool_git_status → tool_git_diff → tool_run_tests → shrne
```

Rozdíl není v tom, že by LLM dělal něco jiného. Rozdíl je v **eliminaci context-switchingu** — dev nemusí přepínat mezi editorem, terminálem, prohlížečem a dokumentací. Vše je v jednom dialogu.

### 2.2 Srovnání v metrikách

| Aspekt | Manuální | MCP | Rozdíl |
|---|---|---|---|
| Počet přepnutí kontextu | ~5-7 / min | ~0-1 / min | Eliminace |
| Čas od záměru k informaci | 15-30s | 2-5s | 3-6× |
| Zachycení do audit logu | Ruční | Automatické | ✅ |
| Opakovatelnost | Musíš si pamatovat | Tool description stačí | ✅ |
| Učení nového člena | Předat zkušenost | Tool descriptions + prompty | Strukturované |

### 2.3 Kde je hranice?

MCP nenahrazuje:
- **Rozhodování** — LLM navrhuje, dev schvaluje
- **Kreativní návrh** — architekturu, volbu knihovny, strategii
- **Bezpečnostní rozhodnutí** — co commitnout, jaké credentials použít

MCP nahrazuje:
- **Vyhledávání informací** — "kde je definice X?", "co je v tom souboru?"
- **Stav systému** — "co je změněné?", "prošly testy?", "jaký je log?"
- **Opakované dotazy** — "jaká je ACI barva pro červenou?", "co říká KB o X?"

---

## 3. Každodenní scénáře

### Scénář 1: Ranní checkpoint

**Cíl:** Zjistit stav všech repozitářů, co se dělo od poslední session, načíst kontext.

**Manuálně (6-8 minut):**
```powershell
cd _github
# pro každý repo:
cd repo && git status && git log -3 --oneline && cd ..
cd B2B-Knowledge-Base
# hledat v dokumentech...
```

**MCP (30 sekund):**
```
tool_git_status_all()                    → přehled všech 13 repozitářů
tool_session_state(action="status")      → poslední uložený stav
tool_kb_search("current status session") → co je v KB
```

**Marginal analysis:** 6-8 min → 30s = 12-16× zrychlení. Při 1× denně = ~6 min/den úspora. Za měsíc = ~2 hodiny.

---

### Scénář 2: Iterace kód → test → fix

**Cíl:** Upravit kód, spustit testy, opravit chybu, zkontrolovat změny.

**Manuálně:**
1. Editovat soubor v editoru
2. Přepnout do terminálu: `uv run pytest`
3. Číst error — přepnout zpět do editoru
4. Opravit — přepnout do terminálu — znovu spustit
5. `git diff` pro kontrolu

**MCP:**
1. LLM edituje soubor přes `tool_write_file`
2. LLM zavolá `tool_run_tests` (jakmile bude implementovaný)
3. LLM čte error, rovnou edituje
4. `tool_git_diff` pro kontrolu před commitem

**Klíčový rozdíl:** Žádné alt-tab, žádné přepínání oken. Vše v jednom proudu.

---

### Scénář 3: Výzkum / debugging s KB lookupem

**Cíl:** Narazíš na problém, potřebuješ zjistit, co o něm víš.

**Manuálně:**
1. Vzpomenout si, jestli o tom není něco v KB
2. Otevřít souborový manažer
3. Prohledávat MD soubory
4. Případně hledat fulltext

**MCP:**
```
tool_kb_search("VCF writer element count @92")  → rovnou najde relevantní dokumenty
tool_search_files("*.md", "research_docs/")      → doplňkové hledání
```

---

### Scénář 4: Před commitem — bezpečnostní checkpoint

**Cíl:** Zkontrolovat, že se necommitnou secrets, že změny dávají smysl.

**Manuálně:**
1. `git status` — zkontrolovat, co se mění
2. `git diff` — projet očima každý řádek
3. Zkontrolovat, jestli v diffu není `.env` nebo credentials

**MCP:**
```
tool_git_status("repo")            → co je změněné
tool_git_diff("repo")              → diff k review
tool_cross_repo_search("GITHUB_PAT") → ověří, že token není v žádném repu
```

---

### Scénář 5: Nový úkol / explorace neznámého kódu

**Cíl:** Potřebuješ pochopit, jak funguje část kódové báze, kterou jsi psal před týdnem.

**Manuálně:**
1. Otevřít soubor, číst
2. Hledat, kde se volá funkce X
3. Sledovat volání napříč soubory

**MCP:**
```
tool_cross_repo_search("def write")      → najde definice napříč všemi repy
tool_cross_repo_search("class VcfWriter") → všechny výskyty třídy
tool_read_file("repo/path/to/file.py")   → rovnou zobrazí obsah
```

---

### Scénář 6: Session handoff / předání kontextu

**Cíl:** Ukončit session a předat kontext příští session.

**Manuálně:** Zapisovat do poznámek, co bylo uděláno, co zbývá.

**MCP:**
```
tool_session_state("save", "last_task", "Debug VCF element count")
tool_session_state("save", "next_step", "Implement rate limiter")
```

Příští session:
```
tool_session_state("status") → vidíš, kde jsi skončil
```

---

## 4. Tool recepty pro běžné úkoly

### Recept 1: "Ukaž mi přehled"
```
tool_git_status_all()
tool_session_state(action="status")
```

### Recept 2: "Co se změnilo a mám to committnout?"
```
tool_git_status("Vcf-compiler")
tool_git_diff("Vcf-compiler", staged=False)
```

### Recept 3: "Najdi definici funkce napříč projekty"
```
tool_cross_repo_search("def validate_vcf")
```

### Recept 4: "Zjisti ACI barvu a tool parametry"
```
tool_aci_lookup(1)          # červená
tool_aci_lookup(42)         # custom
```

### Recept 5: "Ověř VCF soubor po úpravě"
```
tool_validate_vcf("output.VCF")
tool_vcf_diff("original.VCF", "output.VCF")
```

### Recept 6: "Začni novou session — plný start"
```
tool_session_state(action="status")
tool_git_status_all()
tool_kb_search("current status")
tool_cross_repo_search("TODO|FIXME|HACK")
```

---

## 5. Workflow integrace

### 5.1 První den — adoptovat jeden tool

Nejmenší možný krok: **přestat používat `ls` a `cat` v terminálu.**

Když potřebuješ vědět, co je v adresáři, místo:
```powershell
ls _github/Vcf-compiler/dev_scripts/
```
řekni:
```
"co je v dev_scripts?"
```

LLM sám zavolá `tool_list_directory`. Nemusíš nic vysvětlovat — tool description to popisuje.

**Cíl dne 1:** tool_list_directory, tool_read_file, tool_search_files nahradí ruční ls/cat/find.

### 5.2 Týden 1 — přidat git tooly

Když kontroluješ stav:
```
"zkontroluj git status v Vcf-compileru"
```

Místo:
```powershell
cd _github/Vcf-compiler && git status
```

**Cíl týdne 1:** tool_git_status, tool_git_diff, tool_git_log nahradí ruční git commandy.

### 5.3 Týden 2 — přidat doménové tooly

Když analyzuješ VCF:
```
"analyzuj tenhle VCF soubor a řekni mi, co je v něm špatně"
```

Místo:
```powershell
python analyze_vcf.py file.VCF
```

**Cíl týdne 2:** tool_validate_vcf, tool_vcf_analyze, tool_aci_lookup, tool_kb_search.

### 5.4 Měsíc 1 — nativní MCP workflow

MCP je první volba, ne alternativa. Automatické:
- Na začátku session: status + session state + KB kontext
- Během práce: cross-repo search + git diff před commitem
- Na konci session: uložit stav do session_state

---

## 6. Prospektivní část

### 6.1 Kam MCP směřuje (2026–2027)

MCP není "další nástroj" — je to **infrastrukturní standard**, stejně jako HTTP nebo REST. Jeho význam roste s každým novým MCP klientem:

| Období | Milník | Dopad pro solo dev |
|---|---|---|
| Q3 2026 | Stateless MCP release candidate | Jednodušší škálování, nižší režie |
| Q4 2026 | Auth standardizace (OAuth 2.1 pro MCP) | Bezpečné remote servery |
| Q1 2027 | Lokální modely 90%+ parity | Plně lokální AI stack bez API klíčů |
| Q2 2027 | Managed MCP marketplace | One-click instalace serverů |
| Late 2027 | MCP 2.0 (auth, streaming, multi-modal) | Enterprise-grade infrastruktura |

### 6.2 Proč je MCP pro solo dev kritický

Solo dev má **omezenou kapacitu** — čas, pozornost, energie. MCP umožňuje:

1. **Eliminovat context-switching** — každé přepnutí stojí ~23 minut k obnovení focusu
2. **Kodifikovat know-how** — tool descriptions jsou živá dokumentace
3. **Multi-client leverage** — jeden MCP server = všichni klienti (opencode, Claude, VS Code, Cursor)
4. **Zpětná vazba v reálném čase** — audit log, error tracking, cache stats

### 6.3 Dif oproti běžné AI literate populaci

| Úroveň | Chování | Nástroje |
|---|---|---|
| **Konzument (90%)** | Chat, promptování, copy-paste | ChatGPT/Claude web |
| **Power user (~9%)** | Vlastní workflow, API, agenti | opencode, API klíče, skripty |
| **Stavitel (~1%)** | Vlastní MCP servery, infrastruktura | **MCP server + opencode** |

**Aktuální pozice:** Na přechodu z ~9% do ~1%. MCP server je kodifikovaný nástroj, který tuto pozici institucionalizuje.

### 6.4 Síťový efekt MCP

Každý nový tool přidává hodnotu všem existujícím klientům.
Každý nový klient přidává hodnotu všem existujícím toolům.

```
Hodnota MCP ekosystému = nástroje × klienti
```

To není aditivní (n + k), ale multiplikativní (n × k). Každý nový nástroj zvyšuje hodnotu všech klientů a naopak.

---

## 7. Falsifikace

### 7.1 Kdy MCP NENÍ řešení

**Teze:** "MCP je univerzální nástroj, který by měl být použit pro všechno."

**Falsifikace:** MCP má měřitelné overheady a specifické situace, kde je kontraproduktivní.

| Situace | Proč MCP nefunguje | Co místo toho |
|---|---|---|
| **Sub-100ms operace** (např. čtení 1 souboru) | JSON-RPC overhead > samotná operace | Přímé CLI nebo skript |
| **Hromadné operace** (např. git status na 13 rep) | Sériové volání 13× tool_git_status je pomalejší než `git status_all` | Dávkový skript |
| **Jednorázové ad-hoc příkazy** | Tool musíš definovat, otestovat, dokumentovat | Prosté CLI |
| **Když nevíš, co chceš** | MCP vyžaduje definovaný interface | Explorativní programování |
| **Když potřebuješ 100% determinismus** | LLM se může rozhodnout tool nepoužít | Skript/Makefile |
| **Prototypování rychle se měnícího API** | Každá změna toolu = restart serveru | Jupyter / skript |

### 7.2 Overengineering risk

**Riziko:** "Napíšu MCP tool pro všechno, včetně věcí, které by byly jednodušší jako skript."

**Prevence:** Před napsáním každého nového toolu si odpověz:
1. Použiju tenhle tool víc než 3×? (Ne → skript)
2. Potřebuju, aby ho používalo víc klientů? (Ne → skript/CLI)
3. Je operace read-only a bezpečnostně riziková? (Ne → skript)
4. Vyžaduje doménové know-how, které není v promptu? (Ano → MCP tool)

### 7.3 Srovnání: MCP tool vs. skript vs. CLI

| Kriterium | MCP tool | Python skript | CLI příkaz |
|---|---|---|---|
| Čas napsat | 30-60 min | 5-15 min | 0 min |
| Čas použít | 2-5 s | 10-30 s | 1-5 s |
| Multi-klient | ✅ | ❌ | ❌ |
| Audit log | ✅ Automaticky | ❌ | ❌ |
| Input validation | ✅ | ❌ (ručně) | ❌ |
| Deterministický | ❌ (volá LLM) | ✅ | ✅ |
| Udržovatelnost | Střední | Nízká | Nízká |

### 7.4 EROI hranice (z analýzy)

MCP tool se vyplatí, když:
- **EROI ≥ 8/10** — tool použitý > 5×, ušetří > 30 min/týden
- **EROI 5-7/10** — tool použitý 2-5×, spíš edukační hodnota
- **EROI < 5/10** — raději skript nebo CLI

---

## 8. Rozhodovací framework

### 8.1 Flowchart: Jak se rozhodnout

```
Potřebuju provést operaci?
│
├─ Je to jednorázová věc? → CLI / ručně
│
├─ Budu to dělat >3×?
│   │
│   ├─ Je to čistě lokální, bez doménového kontextu? → Python skript
│   │
│   └─ Potřebuji to zpřístupnit LLM / více klientům?
│       │
│       ├─ Je to read-only a bezpečnostně citlivé? → MCP tool (povolené cesty, audit)
│       │
│       ├─ Vyžaduje to doménové know-how (VCF, ACI, KB)?
│       │   → MCP tool (tool description = dokumentace)
│       │
│       └─ Je to write operace?
│           → MCP tool (pouze se zárukou bezpečnosti, .gitignore, forbidden patterns)
│
└─ Budu to dělat >50×? → Zvaž samostatný balíček / pip modul
```

### 8.2 Template pro rozhodování o novém toolu

| Otázka | Odpověď | Akce |
|---|---|---|
| Frekvence použití | >5×/týden, >5×/měsíc, <5× | >5×/měsíc → tool |
| Počet klientů | Jen opencode, více klientů | Více → tool |
| Doménová znalost | Žádná, střední, vysoká | Střední+ → tool |
| Bezpečnostní riziko | Nízké, střední, vysoké | Střední+ → tool (s audit) |
| Write operace | Ano/Ne | Ano → tool (s validací) |

### 8.3 Příklady rozhodnutí z praxe

| Operace | Verdikt | Zdůvodnění |
|---|---|---|
| `git status` | ✅ MCP (tool_git_status) | Read-only, audit, používáno >50×/týden |
| `git commit` | ❌ NE | Write, bezpečnostní riziko, musí schválit dev |
| ACI lookup | ✅ MCP (tool_aci_lookup) | Doménová znalost, cache, používáno denně |
| Vytvořit ZIP archiv | ❌ Skript | Jednorázově, žádné doménové know-how |
| Validace VCF | ✅ MCP (tool_validate_vcf) | Doménová, ověřuje tool parametry |
| Hledání v KB | ✅ MCP (tool_kb_search) | Fulltext, cache, >10×/týden |
| Smazat soubor | ❌ NE | Write, destruktivní, bezpečnostní riziko |
| Cross-repo grep | ✅ MCP (tool_cross_repo_search) | Časté, read-only, .gitignore respekt |

---

## 9. Závěr

### 9.1 Klíčová sdělení

1. **MCP není nástroj — je to infrastruktura.** Jako HTTP nebo REST — jednou napsaný server slouží všem klientům.

2. **Adopce po vrstvách.** Nezačínej všemi 17 tools najednou. Začni filesystemem, přidej git, pak doménové tooly.

3. **MCP first, ne MCP only.** Některé věci zůstanou rychlejší v CLI. Framework ti pomůže rozhodnout se.

4. **Každý tool je investice.** Tool description = dokumentace. Audit log = zpětná vazba. Cache = výkon.

5. **Falsifikace není slabina.** Vědět, kdy MCP NEPOUŽÍT, je stejně důležité jako vědět, jak ho použít.

### 9.2 Akční kroky

| Krok | Co | Kdy |
|---|---|---|
| 1 | Restartovat opencode (nové tooly jsou k dispozici) | Teď |
| 2 | Zkusit ranní checkpoint přes MCP (scénář 1) | Zítra ráno |
| 3 | Při příštím debug použít KB search místo manuálního hledání | Při nejbližší příležitosti |
| 4 | Před commitem vždy zavolat `tool_git_diff` | Ode dneška |
| 5 | Na konci každé session uložit stav do `tool_session_state` | Ode dneška |
| 6 | Za týden zhodnotit: které tooly ušetřily nejvíc času | Za týden |

### 9.3 Měření úspěchu

Po měsíci používání:

| Metrika | Cíl |
|---|---|
| Počet tool callů / session | >30 (průměr) |
| Ušetřený čas / den | >30 min |
| Počet session s uloženým stavem | >80 % |
| Čas od záměru k informaci | <5 s (vs. 15-30s dříve) |
| Subjektivní snížení frustrace | "Méně přepínání, víc flow" |

---

*Tento dokument je živý. Aktualizace dle nových zkušeností a toolů.*
